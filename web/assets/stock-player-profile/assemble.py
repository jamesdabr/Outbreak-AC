"""T282/D479 fixed 90-file private local pack. No import-time IO or project imports.

Only new pack-root/manifest/PROVENANCE outputs. Installed Pillow decodes the
three pinned stock JPEGs; no resize, recolor, external tools, network or retry.
"""
import hashlib
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import sys
from PIL import Image, __version__ as PILLOW_VERSION

HERE = Path(__file__).absolute().parent
REPO = HERE.parents[2]
BASE = REPO / 'web/assets/blackwood-profile'
BASE_PIN = '8c4f7eef5f0deafb06bec60d62be529a684a30d56bbdc6dc3e5f38dd21c69e60'
PREFIX = 'packages/models/playermodels/'
STOCK = (
    ('tris.md2', 'tris.md2', '4b4c61f40c62f612f488eec644cd41dce151790b1eb9da39c4b16b6e9fd040eb'),
    ('md2.cfg', 'md2.cfg', '5ba275c4e01b8d45dcde81f6261f3e31666329bf7b6fc0b19699cb0223068827'),
    ('license.txt', 'license.txt', 'f7489171be41ac97871dfd78fb384f524873c5c497b54999884aff876f311a36'),
    ('skin.jpg', 'skin.png', '3afff2bdbfcd395dffc94616a568d6ea619fd2e7daf1c7c987f2873682012346'),
    ('CLA/01.jpg', 'CLA/01.png', '4a6ab3ec81d2adcc1260ae13a0436d6f6a858d5c5cdb5ba44333b02e570dc572'),
    ('RVSF/01.jpg', 'RVSF/01.png', '3afff2bdbfcd395dffc94616a568d6ea619fd2e7daf1c7c987f2873682012346'),
)
ADDITIONS = b''.join(b'scriptcontext MDLCFG '+name+b'\n'
                     for name in (b'md2tag', b'mdlshadowdist', b'mdlcachelimit'))
MARKER = b'isolatecontext MDLCFG\n'
NOTICE = PREFIX+'license.txt'
STOCK_LICENSE = 'Bundled AssaultCube player notice: personal use; other uses require author permission'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False)+'\n').encode()


def relative(name):
    p = PurePosixPath(name)
    need(not p.is_absolute() and str(p) == name and '\\' not in name and
         all(v not in ('', '.', '..') for v in name.split('/')), 'unsafe member path')
    return name


def no_links(path):
    need(not any(p.is_symlink() for p in (path, *path.parents)), 'symlink path refused: '+str(path))


def members(root):
    no_links(root)
    result = []
    for path in sorted(root.rglob('*')):
        no_links(path)
        need(path.is_file() or path.is_dir(), 'nonordinary pack member')
        if path.is_file():
            result.append(relative(path.relative_to(root).as_posix()))
    need(len({v.casefold() for v in result}) == len(result), 'case alias')
    return sorted(result)


def decoded(data, expected_format):
    with Image.open(BytesIO(data)) as image:
        need(image.format == expected_format, 'unexpected image format')
        image.load()
        return image.convert('RGB'), image.convert('RGBA')


