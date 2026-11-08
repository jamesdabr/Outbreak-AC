"""SPDX-License-Identifier: MIT. Targeted structural checks, not engine/runtime proof."""
import gzip
import hashlib
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import zlib

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import generate_pack as gen
from glyphs import glyph
from validate_pack import Invalid, clear, decode_map, decode_png, route, validate


class PackTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'pack'
        self.manifest=gen.generate(self.root)

    def replace(self,name,data):
        (self.root/name).write_bytes(data)
        entry=next(e for e in self.manifest['entries'] if e['path']==name)
        entry['bytes']=len(data)
        entry['sha256']=hashlib.sha256(data).hexdigest()
        self.manifest['raw_bytes']=sum(e['bytes'] for e in self.manifest['entries'])

    def test_complete_declared_pack(self):
        result=validate(self.root,self.manifest)
        self.assertEqual(result['map_cubes'],4096)
        self.assertEqual(result['entities'],9)
        self.assertEqual(len(result['player_starts']),4)
        self.assertEqual(result['runtime_validation'],'NOT RUN')
        self.assertEqual(result['structural_validation'],'PASS')
        self.assertFalse(self.manifest['runtime_verified'])

    def test_two_generation_runs_byte_identical(self):
        first={e['path']:(self.root/e['path']).read_bytes() for e in self.manifest['entries']}
        second=gen.generate(self.root)
        self.assertEqual(gen.canonical(self.manifest),gen.canonical(second))
        self.assertEqual(first,{name:(self.root/name).read_bytes() for name in first})

    def test_empty_sky_aliases_are_original_png(self):
        for side in ('lf','rt','ft','bk','dn','up'):
            name=f'packages/textures/skymaps/_{side}.jpg'
            data=(self.root/name).read_bytes()
            self.assertEqual(data[:8],b'\x89PNG\r\n\x1a\n')
            self.assertEqual(decode_png(data)[:2],(64,64))
            self.assertEqual(next(e for e in self.manifest['entries'] if e['path']==name)['encoded_format'],'PNG')

    def test_png_crc_truncation_and_dimensions(self):
        data=(self.root/'packages/outbreak/fallback.png').read_bytes()
        bad=bytearray(data); bad[40]^=1
        for value in (b'bad signature',data[:-3],bytes(bad),data+b'trailing'):
            with self.subTest(size=len(value)),self.assertRaises(Invalid):
                decode_png(value)
        huge=data[:8]+gen.chunk(b'IHDR',struct.pack('>IIBBBBB',1024,64,8,6,0,0,0))+data[33:]
        with self.assertRaisesRegex(Invalid,'dimensions'):
            decode_png(huge)

    def test_png_bounded_scanline_and_required_notice(self):
        prefix=b'\x89PNG\r\n\x1a\n'+gen.chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,6,0,0,0))
        notice=gen.chunk(b'tEXt',b'License\0'+gen.NOTICE.encode())
        oversized=prefix+notice+gen.chunk(b'IDAT',zlib.compress(b'\0'*10000))+gen.chunk(b'IEND',b'')
        with self.assertRaisesRegex(Invalid,'bounds|scanline'):
            decode_png(oversized)
        no_notice=prefix+gen.chunk(b'IDAT',zlib.compress(b'\0'*5))+gen.chunk(b'IEND',b'')
        with self.assertRaisesRegex(Invalid,'permission notice'):
            decode_png(no_notice)

    def test_font_all_basic_glyphs_nonblank_and_digits_distinct(self):
        for code in range(33,127):
            rows=glyph(chr(code))
            self.assertEqual(len(rows),7)
            self.assertTrue(all(len(row)==5 and set(row)<={'0','1'} for row in rows))
            self.assertTrue(any('1' in row for row in rows))
        self.assertEqual(len({tuple(glyph(c)) for c in '0123456789'}),10)
        self.assertNotEqual(glyph('A'),glyph('B'))
        self.assertEqual(glyph('a'),glyph('A'))
        self.assertEqual(decode_png((self.root/'packages/outbreak/font.png').read_bytes())[:2],(256,128))

    def test_font_atlas_bounds_or_coverage_rejected(self):
        path='config/font.cfg'
        original=(self.root/path).read_bytes()
        self.replace(path,original.replace(b'fontchar 1 0 14 20',b'fontchar 255 0 14 20',1))
        with self.assertRaisesRegex(Invalid,'atlas bounds'):
            validate(self.root,self.manifest)
        self.replace(path,original.replace(b'fontchar 1 0 14 20\n',b'',1))
        with self.assertRaisesRegex(Invalid,'coverage'):
            validate(self.root,self.manifest)

    def test_native_rle_chunks_larger_than_255(self):
        blocks=[bytes((0,2,0))]*600+[bytes((4,0,12,2,3,4,0,2,0))]*300
        encoded=gen.rle(blocks)
        self.assertIn(bytes((255,255)),encoded)
        # Independently count runs rather than invoking encoder for expected bytes.
        self.assertEqual(encoded[:9],bytes((0,2,0,255,255,255,255,255,89)))

    def test_map_crc_truncation_and_header(self):
        data=gen.map_bytes()
        bad=bytearray(data);bad[-8]^=1
        for value in (b'not gzip',data[:-4],bytes(bad),data+b'junk'):
            with self.subTest(size=len(value)),self.assertRaises(Invalid):
                decode_map(value)
        raw=bytearray(gzip.decompress(data))
        struct.pack_into('<i',raw,4,9)
        with self.assertRaisesRegex(Invalid,'version'):
            decode_map(gzip.compress(raw,mtime=0))

    def test_map_entities_encoding_and_clearance(self):
        raw=bytearray(gzip.decompress(gen.map_bytes()))
        header=struct.unpack_from('<i',raw,8)[0]
        # A start moved into the known structure wall must not pass.
        struct.pack_into('<2h',raw,header,26,25)
        with self.assertRaisesRegex(Invalid,'blocked player start'):
            decode_map(gzip.compress(raw,mtime=0))
        raw=bytearray(gzip.decompress(gen.map_bytes()))
        raw[header+8]=11  # MAPMODEL would introduce an undeclared dependency.
        with self.assertRaisesRegex(Invalid,'undeclared entity'):
            decode_map(gzip.compress(raw,mtime=0))

    def test_map_rle_malformed_overrun_and_border(self):
        raw=gzip.decompress(gen.map_bytes())
        header=struct.unpack_from('<i',raw,8)[0]
        count=struct.unpack_from('<i',raw,16)[0]
        geometry=header+count*16
        for broken in (b'\xff\x01',b'\x07',b'\x00',b'\x00\x02\0'+b'\xff\xff'*17):
            with self.subTest(broken=broken[:5]),self.assertRaises(Invalid):
                decode_map(gzip.compress(raw[:geometry]+broken,mtime=0))
        # First unit cube is the world corner: a complete all-open grid violates MINBORD.
        all_open=b''.join([bytes((4,0,12,2,3,4,0,2,0))]*4096)
        with self.assertRaisesRegex(Invalid,'MINBORD'):
            decode_map(gzip.compress(raw[:geometry]+all_open,mtime=0))

    def test_geometry_three_routes_and_collision_radius(self):
        cells,_=decode_map(gen.map_bytes())
        route(cells,[(16,32),(48,32)])
        route(cells,[(16,32),(16,18),(48,18),(48,32)])
        route(cells,[(16,32),(16,46),(48,46),(48,32)])
        self.assertTrue(clear(cells,24.8,25))
        self.assertFalse(clear(cells,25,25))
        self.assertFalse(clear(cells,32,24))
        self.assertTrue(clear(cells,32,32))
        with self.assertRaisesRegex(Invalid,'blocked approach'):
            route(cells,[(16,25),(32,25)])

    def test_no_native_profiles_or_stock_config_references(self):
        cfg='config/browser.cfg'
        self.replace(cfg,(self.root/cfg).read_bytes()+b'\nexec config/menus.cfg\n')
        with self.assertRaisesRegex(Invalid,'unexpected browser config'):
            validate(self.root,self.manifest)
        self.manifest['entries'][0]['path']='../escape'
        with self.assertRaises(Invalid):
            validate(self.root,self.manifest)

    def test_extra_file_and_symlink_rejected_without_overwrite(self):
        extra=self.root/'config/authprivate.cfg'
        extra.write_text('fixture never read by generator')
        with self.assertRaisesRegex(ValueError,'undeclared'):
            gen.generate(self.root)
        with self.assertRaisesRegex(Invalid,'undeclared'):
            validate(self.root,self.manifest)
        extra.unlink()  # Own temporary fixture only.
        image=self.root/'packages/outbreak/fallback.png'
        image.unlink()
        image.symlink_to(self.root/'packages/outbreak/font.png')
        with self.assertRaisesRegex(ValueError,'symlink'):
            gen.generate(self.root)
        with self.assertRaisesRegex(Invalid,'symlink'):
            validate(self.root,self.manifest)

    def test_manifest_hash_and_missing_original_reference(self):
        self.manifest['entries'][0]['sha256']='0'*64
        with self.assertRaisesRegex(Invalid,'hash mismatch'):
            validate(self.root,self.manifest)
        self.manifest=gen.generate(self.root)
        cfg='packages/maps/dev_outbreak_browser.cfg'
        self.replace(cfg,(self.root/cfg).read_bytes().replace(b'outbreak/wall.png',b'stock/not-present.jpg'))
        with self.assertRaisesRegex(Invalid,'missing/non-original texture'):
            validate(self.root,self.manifest)


if __name__=='__main__':
    unittest.main()
