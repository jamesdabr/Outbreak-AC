"""FIXTURE_ONLY gates/receipt tests; subprocesses and sockets forbidden."""
import argparse,copy,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'web/transport/tests/two-client/T067'))
import policy,supervise
from test_preparation import fixture
RECEIPT=None
def impaired_fixture():
 p,v=fixture();p.update(ticket='T082',execution_release='EXPLICIT_IMPAIRED_TWO_CLIENT_NATIVE_GAME_EXECUTION',impairment=copy.deepcopy(policy.IMPAIRMENT));p['scope'].update(role='full-cpp-two-browser-native-game-impaired',baseline_only=False);p['accepted_dependencies'].update(T079='ACCEPTED',T082='ACCEPTED')
 p['outputs']={'result':'web/transport/results/impaired-T082/runtime-FIXTURE_ONLY','native':'web/server/run/T082-FIXTURE_ONLY'}
 base='web/transport/tests/impaired/T082';members=sorted(f.name for f in HERE.iterdir() if f.is_file());p['trees']['impairment_driver']={'root':base,'members':members};v.trees[base]=list(members)
 for name in members:p['files'][base+'/'+name]={'role':'driver','sha256':'a'*64};v.hashes[base+'/'+name]='a'*64
 v.documents[base+'/preset.json']=copy.deepcopy(policy.IMPAIRMENT)
 return p,v
