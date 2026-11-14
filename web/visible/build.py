#!/usr/bin/env python3
"""T259: isolated cached browser build. Default prints commands; --execute builds."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / 'web/visible'
OUTPUT = ROOT / 'web/visible/candidates/stock-combat-1'
# Same 53 CLIENT_OBJS as source/src/Makefile and the existing browser recipe.
CPP_NAMES = '''crypto audiomanager autodownload client clientgame clients2c command
console docs editing entities http log main menus oggstream openal packetqueue
physics protocol rendercubes rendergl renderhud rendermodel renderparticles
rendertext rndmap scoreboard serverms server serverbrowser shadow soundlocation
soundscheduler stream texture tools water weapon wizard world worldio worldlight
worldocull worldrender zip bot/bot bot/botmanager bot/bot_ai bot/bot_util
bot/bot_waypoint bot/ac_bot bot/ac_bot_ai'''.split()
UNITS = ['source/src/' + name + '.cpp' for name in CPP_NAMES]
UNITS += ['source/enet/' + name + '.c' for name in
          ('callbacks', 'compress', 'host', 'list', 'packet', 'peer', 'protocol')]
UNITS += ['web/transport/enet_websocket.c']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(65536), b''):
            h.update(block)
    return h.hexdigest()


def repo_path(value):
    relative = Path(value)
    require(not relative.is_absolute() and '..' not in relative.parts,
            'Expected a repository-relative path')
    result = ROOT / relative
    require(not any(p.is_symlink() for p in (result, *result.parents)),
            'Symlink path refused: ' + value)
    return result


def inspect_inputs(cfg):
    require(repo_path(cfg['output']) == OUTPUT, 'Only stock-combat-1 is supported')
    require(not os.path.lexists(OUTPUT), 'Candidate already exists; no overwrite or retry')
    sdk = Path(cfg['sdk_root'])
    require(str(sdk) == '/private/tmp/outbreak-web-sdk', 'Use the installed SDK')
    version = sdk / 'upstream/emscripten/emscripten-version.txt'
    require(json.loads(version.read_text()) == cfg['sdk_version'] == '7.0.0',
            'Cached Emscripten 7.0.0 required')
    for launcher in ('emcc', 'em++'):
        require((sdk / 'upstream/emscripten' / launcher).is_file(),
                'Missing compiler launcher: ' + launcher)
    require('-DOUTBREAK_NETWORK_CLIENT' in cfg['common_cxx'] and
            '-DOUTBREAK_BLACKWOOD_CLIENT' in cfg['common_cxx'],
            'Network and Blackwood presentation flags required')
    require(len(CPP_NAMES) == 53 and len(UNITS) == 61 and len(set(UNITS)) == 61,
            'Expected 53 C++ and 8 network C units')
    for name in UNITS + [cfg['shell'], cfg['js_library']]:
        require(repo_path(name).is_file(), 'Missing source/input: ' + name)

    manifest_path = repo_path(cfg['manifest'])
    require(sha256(manifest_path) == cfg['manifest_sha256'],
            'Approved Blackwood manifest changed')
    manifest = json.loads(manifest_path.read_text())
    entries = manifest['entries']
    require(len(entries) == cfg['pack_files'] == 97 and manifest['mount'] == '/outbreak',
            'Approved 97-file /outbreak pack required')
    pack = repo_path(cfg['pack_root'])
    expected = set()
    for entry in entries:
        name = entry['path']
        require(name not in expected, 'Duplicate pack member')
        expected.add(name)
        member = repo_path(cfg['pack_root'] + '/' + name)
        require(member.is_file() and member.stat().st_size == entry['bytes'] and
                sha256(member) == entry['sha256'], 'Pack member changed: ' + name)
    actual = set()
    for member in pack.rglob('*'):
        require(not member.is_symlink(), 'Pack symlinks are not supported')
        if member.is_file():
            actual.add(member.relative_to(pack).as_posix())
    require(actual == expected, 'Pack has missing or extra files')

    cache = repo_path(cfg['cache_source'])
    for port in ('sdl2', 'sdl2_image', 'zlib', 'vorbis', 'ogg', 'libpng'):
        require((cache / 'ports' / port / '.emscripten_url').is_file(),
                'Missing cached port: ' + port)
    for library in ('libSDL2.a', 'libSDL2_image-png.a', 'libal.a', 'libz.a',
                    'libvorbis.a', 'libogg.a', 'libpng.a'):
        require((cache / 'sysroot/lib/wasm32-emscripten' / library).is_file(),
                'Missing cached library: ' + library)
    return sdk, cache


def commands(cfg, sdk):
    rows = []
    includes = ['-I' + str(ROOT / p) for p in
                ('source/src', 'source/src/bot', 'source/enet/include', 'web/transport')]
    objects = []
    for index, source in enumerate(UNITS):
        cpp = source.endswith('.cpp')
        obj = OUTPUT / 'objects' / ('%02d.o' % index)
        objects.append(str(obj))
        argv = [str(sdk / 'upstream/emscripten' / ('em++' if cpp else 'emcc'))]
        argv += cfg['common_cxx'] + cfg['ports'] if cpp else cfg['common_c']
        argv += includes + ['-c', str(ROOT / source), '-o', str(obj)]
        rows.append(('%02d-%s' % (index, Path(source).stem), argv))
    link = [str(sdk / 'upstream/emscripten/em++')] + objects + cfg['ports'] + cfg['link']
    link += ['--js-library', str(ROOT / cfg['js_library']),
             '--shell-file', str(ROOT / cfg['shell']),
             '--preload-file', str(ROOT / cfg['pack_root']) + '@/outbreak',
             '-o', str(OUTPUT / 'bundle/index.html')]
    rows.append(('link', link))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true',
                        help='Build only after separate MAIN release; otherwise print commands')
    args = parser.parse_args()
    cfg = json.loads((HERE / 'config.json').read_text())
    sdk, cache = inspect_inputs(cfg)
    rows = commands(cfg, sdk)
    if not args.execute:
        print('\n'.join(shlex.join(argv) for _, argv in rows))
        print('Read-only plan. Build requires a separate MAIN release and --execute.')
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir()  # Exclusive: a raced or occupied candidate is never adopted.
    for directory in ('objects', 'bundle', 'logs', 'tmp', 'node-cache'):
        (OUTPUT / directory).mkdir()
    shutil.copytree(cache, OUTPUT / 'cache')
    env = dict(PATH='/usr/bin:/bin:/usr/sbin:/sbin', EMSDK=str(sdk),
               EMSDK_PYTHON=sys.executable, EM_CONFIG=str(sdk / '.emscripten'),
               EM_CACHE=str(OUTPUT / 'cache'), EM_PORTS=str(OUTPUT / 'cache/ports'),
               EM_FROZEN_CACHE='1', NODE_COMPILE_CACHE=str(OUTPUT / 'node-cache'),
               EMCC_TEMP_DIR=str(OUTPUT / 'tmp'), TMPDIR=str(OUTPUT / 'tmp'),
               PYTHONDONTWRITEBYTECODE='1')
    with (OUTPUT / 'logs/commands.txt').open('x') as command_log:
        for label, argv in rows:
            command_log.write(shlex.join(argv) + '\n')
            command_log.flush()
            print('Building ' + label, flush=True)
            with (OUTPUT / 'logs' / (label + '.log')).open('xb') as log:
                subprocess.run(argv, cwd=ROOT, env=env, stdout=log,
                               stderr=subprocess.STDOUT, check=True)
    for name in ('index.html', 'index.js', 'index.wasm', 'index.data'):
        require((OUTPUT / 'bundle' / name).is_file(), 'Missing linked output: ' + name)
    print('Built ' + str(OUTPUT / 'bundle/index.html'))
    print('Browser playtest and server join/spawn remain separately authorized.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print('Visible build stopped; preserve any candidate and logs: ' + str(error),
              file=sys.stderr)
        raise SystemExit(1)
