# T268 four-file source diffs

Baseline: accepted T265 pass-7 snapshots. Build/verifier unchanged.

## stage.py

```diff
--- T265-accepted/stage.py
+++ T268/stage.py
@@ -44,6 +44,15 @@
  ('FIXTURE_ONLY-gx0ewpha',138037844,1794134245530215563,1794134245530245646),
  ('FIXTURE_ONLY-hghnb9_0',138028804,1794134032415877479,1794134032415897853),
  ('FIXTURE_ONLY-ktpjacgc',138010533,1794133723100585246,1794133723100612621))}
+# D450: closed roster from accepted plan-pass-7 (a2dfd976...e0faae40).
+OPAQUE_COPY_CASES=(
+ '001-D446_known_without_open','002-D446_readable_hash_unchanged',
+ '003-D446_unknown_unreadable','004-D446_unknown_path','005-D446_unknown_field',
+ '006-D446_bool_mode','007-D446_hashed_promotion','008-D446_consume_promotion',
+ '009-D446_missing_known','010-D446_file_type','011-D446_device','012-D446_inode',
+ '013-D446_bytes','014-D446_mode','015-D446_uid','016-D446_gid','017-D446_nlink',
+ '018-D446_mtime_ns','019-D446_ctime_ns')
+OPAQUE_COPY_PATHS=frozenset('web/server/blackwood_candidate/supervisor-fixtures-1/pass-7/'+case+'/'+suffix for case in OPAQUE_COPY_CASES for suffix in OPAQUE_FILES)
 
 class Refused(ValueError):pass
 def need(v,why):
@@ -77,13 +86,19 @@
 def beneath(p,base):return p==base or p.startswith(base+'/')
 def opaque_key(root,path):
  prefix=str(Path(root))+'/';name=str(path);key=name[len(prefix):] if name.startswith(prefix) else None
- return key if key in OPAQUE_FILES else None
+ return key if key in OPAQUE_FILES or key in OPAQUE_COPY_PATHS else None
 def opaque_metadata(info):
  return {'kind':'opaque_file','device':info.st_dev,'inode':info.st_ino,'bytes':info.st_size,'mode':stat.S_IMODE(info.st_mode),'uid':info.st_uid,'gid':info.st_gid,'nlink':info.st_nlink,'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns}
 def opaque_row(root,path,info):
  key=opaque_key(root,path)
  if key is None:return None
- row=opaque_metadata(info);need(stat.S_ISREG(info.st_mode) and same_typed(row,OPAQUE_FILES[key]),'D446 historical fixture metadata changed: '+str(path));return row
+ row=opaque_metadata(info);need(stat.S_ISREG(info.st_mode),'opaque historical fixture changed type');validate_opaque_identity(root,path,row);return row
+def validate_opaque_identity(root,path,row):
+ key=opaque_key(root,path);need(key is not None,'unknown opaque historical fixture path')
+ if key in OPAQUE_FILES:need(same_typed(row,OPAQUE_FILES[key]),'D446 historical fixture metadata changed: '+str(path));return
+ exact(row,['kind','device','inode','bytes','mode','uid','gid','nlink','mtime_ns','ctime_ns'],'D450 opaque copy fields')
+ need(row['kind']=='opaque_file' and all(integer(row[n]) for n in row if n!='kind') and row['inode']>0,'D450 opaque copy integer identity')
+ need({n:row[n] for n in ('device','bytes','mode','uid','gid','nlink')}=={'device':16777232,'bytes':12,'mode':0,'uid':501,'gid':20,'nlink':1},'D450 opaque copy metadata policy')
 def require_opaque_presence(root,observed):
  if Path(root)==ROOT:need(all(str(Path(root)/name) in observed for name in OPAQUE_FILES),'known D446 historical fixture missing')
 def loads(data,limit=MAX_CONTROL):
@@ -165,7 +180,7 @@
  for name,h in p['files'].items():absolute(name);digest(h);need(opaque_key(root,name) is None,'D446 fixture cannot be a hashed input')
  need(type(p['opaque_files']) is dict,'opaque preservation map')
  for name,row in p['opaque_files'].items():
-  absolute(name);key=opaque_key(root,name);need(key is not None and same_typed(row,OPAQUE_FILES[key]),'unknown/altered D446 opaque preservation row')
+  absolute(name);validate_opaque_identity(root,name,row)
  require_opaque_presence(root,p['opaque_files'])
  for name,row in p['links'].items():
   absolute(name);need(opaque_key(root,name) is None,'D446 fixture cannot become a link');exact(row,['target','mode'],'opaque link record');need(type(row['target']) is str and integer(row['mode'],0,0o7777),'opaque link metadata')
```

