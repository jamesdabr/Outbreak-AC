# T273 six-file source diffs

Baseline: accepted T272 pass10 snapshots. Canonical record schema/commands/cleanup unchanged.

## stage.py

```diff
--- T272-accepted/stage.py
+++ T273/stage.py
@@ -7,6 +7,13 @@
 SDK_PTHREAD_ALIAS=(SDK+'/usr/include/pthread.h','pthread/pthread.h',0o755,SDK+'/usr/include/pthread/pthread.h')
 SDK_SCHED_ALIAS=(SDK+'/usr/include/sched.h','pthread/sched.h',0o755,SDK+'/usr/include/pthread/sched.h')
 SDK_HEADER_ALIASES=(SDK_PTHREAD_ALIAS,SDK_SCHED_ALIAS)
+SDK_LINK_ALIASES={
+ SDK+'/usr/lib/'+leaf:(SDK+'/usr/lib/'+target,tuple((SDK+'/usr/lib/'+edge,raw) for edge,raw in edges))
+ for leaf,target,edges in (
+ ('libc++.tbd','libc++.1.tbd',(('libc++.tbd','libc++.1.tbd'),)),
+ ('libz.tbd','libz.1.tbd',(('libz.tbd','libz.1.tbd'),)),
+ ('libSystem.tbd','libSystem.B.tbd',(('libSystem.tbd','libSystem.B.tbd'),)),
+ ('libpthread.tbd','libSystem.B.tbd',(('libpthread.tbd','libSystem.tbd'),('libSystem.tbd','libSystem.B.tbd'))))}
 CLT='/Library/Developer/CommandLineTools'
 PYTHON='/Library/Frameworks/Python.framework/Versions/3.11'
 FRAMEWORK='source/xcode/Frameworks/SDL2.framework'
@@ -221,6 +228,19 @@
  need(digest(inputs[target])==digest(sdk_files[relative])==view.hash(target),'SDK header target bytes changed')
  return target
 
+def sdk_link_path(view,path):
+ """D462 fixed linker spellings only; never adopt a discovered alias."""
+ absolute(path)
+ if path not in SDK_LINK_ALIASES:
+  physical=view.canonical(path);need(path==physical,'unknown external linker alias');return physical
+ target,edges=SDK_LINK_ALIASES[path]
+ for alias,raw in edges:
+  need(view.ordinary_ancestors(alias) and view.link_identity(alias)=={'target':raw,'mode':0o755},'fixed SDK linker edge text/mode/type changed')
+ need(view.ordinary_ancestors(target) and view.ordinary(target) and view.canonical(target)==target and view.canonical(path)==target,'SDK linker target must remain canonical ordinary single-link')
+ relative=target[len(SDK)+1:]
+ need(target in view.declared_inputs and relative in view.sdk_files and digest(view.declared_inputs[target])==digest(view.sdk_files[relative])==view.hash(target),'SDK linker canonical target declaration/hash changed')
+ return target
+
 def authorize(data,expected_sha,ident,view,existing=False,verify_preservation=True):
  need(sha(data)==digest(expected_sha),'authorization digest mismatch');p=loads(data);root=view.root;identifier(ident)
  exact(p,['schema_version','kind','authority','status','execution_release','recipe','ticket','candidate_id','decision','source_revision','source_manifest','bindings','source_acceptance','observation'],'authorization fields')
```

## build.py

```diff
--- T272-accepted/build.py
+++ T273/build.py
@@ -279,7 +279,7 @@
   elif stage.beneath(physical,copy):
    name=physical[len(copy)+1:];stage.need(name in signed and signed[name]['kind']=='file' and view.hash(physical)==signed[name]['sha256'],'unknown/changed staged linker input');origin='OWN_SIGNED_FRAMEWORK'
   else:
-   stage.need(path==physical and stage.beneath(physical,stage.CLT) and physical in view.declared_inputs and view.hash(physical)==view.declared_inputs[physical],'undeclared/changed/non-SDK linker input');origin=physical
+   stage.need(stage.sdk_link_path(view,path)==physical and stage.beneath(physical,stage.CLT) and physical in view.declared_inputs and view.hash(physical)==view.declared_inputs[physical],'undeclared/changed/non-SDK linker input');origin=physical
   if physical not in files:files[physical]={'origin':origin,'sha256':view.hash(physical),'archive_members':[]}
   if member and member not in files[physical]['archive_members']:files[physical]['archive_members'].append(member)
  stage.need(set(objects)<=set(files),'linker trace missing fresh objects')
```

