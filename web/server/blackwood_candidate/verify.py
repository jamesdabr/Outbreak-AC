"""Independent candidate record/current-byte verifier. No compiler/signing/server launch."""
import argparse,json,re
from pathlib import Path
import stage
from build import Runner  # Shared bounded capture only; verification logic below is separate.
ROOT=stage.ROOT

def verify(root,ident,pin,expected,receipt=None):
 root=str(Path(root).resolve());base=Path(stage.attempt(root,ident));pins_path=Path(pin)
 view=stage.View(root);inspector=Runner(root,base,persist=False,view=view);inspector.check()
 stage.need(pins_path.is_absolute() and pins_path.parent==Path(root)/'notes/decisions' and pins_path.suffix=='.json' and not pins_path.is_symlink(),'MAIN verification pins path')
 if receipt is not None:stage.need(Path(receipt)==base/'verification/receipt.json','exact owned receipt path required')
 stage.need(pins_path.stat().st_nlink==1 and pins_path.stat().st_size<=stage.MAX_CONTROL and str(pins_path.resolve())==str(pins_path) and all(not p.is_symlink() for p in pins_path.parents),'ordinary bounded current MAIN control')
 def current_pins():stage.owned_path(root,pins_path);return stage.read_bounded(pins_path,stage.MAX_CONTROL)
 data=current_pins();view.active=str(base);auth=stage.authorize(data,expected,ident,view,existing=True);view.declared_inputs=auth['observation']['inputs'];recipe=stage.commands(root,ident);inspector.check()
 stage.need(not (base/'failure.json').exists() and not (base/'failure.json').is_symlink(),'refusal marker present')
 stage.need(base.is_dir() and not base.is_symlink(),'ordinary candidate root')
 stage.owned_paths(base,auth['observation']['source_framework']);stage.owned_path(base,base/'report.json');stage.owned_path(base,base/'freeze.json')
 old=base/'verification/receipt.json'
 def slot_identity():
  stage.owned_path(base,old.parent,'directory')
  if not old.exists() and not old.is_symlink():return None
  stage.owned_path(base,old);s=old.lstat();stage.need(stage.stat.S_IMODE(s.st_mode)==0o644,'optional receipt ordinary0644 identity');return (s.st_dev,s.st_ino,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode)
 expected_slot=slot_identity()
 def receipt_boundary(encoded=None):
  inspector.check();observed=slot_identity();stage.need(observed==expected_slot,'receipt slot created/replaced/deleted during verification')
  if observed is not None and encoded is not None:stage.need(stage.read_bounded(old,len(encoded))==encoded and slot_identity()==observed,'final exact receipt content/ordinary identity differs')
  inspector.check()
 record=view.json(str(base/'report.json'));freeze=view.json(str(base/'freeze.json'))
 stage.exact(record,['schema_version','kind','recipe','candidate_id','pins_path','pins_sha256','status','fixture_only','source_revision','source_manifest','source_acceptance','map_seed','claims','object_reuse','container_preexisting','protection_before','steps','tool_identity','stage_before','stage_after','sign_steps','signature_steps','framework_checks','modes','errors','elapsed_ms'],'build record fields')
 stage.need(type(record['schema_version']) is int and record['schema_version']==1 and record['kind']=='BLACKWOOD_NATIVE_BUILD_RECORD' and record['recipe']=='blackwood_native_standalone_v1' and record['candidate_id']==ident and record['pins_path']==str(pin) and record['pins_sha256']==expected and record['status']=='BLACKWOOD_NATIVE_LINKED_NOT_RUN' and record['claims']==stage.CLAIMS and all(v is False for v in record['claims'].values()) and record['fixture_only'] is view.fixture_only and record['source_revision']==auth['source_revision'] and record['source_manifest']==auth['source_manifest'] and record['source_acceptance']==auth['source_acceptance'] and record['object_reuse'] is False and record['errors']==[] and type(record['container_preexisting']) is bool and type(record['elapsed_ms']) in (int,float) and 0<=record['elapsed_ms']<=1800000,'candidate failed/reused/runtime/authority record')
 stage.need(record['container_preexisting']==(str(base.parent) in auth['observation']['preservation']['directories']),'original container phase mismatch')
 stage.exact(freeze,['schema_version','kind','candidate_id','status','fixture_only','files','optional_receipt','claims'],'freeze fields')
 stage.need(type(freeze['schema_version']) is int and freeze['schema_version']==1 and freeze['kind']=='BLACKWOOD_NATIVE_TERMINAL_FREEZE' and freeze['candidate_id']==ident and freeze['fixture_only'] is view.fixture_only and freeze['status']==record['status'] and stage.same_typed(freeze['claims'],stage.CLAIMS) and freeze['optional_receipt']=='verification/receipt.json','freeze identity')
 def frozen():
  items=stage.owned_inventory(base,auth['observation']['source_framework']);items.pop('freeze.json',None);items.pop('verification/receipt.json',None);stage.need(stage.same_typed(items,freeze['files']),'terminal owned inventory/hash/mode/link mismatch')
 stage.need(stage.same_typed(record['map_seed'],stage.seed_record(base,auth['observation']['map_seed'])),'independent staged seed mismatch')
 expected_plan={'schema_version':1,'kind':'BLACKWOOD_NATIVE_BUILD_PLAN','status':'NOT_EXECUTED','recipe':stage.RECIPE,'candidate_id':ident,'source_revision':auth['source_revision'],'source_manifest':auth['source_manifest'],'source_acceptance':auth['source_acceptance'],'observation':auth['observation'],'commands':stage.command_plan(root,ident),'environment':{'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','TMPDIR':str(base/'tmp'),'CLANG_MODULE_CACHE_PATH':str(base/'tmp/modules')},'claims':stage.CLAIMS.copy(),'pending':[]}
 stage.owned_path(base,base/'plan.json');stage.need(stage.same_typed(view.json(str(base/'plan.json')),expected_plan),'immutable pre-effect plan differs')
 frozen();stage.need(stage.same_typed(stage.protected_inventory(root,str(base),not record['container_preexisting']),record['protection_before']),'original membership/modes/links changed')
 copy=base/'deps-signed/SDL2.framework';stage.need(stage.same_typed(record['stage_before'],auth['observation']['source_framework']) and stage.same_typed(stage.inventory(copy),record['stage_after']),'actual stage inventory mismatch');stage.signed_inventory(record['stage_before'],record['stage_after'])
 steps=record['steps'];stage.need(type(steps) is list and len(steps)==126,'command record bound');cursor=0;total_log_bytes=0
 env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','TMPDIR':str(base/'tmp'),'CLANG_MODULE_CACHE_PATH':str(base/'tmp/modules')}
 def step(index,kind,argv):
  nonlocal cursor,total_log_bytes
  stage.need(type(index) is int and index==cursor and cursor<len(steps),'ordered command record index');s=steps[cursor];cursor+=1
  stage.validate_step(s,index,kind,argv,env)
  armed=view.arm_tool(s['tool_role']['role'],auth['observation']['tools'][s['tool_role']['role']]['sha256']);stage.need(s['tool_role']==armed,'historical/current named tool identity changed')
  raw_path=stage.owned_path(base,base/f'logs/{index:03d}.receipt.json');raw=stage.loads(stage.read_bounded(raw_path,stage.MAX_CONTROL));stage.exact(raw,stage.STEP_KEYS,'raw pending command receipt fields')
  stage.need(type(raw['elapsed_ms']) in (int,float) and 0<=raw['elapsed_ms']<=s['elapsed_ms'],'raw receipt elapsed bound');pending=dict(s);pending.update(status='PENDING_PUBLICATION',publication='PENDING',elapsed_ms=raw['elapsed_ms']);stage.need(stage.same_typed(raw,pending),'raw receipt differs from confirmed report ledger')
  text=[];command_bytes=0
  for name in ('stdout','stderr'):
   need_path=f'logs/{index:03d}.{name}';stage.need(s[name+'_path']==need_path,'log path');p=stage.owned_path(base,base/need_path);size=p.stat().st_size;stage.need(size==s[name+'_bytes'] and command_bytes+size<=stage.MAX_LOG and total_log_bytes+size<=64*1024*1024,'log size bound before allocation');b=stage.read_bounded(p,size);command_bytes+=len(b);total_log_bytes+=len(b);stage.need(len(b)==size and stage.sha(b)==s[name+'_sha256'],'log missing/corrupt/overflow');text.append(b.decode(errors='replace'))
  return text
 stage.exact(record['tool_identity'],['cc','cxx'],'compiler identity fields')
 for role in ('cc','cxx'):
  out,err=step(record['tool_identity'][role],'compiler_identity',[stage.TOOLS[role],'--version']);stage.need('Apple clang version 17.' in out and 'Target: arm64-apple-darwin' in out and 'InstalledDir: '+stage.CLT+'/usr/bin' in out,'compiler identity provenance')
 stage.need(view.json(stage.SDK+'/SDKSettings.json').get('Version')=='15.5','SDK version')
 stage.need(len(record['sign_steps'])==2 and len(record['signature_steps'])==4,'signing order/count')
 for index,argv in zip(record['sign_steps'],recipe['sign']):step(index,'adhoc_sign_copy',argv)
 for index,argv in zip(record['signature_steps'],recipe['signature']):step(index,'verify_copy_signature',argv)
 def inspect(row,path,kind,rpath=False):
  stage.owned_path(base,path)
  stage.need(view.ordinary(path) and view.canonical(path)==path and (kind!=2 or view.mode(path)&0o100),'ordinary executable artifact required')
  stage.exact(row,['path','sha256','kind','steps'],'artifact inspection record');stage.need(row['path']==path and type(row['kind']) is int and row['kind']==kind and view.hash(path)==row['sha256'],'artifact identity');stage.macho(Path(path).read_bytes(),kind)
  stage.exact(row['steps'],['file','dependencies','load_commands','signature','adhoc'],'inspection command set')
  for name,argv in [('file',[stage.TOOLS['file'],path]),('dependencies',[stage.TOOLS['otool'],'-L',path]),('load_commands',[stage.TOOLS['otool'],'-l',path]),('signature',[stage.TOOLS['codesign'],'--verify','--verbose=4',path]),('adhoc',[stage.TOOLS['codesign'],'--display','--verbose=4',path])]:
   out,err=step(row['steps'][name],name,argv)
   if name=='file':stage.need('Mach-O' in out and 'arm64' in out,'recorded Mach-O signature')
   if name=='adhoc':stage.need('Signature=adhoc' in err,'recorded adhoc signature')
   if name=='load_commands':
    if rpath:stage.rpaths(out,[str(base/'deps-signed'),str(copy/'Versions/A/Frameworks')])
    else:stage.need(all(p in ('@loader_path/Frameworks','@executable_path/Frameworks') for p in re.findall(r'cmd LC_RPATH\n\s*cmdsize \d+\n\s*path (.*?) \(offset',out)),'framework RPATH')
   if name=='dependencies':
    names=stage.otool_dependencies(out,path);stage.need(names and all((s in ('@rpath/SDL2.framework/Versions/A/SDL2','@rpath/hidapi.framework/Versions/A/hidapi') or s.startswith(('/usr/lib/','/System/Library/Frameworks/'))) and '..' not in s.split('/') for s in names),'dynamic dependency escape')
    if rpath:stage.need('@rpath/SDL2.framework/Versions/A/SDL2' in names,'SDL load missing')
 stage.need(len(record['framework_checks'])==2,'framework inspection count')
 libraries=[str(copy/'Versions/A/SDL2'),str(copy/'Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi')]
 for row,path in zip(record['framework_checks'],libraries):inspect(row,path,6)
 stage.exact(record['modes'],['release','debug'],'two native modes required');binaries={}
 for mode,spec in recipe['modes'].items():
  m=record['modes'][mode];stage.exact(m,['units','binary','link_step','link_inputs','inspection'],'mode record');stage.need(m['binary']==spec['binary'] and len(m['units'])==16,'16 units per mode')
  for row,planned in zip(m['units'],spec['units']):
   stage.exact(row,[*planned,'discover_step','compile_step','file_step','dependencies','object_sha256','pre_dep_sha256','dep_sha256'],'unit record');stage.need(all(row[k]==v for k,v in planned.items()),'fixed unit/object/command plan mismatch')
   step(row['discover_step'],'discover_dependencies',planned['discover']);step(row['compile_step'],'compile',planned['compile']);out,err=step(row['file_step'],'object_file',[stage.TOOLS['file'],row['object']]);stage.need('Mach-O 64-bit object arm64' in out,'object signature')
   for key in ('object','pre_dep','dep'):stage.owned_path(base,row[key])
   stage.need(view.hash(row['object'])==row['object_sha256'] and view.hash(row['pre_dep'])==row['pre_dep_sha256'] and view.hash(row['dep'])==row['dep_sha256'],'object/dependency record bytes changed');stage.macho(Path(row['object']).read_bytes(),1)
   before=stage.dependency_paths(Path(row['pre_dep']).read_text(),row['object'],view,ident);after=stage.dependency_paths(Path(row['dep']).read_text(),row['object'],view,ident);stage.need(before==after==row['dependencies'] and root+'/'+row['unit'] in before,'consumed dependency membership/source/current hash differs')
  out,err=step(m['link_step'],'link',spec['link']);actual={};objects={row['object'] for row in m['units']}
  for line in out.splitlines():
   line=line.strip()
   if not line:continue
   match=re.fullmatch(r'(.+\.a)\(([^/()]+)\)',line);path=match.group(1) if match else line;physical=view.canonical(stage.absolute(path))
   stage.need(view.consume(physical),'nonordinary/multilink/role-as-link-input')
   if stage.beneath(physical,str(base)):stage.owned_path(base,physical)
   if physical in objects:origin='OWN_FRESH_OBJECT'
   elif stage.beneath(physical,str(copy)):
    item=record['stage_after'].get(physical[len(str(copy))+1:]);stage.need(item and item['kind']=='file' and view.hash(physical)==item['sha256'],'copied link file');origin='OWN_SIGNED_FRAMEWORK'
   else:stage.need(stage.sdk_link_path(view,path)==physical and stage.beneath(physical,stage.CLT) and physical in view.declared_inputs and view.hash(physical)==view.declared_inputs[physical],'unlisted actual linker dependency');origin=physical
   if physical not in actual:actual[physical]={'origin':origin,'sha256':view.hash(physical),'archive_members':[]}
   if match and match.group(2) not in actual[physical]['archive_members']:actual[physical]['archive_members'].append(match.group(2))
  stage.need(actual==m['link_inputs'] and objects<=set(actual) and str(copy/'Versions/A/SDL2') in actual and any(stage.beneath(p,stage.SDK+'/usr/lib') for p in actual),'actual link trace inventory differs')
  stage.need(stage.SDK+'/usr/lib/libc++.1.tbd' in actual and stage.CLT+'/usr/lib/clang/17/lib/darwin/libclang_rt.osx.a' in actual,'actual canonical C++/runtime link prerequisite missing')
  inspect(m['inspection'],spec['binary'],2,True);binaries[mode]={'path':spec['binary'],'sha256':view.hash(spec['binary'])}
 stage.need(cursor==len(steps),'extra/reused command records')
 # Re-run ONLY read-only inspectors, not compilers/signers or artifact programs.
 inspector.check()
 for path,kind in [(p,6) for p in libraries]+[(v['path'],2) for v in binaries.values()]:
  stage.owned_path(base,path)
  stage.macho(Path(path).read_bytes(),kind)
  for args in ([stage.TOOLS['file'],path],[stage.TOOLS['otool'],'-L',path],[stage.TOOLS['otool'],'-l',path],[stage.TOOLS['codesign'],'--verify','--verbose=4',path],[stage.TOOLS['codesign'],'--display','--verbose=4',path]):
   _,out,err=inspector.run('verification_readonly',args)
   if args[0]==stage.TOOLS['file']:stage.need('Mach-O' in out and 'arm64' in out,'live file signature')
   if '--display' in args:stage.need('Signature=adhoc' in err,'live signature identity')
   if args[0]==stage.TOOLS['otool'] and args[1]=='-L':
    names=stage.otool_dependencies(out,path);stage.need(names and all((s in ('@rpath/SDL2.framework/Versions/A/SDL2','@rpath/hidapi.framework/Versions/A/hidapi') or s.startswith(('/usr/lib/','/System/Library/Frameworks/'))) and '..' not in s.split('/') for s in names),'live dynamic dependency escape')
    if kind==2:stage.need('@rpath/SDL2.framework/Versions/A/SDL2' in names,'live SDL load missing')
   if args[0]==stage.TOOLS['otool'] and args[1]=='-l':
    if kind==2:stage.rpaths(out,[str(base/'deps-signed'),str(copy/'Versions/A/Frameworks')])
    else:stage.need(all(p in ('@loader_path/Frameworks','@executable_path/Frameworks') for p in re.findall(r'cmd LC_RPATH\n\s*cmdsize \d+\n\s*path (.*?) \(offset',out)),'live framework RPATH')
 def final_current(encoded=None):
  inspector.check();stage.need(not (base/'failure.json').exists() and not (base/'failure.json').is_symlink(),'late refusal marker')
  stage.authorize(current_pins(),expected,ident,view,existing=True)
  stage.need(stage.same_typed(stage.protected_inventory(root,str(base),not record['container_preexisting']),record['protection_before']),'late original complete protection changed, including unconsumed history')
  stage.need(stage.same_typed(stage.seed_record(base,auth['observation']['map_seed']),record['map_seed']),'late runtime seed changed')
  frozen();receipt_boundary(encoded)
 final_current()
 result={'schema_version':1,'kind':'BLACKWOOD_NATIVE_VERIFICATION','candidate_id':ident,'recipe':stage.RECIPE,'status':'VERIFIED_BUILD_ONLY_NOT_RUN','fixture_only':bool(view.fixture_only),'pins_sha256':expected,'report_sha256':view.hash(str(base/'report.json')),'freeze_sha256':view.hash(str(base/'freeze.json')),'source_manifest':auth['source_manifest'],'source_acceptance':auth['source_acceptance'],'map_seed':record['map_seed'],'binaries':binaries,'claims':stage.CLAIMS.copy()}
 encoded=stage.canonical_json(result).encode();receipt_boundary(encoded)
 if expected_slot is not None:receipt_boundary(encoded)
 elif receipt is not None:
  final_current(encoded);stage.owned_path(base,old,absent=True);stage.durable_new(old,encoded,check=inspector.check);inspector.check();expected_slot=slot_identity();stage.need(expected_slot is not None,'requested receipt absent after publication');receipt_boundary(encoded)
 final_current(encoded);stage.need(receipt is None or slot_identity() is not None,'requested final receipt presence');receipt_boundary(encoded)

 return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--candidate-id',required=True);p.add_argument('--pins',required=True);p.add_argument('--pins-sha256',required=True);p.add_argument('--receipt');a=p.parse_args();print(stage.canonical_json(verify(ROOT,a.candidate_id,a.pins,a.pins_sha256,a.receipt)))
if __name__=='__main__':
 try:main()
 except (stage.Refused,OSError,ValueError) as e:print(stage.canonical_json({'status':'REFUSED','reason':str(e),'claims':stage.CLAIMS}));raise SystemExit(2)
