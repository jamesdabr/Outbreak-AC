"""FIXTURE_ONLY, no actual game/tool execution. All process/socket effects forbidden."""
import ast,copy,json,re,socket,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import policy,supervise,ownership
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
CONTRACT=json.loads((HERE/'diagnostic-schema.json').read_text())
H='a'*64

class FakeView:
 def __init__(self):self.hashes={};self.documents={};self.texts={};self.sizes={};self.trees={};self.changed=set()
 def regular(self,p):return p not in self.changed
 def hash(self,p):return self.hashes[p]
 def json(self,p):return self.documents[p]
 def text(self,p):return self.texts[p]
 def size(self,p):return self.sizes[p]
 def members(self,p):return set(self.trees[p])
 def aliases(self,p):return set()
 def key(self,p):return p.removeprefix(str(ROOT)+'/')

def fixture():
 """Invented file identities. Cannot authorize RealView or be a game result."""
 v=FakeView();p=dict(schema_version=1,ticket='T067',status='RELEASED',authority=dict(owner='MAIN',decision='D999',path='notes/decisions/FIXTURE_ONLY.md'),execution_release='EXPLICIT_TWO_CLIENT_NATIVE_GAME_EXECUTION',attempt='FIXTURE_ONLY',scope=dict(profile='network-client',role='full-cpp-two-browser-native-game',clients=2,capacity=2,map_revision=2,trusted_only=True,baseline_only=True),accepted_dependencies={k:'ACCEPTED' for k in policy.DEPENDENCIES},files={},trees={},aliases=[],diagnostic_contract=CONTRACT,outputs={'result':'web/transport/results/two-client-T067/runtime-FIXTURE_ONLY','native':'web/server/run/T067-FIXTURE_ONLY'})
 def add(name,role,h=H):v.hashes[name]=h;p['files'][name]={'role':role,'sha256':h}
 make=(ROOT/'source/src/Makefile').read_text();cpp=re.findall(r'([A-Za-z0-9_/]+)\.o',re.search(r'CLIENT_OBJS=\s*\\\n(.*?)\n\nCLIENT_PCH=',make,re.S).group(1))
 for name in ['Makefile','browsernet.h','browsernet_observer.h','sound.h']+[x+'.cpp' for x in cpp]:add('source/src/'+name,'source')
 v.texts['source/src/Makefile']=make
 for name in ['callbacks','compress','host','list','packet','peer','protocol']:add('source/enet/'+name+'.c','source')
 for n in ['enet_websocket.c','enet_websocket.js','enet_ws_bridge.h']:add('web/transport/'+n,'source')
 for n in ['gateway.cjs','gateway-limits.cjs']:add('web/transport/'+n,'gateway')
 add('web/transport/tests/two-client/T067/supervise.py','driver');add('web/transport/vendor/ws-8.21.0/index.js','vendor')
 node='/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node';chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';pw='/Users/jd1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.js';core=pw.replace('/playwright/','/playwright-core/')
 add(node,'node','27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1');add('/private/tmp/outbreak-web-sdk/fixture-sdk','sdk')
 for n in [chrome,pw,core,'/usr/bin/unifdef','/usr/bin/codesign','/usr/sbin/lsof','/bin/ps']:add(n,'tool')
 p['tools']=dict(node=node,browser=chrome,playwright=pw)
 for n in ['game.html','game.js','game.wasm','game.data']:add('web/build/network-out/'+n,'bundle')
 add('web/build/network-out/notices/LICENSE.txt','notice');add('web/build/network-out/build-metadata.json','metadata')
 v.documents['web/build/network-out/build-metadata.json']=dict(profile='NETWORK_CLIENT original-network-media',status='LINKED_NOT_BROWSER_VERIFIED',bundle_id=H,ticket='T066 revision4.0',units=[{}]*61,compiles=[{}]*61,object_reuse=False,stable_inventory=True,claims={'browser_runtime':False})
 p['bundle']=dict(root='web/build/network-out',runtime=dict(shell='game.html',js='game.js',wasm='game.wasm',data='game.data'),notices=['notices/LICENSE.txt'],metadata='build-metadata.json',metadata_assertions={k:dict(path=[field],value=value) for k,field,value in [('profile','profile','NETWORK_CLIENT original-network-media'),('status','status','LINKED_NOT_BROWSER_VERIFIED'),('artifact_id','bundle_id',H)]})
 # D064 is real read-only acceptance DATA; file IO remains a fake view.
 acceptance='notes/decisions/D064-accepted-network-artifact.json';a=json.loads((ROOT/acceptance).read_text());add(acceptance,'authority',policy.sha((ROOT/acceptance).read_bytes()));v.documents[acceptance]=a
 for n in list(p['files']):
  if n.startswith('web/build/network-out/') and n not in a['published_files']:p['files'].pop(n);v.hashes.pop(n)
 for n,h in a['published_files'].items():add(n,'notice' if '/notices/' in n else ('metadata' if n.endswith('.json') else 'bundle'),h)
 for pk,hk in [('build_pins','build_pins_sha256'),('verifier','verifier_sha256'),('verification_receipt','verification_receipt_sha256')]:add(a[pk],'authority' if pk=='build_pins' else 'metadata',a[hk])
 p['bundle']['runtime']=dict(shell='index.html',js='index.js',wasm='index.wasm',data='index.data');p['bundle']['notices']=[n.removeprefix('web/build/network-out/') for n in a['published_files'] if '/notices/' in n]
 p['bundle']['metadata_assertions']['artifact_id']['value']=a['bundle_id'];v.documents['web/build/network-out/build-metadata.json']['bundle_id']=a['bundle_id']
 manifest=json.loads((ROOT/'web/assets/network-profile/manifest.json').read_text())
 v.documents['web/assets/network-profile/manifest.json']=manifest;add('web/assets/network-profile/manifest.json','pack',policy.PACK_HASH)
 for e in manifest['entries']:n='web/assets/network-profile/pack-root/'+e['path'];add(n,'pack',e['sha256']);v.sizes[n]=e['bytes']
 p['pack']=dict(root='web/assets/network-profile/pack-root',manifest='web/assets/network-profile/manifest.json',manifest_sha256=policy.PACK_HASH,files=79,bytes=388791,map_revision=2)
 ident='notes/decisions/D052-native-header-identity.json';identity=json.loads((ROOT/ident).read_text());add(ident,'authority','5441fbb6ed7c9a5e5eae2fff6b89d19ceaa8e3f11d0e557357791a01eed471ec');v.documents[ident]=identity
 for n,h in [(identity['path'],identity['current_sha256']),(identity['preserved_original'],identity['original_compile_sha256']),(identity['unifdef'],identity['unifdef_sha256'])]:add(n,'tool' if n.startswith('/') else 'source',h)
 ledger='web/server/lifecycle/build-report.json';add(ledger,'metadata');v.documents[ledger]={'modes':{'release':{'compile':[{'dependencies':{'source/src/sound.h':identity['original_compile_sha256']}}]}}}
 native='web/server/out-lifecycle/release/ac_server';add(native,'native',policy.NATIVE_HASH)
 for n,h in [('web/server/deps-signed/SDL2.framework/Versions/A/SDL2','5faae862816a57f36e11164dfbf5500021a2fbe65a0b23297c9697738c1c9767'),('web/server/deps-signed/SDL2.framework/Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi','62e00aa847d78ed4d1f6188ade82c0b271b73c2278c6bac9b08056eb036e8de0')]:add(n,'library',h)
 p['native']=dict(binary=native,sha256=policy.NATIVE_HASH,dependency_ledger=ledger,sound_identity=ident,argv_tail=policy.native_arguments(),parameters=policy.parameters(),rotation=policy.rotation())
 add(p['authority']['path'],'authority');add(CONTRACT['accepted_handoff'],'schema')
 roots=dict(source='source/src',core='source/enet',driver='web/transport/tests/two-client/T067',sdk='/private/tmp/outbreak-web-sdk',vendor='web/transport/vendor/ws-8.21.0',bundle='web/build/network-out',pack=p['pack']['root'],browser='/Applications/Google Chrome.app',playwright=str(Path(pw).parent),playwright_core=str(Path(core).parent))
 for role,root in roots.items():members=sorted(n[len(root)+1:] for n in p['files'] if n.startswith(root+'/'));v.trees[root]=list(members);p['trees'][role]=dict(root=root,members=members)
 return p,v