## test_preparation.py

```diff
--- T265-accepted/test_preparation.py
+++ T268/test_preparation.py
@@ -381,6 +381,17 @@
  base=f.output();p=base/'freeze.json';doc=stage.loads(p.read_bytes(),stage.MAX_RECORD);items=stage.inventory(base,False)
  for n in ('freeze.json','failure.json','verification/receipt.json'):items.pop(n,None)
  doc['files']=items;p.write_text(stage.canonical_json(doc))
+
+def opaque_test_stat(info):
+ fields={n:getattr(info,n) for n in ('st_mode','st_dev','st_ino','st_size','st_uid','st_gid','st_nlink','st_mtime_ns','st_ctime_ns')}
+ fields.update(st_mode=stat.S_IFREG,st_dev=16777232,st_uid=501,st_gid=20)
+ return types.SimpleNamespace(**fields)
+
+def injected_lstat(records,original):
+ def observed(path,*args,**kwargs):
+  actual=original(path,*args,**kwargs) # Still require the readable fixture to exist.
+  return records.get(str(path),actual)
+ return observed
 
 CONTROL_CASES=(
  ('schema_bool',lambda p:p.update(schema_version=True)),('authority',lambda p:p.update(authority='worker')),('status',lambda p:p.update(status='PREPARED')),('execution_release',lambda p:p.update(execution_release='OTHER')),('recipe',lambda p:p.update(recipe='native_standalone_v1')),('candidate_path',lambda p:p.update(candidate_id='../x')),('unknown',lambda p:p.update(extra='x')),('HEAD',lambda p:p.update(source_revision='2'*40)),('binding',lambda p:p['bindings'].update(system_sdk='/tmp/latest')),('tool_path',lambda p:p['observation']['tools']['cc'].update(path='/bin/sh')),('flags',lambda p:p['observation']['flags']['release'].append('-DFAKE')),('units',lambda p:p['observation']['units']['c'].pop()),('missing_link_input',lambda p:p['observation']['inputs'].pop(stage.CLT+'/usr/bin/ld')),('missing_runtime',lambda p:p['observation']['inputs'].pop(stage.CLT+'/usr/lib/clang/17/lib/darwin/libclang_rt.osx.a')),('missing_cpp_stub',lambda p:p['observation']['inputs'].pop(stage.SDK+'/usr/lib/libc++.1.tbd')),('source_reference',lambda p:p['source_acceptance']['decision'].update(sha256='0'*64)),('source_bool',lambda p:p['source_acceptance']['files'][0].update(bytes=True)),('source_unknown',lambda p:p['source_acceptance'].update(extra=1)),('source_files',lambda p:p['source_acceptance']['files'].pop()),('map_revision_data',lambda p:next(r for r in p['observation']['map_seed']['files'] if r['target'].endswith('.cgz')).update(bytes=561)),('map_target',lambda p:p['observation']['map_seed']['files'][0].update(target='packages/maps/ac_desert.cgz')),('map_notice',lambda p:p['observation']['map_seed']['files'][0].update(source='missing.cgz.LICENSE.txt')),('map_sha',lambda p:p['observation']['map_seed']['files'][0].update(sha256='0'*64)),('map_mode_bool',lambda p:p['observation']['map_seed']['files'][0].update(mode=True)),('rotation',lambda p:p['observation']['map_seed']['rotation'].update(sha256='0'*64)),('map_unknown',lambda p:p['observation']['map_seed'].update(extra=1)),('manifest_path',lambda p:p['source_manifest'].update(path='web/repro/source-manifest.json')),('observation_unknown',lambda p:p['observation'].update(extra=1)),('SDK_hash',lambda p:p['observation']['system_sdk']['files'].update({'usr/include/zlib.h':'0'*64})),('authoring_missing',lambda p:p['observation']['inputs'].pop(stage.PYTHON+'/bin/python3.11')))
@@ -681,16 +692,16 @@
   add('D235_backend_'+variant,backend)
  for variant in ('known_without_open','readable_hash_unchanged','unknown_unreadable','unknown_path','unknown_field','bool_mode','hashed_promotion','consume_promotion','missing_known','file_type','device','inode','bytes','mode','uid','gid','nlink','mtime_ns','ctime_ns'):
   def opaque_case(f,variant=variant):
-   expected={}
+   expected={};metadata={}
    for name in stage.OPAQUE_FILES:
-    p=f.put(name,b'FIXTURE_ONLY',0);expected[name]=stage.opaque_metadata(p.lstat())
+    p=f.put(name,b'FIXTURE_ONLY');metadata[str(p)]=opaque_test_stat(p.lstat());expected[name]=stage.opaque_metadata(metadata[str(p)])
    keys=set(str(Path(f.root)/n) for n in expected);first=next(iter(expected));path=Path(f.root)/first;original=stage.file_sha;reads=[]
    def observed(p,*args,**kwargs):
     name=str(p);reads.append(name)
     if name in keys:raise AssertionError('D446 fixture opened instead of metadata preservation')
     if name.endswith('/UNKNOWN_UNREADABLE'):raise PermissionError('FIXTURE_ONLY unknown unreadable file')
     return original(p,*args,**kwargs)
-   with patch.object(stage,'OPAQUE_FILES',expected),patch.object(stage,'file_sha',observed):
+   with patch.object(stage,'OPAQUE_FILES',expected),patch.object(stage,'file_sha',observed),patch.object(Path,'lstat',injected_lstat(metadata,Path.lstat)):
     if variant=='unknown_unreadable':
      unknown=f.put('web/UNKNOWN_UNREADABLE');refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root));assert str(unknown) in reads;return
     preserved=f.view.preservation();protected=stage.protected_inventory(f.root)
@@ -721,6 +732,48 @@
      refused(lambda:stage.opaque_row(f.root,path,types.SimpleNamespace(**fields)))
     f.case_observation={'variant':variant,'opaque_count':len(keys),'known_file_content_reads':len(keys&set(reads)),'classification':'SIMULATED_METADATA'}
   add('D446_'+variant,opaque_case)
+ for variant in ('known_closed_set','unknown_case','unknown_index','unknown_pass','unknown_suffix','file_type','mode','bytes','uid','gid','device','nlink','bool_inode','negative_time','extra_field','consume_promotion','inode_changed','mtime_changed','ctime_changed'):
+  def copy_case(f,variant=variant):
+   name=sorted(stage.OPAQUE_COPY_PATHS)[0]
+   replacements={'unknown_case':('D446_known_without_open','D446_UNKNOWN'),'unknown_index':('001-D446','099-D446'),'unknown_pass':('/pass-7/','/pass-8/'),'unknown_suffix':('/bad-mode','/UNKNOWN_BAD_MODE')}
+   if variant in replacements:
+    old,new=replacements[variant];name=name.replace(old,new)
+   names=sorted(stage.OPAQUE_COPY_PATHS) if variant=='known_closed_set' else [name];metadata={}
+   for member in names:
+    p=f.put(member,b'FIXTURE_ONLY');metadata[str(p)]=opaque_test_stat(p.lstat())
+   path=Path(f.root)/name;original=stage.file_sha;attempts=[]
+   def read(p,*args,**kwargs):
+    if str(p) in metadata:
+     attempts.append(str(p))
+     if variant in replacements:raise PermissionError('FIXTURE_ONLY unknown unreadable copy')
+     raise AssertionError('known copy opened for content')
+    return original(p,*args,**kwargs)
+   with patch.object(stage,'file_sha',read),patch.object(Path,'lstat',injected_lstat(metadata,Path.lstat)):
+    if variant in replacements:
+     refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root));assert attempts;return
+    preserved=f.view.preservation();protected=stage.protected_inventory(f.root);row=preserved['opaque_files'][str(path)]
+    assert set(preserved['opaque_files'])==set(metadata) and protected[str(path)]==row and not attempts
+    if variant=='known_closed_set':assert len(metadata)==133
+    elif variant=='consume_promotion':
+     assert not NATIVE_VIEW.ordinary(f.view,str(path)) and not f.view.consume(str(path));refused(lambda:NATIVE_VIEW.hash(f.view,str(path)))
+     doc={'schema_version':1,'kind':'SOURCE_INPUT_MANIFEST','source_revision':'1'*40,'entries':[{'path':name,'bytes':12,'mode':0o644,'sha256':'0'*64}]};refused(lambda:stage.source_manifest(doc,'1'*40,f.view,f.root))
+     f.view.declared_inputs={str(path):'0'*64};refused(lambda:stage.dependency_paths('/FIXTURE_ONLY.o: '+str(path),'/FIXTURE_ONLY.o',f.view,f.ident))
+    elif variant in ('inode_changed','mtime_changed','ctime_changed'):
+     f.auth['observation']['preservation']=preserved;f.write();f.gate()
+     attribute={'inode_changed':'st_ino','mtime_changed':'st_mtime_ns','ctime_changed':'st_ctime_ns'}[variant];setattr(metadata[str(path)],attribute,getattr(metadata[str(path)],attribute)+1)
+     refused(f.gate);assert stage.protected_inventory(f.root)[str(path)]!=protected[str(path)]
+    elif variant=='file_type':
+     metadata[str(path)].st_mode=stat.S_IFDIR;refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root))
+    else:
+     changed=copy.deepcopy(preserved);altered=changed['opaque_files'][str(path)]
+     if variant=='extra_field':altered['unknown']=0
+     elif variant=='bool_inode':altered['inode']=True
+     elif variant=='negative_time':altered['ctime_ns']=-1
+     else:altered[variant]+=1
+     refused(lambda:stage.validate_preservation(changed,f.root))
+    assert not attempts
+    f.case_observation={'variant':variant,'known_copy_count':len(metadata),'known_content_reads':len(attempts),'actual_files_readable':True,'metadata_and_read_denial':'INJECTED_ONLY'}
+  add('D450_'+variant,copy_case)
  return rows
 
 def main():
```

