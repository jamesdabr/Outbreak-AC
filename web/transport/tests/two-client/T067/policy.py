"""T067 preparation: pure gates/evidence checks. No process, socket or staging imports."""
import hashlib,json,math,re
from pathlib import PurePosixPath

class Refused(ValueError): pass
def require(value,why):
 if not value: raise Refused(why)
def exact(value,keys,why):require(type(value) is dict and set(value)==set(keys),why)
def sha(data):return hashlib.sha256(data).hexdigest()
def relative(value):
 require(type(value) is str and value and '\\' not in value and '%' not in value and '?' not in value and '#' not in value,'noncanonical path')
 p=PurePosixPath(value);require(not p.is_absolute() and all(n not in ('','.','..') for n in value.split('/')),'escaping path');return value
def digest(v):require(type(v) is str and re.fullmatch('[0-9a-f]{64}',v),'SHA256 required');return v
def integer(v,low=0,high=2**31-1):return type(v) is int and low<=v<=high
def finite(v):return type(v) in (int,float) and math.isfinite(v)
def position(v):return type(v) is list and len(v)==3 and all(finite(n) for n in v)
def canonical_token(v):return type(v) is str and re.fullmatch('[A-Za-z0-9_-]{21}[AQgw]',v) is not None
def redact(value,caps=()):
 if isinstance(value,str):
  for cap in caps:value=value.replace(cap,'[redacted]')
  value=re.sub(r'(?i)([?&](?:cap|token|capability)=)[^\s&"<>]+',r'\1[redacted]',value)
  value=re.sub(r'(?i)(bearer\s+)[A-Za-z0-9._~-]+',r'\1[redacted]',value)
  return value[:2048]
 if type(value) is list:return [redact(x,caps) for x in value]
 if type(value) is dict:return {k:('[redacted]' if re.search(r'(?i)^(capability|token|private_key|password)$',k) else redact(v,caps)) for k,v in value.items()}
 return value

REQUIRED_ROLES={'source','driver','sdk','node','tool','vendor','gateway','native','library','pack','bundle','metadata','notice','authority','schema'}
DEPENDENCIES={'T061','T065','T066','T070','T072','T077','T058','T057','T064','T062'}
NATIVE_HASH='49a1d28a6251213e27464afb36b6d974215c9886045a38d00a9cfe66befb096a'
PACK_HASH='c9ecfa62f7e4ca7111a9d3a23a9c97b906d11399d32f6f312463c6697a3359d7'
STATES=['BN_IDLE','BN_OPENING','BN_OPEN','BN_JOINING','BN_ACTIVE','BN_CLOSING','BN_FAILED']
COUNTER_ROLES={'local_attempts','join_timeouts','send_rejected','map_receipts','spawn_acknowledgments'}
def file_path(value,role):
 if not value.startswith('/'):return relative(value)
 require('..' not in value.split('/') and '\\' not in value,'escaping tool path')
 require((role in ('sdk','node') and value.startswith(('/private/tmp/outbreak-web-sdk/','/Library/Developer/CommandLineTools/'))) or
         (role=='tool' and (value in ('/usr/bin/unifdef','/usr/bin/codesign','/usr/sbin/lsof','/bin/ps') or value.startswith(('/Applications/Google Chrome.app/','/Users/jd1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/','/Users/jd1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core/')))),'absolute file outside approved tools')
 return value

def schema(value):
 exact(value,['schema_version','accepted_handoff','states','alive_state','running_phase','counter_keys','counter_roles','milestone_kind','opened_kind','opened_ordinal'],'missing accepted diagnostic contract')
 require(value['schema_version']==1 and type(value['accepted_handoff']) is str and value['accepted_handoff'].startswith('notes/handoffs/T061-'),'accepted T061 schema provenance')
 require(type(value['states']) is dict and set(value['states'])==set(STATES) and len(set(value['states'].values()))==7 and all(type(x) is str and x for x in value['states'].values()),'exact public state mapping')
 require(integer(value['alive_state']) and value['running_phase']=='running','public main/entity meanings required')
 keys=value['counter_keys'];require(type(keys) is list and keys and len(keys)==len(set(keys)) and all(type(k) is str and re.fullmatch('[a-z][a-z_0-9]*',k) for k in keys),'public counter key list')
 require(type(value['counter_roles']) is dict and set(value['counter_roles'])==COUNTER_ROLES and all(k in keys for k in value['counter_roles'].values()),'counter semantic mapping required')
 keys_expected='begin_calls repeated_begin frame_calls frame_advances ws_frames service_calls game_events receive_packets send_queued send_rejected owned_local_attempts milestones life_observations position_receipts remove_receipts map_receipts join_timeouts spawn_requests spawn_acknowledgments teardowns'.split()
 require(value['counter_keys']==keys_expected and value['states']=={s:s for s in STATES} and value['alive_state']==0 and value['milestone_kind']==1 and value['opened_kind']==0 and value['opened_ordinal']==2,'not accepted T061/D055 schema')
 require(value['counter_roles']==dict(local_attempts='owned_local_attempts',join_timeouts='join_timeouts',send_rejected='send_rejected',map_receipts='map_receipts',spawn_acknowledgments='spawn_acknowledgments'),'counter meanings changed')
 return value

