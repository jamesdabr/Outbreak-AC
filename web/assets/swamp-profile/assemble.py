"""T290: fixed local Swamp asset assembly; no project imports or execution.

One exclusive generation. Standard library + installed Pillow only. No network,
subprocess, map config execution, overwrite, cleanup, runtime or build.
"""
import hashlib
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import sys
from collections import Counter
from PIL import Image, __version__ as PILLOW_VERSION

HERE = Path(__file__).absolute().parent
REPO = HERE.parents[2]
BASE = REPO/'web/assets/stock-combat-profile'
INVENTORY = REPO/'notes/analysis/T288-resource-paths-4.json'
BASE_PIN = '8e8ab354b21260cc2393e5d9cb0da29c860ea869231be11e88e81706719ecd7e'
INVENTORY_PIN = '91d851a4d971d27c370a74160d4d05f6b14167d69622920348b60aed3b25e2a5'
SOURCE_SET_PIN = '3939e7dd8bb7e569e3c76b71873fc7f1df2491c229f5a8c87709ac959544ae9d'
MAP = 'packages/maps/official/ac_swamp.cgz'
MAP_PIN = 'acb8d878f90fb4dfa1a53aa69b4500282bace127fe426a658f348a70a4fde9aa'
AUDIO_NOTICE = 'docs/package_copyrights.txt'
ADDITIONS = {
    b'isolatecontext MAPCFG\n': b''.join(b'scriptcontext MAPCFG '+v+b'\n' for v in (b'loadsky', b'mapmodel', b'mapsound')),
    b'isolatecontext MDLCFG\n': b''.join(b'scriptcontext MDLCFG '+v+b'\n' for v in (b'mdlattribute', b'mdlvertexlight', b'mdlalphatest', b'mdlcullface')),
}


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
    p = PurePosixPath(name)
    need(not p.is_absolute() and str(p) == name and '\\' not in name and
         all(v not in ('', '.', '..') for v in name.split('/')), 'unsafe path')
    return name


def members(root):
    no_links(root)
    result = []
    for path in root.rglob('*'):
        no_links(path)
        need(path.is_file() or path.is_dir(), 'nonordinary member')
        if path.is_file():
            result.append(relative(path.relative_to(root).as_posix()))
    need(len(result) == len({p.casefold() for p in result}), 'case alias')
    return sorted(result)