## verify.py

```diff
--- T272-accepted/verify.py
+++ T273/verify.py
@@ -96,7 +96,7 @@
    if physical in objects:origin='OWN_FRESH_OBJECT'
    elif stage.beneath(physical,str(copy)):
     item=record['stage_after'].get(physical[len(str(copy))+1:]);stage.need(item and item['kind']=='file' and view.hash(physical)==item['sha256'],'copied link file');origin='OWN_SIGNED_FRAMEWORK'
-   else:stage.need(path==physical and stage.beneath(physical,stage.CLT) and physical in view.declared_inputs and view.hash(physical)==view.declared_inputs[physical],'unlisted actual linker dependency');origin=physical
+   else:stage.need(stage.sdk_link_path(view,path)==physical and stage.beneath(physical,stage.CLT) and physical in view.declared_inputs and view.hash(physical)==view.declared_inputs[physical],'unlisted actual linker dependency');origin=physical
    if physical not in actual:actual[physical]={'origin':origin,'sha256':view.hash(physical),'archive_members':[]}
    if match and match.group(2) not in actual[physical]['archive_members']:actual[physical]['archive_members'].append(match.group(2))
   stage.need(actual==m['link_inputs'] and objects<=set(actual) and str(copy/'Versions/A/SDL2') in actual and any(stage.beneath(p,stage.SDK+'/usr/lib') for p in actual),'actual link trace inventory differs')
```

## test_preparation.py