IMPAIRMENT={'schema_version':1,'profile':'delay40_drop50_v1','delay_ms':40,'drop_every':50,'queue_datagrams':64,'queue_bytes':131072,'max_pending_ms':500}
def validate_pins(data,expected_sha,expected_attempt,view,case_kind='baseline'):
 """view is read-only IO; CLI always uses RealView, tests explicitly mock it."""
 require(sha(data)==digest(expected_sha),'pin digest mismatch');p=json.loads(data)
 require(case_kind in ('baseline','impaired40_drop50'),'unknown fixed case');impaired=case_kind=='impaired40_drop50'
 exact(p,['schema_version','ticket','status','authority','execution_release','attempt','scope','accepted_dependencies','files','trees','aliases','bundle','pack','native','diagnostic_contract','tools','outputs']+(['impairment'] if impaired else []),'incomplete pins')
 require(p['schema_version']==1 and p['ticket']==('T082' if impaired else 'T067') and p['status']=='RELEASED' and p['execution_release']==('EXPLICIT_IMPAIRED_TWO_CLIENT_NATIVE_GAME_EXECUTION' if impaired else 'EXPLICIT_TWO_CLIENT_NATIVE_GAME_EXECUTION'),'execution authority missing')
 if impaired:require(p['impairment']==IMPAIRMENT and all(type(p['impairment'][k]) is type(v) for k,v in IMPAIRMENT.items()),'fixed impairment preset required')
 exact(p['authority'],['owner','decision','path'],'authority shape')
 require(p['authority']['owner']=='MAIN' and re.fullmatch(r'D\d+',p['authority']['decision']) and relative(p['authority']['path']).startswith('notes/decisions/'),'MAIN authority required')
 require(p['attempt']==expected_attempt and re.fullmatch('[a-zA-Z0-9_-]{1,48}',expected_attempt),'attempt mismatch')
 require(p['scope']=={'profile':'network-client','role':'full-cpp-two-browser-native-game-impaired' if impaired else 'full-cpp-two-browser-native-game','clients':2,'capacity':2,'map_revision':2,'trusted_only':True,'baseline_only':not impaired},'wrong profile/role/scope')
 if impaired:require(type(p['schema_version']) is int and p['scope']['baseline_only'] is False and p['scope']['trusted_only'] is True and all(type(p['scope'][k]) is int for k in ('clients','capacity','map_revision')),'impaired scope types')
 require(type(p['accepted_dependencies']) is dict and set(p['accepted_dependencies'])==DEPENDENCIES|({'T079','T082'} if impaired else set()) and all(v=='ACCEPTED' for v in p['accepted_dependencies'].values()),'pending source/full build')
 require(type(p['files']) is dict and p['files'],'complete file pins required');roles=set()
 for name,row in p['files'].items():
  exact(row,['sha256','role'],'file row');digest(row['sha256']);require(row['role'] in REQUIRED_ROLES,'unknown role');file_path(name,row['role']);roles.add(row['role'])
  require(view.regular(name) and view.hash(name)==row['sha256'],'file changed/symlink: '+name)
 require(roles==REQUIRED_ROLES,'missing closure roles')
 require(p['authority']['path'] in p['files'] and p['files'][p['authority']['path']]['role']=='authority','authority not pinned')
 expected_trees={'source':'source/src','core':'source/enet','driver':'web/transport/tests/two-client/T067','sdk':'/private/tmp/outbreak-web-sdk','vendor':'web/transport/vendor/ws-8.21.0','bundle':'web/build/network-out','pack':'web/assets/network-profile/pack-root'}
 expected_trees.update(browser='/Applications/Google Chrome.app',playwright='/Users/jd1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright',playwright_core='/Users/jd1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core')
 if impaired:expected_trees['impairment_driver']='web/transport/tests/impaired/T082'
 require(type(p['trees']) is dict and set(p['trees'])==set(expected_trees),'complete membership trees required')
 for role,tree in p['trees'].items():
  exact(tree,['root','members'],'tree fields');require(tree['root']==expected_trees[role],'tree root/profile');require(type(tree['members']) is list and tree['members'] and len(tree['members'])==len(set(tree['members'])),'duplicate/empty membership')
  members={relative(x) for x in tree['members']};require(members==view.members(tree['root']),'tree membership changed: '+role)
  require(all(tree['root']+'/'+x in p['files'] for x in members),'unhashed tree member')
 if impaired:
  for name in ('run.py','shaper.cjs','preset.json'):require('web/transport/tests/impaired/T082/'+name in p['files'] and p['files']['web/transport/tests/impaired/T082/'+name]['role']=='driver','missing fixed impairment source/role')
  cfg=view.json('web/transport/tests/impaired/T082/preset.json');require(cfg==IMPAIRMENT and all(type(cfg[k]) is type(v) for k,v in IMPAIRMENT.items()),'changed impairment preset data')
 make='source/src/Makefile';require(make in p['files'],'native client inventory missing')
 block=re.search(r'CLIENT_OBJS=\s*\\\n(.*?)\n\nCLIENT_PCH=',view.text(make),re.S);require(block is not None,'genuine client inventory')
 cpp=re.findall(r'([A-Za-z0-9_/]+)\.o',block.group(1));require(len(cpp)==53 and len(set(cpp))==53,'53 genuine client units required')
 required={f'source/src/{n}.cpp' for n in cpp}|{f'source/enet/{n}.c' for n in ['callbacks','compress','host','list','packet','peer','protocol']}|{'web/transport/enet_websocket.c','web/transport/enet_websocket.js','web/transport/enet_ws_bridge.h','source/src/browsernet.h','source/src/browsernet_observer.h','web/transport/gateway.cjs','web/transport/gateway-limits.cjs'}
 require(required<=set(p['files']),'partial game/backend/gateway source closure')
 require(type(p['aliases']) is list,'explicit SDK aliases required')
 for a in p['aliases']:
  exact(a,['path','target','resolved','sha256'],'alias fields');role='sdk' if a['path'].startswith('/private/tmp/outbreak-web-sdk/') else 'tool';file_path(a['path'],role);file_path(a['resolved'],role)
  require(view.link(a['path'])==a['target'] and view.resolved(a['path'])==a['resolved'],'alias chain changed')
  if a['sha256'] is not None:digest(a['sha256']);require(view.hash(a['resolved'])==a['sha256'],'alias target hash')
  else:require(any(a['resolved']==t['root'] or a['resolved'].startswith(t['root']+'/') for t in p['trees'].values()),'directory alias outside complete inventory')
 require({a['path'] for a in p['aliases']}==set().union(*(view.aliases(p['trees'][r]['root']) for r in ('sdk','browser','playwright','playwright_core'))),'unrecorded tool/SDK alias membership')
 exact(p['bundle'],['root','runtime','notices','metadata','metadata_assertions'],'bundle fields')
 b=p['bundle'];require(b['root']=='web/build/network-out' and b['root']==p['trees']['bundle']['root'],'unpinned output root')
 require(type(b['runtime']) is dict and set(b['runtime'])=={'shell','js','wasm','data'},'four runtime roles')
 require(len(set(b['runtime'].values()))==4,'duplicate runtime member')
 for kind,suffix in [('shell','.html'),('js','.js'),('wasm','.wasm'),('data','.data')]:
  name=relative(b['runtime'][kind]);require(name.endswith(suffix) and b['root']+'/'+name in p['files'] and p['files'][b['root']+'/'+name]['role']=='bundle','wrong runtime role')
 require(type(b['notices']) is list and b['notices'],'notice membership required')
 for n in b['notices']:
  relative(n);require(n.startswith('notices/') and b['root']+'/'+n in p['files'] and p['files'][b['root']+'/'+n]['role']=='notice' and not n.endswith(('.js','.wasm','.data','.html')),'notice route role')
 for name in p['trees']['bundle']['members']:
  row=p['files'][b['root']+'/'+name]
  require(name in set(b['runtime'].values())|set(b['notices']) or (row['role']=='metadata' and name.endswith('.json')),'unexpected published artifact member')
 meta=b['root']+'/'+relative(b['metadata']);require(meta in p['files'] and p['files'][meta]['role']=='metadata','metadata missing')
 require(type(b['metadata_assertions']) is dict and set(b['metadata_assertions'])=={'profile','status','artifact_id'},'accepted metadata meanings missing')
 rawmeta=view.json(meta)
 for meaning,check in b['metadata_assertions'].items():
  exact(check,['path','value'],'metadata assertion');require(type(check['path']) is list and check['path'] and all(type(k) is str and k not in ('__proto__','prototype','constructor') for k in check['path']),'metadata data path')
  value=rawmeta
  for key in check['path']:require(type(value) is dict and key in value,'missing metadata path');value=value[key]
  require(value==check['value'],'metadata mismatch')
 require(b['metadata_assertions']['profile']=={'path':['profile'],'value':'NETWORK_CLIENT original-network-media'} and b['metadata_assertions']['status']=={'path':['status'],'value':'LINKED_NOT_BROWSER_VERIFIED'} and b['metadata_assertions']['artifact_id']['path']==['bundle_id'],'accepted T066 metadata meanings')
 digest(b['metadata_assertions']['artifact_id']['value'])
 require(rawmeta.get('ticket')=='T066 revision4.0' and len(rawmeta.get('units',[]))==61 and len(rawmeta.get('compiles',[]))==61 and rawmeta.get('object_reuse') is False and rawmeta.get('stable_inventory') is True and not any(rawmeta.get('claims',{'missing':True}).values()),'not actual full61-unit build; no runtime acceptance inferred')
 acceptance='notes/decisions/D064-accepted-network-artifact.json'
 require(acceptance in p['files'] and view.hash(acceptance)=='3ec3fb4368d22a5abb6d1885e40d3baf9e0ba2a218a99f935effee7f6970c97d','D064 actual artifact acceptance missing/changed')
 a=view.json(acceptance);require(a['authority']=='MAIN' and a['status']=='ACCEPTED' and a['scope']=='FULL_NETWORK_BUILD_AND_PUBLISHED_VERIFICATION_ONLY' and a['bundle_id']==rawmeta['bundle_id'],'actual accepted artifact identity')
 require(set(a['published_files'])=={b['root']+'/'+x for x in p['trees']['bundle']['members']},'D064 artifact membership')
 for f,h in a['published_files'].items():require(p['files'][f]['sha256']==h,'D064 published bytes changed')
 for pathkey,hashkey in [('build_pins','build_pins_sha256'),('verifier','verifier_sha256'),('verification_receipt','verification_receipt_sha256')]:
  f=a[pathkey];require(f in p['files'] and view.hash(f)==a[hashkey],'separate accepted build/verifier/receipt not pinned')
 require(p['pack']=={'root':'web/assets/network-profile/pack-root','manifest':'web/assets/network-profile/manifest.json','manifest_sha256':PACK_HASH,'files':79,'bytes':388791,'map_revision':2},'wrong network pack')
 pack=p['pack'];require(pack['root']==p['trees']['pack']['root'] and view.hash(pack['manifest'])==PACK_HASH,'pack manifest changed')
 entries=view.json(pack['manifest'])['entries'];require(len(entries)==79 and len(p['trees']['pack']['members'])==79,'pack membership')
 require(sum(e['bytes'] for e in entries)==388791,'pack byte total')
 for e in entries:
  name=pack['root']+'/'+relative(e['path']);require(view.hash(name)==e['sha256'] and view.size(name)==e['bytes'],'pack entry changed')
 exact(p['native'],['binary','sha256','dependency_ledger','sound_identity','argv_tail','parameters','rotation'],'native fields')
 n=p['native'];require(n['binary']=='web/server/out-lifecycle/release/ac_server' and n['sha256']==NATIVE_HASH and view.hash(n['binary'])==NATIVE_HASH,'native changed')
 require(n['argv_tail']==native_arguments() and n['parameters']==parameters() and n['rotation']==rotation(),'native c2 sandbox parameters changed')
 require(n['dependency_ledger']=='web/server/lifecycle/build-report.json' and n['sound_identity']=='notes/decisions/D052-native-header-identity.json','native ledger authority')
 for f in [n['dependency_ledger'],n['sound_identity']]:require(f in p['files'],'native ledger not pinned')
 for tool in ['/usr/bin/unifdef','/usr/bin/codesign','/usr/sbin/lsof','/bin/ps']:require(tool in p['files'] and p['files'][tool]['role']=='tool','missing owned lifecycle tool pin')
 require(view.hash(n['sound_identity'])=='5441fbb6ed7c9a5e5eae2fff6b89d19ceaa8e3f11d0e557357791a01eed471ec','D052 manifest changed')
 identity=view.json(n['sound_identity'])
 for f,h in [(identity['preserved_original'],identity['original_compile_sha256']),(identity['path'],identity['current_sha256']),(identity['unifdef'],identity['unifdef_sha256'])]:require(f in p['files'] and view.hash(f)==h,'D052 raw/tool identity not pinned')
 libs={'web/server/deps-signed/SDL2.framework/Versions/A/SDL2':'5faae862816a57f36e11164dfbf5500021a2fbe65a0b23297c9697738c1c9767','web/server/deps-signed/SDL2.framework/Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi':'62e00aa847d78ed4d1f6188ade82c0b271b73c2278c6bac9b08056eb036e8de0'}
 for f,h in libs.items():require(f in p['files'] and p['files'][f]=={'role':'library','sha256':h},'native signed libraries changed/missing')
 for unit in view.json(n['dependency_ledger'])['modes']['release']['compile']:
  for f,old in unit['dependencies'].items():
   key=view.key(f);require(key in p['files'],'native dependency absent: '+key);now=view.hash(key)
   require(now==old or (key==identity['path'] and old==identity['original_compile_sha256'] and now==identity['current_sha256']),'native dependency changed: '+key)
 contract=schema(p['diagnostic_contract']);require(contract['accepted_handoff'] in p['files'] and p['files'][contract['accepted_handoff']]['role']=='schema','unaccepted diagnostic schema')
 exact(p['tools'],['node','browser','playwright'],'tool roles')
 for name in p['tools'].values():require(name in p['files'],'unpinned tool')
 require(p['tools']['node']=='/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node','Node path') # absolute tools handled by explicit view allowlist
 require(p['files'][p['tools']['node']]['sha256']=='27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1','Node binary pin')
 require(p['tools']['browser']=='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' and p['tools']['playwright']=='/Users/jd1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.js','approved browser tools')
 require(p['outputs']=={'result':('web/transport/results/impaired-T082/runtime-' if impaired else 'web/transport/results/two-client-T067/runtime-')+expected_attempt,'native':('web/server/run/T082-' if impaired else 'web/server/run/T067-')+expected_attempt},'output ownership')
 return p

