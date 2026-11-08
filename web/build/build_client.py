#!/usr/bin/env python3
"""Real client compilation, diagnostic link and accepted-pack packaging."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
from compile_probe import native_outputs, safe_path
from preflight import ROOT


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(paths):
    return {str(p.relative_to(ROOT)): sha(p) for p in sorted(paths) if p.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4, choices=range(1, 9))
    parser.add_argument('--link-check', action='store_true', help='Diagnostic JS/Wasm link without any preload; not the final game bundle')
    parser.add_argument('--pack-sha256', help='Exact MAIN-accepted original manifest SHA-256, required for final packaging')
    parser.add_argument('--pack-authorization', type=Path, help='Lead decision recording that accepted pack identity')
    parser.add_argument('--evidence-dir', default='web/build/generated/t031', help='Owned attempt directory beneath web/build/generated')
    args = parser.parse_args()
    config_path = ROOT / 'web/build/client-config.json'
    cfg = json.loads(config_path.read_text())
    sdk = Path(cfg['sdk_root'])
    compiler = sdk / 'upstream/emscripten'
    output = safe_path(args.evidence_dir)
    assert output.is_relative_to(ROOT / 'web/build/generated'), 'Evidence must stay in generated'
    output.mkdir(parents=True, exist_ok=True)
    cache = safe_path('web/build/.cache')
    temp = safe_path('web/build/generated/tmp')
    temp.mkdir(exist_ok=True)
    env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'EMSDK': str(sdk), 'EMSDK_PYTHON': sys.executable,
           'EM_CONFIG': str(sdk / '.emscripten'), 'EM_CACHE': str(cache), 'EM_PORTS': str(cache / 'ports'),
           'NODE_COMPILE_CACHE': str(cache / 'node_compile_cache'), 'EMCC_TEMP_DIR': str(temp),
           'TMPDIR': str(temp), 'PYTHONDONTWRITEBYTECODE': '1'}
    # Pin the installed PNG recipe against the inspected source before compiler use.
    inspected_png = Path('/private/tmp/outbreak-web-sdk-inspection/compiler/emscripten-777e6e5db7b4990bcaeb1b9998ed642cc84e6629/tools/ports/libpng.py')
    assert sha(compiler / 'tools/ports/libpng.py') == sha(inspected_png)
    assert (compiler / 'emscripten-revision.txt').read_text().strip() == cfg['compiler_revision']
    assert (compiler / 'emscripten-version.txt').read_text().strip().strip('"') == cfg['sdk_version']
    makefile = ROOT / 'source/src/Makefile'
    block = re.search(r'CLIENT_OBJS=\s*\\\n(.*?)\n\nCLIENT_PCH=', makefile.read_text(), re.S).group(1)
    cpp = [ROOT / f'source/src/{name}.cpp' for name in re.findall(r'([A-Za-z0-9_/]+)\.o', block)]
    enet = [ROOT / f'source/enet/{name}.c' for name in ('callbacks', 'compress', 'host', 'list', 'packet', 'peer', 'protocol', 'unix')]
    assert len(cpp) == 53 and len(enet) == 8 and all(p.is_file() for p in cpp + enet)
    shared = [config_path, Path(__file__), ROOT / 'web/build/shell.html', makefile]
    shared += list((ROOT / 'source/src').rglob('*.h')) + list((ROOT / 'source/enet/include').rglob('*.h')) + list((ROOT / 'web/runtime').rglob('*.h'))
    shared += [p for p in (ROOT / 'web/build/notices').rglob('*') if p.is_file()]
    initial = snapshot(shared + cpp + enet)
    native_before = native_outputs()
    old_path = output / 'result.json'
    old = json.loads(old_path.read_text()) if old_path.is_file() else {}
    old_runs = {r['source']: r for r in old.get('compiles', [])}
    report = {'ticket': cfg['ticket'], 'scope': 'full_client_compile_link_not_runtime', 'started_utc': datetime.now(timezone.utc).isoformat(),
              'environment': env, 'sdk_version': cfg['sdk_version'], 'compiler_revision': cfg['compiler_revision'],
              'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'config': cfg, 'source_inventory': [str(p.relative_to(ROOT)) for p in cpp + enet], 'inputs_before': initial,
              'libpng_recipe_sha256': sha(inspected_png), 'compiles': [], 'link': None,
              'claims': {'browser_runtime': False, 'renderer': False, 'multiplayer': False},
              'omissions': ['offline-map profile only', 'audio and player/weapon models omitted by runtime profile',
                            'browser mapshot/minimap texture readback unavailable under D008', 'no browser multiplayer'],
              'compatibility_profile': 'safe legacy GL emulation; existing direct model drawing under D008; native display lists retained'}
    version = subprocess.run([str(compiler / 'em++'), '--version'], cwd=ROOT, env=env, capture_output=True, text=True)
    report['compiler_version'] = {'exit_code': version.returncode, 'output': version.stdout + version.stderr}
    assert version.returncode == 0 and f"7.0.0 ({cfg['compiler_revision']})" in version.stdout + version.stderr
    shared_hashes = snapshot(shared)

    def compile_one(source):
        rel = str(source.relative_to(ROOT))
        obj = safe_path(str((output / 'objects' / (rel + '.o')).relative_to(ROOT)))
        obj.parent.mkdir(parents=True, exist_ok=True)
        log = safe_path(str((output / 'logs' / (rel + '.log')).relative_to(ROOT)))
        log.parent.mkdir(parents=True, exist_ok=True)
        command = [str(compiler / ('em++' if source.suffix == '.cpp' else 'emcc'))]
        command += cfg['common_cxx'] + cfg['ports'] if source.suffix == '.cpp' else cfg['common_c']
        command += ['-I' + str(ROOT / p) for p in ('source/src', 'source/src/bot', 'source/enet/include')]
        command += ['-c', str(source), '-o', str(obj)]
        before = sha(source)
        previous = old_runs.get(rel, {})
        reused = (previous.get('status') == 'PASS' and previous.get('command') == command and previous.get('source_sha256_after') == before
                  and old.get('shared_hashes') == shared_hashes and obj.is_file() and previous.get('object_sha256') == sha(obj))
        if reused:
            item = dict(previous)
            item['reused_verified_object'] = True
            return item
        obj.unlink(missing_ok=True)
        done = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        log.write_text(done.stdout)
        wasm = obj.is_file() and obj.read_bytes()[:8] == b'\x00asm\x01\x00\x00\x00'
        after = sha(source)
        print(f'{rel}: exit {done.returncode}', flush=True)
        return {'source': rel, 'command': command, 'exit_code': done.returncode, 'source_sha256_before': before,
                'source_sha256_after': after, 'object': str(obj.relative_to(ROOT)), 'log': str(log.relative_to(ROOT)),
                'object_sha256': sha(obj) if obj.is_file() else None, 'wasm_object': wasm,
                'status': 'PASS' if done.returncode == 0 and wasm and before == after else 'FAIL', 'reused_verified_object': False}

    # Warm the newly authorized PNG port once before parallel independent compiles.
    report['compiles'].append(compile_one(cpp[0]))
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        report['compiles'] += list(pool.map(compile_one, cpp[1:] + enet))
    report['shared_hashes'] = shared_hashes
    report['inputs_after'] = snapshot(shared + cpp + enet)
    report['stale_inputs'] = [p for p in initial if initial[p] != report['inputs_after'].get(p)]
    # The SDK derives suffixes from the first dot in a URL basename, so the
    # versioned PNG URL is cached as libpng.6.59.tar.gz, not libpng.tar.gz.
    ports = json.loads((ROOT / 'web/build/sdk-inspection/sources-and-artifacts.json').read_text())['ports']
    ports += [{'name': 'libpng', 'version_or_tag': '1.6.59',
               'url': 'https://storage.googleapis.com/webassembly/emscripten-ports/libpng-1.6.59.tar.gz',
               'expected_sha512': cfg['libpng_sha512'], 'recipe_sha256': sha(inspected_png)}]
    report['port_integrity'] = []
    for port in ports:
        archives = [p for p in (cache / 'ports').glob(port['name'] + '.*') if p.is_file() and p.name.endswith(('.zip', '.tar.gz'))]
        assert len(archives) == 1, (port['name'], archives)
        recipe = compiler / 'tools/ports' / (port['name'] + '.py')
        actual_hash = hashlib.sha512(archives[0].read_bytes()).hexdigest()
        recipe_hash = sha(recipe)
        assert actual_hash == port['expected_sha512'] and recipe_hash == port['recipe_sha256']
        report['port_integrity'].append({'name': port['name'], 'version_or_tag': port['version_or_tag'], 'url': port['url'],
                                         'archive': str(archives[0].relative_to(ROOT)), 'sha512': actual_hash,
                                         'recipe_sha256': recipe_hash, 'status': 'PASS'})
    success = all(r['status'] == 'PASS' for r in report['compiles']) and not report['stale_inputs']
    if success and (args.link_check or args.pack_sha256):
        pack_inputs = {}
        if args.pack_sha256:
            manifest = ROOT / 'web/assets/original/manifest.json'
            assert args.pack_authorization and args.pack_authorization.is_file(), 'Accepted pack decision required'
            assert sha(manifest) == args.pack_sha256, 'Pack manifest differs from accepted identity'
            pack_root = ROOT / 'web/assets/original/pack-root'
            entries = json.loads(manifest.read_text())['entries']
            expected = set()
            for entry in entries:
                path = pack_root / entry['path']
                assert not Path(entry['path']).is_absolute() and '..' not in Path(entry['path']).parts
                assert path.resolve().is_relative_to(pack_root.resolve()) and not path.is_symlink()
                assert all(not p.is_symlink() for p in path.parents if p.is_relative_to(pack_root))
                assert entry['original'] is True and entry['license'] == 'MIT'
                assert path.is_file() and path.stat().st_size == entry['bytes'] and sha(path) == entry['sha256'], entry['path']
                assert entry['virtual_path'] == '/outbreak/' + entry['path']
                expected.add(entry['path'])
            actual = {str(p.relative_to(pack_root)) for p in pack_root.rglob('*') if p.is_file()}
            assert len(expected) == len(entries) == 41 and expected == actual, 'Pack membership differs'
            assert sum(e['bytes'] for e in entries) == 87897, 'Accepted pack raw size differs'
            pack_inputs = snapshot([manifest] + [p for p in pack_root.rglob('*') if p.is_file()])
            report['pack_validation'] = {'manifest_sha256': args.pack_sha256, 'file_count': len(entries),
                                         'raw_bytes': 87897, 'exact_membership_and_hashes': 'PASS'}
            report['pack_authorization'] = {'path': str(args.pack_authorization), 'sha256': sha(args.pack_authorization)}
            report['pack_inputs'] = pack_inputs
            dest = safe_path('web/build/out/index.html')
        else:
            dest = safe_path(str((output / 'link-check/client.js').relative_to(ROOT)))
        dest.parent.mkdir(parents=True, exist_ok=True)
        for suffix in ('.html', '.js', '.wasm', '.data'):
            sibling = safe_path(str(dest.with_suffix(suffix).relative_to(ROOT)))
            if sibling.is_file():
                sibling.unlink()
        if args.pack_sha256:
            safe_path('web/build/out/build-metadata.json').unlink(missing_ok=True)
        command = [str(compiler / 'em++')] + [str(ROOT / r['object']) for r in report['compiles']] + cfg['ports'] + cfg['link']
        if args.pack_sha256:
            command += ['--shell-file', str(ROOT / 'web/build/shell.html'), '--preload-file', str(pack_root) + '@/outbreak']
        command += ['-o', str(dest)]
        done = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        (output / 'link.log').write_text(done.stdout)
        stale_pack = any(not (ROOT / p).is_file() or sha(ROOT / p) != h for p, h in pack_inputs.items())
        if args.pack_sha256:
            stale_pack |= actual != {str(p.relative_to(pack_root)) for p in pack_root.rglob('*') if p.is_file()}
        if args.pack_sha256 and done.returncode == 0 and not stale_pack:
            for notice in (ROOT / 'web/build/notices').rglob('*'):
                if notice.is_file():
                    copied = safe_path('web/build/out/notices/' + str(notice.relative_to(ROOT / 'web/build/notices')))
                    copied.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(notice, copied)
        report['link'] = {'command': command, 'exit_code': done.returncode, 'log': str((output / 'link.log').relative_to(ROOT)),
                          'preload_requested': bool(args.pack_sha256),
                          'packaged': bool(args.pack_sha256) and done.returncode == 0 and not stale_pack,
                          'pack_changed_during_link': stale_pack,
                          'outputs': snapshot([p for p in dest.parent.rglob('*') if p.is_file()])}
        success = done.returncode == 0 and not stale_pack
    report['inputs_final'] = snapshot(shared + cpp + enet)
    report['stale_inputs'] = [p for p in initial if initial[p] != report['inputs_final'].get(p)]
    success &= not report['stale_inputs']
    report['native_outputs_unchanged'] = native_before == native_outputs()
    report['status'] = 'PASS' if success and report['native_outputs_unchanged'] else 'FAIL'
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    if success and args.pack_sha256 and report['link']:
        report['bundle_id'] = hashlib.sha256(json.dumps({'inputs': report['inputs_final'], 'pack': report['pack_inputs'],
                                                       'config': cfg}, sort_keys=True).encode()).hexdigest()
        metadata = safe_path('web/build/out/build-metadata.json')
        metadata.write_text(json.dumps(report, indent=2) + '\n')
        report['bundle_metadata_sha256'] = sha(metadata)
    old_path.write_text(json.dumps(report, indent=2) + '\n')
    print(f"{report['status']}: {sum(r['status'] == 'PASS' for r in report['compiles'])}/61 target sources; link={report['link'] and report['link']['exit_code']}")
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
