"""T167 guarded FIXTURE_ONLY preparation. Inspect/pin before a named fresh pass."""
import argparse,ast,builtins,copy,errno,hashlib,importlib.util,io,json,math,os,re,selectors,shlex,shutil,signal,socket,stat,struct,subprocess,sys,time,types
from pathlib import Path
from unittest.mock import patch

OWN=Path(__file__).absolute().parent
PROJECT=OWN.parents[2]
OUTPUT_CAP=8388608
STORAGE_CAP=134217728
PASS_SECONDS=300
stage=build=verify=NATIVE_OPS=NATIVE_VIEW=None

class Guards:
 """Install before project imports. Real host effects stay denied throughout tests."""
 def __init__(self,roots,started=None):self.roots=tuple(map(Path,roots));self.patches=[];self.denials=[];self.fds={};self.fd_paths={};self.open_context=[];self.namespace_epoch=0;self.write_parent_cache={};self.observed=0;self.end=(time.monotonic() if started is None else started)+PASS_SECONDS
 def check(self):
  if time.monotonic()>=self.end:raise AssertionError('FIXTURE pass absolute300s deadline')
 def charge(self,data):
  self.observed+=len(data)
  if self.observed>OUTPUT_CAP:raise AssertionError('FIXTURE aggregate output bound before retention')
 def denied(self,*a,**k):self.denials.append('HOST_BOUNDARY_DENIED');raise AssertionError('REAL PROCESS/SIGNAL/WAIT/NETWORK/TOOL/COPY FORBIDDEN')
 def blocked(self,reason):self.denials.append(reason[:128]);raise AssertionError(reason)
 def allowed(self,path,write=False):
  if isinstance(path,int):
   if write:
    s=os.fstat(path)
    if self.fds.get(path)!=(s.st_dev,s.st_ino):self.blocked('unowned/reused write fd')
   return
  absolute=os.path.abspath(os.fspath(path))
  fixture=any(absolute==str(r) or absolute.startswith(str(r)+'/') for r in self.roots)
  # Read-only membership is lexical in both implementations. Avoid constructing
  # every ancestor Path for each audited metadata read; write checks stay below.
  if not write and fixture:return
  p=Path(absolute)
  if write:self.check()
  if write and not fixture:self.blocked('write outside named fixture roots: '+str(p))
  if write:
   key=str(p.parent);cached=self.write_parent_cache.get(key)
   if cached is None or cached[0]!=self.namespace_epoch:cached=(self.namespace_epoch,Path(os.path.realpath(p.parent)));self.write_parent_cache[key]=cached
   if not any(cached[1]==r or r in cached[1].parents for r in self.roots):self.blocked('write ancestor escapes fixture roots: '+str(p))
  if not write and not fixture:
   if p==PROJECT or PROJECT in p.parents:
    if p!=OWN and OWN not in p.parents and p not in OWN.parents:self.blocked('real project source/old module read forbidden: '+str(p))
   if str(p).startswith(('/Library/Developer/CommandLineTools','/private/tmp/outbreak-web-sdk','/usr/bin/')):self.blocked('REAL TOOL/SDK/FRAMEWORK inspection forbidden')
 def install(self):
  self.active=True
  def audit(event,args):
   if not self.active:return
   if event=='open':
    path,mode,flags=args
    if not isinstance(path,int) and not os.path.isabs(path) and self.open_context:path=self.open_context[-1]
    self.allowed(path,bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)))
    if not isinstance(path,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND) and os.path.islink(path):
     target=Path(os.path.realpath(path))
     if not any(target==r or r in target.parents for r in self.roots):self.blocked('write follows escaped fixture leaf')
    if not isinstance(path,int) and not flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):
     p=Path(os.path.abspath(os.fspath(path)))
     if not any(p==r or r in p.parents for r in self.roots) and not (p==OWN or OWN in p.parents) and not str(p).startswith('/Library/Frameworks/Python.framework/Versions/3.11/lib/'):self.blocked('unmapped nonfixture file read: '+str(p))
   elif event=='exec':
    name=args[0].co_filename
    if os.path.isabs(name):
     p=Path(name)
     if (p==PROJECT or PROJECT in p.parents) and not (p.parent==OWN and p.name in ('stage.py','build.py','verify.py','test_preparation.py')):raise AssertionError('old/extra project code execution denied')
   elif event in ('subprocess.Popen','os.system','os.fork','os.forkpty','os.posix_spawn','os.exec','os.kill','os.killpg','socket.connect','socket.bind'):self.denied()
   elif event.startswith('ctypes.'):self.denied()
  sys.addaudithook(audit)
  def wrap_open(original):
   def opened(path,mode='r',*args,**kwargs):
    writing=isinstance(mode,str) and any(c in mode for c in 'wax+');self.allowed(path,writing);f=original(path,mode,*args,**kwargs)
    if writing:
     s=os.fstat(f.fileno());self.fds[f.fileno()]=(s.st_dev,s.st_ino)
    return f
   return opened
  def os_open(original):
   def opened(path,flags,*args,**kwargs):
    writing=bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND));actual=path
    if kwargs.get('dir_fd') is not None:
     # Only fixture reservation uses relative dirfds; establish confinement by retained fd ancestry.
     self.allowed(kwargs['dir_fd'],True)
     if Path(path).is_absolute() or '..' in Path(path).parts:raise AssertionError('relative fd path')
     actual=self.fd_paths[kwargs['dir_fd']]/path
    else:self.allowed(path,writing)
    self.open_context.append(actual)
    try:fd=original(path,flags,*args,**kwargs)
    finally:self.open_context.pop()
    if kwargs.get('dir_fd') is not None or any(Path(os.path.abspath(os.fspath(path)))==r or r in Path(os.path.abspath(os.fspath(path))).parents for r in self.roots):
     s=os.fstat(fd);self.fds[fd]=(s.st_dev,s.st_ino);self.fd_paths[fd]=Path(os.path.abspath(os.fspath(actual)))
    return fd
   return opened
  self.patches.extend([patch.object(builtins,'open',wrap_open(builtins.open)),patch.object(io,'open',wrap_open(io.open)),patch.object(os,'open',os_open(os.open))])
  original_import=builtins.__import__
  def imported(name,*args,**kwargs):
   if name.split('.')[0] in ('ctypes','_ctypes'):self.denied()
   return original_import(name,*args,**kwargs)
  self.patches.append(patch.object(builtins,'__import__',imported))
  for owner,names in [(subprocess,['Popen','run','call','check_call','check_output']),(os,['system','popen','fork','forkpty','posix_spawn','posix_spawnp','kill','killpg','wait','waitpid','waitid','getpgid','setpgid','setsid','getsid']+[n for n in dir(os) if n.startswith(('exec','spawn'))]),(signal,['signal','setitimer','alarm','pthread_kill','raise_signal']),(socket,['socket','create_connection','getaddrinfo']),(shutil,['copytree','copy','copy2','copyfile'])]:
   for name in names:
    if hasattr(owner,name):self.patches.append(patch.object(owner,name,self.denied))
  for name in ['mkdir','unlink','remove','rmdir','chmod','lchmod','chown','utime','symlink','link','rename','replace']:
   if not hasattr(os,name):continue
   original=getattr(os,name)
   def mutate(*args,_original=original,_name=name,**kwargs):
    self.check()
    positions=[1] if _name=='symlink' else [0,1] if _name in ('link','rename','replace') else [0]
    for i in positions:
     if kwargs.get('dir_fd') is not None or kwargs.get('src_dir_fd') is not None or kwargs.get('dst_dir_fd') is not None:
      for k in ('dir_fd','src_dir_fd','dst_dir_fd'):
       if kwargs.get(k) is not None:self.allowed(kwargs[k],True)
      if Path(args[i]).is_absolute() or '..' in Path(args[i]).parts:raise AssertionError('unsafe dirfd mutation')
     else:self.allowed(args[i],True)
    result=_original(*args,**kwargs)
    if _name in ('mkdir','unlink','remove','rmdir','symlink','link','rename','replace'):self.namespace_epoch+=1
    return result
   self.patches.append(patch.object(os,name,mutate))
  original_fchmod=os.fchmod
  def fchmod(fd,mode):self.allowed(fd,True);return original_fchmod(fd,mode)
  self.patches.append(patch.object(os,'fchmod',fchmod))
  for name in ('stat','lstat','scandir'):
   original=getattr(os,name)
   def read(path,*args,_original=original,**kwargs):
    if kwargs.get('dir_fd') is None:self.allowed(path)
    return _original(path,*args,**kwargs)
   self.patches.append(patch.object(os,name,read))
  for item in self.patches:item.start()
 def restore(self):
  self.active=False
  for item in reversed(self.patches):item.stop()

def macho(kind,rpaths=()):
 blocks=[]
 for path in rpaths:
  data=path.encode()+b'\0';size=(12+len(data)+7)//8*8;blocks.append(struct.pack('<III',0x8000001c,size,12)+data+bytes(size-12-len(data)))
 if kind!=1:blocks.append(struct.pack('<IIII',0x1d,16,32+sum(map(len,blocks))+16,16))
 return struct.pack('<8I',0xfeedfacf,0x100000c,0,kind,len(blocks),sum(map(len,blocks)),0,0)+b''.join(blocks)+(b'FIXTURE_ONLY_SIG' if kind!=1 else b'FIXTURE_ONLY_OBJECT')

def fat(data):
 other=macho(6);start=4096;second=8192
 header=struct.pack('>II',0xcafebabe,2)+struct.pack('>5I',0x1000007,3,start,len(other),12)+struct.pack('>5I',0x100000c,0,second,len(data),12)
 return header+bytes(start-len(header))+other+bytes(second-start-len(other))+data

