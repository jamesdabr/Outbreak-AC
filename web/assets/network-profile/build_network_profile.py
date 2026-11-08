#!/usr/bin/env python3
"""T064 deterministic DATA-only derivative. No host config/game/tool execution."""
import json
from pathlib import Path
import struct
import sys

sys.dont_write_bytecode = True
from map_format import REPO, HERE, ENTITY, require, digest, regular, confined, members, parse, deflate, original_parser, anchors_report

PIN = '7def7d8da8a9567f8023f5675f6fa9369edcd930f635794c9c95ca106868e283'
SOURCE_MANIFEST = 'web/assets/audio-profile/manifest.json'
SOURCE_ROOT = 'web/assets/audio-profile/pack-root'
MAP = 'packages/maps/dev_outbreak_browser.cgz'
STARTS = ((16, 16, 5, 1350), (48, 16, 5, 2250), (16, 48, 5, 450), (48, 48, 5, 3150),
          (16, 32, 5, 900), (48, 32, 5, 2700), (32, 16, 5, 1800), (32, 48, 5, 0))
NATIVE_PINS = {
    'source/src/world.h': '7fc623e91fb09b9b2bf88c7508fb68d8b8c19b815e34062dc9c43c9e5816bcc3',
    'source/src/entity.h': 'dc42d6285c64139db7f4cf2fb9c509604128d823dd86b37112e8a8bac309ac30',
    'source/src/server.h': '3ca9c5b38b9af9eaee5b2169b5617997eb6156417e10148405dc9d0c378ae7b5',
    'source/src/tools.cpp': 'fe7055c0ce7ac986ff632f22e887de6b621fe85a3d601b6dcbfd6851b724ec5c',
    'source/src/protocol.cpp': '85ab66b5667459025ff1a83fb7811f1545d3254606ff1388167184e973327036',
    'source/src/protocol.h': 'a3e8f928b31976836d239817cd03300a11460d0ee9994417274b775990add42c',
    'source/src/serverfiles.h': 'efca26aaefb9d33cc8623bc84dcf06f3a1f10d0b9d9664fff78790dab2bed75f',
}


def canonical(value):
    return json.dumps(value, indent=2, sort_keys=True) + '\n'


def source(manifest_path=None, root=None):
    path = regular(manifest_path or REPO / SOURCE_MANIFEST)
    root = regular(root or REPO / SOURCE_ROOT)
    require(digest(path.read_bytes()) == PIN, 'T053 manifest pin')
    parent = json.loads(path.read_text())
    # These inspected stdlib-only helpers retain original upstream byte/notice closure.
    for name, pin in {
        'web/assets/audio-profile/check_profile.py': '1045add62a22392787272756b48e990dc6b2354fd6cfb16e1e626b1faab103ab',
        'web/assets/audio-profile/build_profile.py': '60f40d0b29344402196ad066a0bf9257e0f8dbdc96f54a24e294e7d0a535a782',
        'web/assets/media-profile/assemble.py': 'b0c96708226e30386af646f028f006309017934bacbd0ad8ddebdf58f475fc8d',
    }.items():
        require(digest(regular(REPO / name).read_bytes()) == pin, 'inspected source helper changed')
    sys.path.insert(0, str(REPO / 'web/assets/audio-profile'))
    from check_profile import validate
    validate(root, parent)
    require(parent['raw_bytes'] == 388764 and len(parent['entries']) == 79, 'T053 totals')
    payloads = {e['path']: confined(root, e['path']).read_bytes() for e in parent['entries']}
    return parent, payloads


def native_rules():
    for name, pin in NATIVE_PINS.items():
        require(digest(regular(REPO / name).read_bytes()) == pin, 'audited native source changed: ' + name)
    return dict(source_sha256=NATIVE_PINS, minimum_ffa_starts=5, ffa_attr2=100, supplied_ffa_starts=8,
                hasffaspawns_source_condition='es.spawns[2] >= MINSPAWNS', source_rule_satisfied=True,
                deathmatch_spawn_prerequisite_satisfied=True, actual_native_mode_selection='NOT RUN',
                citations=['source/src/world.h:150', 'source/src/entity.h:30', 'source/src/tools.cpp:291',
                           'source/src/tools.cpp:312', 'source/src/protocol.cpp:519',
                           'source/src/protocol.h:170', 'source/src/server.h:484', 'source/src/serverfiles.h:1001'])