```diff
--- T272-accepted/test_preparation.py
+++ T273/test_preparation.py
@@ -155,12 +155,14 @@
   self.put('web/server/history/opaque-parent/keep')
   (root/'web/server/history/opaque-parent/opaque').symlink_to('/FIXTURE_ONLY/nonexistent/outside')
   for path in [*stage.TOOLS.values(),stage.CLT+'/usr/bin/clang',stage.CLT+'/usr/bin/ld',stage.CLT+'/usr/lib/clang/17/include/stddef.h',stage.CLT+'/usr/lib/clang/17/lib/darwin/libclang_rt.osx.a',stage.PYTHON+'/bin/python3.11']:self.ext(path,b'FIXTURE_ONLY_TOOL',0o755)
-  for path in ['SDKSettings.json','usr/include/zlib.h','usr/include/pthread/pthread.h','usr/include/pthread/sched.h','usr/lib/libz.tbd','usr/lib/libpthread.tbd','usr/lib/libc++.1.tbd']:self.ext(stage.SDK+'/'+path,b'{"Version":"15.5"}' if path=='SDKSettings.json' else b'FIXTURE_ONLY_SDK')
+  for path in ['SDKSettings.json','usr/include/zlib.h','usr/include/pthread/pthread.h','usr/include/pthread/sched.h','usr/lib/libz.1.tbd','usr/lib/libSystem.B.tbd','usr/lib/libc++.1.tbd']:self.ext(stage.SDK+'/'+path,b'{"Version":"15.5"}' if path=='SDKSettings.json' else b'FIXTURE_ONLY_SDK')
   for name in stage.ADAPTER_HEADER_PINS:self.ext(stage.SDK+'/usr/include/'+name,b'FIXTURE_ONLY_D235_HEADER')
   for name in stage.ADAPTER_STDLIB_ROLES:self.ext(name,b'FIXTURE_ONLY_LAZY_CTYPES')
   self.sdk_root=root/'EXTERNAL/SDK'
   for name,raw,mode,_ in stage.SDK_HEADER_ALIASES:
    p=self.sdk_root/name[len(stage.SDK)+1:];p.symlink_to(raw);os.lchmod(p,mode);self.external[name]=p
+  for alias,(_,edges) in stage.SDK_LINK_ALIASES.items():
+   raw=next(raw for edge,raw in edges if edge==alias);p=self.sdk_root/alias[len(stage.SDK)+1:];p.symlink_to(raw);os.lchmod(p,0o755);self.external[alias]=p
   # Exercise legitimate multi-hardlink installed launchers at their exact virtual roles.
   anchor=self.external[stage.TOOLS['cc']]
   for role in ('cxx','otool'):
@@ -345,7 +347,7 @@
    if f.action_fault=='rpath':paths[0]='/FIXTURE_ONLY/old'
    binary.write_bytes(macho(2,paths));binary.chmod(0o755);objects=[x for x in argv if x.endswith('.o')]
    if f.action_fault=='link_missing_object':objects.pop()
-   out='\n'.join(objects+[str(base/'deps-signed/SDL2.framework/Versions/A/SDL2'),stage.SDK+'/usr/lib/libz.tbd',stage.SDK+'/usr/lib/libpthread.tbd',stage.SDK+'/usr/lib/libc++.1.tbd',stage.CLT+'/usr/lib/clang/17/lib/darwin/libclang_rt.osx.a(FIXTURE_ONLY.o)'])+'\n'
+   out='\n'.join(objects+[str(base/'deps-signed/SDL2.framework/Versions/A/SDL2'),stage.SDK+'/usr/lib/libz.tbd',stage.SDK+'/usr/lib/libpthread.tbd',stage.SDK+'/usr/lib/libc++.tbd',stage.SDK+'/usr/lib/libSystem.tbd',stage.CLT+'/usr/lib/clang/17/lib/darwin/libclang_rt.osx.a(FIXTURE_ONLY.o)'])+'\n'
   elif tool==stage.TOOLS['file']:out='Mach-O 64-bit '+('object' if argv[-1].endswith('.o') else 'executable' if argv[-1].endswith('/ac_server') else 'dynamically linked shared library')+' arm64 FIXTURE_ONLY\n'
   elif tool==stage.TOOLS['otool']:
    p=argv[-1];out=p+':\n'
@@ -830,6 +832,60 @@
     f.auth['source_manifest']['path']=stage.manifest_path('OTHER_CANDIDATE') if variant=='wrong_candidate' else 'web/repro/blackwood-source-manifest.json';f.write();refused(f.gate)
    assert not f.tool_calls and not f.output().exists();f.case_observation={'variant':variant,'derived_manifest':path,'actual_manifest_write':False}
   add('D456_manifest_'+variant,manifest_case)
+ def alias_success(f):
+  f.gate();f.view.declared_inputs=f.auth['observation']['inputs']
+  for alias,(target,edges) in stage.SDK_LINK_ALIASES.items():
+   assert stage.sdk_link_path(f.view,alias)==target and stage.sdk_link_path(f.view,target)==target
+  f.case_observation={'fixed_aliases':4,'canonical_targets':3,'result':'PASS'}
+ add('D462_exact_aliases_and_canonical_targets',alias_success)
+ def alias_edges(f):
+  f.gate();f.view.declared_inputs=f.auth['observation']['inputs'];count=0
+  for alias,(_,edges) in stage.SDK_LINK_ALIASES.items():
+   for edge,raw in edges:
+    p=f.view.mapped(edge)
+    for mutation in ('text','mode','type','missing'):
+     if mutation=='mode':os.lchmod(p,0o700)
+     else:
+      p.unlink()
+      if mutation=='text':p.symlink_to('./'+raw);os.lchmod(p,0o755)
+      elif mutation=='type':p.write_bytes(b'FIXTURE_ONLY_SDK')
+     refused(lambda:stage.sdk_link_path(f.view,alias));count+=1
+     if p.exists() or p.is_symlink():p.unlink()
+     p.symlink_to(raw);os.lchmod(p,0o755)
+  f.case_observation={'exact_edge_mutations_refused':count}
+ add('D462_edge_text_mode_type_missing',alias_edges)
+ def alias_targets(f):
+  f.gate();f.view.declared_inputs=f.auth['observation']['inputs'];count=0
+  for alias,(target,_) in stage.SDK_LINK_ALIASES.items():
+   p=f.view.mapped(target);data=p.read_bytes();relative=target[len(stage.SDK)+1:]
+   p.write_bytes(b'FIXTURE_ONLY_CHANGED');refused(lambda:stage.sdk_link_path(f.view,alias));p.write_bytes(data);count+=1
+   extra=p.with_name('FIXTURE_ONLY_HARDLINK');os.link(p,extra);refused(lambda:stage.sdk_link_path(f.view,alias));extra.unlink();count+=1
+   p.rename(extra);p.symlink_to(extra.name);refused(lambda:stage.sdk_link_path(f.view,alias));p.unlink();extra.rename(p);count+=1
+   h=f.view.declared_inputs.pop(target);refused(lambda:stage.sdk_link_path(f.view,alias));f.view.declared_inputs[target]=h;count+=1
+   h=f.view.sdk_files.pop(relative);refused(lambda:stage.sdk_link_path(f.view,alias));f.view.sdk_files[relative]=h;count+=1
+   h=f.view.sdk_files[relative];f.view.sdk_files[relative]='0'*64;refused(lambda:stage.sdk_link_path(f.view,alias));f.view.sdk_files[relative]=h;count+=1
+  f.case_observation={'target_hash_link_and_declaration_refusals':count}
+ add('D462_target_hash_type_links_declarations',alias_targets)
+ def alias_unknown(f):
+  f.gate();f.view.declared_inputs=f.auth['observation']['inputs'];unknown=stage.SDK+'/usr/lib/UNKNOWN.tbd';p=f.view.mapped(unknown);p.symlink_to('libc++.1.tbd');os.lchmod(p,0o755);refused(lambda:stage.sdk_link_path(f.view,unknown));p.unlink()
+  leaf=stage.SDK+'/usr/lib/libpthread.tbd';p=f.view.mapped(leaf);p.unlink();p.symlink_to('EXTRA_HOP.tbd');hop=p.with_name('EXTRA_HOP.tbd');hop.symlink_to('libSystem.tbd');os.lchmod(p,0o755);os.lchmod(hop,0o755);refused(lambda:stage.sdk_link_path(f.view,leaf))
+  f.case_observation={'unknown_same_target_alias':'REFUSED','extra_hop_same_canonical_target':'REFUSED'}
+ add('D462_unknown_alias_and_extra_hop',alias_unknown)
+ def alias_intermediate(f):
+  f.gate();f.view.declared_inputs=f.auth['observation']['inputs'];leaf=stage.SDK+'/usr/lib/libpthread.tbd';middle=f.view.mapped(stage.SDK+'/usr/lib/libSystem.tbd');assert os.readlink(f.view.mapped(leaf))=='libSystem.tbd'
+  middle.unlink();middle.symlink_to('./libSystem.B.tbd');os.lchmod(middle,0o755);refused(lambda:stage.sdk_link_path(f.view,leaf));middle.unlink();middle.symlink_to('libSystem.B.tbd');os.lchmod(middle,0o755)
+  parent=middle.parent;other=parent.with_name('FIXTURE_ONLY_LIB_MOVED');parent.rename(other);parent.symlink_to(other.name,target_is_directory=True);refused(lambda:stage.sdk_link_path(f.view,leaf))
+  f.case_observation={'pthread_intermediate_raw_edge':'REFUSED_WHEN_CHANGED','symlink_ancestor':'REFUSED'}
+ add('D462_pthread_intermediate_and_ancestors',alias_intermediate)
+ def alias_trace(f):
+  record=f.pipeline();assert record['status']=='BLACKWOOD_NATIVE_LINKED_NOT_RUN',record['errors']
+  for mode in ('release','debug'):
+   inputs=record['modes'][mode]['link_inputs'];assert not set(stage.SDK_LINK_ALIASES)&set(inputs)
+   assert {target for target,_ in stage.SDK_LINK_ALIASES.values()}<=set(inputs)
+   for target,_ in stage.SDK_LINK_ALIASES.values():assert inputs[target]['origin']==target
+   index=record['modes'][mode]['link_step'];trace=(f.output()/f'logs/{index:03d}.stdout').read_text();assert all(alias in trace.splitlines() for alias in stage.SDK_LINK_ALIASES)
+  assert f.check()['status']=='VERIFIED_BUILD_ONLY_NOT_RUN';f.case_observation={'four_alias_raw_trace':'PASS','canonical_record_format':'UNCHANGED','independent_verifier':'PASS'}
+ add('D462_complete_alias_trace_canonical_records',alias_trace)
  return rows
 
 def main():
```