class Fixture:
 def __init__(self,root,guards):
  self.root=str(root);self.guards=guards;self.ident='FIXTURE_ONLY';self.pin=root/'notes/decisions/FIXTURE_ONLY.json';self.external={};self.views=[];self.action_fault=None;self.fx_fault=None;self.late=None;self.tool_calls=[]
  self.put('.git/HEAD',b'1'*40+b'\n');self.put('notes/decisions/FIXTURE_ONLY.md');self.put('web/runtime/history/unconsumed.txt')
  self.put('notes/FIXTURE_ONLY_UNCONSUMED.md')
  self.put('source/src/Makefile',('SERVER_OBJS= \\\n'+''.join('\t'+Path(n).stem+'-standalone.o'+(' \\\n' if i<7 else '\n') for i,n in enumerate(stage.CPP))+'MASTER_OBJS=x\n').encode())
  self.put('source/enet/Makefile.am',('libenet_la_SOURCES = '+' '.join(Path(n).name for n in stage.C)+' win32.c\n').encode())
  for name in stage.CPP+stage.C+list(stage.SOURCE_HASHES)+['source/src/sound.h']+['web/server/blackwood_candidate/'+n for n in stage.SCRIPT_NAMES]+list(stage.SOURCE_REFERENCES.values()):self.put(name)
  self.source_pins={n:stage.sha((root/n).read_bytes()) for n in stage.SOURCE_HASHES};self.reference_pins={k:stage.sha((root/n).read_bytes()) for k,n in stage.SOURCE_REFERENCES.items()}
  f=Path(stage.FRAMEWORK)
  for name in ['COPYING.txt','Versions/A/Headers/SDL.h','Versions/A/Resources/Info.plist','Versions/A/Frameworks/hidapi.framework/Versions/A/Resources/Info.plist']:self.put(str(f/name))
  self.put(str(f/'Versions/A/SDL2'),macho(6),0o755);self.put(str(f/'Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi'),macho(6),0o755)
  for name,(raw,_) in stage.FRAMEWORK_LINKS.items():
   p=root/f/name;p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to(raw);os.lchmod(p,0o755)
  self.put('web/server/history/opaque-parent/keep')
  (root/'web/server/history/opaque-parent/opaque').symlink_to('/FIXTURE_ONLY/nonexistent/outside')
  for path in [*stage.TOOLS.values(),stage.CLT+'/usr/bin/clang',stage.CLT+'/usr/bin/ld',stage.CLT+'/usr/lib/clang/17/include/stddef.h',stage.CLT+'/usr/lib/clang/17/lib/darwin/libclang_rt.osx.a',stage.PYTHON+'/bin/python3.11']:self.ext(path,b'FIXTURE_ONLY_TOOL',0o755)
  for path in ['SDKSettings.json','usr/include/zlib.h','usr/include/pthread/pthread.h','usr/include/pthread/sched.h','usr/lib/libz.1.tbd','usr/lib/libSystem.B.tbd','usr/lib/libc++.1.tbd']:self.ext(stage.SDK+'/'+path,b'{"Version":"15.5"}' if path=='SDKSettings.json' else b'FIXTURE_ONLY_SDK')
  for name in stage.ADAPTER_HEADER_PINS:self.ext(stage.SDK+'/usr/include/'+name,b'FIXTURE_ONLY_D235_HEADER')
  for name in stage.ADAPTER_STDLIB_ROLES:self.ext(name,b'FIXTURE_ONLY_LAZY_CTYPES')
  self.sdk_root=root/'EXTERNAL/SDK'
  for name,raw,mode,_ in stage.SDK_HEADER_ALIASES:
   p=self.sdk_root/name[len(stage.SDK)+1:];p.symlink_to(raw);os.lchmod(p,mode);self.external[name]=p
  for alias,(_,edges) in stage.SDK_LINK_ALIASES.items():
   raw=next(raw for edge,raw in edges if edge==alias);p=self.sdk_root/alias[len(stage.SDK)+1:];p.symlink_to(raw);os.lchmod(p,0o755);self.external[alias]=p
  # Exercise legitimate multi-hardlink installed launchers at their exact virtual roles.
  anchor=self.external[stage.TOOLS['cc']]
  for role in ('cxx','otool'):
   p=self.external[stage.TOOLS[role]];p.unlink();os.link(anchor,p)
  self.tool_pins={k:stage.sha(self.external[n].read_bytes()) for k,n in stage.TOOLS.items()}
  self.make_assets();self.view=self.new_view()
  package=stage.CPP+stage.C+list(stage.SOURCE_HASHES)+['source/src/sound.h','source/src/Makefile','source/enet/Makefile.am','notes/decisions/FIXTURE_ONLY.md']+list(stage.SOURCE_REFERENCES.values())+['web/server/blackwood_candidate/'+n for n in stage.SCRIPT_NAMES]
  package+=sorted(stage.FRAMEWORK+'/'+n for n,v in self.view.framework().items() if v['kind']=='file')
  package+=sorted(str(p.relative_to(root)) for p in (root/stage.ASSET_ROOT).rglob('*') if p.is_file())
  entries=[{'path':n,'bytes':(root/n).stat().st_size,'sha256':stage.sha((root/n).read_bytes()),'mode':(root/n).stat().st_mode&0o7777} for n in sorted(set(package))]
  self.put(stage.manifest_path(self.ident),stage.canonical_json({'schema_version':1,'kind':'SOURCE_INPUT_MANIFEST','source_revision':'1'*40,'entries':entries}).encode())
  inputs={self.root+'/'+x['path']:x['sha256'] for x in entries};inputs[self.root+'/'+stage.manifest_path(self.ident)]=self.view.hash(self.root+'/'+stage.manifest_path(self.ident))
  inputs.update({n:self.view.hash(n) for n in self.external if self.view.ordinary(n) or n in stage.TOOLS.values()})
  sdk={n[len(stage.SDK)+1:]:h for n,h in inputs.items() if n.startswith(stage.SDK+'/')}
  accepted={'ticket':'T163',**{k:{'path':n,'sha256':self.reference_pins[k]} for k,n in stage.SOURCE_REFERENCES.items()},'files':[{'path':n,'bytes':(root/n).stat().st_size,'sha256':self.source_pins[n],'mode':0o644} for n in sorted(stage.SOURCE_HASHES)]}
  self.auth={'schema_version':1,'kind':'BLACKWOOD_NATIVE_BUILD_AUTHORIZATION','authority':'MAIN','status':'ACCEPTED','execution_release':'EXPLICIT_BLACKWOOD_NATIVE_BUILD_EXECUTION','recipe':stage.RECIPE,'ticket':'FIXTURE_ONLY_NOT_REAL_AUTHORITY','candidate_id':self.ident,'decision':'notes/decisions/FIXTURE_ONLY.md','source_revision':'1'*40,'source_manifest':{'path':stage.manifest_path(self.ident),'sha256':self.view.hash(self.root+'/'+stage.manifest_path(self.ident))},'source_acceptance':accepted,'bindings':{'repository':self.root,'system_sdk':stage.SDK,'source_framework':self.root+'/'+stage.FRAMEWORK},'observation':{'inputs':inputs,'preservation':self.view.preservation(),'source_framework':self.view.framework(),'units':{'cpp':list(stage.CPP),'c':list(stage.C)},'tools':{k:{'path':n,'sha256':self.tool_pins[k]} for k,n in stage.TOOLS.items()},'system_sdk':{'root':stage.SDK,'files':sdk},'flags':{m:stage.flags(self.root,self.ident,m) for m in ('release','debug')},'errors':[],'map_seed':stage.map_declaration(self.view)}}
  self.write()
 def put(self,name,data=b'FIXTURE_ONLY\n',mode=0o644):
  p=Path(self.root)/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);p.chmod(mode);return p
 def ext(self,name,data,mode=0o644):
  p=Path(self.root)/'EXTERNAL/SDK'/name[len(stage.SDK)+1:] if name.startswith(stage.SDK+'/') else Path(self.root)/'EXTERNAL'/hashlib.sha256(name.encode()).hexdigest();p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);p.chmod(mode);self.external[name]=p
 def make_assets(self):
  cfg=b'// FIXTURE_ONLY\nmapmodelreset\nmapsoundreset\ntexturereset\ntexture 0 "outbreak/ceiling.png"\ntexture 0 "outbreak/ground.png"\ntexture 0 "outbreak/wall.png"\nfog 256\nfogcolour 0x18232B\n'
  self.seed_specs=[];names={}
  for source,target,size,_ in stage.SEED_ROWS:
   data=cfg+b'//'+b'X'*(size-len(cfg)-3)+b'\n' if source.endswith('.cfg') else (b'FIXTURE_ONLY_DATA\n'+b'X'*size)[:size]
   names[source]=data;self.seed_specs.append((source,target,size,stage.sha(data)))
  for n in ['packages/textures/outbreak/ceiling.png','packages/textures/outbreak/ground.png','packages/textures/outbreak/wall.png']:names[n]=b'FIXTURE_ONLY_TEXTURE'
  for i in range(84-len(names)):names[f'FIXTURE_ONLY/m{i:02d}.txt']=b'FIXTURE_ONLY_ASSET'
  rows=[]
  for n,data in sorted(names.items()):
   self.put(stage.ASSET_ROOT+'/pack-root/'+n,data);h=stage.sha(data);rows.append({'path':n,'bytes':len(data),'sha256':h,'notice':'notices/blackwood-candidate/LICENSE.txt','source_manifest':'web/assets/FIXTURE_ONLY/manifest.json','source_path':n,'source_sha256':h})
  manifest=self.put(stage.ASSET_ROOT+'/manifest.json',stage.canonical_json({'fixture_only':True,'entries':rows}).encode());provenance=self.put(stage.ASSET_ROOT+'/PROVENANCE.json',b'{"fixture_only":true}\n');self.asset_pins=(stage.sha(manifest.read_bytes()),stage.sha(provenance.read_bytes()))
 def write(self):self.pin.write_text(stage.canonical_json(self.auth));self.digest=stage.sha(self.pin.read_bytes())
 def new_view(self):
  v=FixtureView(self);self.views.append(v);return v
 def output(self):return Path(stage.attempt(self.root,self.ident))
 def gate(self):return stage.authorize(self.pin.read_bytes(),self.digest,self.ident,self.view)
 def pipeline(self):return build.execute(self.root,self.ident,self.pin,self.digest)
 def check(self,receipt=None):return verify.verify(self.root,self.ident,self.pin,self.digest,receipt)

class FixtureView:
 """Methods are completed from the actual View only after guarded own imports."""
 def __init__(self,f):self.f=f;self.root=f.root;self.fixture_only=True;self.consumed=set();self.armed={};self.ancestor_cache={}
 def mapped(self,p):
  if p.startswith(stage.SDK+'/'):return self.f.sdk_root/p[len(stage.SDK)+1:]
  if p.startswith((stage.CLT+'/',stage.PYTHON+'/')) or p in stage.TOOLS.values():return self.f.external.get(p,Path(self.root)/'EXTERNAL'/hashlib.sha256(p.encode()).hexdigest())
  return Path(p)
 def exists(self,p):q=self.mapped(p);return q.exists() or q.is_symlink()
 def file_stat(self,p):return self.mapped(p).lstat()
 def ordinary(self,p):
  if stage.fixture_forest(self.root,p) is not None:return False
  try:s=self.file_stat(p);return stat.S_ISREG(s.st_mode) and s.st_nlink==1 and self.ordinary_ancestors(p)
  except OSError:return False
 def canonical(self,p):
  if p.startswith(stage.SDK+'/'):
   physical=self.mapped(p).resolve(strict=True)
   return stage.SDK+'/'+str(physical.relative_to(self.f.sdk_root)) if physical.is_relative_to(self.f.sdk_root) else str(physical)
  return p if p in self.f.external else str(Path(p).resolve(strict=True))
 def ordinary_ancestors(self,p):
  try:
   epoch=self.f.guards.namespace_epoch
   for q in self.mapped(p).parents:
    key=str(q);cached=self.ancestor_cache.get(key)
    if cached is None or cached[0]!=epoch:cached=(epoch,stat.S_ISDIR(q.lstat().st_mode));self.ancestor_cache[key]=cached
    if not cached[1]:return False
   return True
  except OSError:return False
 def link_identity(self,p):
  s=self.mapped(p).lstat();return {'target':os.readlink(self.mapped(p)),'mode':s.st_mode&0o7777} if stat.S_ISLNK(s.st_mode) else None
 def hash(self,p):return stage.sha(self.mapped(p).read_bytes())
 def size(self,p):return self.mapped(p).stat().st_size
 def mode(self,p):return self.mapped(p).stat().st_mode&0o7777
 def text(self,p):return self.mapped(p).read_text()
 def json(self,p):return stage.loads(self.mapped(p).read_bytes(),stage.MAX_RECORD)
 def authoring_files(self):p=stage.PYTHON+'/bin/python3.11';return {p:self.hash(p)}
 def preservation(self):return stage.preservation_record(self.root,getattr(self,'active',None),browser_sdk=None,omit_container=getattr(self,'omit_container',False),native_sdk=self.f.sdk_root)
 def source_hashes(self):return self.f.source_pins
 def source_references(self):return self.f.reference_pins
 def seed_rows(self):return self.f.seed_specs
 def asset_hashes(self):return self.f.asset_pins
 def tool_hashes(self):return self.f.tool_pins
 def abi_headers(self):return {n:self.hash(stage.SDK+'/usr/include/'+n) for n in stage.ADAPTER_HEADER_PINS}

