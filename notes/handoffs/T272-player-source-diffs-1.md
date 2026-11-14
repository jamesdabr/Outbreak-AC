# T272 five-file source diffs

Baseline: accepted T270 pass9 snapshots. Verifier unchanged, RealOps backend AST-identical.

## stage.py

```diff
--- T270-accepted/stage.py
+++ T272/stage.py
@@ -19,7 +19,7 @@
 MAX_CONTROL=32*1024*1024
 MAX_RECORD=128*1024*1024
 RECIPE='blackwood_native_standalone_v1'
-MANIFEST='web/repro/blackwood-source-manifest.json'
+MANIFEST_DIR='web/repro/blackwood-source-manifests'
 ASSET_ROOT='web/assets/blackwood-profile'
 ASSET_MANIFEST_SHA='8c4f7eef5f0deafb06bec60d62be529a684a30d56bbdc6dc3e5f38dd21c69e60'
 ASSET_PROVENANCE_SHA='48b1bbd659fa0193bce88a8d76a9146fa8e84bc981f20c4203c133e26b64b3c3'
@@ -75,6 +75,9 @@
 def absolute(s):
  need(type(s) is str and s.startswith('/') and str(PurePosixPath(s))==s and all(p not in ('.','..') for p in s.split('/')[1:]) and not any(ord(c)<32 for c in s) and '\\' not in s,'noncanonical absolute path');return s
 def identifier(s):need(type(s) is str and re.fullmatch('[A-Za-z0-9_-]{1,48}',s),'invalid candidate ID');return s
+def manifest_path(ident):return MANIFEST_DIR+'/'+identifier(ident)+'.json'
+def exit0_observation(value,pid):
+ return integer(pid,1,2**31-1) and same_typed(value,{'pid':pid,'signo':20,'code':1,'status':0,'errno':0})
 def beneath(p,base):return p==base or p.startswith(base+'/')
 def fixture_forest(root,path):
  prefix=str(Path(root))+'/';name=str(path)
@@ -151,13 +154,13 @@
   modes[mode]['link']=[TOOLS['cxx'],*f[:5],*opt,*objects,'-F'+base+'/deps-signed','-framework','SDL2','-lz','-lpthread','-Wl,-t','-Wl,-rpath,'+base+'/deps-signed','-Wl,-rpath,'+copy+'/Versions/A/Frameworks','-o',modes[mode]['binary']]
  return {'sign':signing,'signature':signature,'modes':modes}
 
-def source_manifest(doc,revision,view,root):
+def source_manifest(doc,revision,view,root,manifest_relative=None):
  exact(doc,['schema_version','kind','source_revision','entries'],'source manifest fields')
  need(type(doc['schema_version']) is int and doc['schema_version']==1 and doc['kind']=='SOURCE_INPUT_MANIFEST' and doc['source_revision']==revision,'source manifest identity')
  need(type(doc['entries']) is list and doc['entries'],'empty source manifest');paths=[]
  for e in doc['entries']:
   exact(e,['path','bytes','sha256','mode'],'source entry fields');rel(e['path']);digest(e['sha256']);need(integer(e['bytes']) and type(e['mode']) is int and e['mode'] in (420,493),'source entry mode/size')
-  need(e['path']!='web/repro/blackwood-source-manifest.json','manifest self reference');p=root+'/'+e['path'];need(view.ordinary(p) and view.canonical(p)==p and view.hash(p)==e['sha256'] and view.size(p)==e['bytes'] and view.mode(p)==e['mode'],'source entry changed/link');paths.append(e['path'])
+  need(e['path']!=(manifest_relative or 'web/repro/blackwood-source-manifest.json'),'manifest self reference');p=root+'/'+e['path'];need(view.ordinary(p) and view.canonical(p)==p and view.hash(p)==e['sha256'] and view.size(p)==e['bytes'] and view.mode(p)==e['mode'],'source entry changed/link');paths.append(e['path'])
  need(paths==sorted(set(paths)),'source entries unique/sorted');return set(paths)
 
 def validate_framework(items):
@@ -227,8 +230,8 @@
  decision=rel(p['decision']);need(decision.startswith('notes/decisions/') and decision.endswith('.md') and len(PurePosixPath(decision).parts)==3,'decision path')
  need(type(p['source_revision']) is str and re.fullmatch('[0-9a-f]{40}',p['source_revision']) and p['source_revision']==view.head(),'actual HEAD mismatch')
  need(p['bindings']=={'repository':root,'system_sdk':SDK,'source_framework':root+'/'+FRAMEWORK},'root/SDK/framework binding mismatch')
- exact(p['source_manifest'],['path','sha256'],'manifest identity');need(p['source_manifest']['path']=='web/repro/blackwood-source-manifest.json','source manifest location');manifest=root+'/'+p['source_manifest']['path'];need(view.hash(manifest)==digest(p['source_manifest']['sha256']),'source manifest digest')
- entries=source_manifest(view.json(manifest),p['source_revision'],view,root)
+ exact(p['source_manifest'],['path','sha256'],'manifest identity');need(p['source_manifest']['path']==manifest_path(ident),'candidate-bound source manifest location');manifest=root+'/'+p['source_manifest']['path'];need(view.hash(manifest)==digest(p['source_manifest']['sha256']),'source manifest digest')
+ entries=source_manifest(view.json(manifest),p['source_revision'],view,root,manifest_path(ident))
  view.source_entries=entries
  source_acceptance(p['source_acceptance'],view,entries)
  required=set(CPP+C+['source/src/Makefile','source/enet/Makefile.am']+['web/server/blackwood_candidate/'+n for n in SCRIPT_NAMES]);need(required<=entries,'source manifest incomplete native recipe')
@@ -702,7 +705,7 @@
  exact(row['nonreaping'],['pid','signo','code','status','errno'],'nonreaping terminal record');need(all(type(v) is int for v in row['nonreaping'].values()) and row['nonreaping']=={'pid':row['pid'],'signo':20,'code':1,'status':0,'errno':0},'nonreaping exit0 observation')
  native=row['native_last'];exact(native,['pid','result','errno','record_bytes','record_hex'],'bounded last native observation');need(type(native['pid']) is int and native['pid']==row['pid'] and type(native['result']) is int and native['result']==0 and type(native['errno']) is int and native['errno']==0 and type(native['record_bytes']) is int and native['record_bytes']==104 and type(native['record_hex']) is str and re.fullmatch('[0-9a-f]{208}',native['record_hex']),'native observation shape')
  signo,association,code,pid,uid,status=struct.unpack_from('<iiiiIi',bytes.fromhex(native['record_hex']));need((signo,association,code,pid,status)==(20,0,1,row['pid'],0),'native observation differs from successful child event')
- need(row['group_signal'] in ('SIGKILL_SENT_WHILE_ANCHORED','ESRCH_WHILE_ANCHORED') and row['timed_out'] is False and row['overflow'] is False and row['primary'] is None and row['secondary']==[],'step cleanup/failure facts')
+ need(row['group_signal'] in ('SIGKILL_SENT_WHILE_ANCHORED','ESRCH_WHILE_ANCHORED','EPERM_DENIED_WHILE_ANCHORED') and row['timed_out'] is False and row['overflow'] is False and row['primary'] is None and row['secondary']==[],'step cleanup/failure facts')
  need(row['status']=='PASS' and row['publication']=='CONFIRMED' and type(row['elapsed_ms']) in (int,float) and math.isfinite(row['elapsed_ms']) and 0<=row['elapsed_ms']<=120000,'step terminal/publication/time')
  need(row['io_unresolved']==[],'unresolved command persistence handle')
  need(type(row['cleanup_attempts']) is list and row['cleanup_attempts']==['signal_anchored_group','wait_original_handle','observe_group_empty_readonly','selector_close','stdout_close','stderr_close'],'independent normal cleanup sequence')
```