## SCHEMA.md

```diff
--- T272-accepted/SCHEMA.md
+++ T273/SCHEMA.md
@@ -1,6 +1,6 @@
 # Blackwood native preparation schema
 
-Authority: accepted prior preparations plus T2721.0/D456, BLACKWOOD_NATIVE_BUILD_PREPARATION0.5, with D235's fixed Darwin nonreaping adapter. Source and guarded SIMULATED preparation only. No current actual plan/build/verify/tool/signing/copy/runtime authority.
+Authority: accepted prior preparations plus T2731.0/D462, BLACKWOOD_NATIVE_BUILD_PREPARATION0.6, with D235's fixed Darwin nonreaping adapter. Source and guarded SIMULATED preparation only. No current actual plan/build/verify/tool/signing/copy/runtime authority.
 
 Every object below has exactly the named fields. Maps have the constrained key/value types stated below, not extension dictionaries. Unknown fields, duplicate JSON keys, nonfinite floats, bool-as-int, noncanonical paths, aliases and overlaps refuse. Generated JSON is sorted-key, indented two spaces, ASCII, LF terminated, with finite numbers. Control/manifest/plan ceilings are32MiB; report/freeze128MiB. Byte counts and integer metadata are nonnegative integers excluding bool; digests are64 lowercase hexadecimal characters. File reads require ordinary single-link data and ordinary ancestors, except the explicitly named installed launcher roles. Successful reports/verification cannot contain partial/null records.
 
@@ -86,3 +86,5 @@
 D456 adds successful-step group_signal `EPERM_DENIED_WHILE_ANCHORED` as an explicit signal denial. It never means a sent signal or inferred group absence. Success still requires a prior exact typed original-child exit0 observation, original-handle reap returning integer0, independent positive group_empty:true, all original cleanup/publication/closure/deadline checks, no primary/secondary/output/I/O error. PermissionError with any other errno fails; missing/failed/wrong-child terminal observations and unknown/live groups fail. The denial enum remains in raw receipt and final ledger; verifier reconstructs the same strict success facts. No signal retry, post-reap mutation, PID discovery or extra grace is introduced. RealOps backend is unchanged.
 
 Source manifest Reference.path is exactly `web/repro/blackwood-source-manifests/` + validated candidate ID + `.json`, derived by stage.manifest_path. Wrong candidate and legacy/global manifest inputs refuse. Source entries cannot include the active manifest itself, preventing a self-hash cycle. No new path/CLI selector is added. The earlier singleton `web/repro/blackwood-source-manifest.json` and all historical controls/failed attempts remain unchanged; future attempts get fresh candidate-bound identities.
+
+D462 linker-only alias normalization is fixed to SDK/usr/lib/libc++.tbd→libc++.1.tbd, libz.tbd→libz.1.tbd, libSystem.tbd→libSystem.B.tbd and libpthread.tbd→libSystem.tbd→libSystem.B.tbd. Every raw edge must remain a symlink with exact text/mode0755 and ordinary ancestors; pthread requires both edges. Canonical terminal must be ordinary/single-link, have ordinary ancestors, resolve to itself and equal the leaf's canonical resolution. Its current SHA must equal both declared observation.inputs and system_sdk.files identities. Unknown aliases, changed edges/modes/types, extra hops, alias ancestors, target aliases/hardlinks/hash changes or missing declarations refuse. No supplied alias map or generic normalization. Builder and verifier independently reconstruct raw traces using the same pure fixed stage validator. LinkInput keys/origin/hashes remain canonical; archive/object/framework rules unchanged. The compiler-header alias policy remains the separate two-header rule; these linker aliases cannot normalize compiler dependency files.
```

