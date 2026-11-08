"""Inspected stdlib-only T080 tests; all fixtures confined to this new folder."""
import copy
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.dont_write_bytecode=True
import candidate as c
import validate as v


class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp=Path(tempfile.mkdtemp(prefix='test-',dir=c.HERE))
        def cleanup():
            for p in sorted(self.temp.rglob('*'),key=lambda p:len(p.parts),reverse=True):
                if p.is_symlink() or p.is_file():p.unlink()
                else:p.rmdir()
            self.temp.rmdir()
        self.addCleanup(cleanup)
        self.root=self.temp/'pack'
        self.manifest=c.build(self.root)
        self.p,_=c.inputs()

    def changed(self,name,data):
        (self.root/name).write_bytes(data)
        self.manifest=c.manifest(c.files(self.root))

    def rejected(self):
        with self.assertRaises((ValueError,KeyError,TypeError,IndexError,StopIteration)):
            v.validate(self.root,self.manifest)

    def test_positive_and_second_isolated_generation(self):
        other=self.temp/'second'
        self.assertEqual(c.build(other),self.manifest)
        self.assertEqual(c.files(other),c.files(self.root))
        result=v.validate(self.root,self.manifest)
        # Native open cells include wall-adjacent cells excluded by T076's
        # inflated proxy navigation grid (10420 nodes). They are distinct.
        self.assertEqual(result['map']['open_cells'],11752)
        self.assertEqual(result['map']['native_yaw_tenths'],[1350,1800,2250,2700,3150,0,450,900])
        self.assertEqual(result['sidecar']['canonical_slots'],32)
        side=json.loads((self.root/c.ANCHORS).read_bytes())
        self.assertEqual(side['deployment_clusters'][0]['slots'][0]['position_q10'],[19072,19072,0])

    def test_gzip_corruption_bounds(self):
        data=(self.root/c.CGZ).read_bytes()
        cases=[data[:-1],data+b'x',data+data,data[:4]+b'\x01'+data[5:],data[:-8]+b'\0'*8,c.gzip(b'x'*(1024*1024+1))]
        for n,bad in enumerate(cases):
            with self.subTest(case=n):
                self.changed(c.CGZ,bad);self.rejected()

    def test_native_headers_and_entities(self):
        raw,_,_=v.decode((self.root/c.CGZ).read_bytes());header=struct.unpack_from('<i',raw,8)[0]
        edits=[(0,b'BAD!'),(4,struct.pack('<i',9)),(12,struct.pack('<i',6)),(16,struct.pack('<i',20)),
               (924,struct.pack('<i',2)),(932,struct.pack('<i',1)),(148,b'\x01'),(981,b'\x00'),
               (header,struct.pack('<h',19)),(header+4,struct.pack('<h',0)),(header+6,struct.pack('<h',450)),
               (header+9,b'\x63'),(header+8*16+9,b'\xff')]
        for n,(offset,value) in enumerate(edits):
            with self.subTest(case=n):
                bad=raw[:offset]+value+raw[offset+len(value):]
                self.changed(c.CGZ,c.gzip(bad));self.rejected()

    def test_rle_invalid_and_geometry(self):
        raw,_,_=v.decode((self.root/c.CGZ).read_bytes());start=struct.unpack_from('<i',raw,8)[0]+21*16
        for n,tail in enumerate([b'\xff\x01',b'\x00\x02\x00\xff\x00',b'\x05',raw[start:-1],raw[start:]+b'\x00',b'\x04\x00\x10\x02\x03\x04\x00\x02\x00'+raw[start+3:]]):
            with self.subTest(case=n):self.changed(c.CGZ,c.gzip(raw[:start]+tail));self.rejected()

    def test_sidecar_source_schema_and_no_grants(self):
        base=c.sidecar(self.p)
        mutations=[lambda s:s.update(unknown=1),lambda s:s.update(schema_version=True),
          lambda s:s['deployment_clusters'][0]['slots'][0].update(position_q10=[19*1024,19*1024,0]),
          lambda s:s['deployment_clusters'][0]['slots'][0].update(position_q10=[19072,19072,5120]),
          lambda s:s['loot'][0].update(stock=10),lambda s:s['loot'][0].update(kind='rifle'),
          lambda s:s['barricades'][0].update(hp=100),lambda s:s['walkers'][0].update(id='BW-L01'),
          lambda s:s['reinforcements'][0]['position_q10'].__setitem__(0,0),
          lambda s:s['predators'].reverse(),lambda s:s['regions'][0]['bounds_q10'].__setitem__(0,0),
          lambda s:s['portals'][0]['position_q10'].__setitem__(0,0),
          lambda s:s['reserved_corridors'].reverse(),lambda s:s['extraction']['bounds_q10'].__setitem__(5,0),
          lambda s:s.update(limitations=[]),lambda s:s.update(source_plan_sha256='0'*64)]
        for n,mutate in enumerate(mutations):
            with self.subTest(case=n):
                side=copy.deepcopy(base);mutate(side);self.changed(c.ANCHORS,c.canonical(side).encode());self.rejected()

    def test_missing_extra_and_symlink(self):
        path=self.root/c.CFG;original=path.read_bytes();path.unlink();self.rejected();path.write_bytes(original)
        extra=self.root/'extra';extra.write_bytes(b'x');self.rejected();extra.unlink()
        path.unlink();path.symlink_to(self.root/'LICENSE.txt');self.rejected()

    def test_manifest_paths_and_schema(self):
        base=copy.deepcopy(self.manifest)
        for path in ('../escape','/tmp/escape','packages/../escape','packages\\escape','C:escape'):
            self.manifest=copy.deepcopy(base);self.manifest['entries'][0]['path']=path;self.rejected()
        self.manifest=copy.deepcopy(base);self.manifest['entries'].append(copy.deepcopy(base['entries'][0]));self.rejected()
        self.manifest=copy.deepcopy(base);self.manifest['runtime']=True;self.rejected()
        self.manifest=copy.deepcopy(base);self.manifest['entries'][0]['bytes']=True;self.rejected()
        self.manifest=copy.deepcopy(base);self.manifest['entries'][0]['notice']='elsewhere';self.rejected()
        self.manifest=copy.deepcopy(base);self.manifest['extra']=1;self.rejected()

    def test_provenance_config_license_modified_even_with_new_hash(self):
        for name in ('PROVENANCE.json','LICENSE.txt',c.CFG):
            with self.subTest(member=name):
                original=(self.root/name).read_bytes()
                self.changed(name,original+b'\n');self.rejected();self.changed(name,original)

    def test_source_pin_mismatch_and_one_shot_output(self):
        pins=dict(c.PINS);pins[c.PLAN]='0'*64
        with patch.object(c,'PINS',pins):self.rejected()
        with self.assertRaises(ValueError):c.build(self.root)
        with self.assertRaises(ValueError):c.q(1.0001)


if __name__=='__main__':unittest.main(verbosity=2)
