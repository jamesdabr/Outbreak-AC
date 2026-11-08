"""SPDX-License-Identifier: MIT. Original model fixtures; no engine execution."""
import copy
import binascii
import hashlib
from pathlib import Path
import struct
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import generate_models as gen
from validate_models import Invalid,decode_md3,decode_png,decode_config,validate


class ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw={name:gen.model(name)[0] for name in ('survivor','pistol','rifle')}

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'pack'
        self.manifest=gen.generate(self.root)

    def test_original_models_counts_poses_tags(self):
        result,decoded=validate(self.root,self.manifest)
        self.assertEqual(result['declared_files'],19)
        self.assertEqual(result['actual_engine_load'],'NOT RUN')
        self.assertEqual([decoded[n]['frames'] for n in ('survivor','pistol','rifle')],[26,3,3])
        self.assertEqual([decoded[n]['surfaces'][0]['vertices'] for n in ('survivor','pistol','rifle')],[336,96,144])
        self.assertTrue(all(tuple(tags)==('tag_weapon','tag_head') for tags in decoded['survivor']['tags']))
        self.assertAlmostEqual(decoded['survivor']['frame_bounds'][0]['max'][2]/16,5.2,delta=.001)

    def test_generation_byte_identity(self):
        before={e['path']:(self.root/e['path']).read_bytes() for e in self.manifest['entries']}
        second=gen.generate(self.root)
        self.assertEqual(gen.canonical(self.manifest),gen.canonical(second))
        self.assertEqual(before,{n:(self.root/n).read_bytes() for n in before})

    def test_bad_header_counts_offsets_and_truncation(self):
        for offset,value in ((4,14),(76,65),(80,-1),(84,9),(92,0),(96,108),(100,2**30),(104,0)):
            bad=bytearray(self.raw['survivor']);struct.pack_into('<i',bad,offset,value)
            with self.subTest(offset=offset),self.assertRaises(Invalid):decode_md3(bad)
        for bad in (b'',self.raw['survivor'][:-1],self.raw['survivor']+b'junk',b'NOPE'+self.raw['survivor'][4:]):
            with self.assertRaises(Invalid):decode_md3(bad)

    def test_bad_surface_offsets_count_frame_match(self):
        so=struct.unpack_from('<i',self.raw['survivor'],100)[0]
        for relative,value in ((72,1),(76,0),(80,513),(84,1025),(88,-1),(92,1),(96,2**30),(100,-1),(104,0)):
            bad=bytearray(self.raw['survivor']);struct.pack_into('<i',bad,so+relative,value)
            with self.subTest(relative=relative),self.assertRaises(Invalid):decode_md3(bad)

    def test_bad_indices_uv_normals_and_degenerate_geometry(self):
        raw=self.raw['survivor'];so=struct.unpack_from('<i',raw,100)[0]
        ot,ouv,ov=struct.unpack_from('<i',raw,so+88)[0],struct.unpack_from('<i',raw,so+96)[0],struct.unpack_from('<i',raw,so+100)[0]
        for index in (-1,9999):
            bad=bytearray(raw);struct.pack_into('<i',bad,so+ot,index)
            with self.assertRaisesRegex(Invalid,'indices'):decode_md3(bad)
        for uv in (2.0,float('nan')):
            bad=bytearray(raw);struct.pack_into('<f',bad,so+ouv,uv)
            with self.assertRaises(Invalid):decode_md3(bad)
        bad=bytearray(raw);struct.pack_into('<H',bad,so+ov+6,0)
        with self.assertRaisesRegex(Invalid,'normal/winding'):decode_md3(bad)
        bad=bytearray(raw);bad[so+ov+8:so+ov+14]=bad[so+ov:so+ov+6]
        with self.assertRaisesRegex(Invalid,'degenerate'):decode_md3(bad)

    def test_bad_frame_bounds_and_tags(self):
        raw=self.raw['survivor'];to=struct.unpack_from('<i',raw,96)[0]
        for offset,value in ((108,float('nan')),(108+12,9999.),(to+64,1e6),(to+76,2.)):
            bad=bytearray(raw);struct.pack_into('<f',bad,offset,value)
            with self.subTest(offset=offset),self.assertRaises(Invalid):decode_md3(bad)
        bad=bytearray(raw);bad[to+112:to+112+64]=bad[to:to+64]
        with self.assertRaisesRegex(Invalid,'tag names'):decode_md3(bad)
        bad=bytearray(raw);bad[to+2*112:to+3*112]=raw[to+3*112:to+4*112];bad[to+3*112:to+4*112]=raw[to+2*112:to+3*112]
        with self.assertRaisesRegex(Invalid,'tag continuity'):decode_md3(bad)

    def test_config_native_names_ranges_references_and_allowlist(self):
        model=decode_md3(self.raw['survivor']);declared={e['path'] for e in self.manifest['entries']}
        raw=gen.config('survivor')
        for bad in (raw.replace(b'"run" 1 8',b'"crawl" 1 8'),raw.replace(b'"run" 1 8',b'"run" 25 8'),raw.replace(b'md3load tris.md3',b'md3load ../stock.md3'),raw.replace(b'md3skin body skin.png',b'md3skin body stock.png'),raw+b'exec config/native.cfg\n',raw+b'mdlscale $dynamic\n'):
            with self.assertRaises(Invalid):decode_config(bad,'survivor',model,declared)

    def test_png_crc_dimension_and_truncated_data(self):
        raw=gen.png('survivor');self.assertEqual(decode_png(raw),dict(width=64,height=64))
        bad=bytearray(raw);bad[-1]^=1
        for value in (raw[:-5],bytes(bad),raw+b'junk',b'garbage',raw[:33]+raw[8:33]+raw[33:]):
            with self.assertRaises(Invalid):decode_png(value)
        oversized=bytearray(raw);struct.pack_into('>I',oversized,16,256)
        struct.pack_into('>I',oversized,29,binascii.crc32(oversized[12:29])&0xffffffff)
        with self.assertRaisesRegex(Invalid,'dimensions'):decode_png(oversized)

    def test_exact_membership_hash_notices_and_symlinks(self):
        extra=self.root/'unexpected.txt';extra.write_text('owned fixture')
        with self.assertRaisesRegex(ValueError,'undeclared'):gen.generate(self.root)
        with self.assertRaisesRegex(Invalid,'undeclared'):validate(self.root,self.manifest)
        self.assertEqual(extra.read_text(),'owned fixture');extra.unlink()
        m=copy.deepcopy(self.manifest);m['entries'][0]['sha256']='0'*64
        with self.assertRaisesRegex(Invalid,'hash'):validate(self.root,m)
        path=self.root/(gen.PREFIX+'pistol/skin.png');path.unlink();path.symlink_to('/outside-model-fixture-not-read')
        with self.assertRaisesRegex(ValueError,'symlink'):gen.generate(self.root)
        with self.assertRaisesRegex(ValueError,'symlink'):validate(self.root,self.manifest)
        self.assertTrue(path.is_symlink())

    def test_metadata_bounds_and_path_escape(self):
        m=copy.deepcopy(self.manifest);m['models']['survivor']['frame_bounds'][0]['max_engine'][2]=999
        with self.assertRaisesRegex(Invalid,'bounds metadata'):validate(self.root,m)
        for path in ('../escape','/absolute',gen.PREFIX+'../elsewhere'):
            with self.assertRaises(ValueError):gen.safe(self.root,path)


if __name__=='__main__':unittest.main()