## build.py

```diff
--- T270-accepted/build.py
+++ T272/build.py
@@ -1,5 +1,5 @@
 """T167 candidate builder. Preparation plans are pure; real tools need MAIN pins."""
-import argparse,json,os,time
+import argparse,errno,json,os,time
 from pathlib import Path
 import stage
 ROOT=stage.ROOT
@@ -204,6 +204,10 @@
     def signal_owned():
      try:self.fx.kill(child,persistence_check);row['group_signal']='SIGKILL_SENT_WHILE_ANCHORED'
      except ProcessLookupError:row['group_signal']='ESRCH_WHILE_ANCHORED'
+     except PermissionError as e:
+      if e.errno!=errno.EPERM:raise
+      row['group_signal']='EPERM_DENIED_WHILE_ANCHORED'
+      if not stage.exit0_observation(row['nonreaping'],child.pid):raise
     cleanup('signal_anchored_group',signal_owned)
     try:row['native_last']=self.fx.native_last(child)
     except BaseException as e:secondary('capture_cleanup_native_last',e)
@@ -220,6 +224,7 @@
    row['timed_out']=row['timed_out'] or self.expired or self.fx.clock()>=end
    if row['timed_out']:primary('original deadline crossed')
    if row['exit']!=0 or not reaped or row['group_empty'] is not True:primary('nonzero/unreaped/unresolved group closure')
+   if row['group_signal']=='EPERM_DENIED_WHILE_ANCHORED' and not (stage.exit0_observation(row['nonreaping'],row['pid']) and type(row['exit']) is int and row['exit']==0 and reaped and row['group_empty'] is True):primary('EPERM denial lacks confirmed original exit0/reap0/empty group')
    if row['nonreaping'] is not None:
     expected=row['nonreaping']['status'] if row['nonreaping']['code']==1 else -row['nonreaping']['status']
     if row['exit']!=expected:primary('nonreaping observation differs from original-handle wait')
```