def pixels(raw, fmt):
    with Image.open(BytesIO(raw)) as image:
        need(image.format == fmt, 'unexpected encoding')
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
        need(path.is_file(), 'missing ordinary input: '+str(path))
        raw = path.read_bytes(); snapshots[path] = raw
        return raw
    base_raw = read(BASE/'manifest.json'); inventory_raw = read(INVENTORY)
    need(sha(base_raw) == BASE_PIN and sha(inventory_raw) == INVENTORY_PIN, 'accepted inputs changed')
    base = json.loads(base_raw); inventory = json.loads(inventory_raw)
    rows = base['entries']; names = [relative(r['path']) for r in rows]
    need(base['mount'] == '/outbreak' and base['schema_version'] == 1 and
         len(names) == len(set(names)) == 97 and members(BASE/'pack-root') == sorted(names), 'base97 closure conflict')
    media = {}
    for model in inventory['models']:
        for row in [model['config'], *model['geometry'], *model['skins']]:
            name = relative(row['path'])
            need(name not in media or media[name] == row, 'inconsistent resource rows')
            media[name] = row
    for group in ('textures', 'sky', 'sounds'):
        for row in inventory[group]:
            name = relative(row['path'])
            need(name not in media or media[name]['bytes'] == row['bytes'], 'resource size conflict')
            media[name] = row
    notices = {relative(r['path']): r for r in inventory['notices']}
    new_names = set(media) | set(notices) | {AUDIO_NOTICE, MAP}
    need(len(media) == 230 and len(notices) == 17 and len(new_names) == 249 and not set(names)&new_names,
         'count/path conflict; stop before generation')
    need(Counter(Path(n).suffix for n in media) == {'.cfg':55, '.md3':51, '.jpg':114, '.png':1, '.ogg':9},
         'media categories conflict')
    originals = {n: read(REPO/n) for n in sorted(new_names)}
    identities = [[n, len(raw), sha(raw)] for n, raw in originals.items()]
    need(sha(json.dumps(identities, separators=(',', ':')).encode()) == SOURCE_SET_PIN, 'original set changed')
    need(sha(originals[MAP]) == MAP_PIN and len(originals[MAP]) == 23987, 'Swamp179 identity changed')
    for n, row in media.items():
        need(row['exists'] and len(originals[n]) == row['bytes'], 'resource input mismatch')
    for n, row in notices.items():
        need(originals[n].decode('utf-8', errors='replace') == row['text'], 'notice inventory changed')
    blobs, entries = {}, {}
    for row in rows:
        n = row['path']; source = BASE/'pack-root'/n; raw = read(source)
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'] and row['virtual_path'] == '/outbreak/'+n,
             'base bytes changed: '+n)
        blobs[n] = raw
        entries[n] = dict(row, source_path=source.relative_to(REPO).as_posix(), source_sha256=sha(raw),
                          source_manifest='web/assets/stock-combat-profile/manifest.json')
    old_cfg = blobs['config/browser.cfg']; cfg = old_cfg
    need(old_cfg.endswith(b'sealcontexts\n'), 'missing seal')
    for marker, addition in ADDITIONS.items():
        need(cfg.count(marker) == 1 and all(line not in cfg.splitlines() for line in addition.splitlines()), 'unexpected CFG')
        cfg = cfg.replace(marker, addition+marker)
    restored = cfg
    for addition in ADDITIONS.values():
        restored = restored.replace(addition, b'')
    need(restored == old_cfg, 'CFG delta conflict')
    blobs['config/browser.cfg'] = cfg
    operations = [dict(path='config/browser.cfg', operation='SEVEN_WHITELIST_ADDITIONS_ONLY',
                       source_sha256=sha(old_cfg), derived_sha256=sha(cfg),
                       added_lines=[line.decode() for block in ADDITIONS.values() for line in block.splitlines()])]
    image_sources = {}
    for n, raw in originals.items():
        applicable = [notice for notice in notices if n.startswith(str(PurePosixPath(notice).parent)+'/')]
        if n.endswith('.ogg') or n == AUDIO_NOTICE:
            applicable = [AUDIO_NOTICE]
        if n in notices:
            applicable = [n]
        need(applicable or n == MAP, 'missing notice association: '+n)
        license_text = 'Original mixed author-specific terms; see per-file notice; local/private only'
        if n == MAP:
            license_text = 'Embedded map notice cc-by-nc-sa-3.0; ac_swamp by Undead & ExodusS; map only'
        entry = dict(path=n, virtual_path='/outbreak/'+n, source_path=n, source_sha256=sha(raw),
                     license=license_text, notice=applicable[0] if applicable else MAP,
                     notices=sorted(applicable), encoding='ORIGINAL_BYTES')
        operation = dict(path=n, source_path=n, source_bytes=len(raw), source_sha256=sha(raw),
                         notices=sorted(applicable), operation='BYTE_IDENTICAL_COPY', encoding='ORIGINAL_BYTES')
        data = raw
        if n.endswith('.jpg'):
            rgb, rgba = pixels(raw, 'JPEG'); out = BytesIO()
            rgb.save(out, format='PNG', compress_level=9); data = out.getvalue()
            image_sources[n] = raw
            detail = dict(encoding='PNG', source_encoding='JPEG', virtual_filename_unchanged=True,
                          dimensions=list(rgb.size), rgb_pixel_sha256=sha(rgb.tobytes()),
                          rgba_pixel_sha256=sha(rgba.tobytes()), resize=False, recolor=False, orientation_transform=False)
            entry.update(detail); operation.update(detail, operation='JPEG_TO_PNG_SAME_VIRTUAL_PATH')
        blobs[n] = data; entries[n] = entry
        operation.update(derived_bytes=len(data), derived_sha256=sha(data)); operations.append(operation)
    need(len(blobs) == len(entries) == 346, 'exact346 conflict before writes')
    for n, raw in blobs.items():
        entries[n].update(bytes=len(raw), sha256=sha(raw))
    manifest = dict(base, profile='SWAMP_LOCAL_PRIVATE_USE', entries=[entries[n] for n in sorted(entries)],
                    inputs=[dict(path='web/assets/stock-combat-profile/manifest.json', sha256=BASE_PIN),
                            dict(path=INVENTORY.relative_to(REPO).as_posix(), sha256=INVENTORY_PIN)] +
                           [dict(path=n, sha256=sha(raw)) for n, raw in originals.items()],
                    raw_bytes=sum(map(len, blobs.values())))
    need(set(manifest) == set(base), 'manifest schema keys changed')
    def write(path, raw):
        no_links(path); need(path.is_relative_to(HERE), 'output escape')
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as output:
            output.write(raw)
    pack.mkdir()
    for n in sorted(blobs):
        write(pack/relative(n), blobs[n])
    need(members(pack) == sorted(blobs), 'written closure mismatch')
    for n, raw in blobs.items():
        actual = (pack/n).read_bytes()
        need(actual == raw and len(actual) == entries[n]['bytes'] and sha(actual) == entries[n]['sha256'], 'written identity mismatch')
    for n in names:
        if n != 'config/browser.cfg':
            need((pack/n).read_bytes() == snapshots[BASE/'pack-root'/n], 'base byte-copy mismatch')
    for n, raw in originals.items():
        if n not in image_sources:
            need((pack/n).read_bytes() == raw, 'original byte-copy mismatch')
    for n, raw in image_sources.items():
        rgb, rgba = pixels(raw, 'JPEG'); out_rgb, out_rgba = pixels((pack/n).read_bytes(), 'PNG')
        need(rgb.size == out_rgb.size and rgb.tobytes() == out_rgb.tobytes() and
             rgba.size == out_rgba.size and rgba.tobytes() == out_rgba.tobytes(), 'decoded pixel mismatch')
    restored = (pack/'config/browser.cfg').read_bytes()
    for addition in ADDITIONS.values():
        restored = restored.replace(addition, b'')
    need(restored == old_cfg and all(p.read_bytes() == raw for p, raw in snapshots.items()), 'CFG/original preservation mismatch')
    provenance = dict(schema_version=1, ticket='T2901.0', contract='STOCK_FIRST_PROTOTYPE0.6/D491',
                      base_manifest_sha256=BASE_PIN, inventory_sha256=INVENTORY_PIN, source_set_sha256=SOURCE_SET_PIN,
                      assembler_sha256=sha(Path(__file__).read_bytes()), pillow_version=PILLOW_VERSION,
                      selected_map=dict(name='ac_swamp', revision=179, path=MAP, bytes=23987, sha256=MAP_PIN,
                                        embedded_automatic_config_preserved=True, embedded_notice='cc-by-nc-sa-3.0'),
                      operations=operations, source_identities=[dict(path=p.relative_to(REPO).as_posix(), bytes=len(raw), sha256=sha(raw))
                                                               for p, raw in sorted(snapshots.items())],
                      stock_is_MIT=False, public_distribution_authorized=False, local_private_only=True,
                      notices=[dict(path=n, sha256=sha(originals[n]), text_encoding='utf-8 with replacement for display only',
                                    text=notices[n]['text']) for n in sorted(notices)],
                      audio_notice=AUDIO_NOTICE, no_blanket_map_license_for_media=True,
                      checks=dict(exact_members=346, base_unchanged_copies=96, new_original_byte_copies=135,
                                  JPEG_to_PNG_RGB_and_RGBA_equalities=114, only_seven_CFG_commands_added=True,
                                  isolation_and_seal_preserved=True, all_written_bytes_lengths_hashes_match=True,
                                  original_inputs_unchanged=True), raw_bytes=manifest['raw_bytes'], runtime_verified=False)
    for filename, value in (('manifest.json', manifest), ('PROVENANCE.json', provenance)):
        write(HERE/filename, encode(value))
        need(json.loads((HERE/filename).read_bytes()) == value, 'metadata readback mismatch')
    print('PASS exact346:97base+249new;96 unchanged base copies;135 original new byte copies;114 same-path RGB/RGBA-equal PNGs')
    print('PASS closure/bytes/lengths/hashes, seven-command CFG delta, isolation/seal, original input preservation')
    print('Raw pack bytes:', manifest['raw_bytes'], 'Pillow:', PILLOW_VERSION)
    for filename in ('manifest.json', 'PROVENANCE.json'):
        raw = (HERE/filename).read_bytes(); print(filename, len(raw), sha(raw))
    print('Swamp179 CGZ:', len(originals[MAP]), sha(originals[MAP]))
    print('No build/runtime/services/network; original assets immutable; local/private only.')


if __name__ == '__main__':
    main()