## README.md

```diff
--- T272-accepted/README.md
+++ T273/README.md
@@ -46,3 +46,5 @@
 Physical framework copying uses the actual new bounded byte/mode/link copier against fake files in preparation; guards still deny any original framework/SDK path or library copy helper. Default SIGCHLD and fixed nonreaping ownership are rechecked before group mutation, and ECHILD cannot become a successful original-handle reap. The pinned Popen instance hook closes its exit0 fallback only, without a new child command or generic wait selector. Preparation facts never establish actual Darwin ABI/tool support.
 
 T2721.0/D456 under preparation0.5 records anchored signal EPERM explicitly and permits success only after prior original exit0, actual original reap0, positive empty-group observation and every other successful-step obligation. All other denial/unknown/live/reap/observation/publication/deadline faults still refuse. No retry/post-reap signal/backend change follows. Manifest paths now derive from each validated candidate ID under web/repro/blackwood-source-manifests/. New attempts reject the old singleton and wrong-ID manifests or self-reference. Existing singleton/control/visible-native-1 artifacts are preserved. Targeted guarded pass10 is source/simulation only; no actual signal/tool/build or attempt retry.
+
+T2731.0/D462 under preparation0.6 adopts exactly four fixed SDK linker spellings: libc++.tbd, libz.tbd, libSystem.tbd and libpthread.tbd, with pthread's full intermediate edge. Both trace reconstructions validate raw link metadata and canonical declared SDK/input/current target hashes, then retain existing canonical records. Unknown/changed aliases still refuse; compiler-header aliases are unchanged. Guarded pass11 selects six focused alias cases and existing complete fake build/verifier success. No failed attempt/control/manifest is changed and no real retry/verifier/build is released.
```