def parameters():return 'demo_save:0\nmandatory_auth:0\nlogthreshold_syslog:5\nlogthreshold_file:5\n'
def rotation():return 'dev_outbreak_browser dm weight:100 repeat:100 time:2 mintime:2 maxtime:2 minplayers:0 maxplayers:8 maxteamsize:8 manual:0\n'
def native_arguments():return ['-i127.0.0.1','-f29863','-c2','-LS5','-LF5','-Hlogs/','-Aconfig/serverparameters.cfg','-Uconfig/servervita','-Wdemo/','-rconfig/maprot.cfg','-Xconfig/serverpwd.cfg','-Bconfig/serverblacklist.cfg','-Gconfig/geoip.cfg','-Kconfig/nicknameblacklist.cfg','-Iconfig/serverinfo','-Oconfig/motd','-gconfig/forbidden.cfg','-Z0']

def route(raw,pins):
 require(type(raw) is str and raw.startswith('/') and '?' not in raw and '#' not in raw and '%' not in raw and '\\' not in raw,'route rejected')
 b=pins['bundle'];mapping={'/':b['runtime']['shell'],**{'/'+n:n for n in list(b['runtime'].values())+b['notices']}}
 require(raw in mapping,'not a pinned runtime/notice route');return b['root']+'/'+mapping[raw]

