"""PREPARED ONLY. --prepare-plan is pure; execution needs future MAIN pins/release.
No command in this module is invoked by preparation/helper tests.
"""
import argparse,json,os,re,time
from pathlib import Path
import policy,ownership
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
EXECUTION_STARTED=False

class RealView:
 def __init__(self,root):self.root=Path(root)
 def path(self,name):return Path(name) if name.startswith('/') else self.root/name
 def key(self,name):return str(Path(name).relative_to(self.root)) if Path(name).is_absolute() and Path(name).is_relative_to(self.root) else name
 def hash(self,name):return policy.sha(self.path(name).read_bytes())
 def size(self,name):return self.path(name).stat().st_size
 def regular(self,name):
  p=self.path(name)
  return p.is_file() and not p.is_symlink() and not any(q.is_symlink() for q in p.parents)
 def json(self,name):return json.loads(self.path(name).read_text())
 def text(self,name):return self.path(name).read_text()
 def members(self,root):return {str(p.relative_to(self.path(root))) for p in self.path(root).rglob('*') if p.is_file() and not p.is_symlink()}
 def aliases(self,root):return {str(p) for p in self.path(root).rglob('*') if p.is_symlink()}
 def link(self,name):return os.readlink(self.path(name))
 def resolved(self,name):return str(self.path(name).resolve(strict=True))

def authorize(root,pin_path,expected_sha,attempt,view=None,case_kind='baseline'):
 root=Path(root);p=Path(pin_path)
 policy.require(p.is_absolute() and p.parent==root/'notes/decisions' and p.suffix=='.json' and not p.is_symlink(),'MAIN decision pin path required')
 policy.require(p.is_file(),'missing pins; no runtime')
 data=p.read_bytes();pins=policy.validate_pins(data,expected_sha,attempt,view or RealView(root),case_kind)
 policy.require(pins['diagnostic_contract']==json.loads((HERE/'diagnostic-schema.json').read_text()),'accepted schema must match frozen observer')
 return pins

def gated_execute(root,pin_path,expected_sha,attempt,effects,view=None,case_kind='baseline'):
 """No effect methods before the complete read-only authorization succeeds."""
 pins=authorize(root,pin_path,expected_sha,attempt,view,case_kind)
 return effects.run(pins,{'pins_path':str(pin_path),'pins_sha':expected_sha})

def plan():
 return {'status':'NOT_RUN','phase':'PREPARATION_ONLY','accepted_build_evidence':'D064 T070 full61-unit artifact + separate T072 verifier/receipt; runtime NOT RUN','pending':['MAIN runtime pins binding exact D064 acceptance/artifact/verifier/receipt','MAIN complete pins + out-of-band expected SHA','explicit execution release + runtime output allowlist'],
 'accepted_schema':'T0613.7/D055 published state; main0.1/T065 model outcomes','topology':'2 isolated Chrome/context/Module profiles -> gateway29865 -> native UDP29863/c2; static29866',
 'limits':{'baseline_seconds':180,'join_after_open_ms':15000,'movement_deadline_ms':2000,'native_shutdown_ms':3000,'gateway_close_ms':2000,'events':512,'bytes_per_child':8388608},
 'native_arguments':policy.native_arguments(),'staging':'RESERVED / NOT CREATED before complete future gate','state_actions':'ordinary canvas click, W250ms/key-up/Escape only; no Module/function/packet/state writes'}

