"""T049 inert text fixtures test merge rules; no engine/media execution."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import assemble as assembly
from validate import validate


class MergeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.repo=Path(self.temp.name);self.output=self.repo/'output'
        self.specs=[]
        for key in ('map','audio','models'):
            files={'config/browser.cfg':b'audio 0\nmap-restriction fixture\nisolatecontext MAPCFG\nisolatecontext MDLCFG\nsealcontexts\n','LICENSE.txt':b'fixture map notice'} if key=='map' else {f'packages/{key}/fixture.txt':b'authored inert fixture',f'packages/{key}/LICENSE.txt':b'fixture notice'}
            root=self.repo/key/'pack-root';root.mkdir(parents=True)
            notice='LICENSE.txt' if key=='map' else f'packages/{key}/LICENSE.txt'
            entries=[]
            for name,raw in sorted(files.items()):
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
                entries.append(dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),notice=notice,license='MIT',original=True))
            mp=self.repo/key/'manifest.json';mp.write_text(json.dumps(dict(entries=entries)))
            self.specs.append(dict(id=key,manifest=f'{key}/manifest.json',root=f'{key}/pack-root',sha256=hashlib.sha256(mp.read_bytes()).hexdigest(),count=2))

    def build(self):return assembly.assemble(self.repo,self.output,self.specs,6)
    def verify(self,manifest):return validate(self.repo,self.output,manifest,self.specs,6)

    def repin(self,spec,manifest):
        path=self.repo/spec['manifest'];path.write_text(json.dumps(manifest));spec['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()

    def test_exact_merge_and_determinism(self):
        first=self.build();self.assertEqual(self.verify(first)['copied_byte_identical'],5)
        before={p.relative_to(self.output).as_posix():p.read_bytes() for p in self.output.rglob('*') if p.is_file()}
        second=self.build()
        self.assertEqual(assembly.canonical(first),assembly.canonical(second))
        self.assertEqual(before,{n:(self.output/n).read_bytes() for n in before})
        self.assertIn(assembly.INSERT+assembly.MARKER,(self.output/'config/browser.cfg').read_bytes())
        self.assertNotIn(assembly.INSERT,(self.repo/'map/pack-root/config/browser.cfg').read_bytes())

    def test_manifest_pin_rejected_before_writes(self):
        (self.repo/'map/manifest.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'pin mismatch'):self.build()
        self.assertFalse(self.output.exists())

    def test_source_payload_hash_and_extra_file(self):
        source=self.repo/'audio/pack-root/packages/audio/fixture.txt';source.write_text('changed')
        with self.assertRaisesRegex(ValueError,'hash/size'):self.build()
        source.write_bytes(b'authored inert fixture')
        (self.repo/'audio/pack-root/undeclared.txt').write_text('owned test artifact')
        with self.assertRaisesRegex(ValueError,'membership'):self.build()

    def test_source_collision_rejected(self):
        spec=self.specs[1];path=self.repo/spec['manifest'];manifest=json.loads(path.read_text())
        source=self.repo/spec['root']/'packages/audio/fixture.txt';raw=source.read_bytes();source.unlink()
        manifest['entries'][1]['path']='config/browser.cfg'
        target=self.repo/spec['root']/'config/browser.cfg';target.parent.mkdir();target.write_bytes(raw)
        self.repin(spec,manifest)
        with self.assertRaisesRegex(ValueError,'collision'):self.build()

    def test_source_traversal_and_symlink(self):
        spec=self.specs[1];mp=self.repo/spec['manifest'];original=json.loads(mp.read_text())
        for name in ('../escape','/absolute','packages/audio/../fixture.txt'):
            with self.assertRaises(ValueError):assembly.confined(self.repo/spec['root'],name)
        target=self.repo/spec['root']/'packages/audio/fixture.txt';target.unlink();target.symlink_to('/outside-merge-fixture-not-read')
        with self.assertRaisesRegex(ValueError,'symlink'):self.build()
        self.assertTrue(target.is_symlink())

    def test_extra_permission_or_setting_change_rejected(self):
        manifest=self.build();path=self.output/'config/browser.cfg';original=path.read_bytes()
        for bad in (original+b'scriptcontext MDLCFG exec\n',original.replace(b'audio 0',b'audio 1'),original.replace(assembly.INSERT,b'')):
            path.write_bytes(bad)
            with self.assertRaisesRegex(ValueError,'extra command mismatch'):self.verify(manifest)
        path.write_bytes(original)
        self.verify(manifest)

    def test_output_symlink_or_undeclared_preserved(self):
        manifest=self.build();extra=self.output/'extra.txt';extra.write_text('keep this fixture')
        with self.assertRaises(ValueError):self.build()
        with self.assertRaises(ValueError):self.verify(manifest)
        self.assertEqual(extra.read_text(),'keep this fixture');extra.unlink()
        path=self.output/'config/browser.cfg';path.unlink();path.symlink_to('/outside-stage-fixture-not-read')
        with self.assertRaisesRegex(ValueError,'symlink'):self.build()
        with self.assertRaisesRegex(ValueError,'symlink'):self.verify(manifest)
        self.assertTrue(path.is_symlink())

    def test_provenance_recipe_or_membership_tampering(self):
        manifest=self.build()
        for kind in ('recipe','provenance','membership'):
            bad=copy.deepcopy(manifest)
            if kind=='recipe':next(e for e in bad['entries'] if e['path']=='config/browser.cfg')['derivation']['inserted_lines'].append('scriptcontext MDLCFG exec')
            elif kind=='provenance':bad['entries'][0]['provenance']['input_manifest_sha256']='0'*64
            else:bad['entries'].pop()
            with self.subTest(kind=kind),self.assertRaises(ValueError):self.verify(bad)


if __name__=='__main__':unittest.main()