def request_route(method,raw,pins):
 require(method=='GET','method rejected')
 if raw=='/favicon.ico':return (204,None)
 return (200,route(raw,pins))

# Source-derived positive identity, not permission to infer missing fields.
# Mirrored as JSON in observe.cjs; SOURCE fixtures verify exact agreement.
FIRST_FRAME_IDENTITY={
 'timing':{'frame_id':0,'prediction_elapsed_ms':0,'embedded_server_path_compiled':False},
 'diagnostics':{'frame_count':1,'rendered_frame_count':0,'phase':'loading','map_name':'dev_outbreak_browser'},
 'counters':{'begin_calls':1,'repeated_begin':0,'frame_calls':1,'frame_advances':1,'ws_frames':1,'milestones':0,'map_receipts':0,'spawn_acknowledgments':0,'teardowns':0},
}

def timing_classification(s):
 """Pure reference for the JS source classifier; no first-frame success gate."""
 n=s.get('network');d=s.get('diagnostics');t=s.get('timing');b=s.get('browser',{})
 if n is not None:require(type(n) is dict and n.get('error')==0 and n.get('state') not in ('BN_FAILED','BN_CLOSING'),'published lifecycle/global error')
 if d is not None:require(type(d) is dict and d.get('runtime_errors')==[] and d.get('phase') not in ('error','stopped'),'published lifecycle/global error')
 require(b.get('visibility')=='visible','actual visibility failure')
 if t is None:return 'WAITING'
 require(type(t) is dict and t.get('schema_version')==1 and integer(t.get('frame_id')) and finite(t.get('raw_elapsed_ms')) and t['raw_elapsed_ms']>=0 and finite(t.get('prediction_elapsed_ms')) and 0<=t['prediction_elapsed_ms']<=50 and t.get('embedded_server_path_compiled') is False and b.get('timing_frozen') is True,'invalid published timing')
 if t['frame_id']>0:
  require(t['raw_elapsed_ms']<=1000,'later main-frame interval exceeds1000ms; backend cause unproven')
  return 'LATER_FRAME'
 require(type(n) is dict and type(d) is dict and n.get('schema_version')==1 and n.get('profile')=='network-client' and d.get('schema_version')==1 and d.get('profile')=='network-client' and b.get('network_frozen') is True,'ambiguous frame0 identity')
 counters=n.get('counters');require(type(counters) is dict and set(counters)==set(schema_counter_keys()) and all(integer(v) for v in counters.values()),'ambiguous frame0 counters')
 for section,actual in [('timing',t),('diagnostics',d),('counters',counters)]:
  require(all(type(actual.get(k)) is type(v) and actual[k]==v for k,v in FIRST_FRAME_IDENTITY[section].items()),'ambiguous frame0 identity')
 require(n.get('state') in ('BN_OPENING','BN_JOINING') and t.get('lifecycle_state')==STATES.index(n['state']) and n.get('map_name')=='' and type(n.get('map_revision')) is int and n['map_revision']==0 and type(n.get('own',{}).get('cn')) is int and n['own']['cn']==-1 and type(n['own'].get('life')) is int and n['own']['life']==-1,'ambiguous frame0 lifecycle')
 require(all(counters[k]==0 for k in ('owned_local_attempts','join_timeouts','send_rejected')),'owned client error/local attempt')
 events=n.get('events');require(type(events) is list and len(events)==(1 if n['state']=='BN_OPENING' else 2) and all(type(e) is dict and e.get('kind')==0 and e.get('milestone')==0 and e.get('cn')==-1 and e.get('life')==-1 and e.get('error')==0 and finite(e.get('at_ms')) and e['at_ms']>=0 for e in events) and all(events[i]['at_ms']<=events[i+1]['at_ms'] for i in range(len(events)-1)),'ambiguous frame0 events')
 return 'STARTUP_FRAME0'