class Runtime:
 """Future entrypoint. Imports with side effects/process/network only AFTER pins gate.
 This path is intentionally not called under preparation; tests pass fake effects.
 """
 def __init__(self,root,case_kind='baseline'):self.root=Path(root);self.case_kind=case_kind
 def run(self,pins,receipt):
  policy.require(self.case_kind in ('baseline','impaired40_drop50') and pins['ticket']==('T082' if self.case_kind=='impaired40_drop50' else 'T067'),'runtime fixed case mismatch')
  import base64,errno,pty,selectors,signal,socket,subprocess,threading
  root=self.root;view=RealView(root);start=time.monotonic();wall=time.time();report={'status':'FAIL','kind':'ACTUAL full two-game-client baseline','errors':[],'cleanup':{},'pins_scope':pins['scope']}
  if self.case_kind=='impaired40_drop50':report['kind']='ACTUAL_IMPAIRED_TWO_GAME_CLIENT'
  n=None;child=None;watch=None;fd=None;slave=None;selector=selectors.DefaultSelector();buffers={k:bytearray() for k in ['native','stdout','stderr']};cap=8*1024*1024;owned={}
  def command(args,timeout=2):
   global EXECUTION_STARTED
   EXECUTION_STARTED=True
   r=subprocess.run(args,cwd=root,capture_output=True,text=True,timeout=timeout);return {'argv':args,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
  def drain(timeout=.05):
   for key,_ in selector.select(timeout):
    try:b=os.read(key.fd,16384)
    except OSError as e:
     if e.errno==errno.EIO:b=b''
     else:raise
    if not b:selector.unregister(key.fileobj);continue
    buffers[key.data].extend(b);policy.require(len(buffers[key.data])<=cap,'8MiB child output overflow')
  def free_ports(ports):
   rows=[]
   for protocol,port in ports:
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM if protocol=='UDP' else socket.SOCK_STREAM) as s:
     if protocol=='TCP':s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
     try:s.bind(('127.0.0.1',port));row={'protocol':protocol,'port':port,'bind':True,'errno':None}
     except OSError as e:row={'protocol':protocol,'port':port,'bind':False,'errno':e.errno}
     rows.append(row)
   return rows
  ports=[('UDP',x) for x in [29863,29864,28762]]+[('TCP',x) for x in [29865,29866]]
  # These preflight actions are unreachable until exact future execution pins.
  policy.require(view.hash(pins['native']['sound_identity'])=='5441fbb6ed7c9a5e5eae2fff6b89d19ceaa8e3f11d0e557357791a01eed471ec','D052 manifest identity')
  identity=view.json(pins['native']['sound_identity']);ledger=view.json(pins['native']['dependency_ledger']);recorded={}
  policy.require(view.hash(identity['preserved_original'])==identity['original_compile_sha256'] and view.hash(identity['path'])==identity['current_sha256'],'D052 exact raw inputs')
  for c in ledger['modes']['release']['compile']:recorded.update(c['dependencies'])
  for name,h in recorded.items():
   key=str(Path(name).relative_to(root)) if Path(name).is_absolute() and Path(name).is_relative_to(root) else name
   policy.require(key in pins['files'],'native dependency missing from pins: '+key)
   current=view.hash(name)
   if current!=h:policy.require(Path(name)==root/identity['path'] and h==identity['original_compile_sha256'] and current==identity['current_sha256'],'native dependency changed')
  policy.require(view.hash(identity['unifdef'])==identity['unifdef_sha256'],'unifdef pin')
  for name in [identity['preserved_original'],identity['path']]:
   row=command([identity['unifdef'],*identity['unifdef_args'],str(view.path(name))]);tokens=re.findall(r'\w+|[^\s]',re.sub(r'//[^\n]*|/\*.*?\*/','',row['stdout'],flags=re.S))
   policy.require(row['exit'] in (0,1) and len(tokens)==410 and policy.sha(' '.join(tokens).encode())==identity['normalized_native_token_sha256'],'D052 native view')
  for name,row in pins['files'].items():
   if row['role'] in ('native','library'):policy.require(command(['/usr/bin/codesign','--verify','--verbose=4',str(view.path(name))])['exit']==0,'code signature')
  precheck=free_ports(ports);policy.require(all(r['bind'] for r in precheck),'occupied/refused fixed port')
  for args in [['/usr/sbin/lsof','-nP','-iUDP:29863','-iUDP:29864','-iUDP:28762'],['/usr/sbin/lsof','-nP','-a','-iTCP:29865','-iTCP:29866','-sTCP:LISTEN']]:
   r=command(args);policy.require(r['exit']==1 and not r['stdout'] and not r['stderr'],'fixed owner/listener check')
  result=root/pins['outputs']['result'];native=root/pins['outputs']['native'];policy.require(not result.exists() and not native.exists(),'attempt already exists')
  result.mkdir(parents=True);native.mkdir(parents=True)
  def scan_owned():
   rows=ownership.parse(command(['/bin/ps','-axo','pid=,ppid=,pgid=,lstart=,command='])['stdout'])
   for row in ownership.select(rows,str(result),pins['tools']['browser']):
    if row['pid'] not in owned:owned[row['pid']]=row
   return {r['pid']:r for r in rows}
  report['precheck']=precheck
  try:
   for name in ['config/serverinfo','config/motd','logs/misc','logs/docs','demo','private','packages/maps/official','packages/maps/servermaps/incoming']:(native/name).mkdir(parents=True)
   (native/'config/serverparameters.cfg').write_text(pins['native']['parameters']);(native/'config/maprot.cfg').write_text(pins['native']['rotation'])
   for name in ['serverpwd.cfg','serverblacklist.cfg','geoip.cfg','nicknameblacklist.cfg','forbidden.cfg']:(native/'config'/name).write_bytes(b'')
   pack=root/pins['pack']['root']
   for name in ['dev_outbreak_browser.cgz','dev_outbreak_browser.cfg','dev_outbreak_browser.cgz.LICENSE.txt']:(native/'packages/maps/servermaps'/name).write_bytes((pack/'packages/maps'/name).read_bytes())
   (native/'LICENSE.txt').write_bytes((pack/'LICENSE.txt').read_bytes())
   report['staged']={str(p.relative_to(native)):policy.sha(p.read_bytes()) for p in native.rglob('*') if p.is_file()}
   fd,slave=pty.openpty();argv=[str(root/pins['native']['binary']),*pins['native']['argv_tail']];report['native_argv']=argv
   n=subprocess.Popen(argv,cwd=native,env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','LANG':'C','LC_ALL':'C'},stdin=subprocess.DEVNULL,stdout=slave,stderr=slave,start_new_session=True);os.close(slave);slave=None
   report['native_pid']=n.pid;os.set_blocking(fd,False);selector.register(fd,selectors.EVENT_READ,'native')
   def hardstop():
    for p in [child,n]:
     if p is not None and p.poll() is None:
      try:os.killpg(p.pid,signal.SIGKILL);report['kill_fallback']=True
      except ProcessLookupError:pass
   watch=threading.Timer(180,hardstop);watch.daemon=True;watch.start()
   until=time.monotonic()+8
   while time.monotonic()<until and n.poll() is None:
    drain()
    if b'dedicated server started' in buffers['native'] and b'added 1 servermaps' in buffers['native']:break
   policy.require(n.poll() is None and b'added 1 servermaps' in buffers['native'],'native startup')
   loaded=command(['/usr/sbin/lsof','-nP','-p',str(n.pid),'-F','ftn']);report['native_loaded']=loaded
   for name,row in pins['files'].items():
    if row['role']=='library':policy.require('n'+str(root/name)+'\n' in loaded['stdout'],'actual loaded library missing')
   # No caps in this JSON. Node makes two fresh one-use values in memory.
   child_plan={**pins,**receipt,'root':str(root),'result':str(result)}
   if self.case_kind=='impaired40_drop50':child_plan['case_kind']=self.case_kind
   planpath=result/'validated-plan.json';planpath.write_text(json.dumps(child_plan))
   env={'PATH':'/usr/bin:/bin','WS_NO_BUFFER_UTIL':'1','WS_NO_UTF_8_VALIDATE':'1','TMPDIR':str(result)}
   child=subprocess.Popen([pins['tools']['node'],str(HERE/'observe.cjs'),str(planpath)],cwd=result,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
   selector.register(child.stdout,selectors.EVENT_READ,'stdout');selector.register(child.stderr,selectors.EVENT_READ,'stderr')
   while child.poll() is None:
    drain();scan_owned();policy.require(n.poll() is None,'native exited');policy.require(time.monotonic()-start<160,'baseline deadline including owned cleanup reserve')
   child.wait(timeout=1)
   while any(k.data in ('stdout','stderr') for k in selector.get_map().values()):drain()
   report['observer']=json.loads(buffers['stdout']);policy.require(child.returncode==0,'observer failed')
   proof=report['observer'];contract=pins['diagnostic_contract']
   for sample in proof['active']:policy.observation(sample,contract,True)
   policy.require(proof['active'][0]['network']['own']['cn']!=proof['active'][1]['network']['own']['cn'],'duplicate cn')
   policy.require(len(proof['moves'])==2 and [m['mover'] for m in proof['moves']]==['A','B'] and not proof['errors'],'two directional proofs required')
   g=proof['gateway_receipt'];policy.require(g['failure'] is None and g['counters']['admitted']==2 and g['counters']['udp_allocated']==2 and len(g['sessions'])==2,'gateway pair receipt')
   tuples=[s['udp_tuple'] for s in g['sessions']];policy.require(all(t['address']=='127.0.0.1' and policy.integer(t['port'],1,65535) for t in tuples) and tuples[0]['port']!=tuples[1]['port'],'distinct gateway UDP tuples')
   ports.extend(('UDP',t['port']) for t in tuples);ports.extend(('TCP',x) for x in proof['control_ports'])
   for move in proof['moves']:
    for s in [move['a_before'],move['a_settled'],move['b_before'],move['b_after']]:policy.observation(s,contract,True)
    policy.cross_receipt(move['a_before'],move['a_settled'],move['b_before'],move['b_after'],move['elapsed_ms'])
   report['evidence_validated']=True
  except Exception as e:report['errors'].append(str(e))
  finally:
   if child is not None and child.poll() is None:
    os.killpg(child.pid,signal.SIGTERM)
    try:child.wait(timeout=5)
    except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait(timeout=1);report['kill_fallback']=True
   shutdown=time.monotonic()
   if n is not None:
    if n.poll() is None:os.killpg(n.pid,signal.SIGINT)
    while n.poll() is None and time.monotonic()-shutdown<3:drain()
    if n.poll() is None:os.killpg(n.pid,signal.SIGKILL);report['kill_fallback']=True
    n.wait(timeout=1);report['native_exit']=n.returncode;report['native_shutdown_ms']=(time.monotonic()-shutdown)*1000
   # Discover isolated-profile Chrome even if Node died before its final JSON.
   # Re-check command/parent identity before signalling; never kill unrelated PIDs.
   current=scan_owned();left=[pid for pid,row in owned.items() if pid in current and ownership.same_identity(row,current[pid])]
   if left:
    report['errors'].append('observer left owned browser resources; reruns frozen');report['kill_fallback']=True
    ownership.signal_owned(owned,current,os.kill,signal.SIGTERM)
    deadline=time.monotonic()+2
    while time.monotonic()<deadline:
     current=scan_owned()
     if not any(pid in current and ownership.same_identity(owned[pid],current[pid]) for pid in left):break
     time.sleep(.05)
    current=scan_owned()
    ownership.signal_owned(owned,current,os.kill,signal.SIGKILL)
   import shutil
   for base in result.glob('browser-temp-*'):
    policy.require(base.parent==result and not base.is_symlink(),'owned profile root changed')
    if base.is_dir():shutil.rmtree(base)
   report['owned_browser_processes']=[{k:r[k] for k in ('pid','ppid','pgid')} for r in owned.values()]
   try:drain(0)
   except Exception as e:report['errors'].append(str(e))
   selector.close()
   for f in [fd,slave]:
    if f is not None:os.close(f)
   if child is not None:child.stdout.close();child.stderr.close()
   groups=[]
   for proc in [child,n]:
    if proc is not None:
     try:os.killpg(proc.pid,0);groups.append({'pgid':proc.pid,'gone':False})
     except ProcessLookupError:groups.append({'pgid':proc.pid,'gone':True})
   report['process_groups']=groups
   browser_gone=[]
   for pid in report.get('observer',{}).get('browser_pids',[]):
    try:os.kill(pid,0);browser_gone.append(False)
    except ProcessLookupError:browser_gone.append(True)
   receiptpath=result/'browser-ownership.json'
   if receiptpath.exists():
    policy.require(not receiptpath.is_symlink() and receiptpath.stat().st_size<16384,'invalid early ownership receipt')
    early=json.loads(receiptpath.read_text());policy.require(early.get('schema_version')==1 and len(early.get('control_ports',[]))<=2,'early receipt schema')
    for port in early['control_ports']:policy.require(policy.integer(port,1,65535),'invalid owned control port');ports.append(('TCP',port))
    report['early_browser_ownership']=early
   # T077: failure before baseline proof still owns final/retired gateway tuples.
   observed_udp,tuple_errors=policy.gateway_cleanup_ports(report.get('observer',{}))
   ports.extend(('UDP',port) for port in observed_udp)
   report['gateway_tuple_cleanup']={'ports':observed_udp,'complete':not tuple_errors,'errors':tuple_errors}
   report['errors'].extend(tuple_errors)
   report['ports']=free_ports(set(ports))
   report['tcp_cleanup']=command(['/usr/sbin/lsof','-nP',*['-iTCP:'+str(p) for protocol,p in set(ports) if protocol=='TCP'],'-sTCP:LISTEN'])
   report['udp_cleanup']=command(['/usr/sbin/lsof','-nP',*['-iUDP:'+str(p) for protocol,p in set(ports) if protocol=='UDP']])
   report['source_stable']=all(view.hash(p)==r['sha256'] for p,r in pins['files'].items())
   report['elapsed_ms']=(time.monotonic()-start)*1000
   # Cleanup is independently verified below; missing facts never default to success.
   c=report.get('observer',{}).get('cleanup',{})
   current=scan_owned();owned_gone=all(pid not in current or not ownership.same_identity(row,current[pid]) for pid,row in owned.items())
   report['cleanup']={**c,'groups_reaped':len(groups)==2 and all(r['gone'] for r in groups) and len(browser_gone)==2 and all(browser_gone) and owned_gone,'handles_empty':c.get('gateway_closed') is True and c.get('static_closed') is True and c.get('browsers_stopped') is True,'native_exit':report.get('native_exit'),'native_shutdown_ms':report.get('native_shutdown_ms'),'kill_fallback':report.get('kill_fallback',False),'ports_released':not tuple_errors and all(r['bind'] for r in report['ports']) and all(report[k]['exit']==1 and not report[k]['stdout'] and not report[k]['stderr'] for k in ('tcp_cleanup','udp_cleanup'))}
   try:
    if self.case_kind=='impaired40_drop50':policy.shaper_receipt(report.get('observer',{}).get('shaper'))
    policy.cleanup_ok(report['cleanup']);policy.require(report.get('evidence_validated') and report['source_stable'] and not report['errors'] and report['elapsed_ms']<=180000,'incomplete runtime evidence');report['status']='PASS'
   except Exception as e:report['errors'].append(str(e))
   report['reruns_frozen']=report.get('native_exit')!=0 or report['status']!='PASS'
   if watch:watch.cancel()
   # Redaction precedes every persisted diagnostic, including raw stderr/native logs.
   (result/'result.json').write_text(json.dumps(policy.redact(report),indent=2)+'\n')
   for k,v in buffers.items():(result/(k+'.log')).write_text(policy.redact(v.decode(errors='replace')))
  return report

def main():
 p=argparse.ArgumentParser();p.add_argument('--prepare-plan',action='store_true');p.add_argument('--execute',action='store_true');p.add_argument('--pins');p.add_argument('--pins-sha');p.add_argument('--attempt');args=p.parse_args()
 if args.prepare_plan and not any([args.execute,args.pins,args.pins_sha,args.attempt]):print(json.dumps(plan(),indent=2));return 0
 policy.require(args.execute and args.pins and args.pins_sha and args.attempt and not args.prepare_plan,'future MAIN execution pins required; no action')
 result=gated_execute(ROOT,args.pins,args.pins_sha,args.attempt,Runtime(ROOT));print(json.dumps(policy.redact(result),indent=2));return 0 if result['status']=='PASS' else 1
if __name__=='__main__':
 try:raise SystemExit(main())
 except (policy.Refused,ValueError,OSError) as e:print(json.dumps({'status':'REFUSED','reason':str(e),'runtime_started':EXECUTION_STARTED,'success_claimed':False}));raise SystemExit(2)