def derive(data):
    old = parse(data)
    original_parser().decode_map(data)  # bounded original RLE/entity/geometry validation
    require(old['count'] == 9 and old['revision'] == 1, 'original count/revision')
    require([e[4] for e in old['entities']] == [2] * 4 + [1] * 5, 'original ordered starts/lights')
    header = bytearray(old['header'])
    struct.pack_into('<i', header, 16, 13)
    struct.pack_into('<i', header, 924, 2)
    starts = b''.join(ENTITY.pack(x, y, z, yaw, 2, 100, 0, 0, 0, 0, 0) for x, y, z, yaw in STARTS)
    return deflate(bytes(header) + starts + b''.join(old['records'][4:]) + old['geometry'])


def derivation(old_data, new_data):
    old, new = parse(old_data), parse(new_data)
    return dict(operation='replace four PLAYERSTART records by eight released FFA anchors; change only count/revision header fields',
                source_sha256=digest(old_data), result_sha256=digest(new_data), source_raw_sha256=digest(old['raw']),
                result_raw_sha256=digest(new['raw']), header_changes=[dict(offset=16, old=9, new=13), dict(offset=924, old=1, new=2)],
                entity_layout='<hhhhBBBBhbB', entity_bytes=16, old_entities=9, new_entities=13,
                old_starts=4, new_starts=[list(s) for s in STARTS], ffa_attr2=100, unchanged_lights=5,
                unchanged_light_records_sha256=digest(b''.join(old['records'][4:])),
                unchanged_rle_sha256=digest(old['geometry']), all_other_decompressed_bytes_unchanged=True,
                gzip=dict(header_hex='1f8b08000000000002ff', mtime=0, level=9, os=255, footer='CRC32 and ISIZE of decompressed data'))


def entry(src, raw, old_map, new_map):
    name = src['path']
    result = dict(path=name, virtual_path='/outbreak/' + name, bytes=len(raw), sha256=digest(raw),
                  notice=src['notice'], license=src['license'],
                  provenance=dict(source_root=SOURCE_ROOT, source_manifest=SOURCE_MANIFEST, source_manifest_sha256=PIN,
                                  source_path=name, source_sha256=src['sha256'], source_entry=src))
    if name == MAP:
        result['derivation'] = derivation(old_map, new_map)
    return result


def build(root, manifest_path=None, source_root=None):
    root = regular(root)
    parent, payloads = source(manifest_path, source_root)
    rules = native_rules()
    old_map = payloads[MAP]
    new_map = derive(old_map)
    cells, _ = original_parser().decode_map(old_map)
    report = anchors_report(cells, STARTS)
    report['native_rules'] = rules
    report['map_revision'] = 2
    report['map_sha256'] = digest(new_map)
    require(members(root) <= set(payloads), 'undeclared output members')
    for name in payloads:
        confined(root, name)
    entries = []
    for src in parent['entries']:
        name = src['path']
        raw = new_map if name == MAP else payloads[name]
        path = confined(root, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        entries.append(entry(src, raw, old_map, new_map))
    manifest = dict(schema_version=1, ticket='T064 revision3.7', profile='original-network-eight-ffa-data', mount='/outbreak',
                    source_root=SOURCE_ROOT, source_manifest=SOURCE_MANIFEST, source_manifest_sha256=PIN,
                    entries=entries, raw_bytes=sum(e['bytes'] for e in entries), copied_files=78, derived_files=[MAP],
                    map_revision=2, runtime_verified=False, overlay_performed=False)
    return manifest, report


if __name__ == '__main__':
    manifest, report = build(HERE / 'pack-root')
    (HERE / 'manifest.json').write_text(canonical(manifest))
    (HERE / 'anchors.json').write_text(canonical(report))
    print('T064 DATA only:79 files / %d bytes; native decode/mode/gameplay NOT RUN' % manifest['raw_bytes'])