def sample(cn=0,x=0,frame=10):
 counters=dict.fromkeys(CONTRACT['counter_keys'],0);counters.update(map_receipts=1,spawn_acknowledgments=1,milestones=4,begin_calls=1)
 events=[dict(kind=0,milestone=0,cn=-1,life=-1,error=0,at_ms=t) for t in (0,10)]+[dict(kind=1,milestone=i,cn=cn,life=-1 if i<4 else 0,error=0,at_ms=10+i*10) for i in range(1,5)]
 return dict(network=dict(schema_version=1,profile='network-client',state='BN_ACTIVE',error=0,map_name='dev_outbreak_browser',map_revision=2,own=dict(cn=cn,life=0,state=0,position=[x,0,8]),remotes=[dict(cn=1-cn,life=0,position=[0,0,8],parse_count=1,last_parse_ms=50)],counters=counters,events=events,coverage='owned client send/local receive paths only; main/local server unobserved'),diagnostics=dict(schema_version=1,profile='network-client',phase='running',frame_count=frame,rendered_frame_count=frame,map_name='dev_outbreak_browser',player_position=[x,0,8],input_locked=True,runtime_errors=[]),timing=dict(schema_version=1,frame_id=frame,raw_elapsed_ms=16,prediction_elapsed_ms=16,lifecycle_state=4,embedded_server_path_compiled=False),browser=dict(now_ms=100,focused=True,visibility='visible',network_frozen=True,timing_frozen=True,canvas_width=1280,canvas_height=720),model=None,audio=None)

