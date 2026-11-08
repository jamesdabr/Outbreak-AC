"""T064 data/negative fixtures only. No native tools, config or game execution."""
import copy
import json
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import unittest
import zlib

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_network_profile as build
import validate_network_profile as check
from map_format import require, parse, deflate, inflate, confined, digest, members


class NetworkProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='t064-fixtures-', dir='/private/tmp')
        cls.base = Path(cls.temp.name)
        cls.root = cls.base / 'pack'
        cls.manifest, cls.report = build.build(cls.root)
        cls.parent, cls.payloads = build.source()

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def fixture(self):
        tmp = tempfile.TemporaryDirectory(prefix='t064-case-', dir='/private/tmp')
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name) / 'pack'
        shutil.copytree(self.root, root)
        return root, copy.deepcopy(self.manifest)

    def test_exact_pack_report_and_determinism(self):
        result = check.validate(self.root, self.manifest, self.report)
        self.assertEqual(result['byte_identical_copies'], 78)
        self.assertEqual(len(self.report['anchors']), 8)
        self.assertEqual(self.report['minimum_horizontal_separation'], 16)
        second, report = build.build(self.base / 'second')
        self.assertEqual(second, self.manifest)
        self.assertEqual(report, self.report)
        self.assertEqual({n: (self.root / n).read_bytes() for n in members(self.root)},
                         {n: (self.base / 'second' / n).read_bytes() for n in members(self.base / 'second')})

    def test_two_header_fields_lights_and_geometry(self):
        old = parse(self.payloads[build.MAP])
        new = parse((self.root / build.MAP).read_bytes())
        self.assertEqual((old['count'], old['revision'], new['count'], new['revision']), (9, 1, 13, 2))
        changed = {i for i, (a, b) in enumerate(zip(old['header'], new['header'])) if a != b}
        self.assertEqual(changed, {16, 924})
        self.assertEqual(old['records'][4:], new['records'][8:])
        self.assertEqual(old['geometry'], new['geometry'])

    def test_missing_and_extra_member(self):
        for extra in (False, True):
            with self.subTest(extra=extra):
                root, manifest = self.fixture()
                if extra:
                    (root / 'extra.txt').write_bytes(b'extra')
                else:
                    (root / 'config/font.cfg').unlink()
                with self.assertRaisesRegex(ValueError, 'member/order'):
                    check.validate(root, manifest)

    def test_changed_nonmap_even_with_rehashed_entry(self):
        for name in ('config/browser.cfg', 'LICENSE.txt', 'packages/maps/dev_outbreak_browser.cgz.LICENSE.txt'):
            with self.subTest(name=name):
                root, manifest = self.fixture()
                raw = (root / name).read_bytes() + b'changed'
                (root / name).write_bytes(raw)
                item = next(e for e in manifest['entries'] if e['path'] == name)
                item.update(bytes=len(raw), sha256=digest(raw))
                with self.assertRaisesRegex(ValueError, 'copied bytes'):
                    check.validate(root, manifest)

    def mutate_map(self, mutation, expected):
        root, manifest = self.fixture()
        parsed = parse((root / build.MAP).read_bytes())
        raw = bytearray(parsed['raw'])
        mutation(raw, parsed)
        data = deflate(bytes(raw))
        (root / build.MAP).write_bytes(data)
        item = next(e for e in manifest['entries'] if e['path'] == build.MAP)
        item.update(bytes=len(data), sha256=digest(data))
        with self.assertRaisesRegex(ValueError, expected):
            check.validate(root, manifest)

    def test_wrong_ffa_team_attribute(self):
        self.mutate_map(lambda raw, p: raw.__setitem__(p['header_size'] + 9, 0), 'FFA attrs')

    def test_wrong_yaw_or_duplicate_anchor(self):
        self.mutate_map(lambda raw, p: struct.pack_into('<h', raw, p['header_size'] + 6, 900), 'FFA attrs')
        self.mutate_map(lambda raw, p: raw.__setitem__(slice(p['header_size'] + 16, p['header_size'] + 32), raw[p['header_size']:p['header_size'] + 16]), 'FFA attrs')

    def test_wrong_revision(self):
        self.mutate_map(lambda raw, p: struct.pack_into('<i', raw, 924, 1), 'count/revision')

    def test_other_header_extra_light_geometry_change(self):
        for where, error in ((20, 'header/extra'), (981, 'header/extra'), ('light', 'LIGHT'), ('geometry', 'geometry')):
            with self.subTest(where=where):
                def mutation(raw, p):
                    offset = p['header_size'] + 8 * 16 if where == 'light' else p['header_size'] + 13 * 16 if where == 'geometry' else where
                    raw[offset] ^= 1
                self.mutate_map(mutation, error)

    def test_provenance_notice_and_runtime_claim(self):
        for field, value in (('notice', 'missing.txt'), ('license', 'not-MIT'), ('provenance', {})):
            with self.subTest(field=field):
                manifest = copy.deepcopy(self.manifest)
                manifest['entries'][0][field] = value
                with self.assertRaisesRegex(ValueError, 'provenance/notices'):
                    check.validate(self.root, manifest)
        manifest = dict(self.manifest, runtime_verified=True)
        with self.assertRaisesRegex(ValueError, 'runtime/overlay'):
            check.validate(self.root, manifest)

    def test_unsafe_paths_and_symlinks(self):
        for name in ('../escape', '/absolute', 'config/../escape', 'a\\b', 'a:b'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                confined(self.root, name)
        root, manifest = self.fixture()
        (root / 'LICENSE.txt').unlink()
        (root / 'LICENSE.txt').symlink_to(self.root / 'LICENSE.txt')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            check.validate(root, manifest)

    def test_gzip_crc_trailing_mtime_and_bounded_inflate(self):
        data = (self.root / build.MAP).read_bytes()
        mutations = [data[:-1], data + b'extra', data[:4] + b'\1' + data[5:], data[:-8] + bytes([data[-8] ^ 1]) + data[-7:]]
        raw = b'x' * (1024 * 1024 + 1)
        compressor = zlib.compressobj(9, zlib.DEFLATED, 31)
        bomb = compressor.compress(raw) + compressor.flush()
        mutations.append(bytes.fromhex('1f8b08000000000002ff') + bomb[10:])
        for candidate in mutations:
            with self.subTest(length=len(candidate)), self.assertRaises(ValueError):
                inflate(candidate)

    def test_anchor_report_is_not_trusted(self):
        report = copy.deepcopy(self.report)
        report['native_rules']['minimum_ffa_starts'] = 2
        with self.assertRaisesRegex(ValueError, 'report mismatch'):
            check.validate(self.root, self.manifest, report)


if __name__ == '__main__':
    unittest.main(verbosity=2)