class Pipe:
 def __init__(self,tag,data):self.tag=tag;self.data=data;self.read=False;self.closed=False
class Selector:
 def __init__(self):self.members={};self.closed=False

class FakeDurable:
 def __init__(self,fx,fault):self.fx=fx;self.fault=fault;self.events=[];self.file=1000001;self.directory=1000002
 def event(self,name):
  self.events.append({'action':name,'at':self.fx.at})
  if self.fault==name+'_late':self.fx.at=121
  if self.fault==name+'_error':raise OSError('FIXTURE_ONLY '+name+' ambiguous error')
 def open_file(self,path):self.event('open');return self.file
 def chmod(self,fd):assert fd==self.file;self.event('chmod')
 def write(self,fd,data):assert fd==self.file;self.event('write');return len(data)
 def flush(self,fd):assert fd==self.file;self.event('flush')
 def fsync(self,fd):self.event('fsync' if fd==self.file else 'directory_fsync')
 def close(self,fd):self.event('close' if fd==self.file else 'directory_close')
 def open_directory(self,path):self.event('directory_open');return self.directory

class FakeOps:
 """Fake effects only; actual Runner owns all sequencing, bounds and receipts."""
 def __init__(self,f):self.f=f;self.at=0.;self.calls=[];self.child=None;self.closed_fail=set();self.last=None
 def clock(self):self.f.guards.check();return self.at
 def fault(self,name):
  self.calls.append(name)
  if self.f.fx_fault==name:raise RuntimeError('FIXTURE_ONLY '+name)
 def process_support(self):self.fault('process_support')
 def retain(self,child):self.fault('retain');assert child is self.child
 def native_last(self,child):return self.last if child is self.child else None
 def arm(self,state,callback,seconds):self.fault('arm');self.callback=callback;state['fake']=True
 def restore(self,state,failed,check):
  self.calls.append('restore')
  if not state:return True
  try:check()
  except BaseException as e:failed('fake_restore_SKIPPED_EXPIRED',e);return False
  if self.f.fx_fault=='restore':failed('fake_restore',RuntimeError('FIXTURE_ONLY restore'));return False
  return True
 def spawn(self,argv,root,env):
  self.fault('spawn');out,err=self.emit(argv);self.f.guards.charge(out+err);self.last=None;self.child=types.SimpleNamespace(pid=424242,stdout=Pipe(0,out),stderr=Pipe(1,err))
  if self.f.fx_fault=='guard_spawn':self.callback()
  return self.child
 def selector(self):
  self.fault('selector')
  if self.f.fx_fault=='guard_setup':self.callback()
  return Selector()
 def nonblock(self,p):self.fault('nonblock_'+str(p.tag))
 def register(self,s,p,tag):self.fault('register_'+str(tag));s.members[tag]=p
 def select(self,s,timeout):
  self.fault('select');assert 0<timeout<=.05;self.at+=.001
  if self.f.fx_fault in ('kill_esrch','kill_error','wait_timeout','wait_error','combined'):raise RuntimeError('FIXTURE_ONLY primary drain')
  if self.f.fx_fault=='drain_cross':self.at=111
  return [(types.SimpleNamespace(data=k,fileobj=p),1) for k,p in list(s.members.items())]
 def unregister(self,s,p):s.members.pop(p.tag)
 def read(self,p):self.fault('read_'+str(p.tag));data=p.data if not p.read else b'';p.read=True;return data
 def observe_exit(self,c,check):
  self.fault('observe_exit');check();assert c is self.child;data=struct.pack('<iiiiIi',20,0,1,c.pid,501,0)+bytes(80);self.last={'pid':c.pid,'result':0,'errno':0,'record_bytes':104,'record_hex':data.hex()};return {'pid':c.pid,'signo':20,'code':1,'status':0,'errno':0}
 def kill(self,c,check):
  self.fault('kill');check();assert c is self.child
  if self.f.fx_fault=='anchored_eperm':raise PermissionError(errno.EPERM,'FIXTURE_ONLY anchored signal denied')
  if self.f.fx_fault=='kill_esrch':raise ProcessLookupError(errno.ESRCH,'FIXTURE_ONLY ESRCH')
  if self.f.fx_fault in ('kill_error','combined'):raise PermissionError('FIXTURE_ONLY kill denied')
 def wait(self,c,timeout):
  self.fault('wait');assert c is self.child and 0<timeout<=2 and timeout<=120-self.at
  if self.f.fx_fault in ('wait_timeout','combined'):raise subprocess.TimeoutExpired('FIXTURE_ONLY',timeout)
  if self.f.fx_fault=='wait_error':raise RuntimeError('FIXTURE_ONLY wait error')
  if self.f.fx_fault=='wait_cross':self.at=121
  return 0
 def group_empty(self,c):
  self.fault('group_empty');assert c is self.child
  if self.f.fx_fault=='io_expired_before_persist':self.at=121
  return self.f.fx_fault!='group_live'
 def close(self,value):
  name='selector_close' if isinstance(value,Selector) else 'close_'+str(value.tag);self.calls.append(name)
  if (self.f.fx_fault==name or self.f.fx_fault=='combined' and name in ('selector_close','close_0')) and name not in self.closed_fail:self.closed_fail.add(name);raise RuntimeError('FIXTURE_ONLY '+name)
  value.closed=True
 def persist(self,base,name,data,check):
  self.fault('persist_'+('receipt' if name.endswith('.json') else 'stdout' if name.endswith('.stdout') else 'stderr'))
  selected=self.f.fx_fault or ''
  if selected.startswith('io_') and (name.endswith('.stdout') and selected!='io_receipt_write_late' or name.endswith('.json') and selected=='io_receipt_write_late'):
   fault='write_late' if selected=='io_receipt_write_late' else selected[3:];fs=FakeDurable(self,fault);self.f.io_events=fs.events;stage.durable_new(Path(base)/name,data,check=check,fs=fs)
  else:stage.durable_new(Path(base)/name,data,check=check)
 def emit(self,argv):
  f=self.f;base=f.output();f.tool_calls.append(list(argv));out='';err='';tool=argv[0]
  if '--version' in argv:out='Apple clang version 17.0.0 FIXTURE_ONLY\nTarget: arm64-apple-darwin25\nInstalledDir: '+stage.CLT+'/usr/bin\n'
  elif '--force' in argv:
   p=Path(argv[-1])/('Versions/A/hidapi' if argv[-1].endswith('hidapi.framework') else 'Versions/A/SDL2');data=p.read_bytes();p.write_bytes(data[:-1]+b'X')
   if f.action_fault=='sign_header':(base/'deps-signed/SDL2.framework/Versions/A/Headers/SDL.h').write_bytes(b'FIXTURE_ONLY_CHANGED')
  elif '-M' in argv or '-MD' in argv:
   source=argv[-1] if '-M' in argv else argv[argv.index('-c')+1];obj=argv[argv.index('-MT')+1] if '-M' in argv else argv[argv.index('-o')+1];dep=argv[argv.index('-MF')+1]
   names=[source,f.root+'/source/src/sound.h',str(base/'deps-signed/SDL2.framework/Headers/SDL.h'),stage.SDK_HEADER_ALIASES[0][0],stage.SDK_HEADER_ALIASES[1][0],stage.SDK+'/usr/include/zlib.h',stage.CLT+'/usr/lib/clang/17/include/stddef.h']
   if f.action_fault=='undeclared_dep':names.append(f.root+'/web/runtime/history/unconsumed.txt')
   if f.action_fault=='dep_mismatch' and '-MD' in argv:names.pop()
   if f.action_fault=='missing_source':names.remove(source)
   Path(dep).write_text(obj+': '+' '.join(shlex.quote(n) for n in names)+'\n')
   if '-MD' in argv:Path(obj).write_bytes(macho(1))
  elif '-Wl,-t' in argv:
   binary=Path(argv[-1]);paths=[str(base/'deps-signed'),str(base/'deps-signed/SDL2.framework/Versions/A/Frameworks')]
   if f.action_fault=='rpath':paths[0]='/FIXTURE_ONLY/old'
   binary.write_bytes(macho(2,paths));binary.chmod(0o755);objects=[x for x in argv if x.endswith('.o')]
   if f.action_fault=='link_missing_object':objects.pop()
   out='\n'.join(objects+[str(base/'deps-signed/SDL2.framework/Versions/A/SDL2'),stage.SDK+'/usr/lib/libz.tbd',stage.SDK+'/usr/lib/libpthread.tbd',stage.SDK+'/usr/lib/libc++.tbd',stage.SDK+'/usr/lib/libSystem.tbd',stage.CLT+'/usr/lib/clang/17/lib/darwin/libclang_rt.osx.a(FIXTURE_ONLY.o)'])+'\n'
  elif tool==stage.TOOLS['file']:out='Mach-O 64-bit '+('object' if argv[-1].endswith('.o') else 'executable' if argv[-1].endswith('/ac_server') else 'dynamically linked shared library')+' arm64 FIXTURE_ONLY\n'
  elif tool==stage.TOOLS['otool']:
   p=argv[-1];out=p+':\n'
   if argv[1]=='-L':
    names=['@rpath/SDL2.framework/Versions/A/SDL2','/usr/lib/libSystem.B.dylib']
    if f.action_fault=='dylib':names.append('/FIXTURE_ONLY/foreign.dylib')
    lines=''.join('\t'+n+' (compatibility version 1.0.0, current version 1.0.0)\n' for n in names)
    out=p+' (architecture x86_64):\n'+lines+p+' (architecture arm64):\n'+lines if not p.endswith('/ac_server') else p+':\n'+lines
   else:
    paths=[str(base/'deps-signed'),str(base/'deps-signed/SDL2.framework/Versions/A/Frameworks')] if p.endswith('/ac_server') else ['@loader_path/Frameworks']
    if f.action_fault=='rpath' and p.endswith('/ac_server'):paths[0]='/FIXTURE_ONLY/old'
    out+=''.join('Load command 0\n cmd LC_RPATH\n cmdsize 32\n path '+v+' (offset 12)\n' for v in paths)
  elif '--display' in argv:err=('Signature=other' if f.action_fault=='signature' else 'Signature=adhoc')+'\nFIXTURE_ONLY\n'
  if f.late:f.late(argv)
  return out.encode(),err.encode()

def refused(fn):
 try:fn()
 except (stage.Refused,OSError):return
 raise AssertionError('expected a discriminating refusal')

def fixture_copy(src,dest):
 """Physical fake-data boundary; never call real SDK/framework copy helpers."""
 src=Path(src);dest=Path(dest);dest.mkdir()
 for parent,dirs,files in os.walk(src,followlinks=False):
  target=dest/Path(parent).relative_to(src)
  for name in dirs+files:
   p=Path(parent)/name;q=target/name
   if p.is_symlink():q.symlink_to(os.readlink(p));os.lchmod(q,p.lstat().st_mode&0o7777)
   elif p.is_dir():q.mkdir();q.chmod(p.stat().st_mode&0o7777)
   else:q.write_bytes(p.read_bytes());q.chmod(p.stat().st_mode&0o7777)