## test_preparation.py

```diff
--- T270-accepted/test_preparation.py
+++ T272/test_preparation.py
@@ -171,12 +171,12 @@
   package+=sorted(stage.FRAMEWORK+'/'+n for n,v in self.view.framework().items() if v['kind']=='file')
   package+=sorted(str(p.relative_to(root)) for p in (root/stage.ASSET_ROOT).rglob('*') if p.is_file())
   entries=[{'path':n,'bytes':(root/n).stat().st_size,'sha256':stage.sha((root/n).read_bytes()),'mode':(root/n).stat().st_mode&0o7777} for n in sorted(set(package))]
-  self.put(stage.MANIFEST,stage.canonical_json({'schema_version':1,'kind':'SOURCE_INPUT_MANIFEST','source_revision':'1'*40,'entries':entries}).encode())
-  inputs={self.root+'/'+x['path']:x['sha256'] for x in entries};inputs[self.root+'/'+stage.MANIFEST]=self.view.hash(self.root+'/'+stage.MANIFEST)
+  self.put(stage.manifest_path(self.ident),stage.canonical_json({'schema_version':1,'kind':'SOURCE_INPUT_MANIFEST','source_revision':'1'*40,'entries':entries}).encode())
+  inputs={self.root+'/'+x['path']:x['sha256'] for x in entries};inputs[self.root+'/'+stage.manifest_path(self.ident)]=self.view.hash(self.root+'/'+stage.manifest_path(self.ident))
   inputs.update({n:self.view.hash(n) for n in self.external if self.view.ordinary(n) or n in stage.TOOLS.values()})
   sdk={n[len(stage.SDK)+1:]:h for n,h in inputs.items() if n.startswith(stage.SDK+'/')}
   accepted={'ticket':'T163',**{k:{'path':n,'sha256':self.reference_pins[k]} for k,n in stage.SOURCE_REFERENCES.items()},'files':[{'path':n,'bytes':(root/n).stat().st_size,'sha256':self.source_pins[n],'mode':0o644} for n in sorted(stage.SOURCE_HASHES)]}
-  self.auth={'schema_version':1,'kind':'BLACKWOOD_NATIVE_BUILD_AUTHORIZATION','authority':'MAIN','status':'ACCEPTED','execution_release':'EXPLICIT_BLACKWOOD_NATIVE_BUILD_EXECUTION','recipe':stage.RECIPE,'ticket':'FIXTURE_ONLY_NOT_REAL_AUTHORITY','candidate_id':self.ident,'decision':'notes/decisions/FIXTURE_ONLY.md','source_revision':'1'*40,'source_manifest':{'path':stage.MANIFEST,'sha256':self.view.hash(self.root+'/'+stage.MANIFEST)},'source_acceptance':accepted,'bindings':{'repository':self.root,'system_sdk':stage.SDK,'source_framework':self.root+'/'+stage.FRAMEWORK},'observation':{'inputs':inputs,'preservation':self.view.preservation(),'source_framework':self.view.framework(),'units':{'cpp':list(stage.CPP),'c':list(stage.C)},'tools':{k:{'path':n,'sha256':self.tool_pins[k]} for k,n in stage.TOOLS.items()},'system_sdk':{'root':stage.SDK,'files':sdk},'flags':{m:stage.flags(self.root,self.ident,m) for m in ('release','debug')},'errors':[],'map_seed':stage.map_declaration(self.view)}}
+  self.auth={'schema_version':1,'kind':'BLACKWOOD_NATIVE_BUILD_AUTHORIZATION','authority':'MAIN','status':'ACCEPTED','execution_release':'EXPLICIT_BLACKWOOD_NATIVE_BUILD_EXECUTION','recipe':stage.RECIPE,'ticket':'FIXTURE_ONLY_NOT_REAL_AUTHORITY','candidate_id':self.ident,'decision':'notes/decisions/FIXTURE_ONLY.md','source_revision':'1'*40,'source_manifest':{'path':stage.manifest_path(self.ident),'sha256':self.view.hash(self.root+'/'+stage.manifest_path(self.ident))},'source_acceptance':accepted,'bindings':{'repository':self.root,'system_sdk':stage.SDK,'source_framework':self.root+'/'+stage.FRAMEWORK},'observation':{'inputs':inputs,'preservation':self.view.preservation(),'source_framework':self.view.framework(),'units':{'cpp':list(stage.CPP),'c':list(stage.C)},'tools':{k:{'path':n,'sha256':self.tool_pins[k]} for k,n in stage.TOOLS.items()},'system_sdk':{'root':stage.SDK,'files':sdk},'flags':{m:stage.flags(self.root,self.ident,m) for m in ('release','debug')},'errors':[],'map_seed':stage.map_declaration(self.view)}}
   self.write()
  def put(self,name,data=b'FIXTURE_ONLY\n',mode=0o644):
   p=Path(self.root)/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);p.chmod(mode);return p
@@ -303,6 +303,7 @@
   self.fault('observe_exit');check();assert c is self.child;data=struct.pack('<iiiiIi',20,0,1,c.pid,501,0)+bytes(80);self.last={'pid':c.pid,'result':0,'errno':0,'record_bytes':104,'record_hex':data.hex()};return {'pid':c.pid,'signo':20,'code':1,'status':0,'errno':0}
  def kill(self,c,check):
   self.fault('kill');check();assert c is self.child
+  if self.f.fx_fault=='anchored_eperm':raise PermissionError(errno.EPERM,'FIXTURE_ONLY anchored signal denied')
   if self.f.fx_fault=='kill_esrch':raise ProcessLookupError(errno.ESRCH,'FIXTURE_ONLY ESRCH')
   if self.f.fx_fault in ('kill_error','combined'):raise PermissionError('FIXTURE_ONLY kill denied')
  def wait(self,c,timeout):
@@ -764,6 +765,71 @@
      refused(f.gate);assert stage.protected_inventory(f.root)[str(base)]!=protected[str(base)]
     f.case_observation={'variant':variant,'tree_rows':rows,'fixture_content_reads':0,'new_physical_files':'READABLE; special/unreadable/link metadata INJECTED'}
   add('D453_'+variant,tree_case)
+ for variant in ('confirmed_empty','live_group','unknown_group','group_error','reap_error','reap_unknown','reap_nonzero','missing_observation','nonzero_observation','wrong_pid','unexpected_errno','other_error','deadline','log_failure','receipt_failure','strict_ledger'):
+  def eperm_case(f,variant=variant):
+   f.gate();f.view.declared_inputs=f.auth['observation']['inputs'];base=Path(f.root)/'capture';(base/'logs').mkdir(parents=True);(base/'tmp').mkdir();fx=FakeOps(f);f.fx_fault='anchored_eperm';runner=build.Runner(f.root,base,fx=fx,view=f.view)
+   group=fx.group_empty;wait=fx.wait;observe=fx.observe_exit;close=fx.close;persist=fx.persist
+   if variant in ('live_group','unknown_group','group_error','deadline'):
+    def group_result(child):
+     value=group(child)
+     if variant=='group_error':raise OSError('FIXTURE_ONLY unresolved group')
+     if variant=='deadline':fx.at=121;return value
+     return False if variant=='live_group' else None
+    fx.group_empty=group_result
+   if variant.startswith('reap_'):
+    def reap(child,timeout):
+     wait(child,timeout)
+     if variant=='reap_error':raise RuntimeError('FIXTURE_ONLY failed reap')
+     return None if variant=='reap_unknown' else 1
+    fx.wait=reap
+   if variant in ('missing_observation','nonzero_observation','wrong_pid'):
+    def terminal(child,check):
+     if variant=='missing_observation':raise stage.Refused('FIXTURE_ONLY missing terminal observation')
+     row=observe(child,check);row['status' if variant=='nonzero_observation' else 'pid']+=1;return row
+    fx.observe_exit=terminal
+   if variant=='unexpected_errno':
+    def denied(child,check):fx.calls.append('kill');check();assert child is fx.child;raise PermissionError(errno.EACCES,'FIXTURE_ONLY unexpected denial')
+    fx.kill=denied
+   if variant=='other_error':
+    def closing(value):
+     close(value)
+     if isinstance(value,Selector):raise RuntimeError('FIXTURE_ONLY unrelated cleanup error')
+    fx.close=closing
+   if variant in ('log_failure','receipt_failure'):
+    def publication(base,name,data,check):
+     if name.endswith('.stdout' if variant=='log_failure' else '.receipt.json'):raise OSError('FIXTURE_ONLY publication failure')
+     return persist(base,name,data,check)
+    fx.persist=publication
+   okay=variant in ('confirmed_empty','strict_ledger')
+   if okay:runner.run('compiler_identity',[stage.TOOLS['cc'],'--version'])
+   else:refused(lambda:runner.run('compiler_identity',[stage.TOOLS['cc'],'--version']))
+   row=runner.records[0];assert (row['status']=='PASS')==okay and fx.calls.count('kill')==1 and fx.calls.count('wait')==1
+   assert fx.calls.index('kill')<fx.calls.index('wait')
+   if okay:
+    assert row['group_signal']=='EPERM_DENIED_WHILE_ANCHORED' and row['secondary']==[] and row['child_reaped'] and row['exit']==0 and row['group_empty'] is True
+    stage.validate_step(row,0,'compiler_identity',[stage.TOOLS['cc'],'--version'],runner.env)
+   if variant=='strict_ledger':
+    for field,value in (('group_empty',None),('exit',None),('child_reaped',False),('nonreaping',None),('group_signal','EPERM_ASSUMED_EMPTY'),('secondary',[{'action':'x','error':'other'}])):
+     changed=copy.deepcopy(row);changed[field]=value;refused(lambda:stage.validate_step(changed,0,'compiler_identity',[stage.TOOLS['cc'],'--version'],runner.env))
+   f.case_observation={'variant':variant,'record':row,'fake_calls':fx.calls,'actual_signal':False}
+  add('D456_eperm_'+variant,eperm_case)
+ def eperm_pipeline(f):
+  f.fx_fault='anchored_eperm';record=f.pipeline();assert record['status']=='BLACKWOOD_NATIVE_LINKED_NOT_RUN',record['errors'];assert len(record['steps'])==126 and all(row['group_signal']=='EPERM_DENIED_WHILE_ANCHORED' for row in record['steps'])
+  assert f.check()['status']=='VERIFIED_BUILD_ONLY_NOT_RUN';f.case_observation={'denial_steps':126,'independent_verifier':'PASS','actual_process':False}
+ add('D456_complete_eperm_build_and_verifier',eperm_pipeline)
+ for variant in ('binding','wrong_candidate','legacy','self_reference','invalid_id'):
+  def manifest_case(f,variant=variant):
+   f.gate();path=stage.manifest_path(f.ident);assert path=='web/repro/blackwood-source-manifests/'+f.ident+'.json'
+   if variant=='binding':
+    old=f.put('web/repro/blackwood-source-manifest.json',b'FIXTURE_ONLY_PRESERVED_OLD');f.auth['observation']['preservation']=f.view.preservation();f.write();f.gate();assert old.read_bytes()==b'FIXTURE_ONLY_PRESERVED_OLD'
+   elif variant=='invalid_id':
+    for ident in ('../bad','',True):refused(lambda ident=ident:stage.manifest_path(ident))
+   elif variant=='self_reference':
+    manifest=Path(f.root)/path;doc=stage.loads(manifest.read_bytes());doc['entries'].append({'path':path,'bytes':manifest.stat().st_size,'sha256':stage.sha(manifest.read_bytes()),'mode':0o644});doc['entries'].sort(key=lambda row:row['path']);manifest.write_text(stage.canonical_json(doc));h=stage.sha(manifest.read_bytes());f.auth['source_manifest']['sha256']=h;f.auth['observation']['inputs'][str(manifest)]=h;f.write();refused(f.gate)
+   else:
+    f.auth['source_manifest']['path']=stage.manifest_path('OTHER_CANDIDATE') if variant=='wrong_candidate' else 'web/repro/blackwood-source-manifest.json';f.write();refused(f.gate)
+   assert not f.tool_calls and not f.output().exists();f.case_observation={'variant':variant,'derived_manifest':path,'actual_manifest_write':False}
+  add('D456_manifest_'+variant,manifest_case)
  return rows
 
 def main():
```

