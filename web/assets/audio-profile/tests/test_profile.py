"""T053 byte-only fixtures use owned temporary copies; never media playback."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build_profile as build
from check_profile import validate


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name);self.root=self.base/'output'

    def copied_source(self):
        root=self.base/'source';shutil.copytree(build.REPO/build.SOURCE_ROOT,root)
        manifest=self.base/'source-manifest.json';manifest.write_bytes((build.REPO/build.SOURCE_MANIFEST).read_bytes())
        return manifest,root

    def test_exact_two_lines_and_78_copies(self):
        m=build.build(self.root);result=validate(self.root,m)
        self.assertEqual((result['files'],result['byte_identical_copies']),(79,78))
        original=(build.REPO/build.SOURCE_ROOT/build.BROWSER).read_bytes()
        changed=(self.root/build.BROWSER).read_bytes()
        self.assertEqual(changed.replace(b'\naudio 1\n',b'\naudio 0\n').replace(b'\nsoundvol 96\n',b'\nsoundvol 0\n'),original)
        self.assertIn(b'musicvol 0\n',changed);self.assertIn(b'hudgun 0\n',changed)
        self.assertFalse(m['runtime_verified'])

    def test_determinism(self):
        first=build.build(self.root)
        data={e['path']:(self.root/e['path']).read_bytes() for e in first['entries']}
        second=build.build(self.root)
        self.assertEqual(build.canonical(first),build.canonical(second))
        self.assertEqual(data,{n:(self.root/n).read_bytes() for n in data})

    def test_source_pin_and_changed_payload_rejected(self):
        manifest,root=self.copied_source();original=manifest.read_bytes();manifest.write_bytes(b'{}')
        with self.assertRaisesRegex(ValueError,'pin'):build.build(self.root,manifest,root)
        self.assertFalse(self.root.exists());manifest.write_bytes(original)
        (root/'packages/audio/outbreak/proof_tone.wav').write_bytes(b'changed fixture')
        with self.assertRaisesRegex(ValueError,'source hash'):build.build(self.root,manifest,root)
        self.assertFalse(self.root.exists())

    def test_missing_extra_or_symlink_source_rejected(self):
        manifest,root=self.copied_source();path=root/'packages/audio/outbreak/proof_tone.wav';original=path.read_bytes();path.unlink()
        with self.assertRaisesRegex(ValueError,'membership'):build.build(self.root,manifest,root)
        path.write_bytes(original);extra=root/'extra.txt';extra.write_text('owned fixture')
        with self.assertRaisesRegex(ValueError,'membership'):build.build(self.root,manifest,root)
        self.assertEqual(extra.read_text(),'owned fixture');extra.unlink();path.unlink();path.symlink_to('/outside-profile-fixture-not-read')
        with self.assertRaisesRegex(ValueError,'symlink'):build.build(self.root,manifest,root)
        self.assertTrue(path.is_symlink())

    def test_wrong_config_change_and_extra_permission(self):
        m=build.build(self.root);path=self.root/build.BROWSER;raw=path.read_bytes()
        for bad in (raw.replace(b'musicvol 0',b'musicvol 96'),raw.replace(b'soundvol 96',b'soundvol 95'),raw+b'scriptcontext MDLCFG exec\n'):
            path.write_bytes(bad)
            with self.assertRaisesRegex(ValueError,'bytes differ'):validate(self.root,m)
        path.write_bytes(raw);validate(self.root,m)

    def test_extra_output_and_symlink_preserved(self):
        m=build.build(self.root);extra=self.root/'extra.txt';extra.write_text('keep')
        with self.assertRaisesRegex(ValueError,'undeclared'):build.build(self.root)
        with self.assertRaisesRegex(ValueError,'membership'):validate(self.root,m)
        self.assertEqual(extra.read_text(),'keep');extra.unlink()
        path=self.root/build.BROWSER;path.unlink();path.symlink_to('/outside-profile-fixture-not-read')
        with self.assertRaisesRegex(ValueError,'symlink'):build.build(self.root)
        with self.assertRaisesRegex(ValueError,'symlink'):validate(self.root,m)
        self.assertTrue(path.is_symlink())

    def test_metadata_provenance_and_traversal(self):
        original=build.build(self.root)
        for kind in ('source','hash','notice','recipe'):
            m=copy.deepcopy(original)
            if kind=='source':m['entries'][0]['provenance']['source_manifest_sha256']='0'*64
            elif kind=='hash':m['entries'][0]['sha256']='0'*64
            elif kind=='notice':m['entries'][0]['notice']='missing.txt'
            else:next(e for e in m['entries'] if e['path']==build.BROWSER)['derivation']['changes'].append(dict(old='musicvol 0',new='musicvol 1'))
            with self.subTest(kind=kind),self.assertRaises(ValueError):validate(self.root,m)
        for name in ('../escape','/absolute','packages/../../escape'):
            with self.assertRaises(ValueError):build.upstream.confined(self.root,name)

    def test_ambiguous_or_missing_setting_line(self):
        for raw in (b'audio 0\nsoundvol 0\naudio 0\n',b'audio 0\nmusicvol 0\n',b'audio 1\nsoundvol 0\n'):
            with self.assertRaisesRegex(ValueError,'setting count'):build.derive(raw)


if __name__=='__main__':unittest.main()