def reseal(f):
 base=f.output();p=base/'freeze.json';doc=stage.loads(p.read_bytes(),stage.MAX_RECORD);items=stage.inventory(base,False)
 for n in ('freeze.json','failure.json','verification/receipt.json'):items.pop(n,None)
 doc['files']=items;p.write_text(stage.canonical_json(doc))

def opaque_test_stat(info):
 fields={n:getattr(info,n) for n in ('st_mode','st_dev','st_ino','st_size','st_uid','st_gid','st_nlink','st_mtime_ns','st_ctime_ns')}
 fields.update(st_mode=stat.S_IFREG,st_dev=16777232,st_uid=501,st_gid=20)
 return types.SimpleNamespace(**fields)

def injected_lstat(records,original):
 def observed(path,*args,**kwargs):
  actual=original(path,*args,**kwargs) # Still require the readable fixture to exist.
  return records.get(str(path),actual)
 return observed

CONTROL_CASES=(
 ('schema_bool',lambda p:p.update(schema_version=True)),('authority',lambda p:p.update(authority='worker')),('status',lambda p:p.update(status='PREPARED')),('execution_release',lambda p:p.update(execution_release='OTHER')),('recipe',lambda p:p.update(recipe='native_standalone_v1')),('candidate_path',lambda p:p.update(candidate_id='../x')),('unknown',lambda p:p.update(extra='x')),('HEAD',lambda p:p.update(source_revision='2'*40)),('binding',lambda p:p['bindings'].update(system_sdk='/tmp/latest')),('tool_path',lambda p:p['observation']['tools']['cc'].update(path='/bin/sh')),('flags',lambda p:p['observation']['flags']['release'].append('-DFAKE')),('units',lambda p:p['observation']['units']['c'].pop()),('missing_link_input',lambda p:p['observation']['inputs'].pop(stage.CLT+'/usr/bin/ld')),('missing_runtime',lambda p:p['observation']['inputs'].pop(stage.CLT+'/usr/lib/clang/17/lib/darwin/libclang_rt.osx.a')),('missing_cpp_stub',lambda p:p['observation']['inputs'].pop(stage.SDK+'/usr/lib/libc++.1.tbd')),('source_reference',lambda p:p['source_acceptance']['decision'].update(sha256='0'*64)),('source_bool',lambda p:p['source_acceptance']['files'][0].update(bytes=True)),('source_unknown',lambda p:p['source_acceptance'].update(extra=1)),('source_files',lambda p:p['source_acceptance']['files'].pop()),('map_revision_data',lambda p:next(r for r in p['observation']['map_seed']['files'] if r['target'].endswith('.cgz')).update(bytes=561)),('map_target',lambda p:p['observation']['map_seed']['files'][0].update(target='packages/maps/ac_desert.cgz')),('map_notice',lambda p:p['observation']['map_seed']['files'][0].update(source='missing.cgz.LICENSE.txt')),('map_sha',lambda p:p['observation']['map_seed']['files'][0].update(sha256='0'*64)),('map_mode_bool',lambda p:p['observation']['map_seed']['files'][0].update(mode=True)),('rotation',lambda p:p['observation']['map_seed']['rotation'].update(sha256='0'*64)),('map_unknown',lambda p:p['observation']['map_seed'].update(extra=1)),('manifest_path',lambda p:p['source_manifest'].update(path='web/repro/source-manifest.json')),('observation_unknown',lambda p:p['observation'].update(extra=1)),('SDK_hash',lambda p:p['observation']['system_sdk']['files'].update({'usr/include/zlib.h':'0'*64})),('authoring_missing',lambda p:p['observation']['inputs'].pop(stage.PYTHON+'/bin/python3.11')))

SUPERVISOR_CASES=('normal','process_support','arm','spawn','retain','selector','nonblock_0','nonblock_1','register_0','register_1','read_0','read_1','select','observe_exit','guard_spawn','guard_setup','kill_esrch','kill_error','wait_timeout','wait_error','group_live','group_empty','selector_close','close_0','close_1','combined','restore','persist_stdout','persist_stderr','persist_receipt','drain_cross','wait_cross','zero_budget','short_budget','command_output_cap','aggregate_output_cap','io_open_late','io_write_late','io_flush_late','io_fsync_late','io_close_late','io_directory_open_late','io_directory_fsync_late','io_directory_close_late','io_close_error','io_write_error','io_receipt_write_late','io_expired_before_persist')
ABI_CASES=('no_event','exit_zero','exit255','killed','dumped','wrong_pid','wrong_signo','wrong_code','exit_range','signal_range','association_errno','short_record','bool_result','unexpected_result','success_errno','ECHILD','other_errno','EINTR_once','EINTR_exhausted','deadline_before','deadline_after','anchor_lost_before','anchor_lost_after','different_handle','changed_pid','bad_layout','wrong_endian','wrong_platform','fixed_native_call_types_and_zeroing')