def schema_counter_keys():
 return 'begin_calls repeated_begin frame_calls frame_advances ws_frames service_calls game_events receive_packets send_queued send_rejected owned_local_attempts milestones life_observations position_receipts remove_receipts map_receipts join_timeouts spawn_requests spawn_acknowledgments teardowns'.split()

def bounded_failure_samples(value,required_clients=()):
 """Validate retained observations structurally, without accepting game success.
 Null means not observed. Real error/partial-join fields must remain intact.
 """
 require(type(value) is dict and set(value)<=set(('A','B')) and set(required_clients)<=set(value),'missing/unbounded client evidence')
 for name,row in value.items():
  exact(row,['last','first_active','startup'],'client evidence slots')
  require(row['last'] is not None,'missing last published sample')
  for slot,s in row.items():
   if s is None:continue
   exact(s,['network','diagnostics','timing','browser','model','audio'],'full published sample required')
   if slot=='first_active':require(type(s['network']) is dict and s['network'].get('state')=='BN_ACTIVE' and s['network'].get('error')==0,'first ACTIVE observation missing')
   if slot=='startup':require(timing_classification(s)=='STARTUP_FRAME0','invalid retained startup identity')
   for component in ('network','diagnostics','model','audio'):
    data=s[component]
    if data is None:continue
    require(type(data) is dict,'published component shape')
    if component=='network':require(type(data.get('events')) is list and len(data['events'])<=512 and type(data.get('remotes')) is list and len(data['remotes'])<=256,'unbounded network sample')
    if component=='diagnostics':require(type(data.get('runtime_errors')) is list and len(data['runtime_errors'])<=512,'unbounded runtime errors')
    if component=='model':require(type(data.get('preloads')) is list and len(data['preloads'])<=3,'unbounded model sample')
   require(type(s['browser']) is dict and (s['timing'] is None or type(s['timing']) is dict),'published sample metadata')
 require(len(json.dumps(value).encode())<=1024*1024,'failure evidence byte bound')
 return value

