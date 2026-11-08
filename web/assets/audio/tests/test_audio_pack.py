"""SPDX-License-Identifier: MIT. Data validation only, never listening/playback."""
import copy
import hashlib
from pathlib import Path
import struct
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import audio_pack as audio


class AudioTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'pack'
        self.manifest=audio.generate(self.root)

    def test_exact_names_formats_and_bounds(self):
        self.assertEqual(set(audio.SPECS),{'proof_tone','pistol','rifle','reload','footstep','walker_attack','predator_front','predator_flank','extraction'})
        result=audio.validate(self.root,self.manifest)
        self.assertEqual(result['cue_count'],9)
        self.assertEqual(result['declared_files'],19)
        self.assertEqual(result['listening'],'NOT RUN')
        for value in result['measurements'].values():
            self.assertTrue(0<value['duration_seconds']<=1)
            self.assertTrue(0<value['peak']<=8191)
            self.assertEqual((value['first_sample'],value['last_sample']),(0,0))

    def test_deterministic_bytes_and_manifest(self):
        first={e['path']:(self.root/e['path']).read_bytes() for e in self.manifest['entries']}
        second=audio.generate(self.root)
        self.assertEqual(audio.canonical(self.manifest),audio.canonical(second))
        self.assertEqual(first,{n:(self.root/n).read_bytes() for n in first})

    def test_malformed_riff_format_and_payload(self):
        original=audio.wav('proof_tone')
        for offset,value in ((4,0),(16,18),(20,3),(22,2),(24,44100),(32,4),(34,8),(40,1)):
            bad=bytearray(original)
            struct.pack_into('<H' if offset in (20,22,32,34) else '<I',bad,offset,value)
            with self.subTest(offset=offset),self.assertRaises(ValueError):
                audio.decode(bytes(bad))
        for bad in (b'not RIFF',original[:-2],original+b'junk',original*2):
            with self.subTest(size=len(bad)),self.assertRaises(ValueError):
                audio.decode(bad)

    def test_silence_peak_endpoints_and_envelope(self):
        original=audio.wav('proof_tone')
        silence=original[:44]+bytes(len(original)-44)
        with self.assertRaisesRegex(ValueError,'nonzero'):
            audio.decode(silence)
        for index,value,message in ((500,10000,'amplitude'),(0,1,'endpoints'),(1,1000,'envelope')):
            bad=bytearray(original)
            struct.pack_into('<h',bad,44+index*2,value)
            with self.subTest(index=index),self.assertRaisesRegex(ValueError,message):
                audio.decode(bytes(bad))

    def test_per_pulse_envelope_rejected(self):
        name=audio.PREFIX+'predator_front.wav'
        path=self.root/name
        bad=bytearray(path.read_bytes())
        struct.pack_into('<h',bad,44+(300*22050//1000)*2,1000)
        path.write_bytes(bad)
        entry=next(e for e in self.manifest['entries'] if e['path']==name)
        entry['sha256']=hashlib.sha256(bad).hexdigest()
        with self.assertRaisesRegex(ValueError,'per-pulse'):
            audio.validate(self.root,self.manifest)

    def test_front_flank_patterns_distinct(self):
        result=audio.validate(self.root,self.manifest)['measurements']
        self.assertEqual(len(result['predator_front']['silent_gaps_ms']),1)
        self.assertEqual(len(result['predator_flank']['silent_gaps_ms']),2)
        self.assertNotEqual(audio.wav('predator_front'),audio.wav('predator_flank'))
        # Intended pitch patterns are explicit generation data, not a listening result.
        self.assertEqual([s[2] for s in audio.SPECS['predator_front'][1]],[330,660])
        self.assertEqual([s[2] for s in audio.SPECS['predator_flank'][1]],[660,440,220])

    def test_undeclared_files_and_symlinks_preserved_and_rejected(self):
        extra=self.root/'unexpected.txt'
        extra.write_text('owned fixture')
        with self.assertRaisesRegex(ValueError,'undeclared'):
            audio.generate(self.root)
        with self.assertRaisesRegex(ValueError,'undeclared'):
            audio.validate(self.root,self.manifest)
        self.assertEqual(extra.read_text(),'owned fixture')
        extra.unlink()
        path=self.root/(audio.PREFIX+'proof_tone.wav')
        path.unlink()
        path.symlink_to('/outside-audio-fixture-never-read')
        with self.assertRaisesRegex(ValueError,'symlink'):
            audio.generate(self.root)
        with self.assertRaisesRegex(ValueError,'symlink'):
            audio.validate(self.root,self.manifest)
        self.assertTrue(path.is_symlink())

    def test_manifest_tampering_membership_and_notices(self):
        for field,value in (('sha256','0'*64),('bytes',0),('original',False)):
            m=copy.deepcopy(self.manifest)
            m['entries'][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                audio.validate(self.root,m)
        m=copy.deepcopy(self.manifest)
        m['entries'].pop()
        with self.assertRaisesRegex(ValueError,'membership'):
            audio.validate(self.root,m)
        notice=self.root/(audio.PREFIX+'pistol.wav.LICENSE.txt')
        notice.write_text('wrong license')
        with self.assertRaises(ValueError):
            audio.validate(self.root,self.manifest)

    def test_traversal_rejected(self):
        for name in ('/absolute','../escape',audio.PREFIX+'../../escape','packages/audio/other.wav'):
            with self.subTest(name=name),self.assertRaises(ValueError):
                audio.safe(self.root,name)


if __name__=='__main__':
    unittest.main()
