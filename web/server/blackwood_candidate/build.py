"""T167 candidate builder. Preparation plans are pure; real tools need MAIN pins."""
import argparse,errno,json,os,time
from pathlib import Path
import stage
ROOT=stage.ROOT
_OWNED_CHILD_HANDLES=[] # Strong original handles remain here when reap is unresolved.
_OWNED_CLOSE_RESOURCES=[] # Never retry or destroy ambiguous/expired close resources.
_BORROWED_GUARDS=[]

WAIT_ABI={'platform':'darwin','machine':'arm64','byteorder':'little','int':4,'uint':4,'long':8,'ulong':8,'pointer':8,'record':104,'alignment':8,'pid_offset':12,'status_offset':20}

def bind_wait_function(ffi,library,Info):
 function=library.waitid;function.argtypes=[ffi.c_int,ffi.c_uint32,ffi.POINTER(Info),ffi.c_int];function.restype=ffi.c_int;return function

def native_wait_call(ffi,function,Info,pid,zero):
 stage.need(stage.integer(pid,1,2**31-1) and type(zero) is bytes and zero==bytes(104),'fixed PID and whole104 zero record')
 info=Info();ffi.memset(ffi.byref(info),0,104);ffi.set_errno(0);result=function(1,pid,ffi.byref(info),37)
 return result,ffi.get_errno(),ffi.string_at(ffi.byref(info),104)

def load_darwin_waitid():
 """D235 dormant fixed loader. Never called or imported in preparation fixtures."""
 import ctypes
 import platform
 import sys
 class Value(ctypes.Union):_fields_=[('integer',ctypes.c_int),('pointer',ctypes.c_void_p)]
 class Info(ctypes.Structure):
  _fields_=[('signo',ctypes.c_int),('error',ctypes.c_int),('code',ctypes.c_int),('pid',ctypes.c_int32),('uid',ctypes.c_uint32),('status',ctypes.c_int),('address',ctypes.c_void_p),('value',Value),('band',ctypes.c_long),('pad',ctypes.c_ulong*7)]
 abi={'platform':sys.platform,'machine':platform.machine(),'byteorder':sys.byteorder,'int':ctypes.sizeof(ctypes.c_int),'uint':ctypes.sizeof(ctypes.c_uint),'long':ctypes.sizeof(ctypes.c_long),'ulong':ctypes.sizeof(ctypes.c_ulong),'pointer':ctypes.sizeof(ctypes.c_void_p),'record':ctypes.sizeof(Info),'alignment':ctypes.alignment(Info),'pid_offset':Info.pid.offset,'status_offset':Info.status.offset}
 stage.need(abi==WAIT_ABI,'fixed Darwin arm64 LP64 waitid ABI required before library resolution')
 library=ctypes.CDLL('/usr/lib/libSystem.B.dylib',use_errno=True);function=bind_wait_function(ctypes,library,Info)
 class Native:
  def __init__(self):self.abi=abi;self.library=library
  def call(self,pid,zero):
   return native_wait_call(ctypes,function,Info,pid,zero)
 return Native()

class DarwinWaitid:
 """Actual adapter logic with a fake native boundary during preparation only."""
 def __init__(self,native=None):
  self.native=load_darwin_waitid() if native is None else native;stage.need(type(self.native.abi) is dict and self.native.abi==WAIT_ABI,'unsupported nonreaping ABI/layout');self.owner=None;self.pid=None;self.last=None;self.anchor_lost=False
 def bind(self,child):
  stage.need(stage.integer(child.pid,1,2**31-1) and getattr(child,'returncode',None) is None,'original waitable child required');self.owner=child;self.pid=child.pid;self.last=None;self.anchor_lost=False
 def require_anchor(self,child):
  good=not self.anchor_lost and child is self.owner and child.pid==self.pid and getattr(child,'returncode',None) is None
  if not good:self.anchor_lost=True
  stage.need(good,'original unreaped anchor lost')
 def observe(self,child,check):
  for _ in range(16):
   check();self.require_anchor(child)
   result,error,data=self.native.call(self.pid,bytes(104))
   self.last={'pid':self.pid,'result':result if type(result) is int else None,'errno':error if type(error) is int else None,'record_bytes':len(data) if type(data) is bytes else None,'record_hex':data[:104].hex() if type(data) is bytes else None}
   if not (type(result) is int and type(error) is int and type(data) is bytes and len(data)==104) or result==-1 and error!=4 or result not in (0,-1) or result==0 and error!=0:self.anchor_lost=True
   check();self.require_anchor(child)
   if result==-1:
    if error==4:continue # Darwin EINTR; original absolute deadline and finite retry cap remain.
    raise stage.Refused('waitid ECHILD/lost anchor' if error==10 else 'waitid errno '+str(error))
   stage.need(result==0 and error==0,'unexpected waitid result/errno')
   if data==bytes(104):return None
   signo,association,code,pid,uid,status=stage.struct.unpack_from('<iiiiIi',data)
   if not (signo==20 and association==0 and pid==self.pid and code in (1,2,3) and (0<=status<=255 if code==1 else 1<=status<=31)):self.anchor_lost=True;raise stage.Refused('waitid terminal event identity/status; anchor uncertain')
   return {'pid':pid,'signo':signo,'code':code,'status':status,'errno':association}
  raise stage.Refused('bounded waitid EINTR retries exhausted')