def gateway_cleanup_ports(proof):
 """All valid observed owned tuples, even partial-join failure. Missing facts fail.
 Protocol is UDP by the accepted gateway's udp_tuple schema, family IPv4.
 """
 ports=set();errors=[]
 if type(proof) is not dict:return [],['missing final gateway observation']
 if type(proof.get('gateway_final')) is not dict:errors.append('missing final gateway observation')
 for key in ('gateway_receipt','gateway_final'):
  if key not in proof:continue
  g=proof[key]
  if type(g) is not dict or type(g.get('schema_version')) is not int or g['schema_version']!=1 or g.get('address')!={'address':'127.0.0.1','port':29865,'family':'IPv4'}:
   errors.append('invalid '+key+' gateway identity');continue
  sessions=g.get('sessions')
  if type(sessions) is not list or len(sessions)>2:errors.append('invalid '+key+' session bound');continue
  seen=set()
  for s in sessions:
   if type(s) is not dict or s.get('session_id') not in ('s1','s2') or s['session_id'] in seen or 'udp_tuple' not in s or type(s.get('upstream_connected')) is not bool:errors.append('invalid/missing owned session facts');continue
   seen.add(s['session_id'])
   t=s.get('udp_tuple')
   if t is None:
    if s.get('upstream_connected') is True:errors.append('missing connected owned UDP tuple')
    continue
   if type(t) is dict and set(t)=={'address','port','family'} and t['address']=='127.0.0.1' and t['family']=='IPv4' and integer(t['port'],1,65535):ports.add(t['port'])
   else:errors.append('invalid owned UDP tuple')
 return sorted(ports),errors

