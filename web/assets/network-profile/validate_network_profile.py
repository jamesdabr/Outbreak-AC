#!/usr/bin/env python3
"""T064 independent transition checks plus exact source/provenance/member closure."""
import argparse
import json
from pathlib import Path
import struct
import sys

sys.dont_write_bytecode = True
from map_format import HERE, ENTITY, require, digest, regular, confined, members, parse, deflate, original_parser, anchors_report
from build_network_profile import PIN, SOURCE_ROOT, SOURCE_MANIFEST, MAP, source, native_rules, entry

# Deliberately literal ticket list: validator does not trust the builder's STARTS.
EXPECTED = ((16, 16, 5, 1350), (48, 16, 5, 2250), (16, 48, 5, 450), (48, 48, 5, 3150),
            (16, 32, 5, 900), (48, 32, 5, 2700), (32, 16, 5, 1800), (32, 48, 5, 0))


def transition(old_data, new_data):
    old, new = parse(old_data), parse(new_data)
    cells, original_entities = original_parser().decode_map(old_data)
    require(old['count'] == 9 and old['revision'] == 1 and len(original_entities) == 9, 'source revision/entity count')
    require([e[4] for e in old['entities']] == [2] * 4 + [1] * 5, 'source entity order')
    require(new['count'] == 13 and new['revision'] == 2, 'derived count/revision')
    require(old['header_size'] == new['header_size'], 'header size changed')
    masked = bytearray(new['header'])
    struct.pack_into('<i', masked, 16, 9)
    struct.pack_into('<i', masked, 924, 1)
    require(bytes(masked) == old['header'], 'other header/extra metadata changed')
    require(new['entities'][:8] == [(*p, 2, 100, 0, 0, 0, 0, 0) for p in EXPECTED], 'exact ordered FFA attrs/anchors')
    require(new['records'][8:] == old['records'][4:], 'five LIGHT bytes/order changed')
    require(new['geometry'] == old['geometry'], 'RLE geometry bytes changed')
    require(new['raw'] == new['header'] + b''.join(new['records']) + old['geometry'], 'raw structure')
    require(deflate(new['raw']) == new_data, 'noncanonical deterministic gzip stream')
    report = anchors_report(cells, EXPECTED)
    report.update(native_rules=native_rules(), map_revision=2, map_sha256=digest(new_data))
    return report


def validate(root, manifest, report=None, manifest_path=None, source_root=None):
    root = regular(root)
    parent, payloads = source(manifest_path, source_root)
    require(set(manifest) == {'schema_version', 'ticket', 'profile', 'mount', 'source_root', 'source_manifest',
                             'source_manifest_sha256', 'entries', 'raw_bytes', 'copied_files', 'derived_files',
                             'map_revision', 'runtime_verified', 'overlay_performed'}, 'manifest schema')
    require((manifest['schema_version'], manifest['ticket'], manifest['profile'], manifest['mount']) ==
            (1, 'T064 revision3.7', 'original-network-eight-ffa-data', '/outbreak'), 'profile identity')
    require((manifest['source_root'], manifest['source_manifest'], manifest['source_manifest_sha256']) ==
            (SOURCE_ROOT, SOURCE_MANIFEST, PIN), 'source identity')
    names = [e['path'] for e in manifest['entries']]
    require(len(names) == 79 and names == sorted(payloads) and members(root) == set(names), 'exact79 member/order closure')
    old_map, new_map = payloads[MAP], confined(root, MAP).read_bytes()
    expected_report = transition(old_map, new_map)
    copied = 0
    for actual, src in zip(manifest['entries'], parent['entries']):
        name = actual['path']
        raw = confined(root, name).read_bytes()
        if name != MAP:
            require(raw == payloads[name], 'copied bytes changed: ' + name)
            copied += 1
        require(actual == entry(src, raw, old_map, new_map), 'entry identity/provenance/notices/derivation: ' + name)
        require(actual['license'] == 'MIT' and actual['notice'] in names, 'notice/license closure')
        confined(root, actual['notice'])
    require(copied == manifest['copied_files'] == 78 and manifest['derived_files'] == [MAP], 'sole derivative')
    require(manifest['raw_bytes'] == sum(e['bytes'] for e in manifest['entries']), 'aggregate bytes')
    require(manifest['map_revision'] == 2 and manifest['runtime_verified'] is False and manifest['overlay_performed'] is False, 'unverified runtime/overlay claim')
    if report is not None:
        require(report == expected_report, 'anchor/native source report mismatch')
    return dict(status='PASS', files=79, byte_identical_copies=78, sole_derived_file=MAP,
                raw_bytes=manifest['raw_bytes'], header_fields_changed=[16, 924], map_revision=2,
                ffa_starts=8, minimum_ffa_starts=5, minimum_horizontal_separation=16,
                unchanged_lights=5, all_other_header_extra_rle_bytes_unchanged=True,
                canonical_gzip_crc_isize=True, native_decode='NOT RUN', dedicated_mode_selection='NOT RUN',
                gameplay='NOT RUN', overlay_performed=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    result = validate(HERE / 'pack-root', json.loads((HERE / 'manifest.json').read_text()),
                      json.loads((HERE / 'anchors.json').read_text()))
    print(json.dumps(result, sort_keys=True))
