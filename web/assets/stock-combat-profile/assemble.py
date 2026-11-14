"""T284: one exclusive, fixed-path, local 97-file asset assembly.

No project imports, subprocesses, network, overwrite, cleanup or runtime effects.
"""
import hashlib
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import sys
from PIL import Image, __version__ as PILLOW_VERSION

HERE = Path(__file__).absolute().parent
REPO = HERE.parents[2]
BASE = REPO/'web/assets/stock-player-profile'
BASE_PIN = '812a3d822e290774cef051a040bdeb03fd1b47f431fe53b7fef2537b5217ce37'
PREFIX = 'packages/models/weapons/'
STOCK = (
    ('license.txt', 'f08789d1c0b9565462402732b767390d9ae636bf14312622874b7dc9bc3c5171'),
    ('pistol/world/tris.md2', '4e5ddea794b200e19ffb18c51a1bd6f6e6a1ce5e2232da75839b8ce17a942af8'),
    ('pistol/world/md2.cfg', '9b7ab2a2ec5a236c9145de2ac4da1e270e71f7a51aa9808eafc3bbaef53a16ec'),
    ('pistol/world/skin.jpg', '77a9f58c3529a6722733dcb46525e34473c26955284477349d782e507e301359'),
    ('assault/world/tris.md2', '32fe4bf7935f95aa392a77c55ab050f8b704f8fc171abcf63b6c0406335bb09c'),
    ('assault/world/md2.cfg', '9ba2f0ac05c0b7044706ec76985a5e1fd9ade55ce318e086248f0fb3d5458b0b'),
    ('assault/world/skin.jpg', '402eb7833a32ec1dff5d5012cdef24e08fed14c18314c2ae01e1f3924f187b48'),
)
WHITELIST = b'scriptcontext MDLCFG md2emit\n'
BINDINGS = b'keymap 49 1\nbind 1 [weapon pistol]\nkeymap 50 2\nbind 2 [weapon assault]\n'
MARKER = b'isolatecontext MDLCFG\n'
NOTICE = PREFIX+'license.txt'
LICENSE = 'CC BY-NC-SA 2.5; Markus Bekel (makkE); see bundled weapons/license.txt'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()


def no_links(path):
    need(not any(p.is_symlink() for p in (path, *path.parents)), 'symlink refused: '+str(path))


def relative(name):
    path = PurePosixPath(name)
    need(not path.is_absolute() and str(path) == name and '\\' not in name and
         all(p not in ('', '.', '..') for p in name.split('/')), 'unsafe path')
    return name


def members(root):
    no_links(root)
    result = []
    for path in root.rglob('*'):
        no_links(path)
        need(path.is_file() or path.is_dir(), 'nonordinary member')
        if path.is_file():
            result.append(relative(path.relative_to(root).as_posix()))
    need(len(result) == len(set(v.casefold() for v in result)), 'case alias')
    return sorted(result)


def pixels(raw, fmt):
    with Image.open(BytesIO(raw)) as image:
        need(image.format == fmt, 'wrong image format')
        image.load()
        return image.convert('RGB'), image.convert('RGBA')