## SCHEMA.md

```diff
--- T265-accepted/SCHEMA.md
+++ T268/SCHEMA.md
@@ -1,6 +1,6 @@
 # Blackwood native preparation schema
 
-Authority: accepted T1671.2/D444 plus T2651.0/D446, BLACKWOOD_NATIVE_BUILD_PREPARATION0.2, with D235's fixed Darwin nonreaping adapter. Source and guarded SIMULATED preparation only. No current actual plan/build/verify/tool/signing/copy/runtime authority.
+Authority: accepted T1671.2/D444 and T265/D448 plus T2681.0/D450, BLACKWOOD_NATIVE_BUILD_PREPARATION0.3, with D235's fixed Darwin nonreaping adapter. Source and guarded SIMULATED preparation only. No current actual plan/build/verify/tool/signing/copy/runtime authority.
 
 Every object below has exactly the named fields. Maps have the constrained key/value types stated below, not extension dictionaries. Unknown fields, duplicate JSON keys, nonfinite floats, bool-as-int, noncanonical paths, aliases and overlaps refuse. Generated JSON is sorted-key, indented two spaces, ASCII, LF terminated, with finite numbers. Control/manifest/plan ceilings are32MiB; report/freeze128MiB. Byte counts and integer metadata are nonnegative integers excluding bool; digests are64 lowercase hexadecimal characters. File reads require ordinary single-link data and ordinary ancestors, except the explicitly named installed launcher roles. Successful reports/verification cannot contain partial/null records.
 
@@ -13,6 +13,8 @@
 `Preservation` is exactly `{files:{absolute:SHA},directories:[absolute sorted unique],links:{absolute:{target:string,mode:uint<=4095}},opaque_files:{absolute:OpaqueFile},absent_roots:[absolute sorted unique]}`. Kinds are disjoint; no present descendant is hidden by an absent root. Historical links are opaque lstat records, never consumed or traversed. The selected authorization's expected external digest/current ordinary identity is checked independently before/after work; it does not hash itself through observation or source manifest. Only the exact new current attempt and a predeclared absent parent container can differ. Full original protection also includes unconsumed history, not only declared compiler inputs.
 
 D446 `OpaqueFile` is exactly `{kind:"opaque_file",device,inode,bytes,mode,uid,gid,nlink,mtime_ns,ctime_ns}` with every numeric field an integer excluding bool, equal to the literal seven path/metadata records in stage.OPAQUE_FILES and D446. These twelve-byte mode0000 historical fixtures are lstat-only, with no content verification available. The same exact row appears in protected_inventory. Production preservation validation and protected inventory require all seven known paths to remain present; synthetic roots do not require actual inode-bound artifacts. Only exact repository-relative paths qualify; unknown unreadable paths fail normal hashing, with no PermissionError fallback. Altered metadata/type, unknown fields/path, hashed/link/directory/absent-kind promotion or consumed source/header/tool/framework/SDK/dependency use refuses. Readable originals retain byte-hash preservation. No permission or original artifact changes are allowed.
+
+D450 extends this same row type only to `web/server/blackwood_candidate/supervisor-fixtures-1/pass-7/` + one of the19 literal `OPAQUE_COPY_CASES` directory strings + one of the seven exact D446 suffixes. The roster is pinned by accepted plan-pass-7 SHA256a2dfd976759128145ae861390cb98473efbd77af7e3ab8185a22aed4e0faae40; at most133 paths, with no presence requirement for copies. Original seven mandatory identities/presence remain unchanged. Copy rows require ordinary files, device16777232/bytes12/mode0/uid501/gid20/nlink1. All numeric fields exclude bool, fit0..2^63-1, and inode is positive. Actual observation/control binds each inode/mtime/ctime; full before/after equality detects changes. Unknown pass/index/case/suffix and consumed promotion refuse. No generic unreadable-prefix or PermissionError exemption exists. New targeted tests use readable files and injected lstat/read denial, never new physical mode0000 copies.
 
 `FrameworkInventory` is a sorted map of relative paths to exactly one of `{kind:"file",mode:uint,bytes:uint,sha256:SHA}`, `{kind:"directory",mode:uint}`, `{kind:"symlink",mode:493,target:relativeRaw,resolved:relativeTerminal}`. It includes all source membership/licenses/Info/headers/binaries and exactly the seven named confined SDL/hidapi links from stage.FRAMEWORK_LINKS. Ordinary members are single-link. Original SDL2/hidapi hashes are fixed unsigned identities; copied post-sign hashes are observed separately. Physical copies have different device/inode identity from originals. Only the two copied binaries plus their exact `_CodeSignature` directories/CodeResources may change; added signature members have their expected directory/file kinds with actual modes recorded, existing kind/mode unchanged. Nested hidapi signing precedes parent SDL2, no --deep and no explicit ac_server signing.
 
```