def startup_sample(raw=1047):
 s=sample(frame=0);n=s['network'];n.update(state='BN_OPENING',map_name='',map_revision=0,remotes=[]);n['own'].update(cn=-1,life=-1,state=5)
 n['counters']=dict.fromkeys(CONTRACT['counter_keys'],0);n['counters'].update(begin_calls=1,frame_calls=1,frame_advances=1,ws_frames=1);n['events']=n['events'][:1]
 s['diagnostics'].update(frame_count=1,rendered_frame_count=0,phase='loading',input_locked=False)
 s['timing'].update(raw_elapsed_ms=raw,prediction_elapsed_ms=0,lifecycle_state=1)
 return s

class Preparation(unittest.TestCase):
 def setUp(self):
  self.patches=[patch('subprocess.Popen',side_effect=AssertionError('FORBIDDEN PROCESS')),patch('subprocess.run',side_effect=AssertionError('FORBIDDEN PROCESS')),patch('socket.socket',side_effect=AssertionError('FORBIDDEN NETWORK')),patch('os.system',side_effect=AssertionError('FORBIDDEN PROCESS')),patch('os.posix_spawn',side_effect=AssertionError('FORBIDDEN PROCESS'))]
  for p in self.patches:p.start()
 def tearDown(self):
  for p in self.patches:p.stop()
 def checkpins(self,p,v):
  data=json.dumps(p).encode();return policy.validate_pins(data,policy.sha(data),'FIXTURE_ONLY',v)
 def test_fixture_only_complete_gate(self):
  p,v=fixture();self.assertEqual(self.checkpins(p,v)['ticket'],'T067')
 def test_negative_pins_before_effects(self):
  cases={
   'authority':lambda p:p['authority'].update(owner='worker'),
   'unreleased':lambda p:p.update(status='PREPARED'),
   'release':lambda p:p.update(execution_release='BUILD_ONLY'),
   'profile':lambda p:p['scope'].update(profile='offline'),
   'role':lambda p:p['scope'].update(role='socket-only'),
   'dependency':lambda p:p['accepted_dependencies'].update(T070='SUBMITTED'),
   'verifier':lambda p:p['accepted_dependencies'].pop('T072'),
   'observer_correction_missing':lambda p:p['accepted_dependencies'].pop('T077'),
   'observer_correction_unaccepted':lambda p:p['accepted_dependencies'].update(T077='SUBMITTED'),
   'bundle':lambda p:p['bundle']['runtime'].pop('wasm'),
   'root':lambda p:p['bundle'].update(root='web/build/out'),
   'pack':lambda p:p['pack'].update(map_revision=1),
   'capacity':lambda p:p['native']['argv_tail'].__setitem__(2,'-c1'),
   'output':lambda p:p['outputs'].update(native='source/runtime'),
   'source':lambda p:p['files'].pop('source/src/main.cpp'),
   'tool':lambda p:p['files'].pop('/bin/ps'),
   'path':lambda p:p['bundle']['runtime'].update(shell='../game.html'),
   'metadata':lambda p:p['bundle']['metadata_assertions']['profile'].update(value='offline'),
   'hash':lambda p:p['files']['source/src/Makefile'].update(sha256='b'*64),
   'missing':lambda p:p.pop('files'),
  }
  for name,mutate in cases.items():
   with self.subTest(name=name),tempfile.TemporaryDirectory(prefix='T067-fixture-') as tmp:
    p,v=fixture();mutate(p);root=Path(tmp);folder=root/'notes/decisions';folder.mkdir(parents=True);pin=folder/'FIXTURE_ONLY.json';data=json.dumps(p).encode();pin.write_bytes(data)
    class Effects:
     called=False
     def run(self,*args):self.called=True;raise AssertionError('runtime effect')
    effects=Effects()
    with self.assertRaises((policy.Refused,KeyError)):supervise.gated_execute(root,pin,policy.sha(data),'FIXTURE_ONLY',effects,v)
    self.assertFalse(effects.called);self.assertFalse((root/'web').exists())
 def test_missing_and_digest_authority(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)
   with self.assertRaises(policy.Refused):supervise.authorize(root,root/'notes/decisions/missing.json',H,'x')
  p,v=fixture()
  with self.assertRaises(policy.Refused):policy.validate_pins(json.dumps(p).encode(),'0'*64,'FIXTURE_ONLY',v)
 def test_authorized_fixture_calls_fake_effect_only(self):
  with tempfile.TemporaryDirectory(prefix='T067-fixture-') as tmp:
   root=Path(tmp);folder=root/'notes/decisions';folder.mkdir(parents=True);pin=folder/'FIXTURE_ONLY.json';p,v=fixture();data=json.dumps(p).encode();pin.write_bytes(data)
   class Effects:
    called=0
    def run(self,pins,receipt):self.called+=1;return {'kind':'FIXTURE_ONLY','receipt':receipt}
   effects=Effects();result=supervise.gated_execute(root,pin,policy.sha(data),'FIXTURE_ONLY',effects,v);self.assertEqual(effects.called,1);self.assertEqual(result['kind'],'FIXTURE_ONLY');self.assertFalse((root/'web').exists())
 def test_membership_and_symlink_change(self):
  for change in ['extra','missing','symlink']:
   p,v=fixture()
   if change=='extra':v.trees['source/src'].append('extra.cpp')
   elif change=='missing':v.trees['source/src'].remove('main.cpp')
   else:v.changed.add('source/src/main.cpp')
   with self.assertRaises(policy.Refused):self.checkpins(p,v)
 def test_metadata_cannot_substitute_socket_fixture(self):
  p,v=fixture();v.documents['web/build/network-out/build-metadata.json']['compiles']=[{}]
  with self.assertRaises(policy.Refused):self.checkpins(p,v)
 def test_real_pack_read_only_data(self):
  manifest=ROOT/'web/assets/network-profile/manifest.json';self.assertEqual(policy.sha(manifest.read_bytes()),policy.PACK_HASH);entries=json.loads(manifest.read_text())['entries'];self.assertEqual(len(entries),79)
  for e in entries:
   b=(ROOT/'web/assets/network-profile/pack-root'/e['path']).read_bytes();self.assertEqual(len(b),e['bytes']);self.assertEqual(policy.sha(b),e['sha256'])
 def test_routes(self):
  p,_=fixture();self.assertTrue(policy.route('/',p).endswith('index.html'))
  self.assertEqual(policy.request_route('GET','/favicon.ico',p),(204,None))
  for method,raw in [('POST','/favicon.ico'),('GET','/favicon.ico?x=1'),('GET','/favicon.ico/'),('HEAD','/'),('GET','/unknown')]:
   with self.subTest(method=method,raw=raw),self.assertRaises(policy.Refused):policy.request_route(method,raw,p)
  for route in ['/../config','/game.js?cap=secret','/%2e%2e','/build-metadata.json','/source/src/main.cpp','//game.js','/notices/../game.js']:
   with self.subTest(route=route),self.assertRaises(policy.Refused):policy.route(route,p)
 def test_genuine_auto_spawn_fixture_valid(self):
  s=sample();self.assertEqual(s['network']['counters']['spawn_requests'],0);policy.observation(s,CONTRACT,True)
 def test_negative_diagnostics(self):
  cases=[lambda s:s['network'].update(profile='fixture'),lambda s:s['network'].update(map_revision=1),lambda s:s['network'].update(error=15),lambda s:s['network'].update(events=[]),lambda s:s['network']['counters'].update(spawn_acknowledgments=0),lambda s:s['network']['own'].update(state=1),lambda s:s['timing'].update(embedded_server_path_compiled=True),lambda s:s['browser'].update(visibility='hidden'),lambda s:s['diagnostics'].update(runtime_errors=['GPU failure']),lambda s:s['network']['events'][-1].update(at_ms=15010),lambda s:s['network']['remotes'][0].update(cn=0),lambda s:s['network'].update(coverage='global zero fallback')]
  for i,mutate in enumerate(cases):
   with self.subTest(case=i):
    s=sample();mutate(s)
    with self.assertRaises(policy.Refused):policy.observation(s,CONTRACT,True)
 def test_stage_lag_must_eventually_settle(self):
  s=sample();s['timing']['lifecycle_state']=3
  with self.assertRaises(policy.Refused):policy.observation(s,CONTRACT,True)
  s['timing']['lifecycle_state']=4;policy.observation(s,CONTRACT,True)
 def test_passive_receiver_focus_honest(self):
  s=sample();s['browser']['focused']=False;policy.observation(s,CONTRACT,True)
 def test_cross_receipts_fixture_only(self):
  a0,a1,b0,b1=sample(),sample(x=3,frame=12),sample(cn=1),sample(cn=1,frame=12);b1['network']['remotes'][0].update(position=[3,0,8],parse_count=2,last_parse_ms=60)
  policy.cross_receipt(a0,a1,b0,b1,1000)
  for field in ['own_only','frozen','duplicate','old_parse','wrong_position','late','unfocused']:
   a,b,c,d=copy.deepcopy((a0,a1,b0,b1));elapsed=1000
   if field=='own_only':d['network']['remotes']=[]
   elif field=='frozen':d['timing']['frame_id']=10
   elif field=='duplicate':d['network']['own']['cn']=0
   elif field=='old_parse':d['network']['remotes'][0]['parse_count']=1
   elif field=='wrong_position':d['network']['remotes'][0]['position']=[99,99,8]
   elif field=='unfocused':a['browser']['focused']=False
   else:elapsed=2001
   with self.subTest(field=field),self.assertRaises(policy.Refused):policy.cross_receipt(a,b,c,d,elapsed)
 def test_cleanup_missing_never_success(self):
  c=dict.fromkeys(['keys_released','contexts_closed','browsers_stopped','profiles_removed','gateway_closed','static_closed','groups_reaped','handles_empty','ports_released'],True);c.update(native_exit=0,kill_fallback=False,native_shutdown_ms=10,gateway_close_ms=10);policy.cleanup_ok(c)
  for k in c:
   d=copy.deepcopy(c);d.pop(k)
   with self.subTest(key=k),self.assertRaises(policy.Refused):policy.cleanup_ok(d)
 def test_partial_start_node_failure_ownership(self):
  exe='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';root='/tmp/FIXTURE_ONLY'
  birth='Sun Nov 8 01:01:01 2026'
  rows=ownership.parse(f'10 1 10 {birth} {exe} --user-data-dir={root}/browser-temp-A/playwright_chromiumdev_profile-x --headless\n11 10 10 {birth} helper\n20 1 20 {birth} {exe} --user-data-dir=/Users/real/profile\n21 20 20 {birth} helper')
  selected=ownership.select(rows,root,exe);self.assertEqual([r['pid'] for r in selected],[10,11]);self.assertFalse(ownership.same_identity(selected[0],dict(selected[0],command='unrelated reused PID')))
  self.assertTrue(ownership.same_identity(selected[0],dict(selected[0],ppid=1)))
  self.assertFalse(ownership.same_identity(selected[0],dict(selected[0],birth='later PID reuse')))
  known={r['pid']:r for r in selected};calls=[]
  current={r['pid']:r for r in rows};current[10]=dict(current[10],ppid=1)
  self.assertEqual(ownership.signal_owned(known,current,lambda pid,sig:calls.append((pid,sig)),'TERM'),[11,10]);self.assertEqual(calls,[(11,'TERM'),(10,'TERM')])
  calls.clear();current[10]=dict(current[10],birth='later PID reuse');current.pop(11)
  self.assertEqual(ownership.signal_owned(known,current,lambda pid,sig:calls.append((pid,sig)),'KILL'),[]);self.assertEqual(calls,[])
  self.assertEqual(ownership.select(rows,'/other-attempt',exe),[])
 def test_redaction_deadlines_and_plan(self):
  cap='abcdefghijklmnopqrstuA';self.assertTrue(policy.canonical_token(cap));self.assertFalse(policy.canonical_token(cap[:-1]+'B'))
  data=policy.redact({'url':'ws://x/enet?cap='+cap,'token':cap,'why':'GPU failure '+cap},[cap]);self.assertNotIn(cap,json.dumps(data));self.assertIn('GPU failure',data['why'])
  self.assertEqual(supervise.plan()['status'],'NOT_RUN')
 def test_source_only_no_js_execution(self):
  for f in HERE.glob('*.py'):ast.parse(f.read_text())
  js=(HERE/'observe.cjs').read_text();self.assertNotIn('Module.ccall',js);self.assertIn('browser-ownership.json',js);self.assertIn("fresh.network?.state==='BN_JOINING'",js);self.assertIn("--disable-background-timer-throttling",js)
 def test_T077_historical_snapshot_matches_original_pins(self):
  base=ROOT/'web/transport/results/two-client-T067/source-T075-1';manifest=json.loads((base/'manifest.json').read_text());pins=json.loads((ROOT/'notes/decisions/D068-two-client-game-pins.json').read_text());old=json.loads((ROOT/'web/transport/results/two-client-T067/preparation-20261108-freeze-1/result.json').read_text())['source_files_sha256']
  self.assertEqual(len(manifest['files']),7)
  for row in manifest['files']:self.assertEqual(policy.sha((ROOT/row['snapshot']).read_bytes()),row['sha256']);self.assertEqual(row['sha256'],pins['files'][row['original']]['sha256']);self.assertEqual(row['sha256'],old[row['original']])
 def test_T077_long_genuine_frame0_startup_then_resample(self):
  s=startup_sample();original=copy.deepcopy(s);self.assertEqual(policy.timing_classification(s),'STARTUP_FRAME0');self.assertEqual(s,original)
  with self.assertRaises(policy.Refused):policy.observation(s,CONTRACT,True)
  # Source allows first frame to see actual OPEN before its frame publication.
  joining=copy.deepcopy(s);joining['network']['state']='BN_JOINING';joining['network']['events']*=2;joining['timing']['lifecycle_state']=3;self.assertEqual(policy.timing_classification(joining),'STARTUP_FRAME0')
  later=sample(frame=4);self.assertEqual(policy.timing_classification(later),'LATER_FRAME');policy.observation(later,CONTRACT,True)
 def test_T077_invalid_or_ambiguous_frame0(self):
  changes=[lambda s:s['timing'].pop('frame_id'),lambda s:s['timing'].update(frame_id=False),lambda s:s['diagnostics'].update(frame_count=4),lambda s:s['diagnostics'].update(rendered_frame_count=1),lambda s:s['network']['counters'].update(frame_advances=2),lambda s:s['network']['counters'].update(ws_frames=0),lambda s:s['network']['counters'].update(repeated_begin=1),lambda s:s['network']['counters'].pop('frame_calls'),lambda s:s['network']['own'].update(cn=0),lambda s:s['network'].update(state='BN_ACTIVE'),lambda s:s['network']['events'][0].update(kind=1),lambda s:s['network'].update(map_revision=False),lambda s:s['browser'].update(network_frozen=False)]
  for i,change in enumerate(changes):
   with self.subTest(case=i):
    s=startup_sample();change(s)
    with self.assertRaises(policy.Refused):policy.timing_classification(s)
  short=startup_sample(raw=16);short['diagnostics']['frame_count']=2
  with self.assertRaises(policy.Refused):policy.timing_classification(short)
 def test_T077_later_gap_and_backend_error_still_fail(self):
  s=sample(frame=1);s['timing']['raw_elapsed_ms']=1000;self.assertEqual(policy.timing_classification(s),'LATER_FRAME')
  for frame in [1,2,100]:
   s=sample(frame=frame);s['timing']['raw_elapsed_ms']=1001
   with self.subTest(frame=frame),self.assertRaises(policy.Refused):policy.timing_classification(s)
  for change in [lambda s:s['network'].update(error=15,state='BN_FAILED'),lambda s:s['network'].update(error=2),lambda s:s['network']['counters'].update(join_timeouts=1),lambda s:s['browser'].update(visibility='hidden'),lambda s:s['diagnostics'].update(runtime_errors=['actual fatal'])]:
   s=startup_sample();change(s)
   with self.assertRaises(policy.Refused):policy.timing_classification(s)
 def test_T077_bounded_last_first_active_and_redaction(self):
  initial=sample();last=startup_sample();last['network'].update(state='BN_FAILED',error=15);last['diagnostics']['runtime_errors']=['actual error ws://127.0.0.1/enet?cap=abcdefghijklmnopqrstuA']
  rows={'A':{'last':sample(frame=20),'first_active':initial,'startup':None},'B':{'last':last,'first_active':None,'startup':startup_sample()}}
  self.assertIs(policy.bounded_failure_samples(rows,('A','B')),rows);self.assertEqual(rows['A']['first_active']['timing']['frame_id'],10);self.assertEqual(rows['B']['last']['network']['error'],15)
  encoded=json.dumps(policy.redact(rows,['abcdefghijklmnopqrstuA']));self.assertNotIn('abcdefghijklmnopqrstuA',encoded);self.assertIn('actual error',encoded)
 def test_T077_missing_or_unbounded_failure_samples(self):
  good={'A':{'last':sample(),'first_active':sample(),'startup':None}}
  changes=[lambda v:v['A'].update(last=None),lambda v:v.update(C=copy.deepcopy(v['A'])),lambda v:v['A']['last']['network'].update(events=[{}]*513),lambda v:v['A']['last']['network'].update(remotes=[{}]*257),lambda v:v['A']['last']['diagnostics'].update(runtime_errors=['x']*513),lambda v:v['A']['last']['diagnostics'].update(runtime_errors=['x'*(1024*1024)]),lambda v:v['A']['last'].pop('timing'),lambda v:v['A']['first_active']['network'].update(state='BN_OPENING')]
  for i,change in enumerate(changes):
   with self.subTest(case=i):
    v=copy.deepcopy(good);change(v)
    with self.assertRaises(policy.Refused):policy.bounded_failure_samples(v,('A',))
  with self.assertRaises(policy.Refused):policy.bounded_failure_samples(good,('A','B'))
 def test_T077_failed_partial_join_all_final_udp_tuples(self):
  # Actual historical receipt used as immutable DATA only. No runtime effect.
  old=json.loads((ROOT/'web/transport/results/two-client-T067/runtime-T075-1/result.json').read_text())
  self.assertEqual(old['status'],'FAIL');self.assertNotIn('gateway_receipt',old['observer'])
  ports,errors=policy.gateway_cleanup_ports(old['observer']);self.assertEqual(ports,[61734,62986]);self.assertEqual(errors,[])
  p=copy.deepcopy(old['observer']);p['gateway_receipt']=copy.deepcopy(p['gateway_final']);self.assertEqual(policy.gateway_cleanup_ports(p),(ports,[]))
  for bad in [{'address':'0.0.0.0','port':61734,'family':'IPv4'},{'address':'127.0.0.1','port':True,'family':'IPv4'},{'address':'127.0.0.1','port':65536,'family':'IPv4'},{'address':'127.0.0.1','port':61734,'family':'IPv6'},{'address':'127.0.0.1','port':61734,'family':'IPv4','protocol':'TCP'},None]:
   p=copy.deepcopy(old['observer']);p['gateway_final']['sessions'][0]['udp_tuple']=bad
   valid,errors=policy.gateway_cleanup_ports(p);self.assertEqual(valid,[62986]);self.assertTrue(errors)
  self.assertTrue(policy.gateway_cleanup_ports({})[1])
  p=copy.deepcopy(old['observer']);p['gateway_final']['sessions'][0].pop('udp_tuple');self.assertTrue(policy.gateway_cleanup_ports(p)[1])
  p={'gateway_receipt':copy.deepcopy(old['observer']['gateway_final'])};self.assertEqual(policy.gateway_cleanup_ports(p)[0],ports);self.assertTrue(policy.gateway_cleanup_ports(p)[1])
 def test_T077_JS_classifier_identity_and_retention_SOURCE(self):
  js=(HERE/'observe.cjs').read_text();table=json.loads(re.search(r'const FIRST_FRAME_IDENTITY = (\{.*\});',js).group(1));self.assertEqual(table,policy.FIRST_FRAME_IDENTITY);self.assertEqual(policy.schema_counter_keys(),CONTRACT['counter_keys'])
  read=js.split('async function read(c){',1)[1].split('async function join(c){',1)[0]
  self.assertLess(read.index("retain(c,'last',sample)"),read.index('classifyTiming(sample)'));self.assertIn("retain(c,'first_active',sample)",read);self.assertIn("retain(c,'startup',sample)",read)
  self.assertIn("if(classifyTiming(s)!=='LATER_FRAME')return false",js);self.assertIn('failure evidence byte bound',js);self.assertNotIn("fail('actual frame gap exceeds backend policy')",js)

if __name__=='__main__':unittest.main(verbosity=2)
