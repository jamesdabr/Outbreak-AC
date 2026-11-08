"""T092 candidate builder. Preparation plans are pure; real tools need MAIN pins."""
import argparse,json,os,time
from pathlib import Path
import stage
ROOT=stage.ROOT

def pin_bytes(root,path,expected):
 p=Path(path);stage.need(p.is_absolute() and p.parent==Path(root)/'notes/decisions' and p.suffix=='.json' and not p.is_symlink() and p.is_file(),'absolute MAIN pin JSON required')
 data=p.read_bytes();stage.need(stage.sha(data)==stage.digest(expected),'pins digest changed');return data

class Runner:
 """Only called with recipe-generated argv after authorization. Own group only."""
 def __init__(self,root,base,persist=True):self.root=Path(root);self.base=Path(base);self.persist=persist;self.started=time.monotonic();self.total_bytes=0;self.records=[];self.env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','TMPDIR':str(self.base/'tmp'),'CLANG_MODULE_CACHE_PATH':str(self.base/'tmp/modules')}
 def run(self,kind,argv):
  import subprocess,selectors,signal
  stage.need(time.monotonic()-self.started<1800,'whole attempt1800s deadline')
  index=len(self.records);start=time.monotonic();buffers=[bytearray(),bytearray()];child=None;timed=False;overflow=False;killed=False
  record={'index':index,'kind':kind,'argv':list(argv),'environment':self.env,'timeout_s':120,'exit':None,'timed_out':False,'overflow':False,'kill_fallback':False,'group_reaped':False,'elapsed_ms':0,'stdout_path':f'logs/{index:03d}.stdout','stderr_path':f'logs/{index:03d}.stderr','stdout_sha256':None,'stderr_sha256':None}
  self.records.append(record)
  try:
   stage.owned_path(self.base,self.base/'tmp','directory');stage.owned_path(self.base,self.base/'logs','directory')
   child=subprocess.Popen(argv,cwd=self.root,env=self.env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
   with selectors.DefaultSelector() as selector:
    selector.register(child.stdout,selectors.EVENT_READ,0);selector.register(child.stderr,selectors.EVENT_READ,1)
    while selector.get_map():
     if time.monotonic()-start>=116 or time.monotonic()-self.started>=1796:timed=True;break
     for key,_ in selector.select(.05):
      b=os.read(key.fd,16384)
      if not b:selector.unregister(key.fileobj);continue
      buffers[key.data].extend(b);self.total_bytes+=len(b)
      if sum(map(len,buffers))>stage.MAX_LOG or self.total_bytes>64*1024*1024:overflow=True;break
     if overflow:break
   if child.poll() is None and not (timed or overflow):
    try:child.wait(timeout=max(.001,min(116-(time.monotonic()-start),1796-(time.monotonic()-self.started))))
    except subprocess.TimeoutExpired:timed=True
  finally:
   if child is not None:
    if child.poll() is None:
     os.killpg(child.pid,signal.SIGTERM);killed=True
     try:child.wait(timeout=2)
     except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait(timeout=2);killed=True
    # Parent exit does not prove descendants in its owned group have gone.
    def group_live():
     try:os.killpg(child.pid,0);return True
     except ProcessLookupError:return False
    if group_live():
     os.killpg(child.pid,signal.SIGTERM);killed=True;deadline=time.monotonic()+2
     while group_live() and time.monotonic()<deadline:time.sleep(.01)
     if group_live():os.killpg(child.pid,signal.SIGKILL);killed=True
    record['exit']=child.returncode
    for p in (child.stdout,child.stderr):p.close()
    try:os.killpg(child.pid,0)
    except ProcessLookupError:record['group_reaped']=True
   record.update(timed_out=timed,overflow=overflow,kill_fallback=killed,elapsed_ms=(time.monotonic()-start)*1000)
   for key,b in zip(('stdout','stderr'),buffers):
    data=bytes(b[:stage.MAX_LOG]);file=self.base/record[key+'_path']
    if self.persist:
     stage.owned_path(self.base,file,absent=True)
     with file.open('xb') as output:output.write(data)
    record[key+'_sha256']=stage.sha(data)
  stage.need(record['exit']==0 and not timed and not overflow and not killed and record['group_reaped'] and record['elapsed_ms']<=120000,'command failed/timeout/overflow/owned cleanup')
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
  if physical in objects:origin='OWN_FRESH_OBJECT'
  elif stage.beneath(physical,copy):
   name=physical[len(copy)+1:];stage.need(name in signed and signed[name]['kind']=='file' and view.hash(physical)==signed[name]['sha256'],'unknown/changed staged linker input');origin='OWN_SIGNED_FRAMEWORK'
  else:
   stage.need(stage.beneath(physical,stage.CLT) and physical in view.declared_inputs and view.hash(physical)==view.declared_inputs[physical],'undeclared/changed/non-SDK linker input');origin=physical
  if physical not in files:files[physical]={'origin':origin,'sha256':view.hash(physical),'archive_members':[]}
  if member and member not in files[physical]['archive_members']:files[physical]['archive_members'].append(member)
 stage.need(set(objects)<=set(files),'linker trace missing fresh objects')
 stage.need(copy+'/Versions/A/SDL2' in files,'actual copied SDL2 link input absent')
 stage.need(any(stage.beneath(n,stage.SDK+'/usr/lib') for n in files),'SDK linker input absent')
 return dict(sorted(files.items()))

def execute(root,ident,pin,expected):
 view=stage.View(root);data=pin_bytes(root,pin,expected);auth=stage.authorize(data,expected,ident,view);base=Path(stage.attempt(view.root,ident));container_preexisting=base.parent.exists()
 protection=stage.protected_inventory(view.root);base=stage.reserve(view.root,ident);view.active=str(base);view.omit_container=not container_preexisting;view.declared_inputs=auth['observation']['inputs'];runner=Runner(view.root,base);recipe=stage.commands(view.root,ident)
 record={'schema_version':1,'kind':'NATIVE_CANDIDATE_BUILD_RECORD','recipe':'native_standalone_v1','candidate_id':ident,'pins_path':str(pin),'pins_sha256':expected,'status':'RESERVED','claims':stage.CLAIMS.copy(),'object_reuse':False,'container_preexisting':container_preexisting,'protection_before':protection,'steps':runner.records,'tool_identity':{},'stage_before':None,'stage_after':None,'sign_steps':[],'signature_steps':[],'framework_checks':[],'modes':{},'errors':[],'elapsed_ms':0}
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
  for role in ('cc','cxx'):
   index,out,err=runner.run('compiler_identity',[stage.TOOLS[role],'--version']);tool_identity(out);record['tool_identity'][role]=index
  stage.need(view.json(stage.SDK+'/SDKSettings.json').get('Version')=='15.5','actual SDK version mismatch')
  current();copy=stage.stage_copy(view.root,ident,auth['observation']['source_framework']);record['stage_before']=stage.inventory(copy)
  for argv in recipe['sign']:record['sign_steps'].append(runner.run('adhoc_sign_copy',argv)[0])
  for argv in recipe['signature']:record['signature_steps'].append(runner.run('verify_copy_signature',argv)[0])
  record['stage_after']=stage.signed_inventory(record['stage_before'],stage.inventory(copy))
  for path in fixed_inspections(base,recipe):record['framework_checks'].append(inspect(path,6))
  for mode,spec in recipe['modes'].items():
   m={'units':[],'binary':spec['binary'],'link_step':None,'link_inputs':{},'inspection':None};record['modes'][mode]=m;objects=[]
   for row in spec['units']:
    current();stage.need(all(not Path(row[k]).exists() and not Path(row[k]).is_symlink() and all(not q.is_symlink() for q in Path(row[k]).parents) for k in ('object','dep','pre_dep')),'object/dependency reuse or alias refused')
    discover,_,_=runner.run('discover_dependencies',row['discover']);stage.owned_path(base,row['pre_dep']);stage.owned_paths(base,auth['observation']['source_framework']);before=stage.dependency_paths(Path(row['pre_dep']).read_text(),row['object'],view,ident)
    current();compile_index,_,_=runner.run('compile',row['compile']);stage.owned_path(base,row['dep']);stage.owned_path(base,row['object']);stage.owned_paths(base,auth['observation']['source_framework']);after=stage.dependency_paths(Path(row['dep']).read_text(),row['object'],view,ident);stage.need(before==after,'actual consumed dependency membership/bytes changed')
    stage.macho(Path(row['object']).read_bytes(),1);obj_index,out,err=runner.run('object_file',[stage.TOOLS['file'],row['object']]);stage.need('Mach-O 64-bit object arm64' in out,'actual object signature')
    m['units'].append({**row,'discover_step':discover,'compile_step':compile_index,'file_step':obj_index,'dependencies':before,'object_sha256':view.hash(row['object']),'pre_dep_sha256':view.hash(row['pre_dep']),'dep_sha256':view.hash(row['dep'])});objects.append(row['object'])
   current()
   for unit in m['units']:
    stage.owned_path(base,unit['object'])
    stage.need(view.hash(unit['object'])==unit['object_sha256'],'object changed before link')
    for name,d in unit['dependencies'].items():stage.need(view.hash(name)==d['sha256'],'actual dependency changed before link')
   stage.need(not Path(spec['binary']).exists() and not Path(spec['binary']).is_symlink(),'binary reuse/alias refused');index,out,err=runner.run('link',spec['link']);m['link_step']=index;m['link_inputs']=link_inputs(out,objects,view,ident,record['stage_after']);m['inspection']=inspect(spec['binary'],2,True)
  current(True);record['status']='NATIVE_LINKED_NOT_RUN'
 except Exception as e:record['errors'].append(type(e).__name__+': '+str(e));record['status']='FAILED'
 finally:
  record['elapsed_ms']=(time.monotonic()-runner.started)*1000
  owned_ok=True
  try:current(True);stage.need(record['elapsed_ms']<=1800000,'whole attempt deadline')
  except Exception as e:record['errors'].append(str(e));record['status']='FAILED'
  try:stage.owned_paths(base,auth['observation']['source_framework'])
  except Exception as e:owned_ok=False;record['errors'].append('owned seal refused: '+str(e));record['status']='FAILED'
  stage.owned_path(base,base/'report.json',absent=True)
  with (base/'report.json').open('x') as output:output.write(stage.canonical_json(record))
  if owned_ok:
   files=stage.owned_inventory(base,auth['observation']['source_framework']);files.pop('freeze.json',None);files.pop('verification/receipt.json',None);stage.owned_path(base,base/'freeze.json',absent=True)
   with (base/'freeze.json').open('x') as output:output.write(stage.canonical_json({'schema_version':1,'kind':'NATIVE_CANDIDATE_FREEZE','candidate_id':ident,'status':record['status'],'files':files,'optional_receipt':'verification/receipt.json','claims':stage.CLAIMS.copy()}))
 return record

def plan(root,ident):return {'schema_version':1,'status':'NOT_RUN','candidate_id':stage.identifier(ident),'observation':'Recipe only; any separate read-only observation is not a compiler identity/dependency probe or execution authority','recipe':stage.commands(str(Path(root).resolve()),ident),'pending':['MAIN source manifest and complete current consumed closure','MAIN expected digest + accepted execution pins + separate actual release'],'claims':stage.CLAIMS.copy()}
def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--plan-only',action='store_true');g.add_argument('--execute',action='store_true');p.add_argument('--candidate-id',required=True);p.add_argument('--pins');p.add_argument('--pins-sha256');a=p.parse_args();stage.identifier(a.candidate_id)
 if a.plan_only:
  stage.need(not a.pins and not a.pins_sha256,'plan requires no execution identity');value=plan(ROOT,a.candidate_id);out=ROOT/'web/server/candidate'/('preparation-'+a.candidate_id);out.mkdir(exist_ok=False);(out/'plan.json').write_text(stage.canonical_json(value));print(stage.canonical_json(value));return 0
 stage.need(a.pins and a.pins_sha256,'MAIN execution pins required');r=execute(ROOT,a.candidate_id,a.pins,a.pins_sha256);print(stage.canonical_json({'status':r['status'],'errors':r['errors'],'claims':r['claims']}));return 0 if r['status']=='NATIVE_LINKED_NOT_RUN' else 1
if __name__=='__main__':
 try:raise SystemExit(main())
 except (stage.Refused,OSError,ValueError) as e:print(stage.canonical_json({'status':'REFUSED','reason':str(e),'claims':stage.CLAIMS}));raise SystemExit(2)