## README.md

```diff
--- T265-accepted/README.md
+++ T268/README.md
@@ -3,6 +3,8 @@
 T1671.2 / D443 resumes these six existing files and guarded simulated preparation under D232. D235 adds the fixed lazy Darwin nonreaping adapter. T162 is closed; T149 and QA remain held. Nothing here currently authorizes real project planning, compiler/version/tool inspection, native signing/copy/build/verify, browser/server/network/runtime or Git operations.
 
 T167 preparation is accepted D444. T2651.0/D446 under BLACKWOOD_NATIVE_BUILD_PREPARATION0.2 adds only seven exact historical mode0000 fixture identities as lstat-only preservation rows. Their content cannot be verified; they are never consumed inputs. Unknown unreadable files still refuse; every readable original remains hashed. Targeted guarded pass-7 retains the original202-case definitions and includes the existing full fake build/verifier success. No T264 observation retry, original chmod or actual build is authorized by this correction.
+
+T2681.0/D450 under preparation0.3 additionally recognizes only the finite retained pass-7 D446 case copies of those seven suffixes (19 exact indexed directory names, at most133 paths). Copy inode/timestamps are bound by the observed control and before/after equality; original seven literal pins and mandatory presence are unchanged. Guarded pass-8 uses readable synthetic files with injected lstat/read denial, preventing new unreadable retained artifacts. Old pass-7 data stays unchanged; no T267 retry or actual build follows from this correction.
 
 The accepted native recipe is retained as source DATA from the five pinned web/server/candidate baseline files. No old module is imported or run. Baseline byte copies and pins are under preparation-1/baseline. Preparation evidence records bounded source diffs and exact source/authority/fixture pins before each justified fresh pass. The native successor is disjoint from T164's browser implementation and imports none of it.
 
```