## SCHEMA.md

```diff
--- T270-accepted/SCHEMA.md
+++ T272/SCHEMA.md
@@ -1,12 +1,12 @@
 # Blackwood native preparation schema
 
-Authority: accepted prior preparations plus T2701.0/D453, BLACKWOOD_NATIVE_BUILD_PREPARATION0.4, with D235's fixed Darwin nonreaping adapter. Source and guarded SIMULATED preparation only. No current actual plan/build/verify/tool/signing/copy/runtime authority.
+Authority: accepted prior preparations plus T2721.0/D456, BLACKWOOD_NATIVE_BUILD_PREPARATION0.5, with D235's fixed Darwin nonreaping adapter. Source and guarded SIMULATED preparation only. No current actual plan/build/verify/tool/signing/copy/runtime authority.
 
 Every object below has exactly the named fields. Maps have the constrained key/value types stated below, not extension dictionaries. Unknown fields, duplicate JSON keys, nonfinite floats, bool-as-int, noncanonical paths, aliases and overlaps refuse. Generated JSON is sorted-key, indented two spaces, ASCII, LF terminated, with finite numbers. Control/manifest/plan ceilings are32MiB; report/freeze128MiB. Byte counts and integer metadata are nonnegative integers excluding bool; digests are64 lowercase hexadecimal characters. File reads require ordinary single-link data and ordinary ancestors, except the explicitly named installed launcher roles. Successful reports/verification cannot contain partial/null records.
 
 Canonical relative paths have no empty, dot, dot-dot, backslash, leading slash or control-character component. Absolute paths have one leading slash and the same normalized components. IDs match `[A-Za-z0-9_-]{1,48}`. Repository comes only from this installed module home. No root/tool/SDK/map/flags/environment selector exists.
 
-`Claims` is exactly `{native_runtime:false,gameplay:false,multiplayer:false,authority:false,P0:false}`. `FileRef` is exactly `{path:relative,bytes:uint,sha256:SHA,mode:420|493}`. Source manifest is exactly `{schema_version:1,kind:"SOURCE_INPUT_MANIFEST",source_revision:40hex,entries:[FileRef...]}` with sorted unique paths and no self entry; its only successor location is `web/repro/blackwood-source-manifest.json`. Every entry is checked, even if broader browser/docs provenance rather than native consumption. No worker authors that MAIN file.
+`Claims` is exactly `{native_runtime:false,gameplay:false,multiplayer:false,authority:false,P0:false}`. `FileRef` is exactly `{path:relative,bytes:uint,sha256:SHA,mode:420|493}`. Source manifest is exactly `{schema_version:1,kind:"SOURCE_INPUT_MANIFEST",source_revision:40hex,entries:[FileRef...]}` with sorted unique paths and no self entry; its only successor location is `web/repro/blackwood-source-manifests/CANDIDATE_ID.json`. Every entry is checked, even if broader browser/docs provenance rather than native consumption. No worker authors that MAIN file.
 
 `SourceAcceptance` is exactly `{ticket:"T163",decision:Reference,handoff:Reference,evidence:Reference,files:[FileRef x4]}`. `Reference` is exactly `{path:relative,sha256:SHA}`. The three fixed D223/final-handoff/MAIN-review paths and digests and four sorted source files/hashes are literal stage.py constants from approved BLACKWOOD_BUILD_PREPARATION0.1. All source sizes/modes/current bytes are checked. Native does not have to consume the browser-only private header. Fixture subclasses replace source DATA identities solely inside guarded fakes and remain barred from real authorization.
 
@@ -82,3 +82,7 @@
 The optional receipt slot is independently bound despite its inventory exclusion. Current ordinary0644/single-link file identity includes device/inode/size/mtime/ctime/mode. Existing identity/presence must remain stable through final full observations; absent slots cannot be created unexpectedly. After an explicitly requested durable publication, the new identity becomes the expected one. Every final boundary checks exact reconstructed canonical bytes, ordinary identity, and requested presence AFTER lengthy original/owned observations. Late creation, same-byte replacement or deletion refuses, for default and explicit receipt cases. The initial/current full original forest includes the fixed native SDK as well as original project/browser-SDK forests; opaque old links are never consumed grants.
 
 The fixed backend also requires default SIGCHLD disposition, performs a fresh nonreaping original-child ownership check immediately before a mutating group signal, and treats ECHILD/malformed ownership as lost anchor. No signal or reap follows anchor loss. Its bounded original `Popen.wait` uses that pinned Python instance's `_try_wait` hook solely to propagate ECHILD instead of Python's optimistic exit0 fallback; fixed WNOHANG waits name only the retained original child. The instance hook is restored as a memory operation, never an extra wait. Guarded actual-backend methods cover anchored cleanup, ECHILD before signal, ECHILD during wait and nondefault SIGCHLD without real OS effects. Unreaped child handles and ambiguous/expired pipe/selector resources are strongly retained, with no automatic retry.
+
+D456 adds successful-step group_signal `EPERM_DENIED_WHILE_ANCHORED` as an explicit signal denial. It never means a sent signal or inferred group absence. Success still requires a prior exact typed original-child exit0 observation, original-handle reap returning integer0, independent positive group_empty:true, all original cleanup/publication/closure/deadline checks, no primary/secondary/output/I/O error. PermissionError with any other errno fails; missing/failed/wrong-child terminal observations and unknown/live groups fail. The denial enum remains in raw receipt and final ledger; verifier reconstructs the same strict success facts. No signal retry, post-reap mutation, PID discovery or extra grace is introduced. RealOps backend is unchanged.
+
+Source manifest Reference.path is exactly `web/repro/blackwood-source-manifests/` + validated candidate ID + `.json`, derived by stage.manifest_path. Wrong candidate and legacy/global manifest inputs refuse. Source entries cannot include the active manifest itself, preventing a self-hash cycle. No new path/CLI selector is added. The earlier singleton `web/repro/blackwood-source-manifest.json` and all historical controls/failed attempts remain unchanged; future attempts get fresh candidate-bound identities.
```