def main():
    need(not sys.argv[1:], 'no arguments permitted')
    pack = HERE/'pack-root'
    for path in (pack, HERE/'manifest.json', HERE/'PROVENANCE.json'):
        no_links(path)
        need(not path.exists(), 'existing output refused')
    snapshots = {}
    def read(path):
        no_links(path)
        need(path.is_file(), 'missing input')
        raw = path.read_bytes()
        snapshots[path] = raw
        return raw
    base_raw = read(BASE/'manifest.json')
    need(sha(base_raw) == BASE_PIN, 'accepted base changed')
    base = json.loads(base_raw)
    rows = base['entries']
    names = [relative(row['path']) for row in rows]
    need(base['mount'] == '/outbreak' and base['schema_version'] == 1 and
         len(names) == len(set(names)) == 90, 'expected accepted90')
    need(members(BASE/'pack-root') == sorted(names), 'base membership mismatch')
    blobs, entries, operations, images = {}, {}, [], {}
    for row in rows:
        name = row['path']; source = BASE/'pack-root'/name; raw = read(source)
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'] and
             row['virtual_path'] == '/outbreak/'+name, 'base member changed: '+name)
        blobs[name] = raw
        entries[name] = dict(row, source_path=source.relative_to(REPO).as_posix(),
                             source_manifest='web/assets/stock-player-profile/manifest.json', source_sha256=sha(raw))
    old_cfg = blobs['config/browser.cfg']
    need(old_cfg.count(MARKER) == 1 and old_cfg.endswith(b'sealcontexts\n') and
         WHITELIST not in old_cfg and b'keymap 49 ' not in old_cfg and b'keymap 50 ' not in old_cfg,
         'unexpected CFG baseline')
    cfg = old_cfg.replace(MARKER, WHITELIST+MARKER).replace(b'fov 90\n', BINDINGS+b'fov 90\n')
    need(cfg.count(BINDINGS) == 1 and cfg.replace(WHITELIST, b'').replace(BINDINGS, b'') == old_cfg,
         'CFG delta exceeds approved additions')
    blobs['config/browser.cfg'] = cfg
    operations.append(dict(path='config/browser.cfg', operation='APPROVED_CFG_ADDITIONS_ONLY',
                           source_sha256=sha(old_cfg), derived_sha256=sha(cfg),
                           added_lines=(WHITELIST+BINDINGS).decode().splitlines(), isolation_and_seal_preserved=True))
    for src, pin in STOCK:
        source = REPO/PREFIX/src; raw = read(source)
        need(sha(raw) == pin, 'stock input changed: '+src)
        name = PREFIX+(src[:-4]+'.png' if src.endswith('.jpg') else src)
        need(name not in blobs, 'stock path collision')
        data = raw
        operation = dict(path=name, source_path=source.relative_to(REPO).as_posix(), source_bytes=len(raw),
                         source_sha256=pin, license=LICENSE, notice=NOTICE, operation='BYTE_IDENTICAL_COPY')
        if src.endswith('.jpg'):
            rgb, rgba = pixels(raw, 'JPEG')
            buffer = BytesIO(); rgb.save(buffer, format='PNG', compress_level=9)
            data = buffer.getvalue(); images[name] = (rgb, rgba)
            operation.update(operation='JPEG_TO_PNG_DECODED_PIXEL_COPY', dimensions=list(rgb.size),
                             rgb_pixel_sha256=sha(rgb.tobytes()), rgba_pixel_sha256=sha(rgba.tobytes()),
                             resize=False, recolor=False, orientation_transform=False)
        blobs[name] = data
        entries[name] = dict(path=name, virtual_path='/outbreak/'+name, license=LICENSE, notice=NOTICE,
                             source_path=source.relative_to(REPO).as_posix(), source_sha256=pin)
        operation.update(derived_bytes=len(data), derived_sha256=sha(data)); operations.append(operation)
    need(len(blobs) == len(entries) == 97, 'expected exact97; stop on conflict')
    for name, raw in blobs.items():
        entries[name].update(bytes=len(raw), sha256=sha(raw))
    manifest = dict(base, profile='STOCK_COMBAT_LOCAL_PRIVATE_USE', entries=[entries[n] for n in sorted(entries)],
                    inputs=[dict(path=p.relative_to(REPO).as_posix(), sha256=sha(raw))
                            for p, raw in sorted(snapshots.items()) if p == BASE/'manifest.json' or p.is_relative_to(REPO/PREFIX)],
                    raw_bytes=sum(map(len, blobs.values())))
    need(set(manifest) == set(base), 'manifest shape changed')
    def write(path, raw):
        no_links(path)
        need(path.is_relative_to(HERE), 'output escape')
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as output:
            output.write(raw)
    pack.mkdir()
    for name in sorted(blobs):
        write(pack/relative(name), blobs[name])
    need(members(pack) == sorted(blobs), 'written membership differs')
    for name, raw in blobs.items():
        actual = (pack/name).read_bytes()
        need(actual == raw and sha(actual) == entries[name]['sha256'], 'written bytes/hash mismatch')
    for name in names:
        if name != 'config/browser.cfg':
            need((pack/name).read_bytes() == snapshots[BASE/'pack-root'/name], 'base copy mismatch')
    for src, _ in STOCK:
        if not src.endswith('.jpg'):
            need((pack/PREFIX/src).read_bytes() == snapshots[REPO/PREFIX/src], 'stock byte copy mismatch')
    for name, (rgb, rgba) in images.items():
        out_rgb, out_rgba = pixels((pack/name).read_bytes(), 'PNG')
        need(out_rgb.size == rgb.size and out_rgb.tobytes() == rgb.tobytes() and
             out_rgba.size == rgba.size and out_rgba.tobytes() == rgba.tobytes(), 'pixel mismatch')
    need((pack/'config/browser.cfg').read_bytes().replace(WHITELIST, b'').replace(BINDINGS, b'') == old_cfg,
         'written CFG delta mismatch')
    need(all(p.read_bytes() == raw for p, raw in snapshots.items()), 'original input changed')
    provenance = dict(schema_version=1, ticket='T2841.0', contract='STOCK_FIRST_PROTOTYPE0.3/D483',
                      classification='DATA_ONLY_LOCAL_PRIVATE_USE', base_manifest_sha256=BASE_PIN,
                      assembler_sha256=sha(Path(__file__).read_bytes()), pillow_version=PILLOW_VERSION,
                      source_identities=[dict(path=p.relative_to(REPO).as_posix(), bytes=len(raw), sha256=sha(raw))
                                         for p, raw in sorted(snapshots.items())], operations=operations,
                      weapon_license=LICENSE, weapon_notice=NOTICE,
                      player_notice='packages/models/playermodels/license.txt', player_personal_use_notice_preserved=True,
                      stock_is_MIT=False, public_distribution_authorized=False,
                      checks=dict(exact_members=97, unchanged_base_copies=89, stock_byte_copies=5,
                                  skin_RGB_and_RGBA_equalities=2, approved_CFG_delta_only=True,
                                  original_inputs_unchanged=True, all_written_bytes_and_hashes_match=True),
                      raw_bytes=manifest['raw_bytes'], runtime_verified=False)
    for filename, value in (('manifest.json', manifest), ('PROVENANCE.json', provenance)):
        write(HERE/filename, encode(value))
        need(json.loads((HERE/filename).read_bytes()) == value, 'metadata readback mismatch')
    print('PASS exact97; 89 base copies, 1 approved CFG override, 5 stock byte copies, 2 RGB/RGBA-equal PNGs')
    print('PASS membership, bytes/hashes, input preservation, CFG isolation/seal; Pillow', PILLOW_VERSION)
    print('Raw pack bytes:', manifest['raw_bytes'])
    for operation in operations:
        print(operation['path'], operation.get('dimensions', ''), operation.get('derived_bytes', ''), operation['derived_sha256'])
    for filename in ('manifest.json', 'PROVENANCE.json'):
        raw = (HERE/filename).read_bytes(); print(filename, len(raw), sha(raw))
    print('Build/runtime/browser/network NOT RUN; no audio added.')


if __name__ == '__main__':
    main()