def pin_bytes(root,path,expected):
 p=Path(path);stage.need(p.is_absolute() and p.parent==Path(root)/'notes/decisions' and p.suffix=='.json' and not p.is_symlink() and p.is_file(),'absolute MAIN pin JSON required')
 stage.need(p.stat().st_nlink==1 and p.stat().st_size<=stage.MAX_CONTROL and all(q.is_dir() and not q.is_symlink() for q in p.parents),'ordinary bounded MAIN control')
 data=stage.read_bounded(p,stage.MAX_CONTROL);stage.need(stage.sha(data)==stage.digest(expected),'pins digest changed');return data

class RealOps:
 """All process/tool boundaries are injected in preparation; no import-time effects."""
 clock=staticmethod(time.monotonic)
 def spawn(self,argv,root,env):
  import subprocess
  return subprocess.Popen(argv,cwd=root,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 def retain(self,child):self.wait_adapter.bind(child)
 def native_last(self,child):return self.wait_adapter.last if child is not None and hasattr(self,'wait_adapter') and self.wait_adapter.owner is child else None
 def selector(self):
  import selectors
  return selectors.DefaultSelector()
 def nonblock(self,p):os.set_blocking(p.fileno(),False)
 def register(self,s,p,tag):
  import selectors
  s.register(p,selectors.EVENT_READ,tag)
 def select(self,s,timeout):return s.select(timeout)
 def unregister(self,s,p):s.unregister(p)
 def read(self,p):return os.read(p.fileno(),16384)
 def observe_exit(self,child,check):return self.wait_adapter.observe(child,check)
 def process_support(self):
  import signal
  stage.need(signal.getsignal(signal.SIGCHLD)==signal.SIG_DFL,'default SIGCHLD disposition required; no auto/external reap')
  if not hasattr(self,'wait_adapter'):self.wait_adapter=DarwinWaitid()
 def kill(self,child,check):
  import signal
  if self.wait_adapter.owner is not child:self.wait_adapter.bind(child)
  self.wait_adapter.require_anchor(child);self.wait_adapter.observe(child,check);check();self.wait_adapter.require_anchor(child)
  stage.need(stage.integer(child.pid,1,2**31-1) and getattr(child,'returncode',None) is None,'mutating group cleanup requires original unreaped handle passed by Runner')
  os.killpg(child.pid,signal.SIGKILL)
 def wait(self,child,timeout):
  self.wait_adapter.require_anchor(child);stage.need(0<timeout<=2,'original bounded handle wait')
  original=child._try_wait
  def strict_try_wait(flags):
   stage.need(flags==os.WNOHANG,'nonblocking original-handle wait primitive')
   try:pid,status=os.waitpid(child.pid,flags)
   except ChildProcessError:self.wait_adapter.anchor_lost=True;raise stage.Refused('ECHILD during original-handle wait; never pretend exit0')
   stage.need(pid in (0,child.pid),'original-handle wait returned another PID');return pid,status
  child._try_wait=strict_try_wait
  try:return child.wait(timeout=timeout)
  finally:child._try_wait=original
 def group_empty(self,child):
  # Read-only existence observation after reaping. Never send a mutating signal now.
  try:os.killpg(child.pid,0);return False
  except ProcessLookupError:return True
 def close(self,value):value.close()
 def arm(self,state,callback,seconds):
  import signal
  stage.need(signal.getitimer(signal.ITIMER_REAL)==(0.0,0.0),'existing alarm owner; refuse rather than replace')
  state['previous']=signal.signal(signal.SIGALRM,lambda *_:callback());state['handler']=True;state['timer_attempted']=True
  signal.setitimer(signal.ITIMER_REAL,seconds)
 def restore(self,state,failed,check):
  import signal
  okay=True
  if state.get('timer_attempted'):
   try:check();signal.setitimer(signal.ITIMER_REAL,0);state['timer_restored']=True;check()
   except BaseException as e:failed('timer_restore_SKIPPED_OR_FAILED',e);okay=False
  if state.get('handler'):
   try:check();signal.signal(signal.SIGALRM,state['previous']);state['handler_restored']=True;check()
   except BaseException as e:failed('handler_restore_SKIPPED_OR_FAILED',e);okay=False
  return okay
 def persist(self,base,name,data,check):check();stage.owned_path(base,Path(base)/name,absent=True);stage.durable_new(Path(base)/name,data,check=check)

class Runner:
 """Bounded original-handle ownership, independent teardown and honest group closure."""
 def __init__(self,root,base,persist=True,fx=None,view=None,started=None):
  self.root=Path(root);self.base=Path(base);self.persist=persist;self.fx=RealOps() if fx is None else fx;self.view=stage.View(root) if view is None else view
  self.started=self.fx.clock() if started is None else started;self.end=self.started+1800;self.total_bytes=0;self.records=[];self.acquiring=False;self.expired=False;self.cleaning=False;self.view.deadline_check=self.check
  self.env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','TMPDIR':str(self.base/'tmp'),'CLANG_MODULE_CACHE_PATH':str(self.base/'tmp/modules')}
 def check(self,end=None):stage.need((end is None or not self.expired) and self.fx.clock()<min(self.end,self.end if end is None else end),'absolute deadline expired')
 def guard(self):
  self.expired=True
  if not self.acquiring and not self.cleaning:raise stage.Refused('operation/whole guard; cleanup reserve only')
 def run(self,kind,argv):
  self.cleaning=False;start=self.fx.clock();end=min(start+120,self.end);work=end-10;index=len(self.records);buffers=[bytearray(),bytearray()];child=None;selector=None;pipes={};guard={};active={};reaped=False
  row={'index':index,'kind':kind,'argv':list(argv),'environment':self.env,'tool_role':None,'timeout_s':120,'pid':None,'returned_handle':False,'ownership':'NO_RETURNED_HANDLE','exit':None,'child_reaped':False,'nonreaping':None,'native_last':None,'group_empty':None,'group_signal':'NOT_ATTEMPTED','timed_out':False,'overflow':False,'primary':None,'secondary':[],'cleanup_attempts':[],'io_unresolved':[],'elapsed_ms':0,'stdout_path':f'logs/{index:03d}.stdout','stderr_path':f'logs/{index:03d}.stderr','stdout_sha256':None,'stderr_sha256':None,'stdout_bytes':0,'stderr_bytes':0,'publication':'PENDING','status':'FAILED'}
  self.records.append(row)
  def primary(e):
   if row['primary'] is None:row['primary']=str(e)[:512]
  def secondary(action,e):row['secondary'].append({'action':action,'error':str(e)[:512]})
  def publication_failure(action,e):
   primary(e);secondary(action,e)
   if isinstance(e,stage.DurabilityFailure):row['io_unresolved'].extend(h.describe() for h in e.handles)
  def persistence_check():stage.need(self.fx.clock()<end,'original command/whole persistence cutoff')
  def cleanup(action,fn,resource=None):
   row['cleanup_attempts'].append(action)
   if self.fx.clock()>=end:
    if resource is not None:_OWNED_CLOSE_RESOURCES.append((resource,action,'SKIPPED_EXPIRED'))
    secondary(action,'SKIPPED_EXPIRED: original cleanup deadline exhausted; resource retained');return None
   try:return fn()
   except BaseException as e:
    if resource is not None:_OWNED_CLOSE_RESOURCES.append((resource,action,'UNRESOLVED_CLOSE_ERROR'))
    secondary(action,e);return None
  try:
   stage.need(end-start>=20,'insufficient original cleanup reserve; no spawn');self.check(work)
   self.check(work);self.fx.arm(guard,self.guard,max(0,work-self.fx.clock()));self.check(work);self.fx.process_support();self.check(work)
   role=next((r for r,p in stage.TOOLS.items() if p==argv[0]),None);stage.need(role is not None,'unknown fixed tool role');row['tool_role']=self.view.arm_tool(role,self.view.declared_inputs[argv[0]]);self.check(work)
   self.acquiring=True
   try:child=self.fx.spawn(argv,self.root,self.env)
   finally:self.acquiring=False
   row['returned_handle']=True;row['pid']=child.pid;row['ownership']='RETURNED_UNRESOLVED'
   self.fx.retain(child);self.check(work)
   for name in ('stdout','stderr'):pipes[name]=getattr(child,name)
   self.check(work);selector=self.fx.selector()
   for tag,name in enumerate(('stdout','stderr')):
    self.check(work);self.fx.nonblock(pipes[name]);self.check(work);self.fx.register(selector,pipes[name],tag);active[tag]=pipes[name]
   while active:
    self.check(work)
    for key,_ in self.fx.select(selector,min(.05,work-self.fx.clock())):
     self.check(work)
     try:data=self.fx.read(key.fileobj)
     except BlockingIOError:continue
     if not data:self.fx.unregister(selector,key.fileobj);active.pop(key.data)
     else:
      remaining=min(stage.MAX_LOG-sum(map(len,buffers)),64*1024*1024-self.total_bytes)
      take=max(0,min(len(data),remaining));buffers[key.data].extend(data[:take]);self.total_bytes+=len(data)
      if take<len(data):row['overflow']=True;raise stage.Refused('command/aggregate output overflow before retention')
   # Keep original child unreaped while observing termination and cleaning its group.
   while True:
    self.check(work)
    observed=self.fx.observe_exit(child,lambda:self.check(work))
    if observed is not None:row['nonreaping']=observed;break
    self.fx.select(selector,min(.05,work-self.fx.clock()))
  except BaseException as e:
   primary(e);row['timed_out']=self.expired or self.fx.clock()>=work
  finally:
   self.cleaning=True
   if child is not None and not any(h is child for h in _OWNED_CHILD_HANDLES):_OWNED_CHILD_HANDLES.append(child)
   try:row['native_last']=self.fx.native_last(child)
   except BaseException as e:secondary('capture_native_last',e)
   if child is not None:
    row['returned_handle']=True;row['ownership']='RETURNED_UNRESOLVED';row['pid']=child.pid
    for name in ('stdout','stderr'):
     if name not in pipes:
      try:pipes[name]=getattr(child,name)
      except BaseException as e:secondary('retain_'+name,e)
    def signal_owned():
     try:self.fx.kill(child,persistence_check);row['group_signal']='SIGKILL_SENT_WHILE_ANCHORED'
     except ProcessLookupError:row['group_signal']='ESRCH_WHILE_ANCHORED'
     except PermissionError as e:
      if e.errno!=errno.EPERM:raise
      row['group_signal']='EPERM_DENIED_WHILE_ANCHORED'
      if not stage.exit0_observation(row['nonreaping'],child.pid):raise
    cleanup('signal_anchored_group',signal_owned)
    try:row['native_last']=self.fx.native_last(child)
    except BaseException as e:secondary('capture_cleanup_native_last',e)
    def wait_original():
     remaining=end-self.fx.clock();stage.need(remaining>0,'no original reap budget');return self.fx.wait(child,min(2,remaining))
    code=cleanup('wait_original_handle',wait_original)
    if code is not None:row['exit']=code;row['child_reaped']=reaped=True;row['ownership']='REAPED'
    if reaped:_OWNED_CHILD_HANDLES[:]=[h for h in _OWNED_CHILD_HANDLES if h is not child]
    row['group_empty']=cleanup('observe_group_empty_readonly',lambda:self.fx.group_empty(child)) if reaped else None
   if selector is not None:cleanup('selector_close',lambda:self.fx.close(selector),selector)
   for name,pipe in pipes.items():cleanup(name+'_close',lambda p=pipe:self.fx.close(p),pipe)
   # Alarm restoration is independent and before receipt publication.
   if not self.fx.restore(guard,secondary,persistence_check):_BORROWED_GUARDS.append((self.fx,guard))
   row['timed_out']=row['timed_out'] or self.expired or self.fx.clock()>=end
   if row['timed_out']:primary('original deadline crossed')
   if row['exit']!=0 or not reaped or row['group_empty'] is not True:primary('nonzero/unreaped/unresolved group closure')
   if row['group_signal']=='EPERM_DENIED_WHILE_ANCHORED' and not (stage.exit0_observation(row['nonreaping'],row['pid']) and type(row['exit']) is int and row['exit']==0 and reaped and row['group_empty'] is True):primary('EPERM denial lacks confirmed original exit0/reap0/empty group')
   if row['nonreaping'] is not None:
    expected=row['nonreaping']['status'] if row['nonreaping']['code']==1 else -row['nonreaping']['status']
    if row['exit']!=expected:primary('nonreaping observation differs from original-handle wait')
   elif row['primary'] is None:primary('no nonreaping terminal event')
   for name,data in zip(('stdout','stderr'),buffers):
    row[name+'_sha256']=stage.sha(bytes(data));row[name+'_bytes']=len(data)
    if self.persist:
     try:
      persistence_check();self.fx.persist(self.base,row[name+'_path'],bytes(data),persistence_check);persistence_check()
     except BaseException as e:publication_failure('persist_'+name,e)
   row['elapsed_ms']=(self.fx.clock()-start)*1000
   row['status']='PASS' if row['primary'] is None and not row['secondary'] and not row['overflow'] and not row['timed_out'] else 'FAILED'
   if self.persist:
    saved=row['status'];row['status']='PENDING_PUBLICATION' if saved=='PASS' else saved
    try:
     persistence_check();self.fx.persist(self.base,f'logs/{index:03d}.receipt.json',stage.canonical_json(row).encode(),persistence_check);persistence_check();row['publication']='CONFIRMED';row['status']=saved
    except BaseException as e:publication_failure('persist_receipt',e);row['status']='FAILED'
   else:row['publication']='NOT_REQUESTED_READONLY'
   row['elapsed_ms']=(self.fx.clock()-start)*1000
   row['timed_out']=row['timed_out'] or self.fx.clock()>=end
   if row['timed_out'] or row['io_unresolved']:row['status']='FAILED'
  stage.need(row['status']=='PASS','command refused: '+str(row['primary']))
  return index,buffers[0].decode(errors='replace'),buffers[1].decode(errors='replace')

def fixed_inspections(base,plan):
 copy=str(base/'deps-signed/SDL2.framework');nested=copy+'/Versions/A/Frameworks/hidapi.framework'
 libraries=[copy+'/Versions/A/SDL2',nested+'/Versions/A/hidapi']
 return libraries

def tool_identity(text):
 stage.need('Apple clang version 17.' in text and 'Target: arm64-apple-darwin' in text and 'InstalledDir: '+stage.CLT+'/usr/bin' in text,'installed Apple17/arm64/CLT identity mismatch; question before flags')

def load_identity(text,base,kind):
 paths=stage.rpaths(text,[str(base/'deps-signed'),str(base/'deps-signed/SDL2.framework/Versions/A/Frameworks')]) if kind=='server' else re_rpaths(text)
 if kind=='server':stage.need('source/xcode/Frameworks' not in text and 'deps-signed' in text,'original/old RPATH leaked')
 return paths
def re_rpaths(text):
 import re
 return re.findall(r'cmd LC_RPATH\n\s*cmdsize \d+\n\s*path (.*?) \(offset',text)

def link_inputs(text,objects,view,ident,signed):
 """ld -t file list; only declared inputs, own objects and exact signed copy."""
 files={};copy=stage.attempt(view.root,ident)+'/deps-signed/SDL2.framework'
 for line in text.splitlines():
  line=line.strip()
  if not line:continue
  import re
  archive=re.fullmatch(r'(.+\.a)\(([^/()]+)\)',line);member=archive.group(2) if archive else None
  path=archive.group(1) if archive else line;stage.absolute(path);physical=view.canonical(path)
  stage.need(view.consume(physical),'nonordinary/multilink/role-as-link-input')
  if physical in objects:origin='OWN_FRESH_OBJECT'
  elif stage.beneath(physical,copy):
   name=physical[len(copy)+1:];stage.need(name in signed and signed[name]['kind']=='file' and view.hash(physical)==signed[name]['sha256'],'unknown/changed staged linker input');origin='OWN_SIGNED_FRAMEWORK'
  else:
   stage.need(stage.sdk_link_path(view,path)==physical and stage.beneath(physical,stage.CLT) and physical in view.declared_inputs and view.hash(physical)==view.declared_inputs[physical],'undeclared/changed/non-SDK linker input');origin=physical
  if physical not in files:files[physical]={'origin':origin,'sha256':view.hash(physical),'archive_members':[]}
  if member and member not in files[physical]['archive_members']:files[physical]['archive_members'].append(member)
 stage.need(set(objects)<=set(files),'linker trace missing fresh objects')
 stage.need(copy+'/Versions/A/SDL2' in files,'actual copied SDL2 link input absent')
 stage.need(any(stage.beneath(n,stage.SDK+'/usr/lib') for n in files),'SDK linker input absent')
 stage.need(stage.SDK+'/usr/lib/libc++.1.tbd' in files and stage.CLT+'/usr/lib/clang/17/lib/darwin/libclang_rt.osx.a' in files,'canonical C++ text stub/runtime archive absent from actual link closure')
 return dict(sorted(files.items()))

def execute(root,ident,pin,expected):
 fx=RealOps();started=fx.clock()
 def whole_check():stage.need(fx.clock()<started+1800,'original whole attempt cutoff')
 view=stage.View(root);view.deadline_check=whole_check;whole_check();data=pin_bytes(root,pin,expected);auth=stage.authorize(data,expected,ident,view);whole_check();base=Path(stage.attempt(view.root,ident));container_preexisting=base.parent.exists()
 protection=stage.protected_inventory(view.root);whole_check();base=stage.reserve(view.root,ident,whole_check);view.active=str(base);view.omit_container=not container_preexisting;view.declared_inputs=auth['observation']['inputs'];runner=Runner(view.root,base,fx=fx,view=view,started=started);recipe=stage.commands(view.root,ident)
 record={'schema_version':1,'kind':'BLACKWOOD_NATIVE_BUILD_RECORD','recipe':'blackwood_native_standalone_v1','candidate_id':ident,'pins_path':str(pin),'pins_sha256':expected,'status':'RESERVED','fixture_only':bool(view.fixture_only),'source_revision':auth['source_revision'],'source_manifest':auth['source_manifest'],'source_acceptance':auth['source_acceptance'],'map_seed':None,'claims':stage.CLAIMS.copy(),'object_reuse':False,'container_preexisting':container_preexisting,'protection_before':protection,'steps':runner.records,'tool_identity':{},'stage_before':None,'stage_after':None,'sign_steps':[],'signature_steps':[],'framework_checks':[],'modes':{},'errors':[],'elapsed_ms':0}
 def current(full=False):
  stage.authorize(pin_bytes(view.root,pin,expected),expected,ident,view,existing=True,verify_preservation=full)
  stage.owned_paths(base,auth['observation']['source_framework'])
  if full:stage.need(stage.protected_inventory(view.root,str(base),not container_preexisting)==protection,'original membership/mode/link changed')
 def inspect(path,kind,rpaths_required=False):
  stage.owned_path(base,path)
  stage.need(view.ordinary(path) and view.canonical(path)==path and (kind!=2 or view.mode(path)&0o100),'ordinary executable artifact required')
  stage.macho(Path(path).read_bytes(),kind);rows={}
  for role,args in [('file',[stage.TOOLS['file'],path]),('dependencies',[stage.TOOLS['otool'],'-L',path]),('load_commands',[stage.TOOLS['otool'],'-l',path]),('signature',[stage.TOOLS['codesign'],'--verify','--verbose=4',path]),('adhoc',[stage.TOOLS['codesign'],'--display','--verbose=4',path])]:
   index,out,err=runner.run(role,args);rows[role]=index
   if role=='file':stage.need('arm64' in out and 'Mach-O' in out,'actual file architecture')
   if role=='adhoc':stage.need('Signature=adhoc' in err,'actual ad-hoc signature not observed')
   if role=='load_commands':
    if rpaths_required:load_identity(out,base,'server')
    else:stage.need(all(p in ('@loader_path/Frameworks','@executable_path/Frameworks') for p in re_rpaths(out)),'unconfined framework RPATH')
   if role=='dependencies':
    names=stage.otool_dependencies(out,path)
    stage.need(names and all((n in ('@rpath/SDL2.framework/Versions/A/SDL2','@rpath/hidapi.framework/Versions/A/hidapi') or n.startswith(('/usr/lib/','/System/Library/Frameworks/'))) and '..' not in n.split('/') for n in names),'non-system/unconfined dynamic dependency')
    if rpaths_required:stage.need('@rpath/SDL2.framework/Versions/A/SDL2' in names,'native SDL dependency missing')
  return {'path':path,'sha256':view.hash(path),'kind':kind,'steps':rows}
 try:
  runner.check();stage.durable_new(base/'plan.json',stage.canonical_json(plan(view.root,ident,auth)).encode(),stage.MAX_CONTROL,check=runner.check)
  record['map_seed']=stage.stage_seed(view,base,auth['observation']['map_seed'],runner.check)
  for role in ('cc','cxx'):
   index,out,err=runner.run('compiler_identity',[stage.TOOLS[role],'--version']);tool_identity(out);record['tool_identity'][role]=index
  stage.need(view.json(stage.SDK+'/SDKSettings.json').get('Version')=='15.5','actual SDK version mismatch')
  current();copy=stage.stage_copy(view.root,ident,auth['observation']['source_framework'],runner.check);record['stage_before']=stage.inventory(copy)
  for argv in recipe['sign']:record['sign_steps'].append(runner.run('adhoc_sign_copy',argv)[0])
  for argv in recipe['signature']:record['signature_steps'].append(runner.run('verify_copy_signature',argv)[0])
  record['stage_after']=stage.signed_inventory(record['stage_before'],stage.inventory(copy))
  for path in fixed_inspections(base,recipe):record['framework_checks'].append(inspect(path,6))
  for mode,spec in recipe['modes'].items():
   m={'units':[],'binary':spec['binary'],'link_step':None,'link_inputs':{},'inspection':None};record['modes'][mode]=m;objects=[]
   for row in spec['units']:
    current();stage.need(all(not Path(row[k]).exists() and not Path(row[k]).is_symlink() and all(not q.is_symlink() for q in Path(row[k]).parents) for k in ('object','dep','pre_dep')),'object/dependency reuse or alias refused')
    discover,_,_=runner.run('discover_dependencies',row['discover']);stage.owned_path(base,row['pre_dep']);stage.owned_paths(base,auth['observation']['source_framework']);before=stage.dependency_paths(Path(row['pre_dep']).read_text(),row['object'],view,ident);stage.need(view.root+'/'+row['unit'] in before,'actual prescan missing source unit')
    current();compile_index,_,_=runner.run('compile',row['compile']);stage.owned_path(base,row['dep']);stage.owned_path(base,row['object']);stage.owned_paths(base,auth['observation']['source_framework']);after=stage.dependency_paths(Path(row['dep']).read_text(),row['object'],view,ident);stage.need(before==after,'actual consumed dependency membership/bytes changed')
    stage.macho(Path(row['object']).read_bytes(),1);obj_index,out,err=runner.run('object_file',[stage.TOOLS['file'],row['object']]);stage.need('Mach-O 64-bit object arm64' in out,'actual object signature')
    m['units'].append({**row,'discover_step':discover,'compile_step':compile_index,'file_step':obj_index,'dependencies':before,'object_sha256':view.hash(row['object']),'pre_dep_sha256':view.hash(row['pre_dep']),'dep_sha256':view.hash(row['dep'])});objects.append(row['object'])
   current()
   for unit in m['units']:
    stage.owned_path(base,unit['object'])
    stage.need(view.hash(unit['object'])==unit['object_sha256'],'object changed before link')
    for name,d in unit['dependencies'].items():stage.need(view.hash(name)==d['sha256'],'actual dependency changed before link')
   stage.need(not Path(spec['binary']).exists() and not Path(spec['binary']).is_symlink(),'binary reuse/alias refused');index,out,err=runner.run('link',spec['link']);m['link_step']=index;m['link_inputs']=link_inputs(out,objects,view,ident,record['stage_after']);m['inspection']=inspect(spec['binary'],2,True)
  current(True);stage.need(record['map_seed']==stage.seed_record(base,auth['observation']['map_seed']),'seed changed before seal');runner.check();record['status']='BLACKWOOD_NATIVE_LINKED_NOT_RUN'
 except Exception as e:record['errors'].append(type(e).__name__+': '+str(e));record['status']='FAILED'
 finally:
  record['elapsed_ms']=(runner.fx.clock()-runner.started)*1000
  def final_check():
   runner.check();current(True);stage.need(record['map_seed']==stage.seed_record(base,auth['observation']['map_seed']),'final seed identity changed')
   stage.need(all(x['status']=='PASS' and x['publication']=='CONFIRMED' and x['child_reaped'] and x['group_empty'] is True for x in runner.records),'unresolved process/publication')
  Terminal(view,base,runner).seal(record,final_check)
 return record

class Terminal:
 """Keep failure marker through every required durable obligation; unlink last."""
 def __init__(self,view,base,runner):self.view=view;self.base=Path(base);self.runner=runner;self.errors=[]
 def seal(self,record,final_check):
  okay=record['status']=='BLACKWOOD_NATIVE_LINKED_NOT_RUN'
  try:final_check()
  except BaseException as e:okay=False;record['errors'].append(str(e)[:512]);record['status']='FAILED'
  try:
   self.runner.check();stage.owned_path(self.base,self.base/'report.json',absent=True);stage.durable_new(self.base/'report.json',stage.canonical_json(record).encode(),check=self.runner.check);self.runner.check()
  except BaseException as e:self.errors.append('report: '+str(e)[:512]);okay=False
  try:
   self.runner.check();items=stage.owned_inventory(self.base,record['stage_before'] or self.view.framework());items.pop('freeze.json',None);items.pop('failure.json',None);items.pop('verification/receipt.json',None)
   frozen={'schema_version':1,'kind':'BLACKWOOD_NATIVE_TERMINAL_FREEZE','candidate_id':record['candidate_id'],'status':record['status'],'fixture_only':record['fixture_only'],'files':items,'optional_receipt':'verification/receipt.json','claims':stage.CLAIMS.copy()}
   stage.owned_path(self.base,self.base/'freeze.json',absent=True);stage.durable_new(self.base/'freeze.json',stage.canonical_json(frozen).encode(),check=self.runner.check);self.runner.check()
  except BaseException as e:self.errors.append('freeze: '+str(e)[:512]);okay=False
  if okay:
   try:
    stage.need((self.base/'report.json').read_bytes()==stage.canonical_json(record).encode() and (self.base/'freeze.json').read_bytes()==stage.canonical_json(frozen).encode(),'terminal persisted bytes differ')
    actual=stage.owned_inventory(self.base,record['stage_before']);actual.pop('freeze.json',None);actual.pop('failure.json',None);actual.pop('verification/receipt.json',None);stage.need(actual==frozen['files'],'final complete owned graph differs')
    final_check();self.runner.check();stage.owned_path(self.base,self.base/'failure.json');os.unlink(self.base/'failure.json')
   except BaseException as e:self.errors.append('commit: '+str(e)[:512]);okay=False
  if not okay:
   record['status']='FAILED';record['errors'].extend(self.errors)
  return okay

def plan(root,ident,auth=None):
 ident=stage.identifier(ident)
 return {'schema_version':1,'kind':'BLACKWOOD_NATIVE_BUILD_PLAN','status':'NOT_EXECUTED','recipe':stage.RECIPE,'candidate_id':ident,'source_revision':auth['source_revision'] if auth else stage.View(root).head(),'source_manifest':auth['source_manifest'] if auth else None,'source_acceptance':auth['source_acceptance'] if auth else None,'observation':auth['observation'] if auth else None,'commands':stage.command_plan(str(root),ident),'environment':{'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','TMPDIR':stage.attempt(root,ident)+'/tmp','CLANG_MODULE_CACHE_PATH':stage.attempt(root,ident)+'/tmp/modules'},'claims':stage.CLAIMS.copy(),'pending':[] if auth else ['MAIN_COMMON_SOURCE_MANIFEST','EXPLICIT_EXECUTION_PINS_AND_RELEASE','CURRENT_DECLARED_OBSERVATION']}

def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--plan-only',action='store_true');g.add_argument('--execute',action='store_true');p.add_argument('--candidate-id',required=True);p.add_argument('--pins');p.add_argument('--pins-sha256');a=p.parse_args();stage.identifier(a.candidate_id)
 if a.plan_only:
  stage.need(not a.pins and not a.pins_sha256,'plan requires no execution identity');value=plan(ROOT,a.candidate_id);home=ROOT/'web/server/blackwood_candidate';stage.owned_path(home,home,'directory');out=home/('preparation-'+a.candidate_id);stage.owned_path(home,out,absent=True);out.mkdir(exist_ok=False);stage.durable_new(out/'plan.json',stage.canonical_json(value).encode(),stage.MAX_CONTROL);print(stage.canonical_json(value));return 0
 stage.need(a.pins and a.pins_sha256,'MAIN execution pins required');r=execute(ROOT,a.candidate_id,a.pins,a.pins_sha256);print(stage.canonical_json({'status':r['status'],'errors':r['errors'],'claims':r['claims']}));return 0 if r['status']=='BLACKWOOD_NATIVE_LINKED_NOT_RUN' else 1
if __name__=='__main__':
 try:raise SystemExit(main())
 except (stage.Refused,OSError,ValueError) as e:print(stage.canonical_json({'status':'REFUSED','reason':str(e),'claims':stage.CLAIMS}));raise SystemExit(2)