def observation(sample,contract,active=False):
 """Only published state; structure comes from approved APIs, counters from future accepted mapping."""
 exact(sample,['network','diagnostics','timing','browser','model','audio'],'observation fields')
 n=sample['network'];require(type(n) is dict and n.get('schema_version')==1 and n.get('profile')=='network-client' and not n.get('synthetic',False),'non-game snapshot')
 require(n.get('state') in contract['states'].values() and n.get('error')==0,'lifecycle error')
 require(n.get('map_name')=='dev_outbreak_browser' and n.get('map_revision')==2,'wrong actual map')
 require(n.get('coverage')=='owned client send/local receive paths only; main/local server unobserved','coverage qualification missing')
 own=n.get('own');require(type(own) is dict and integer(own.get('cn'),0,255) and integer(own.get('life'),-1) and integer(own.get('state')) and position(own.get('position')),'own state missing')
 require(type(n.get('counters')) is dict and set(n['counters'])==set(contract['counter_keys']) and all(integer(x) for x in n['counters'].values()),'unknown counter schema')
 for semantic in ['local_attempts','join_timeouts','send_rejected']:require(n['counters'][contract['counter_roles'][semantic]]==0,'client error/local attempt')
 require(n['counters'][contract['counter_roles']['map_receipts']]>0,'no genuine map receipt')
 events=n.get('events');require(type(events) is list and len(events)<=512,'event overflow')
 milestones=[];opened=[]
 for e in events:
  require(type(e) is dict and all(k in e for k in ['kind','milestone','cn','life','error','at_ms']) and integer(e['kind']) and integer(e['milestone']) and integer(e['cn'],-1,255) and integer(e['life'],-1) and e['error']==0 and finite(e['at_ms']) and e['at_ms']>=0,'bad published event')
  if e['kind']==contract['opened_kind']:opened.append(e['at_ms'])
  if e['kind']==contract['milestone_kind']:
   require(e['cn']==own['cn'],'milestone identity');milestones.append(e['milestone'])
 require(len(opened)==2 and opened[0]<=opened[1] and milestones[:3]==[1,2,3],'no genuine initial handshake milestones')
 require(all(events[i]['at_ms']<=events[i+1]['at_ms'] for i in range(len(events)-1)),'event chronology')
 first=[e for e in events if e['kind']==1][:4]
 require(all(e['life']==-1 for e in first[:3]),'initial handshake life')
 if active:
  require(n['state']==contract['states']['BN_ACTIVE'] and own['state']==contract['alive_state'] and own['life']>=0 and milestones[:4]==[1,2,3,4] and first[3]['life']>=0 and n['counters'][contract['counter_roles']['spawn_acknowledgments']]>0,'not genuinely active/spawned')
 remotes=n.get('remotes');require(type(remotes) is list and len(remotes)<=256,'remote bound');seen=set()
 for r in remotes:
  require(type(r) is dict and integer(r.get('cn'),0,255) and r['cn']!=own['cn'] and r['cn'] not in seen and integer(r.get('life')) and position(r.get('position')) and integer(r.get('parse_count'),1) and finite(r.get('last_parse_ms')) and r['last_parse_ms']>=0,'bad parsed remote receipt');seen.add(r['cn'])
 d=sample['diagnostics'];t=sample['timing'];b=sample['browser']
 require(type(d) is dict and d.get('schema_version')==1 and d.get('profile')=='network-client' and d.get('phase')==contract['running_phase'] and d.get('map_name')=='dev_outbreak_browser' and integer(d.get('frame_count'),1) and integer(d.get('rendered_frame_count'),1) and d.get('runtime_errors')==[],'runtime/render error')
 require(type(t) is dict and t.get('schema_version')==1 and integer(t.get('frame_id'),1) and finite(t.get('raw_elapsed_ms')) and 0<=t['raw_elapsed_ms']<=1000 and finite(t.get('prediction_elapsed_ms')) and 0<=t['prediction_elapsed_ms']<=50 and t.get('embedded_server_path_compiled') is False,'timing/profile mismatch; startup cannot establish readiness')
 expected_index=STATES.index(next(k for k,v in contract['states'].items() if v==n['state']));require(t.get('lifecycle_state')==expected_index,'inconsistent lifecycle timing')
 require(type(b) is dict and b.get('visibility')=='visible' and type(b.get('focused')) is bool and b.get('network_frozen') is True and b.get('timing_frozen') is True and finite(b.get('now_ms')) and b['now_ms']>=0 and b.get('canvas_width',0)>0 and b.get('canvas_height',0)>0,'not naturally visible/read-only canvas')
 if active:
  spawn=next(e for e in events if e['kind']==1 and e['milestone']==4);require(0<=spawn['at_ms']-opened[1]<15000,'initial join exceeded15s')
 else:require(0<=b['now_ms']-opened[1]<15000,'join deadline expired')
 model=sample['model']
 if model is not None:
  require(type(model) is dict and model.get('schema_version')==1 and model.get('profile')=='network-client' and type(model.get('preloads')) is list and [(r.get('name'),r.get('loaded')) for r in model['preloads']]==[(n,True) for n in ['outbreak/survivor','outbreak/pistol','outbreak/rifle']],'model preload inconsistency; no pixel claim')
 audio=sample['audio']
 if audio is not None:require(type(audio) is dict and audio.get('schema_version')==1 and audio.get('error') is None and all(integer(audio.get(k)) for k in ('gesture_count','play_count')),'audio diagnostic error')
 return sample

def progress(before,after):
 require(after['diagnostics']['rendered_frame_count']>before['diagnostics']['rendered_frame_count'] and after['timing']['frame_id']>before['timing']['frame_id'],'frozen rendered frames')
def cross_receipt(a_before,a_settled,b_before,b_after,elapsed_ms):
 require(a_before['browser']['focused'] and a_settled['browser']['focused'] and a_before['diagnostics'].get('input_locked') is True,'moving page lacks actual focus/capture')
 a=a_settled['network']['own'];require(0<=elapsed_ms<=2000,'cross deadline')
 require(b_before['network']['own']['cn']==b_after['network']['own']['cn'] and b_before['network']['own']['life']==b_after['network']['own']['life'],'receiver identity changed')
 require(a['cn']!=b_after['network']['own']['cn'] and a['cn']==a_before['network']['own']['cn'] and a['life']==a_before['network']['own']['life'],'duplicate/reused own identity')
 require(math.dist(a_before['network']['own']['position'][:2],a['position'][:2])>=2,'no own horizontal movement')
 def find(s):return next((r for r in s['network']['remotes'] if r['cn']==a['cn'] and r['life']==a['life']),None)
 old,new=find(b_before),find(b_after);require(old is not None and new is not None,'own-only evidence')
 require(new['parse_count']>old['parse_count'] and new['last_parse_ms']>old['last_parse_ms'],'no new parsed remote update')
 require(0<=b_after['browser']['now_ms']-new['last_parse_ms']<=2000,'stale/future receiver clock receipt')
 require(math.dist(a['position'][:2],new['position'][:2])<=1,'cross-client position mismatch');progress(a_before,a_settled);progress(b_before,b_after)

def cleanup_ok(r):
 required=['keys_released','contexts_closed','browsers_stopped','profiles_removed','gateway_closed','static_closed','groups_reaped','handles_empty','ports_released']
 require(type(r) is dict and all(r.get(k) is True for k in required),'owned cleanup incomplete')
 require(r.get('native_exit')==0 and r.get('kill_fallback') is False and finite(r.get('native_shutdown_ms')) and 0<=r['native_shutdown_ms']<=3000 and finite(r.get('gateway_close_ms')) and 0<=r['gateway_close_ms']<=2000,'shutdown failure')