## README.md

```diff
--- T270-accepted/README.md
+++ T272/README.md
@@ -15,7 +15,7 @@
 verify.py --candidate-id ID --pins ABS_MAIN_JSON --pins-sha256 SHA [--receipt ABS_OWNED_PATH]
 ```
 
-Future attempt is web/server/blackwood-candidate-attempts/ID; preparation never creates it. A future plan-only call rejects execution pins and exclusively writes its inert new preparation-ID/plan.json, with explicit pending controls, never an actual attempt/tool probe. MAIN authors web/repro/blackwood-source-manifest.json after both preparations are accepted. Old manifests/attempts/builders/frameworks/assets remain immutable.
+Future attempt is web/server/blackwood-candidate-attempts/ID; preparation never creates it. A future plan-only call rejects execution pins and exclusively writes its inert new preparation-ID/plan.json, with explicit pending controls, never an actual attempt/tool probe. MAIN authors web/repro/blackwood-source-manifests/CANDIDATE_ID.json after both preparations are accepted. Old manifests/attempts/builders/frameworks/assets remain immutable.
 
 The native recipe remains8 C++ +8 ENet C units in actual Makefile order, release/debug32 fresh objects, exact arm64/CLT15.5/language/optimization/include/STANDALONE flags and2 owned RPATHs. Exactly126 future version/sign/inspection/prescan/compile/link commands; the independent verifier's20 read-only inspectors require another explicit future invocation. Actual pre/post dependency and linker closure/source/header/launcher checks are mandatory; no old object reuse, browser define, tool fallback or historical token exception.
 