class Preparation(unittest.TestCase):
 def setUp(self):
  self.patches=[patch('subprocess.Popen',side_effect=AssertionError('forbidden process')),patch('subprocess.run',side_effect=AssertionError('forbidden process')),patch('socket.socket',side_effect=AssertionError('forbidden socket')),patch('os.system',side_effect=AssertionError('forbidden process')),patch('os.posix_spawn',side_effect=AssertionError('forbidden process'))]
  for p in self.patches:p.start()
 def tearDown(self):
  for p in self.patches:p.stop()
 def test_complete_case_is_fake_effect_only(self):
  p,v=impaired_fixture();data=json.dumps(p).encode()
  with tempfile.TemporaryDirectory(prefix='T082-FIXTURE-') as tmp:
   root=Path(tmp);folder=root/'notes/decisions';folder.mkdir(parents=True);pin=folder/'FIXTURE_ONLY.json';pin.write_bytes(data)
   class Effect:
    def run(self,pins,receipt):return {'kind':'FIXTURE_ONLY','ticket':pins['ticket']}
   self.assertEqual(supervise.gated_execute(root,pin,policy.sha(data),'FIXTURE_ONLY',Effect(),v,'impaired40_drop50')['kind'],'FIXTURE_ONLY');self.assertFalse((root/'web').exists())
 def test_wrong_case_preset_role_membership_never_effects(self):
  cases=[lambda p:p.update(ticket='T067'),lambda p:p.update(execution_release='EXPLICIT_TWO_CLIENT_NATIVE_GAME_EXECUTION'),lambda p:p['scope'].update(role='full-cpp-two-browser-native-game'),lambda p:p['scope'].update(baseline_only=True),lambda p:p['scope'].update(baseline_only=0),lambda p:p['impairment'].update(delay_ms=0),lambda p:p['impairment'].update(drop_every=100),lambda p:p['impairment'].update(schema_version=True),lambda p:p['impairment'].update(extra_hook='x'),lambda p:p['accepted_dependencies'].pop('T082'),lambda p:p['accepted_dependencies'].update(T079='SUBMITTED'),lambda p:p['trees'].pop('impairment_driver'),lambda p:p['files'].pop('web/transport/tests/impaired/T082/shaper.cjs'),lambda p:p['outputs'].update(result='web/transport/results/two-client-T067/runtime-FIXTURE_ONLY')]
  for i,change in enumerate(cases):
   p,v=impaired_fixture();change(p);data=json.dumps(p).encode()
   with self.subTest(case=i),tempfile.TemporaryDirectory(prefix='T082-FIXTURE-') as tmp:
    root=Path(tmp);folder=root/'notes/decisions';folder.mkdir(parents=True);pin=folder/'FIXTURE_ONLY.json';pin.write_bytes(data)
    class Effect:
     called=False
     def run(self,*a):self.called=True;raise AssertionError('runtime effect')
    e=Effect()
    with self.assertRaises((policy.Refused,KeyError)):supervise.gated_execute(root,pin,policy.sha(data),'FIXTURE_ONLY',e,v,'impaired40_drop50')
    self.assertFalse(e.called);self.assertFalse((root/'web').exists())
 def test_default_baseline_schema_remains_separate(self):
  p,v=fixture();data=json.dumps(p).encode();policy.validate_pins(data,policy.sha(data),'FIXTURE_ONLY',v)
  with self.assertRaises(policy.Refused):policy.validate_pins(data,policy.sha(data),'FIXTURE_ONLY',v,'impaired40_drop50')
  p,v=impaired_fixture();data=json.dumps(p).encode()
  with self.assertRaises(policy.Refused):policy.validate_pins(data,policy.sha(data),'FIXTURE_ONLY',v)
  with self.assertRaises(policy.Refused):policy.validate_pins(data,policy.sha(data),'FIXTURE_ONLY',v,'custom_observer')
 def test_membership_and_data_changed(self):
  p,v=impaired_fixture();v.trees['web/transport/tests/impaired/T082'].append('extra.cjs');data=json.dumps(p).encode()
  with self.assertRaises(policy.Refused):policy.validate_pins(data,policy.sha(data),'FIXTURE_ONLY',v,'impaired40_drop50')
  p,v=impaired_fixture();v.documents['web/transport/tests/impaired/T082/preset.json']['delay_ms']=41;data=json.dumps(p).encode()
  with self.assertRaises(policy.Refused):policy.validate_pins(data,policy.sha(data),'FIXTURE_ONLY',v,'impaired40_drop50')
 def test_node_fixture_receipt_independent_validation(self):
  self.assertEqual(RECEIPT['kind'],'FIXTURE_ONLY_FAKE_FACTORY_CLOCK_TIMERS');self.assertEqual(RECEIPT['actual_sockets'],0);policy.shaper_receipt(RECEIPT['profile_receipt'])
 def test_receipt_no_loss_wrong_counts_latency_cleanup_refused(self):
  mutations=[lambda r:r['directions']['up'].update(dropped=0),lambda r:r['directions']['down'].update(delivered=0),lambda r:r['directions']['up'].update(delay_min_ms=39),lambda r:r['directions']['up'].update(delay_max_ms=500),lambda r:r['directions']['up'].update(callback_calls=99),lambda r:r['directions']['up'].update(peak_datagrams=65),lambda r:r['directions']['up'].update(pending_bytes=1),lambda r:r['directions']['up']['histogram'].update({'40_49':99}),lambda r:r['sockets'][0]['up'].update(observed=51),lambda r:r['events'][0].update(ordinal=49),lambda r:r['events'].pop(),lambda r:r['cleanup'].update(restored=False),lambda r:r['cleanup'].update(timers=1),lambda r:r['faults'].append('native error'),lambda r:r.update(events=[{}]*513),lambda r:r.pop('sockets')]
  for i,change in enumerate(mutations):
   r=copy.deepcopy(RECEIPT['profile_receipt']);change(r)
   with self.subTest(case=i),self.assertRaises((policy.Refused,KeyError)):policy.shaper_receipt(r)
 def test_private_hook_SOURCE_only(self):
  observer=(ROOT/'web/transport/tests/two-client/T067/observe.cjs').read_text();self.assertLess(observer.index('shaper=fixed.install'),observer.index("const {startGateway}=require"));self.assertIn('if(impaired)',observer)
  entry=(HERE/'run.py').read_text();self.assertNotIn('--observer',entry);self.assertNotIn('--case',entry);self.assertNotIn('--flags',entry)
  shim=(HERE/'shaper.cjs').read_text();self.assertNotIn("require('node:dgram')",shim);self.assertNotIn('process.env',shim);self.assertNotIn('createServer',shim)
 def test_historical_driver_and_actual_receipts_unchanged(self):
  base=ROOT/'web/transport/results/two-client-T067';m=json.loads((base/'source-T079-1/manifest.json').read_text());pins=json.loads((ROOT/'notes/decisions/D074-two-client-game-pins.json').read_text());self.assertEqual(len(m['files']),7)
  for row in m['files']:self.assertEqual(policy.sha((ROOT/row['snapshot']).read_bytes()),row['sha256']);self.assertEqual(row['sha256'],pins['files'][row['original']]['sha256'])
  for attempt in ['T075','T079']:
   frozen=json.loads((base/('runtime-'+attempt+'-1')/'freeze.json').read_text())
   for name,h in frozen['files_sha256'].items():self.assertEqual(policy.sha((ROOT/name).read_bytes()),h)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--receipt',required=True,type=Path);args,extra=a.parse_known_args();RECEIPT=json.loads(args.receipt.read_text());unittest.main(argv=[sys.argv[0],*extra],verbosity=2)