def shaper_receipt(r):
 """Independent metadata accounting; only actual runtime + genuine game proof can PASS."""
 exact(r,['schema_version','profile','preset','status','directions','sockets','events','faults','cleanup'],'missing shaper receipt')
 require(type(r['schema_version']) is int and r['schema_version']==1 and r['profile']=='delay40_drop50_v1' and r['status']=='CLOSED' and r['preset']==IMPAIRMENT and all(type(r['preset'][k]) is type(v) for k,v in IMPAIRMENT.items()) and r['faults']==[],'shaper failure/profile')
 require(r['cleanup']=={'closed':True,'restored':True,'open_sockets':0,'timers':0,'buffers':0,'pending_bytes':0} and type(r['cleanup']['closed']) is bool and type(r['cleanup']['restored']) is bool and all(type(r['cleanup'][k]) is int for k in ('open_sockets','timers','buffers','pending_bytes')),'shaper cleanup incomplete')
 exact(r['directions'],['up','down'],'direction schema');require(type(r['sockets']) is list and len(r['sockets'])==2 and [s.get('id') for s in r['sockets']]==[1,2] and all(type(s.get('id')) is int and s.get('closed') is True for s in r['sockets']),'two owned sockets must close')
 for s in r['sockets']:exact(s,['id','closed','up','down'],'socket receipt schema')
 keys='observed bytes dropped scheduled delivered canceled errors pending pending_bytes peak_datagrams peak_bytes callback_calls callback_errors late_callbacks delay_count delay_min_ms delay_max_ms histogram'.split()
 histkeys=['40_49','50_99','100_499'];additive=[k for k in keys if k not in ['peak_datagrams','peak_bytes','delay_min_ms','delay_max_ms','histogram']]
 def stats(c,direction,global_counts=False):
  exact(c,keys,'shaper counter schema');require(all(integer(c[k]) for k in keys if k not in ('delay_min_ms','delay_max_ms','histogram')),'invalid shaper counts')
  exact(c['histogram'],histkeys,'histogram schema');require(all(integer(v) for v in c['histogram'].values()),'histogram counts')
  require(c['observed']==c['dropped']+c['scheduled'] and c['scheduled']==c['delivered']+c['canceled']+c['errors']+c['pending'] and c['errors']==0 and c['pending']==0 and c['pending_bytes']==0,'unaccounted/lost/pending datagrams')
  require(2*c['observed']<=c['bytes']<=4096*c['observed'] and c['peak_datagrams']<=64 and c['peak_bytes']<=131072,'raw byte/queue bounds')
  require(c['delay_count']==c['delivered']==sum(c['histogram'].values()),'delivery delay accounting')
  if c['delivered']:
   require(finite(c['delay_min_ms']) and finite(c['delay_max_ms']) and 40<=c['delay_min_ms']<=c['delay_max_ms']<500,'early/late delivery')
   bounds=[(40,50),(50,100),(100,500)];occupied=[i for i,k in enumerate(histkeys) if c['histogram'][k]];lo,hi=bounds[min(occupied)],bounds[max(occupied)]
   require(lo[0]<=c['delay_min_ms']<lo[1] and hi[0]<=c['delay_max_ms']<hi[1],'histogram delay limits')
  else:require(c['delay_min_ms'] is None and c['delay_max_ms'] is None,'empty latency must be unobserved')
  require(c['callback_calls']==(c['observed'] if direction=='up' else 0) and c['callback_errors']==(c['canceled'] if direction=='up' else 0) and c['late_callbacks']<=(c['canceled'] if direction=='up' else 0),'callback ownership')
  if global_counts:require(c['dropped']==c['observed']//50 and 1<=c['dropped']<=512 and c['delivered']>=1,'no actual fixed-profile loss/delivery or event overflow')
 for direction,c in r['directions'].items():
  stats(c,direction,True)
  per=[s[direction] for s in r['sockets']]
  for row in per:stats(row,direction)
  require(all(c[k]==sum(row[k] for row in per) for k in additive),'socket/global counter mismatch')
  require(all(c['histogram'][k]==sum(row['histogram'][k] for row in per) for k in histkeys),'socket/global histogram mismatch')
  for k in ('peak_datagrams','peak_bytes'):require(max(row[k] for row in per)<=c[k]<=sum(row[k] for row in per),'socket/global queue peak mismatch')
  valid=[row for row in per if row['delivered']];require(c['delay_min_ms']==min(row['delay_min_ms'] for row in valid) and c['delay_max_ms']==max(row['delay_max_ms'] for row in valid),'socket/global latency mismatch')
 events=r['events'];require(type(events) is list and len(events)<=512,'shaper event bound')
 for e in events:
  exact(e,['kind','direction','ordinal','socket'],'drop event schema');require(e['kind']=='profile_drop' and e['direction'] in ('up','down') and integer(e['ordinal'],1) and type(e['socket']) is int and e['socket'] in (1,2),'drop event invalid')
 for direction,c in r['directions'].items():
  drops=[e for e in events if e['direction']==direction];require([e['ordinal'] for e in drops]==list(range(50,c['observed']+1,50)),'wrong exact loss ordinals')
  for s in r['sockets']:require(s[direction]['dropped']==sum(e['socket']==s['id'] for e in drops),'socket loss identity mismatch')
 return r