@@ -44,3 +44,5 @@
 D238: command-associated durability retains the original command/whole cutoff through each unbuffered write/sync/release. Expired raw descriptors are strongly retained as SKIPPED_EXPIRED; ambiguous close errors are UNRESOLVED_CLOSE_ERROR and never retried. Only separate outer FAILED evidence can use remaining original whole time, with refusal preserved. No new close/durability step is started after the command cutoff. D236: exact optional receipt content, ordinary identity and requested presence are checked after final full observations, even though the slot is excluded from the freeze inventory. These paths have explicit fake-clock/late-slot cases. No guarded pass was in flight while applying these source corrections.
 
 Physical framework copying uses the actual new bounded byte/mode/link copier against fake files in preparation; guards still deny any original framework/SDK path or library copy helper. Default SIGCHLD and fixed nonreaping ownership are rechecked before group mutation, and ECHILD cannot become a successful original-handle reap. The pinned Popen instance hook closes its exit0 fallback only, without a new child command or generic wait selector. Preparation facts never establish actual Darwin ABI/tool support.
+
+T2721.0/D456 under preparation0.5 records anchored signal EPERM explicitly and permits success only after prior original exit0, actual original reap0, positive empty-group observation and every other successful-step obligation. All other denial/unknown/live/reap/observation/publication/deadline faults still refuse. No retry/post-reap signal/backend change follows. Manifest paths now derive from each validated candidate ID under web/repro/blackwood-source-manifests/. New attempts reject the old singleton and wrong-ID manifests or self-reference. Existing singleton/control/visible-native-1 artifacts are preserved. Targeted guarded pass10 is source/simulation only; no actual signal/tool/build or attempt retry.
```