def main():
    need(not sys.argv[1:], 'no arguments or output selectors')
    pack = HERE / 'pack-root'
    for path in (pack, HERE/'manifest.json', HERE/'PROVENANCE.json'):
        no_links(path)
        need(not path.exists(), 'existing output refused: '+str(path))
    snapshots = {}
    def read(path):
        no_links(path)
        need(path.is_file(), 'missing ordinary input: '+str(path))
        data = path.read_bytes()
        snapshots[path] = data
        return data
    base_raw = read(BASE/'manifest.json')
    need(sha(base_raw) == BASE_PIN, 'Blackwood84 manifest changed')
    base = json.loads(base_raw)
    rows = base['entries']
    names = [relative(row['path']) for row in rows]
    need(base['schema_version'] == 1 and base['mount'] == '/outbreak' and
         len(names) == len(set(names)) == 84, 'expected Blackwood84; return to MAIN if different')
    need(members(BASE/'pack-root') == sorted(names), 'Blackwood membership differs')
    need(not set(names) & {PREFIX+out for _, out, _ in STOCK}, 'stock additions collide with base')
    blobs, entries, operations = {}, {}, []
    for row in rows:
        name = row['path']; source = BASE/'pack-root'/name; raw = read(source)
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'] and
             row['virtual_path'] == '/outbreak/'+name, 'base member identity changed: '+name)
        blobs[name] = raw
        entries[name] = dict(row, source_path=source.relative_to(REPO).as_posix(),
                             source_manifest='web/assets/blackwood-profile/manifest.json', source_sha256=sha(raw))
    old_cfg = blobs['config/browser.cfg']
    need(old_cfg.count(MARKER) == 1 and old_cfg.endswith(b'sealcontexts\n') and
         all(line not in old_cfg for line in ADDITIONS.splitlines()), 'unexpected MDLCFG baseline')
    blobs['config/browser.cfg'] = old_cfg.replace(MARKER, ADDITIONS+MARKER)
    need(blobs['config/browser.cfg'].replace(ADDITIONS, b'') == old_cfg, 'CFG changed beyond three additions')
    operations.append({'path': 'config/browser.cfg', 'operation': 'THREE_MDLCFG_WHITELIST_ADDITIONS_ONLY',
                       'source_sha256': sha(old_cfg), 'derived_sha256': sha(blobs['config/browser.cfg']),
                       'commands': ['md2tag', 'mdlshadowdist', 'mdlcachelimit'], 'isolation_and_seal_preserved': True})
    images = {}
    for src, dest, pin in STOCK:
        source = REPO/PREFIX/src; raw = read(source)
        need(sha(raw) == pin, 'stock input changed: '+src)
        name = PREFIX+dest; data = raw
        operation = {'path': name, 'source_path': source.relative_to(REPO).as_posix(),
                     'source_bytes': len(raw), 'source_sha256': pin, 'notice': NOTICE,
                     'license': STOCK_LICENSE, 'operation': 'BYTE_IDENTICAL_COPY'}
        if src.endswith('.jpg'):
            rgb, rgba = decoded(raw, 'JPEG')
            buffer = BytesIO(); rgb.save(buffer, format='PNG', compress_level=9)
            data = buffer.getvalue(); images[name] = (rgb, rgba)
            operation.update(operation='JPEG_TO_PNG_DECODED_PIXEL_COPY', dimensions=list(rgb.size),
                             rgb_pixel_sha256=sha(rgb.tobytes()), rgba_pixel_sha256=sha(rgba.tobytes()),
                             resize=False, recolor=False, palette_conversion=False, orientation_transform=False)
        blobs[name] = data
        entries[name] = {'path': name, 'virtual_path': '/outbreak/'+name,
                         'license': STOCK_LICENSE, 'notice': NOTICE,
                         'source_path': source.relative_to(REPO).as_posix(), 'source_sha256': pin}
        operation.update(derived_bytes=len(data), derived_sha256=sha(data))
        operations.append(operation)
    need(len(blobs) == len(entries) == 90, 'expected exact90; return to MAIN, do not change scope')
    cfg_commands = {line.split()[0] for line in blobs[PREFIX+'md2.cfg'].decode().splitlines() if line.strip()}
    need(cfg_commands == {'mdlscale', 'mdltrans', 'mdlshadowdist', 'mdlcachelimit', 'md2tag'}, 'unexpected stock CFG commands')
    for name, raw in blobs.items():
        entries[name].update(bytes=len(raw), sha256=sha(raw))
    manifest = dict(base, profile='STOCK_PLAYER_LOCAL_PERSONAL_USE', entries=[entries[n] for n in sorted(entries)],
                    inputs=[{'path': path.relative_to(REPO).as_posix(), 'sha256': sha(raw)}
                            for path, raw in sorted(snapshots.items()) if path == BASE/'manifest.json' or path.is_relative_to(REPO/PREFIX)],
                    raw_bytes=sum(len(data) for data in blobs.values()), assembly_performed=True,
                    existing_profiles_modified=False, runtime_verified=False, gameplay_verified=False,
                    candidate_balance_accepted=False, transfer_measurement='NOT_OBSERVED')
    need(set(manifest) == set(base), 'retain current mount/entries manifest shape')
    pack.mkdir()
    def write(path, data):
        no_links(path)
        need(path.is_relative_to(HERE), 'output escape')
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as output:
            output.write(data)
    for name in sorted(blobs):
        write(pack/relative(name), blobs[name])
    need(members(pack) == sorted(blobs), 'generated membership differs from exact90')
    for name, wanted in blobs.items():
        actual = (pack/name).read_bytes()
        need(actual == wanted and len(actual) == entries[name]['bytes'] and sha(actual) == entries[name]['sha256'], 'written member mismatch')
    for name in names:
        if name != 'config/browser.cfg':
            need((pack/name).read_bytes() == snapshots[BASE/'pack-root'/name], 'base copy changed')
    for src, dest, _ in STOCK[:3]:
        need((pack/PREFIX/dest).read_bytes() == snapshots[REPO/PREFIX/src], 'stock byte-copy changed')
    for name, (rgb, rgba) in images.items():
        out_rgb, out_rgba = decoded((pack/name).read_bytes(), 'PNG')
        need(out_rgb.size == rgb.size and out_rgb.tobytes() == rgb.tobytes() and
             out_rgba.size == rgba.size and out_rgba.tobytes() == rgba.tobytes(), 'decoded skin pixels changed')
    need((pack/'config/browser.cfg').read_bytes().replace(ADDITIONS, b'') == old_cfg, 'written CFG delta differs')
    need(all(path.read_bytes() == raw for path, raw in snapshots.items()), 'original input changed during assembly')
    provenance = {'schema_version': 1, 'ticket': 'T2821.0', 'contract': 'STOCK_FIRST_PROTOTYPE0.1/D479',
                  'classification': 'DATA_ONLY_PRIVATE_LOCAL_USE', 'base_manifest_sha256': BASE_PIN,
                  'assembler_sha256': sha(Path(__file__).read_bytes()), 'pillow_version': PILLOW_VERSION,
                  'source_identities': [{'path': p.relative_to(REPO).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}
                                        for p, raw in sorted(snapshots.items())],
                  'operations': operations, 'stock_notice': NOTICE, 'stock_license': STOCK_LICENSE,
                  'stock_is_MIT': False, 'public_distribution_authorized': False,
                  'checks': {'exact_members': 90, 'base_unchanged_copies': 83, 'stock_byte_copies': 3,
                             'skin_RGB_and_RGBA_pixel_equalities': 3, 'CFG_only_three_whitelist_additions': True,
                             'original_inputs_unchanged': True, 'all_written_lengths_and_hashes_match': True},
                  'raw_bytes': manifest['raw_bytes'], 'runtime_verified': False}
    write(HERE/'manifest.json', encode(manifest))
    write(HERE/'PROVENANCE.json', encode(provenance))
    need(json.loads((HERE/'manifest.json').read_bytes()) == manifest and
         json.loads((HERE/'PROVENANCE.json').read_bytes()) == provenance, 'metadata readback differs')
    print('PASS exact90: 83 unchanged base copies + 1 CFG whitelist-only override + 3 stock byte copies + 3 decoded-pixel PNG copies')
    print('PASS membership/bytes/hashes, original input preservation, RGB and RGBA pixels, CFG isolation/seal; Pillow', PILLOW_VERSION)
    for path in (HERE/'manifest.json', HERE/'PROVENANCE.json'):
        raw = path.read_bytes(); print(path.name, len(raw), sha(raw))
    print('Pack raw bytes:', manifest['raw_bytes'])
    for operation in operations[1:]:
        print(operation['path'], operation['derived_bytes'], operation['derived_sha256'])
    print('Private local asset assembly only; build/browser/engine/runtime/network NOT RUN.')


if __name__ == '__main__':
    main()
