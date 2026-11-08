#!/usr/bin/env python3
"""T066 shared strict fixed-profile browser recipe/verifier; preparation is read-only.

Only main() --plan-only may write observation plans; execute() needs separate MAIN
pins/release. No SDK/compiler/Node/tool version probing occurs during preparation.
"""
import argparse
import hashlib
import importlib.util
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True

class Shell(HTMLParser):

    def __init__(self):
        super().__init__()
        self.canvas = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'canvas':
            self.canvas.append(values.get('id'))
        if tag == 'script' and 'src' in values:
            self.scripts.append(values['src'])

class Recipe:
    NODE_SHA = '27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1'
    ALIAS_DECISION = 'notes/decisions/D044-approved-sdk-aliases.json'
    ALIAS_SHA = '7b78d4f0ce74b2e1f24459429409ba9e0350e52902b3b600f07c936b5684154f'
    MINIFIER_DECISION = 'notes/decisions/D046-html-minifier-alias.json'
    MINIFIER_SHA = '3ff2a582732afcda98ef07a43384146f93dc39b22c84dbe16e91ca7ca702f01c'
    PNG_RECIPE = '3dc04566b3e646400f7b180ff3cc5d539146008e3b416bcb3e2e34fe53189911'
    MAGIC = b'\0asm\1\0\0\0'
    ARTIFACTS = ('index.html', 'index.js', 'index.wasm', 'index.data')
    subprocess = subprocess  # Tests forbid the actual subprocess boundary.

    def __init__(self, profile):
        self.require(profile in ('audio', 'network'), 'only fixed audio/network recipes exist')
        self.profile = profile
        self.ROOT = Path(__file__).resolve().parents[2]
        self.HERE = self.ROOT / 'web/build'
        self.CONFIG = self.HERE / (profile + '-config.json')
        self.TICKET = 'T060 revision 3.2' if profile == 'audio' else 'T066 revision4.0'
        self.OUTPUT = profile + '-out'
        self.ATTEMPT_ROOT = 'web/build/generated/' + ('t060' if profile == 'audio' else 't066')
        self.SHELL = 'shell.html' if profile == 'audio' else 'network-shell.html'
        self.RELEASE = 'EXPLICIT_' + profile.upper() + '_BUILD_EXECUTION'
        self.PACK_SHA = ('7def7d8da8a9567f8023f5675f6fa9369edcd930f635794c9c95ca106868e283' if profile == 'audio'
                         else 'c9ecfa62f7e4ca7111a9d3a23a9c97b906d11399d32f6f312463c6697a3359d7')
        self.PACK_BYTES = 388764 if profile == 'audio' else 388791
        self.OMISSIONS = (['Embedded offline simulation; not multiplayer',
                          'Original proof audio requested; actual playback/audibility NOT RUN',
                          'Model files packaged; source does not preload models; actual rendering NOT RUN',
                          'No gameplay sound mapping; mapshot/minimap readback unavailable under D008'] if profile == 'audio' else
                         ['NETWORK_CLIENT recipe; actual native game join/spawn and two-client runtime NOT RUN',
                          'Legacy client-reported movement/hits; not authoritative Outbreak gameplay or accepted P0/MVP',
                          'Original proof audio/model preload source present; actual playback/rendering NOT RUN',
                          'No gameplay sound mapping; mapshot/minimap readback unavailable under D008'])

    def require(self, condition, message):
        if not condition:
            raise ValueError(message)

    def canonical(self, value):
        return json.dumps(value, sort_keys=True, indent=2) + '\n'

    def sha(self, path, algorithm='sha256'):
        h = hashlib.new(algorithm)
        with Path(path).open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                h.update(block)
        return h.hexdigest()

    def clean(self, path):
        """Absolute lexical path, no traversal or symlink in any existing component."""
        path = Path(path)
        self.require(path.is_absolute() and '..' not in path.parts, 'absolute confined path required')
        self.require(not any((p.is_symlink() for p in (path, *path.parents))), 'symlink input/output: ' + str(path))
        return path

    def repo(self, name):
        path = Path(name)
        self.require(not path.is_absolute() and '..' not in path.parts and (str(path) == name), 'non-normalized repository path')
        return self.clean(self.ROOT / path)

    def files(self, directory):
        directory = self.clean(directory)
        if not directory.exists():
            return []
        result = []
        for parent, dirs, names in os.walk(directory, followlinks=False):
            for name in dirs + names:
                self.clean(Path(parent) / name)
            result.extend((Path(parent) / name for name in names))
        return sorted(result)

    def snapshot(self, paths):
        result = {}
        for path in sorted(set(map(Path, paths))):
            self.clean(path)
            self.require(path.is_file(), 'missing input: ' + str(path))
            result[str(path)] = self.sha(path)
        return result

    def output_fingerprints(self, root, expected=None):
        root = self.clean(Path(root))
        actual = {name: self.sha(self.clean(root / name)) for name in self.ARTIFACTS}
        if expected is not None:
            self.require(actual == expected, 'output fingerprint mismatch')
        return actual

    def config(self):
        cfg = json.loads(self.CONFIG.read_text())
        base = json.loads((self.HERE / 'client-config.json').read_text())
        identities = dict(ticket='T060 revision 3.2', profile='OFFLINE_MAP original-audio-media', manifest='web/assets/audio-profile/manifest.json', pack_root='web/assets/audio-profile/pack-root', output='web/build/audio-out', attempt_root='web/build/generated/t060')
        if self.profile == 'network':
            identities = dict(ticket=self.TICKET, profile='NETWORK_CLIENT original-network-media',
                              manifest='web/assets/network-profile/manifest.json', pack_root='web/assets/network-profile/pack-root',
                              output='web/build/network-out', attempt_root=self.ATTEMPT_ROOT,
                              js_library='web/transport/enet_websocket.js')
            base['common_cxx'] += ['-DOUTBREAK_NETWORK_CLIENT']
            base['common_c'] += ['-std=gnu11', '-fsigned-char', '-DOUTBREAK_NETWORK_CLIENT']
            shell = (self.HERE / 'shell.html').read_bytes()
            self.require(self.sha(self.clean(self.HERE / 'shell.html')) == '8772af0952c619d85ea9ae502d364d7af9117ea162caf0dab1ac1a635667a8de', 'accepted T056 shell changed')
            self.require((self.HERE / self.SHELL).read_bytes() == shell.replace(
                b'Outbreak \xe2\x80\x94 offline map proof', b'Outbreak \xe2\x80\x94 network scene and join proof', 1), 'network shell changed hooks/flow')
        self.require(cfg == dict(base, **identities), self.profile + ' config changed accepted flags/SDK or paths')
        return cfg

    def units(self):
        text = self.repo('source/src/Makefile').read_text()
        block = re.search('CLIENT_OBJS=\\s*\\\\\\n(.*?)\\n\\nCLIENT_PCH=', text, re.S)
        self.require(block is not None, 'CLIENT_OBJS not recognized')
        cpp = ['source/src/' + name + '.cpp' for name in re.findall('([A-Za-z0-9_/]+)\\.o', block[1])]
        c = ['source/enet/' + name + '.c' for name in ('callbacks', 'compress', 'host', 'list', 'packet', 'peer', 'protocol', 'unix')]
        if self.profile == 'network':
            c = c[:-1] + ['web/transport/enet_websocket.c']
        self.require(len(cpp) == 53 and len(set(cpp)) == 53, 'expected 53 genuine CLIENT_OBJS')
        self.require(len(set(cpp + c)) == 61 and all((self.repo(name).is_file() for name in cpp + c)), 'missing/duplicate translation unit')
        return cpp + c

    def pack(self, cfg):
        self.require(cfg == self.config(), 'profile/config mismatch')
        manifest_path = self.repo(cfg['manifest'])
        self.require(self.sha(manifest_path) == self.PACK_SHA, 'profile manifest mismatch')
        manifest = json.loads(manifest_path.read_text())
        for name, expected in {'web/assets/audio-profile/check_profile.py': '1045add62a22392787272756b48e990dc6b2354fd6cfb16e1e626b1faab103ab', 'web/assets/audio-profile/build_profile.py': '60f40d0b29344402196ad066a0bf9257e0f8dbdc96f54a24e294e7d0a535a782', 'web/assets/media-profile/assemble.py': 'b0c96708226e30386af646f028f006309017934bacbd0ad8ddebdf58f475fc8d'}.items():
            self.require(self.sha(self.repo(name)) == expected, 'inspected profile helper changed')
        if self.profile == 'network':
            self.network_backend()
            pins = {'build_network_profile.py': '342fd0dfc170f0ca5d2bfabac0c7d49b9d6d46481f019376952601148047d409',
                    'map_format.py': '9d52664cd5ed8fc451bb7b60a50efd40ceae7e1924fe7e0721a4d9f2e915385e',
                    'validate_network_profile.py': '31d15e6d46b43fd06a99ebea2831099f67c9460f2b7850da55ccbf754c9689f0'}
            helper_root = self.ROOT / 'web/assets/network-profile'
            for name, pin in pins.items():
                self.require(self.sha(self.clean(helper_root / name)) == pin, 'inspected T064 helper changed')
            sys.path.insert(0, str(helper_root))
            from validate_network_profile import validate
            report = json.loads((helper_root / 'anchors.json').read_text())
            result = validate(self.repo(cfg['pack_root']), manifest, report)
        else:
            sys.path.insert(0, str(self.ROOT / 'web/assets/audio-profile'))
            from check_profile import validate
            result = validate(self.repo(cfg['pack_root']), manifest)
        self.require(result['files'] == 79 and result['raw_bytes'] == self.PACK_BYTES, 'profile closure mismatch')
        return (manifest, result)

    def network_backend(self):
        pins = {'web/transport/enet_websocket.c': '5d386d859e7178e9777de130ac399da26a015f51b78f78d4bcaee86ecfbac053',
                'web/transport/enet_websocket.js': 'ce706fd7b8e2ce583d15483ef122b35f91bc48d14f58af6495994c69c6180d34',
                'web/transport/enet_ws_bridge.h': 'c1905aef1a57b0f599d2e176d90c1e8786fbfea5caf9ec12a8c36f3f7840b832',
                'source/src/browsernet.h': '0a7f522f26d6a29c1956e15a69d601e481790d69091071622f9db73c759e6b44'}
        for name, pin in pins.items():
            self.require(self.sha(self.repo(name)) == pin, 'accepted backend changed: ' + name)
        return pins

    def repository_inputs(self, cfg):
        paths = [self.CONFIG, Path(__file__), self.HERE / 'verify_audio_bundle.py', self.HERE / 'client-config.json', self.HERE / 'build_client.py', self.HERE / 'verify_client_bundle.py', self.HERE / 'compile_probe.py', self.HERE / 'preflight.py', self.HERE / 'shell.html', self.ROOT / 'source/src/Makefile', self.HERE / 'sdk-inspection/sources-and-artifacts.json']
        paths += [self.HERE / 'build_audio_client.py']
        if self.profile == 'network':
            paths += [self.HERE / name for name in ('build_network_client.py', 'verify_network_bundle.py', 'network-shell.html', 'audio-config.json')]
            paths += [self.repo(name) for name in self.network_backend()]
            helper = self.ROOT / 'web/assets/network-profile'
            paths += [helper / name for name in ('manifest.json', 'anchors.json', 'map_format.py', 'build_network_profile.py', 'validate_network_profile.py')]
            paths += [self.ROOT / 'web/assets/original/validate_pack.py']
            paths += self.files(helper / 'pack-root')
            paths += [p for p in self.files(self.ROOT / 'web/transport') if p.suffix in ('.h', '.hpp')]
        for name in ('source/src', 'source/enet', 'web/runtime'):
            paths += [p for p in self.files(self.repo(name)) if p.suffix in ('.cpp', '.c', '.h', '.hpp', '.inc', '.inl')]
        paths += self.files(self.HERE / 'notices')
        for name in ('original', 'audio', 'models', 'media-profile', 'audio-profile'):
            base = self.ROOT / 'web/assets' / name
            paths += [base / 'manifest.json'] + self.files(base / 'pack-root')
        paths += [self.ROOT / 'web/assets/audio-profile/check_profile.py', self.ROOT / 'web/assets/audio-profile/build_profile.py', self.ROOT / 'web/assets/media-profile/assemble.py']
        return self.snapshot(paths)

    def ports(self, cfg):
        inspected = json.loads((self.HERE / 'sdk-inspection/sources-and-artifacts.json').read_text())['ports']
        specs = inspected + [dict(name='libpng', expected_sha512=cfg['libpng_sha512'], recipe_sha256=self.PNG_RECIPE)]
        self.require([s['name'] for s in specs] == ['sdl2', 'sdl2_image', 'zlib', 'vorbis', 'ogg', 'libpng'], 'six ports required')
        result = []
        for spec in specs:
            recipe = self.clean(Path(cfg['sdk_root']) / 'upstream/emscripten/tools/ports' / (spec['name'] + '.py'))
            self.require(self.sha(recipe) == spec['recipe_sha256'], 'port recipe mismatch')
            candidates = [p for p in self.files(self.HERE / '.cache/ports') if p.parent == self.HERE / '.cache/ports' and p.name.startswith(spec['name'] + '.') and (p.name.endswith('.zip') or p.name.endswith('.tar.gz'))]
            self.require(len(candidates) == 1, 'exact retained archive required: ' + spec['name'])
            archive = candidates[0]
            self.require(self.sha(archive, 'sha512') == spec['expected_sha512'], 'port archive mismatch')
            result.append(dict(name=spec['name'], recipe=str(recipe), recipe_sha256=spec['recipe_sha256'], archive=str(archive), archive_sha256=self.sha(archive), archive_sha512=spec['expected_sha512']))
        return result

    def validate_aliases(self, root, records):
        """Only decision-declared aliases traverse links; every hop stays in its root."""
        root = self.clean(Path(root))
        aliases = {r['path']: r for r in records}
        self.require(len(aliases) == len(records), 'duplicate alias')
        for record in records:
            path = Path(record['path'])
            self.require(path.is_relative_to(root) and path.is_symlink(), 'unknown/non-confined alias')
            self.clean(path.parent)
            current = path
            visited = set()
            while current.is_symlink():
                self.require(str(current) in aliases and str(current) not in visited, 'unknown/cyclic alias chain')
                visited.add(str(current))
                text = os.readlink(current)
                self.require(text == aliases[str(current)]['link_text'], 'alias text mismatch')
                self.require(not Path(text).is_absolute(), 'absolute alias escape')
                current = Path(os.path.normpath(current.parent / text))
                self.require(current.is_relative_to(root), 'alias escape')
                self.clean(current.parent)
            self.require(str(current) == record['resolved_path'], 'alias target mismatch')
            self.clean(current)
            self.require(current.is_file() and self.sha(current) == record['resolved_sha256'], 'alias target hash mismatch')
        return records

    def alias_policy(self):
        aliases, decisions = ([], {})
        for name, digest, count in ((self.ALIAS_DECISION, self.ALIAS_SHA, 4), (self.MINIFIER_DECISION, self.MINIFIER_SHA, 1)):
            path = self.repo(name)
            self.require(self.sha(path) == digest, 'alias decision changed: ' + name)
            doc = json.loads(path.read_text())
            self.require(doc['schema_version'] == 1 and len(doc['aliases']) == count, 'alias decision schema')
            records = self.validate_aliases(doc['root'], doc['aliases'])
            supporting = doc.get('inspected_supporting_files', {})
            for source, expected in supporting.items():
                self.require(self.sha(self.clean(Path(source))) == expected, 'alias supporting identity changed: ' + source)
            aliases.extend(records)
            decisions[name] = dict(sha256=digest, root=doc['root'], aliases=records, supporting_files=supporting)
        self.require(len({r['path'] for r in aliases}) == 5, 'exact five approved aliases required')
        return (aliases, decisions)

    def tools(self, cfg):
        sdk = self.clean(Path(cfg['sdk_root']))
        compiler = sdk / 'upstream/emscripten'
        self.require((compiler / 'emscripten-version.txt').read_text().strip().strip('"') == cfg['sdk_version'], 'SDK version file')
        self.require((compiler / 'emscripten-revision.txt').read_text().strip() == cfg['compiler_revision'], 'compiler revision file')
        node = sdk / 'node/24.19.0_64bit/bin/node'
        self.require(self.sha(self.clean(node)) == self.NODE_SHA, 'Node 24.19.0 identity')
        aliases, _ = self.alias_policy()
        paths = [sdk / '.emscripten', node, self.clean(Path(sys.executable).resolve())]
        paths += [p for p in (sdk / 'upstream/bin').iterdir() if p.is_file() and (not p.is_symlink())]
        paths += [Path(a['resolved_path']) for a in aliases]
        for base in ('lib', 'include', 'share'):
            paths += self.files(sdk / 'upstream' / base)
        for parent, dirs, names in os.walk(self.clean(compiler), followlinks=False):
            dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', '.bin')]
            for name in dirs + names:
                self.clean(Path(parent) / name)
            paths += [Path(parent) / name for name in names if not name.endswith('.pyc')]
        return self.snapshot(paths)

    def preservation(self):
        paths = self.files(self.HERE / 'out') + self.files(self.ROOT / 'web/server/out')
        paths += self.files(self.HERE / 'audio-out') + self.files(self.HERE / 'network-out')
        paths += self.files(self.HERE / '.cache')
        for parent, _, names in os.walk(self.ROOT / 'source', followlinks=False):
            for name in names:
                p = Path(parent) / name
                if p.suffix in ('.o', '.lo', '.a', '.gch', '.pch') or p.name in ('ac_client', 'ac_server', 'ac_master'):
                    paths.append(self.clean(p))
        return self.snapshot(paths)

    def observe(self, strict=True):
        cfg = self.config()
        manifest, checked = self.pack(cfg)
        aliases, decisions = self.alias_policy()
        observed = dict(inputs=self.repository_inputs(cfg), units=self.units(), ports=self.ports(cfg), preservation=self.preservation(), pack=checked, tool_errors=[], aliases=aliases, alias_decisions=decisions)
        for name, decision in decisions.items():
            observed['inputs'][str(self.repo(name))] = decision['sha256']
        try:
            observed['inputs'].update(self.tools(cfg))
        except ValueError as error:
            if strict:
                raise
            observed['tool_errors'].append(str(error))
        return (cfg, manifest, observed)

    def attempt_path(self, name):
        path = self.repo(name)
        base = self.ROOT / self.ATTEMPT_ROOT
        self.require(path.parent == base and re.fullmatch('attempt-[A-Za-z0-9_-]+', path.name), 'new direct profile attempt required')
        return path

    def authorize(self, path, expected_sha, observed, attempt, completed=False):
        self.require(path is not None and expected_sha is not None, 'future MAIN pins path AND SHA256 required')
        path = self.clean(Path(path))
        self.require(path.parent == self.ROOT / 'notes/decisions' and path.suffix == '.json', 'pins must be MAIN notes/decisions/*.json')
        self.require(re.fullmatch('[0-9a-f]{64}', expected_sha) is not None and self.sha(path) == expected_sha, 'pins document digest mismatch')
        doc = json.loads(path.read_text())
        keys = {'schema', 'authority', 'status', 'execution_release', 'ticket', 'attempt', 'inputs', 'preservation', 'units', 'ports', 'aliases', 'alias_decisions'}
        if self.profile == 'network':
            keys.add('profile')
            self.require(doc.get('profile') == 'NETWORK_CLIENT original-network-media', 'pins profile mismatch')
        self.require(set(doc) == keys, 'pins schema keys')
        self.require(doc['schema'] == 1 and doc['authority'] == 'MAIN' and (doc['status'] == 'ACCEPTED'), 'unaccepted pins')
        self.require(doc['ticket'] == self.TICKET and doc['execution_release'] == self.RELEASE, 'separate execution release missing')
        self.require(doc['attempt'] == str(attempt.relative_to(self.ROOT)), 'attempt not authorized')
        for key in ('inputs', 'preservation', 'units', 'ports', 'aliases', 'alias_decisions'):
            self.require(doc[key] == observed[key], 'missing/extra/changed ' + key)
        self.require(not observed['tool_errors'], 'unverified tool inventory')
        if not completed:
            self.require(not attempt.exists(), 'attempt already exists; history immutable')
            self.require(not self.clean(self.HERE / self.OUTPUT).exists(), 'profile output already exists; refusing replacement')
        return doc

    def environment(self, cfg, attempt):
        return dict(PATH='/usr/bin:/bin:/usr/sbin:/sbin', EMSDK=cfg['sdk_root'], EMSDK_PYTHON=str(Path(sys.executable).resolve()), EM_CONFIG=cfg['sdk_root'] + '/.emscripten', EM_CACHE=str(attempt / 'cache'), EM_PORTS=str(attempt / 'cache/ports'), EM_FROZEN_CACHE='1', NODE_COMPILE_CACHE=str(attempt / 'node-cache'), EMCC_TEMP_DIR=str(attempt / 'tmp'), TMPDIR=str(attempt / 'tmp'), PYTHONDONTWRITEBYTECODE='1')

    def commands(self, cfg, inventory, attempt):
        self.require(cfg == self.config(), 'profile flags/library/output configuration mismatch')
        self.require(inventory == self.units(), 'socket/source inventory mismatch')
        if self.profile == 'network':
            self.network_backend()
        compiler = Path(cfg['sdk_root']) / 'upstream/emscripten'
        compiles = []
        for index, source in enumerate(inventory):
            cpp = source.endswith('.cpp')
            obj = attempt / 'objects' / (str(index).zfill(2) + '.o')
            command = [str(compiler / ('em++' if cpp else 'emcc'))]
            command += cfg['common_cxx'] + cfg['ports'] if cpp else cfg['common_c']
            includes = ['source/src', 'source/src/bot', 'source/enet/include']
            if self.profile == 'network':
                includes.append('web/transport')
            command += ['-I' + str(self.ROOT / p) for p in includes]
            command += ['-c', str(self.ROOT / source), '-o', str(obj)]
            compiles.append(dict(source=source, object=str(obj), command=command))
        link = [str(compiler / 'em++')] + [c['object'] for c in compiles] + cfg['ports'] + cfg['link']
        if self.profile == 'network':
            link += ['--js-library', str(self.repo(cfg['js_library']))]
        link += ['--shell-file', str(self.HERE / self.SHELL), '--preload-file', str(self.ROOT / cfg['pack_root']) + '@/outbreak', '-o', str(attempt / 'bundle/index.html')]
        node = cfg['sdk_root'] + '/node/24.19.0_64bit/bin/node'
        return (compiles, link, [node, '--check', str(attempt / 'bundle/index.js')])

    def wasm_command(self, cfg, attempt):
        return [cfg['sdk_root'] + '/node/24.19.0_64bit/bin/node', '-e', "if(!WebAssembly.validate(require('fs').readFileSync(process.argv[1])))process.exit(1)", str(attempt / 'bundle/index.wasm')]

    def unchanged(self, observed):
        _, _, current = self.observe()
        for key in ('inputs', 'preservation', 'units', 'ports', 'aliases', 'alias_decisions'):
            self.require(current[key] == observed[key], 'concurrent change to ' + key)

    def run_command(self, command, env, log):
        completed = subprocess.run(command, cwd=self.ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log.write_bytes(completed.stdout)
        self.require(completed.returncode == 0, 'command failed; see ' + str(log))
        return dict(command=command, exit_code=completed.returncode, log=str(log), log_sha256=self.sha(log))

    def execute(self, cfg, manifest, observed, pins, pins_path, pins_sha, attempt):
        self.require(self.authorize(pins_path, pins_sha, observed, attempt) == pins, 'execution pins changed')
        self.unchanged(observed)
        self.require(self.sha(pins_path) == pins_sha, 'pins changed before execution')
        attempt.mkdir(parents=True, exist_ok=False)
        for name in ('objects', 'bundle', 'logs', 'tmp', 'node-cache'):
            (attempt / name).mkdir()
        shutil.copytree(self.HERE / '.cache', attempt / 'cache')
        self.unchanged(observed)
        env = self.environment(cfg, attempt)
        compiles, link, syntax = self.commands(cfg, observed['units'], attempt)
        report = dict(schema=1, status='INCOMPLETE', ticket=cfg['ticket'], inputs=observed['inputs'], preservation=observed['preservation'], units=observed['units'], ports=observed['ports'], aliases=observed['aliases'], alias_decisions=observed['alias_decisions'], environment=env, pins_path=str(pins_path), pins_sha256=pins_sha, attempt=str(attempt.relative_to(self.ROOT)), omissions=self.OMISSIONS, compiles=[], object_reuse=False, claims=dict(browser_runtime=False, audio_playback=False, model_rendering=False, multiplayer=False))
        if self.profile == 'network':
            report['profile'] = cfg['profile']
        report_path = attempt / 'result.json'
        try:
            for index, unit in enumerate(compiles):
                outcome = self.run_command(unit['command'], env, attempt / 'logs' / (str(index) + '.log'))
                obj = Path(unit['object'])
                self.require(obj.read_bytes()[:8] == self.MAGIC, 'invalid Wasm object')
                report['compiles'].append(dict(unit, **outcome, status='PASS', object_sha256=self.sha(obj)))
            self.unchanged(observed)
            for unit in report['compiles']:
                self.require(self.sha(Path(unit['object'])) == unit['object_sha256'], 'object changed before link')
            report['link'] = self.run_command(link, env, attempt / 'logs/link.log')
            self.unchanged(observed)
            report['syntax'] = self.run_command(syntax, env, attempt / 'logs/js-syntax.log')
            report['wasm_validation'] = self.run_command(self.wasm_command(cfg, attempt), env, attempt / 'logs/wasm-validation.log')
            report['preload_validation'] = self.validate_payload(attempt / 'bundle', manifest)
            shutil.copytree(self.HERE / 'notices', attempt / 'bundle/notices')
            self.require(self.snapshot(self.files(attempt / 'bundle/notices')) == {str(attempt / 'bundle/notices' / p.relative_to(self.HERE / 'notices')): self.sha(p) for p in self.files(self.HERE / 'notices')}, 'notices differ')
            self.unchanged(observed)
            self.require(self.sha(pins_path) == pins_sha, 'pins changed during execution')
            report['outputs'] = self.output_fingerprints(attempt / 'bundle')
            report['notices'] = {str(p.relative_to(attempt / 'bundle')): self.sha(p) for p in self.files(attempt / 'bundle/notices')}
            report['stable_inventory'] = True
            report['status'] = 'LINKED_NOT_BROWSER_VERIFIED'
            identity = dict(inputs=report['inputs'], outputs=report['outputs'], pins_sha256=pins_sha, commands=[u['command'] for u in compiles] + [link, syntax, self.wasm_command(cfg, attempt)], environment=env)
            report['bundle_id'] = hashlib.sha256(self.canonical(identity).encode()).hexdigest()
            metadata = attempt / 'bundle/build-metadata.json'
            metadata.write_text(self.canonical(report))
            report['metadata_sha256'] = self.sha(metadata)
            report_path.write_text(self.canonical(report))
            self.verify(attempt / 'bundle', attempt, pins_path, pins_sha)
            self.unchanged(observed)
            target = self.clean(self.HERE / self.OUTPUT)
            self.require(not target.exists(), 'publication target appeared; history preserved')
            stage = attempt / 'publication'
            shutil.copytree(attempt / 'bundle', stage)
            self.require(self.snapshot(self.files(stage)) == {str(stage / p.relative_to(attempt / 'bundle')): self.sha(p) for p in self.files(attempt / 'bundle')}, 'publication copy mismatch')
            self.unchanged(observed)
            os.rename(stage, target)
        except Exception as error:
            report['status'] = 'FAIL'
            report['error'] = str(error)
            report_path.write_text(self.canonical(report))
            raise

    def main(self, argv=None):
        parser = argparse.ArgumentParser(description=__doc__)
        modes = parser.add_mutually_exclusive_group(required=True)
        modes.add_argument('--plan-only', action='store_true')
        modes.add_argument('--execute', action='store_true', help='future separately released MAIN execution only')
        parser.add_argument('--attempt', required=True, help=self.ATTEMPT_ROOT + '/attempt-NEW')
        parser.add_argument('--pins', type=Path)
        parser.add_argument('--pins-sha256')
        parser.add_argument('--plan-name', default='plan.json')
        args = parser.parse_args(argv)
        attempt = self.attempt_path(args.attempt)
        if args.execute:
            self.require(args.pins is not None and args.pins_sha256 is not None, 'future MAIN pins path AND SHA256 required')
            cfg, manifest, observed = self.observe()
            pins = self.authorize(args.pins, args.pins_sha256, observed, attempt)
            self.execute(cfg, manifest, observed, pins, args.pins, args.pins_sha256, attempt)
        else:
            self.require(not attempt.exists(), 'plan attempt already exists; choose a new name')
            self.require(Path(args.plan_name).name == args.plan_name and args.plan_name.endswith('.json'), 'plan filename only')
            cfg, _, observed = self.observe(strict=False)
            compiles, link, syntax = self.commands(cfg, observed['units'], attempt)
            report = dict(status='NOT_EXECUTED', accepted_source_pins=False, pending_source_not_accepted=True, authority='OBSERVATION_ONLY_NOT_APPROVAL', observation=observed, environment=self.environment(cfg, attempt), compiles=compiles, link=link, syntax=syntax, wasm_validation=self.wasm_command(cfg, attempt), omissions=self.OMISSIONS, object_reuse=False, execution_ready=False)
            attempt.mkdir(parents=True, exist_ok=False)
            (attempt / args.plan_name).write_text(self.canonical(report))
            print('NOT_EXECUTED: ' + str(attempt / args.plan_name))
        return 0

    def validate_payload(self, root, manifest):
        """Read actual JS index/data slices, exact non-overlapping 79-member closure."""
        root = self.clean(Path(root))
        for name in self.ARTIFACTS:
            self.clean(root / name)
            self.require((root / name).is_file(), 'missing artifact: ' + name)
        html = (root / 'index.html').read_text()
        shell = Shell()
        shell.feed(html)
        self.require(shell.canvas == ['canvas'] and shell.scripts == ['index.js'] and ('{{{ SCRIPT }}}' not in html), 'generated shell canvas/script mismatch')
        self.require((root / 'index.wasm').read_bytes()[:8] == self.MAGIC, 'invalid Wasm magic/version')
        data = (root / 'index.data').read_bytes()
        self.require(len(data) == self.PACK_BYTES, 'actual data length mismatch')
        entries = re.findall('\\{filename:"([^"]+)",start:(\\d+),end:(\\d+)\\}', (root / 'index.js').read_text())
        expected = {e['virtual_path']: e for e in manifest['entries']}
        self.require(len(entries) == 79 and len(expected) == 79 and (len({e[0] for e in entries}) == 79) and ({e[0] for e in entries} == set(expected)), 'actual preload member mismatch')
        cursor = 0
        checks = []
        for name, start_text, end_text in sorted(entries, key=lambda e: int(e[1])):
            start, end = (int(start_text), int(end_text))
            entry = expected[name]
            self.require(start == cursor and end > start and (end <= len(data)), 'preload overlap/gap/range mismatch')
            raw = data[start:end]
            self.require(len(raw) == entry['bytes'] and hashlib.sha256(raw).hexdigest() == entry['sha256'], 'actual preload bytes mismatch: ' + name)
            checks.append(dict(path=name, start=start, end=end, sha256=entry['sha256']))
            cursor = end
        self.require(cursor == len(data), 'unindexed preload suffix')
        return dict(status='PASS', files=79, raw_bytes=len(data), actual_preload_slices=checks, canvas='canvas', runtime_decoding='NOT RUN')

    def verify(self, root, attempt, pins_path, pins_sha):
        root, attempt = (self.clean(Path(root)), self.clean(Path(attempt)))
        self.require(root in (self.HERE / self.OUTPUT, attempt / 'bundle'), 'explicit profile output or matching attempt bundle required')
        self.attempt_path(str(attempt.relative_to(self.ROOT)))
        cfg, manifest, observed = self.observe()
        self.authorize(pins_path, pins_sha, observed, attempt, completed=True)
        result = json.loads((attempt / 'result.json').read_text())
        if self.profile == 'network':
            self.require(result.get('profile') == cfg['profile'], 'output metadata profile mismatch')
        self.require(result['status'] == 'LINKED_NOT_BROWSER_VERIFIED' and result['stable_inventory'] is True, 'attempt incomplete/failed')
        self.require(result['pins_path'] == str(pins_path) and result['pins_sha256'] == pins_sha, 'attempt pins identity mismatch')
        self.require(result['attempt'] == str(attempt.relative_to(self.ROOT)) and result['ticket'] == cfg['ticket'], 'attempt identity mismatch')
        for key in ('inputs', 'preservation', 'units', 'ports', 'aliases', 'alias_decisions'):
            self.require(result[key] == observed[key], 'current inventory mismatch: ' + key)
        self.require(result['environment'] == self.environment(cfg, attempt) and result['object_reuse'] is False, 'environment/reuse differs')
        self.require(result['omissions'] == self.OMISSIONS and (not any(result['claims'].values())), 'unsupported runtime claim')
        expected_compiles, link, syntax = self.commands(cfg, observed['units'], attempt)
        runs = result['compiles']
        self.require(len(runs) == 61, '61 actual compile records required')

        def command_record(record, command):
            self.require(record['command'] == command and record['exit_code'] == 0, 'command/status mismatch')
            log = self.clean(Path(record['log']))
            self.require(log.parent == attempt / 'logs' and self.sha(log) == record['log_sha256'], 'diagnostic log changed')
        for actual, expected in zip(runs, expected_compiles):
            self.require(actual['source'] == expected['source'] and actual['object'] == expected['object'] and (actual['status'] == 'PASS'), 'compile inventory/status mismatch')
            command_record(actual, expected['command'])
            obj = self.clean(Path(actual['object']))
            self.require(self.sha(obj) == actual['object_sha256'] and obj.read_bytes()[:8] == self.MAGIC, 'object changed/invalid')
        for name, command in (('link', link), ('syntax', syntax), ('wasm_validation', self.wasm_command(cfg, attempt))):
            command_record(result[name], command)
        outputs = self.output_fingerprints(root, result['outputs'])
        metadata = self.clean(root / 'build-metadata.json')
        self.require(self.sha(metadata) == result['metadata_sha256'], 'metadata fingerprint mismatch')
        expected_metadata = dict(result)
        expected_metadata.pop('metadata_sha256')
        self.require(metadata.read_text() == self.canonical(expected_metadata), 'metadata/result mismatch')
        notices = {str(p.relative_to(root)): self.sha(p) for p in self.files(root / 'notices')}
        expected_notices = {'notices/' + str(p.relative_to(self.HERE / 'notices')): self.sha(p) for p in self.files(self.HERE / 'notices')}
        self.require(notices == result['notices'] == expected_notices, 'notice membership/bytes mismatch')
        expected_files = set(self.ARTIFACTS) | {'build-metadata.json'} | set(notices)
        self.require({str(p.relative_to(root)) for p in self.files(root)} == expected_files, 'extra/missing bundle members')
        actual_preload = self.validate_payload(root, manifest)
        self.require(actual_preload == result['preload_validation'], 'preload evidence differs')
        identity = dict(inputs=result['inputs'], outputs=outputs, pins_sha256=pins_sha, commands=[u['command'] for u in expected_compiles] + [link, syntax, self.wasm_command(cfg, attempt)], environment=result['environment'])
        self.require(result['bundle_id'] == hashlib.sha256(self.canonical(identity).encode()).hexdigest(), 'bundle identity mismatch')
        return dict(status='LINKED_NOT_BROWSER_VERIFIED', bundle_id=result['bundle_id'], actual_preload_files=79, files={**outputs, 'build-metadata.json': result['metadata_sha256']}, omissions=self.OMISSIONS)

    def verify_main(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--' + self.profile + '-root', dest='bundle_root', required=True, type=Path)
        parser.add_argument('--attempt', required=True, type=Path)
        parser.add_argument('--pins', required=True, type=Path)
        parser.add_argument('--pins-sha256', required=True)
        args = parser.parse_args()
        print(self.canonical(self.verify(args.bundle_root, args.attempt, args.pins, args.pins_sha256)))