def cases():
 """Fixed finite union. Each tuple is a separately named discriminating case."""
 rows=[]
 def add(name,fn):rows.append((name,fn))
 def success(f):
  f.gate();r=f.pipeline();assert r['status']=='BLACKWOOD_NATIVE_LINKED_NOT_RUN',r['errors'];assert len(r['steps'])==126 and sum(x['kind']=='compile' for x in r['steps'])==32
  assert all(x['child_reaped'] and x['group_empty'] is True and x['exit']==0 for x in r['steps'])
  assert [x['argv'] for x in r['steps']]==[x['argv'] for x in stage.command_plan(f.root,f.ident)]
  assert len(r['map_seed']['files'])==5 and not (f.output()/'failure.json').exists()
  receipt=f.output()/'verification/receipt.json';v=f.check(receipt);assert v['fixture_only'] is True and v['status']=='VERIFIED_BUILD_ONLY_NOT_RUN'
  before=receipt.stat().st_mtime_ns;assert f.check(receipt)==v and receipt.stat().st_mtime_ns==before
 add('complete126_success_and_optional_receipt',success)
 def plan_only(f):
  f.gate();p=build.plan(f.root,f.ident);assert p['kind']=='BLACKWOOD_NATIVE_BUILD_PLAN' and p['status']=='NOT_EXECUTED' and len(p['commands'])==126 and p['source_manifest'] is None and p['pending'] and not f.output().exists() and not f.tool_calls
 add('pure_fake_plan126_without_actual_attempt',plan_only)
 for name,change in CONTROL_CASES:
  def control(f,change=change):f.gate();change(f.auth);f.write();refused(f.gate);assert not f.output().exists() and not f.tool_calls
  add('control_'+name,control)
 def syntax(f):
  for text in ('{"a":1,"a":2}','{"a":NaN}','{"a":1e999}') :refused(lambda text=text:stage.loads(text))
  refused(lambda:stage.authorize(f.pin.read_bytes(),'0'*64,f.ident,f.view))
  refused(lambda:stage.loads(b'X'*33,32))
 add('duplicate_nonfinite_digest_size',syntax)
 def promotion(f):
  f.gate();f.view.fixture_only=False;refused(f.gate);assert not f.tool_calls
 add('fixture_cannot_promote',promotion)
 def source_multilink(f):
  f.gate();os.link(Path(f.root)/'source/src/sound.h',Path(f.root)/'EXTERNAL/source_alias');refused(f.gate)
 add('source_multilink_refusal',source_multilink)
 def header_role(f):
  f.gate();f.view.declared_inputs=f.auth['observation']['inputs'];refused(lambda:stage.dependency_paths('/FIXTURE_ONLY.o: '+stage.TOOLS['cc'],'/FIXTURE_ONLY.o',f.view,f.ident))
  refused(lambda:f.view.arm_tool('cc',f.tool_pins['cc']))
 add('armed_launcher_as_header_refused_and_rearm_retained',header_role)
 def rearm(f):
  f.gate();p=f.external[stage.TOOLS['cc']];old=p.read_bytes();p.unlink();p.write_bytes(old);p.chmod(0o755);refused(f.gate)
 add('same_bytes_tool_identity_rearm',rearm)
 for at in range(2):
  for mutation in ('raw','mode','missing','ordinary','target_hash','target_link','target_hardlink','ancestor_link','target_missing','unknown_alias'):
   def alias(f,at=at,mutation=mutation):
    f.gate();name,raw,mode,target=stage.SDK_HEADER_ALIASES[at];p=f.view.mapped(name);t=f.view.mapped(target)
    if mutation=='raw':p.unlink();p.symlink_to('./'+raw);os.lchmod(p,mode)
    elif mutation=='mode':os.lchmod(p,0o700)
    elif mutation=='missing':p.unlink()
    elif mutation=='ordinary':p.unlink();p.write_bytes(t.read_bytes())
    elif mutation=='target_hash':t.write_bytes(b'FIXTURE_ONLY_CHANGED')
    elif mutation=='target_missing':t.unlink()
    elif mutation=='target_hardlink':os.link(t,t.with_name('same_inode.h'))
    elif mutation=='target_link':other=t.with_name('same_bytes.h');t.rename(other);t.symlink_to(other.name)
    elif mutation=='ancestor_link':other=t.parent.with_name('other');t.parent.rename(other);t.parent.symlink_to('other',target_is_directory=True)
    else:
     name=stage.SDK+'/usr/include/unknown-same.h';q=f.view.mapped(name);q.symlink_to(raw);os.lchmod(q,mode)
    f.view.declared_inputs=f.auth['observation']['inputs'];refused(lambda:stage.dependency_paths('/FIXTURE_ONLY.o: '+name,'/FIXTURE_ONLY.o',f.view,f.ident))
    refused(f.gate)
    assert not f.tool_calls
   add(f'SDK_alias_{at}_{mutation}',alias)
 for name in range(7):
  def frame_link(f,name=name):
   f.gate();key=list(stage.FRAMEWORK_LINKS)[name];p=Path(f.root)/stage.FRAMEWORK/key;p.unlink();p.symlink_to('/FIXTURE_ONLY/outside');refused(f.gate);assert not f.tool_calls
  add(f'framework_link_{name}_escape',frame_link)
 def framework_hardlink(f):
  f.gate();p=Path(f.root)/stage.FRAMEWORK/'COPYING.txt';os.link(p,Path(f.root)/'EXTERNAL/license_hardlink');refused(f.gate)
 add('framework_license_multilink',framework_hardlink)
 def special(f):
  f.gate();name=f.root+'/'+stage.FRAMEWORK+'/COPYING.txt';original=f.view.file_stat;hashed=f.view.hash
  def metadata(path):return types.SimpleNamespace(st_mode=stat.S_IFIFO|0o644,st_nlink=1) if path==name else original(path)
  def read(path):
   if path==name:raise AssertionError('special framework member read before refusal')
   return hashed(path)
  with patch.object(f.view,'file_stat',metadata),patch.object(f.view,'hash',read):refused(f.gate)
  assert not f.tool_calls
 add('framework_special_metadata_before_read',special)
 def extra_framework(f):f.gate();f.put(stage.FRAMEWORK+'/UNKNOWN_MEMBER');refused(f.gate);assert not f.tool_calls
 add('framework_unknown_complete_membership',extra_framework)
 for kind in ('symlink','multilink'):
  def control_identity(f,kind=kind):
   f.gate();other=f.pin.with_name('FIXTURE_ONLY_OTHER.json')
   if kind=='symlink':f.pin.rename(other);f.pin.symlink_to(other.name)
   else:os.link(f.pin,other)
   refused(f.pipeline);assert not f.output().exists() and not f.tool_calls
  add('selected_control_'+kind,control_identity)
 def malformed(f):
  stage.macho(macho(1),1);stage.macho(macho(2),2);stage.macho(fat(macho(6)),6)
  for data,kind in [(b'bad',2),(macho(1),2),(macho(2)[:-1],2),(fat(macho(6))[:40],6)]:refused(lambda data=data,kind=kind:stage.macho(data,kind))
  p='/FIXTURE_ONLY/library';line='\t/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1.0.0)\n';good=p+' (architecture x86_64):\n'+line+p+' (architecture arm64):\n'+line
  assert len(stage.otool_dependencies(good,p))==2
  for text in [good.replace('architecture arm64','architecture unknown'),good.replace('architecture arm64','architecture x86_64'),good+'junk\n',p+':\n'+good,good.replace(p+' (architecture arm64):','/forged (architecture arm64):')]:refused(lambda text=text:stage.otool_dependencies(text,p))
 add('thin_FAT_ranges_signatures_multiarchitecture_sections',malformed)
 def occupied(f):
  f.gate();base=stage.reserve(f.root,f.ident);keep=base/'keep';keep.write_bytes(b'FIXTURE_ONLY');refused(lambda:stage.reserve(f.root,f.ident));assert keep.read_bytes()==b'FIXTURE_ONLY' and (base/'failure.json').exists()
 add('occupied_and_partial_reservation_preserved',occupied)
 for action in ('sign_header','undeclared_dep','dep_mismatch','missing_source','link_missing_object','signature','dylib','rpath'):
  def producer(f,action=action):f.action_fault=action;r=f.pipeline();assert r['status']=='FAILED' and (f.output()/'failure.json').is_file(),r
  add('producer_'+action,producer)
 for mutation in ('report_unknown','runtime_claim','reuse','fixture_promotion','step_unknown','step_bool_pid','step_unreaped','step_group_unresolved','step_unanchored_signal','step_pending_publication','step_timeout_type','step_extra','unit_command','object_corrupt','root_extra','refusal_marker','owned_hardlink','owned_symlink','live_signature','live_dylib','live_rpath','late_unconsumed_history','late_owned_graph','late_control'):
  def verifier_negative(f,mutation=mutation):
   record=f.pipeline();assert record['status']=='BLACKWOOD_NATIVE_LINKED_NOT_RUN',record['errors'];base=f.output()
   if mutation.startswith('late_'):
    def late(argv):
     if '--display' in argv and argv[-1]==str(base/'debug/ac_server'):
      if mutation=='late_unconsumed_history':(Path(f.root)/'notes/FIXTURE_ONLY_UNCONSUMED.md').write_bytes(b'FIXTURE_ONLY_LATE')
      elif mutation=='late_owned_graph':(base/'tmp/FIXTURE_ONLY_LATE').write_bytes(b'FIXTURE_ONLY_LATE')
      else:f.pin.write_bytes(f.pin.read_bytes()+b' ')
    f.late=late;refused(f.check);return
   if mutation.startswith('live_'):f.action_fault=mutation[len('live_'):];refused(f.check);return
   if mutation=='owned_hardlink':os.link(base/'logs/000.stdout',base/'tmp/log_hardlink');refused(f.check);return
   if mutation=='owned_symlink':p=base/'logs/000.stdout';q=base/'tmp/original';p.rename(q);p.symlink_to('../tmp/original');reseal(f);refused(f.check);return
   if mutation=='root_extra':(base/'UNKNOWN_ROOT_ROLE').write_bytes(b'FIXTURE_ONLY');reseal(f);refused(f.check);return
   if mutation=='refusal_marker':(base/'failure.json').write_bytes(b'FIXTURE_ONLY_REFUSAL');refused(f.check);return
   if mutation=='report_unknown':record['unknown']=True
   elif mutation=='runtime_claim':record['claims']['native_runtime']=True
   elif mutation=='reuse':record['object_reuse']=True
   elif mutation=='fixture_promotion':record['fixture_only']=False
   elif mutation=='step_unknown':record['steps'][0]['unknown']=True
   elif mutation=='step_bool_pid':record['steps'][0]['pid']=True
   elif mutation=='step_unreaped':record['steps'][0]['child_reaped']=False
   elif mutation=='step_group_unresolved':record['steps'][0]['group_empty']=None
   elif mutation=='step_unanchored_signal':record['steps'][0]['group_signal']='SIGNALED_AFTER_REAP'
   elif mutation=='step_pending_publication':record['steps'][0]['publication']='PENDING'
   elif mutation=='step_timeout_type':record['steps'][0]['timeout_s']=120.0
   elif mutation=='step_extra':record['steps'].append(copy.deepcopy(record['steps'][-1]))
   elif mutation=='unit_command':record['modes']['release']['units'][0]['compile'].append('-DFAKE')
   elif mutation=='object_corrupt':
    unit=record['modes']['release']['units'][0];Path(unit['object']).write_bytes(b'FIXTURE_ONLY_BAD_MACHO');unit['object_sha256']=stage.sha(Path(unit['object']).read_bytes())
   (base/'report.json').write_text(stage.canonical_json(record));reseal(f);refused(f.check)
  add('verifier_'+mutation,verifier_negative)
 for at in range(6):
  def staged_seed(f,at=at):
   r=f.pipeline();assert r['status']=='BLACKWOOD_NATIVE_LINKED_NOT_RUN',r['errors'];base=f.output()
   target=r['map_seed']['files'][at]['target'] if at<5 else 'packages/maps/servermaps/DEV_EXTRA.cgz'
   p=base/'runtime-seed'/target;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'FIXTURE_ONLY_DEV_561_REV2_OR_CHANGED');reseal(f);refused(f.check)
  add('independent_staged_seed_'+str(at),staged_seed)
 for action in ('create_default','create_requested','delete_default','replace_same_bytes_default','delete_requested_after_publication'):
  def late_receipt(f,action=action):
   r=f.pipeline();assert r['status']=='BLACKWOOD_NATIVE_LINKED_NOT_RUN',r['errors'];base=f.output();old=base/'verification/receipt.json'
   if action in ('delete_default','replace_same_bytes_default'):f.check(old)
   original=stage.protected_inventory;state={'calls':0,'injected':False}
   def observe(*args,**kwargs):
    value=original(*args,**kwargs);state['calls']+=1
    eligible=state['calls']>=2 and not state['injected'] and (old.exists() if action.startswith(('delete','replace')) else not old.exists())
    if eligible:
     state['injected']=True
     if action.startswith('delete'):old.unlink()
     elif action.startswith('replace'):
      swap=base/'tmp/RECEIPT_SWAP';swap.write_bytes(old.read_bytes());os.replace(swap,old)
     else:old.write_bytes(b'FIXTURE_ONLY_LATE_INVALID_RECEIPT')
    return value
   with patch.object(stage,'protected_inventory',observe):refused(lambda:f.check(old if 'requested' in action else None))
   assert state['injected'];f.case_observation={'receipt_fault':action,**state,'receipt_present_after':old.exists()}
  add('D236_receipt_'+action,late_receipt)
 for fault in ('report_write','freeze_write','remove_failure','deadline_report','deadline_freeze','corrupt_report','late_owned'):
  def terminal(f,fault=fault):
   base=Path(f.root)/'terminal';(base/'logs').mkdir(parents=True);(base/'tmp').mkdir();(base/'failure.json').write_bytes(b'FIXTURE_ONLY_REFUSAL');fx=FakeOps(f);runner=build.Runner(f.root,base,fx=fx,view=f.view)
   record={'status':'BLACKWOOD_NATIVE_LINKED_NOT_RUN','candidate_id':f.ident,'fixture_only':True,'stage_before':None,'errors':[]}
   original=stage.durable_new;unlinks=os.unlink;writes=[]
   def persist(path,data,*args,**kwargs):
    writes.append(Path(path).name)
    if fault==Path(path).stem+'_write':raise OSError('FIXTURE_ONLY required write failure')
    result=original(path,b'FIXTURE_ONLY_BAD' if fault=='corrupt_report' and Path(path).name=='report.json' else data,*args,**kwargs)
    if fault=='deadline_'+Path(path).stem:fx.at=1801
    if fault=='late_owned' and Path(path).name=='freeze.json':(base/'tmp/LATE').write_bytes(b'FIXTURE_ONLY')
    return result
   def remove(path,*a,**kw):
    if fault=='remove_failure' and Path(path).name=='failure.json':raise PermissionError('FIXTURE_ONLY marker refusal')
    return unlinks(path,*a,**kw)
   with patch.object(stage,'durable_new',persist),patch.object(os,'unlink',remove):okay=build.Terminal(f.view,base,runner).seal(record,runner.check)
   assert not okay and record['status']=='FAILED' and (base/'failure.json').exists()
   assert 'report.json' in writes
   if fault not in ('deadline_report',):assert 'freeze.json' in writes
  add('terminal_'+fault,terminal)
 for name in SUPERVISOR_CASES:
  def supervisor(f,name=name):
   f.gate();f.view.declared_inputs=f.auth['observation']['inputs'];base=Path(f.root)/'capture';(base/'logs').mkdir(parents=True);(base/'tmp').mkdir();fx=FakeOps(f);runner=build.Runner(f.root,base,fx=fx,view=f.view)
   f.fx_fault=name
   if name=='zero_budget':runner.end=0
   if name=='short_budget':runner.end=19
   if name in ('command_output_cap','aggregate_output_cap'):
    original=fx.emit;fx.emit=lambda argv:(b'FIXTURE_ONLY_OUTPUT'*8,b'')
    if name=='aggregate_output_cap':runner.total_bytes=64*1024*1024-2
   with patch.object(stage,'MAX_LOG',16 if name=='command_output_cap' else stage.MAX_LOG):
    if name=='normal':runner.run('compiler_identity',[stage.TOOLS['cc'],'--version'])
    else:refused(lambda:runner.run('compiler_identity',[stage.TOOLS['cc'],'--version']))
   row=runner.records[0];assert (row['status']=='PASS')==(name=='normal') and row['stdout_bytes']+row['stderr_bytes']<=stage.MAX_LOG
   f.case_observation={'record':row,'calls':fx.calls,'io_events':getattr(f,'io_events',[]),'strong_unreaped_handle_retained':any(h is fx.child for h in build._OWNED_CHILD_HANDLES)}
   if name in ('command_output_cap','aggregate_output_cap'):assert row['overflow'] and row['stdout_bytes']==(16 if name=='command_output_cap' else 2)
   if name in ('zero_budget','short_budget','process_support','arm','spawn'):assert not row['returned_handle']
   else:
    assert row['returned_handle'] and row['pid']==424242
    if name not in ('wait_cross','io_expired_before_persist'):assert 'selector_close' in fx.calls or name in ('retain','selector','guard_setup','guard_spawn')
    if name not in ('wait_cross','io_expired_before_persist'):assert 'close_0' in fx.calls and 'close_1' in fx.calls
    if name in ('wait_timeout','wait_error','combined'):assert not row['child_reaped'] and row['exit'] is None and row['ownership']=='RETURNED_UNRESOLVED'
    if name in ('kill_esrch','kill_error','combined'):assert 'wait' in fx.calls
    if name=='wait_cross':assert row['child_reaped'] and row['exit']==0 and row['timed_out']
    if 'group_empty' in fx.calls:assert fx.calls.index('kill')<fx.calls.index('wait')<fx.calls.index('group_empty')
    if name=='combined':assert row['primary']=='FIXTURE_ONLY primary drain' and len(row['secondary'])>=3
   if name.startswith('io_'):
    events=getattr(f,'io_events',[]);assert all(e['at']<120 for e in events),'post-cutoff filesystem effect'
    if name=='io_expired_before_persist':assert not events and not any(x.startswith('persist_') for x in fx.calls)
    elif name.endswith('_late'):
     assert row['timed_out'] and not any(x=='persist_stderr' for x in fx.calls) if name!='io_receipt_write_late' else row['timed_out']
     if name not in ('io_close_late','io_directory_close_late'):assert row['io_unresolved'] and all(h['state']=='SKIPPED_EXPIRED' and not h['close_attempted'] for h in row['io_unresolved'])
     else:assert not row['io_unresolved']
    if name=='io_close_error':assert row['io_unresolved'][0]['state']=='UNRESOLVED_CLOSE_ERROR' and sum(e['action']=='close' for e in events)==1
   if row['returned_handle'] and not row['child_reaped']:assert any(h is fx.child for h in build._OWNED_CHILD_HANDLES)
   assert len(fx.calls)<50 and fx.calls.count('spawn')<=1 and fx.calls.count('kill')<=1 and fx.calls.count('wait')<=1
  add('supervisor_'+name,supervisor)
 for case in ABI_CASES:
  def abi_case(f,case=case):
   owner=types.SimpleNamespace(pid=424242,returncode=None)
   valid=struct.pack('<iiiiIi',20,0,1,owner.pid,501,0)+bytes(80)
   class Native:
    def __init__(self):self.abi=copy.deepcopy(build.WAIT_ABI);self.calls=0
    def call(self,pid,zero):
     assert pid==424242 and zero==bytes(104);self.calls+=1
     if case=='anchor_lost_after':owner.returncode=0
     if case in ('EINTR_once','EINTR_exhausted') and (self.calls==1 or case=='EINTR_exhausted'):return -1,4,zero
     if case in ('ECHILD','other_errno'):return -1,10 if case=='ECHILD' else 22,zero
     if case in ('no_event','EINTR_once'):return 0,0,zero
     if case=='bool_result':return True,0,valid
     if case=='unexpected_result':return 2,0,valid
     if case=='success_errno':return 0,4,valid
     if case=='short_record':return 0,0,valid[:-1]
     fields=[20,0,1,424242,501,0]
     changes={'exit255':(5,255),'killed':(2,2),'dumped':(2,3),'wrong_pid':(3,7),'wrong_signo':(0,19),'wrong_code':(2,4),'exit_range':(5,256),'signal_range':(2,2),'association_errno':(1,5)}
     if case in changes:i,v=changes[case];fields[i]=v
     if case in ('killed','dumped'):fields[5]=9
     if case=='signal_range':fields[5]=32
     return 0,0,struct.pack('<iiiiIi',*fields)+bytes(80)
   native=Native()
   if case in ('bad_layout','wrong_endian','wrong_platform'):
    native.abi[{'bad_layout':'record','wrong_endian':'byteorder','wrong_platform':'platform'}[case]]={'bad_layout':96,'wrong_endian':'big','wrong_platform':'linux'}[case]
    refused(lambda:build.DarwinWaitid(native));assert not native.calls;return
   if case=='fixed_native_call_types_and_zeroing':
    class Info:
     def __init__(self):self.raw=bytearray(b'X'*104)
    class FFI:
     c_int='SIGNED32';c_uint32='UNSIGNED32'
     def POINTER(self,kind):return ('POINTER',kind)
     def byref(self,info):return info
     def memset(self,info,value,n):assert value==0 and n==104;info.raw[:]=bytes(104)
     def set_errno(self,n):self.error=n
     def get_errno(self):return self.error
     def string_at(self,info,n):assert n==104;return bytes(info.raw)
    ffi=FFI();seen=[]
    def function(kind,pid,info,flags):assert (kind,pid,flags)==(1,424242,37) and info.raw==bytes(104);seen.append(True);info.raw[:]=valid;return 0
    bound=build.bind_wait_function(ffi,types.SimpleNamespace(waitid=function),Info)
    assert bound.argtypes==['SIGNED32','UNSIGNED32',('POINTER',Info),'SIGNED32'] and bound.restype=='SIGNED32'
    assert build.native_wait_call(ffi,bound,Info,424242,bytes(104))==(0,0,valid) and seen==[True]
    refused(lambda:build.native_wait_call(ffi,bound,Info,424242,b'X'*104));return
   with patch.object(build,'load_darwin_waitid',side_effect=AssertionError('REAL_CTYPES_LOADER_FORBIDDEN')):adapter=build.DarwinWaitid(native)
   adapter.bind(owner);calls=[0]
   def check():
    calls[0]+=1
    if case=='deadline_before' or case=='deadline_after' and calls[0]>=2:raise stage.Refused('FIXTURE_ONLY original deadline')
   if case=='anchor_lost_before':owner.returncode=0
   if case=='changed_pid':owner.pid=999
   target=types.SimpleNamespace(pid=424242,returncode=None) if case=='different_handle' else owner
   if case in ('no_event','exit_zero','exit255','killed','dumped','EINTR_once'):
    event=adapter.observe(target,check)
    assert event is None if case in ('no_event','EINTR_once') else event['pid']==424242 and event['status']==(255 if case=='exit255' else 9 if case in ('killed','dumped') else 0)
    assert native.calls==(2 if case=='EINTR_once' else 1) and owner.returncode is None
   else:
    refused(lambda:adapter.observe(target,check))
    if case in ('deadline_before','anchor_lost_before','different_handle','changed_pid'):assert native.calls==0
    if case=='EINTR_exhausted':assert native.calls==16
  add('D235_'+case,abi_case)
 for variant in ('anchored_cleanup','ECHILD_no_signal_or_reap','wait_ECHILD_never_exit0','nondefault_SIGCHLD'):
  def backend(f,variant=variant):
   class Child:
    pid=424242;returncode=None
    def _try_wait(self,flags):raise AssertionError('unchecked Popen ECHILD fallback forbidden')
    def wait(self,timeout):
     pid,status=self._try_wait(os.WNOHANG);assert pid==self.pid;self.returncode=status>>8;return self.returncode
   child=Child();events=[]
   class Native:
    abi=build.WAIT_ABI
    def call(self,pid,zero):return (-1,10,zero) if variant=='ECHILD_no_signal_or_reap' else (0,0,struct.pack('<iiiiIi',20,0,1,pid,501,0)+bytes(80))
   ops=NATIVE_OPS();ops.wait_adapter=build.DarwinWaitid(Native());ops.wait_adapter.bind(child)
   def signal_owned(pid,value):assert pid==child.pid and value==signal.SIGKILL;events.append('signal')
   def wait_owned(pid,flags):
    assert pid==child.pid and flags==os.WNOHANG;events.append('wait')
    if variant=='wait_ECHILD_never_exit0':raise ChildProcessError('FIXTURE_ONLY ECHILD')
    return pid,0
   with patch.object(os,'killpg',signal_owned),patch.object(os,'waitpid',wait_owned):
    if variant=='nondefault_SIGCHLD':
     with patch.object(signal,'getsignal',return_value=signal.SIG_IGN):refused(ops.process_support)
    elif variant=='ECHILD_no_signal_or_reap':
     refused(lambda:ops.wait_adapter.observe(child,lambda:None));refused(lambda:ops.kill(child,lambda:None));refused(lambda:ops.wait(child,1));assert not events and child.returncode is None
    elif variant=='wait_ECHILD_never_exit0':ops.kill(child,lambda:None);refused(lambda:ops.wait(child,1));assert events==['signal','wait'] and child.returncode is None and ops.wait_adapter.anchor_lost
    else:ops.kill(child,lambda:None);assert ops.wait(child,1)==0 and events==['signal','wait']
   f.case_observation={'backend':variant,'events':events,'anchor_lost':ops.wait_adapter.anchor_lost,'returncode':child.returncode}
  add('D235_backend_'+variant,backend)
 # D453 retires the superseded D446/D450 live per-file schema cases.
 # Their immutable pass7/pass8 snapshots/results remain; original202 cases above stay.
 for variant in ('deterministic_no_open','injected_node_kinds','add_member','remove_member','inode','mtime','ctime','mode','uid','gid','nlink','bytes','raw_link','row_extra','row_kind','row_version','row_count_bool','row_digest','unknown_root','outside_unreadable','outside_special','consumed_promotion','root_type','missing_forest','missing_original','changed_original'):
  def tree_case(f,variant=variant):
   metadata={};tree_paths=[]
   for forest in stage.FIXTURE_FORESTS:
    for name in ('readable.txt','nested/leaf.bin','unreadable','fifo','socket','link'):
     p=f.put(forest+'/'+name,b'FIXTURE_ONLY');tree_paths.append(p)
     if name in ('unreadable','fifo','socket','link'):
      info=opaque_test_stat(p.lstat());info.st_mode={'unreadable':stat.S_IFREG,'fifo':stat.S_IFIFO|0o644,'socket':stat.S_IFSOCK|0o644,'link':stat.S_IFLNK|0o755}[name];metadata[str(p)]=info
   base=Path(f.root)/stage.FIXTURE_FORESTS[0];leaf=base/'unreadable';original_read=stage.file_sha;original_lstat=Path.lstat;original_link=os.readlink;original_list=os.listdir;reads=[];links={'target':'/FIXTURE_ONLY/NO_TRAVERSAL'};expected={}
   if variant in ('missing_forest','missing_original','changed_original'):
    for name in stage.OPAQUE_FILES:
     p=f.put(name,b'FIXTURE_ONLY');metadata[str(p)]=opaque_test_stat(p.lstat());expected[name]=stage.opaque_metadata(metadata[str(p)])
   outside=f.put('web/OUTSIDE_UNREADABLE') if variant=='outside_unreadable' else f.put('web/OUTSIDE_SPECIAL') if variant=='outside_special' else None
   if variant=='outside_special':metadata[str(outside)]=opaque_test_stat(outside.lstat());metadata[str(outside)].st_mode=stat.S_IFIFO|0o644
   def read(path,*args,**kwargs):
    if stage.fixture_forest(f.root,str(path)) is not None:raise AssertionError('fixture content opened')
    reads.append(str(path))
    if path==outside:raise PermissionError('FIXTURE_ONLY outside unreadable')
    return original_read(path,*args,**kwargs)
   def link(path,*args,**kwargs):
    if str(path) in metadata and stat.S_ISLNK(metadata[str(path)].st_mode):return links['target']
    return original_link(path,*args,**kwargs)
   def listing(path):
    if str(path) in metadata and stat.S_ISLNK(metadata[str(path)].st_mode):raise AssertionError('fixture symlink traversed')
    return original_list(path)
   with patch.object(Path,'lstat',injected_lstat(metadata,original_lstat)),patch.object(stage,'file_sha',read),patch.object(os,'readlink',link),patch.object(os,'listdir',listing):
    if outside is not None:
     refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root));return
    preserved=f.view.preservation();protected=stage.protected_inventory(f.root);rows=preserved['opaque_fixture_trees'];keys={str(Path(f.root)/n) for n in stage.FIXTURE_FORESTS}
    assert set(rows)==keys and all(protected[n]==rows[n] for n in keys)
    assert preserved==f.view.preservation() and protected==stage.protected_inventory(f.root)
    if variant in ('deterministic_no_open','injected_node_kinds'):assert all(row['entries']==8 for row in rows.values())
    elif variant=='consumed_promotion':
     for path in (base,base/'readable.txt'):
      assert not NATIVE_VIEW.ordinary(f.view,str(path)) and not f.view.consume(str(path));refused(lambda path=path:NATIVE_VIEW.hash(f.view,str(path)))
     doc={'schema_version':1,'kind':'SOURCE_INPUT_MANIFEST','source_revision':'1'*40,'entries':[{'path':stage.FIXTURE_FORESTS[0]+'/readable.txt','bytes':12,'mode':0o644,'sha256':'0'*64}]};refused(lambda:stage.source_manifest(doc,'1'*40,f.view,f.root))
     f.view.declared_inputs={str(base/'readable.txt'):'0'*64};refused(lambda:stage.dependency_paths('/FIXTURE_ONLY.o: '+str(base/'readable.txt'),'/FIXTURE_ONLY.o',f.view,f.ident))
    elif variant.startswith('row_') or variant=='unknown_root':
     changed=copy.deepcopy(preserved);row=changed['opaque_fixture_trees'][str(base)]
     if variant=='row_extra':row['unknown']=0
     elif variant=='row_kind':row['kind']='file'
     elif variant=='row_version':row['schema_version']=True
     elif variant=='row_count_bool':row['entries']=True
     elif variant=='row_digest':row['metadata_sha256']='bad'
     else:changed['opaque_fixture_trees'][str(base)+'_UNKNOWN']=changed['opaque_fixture_trees'].pop(str(base))
     refused(lambda:stage.validate_preservation(changed,f.root))
    elif variant in ('missing_forest','missing_original','changed_original'):
     with patch.object(stage,'ROOT',Path(f.root)),patch.object(stage,'OPAQUE_FILES',expected):
      f.view.preservation();stage.protected_inventory(f.root)
      if variant=='missing_forest':
       missing=copy.deepcopy(preserved);missing['opaque_fixture_trees'].pop(str(base));refused(lambda:stage.validate_preservation(missing,f.root))
       other=Path(f.root)/stage.FIXTURE_FORESTS[1]
       for member in sorted(other.rglob('*'),key=lambda p:len(p.parts),reverse=True):
        if member.is_dir():member.rmdir()
        else:member.unlink()
       other.rmdir();refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root));return
      original=Path(f.root)/next(iter(expected))
      if variant=='missing_original':original.unlink()
      else:metadata[str(original)].st_ino+=1
      refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root))
    elif variant=='root_type':
     metadata[str(base)]=opaque_test_stat(original_lstat(base));refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root))
    else:
     f.auth['observation']['preservation']=preserved;f.write();f.gate()
     if variant=='add_member':f.put(stage.FIXTURE_FORESTS[0]+'/ADDED')
     elif variant=='remove_member':(base/'readable.txt').unlink()
     elif variant=='raw_link':links['target']='/FIXTURE_ONLY/CHANGED'
     else:
      attribute={'inode':'st_ino','mtime':'st_mtime_ns','ctime':'st_ctime_ns','mode':'st_mode','uid':'st_uid','gid':'st_gid','nlink':'st_nlink','bytes':'st_size'}[variant];setattr(metadata[str(leaf)],attribute,getattr(metadata[str(leaf)],attribute)+1)
     refused(f.gate);assert stage.protected_inventory(f.root)[str(base)]!=protected[str(base)]
    f.case_observation={'variant':variant,'tree_rows':rows,'fixture_content_reads':0,'new_physical_files':'READABLE; special/unreadable/link metadata INJECTED'}
  add('D453_'+variant,tree_case)
 for variant in ('confirmed_empty','live_group','unknown_group','group_error','reap_error','reap_unknown','reap_nonzero','missing_observation','nonzero_observation','wrong_pid','unexpected_errno','other_error','deadline','log_failure','receipt_failure','strict_ledger'):
  def eperm_case(f,variant=variant):
   f.gate();f.view.declared_inputs=f.auth['observation']['inputs'];base=Path(f.root)/'capture';(base/'logs').mkdir(parents=True);(base/'tmp').mkdir();fx=FakeOps(f);f.fx_fault='anchored_eperm';runner=build.Runner(f.root,base,fx=fx,view=f.view)
   group=fx.group_empty;wait=fx.wait;observe=fx.observe_exit;close=fx.close;persist=fx.persist
   if variant in ('live_group','unknown_group','group_error','deadline'):
    def group_result(child):
     value=group(child)
     if variant=='group_error':raise OSError('FIXTURE_ONLY unresolved group')
     if variant=='deadline':fx.at=121;return value
     return False if variant=='live_group' else None
    fx.group_empty=group_result
   if variant.startswith('reap_'):
    def reap(child,timeout):
     wait(child,timeout)
     if variant=='reap_error':raise RuntimeError('FIXTURE_ONLY failed reap')
     return None if variant=='reap_unknown' else 1
    fx.wait=reap
   if variant in ('missing_observation','nonzero_observation','wrong_pid'):
    def terminal(child,check):
     if variant=='missing_observation':raise stage.Refused('FIXTURE_ONLY missing terminal observation')
     row=observe(child,check);row['status' if variant=='nonzero_observation' else 'pid']+=1;return row
    fx.observe_exit=terminal
   if variant=='unexpected_errno':
    def denied(child,check):fx.calls.append('kill');check();assert child is fx.child;raise PermissionError(errno.EACCES,'FIXTURE_ONLY unexpected denial')
    fx.kill=denied
   if variant=='other_error':
    def closing(value):
     close(value)
     if isinstance(value,Selector):raise RuntimeError('FIXTURE_ONLY unrelated cleanup error')
    fx.close=closing
   if variant in ('log_failure','receipt_failure'):
    def publication(base,name,data,check):
     if name.endswith('.stdout' if variant=='log_failure' else '.receipt.json'):raise OSError('FIXTURE_ONLY publication failure')
     return persist(base,name,data,check)
    fx.persist=publication
   okay=variant in ('confirmed_empty','strict_ledger')
   if okay:runner.run('compiler_identity',[stage.TOOLS['cc'],'--version'])
   else:refused(lambda:runner.run('compiler_identity',[stage.TOOLS['cc'],'--version']))
   row=runner.records[0];assert (row['status']=='PASS')==okay and fx.calls.count('kill')==1 and fx.calls.count('wait')==1
   assert fx.calls.index('kill')<fx.calls.index('wait')
   if okay:
    assert row['group_signal']=='EPERM_DENIED_WHILE_ANCHORED' and row['secondary']==[] and row['child_reaped'] and row['exit']==0 and row['group_empty'] is True
    stage.validate_step(row,0,'compiler_identity',[stage.TOOLS['cc'],'--version'],runner.env)
   if variant=='strict_ledger':
    for field,value in (('group_empty',None),('exit',None),('child_reaped',False),('nonreaping',None),('group_signal','EPERM_ASSUMED_EMPTY'),('secondary',[{'action':'x','error':'other'}])):
     changed=copy.deepcopy(row);changed[field]=value;refused(lambda:stage.validate_step(changed,0,'compiler_identity',[stage.TOOLS['cc'],'--version'],runner.env))
   f.case_observation={'variant':variant,'record':row,'fake_calls':fx.calls,'actual_signal':False}
  add('D456_eperm_'+variant,eperm_case)
 def eperm_pipeline(f):
  f.fx_fault='anchored_eperm';record=f.pipeline();assert record['status']=='BLACKWOOD_NATIVE_LINKED_NOT_RUN',record['errors'];assert len(record['steps'])==126 and all(row['group_signal']=='EPERM_DENIED_WHILE_ANCHORED' for row in record['steps'])
  assert f.check()['status']=='VERIFIED_BUILD_ONLY_NOT_RUN';f.case_observation={'denial_steps':126,'independent_verifier':'PASS','actual_process':False}
 add('D456_complete_eperm_build_and_verifier',eperm_pipeline)
 for variant in ('binding','wrong_candidate','legacy','self_reference','invalid_id'):
  def manifest_case(f,variant=variant):
   f.gate();path=stage.manifest_path(f.ident);assert path=='web/repro/blackwood-source-manifests/'+f.ident+'.json'
   if variant=='binding':
    old=f.put('web/repro/blackwood-source-manifest.json',b'FIXTURE_ONLY_PRESERVED_OLD');f.auth['observation']['preservation']=f.view.preservation();f.write();f.gate();assert old.read_bytes()==b'FIXTURE_ONLY_PRESERVED_OLD'
   elif variant=='invalid_id':
    for ident in ('../bad','',True):refused(lambda ident=ident:stage.manifest_path(ident))
   elif variant=='self_reference':
    manifest=Path(f.root)/path;doc=stage.loads(manifest.read_bytes());doc['entries'].append({'path':path,'bytes':manifest.stat().st_size,'sha256':stage.sha(manifest.read_bytes()),'mode':0o644});doc['entries'].sort(key=lambda row:row['path']);manifest.write_text(stage.canonical_json(doc));h=stage.sha(manifest.read_bytes());f.auth['source_manifest']['sha256']=h;f.auth['observation']['inputs'][str(manifest)]=h;f.write();refused(f.gate)
   else:
    f.auth['source_manifest']['path']=stage.manifest_path('OTHER_CANDIDATE') if variant=='wrong_candidate' else 'web/repro/blackwood-source-manifest.json';f.write();refused(f.gate)
   assert not f.tool_calls and not f.output().exists();f.case_observation={'variant':variant,'derived_manifest':path,'actual_manifest_write':False}
  add('D456_manifest_'+variant,manifest_case)
 def alias_success(f):
  f.gate();f.view.declared_inputs=f.auth['observation']['inputs']
  for alias,(target,edges) in stage.SDK_LINK_ALIASES.items():
   assert stage.sdk_link_path(f.view,alias)==target and stage.sdk_link_path(f.view,target)==target
  f.case_observation={'fixed_aliases':4,'canonical_targets':3,'result':'PASS'}
 add('D462_exact_aliases_and_canonical_targets',alias_success)
 def alias_edges(f):
  f.gate();f.view.declared_inputs=f.auth['observation']['inputs'];count=0
  for alias,(_,edges) in stage.SDK_LINK_ALIASES.items():
   for edge,raw in edges:
    p=f.view.mapped(edge)
    for mutation in ('text','mode','type','missing'):
     if mutation=='mode':os.lchmod(p,0o700)
     else:
      p.unlink()
      if mutation=='text':p.symlink_to('./'+raw);os.lchmod(p,0o755)
      elif mutation=='type':p.write_bytes(b'FIXTURE_ONLY_SDK')
     refused(lambda:stage.sdk_link_path(f.view,alias));count+=1
     if p.exists() or p.is_symlink():p.unlink()
     p.symlink_to(raw);os.lchmod(p,0o755)
  f.case_observation={'exact_edge_mutations_refused':count}
 add('D462_edge_text_mode_type_missing',alias_edges)
 def alias_targets(f):
  f.gate();f.view.declared_inputs=f.auth['observation']['inputs'];count=0
  for alias,(target,_) in stage.SDK_LINK_ALIASES.items():
   p=f.view.mapped(target);data=p.read_bytes();relative=target[len(stage.SDK)+1:]
   p.write_bytes(b'FIXTURE_ONLY_CHANGED');refused(lambda:stage.sdk_link_path(f.view,alias));p.write_bytes(data);count+=1
   extra=p.with_name('FIXTURE_ONLY_HARDLINK');os.link(p,extra);refused(lambda:stage.sdk_link_path(f.view,alias));extra.unlink();count+=1
   p.rename(extra);p.symlink_to(extra.name);refused(lambda:stage.sdk_link_path(f.view,alias));p.unlink();extra.rename(p);count+=1
   h=f.view.declared_inputs.pop(target);refused(lambda:stage.sdk_link_path(f.view,alias));f.view.declared_inputs[target]=h;count+=1
   h=f.view.sdk_files.pop(relative);refused(lambda:stage.sdk_link_path(f.view,alias));f.view.sdk_files[relative]=h;count+=1
   h=f.view.sdk_files[relative];f.view.sdk_files[relative]='0'*64;refused(lambda:stage.sdk_link_path(f.view,alias));f.view.sdk_files[relative]=h;count+=1
  f.case_observation={'target_hash_link_and_declaration_refusals':count}
 add('D462_target_hash_type_links_declarations',alias_targets)
 def alias_unknown(f):
  f.gate();f.view.declared_inputs=f.auth['observation']['inputs'];unknown=stage.SDK+'/usr/lib/UNKNOWN.tbd';p=f.view.mapped(unknown);p.symlink_to('libc++.1.tbd');os.lchmod(p,0o755);refused(lambda:stage.sdk_link_path(f.view,unknown));p.unlink()
  leaf=stage.SDK+'/usr/lib/libpthread.tbd';p=f.view.mapped(leaf);p.unlink();p.symlink_to('EXTRA_HOP.tbd');hop=p.with_name('EXTRA_HOP.tbd');hop.symlink_to('libSystem.tbd');os.lchmod(p,0o755);os.lchmod(hop,0o755);refused(lambda:stage.sdk_link_path(f.view,leaf))
  f.case_observation={'unknown_same_target_alias':'REFUSED','extra_hop_same_canonical_target':'REFUSED'}
 add('D462_unknown_alias_and_extra_hop',alias_unknown)
 def alias_intermediate(f):
  f.gate();f.view.declared_inputs=f.auth['observation']['inputs'];leaf=stage.SDK+'/usr/lib/libpthread.tbd';middle=f.view.mapped(stage.SDK+'/usr/lib/libSystem.tbd');assert os.readlink(f.view.mapped(leaf))=='libSystem.tbd'
  middle.unlink();middle.symlink_to('./libSystem.B.tbd');os.lchmod(middle,0o755);refused(lambda:stage.sdk_link_path(f.view,leaf));middle.unlink();middle.symlink_to('libSystem.B.tbd');os.lchmod(middle,0o755)
  parent=middle.parent;other=parent.with_name('FIXTURE_ONLY_LIB_MOVED');parent.rename(other);parent.symlink_to(other.name,target_is_directory=True);refused(lambda:stage.sdk_link_path(f.view,leaf))
  f.case_observation={'pthread_intermediate_raw_edge':'REFUSED_WHEN_CHANGED','symlink_ancestor':'REFUSED'}
 add('D462_pthread_intermediate_and_ancestors',alias_intermediate)
 def alias_trace(f):
  record=f.pipeline();assert record['status']=='BLACKWOOD_NATIVE_LINKED_NOT_RUN',record['errors']
  for mode in ('release','debug'):
   inputs=record['modes'][mode]['link_inputs'];assert not set(stage.SDK_LINK_ALIASES)&set(inputs)
   assert {target for target,_ in stage.SDK_LINK_ALIASES.values()}<=set(inputs)
   for target,_ in stage.SDK_LINK_ALIASES.values():assert inputs[target]['origin']==target
   index=record['modes'][mode]['link_step'];trace=(f.output()/f'logs/{index:03d}.stdout').read_text();assert all(alias in trace.splitlines() for alias in stage.SDK_LINK_ALIASES)
  assert f.check()['status']=='VERIFIED_BUILD_ONLY_NOT_RUN';f.case_observation={'four_alias_raw_trace':'PASS','canonical_record_format':'UNCHANGED','independent_verifier':'PASS'}
 add('D462_complete_alias_trace_canonical_records',alias_trace)
 return rows

def main():
 global stage,build,verify,NATIVE_OPS,NATIVE_VIEW
 start=time.monotonic()
 parser=argparse.ArgumentParser();parser.add_argument('--pass-id',required=True);parser.add_argument('--plan-sha256',required=True);args=parser.parse_args()
 assert re.fullmatch(r'pass-[1-9][0-9]*',args.pass_id)
 plan_path=OWN/'preparation-1'/('plan-'+args.pass_id+'.json');data=plan_path.read_bytes();assert hashlib.sha256(data).hexdigest()==args.plan_sha256
 plan=json.loads(data);assert plan['kind']=='T167_GUARDED_PREPARATION_PLAN' and plan['pass_id']==args.pass_id
 names=('stage.py','build.py','verify.py','test_preparation.py','SCHEMA.md','README.md')
 assert set(plan['source_pins'])==set(names)
 for name in names:assert hashlib.sha256((OWN/name).read_bytes()).hexdigest()==plan['source_pins'][name]
 prep=OWN/'preparation-1'/args.pass_id;container=OWN/'supervisor-fixtures-1'
 if not container.exists():container.mkdir()
 fixture_root=container/args.pass_id;prep.mkdir();fixture_root.mkdir();(prep/'sources').mkdir()
 for name in names:
  assert time.monotonic()<start+PASS_SECONDS,'source snapshot original pass cutoff'
  (prep/'sources'/name).write_bytes((OWN/name).read_bytes())
 guards=Guards([prep,fixture_root],start);rows=[];failure=None;patches=[];initial_denials=0
 try:
  guards.install()
  assert 'ctypes' not in sys.modules and '_ctypes' not in sys.modules,'ctypes must not be preloaded in this preparation process'
  # Real host boundaries and old code must already be denied before loading new modules.
  for fn in [lambda:subprocess.Popen([]),lambda:os.killpg(1,9),lambda:os.waitpid(1,0),lambda:socket.socket(),lambda:signal.setitimer(signal.ITIMER_REAL,1),lambda:shutil.copytree('/FIXTURE_ONLY',str(fixture_root/'copy')),lambda:open(PROJECT/'web/server/candidate/stage.py'),lambda:os.mkdir(PROJECT/'web/server/blackwood-candidate-attempts'),lambda:__import__('ctypes')]:
   try:fn()
   except AssertionError:pass
   else:raise AssertionError('guard self-check failed')
  initial_denials=len(guards.denials)
  for name in ('stage','build','verify'):
   assert name not in sys.modules,'preloaded project module'
   spec=importlib.util.spec_from_file_location(name,OWN/(name+'.py'));module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module);globals()[name]=module
  actual_view=stage.View
  NATIVE_VIEW=actual_view
  NATIVE_OPS=build.RealOps
  for name,value in actual_view.__dict__.items():
   if callable(value) and name not in FixtureView.__dict__:setattr(FixtureView,name,value)
  definitions=cases();universe=[n for n,_ in definitions];assert len(universe)<=256 and len(set(plan['cases']))==len(plan['cases']),'finite unique case plan'
  assert hashlib.sha256(('\n'.join(universe)+'\n').encode()).hexdigest()==plan['case_universe_sha256'],'fixed case universe changed'
  definitions=[(n,fn) for n,fn in definitions if n in plan['cases']]
  assert definitions and [n for n,_ in definitions]==plan['cases'],'finite ordered case plan mismatch'
  guards.end=start+PASS_SECONDS-15 # Original pass budget reserves terminal evidence.
  for index,(name,fn) in enumerate(definitions):
   guards.check();case_root=fixture_root/f'{index:03d}-{name}';case_root.mkdir();f=Fixture(case_root,guards)
   patches=[patch.object(stage,'View',lambda root:f.new_view()),patch.object(build,'RealOps',lambda:FakeOps(f))]
   real_protection=stage.protected_inventory
   patches.append(patch.object(stage,'protected_inventory',lambda root,active=None,omit_container=False:real_protection(root,active,omit_container,browser_sdk=None,native_sdk=f.sdk_root)))
   for item in patches:item.start()
   case_failure=None
   try:fn(f)
   except BaseException as e:case_failure=type(e).__name__+': '+str(e)[:2048];raise
   finally:
    for item in reversed(patches):item.stop()
    patches=[]
    if stage is not None:
     observed={'name':name,'classification':'SIMULATED','status':'PASS' if case_failure is None else 'FAILED','failure':case_failure,'details':getattr(f,'case_observation',{}),'fake_tool_calls':len(f.tool_calls),'actual_process':False}
     stage.durable_new(case_root/'case-observation.json',(json.dumps(observed,sort_keys=True,indent=2)+'\n').encode(),check=guards.check)
   guards.check();rows.append({'name':name,'status':'PASS','classification':'SIMULATED','fake_tool_calls':len(f.tool_calls),'actual_process':False})
  assert len(guards.denials)==initial_denials,'unexpected attempt of forbidden host effect'
 except BaseException as e:failure=type(e).__name__+': '+str(e)[:2048]
 finally:
  for item in reversed(patches):item.stop()
  try:
   guards.end=start+PASS_SECONDS # Separate terminal ledger; never a new start/grace.
   guards.check();members=[p for base in (prep,fixture_root) for p in base.rglob('*') if p.is_file()];storage=sum(p.stat().st_size for p in members);assert storage<=STORAGE_CAP and len(members)<=75000,'finite fixture storage/file bound'
   result={'kind':'T167_GUARDED_PREPARATION_RESULT','fixture_only':True,'pass_id':args.pass_id,'status':'PASS' if failure is None else 'FAILED','cases_completed':len(rows),'planned_cases':len(plan['cases']),'cases':rows,'failure':failure,'guard_denials':len(guards.denials),'guard_self_checks':initial_denials,'unexpected_denials':len(guards.denials)-initial_denials,'denial_events':guards.denials[-64:],'output_observed_bytes':guards.observed,'storage_bytes':storage,'elapsed_seconds':time.monotonic()-start,'source_pins':plan['source_pins'],'actual_project_plan_build_verify':False,'actual_process_tool_copy_runtime':False}
   raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
   for path in (prep/'result.json',fixture_root/'result.json'):
    if stage is not None:stage.durable_new(path,raw,check=guards.check)
    else:
     guards.check()
     with path.open('xb') as out:out.write(raw);out.flush();os.fsync(out.fileno())
   summary=json.dumps({k:result[k] for k in ('status','pass_id','cases_completed','planned_cases','failure','output_observed_bytes','storage_bytes','elapsed_seconds')});guards.charge(summary.encode());print(summary)
  finally:guards.restore()
 return 0 if failure is None else 1

if __name__=='__main__':raise SystemExit(main())
