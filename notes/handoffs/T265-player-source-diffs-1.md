# T265 four-file source diffs

Baseline: accepted T167 final pass-6 snapshots. No build.py/verify.py change.

## stage.py

```diff
--- T167-accepted/stage.py
+++ T265/stage.py
@@ -31,6 +31,19 @@
 FRAMEWORK_LINKS={'Headers':('Versions/Current/Headers','Versions/A/Headers'),'Resources':('Versions/Current/Resources','Versions/A/Resources'),'SDL2':('Versions/Current/SDL2','Versions/A/SDL2'),'Versions/Current':('A','Versions/A'),'Versions/A/Frameworks/hidapi.framework/Resources':('Versions/Current/Resources','Versions/A/Frameworks/hidapi.framework/Versions/A/Resources'),'Versions/A/Frameworks/hidapi.framework/hidapi':('Versions/Current/hidapi','Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi'),'Versions/A/Frameworks/hidapi.framework/Versions/Current':('A','Versions/A/Frameworks/hidapi.framework/Versions/A')}
 ADAPTER_HEADER_PINS={'sys/wait.h':'b77f7dd6f592eba8b0d51c15c7b975472fdad50c12ea296f74f062cbf98dcbf7','sys/signal.h':'171af7545ef750627aeba02c1de838c05e2cf396e2f49881ea74dba6990c44a3','sys/_types/_pid_t.h':'052a6dbbec8e30623c2d33dd373992f6c5d0c57c57ed4949d2b48c4ab0976487','sys/_types/_uid_t.h':'d2140a65a17943a857381757c0b73a920f35ade41dc9809437c168be457c276a','sys/_types/_id_t.h':'fb7255c9872e2a805c206796326e21d47146e22c93c09752126d7166bdaba5e5','sys/_types.h':'863c4f07045775002b63b7e616742d9f746e4a02da4441442d8fe1138bbd0ff9','machine/_types.h':'f27264f8fdec9f164b4fc2b556f666ed7c5c0e5b88fd9f23db0b731ffa6cf864','arm/_types.h':'4f0bde85f9a41cc7d30fff22ebd7e8f4eb206a55a926eda012a2e7481e3524fa'}
 ADAPTER_STDLIB_ROLES=(PYTHON+'/lib/python3.11/ctypes/__init__.py',PYTHON+'/lib/python3.11/ctypes/_endian.py',PYTHON+'/lib/python3.11/lib-dynload/_ctypes.cpython-311-darwin.so',PYTHON+'/lib/python3.11/platform.py')
+
+# D446: exact historical fixtures, never consumed inputs. No read-error fallback.
+OPAQUE_FILES={
+ 'web/repro/tests/prerequisites/'+name+'/repo/web/build/.cache/bad-mode':
+ {'kind':'opaque_file','device':16777232,'inode':inode,'bytes':12,'mode':0,'uid':501,'gid':20,'nlink':1,'mtime_ns':mtime,'ctime_ns':ctime}
+ for name,inode,mtime,ctime in (
+ ('FIXTURE_ONLY-a6a8xiso',138018950,1794133833737008579,1794133833737028537),
+ ('T101/FIXTURE_ONLY-_ul9woy_',138138188,1794136186239760878,1794136186239782419),
+ ('FIXTURE_ONLY-am2d_ogp',138048696,1794134709255204182,1794134709255226848),
+ ('FIXTURE_ONLY-wxoxh5ho',138002194,1794133651660215054,1794133651660235304),
+ ('FIXTURE_ONLY-gx0ewpha',138037844,1794134245530215563,1794134245530245646),
+ ('FIXTURE_ONLY-hghnb9_0',138028804,1794134032415877479,1794134032415897853),
+ ('FIXTURE_ONLY-ktpjacgc',138010533,1794133723100585246,1794133723100612621))}
 
 class Refused(ValueError):pass
 def need(v,why):
@@ -62,6 +75,17 @@
  need(type(s) is str and s.startswith('/') and str(PurePosixPath(s))==s and all(p not in ('.','..') for p in s.split('/')[1:]) and not any(ord(c)<32 for c in s) and '\\' not in s,'noncanonical absolute path');return s
 def identifier(s):need(type(s) is str and re.fullmatch('[A-Za-z0-9_-]{1,48}',s),'invalid candidate ID');return s
 def beneath(p,base):return p==base or p.startswith(base+'/')
+def opaque_key(root,path):
+ prefix=str(Path(root))+'/';name=str(path);key=name[len(prefix):] if name.startswith(prefix) else None
+ return key if key in OPAQUE_FILES else None
+def opaque_metadata(info):
+ return {'kind':'opaque_file','device':info.st_dev,'inode':info.st_ino,'bytes':info.st_size,'mode':stat.S_IMODE(info.st_mode),'uid':info.st_uid,'gid':info.st_gid,'nlink':info.st_nlink,'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns}
+def opaque_row(root,path,info):
+ key=opaque_key(root,path)
+ if key is None:return None
+ row=opaque_metadata(info);need(stat.S_ISREG(info.st_mode) and same_typed(row,OPAQUE_FILES[key]),'D446 historical fixture metadata changed: '+str(path));return row
+def require_opaque_presence(root,observed):
+ if Path(root)==ROOT:need(all(str(Path(root)/name) in observed for name in OPAQUE_FILES),'known D446 historical fixture missing')
 def loads(data,limit=MAX_CONTROL):
  need(type(data) in (bytes,str) and len(data if type(data) is bytes else data.encode())<=limit,'JSON size bound')
  def pairs(rows):
@@ -135,18 +159,22 @@
  m=re.search(r'(?m)^libenet_la_SOURCES\s*=\s*(.*)$',enet);need(m,'ENet units absent');c=['source/enet/'+x for x in m.group(1).split() if x!='win32.c']
  need(cpp==CPP and c==C,'fixed ordered16-unit recipe changed');return {'cpp':cpp,'c':c}
 
-def validate_preservation(p):
- exact(p,['files','directories','links','absent_roots'],'preservation record fields')
+def validate_preservation(p,root=ROOT):
+ exact(p,['files','directories','links','absent_roots','opaque_files'],'preservation record fields')
  need(type(p['files']) is dict and type(p['links']) is dict,'preservation maps')
- for name,h in p['files'].items():absolute(name);digest(h)
+ for name,h in p['files'].items():absolute(name);digest(h);need(opaque_key(root,name) is None,'D446 fixture cannot be a hashed input')
+ need(type(p['opaque_files']) is dict,'opaque preservation map')
+ for name,row in p['opaque_files'].items():
+  absolute(name);key=opaque_key(root,name);need(key is not None and same_typed(row,OPAQUE_FILES[key]),'unknown/altered D446 opaque preservation row')
+ require_opaque_presence(root,p['opaque_files'])
  for name,row in p['links'].items():
-  absolute(name);exact(row,['target','mode'],'opaque link record');need(type(row['target']) is str and integer(row['mode'],0,0o7777),'opaque link metadata')
+  absolute(name);need(opaque_key(root,name) is None,'D446 fixture cannot become a link');exact(row,['target','mode'],'opaque link record');need(type(row['target']) is str and integer(row['mode'],0,0o7777),'opaque link metadata')
  for key in ('directories','absent_roots'):
   need(type(p[key]) is list and p[key]==sorted(set(p[key])),'preservation sorted unique paths')
-  for name in p[key]:absolute(name)
- kinds=[set(p['files']),set(p['directories']),set(p['links']),set(p['absent_roots'])]
+  for name in p[key]:absolute(name);need(opaque_key(root,name) is None,'D446 fixture changed preservation kind')
+ kinds=[set(p['files']),set(p['directories']),set(p['links']),set(p['opaque_files']),set(p['absent_roots'])]
  need(sum(map(len,kinds))==len(set().union(*kinds)),'preservation kinds overlap')
- for missing in p['absent_roots']:need(not any(beneath(n,missing) for group in kinds[:3] for n in group),'present member inside absent root')
+ for missing in p['absent_roots']:need(not any(beneath(n,missing) for group in kinds[:-1] for n in group),'present member inside absent root')
  return p
 
 def sdk_header_alias(view,inputs,sdk_files,name):
@@ -193,7 +221,7 @@
   need(beneath(name,root) or beneath(name,CLT) or beneath(name,PYTHON) or name in TOOLS.values(),'undeclared external input role before filesystem access')
   if name in TOOLS.values():view.arm_tool(next(k for k,v in TOOLS.items() if v==name),h)
   else:need(view.consume(name) and view.canonical(name)==name and view.hash(name)==h,'changed/nonordinary canonical input: '+name)
- validate_preservation(o['preservation'])
+ validate_preservation(o['preservation'],root)
  if existing:view.omit_container=str(Path(attempt(root,ident)).parent) not in o['preservation']['directories']
  if verify_preservation:need(view.preservation()==o['preservation'],'protected original membership/link changed')
  need(all(root+'/'+n in o['inputs'] for n in entries) and manifest in o['inputs'] and root+'/'+decision in o['inputs'],'manifest/decision inputs missing')
@@ -223,6 +251,7 @@
  def __init__(self,root=ROOT):
   need(str(Path(root))==str(ROOT),'fixed installed repository required');self.root=str(ROOT);self.consumed=set();self.armed={}
  def ordinary(self,p):
+  if opaque_key(self.root,p) is not None:return False
   try:s=Path(p).lstat();return stat.S_ISREG(s.st_mode) and s.st_nlink==1 and self.ordinary_ancestors(p)
   except OSError:return False
  def consume(self,p):
@@ -253,7 +282,7 @@
  def output_safe(self,ident):
   p=Path(attempt(self.root,ident))
   return all(not q.is_symlink() for q in [p,*p.parents])
- def hash(self,p):return file_sha(p,getattr(self,'deadline_check',None))
+ def hash(self,p):need(opaque_key(self.root,p) is None,'D446 fixture cannot be consumed/hashed');return file_sha(p,getattr(self,'deadline_check',None))
  def size(self,p):return Path(p).stat().st_size
  def mode(self,p):return stat.S_IMODE(Path(p).stat().st_mode)
  def text(self,p):return read_bounded(p,MAX_CONTROL).decode()
@@ -288,7 +317,7 @@
  """Fixed protected forests. Opaque links are lstat records, never traversed.
  Decision/package docs outside forests are independently stable observation inputs.
  """
- root=Path(root);result={'files':{},'directories':[],'links':{},'absent_roots':[]}
+ root=Path(root);result={'files':{},'directories':[],'links':{},'absent_roots':[],'opaque_files':{}}
  roots=[root/n for n in ('source','web','bin_unix','packages','config')]
  if browser_sdk is not None:roots.append(Path(browser_sdk))
  if native_sdk is not None:roots.append(Path(native_sdk))
@@ -301,14 +330,15 @@
    if active and (p==Path(active) or Path(active) in p.parents):continue
    # Parent container adds no ordinary files and is declared phase metadata.
    if active and omit_container and p==root/'web/server/blackwood-candidate-attempts':continue
-   st=p.lstat();name=str(p)
-   if stat.S_ISLNK(st.st_mode):result['links'][name]={'target':os.readlink(p),'mode':stat.S_IMODE(st.st_mode)}
+   st=p.lstat();name=str(p);opaque=opaque_row(root,p,st)
+   if opaque is not None:result['opaque_files'][name]=opaque
+   elif stat.S_ISLNK(st.st_mode):result['links'][name]={'target':os.readlink(p),'mode':stat.S_IMODE(st.st_mode)}
    elif stat.S_ISREG(st.st_mode):result['files'][name]=file_sha(p)
    elif stat.S_ISDIR(st.st_mode):result['directories'].append(name)
    else:raise Refused('special preserved member')
  for k in ('directories','absent_roots'):result[k]=sorted(set(result[k]))
- for k in ('files','links'):result[k]=dict(sorted(result[k].items()))
- return validate_preservation(result)
+ for k in ('files','links','opaque_files'):result[k]=dict(sorted(result[k].items()))
+ return validate_preservation(result,root)
 
 def inventory(root,resolve_links=True):
  root=Path(root);need(root.is_dir() and not root.is_symlink(),'ordinary inventory root required');out={}
@@ -456,12 +486,14 @@
    if base==root and '.git' in p.relative_to(root).parts:continue
    if active and (p==Path(active) or Path(active) in p.parents):continue
    if omit_container and p==root/'web/server/blackwood-candidate-attempts':continue
-   info=p.lstat();row={'mode':stat.S_IMODE(info.st_mode)}
-   if stat.S_ISLNK(info.st_mode):row.update(kind='symlink',target=os.readlink(p))
+   info=p.lstat();row={'mode':stat.S_IMODE(info.st_mode)};opaque=opaque_row(root,p,info)
+   if opaque is not None:row=opaque
+   elif stat.S_ISLNK(info.st_mode):row.update(kind='symlink',target=os.readlink(p))
    elif stat.S_ISREG(info.st_mode):row.update(kind='file',bytes=info.st_size,sha256=file_sha(p))
    elif stat.S_ISDIR(info.st_mode):row.update(kind='directory')
    else:raise Refused('special protected file')
    out[str(p)]=row
+ require_opaque_presence(root,out)
  return dict(sorted(out.items()))
 
 def macho(data,kind):
```

## test_preparation.py

```diff
--- T167-accepted/test_preparation.py
+++ T265/test_preparation.py
@@ -8,7 +8,7 @@
 OUTPUT_CAP=8388608
 STORAGE_CAP=134217728
 PASS_SECONDS=300
-stage=build=verify=NATIVE_OPS=None
+stage=build=verify=NATIVE_OPS=NATIVE_VIEW=None
 
 class Guards:
  """Install before project imports. Real host effects stay denied throughout tests."""
@@ -212,6 +212,7 @@
  def exists(self,p):q=self.mapped(p);return q.exists() or q.is_symlink()
  def file_stat(self,p):return self.mapped(p).lstat()
  def ordinary(self,p):
+  if stage.opaque_key(self.root,p) is not None:return False
   try:s=self.file_stat(p);return stat.S_ISREG(s.st_mode) and s.st_nlink==1 and self.ordinary_ancestors(p)
   except OSError:return False
  def canonical(self,p):
@@ -678,10 +679,52 @@
     else:ops.kill(child,lambda:None);assert ops.wait(child,1)==0 and events==['signal','wait']
    f.case_observation={'backend':variant,'events':events,'anchor_lost':ops.wait_adapter.anchor_lost,'returncode':child.returncode}
   add('D235_backend_'+variant,backend)
+ for variant in ('known_without_open','readable_hash_unchanged','unknown_unreadable','unknown_path','unknown_field','bool_mode','hashed_promotion','consume_promotion','missing_known','file_type','device','inode','bytes','mode','uid','gid','nlink','mtime_ns','ctime_ns'):
+  def opaque_case(f,variant=variant):
+   expected={}
+   for name in stage.OPAQUE_FILES:
+    p=f.put(name,b'FIXTURE_ONLY',0);expected[name]=stage.opaque_metadata(p.lstat())
+   keys=set(str(Path(f.root)/n) for n in expected);first=next(iter(expected));path=Path(f.root)/first;original=stage.file_sha;reads=[]
+   def observed(p,*args,**kwargs):
+    name=str(p);reads.append(name)
+    if name in keys:raise AssertionError('D446 fixture opened instead of metadata preservation')
+    if name.endswith('/UNKNOWN_UNREADABLE'):raise PermissionError('FIXTURE_ONLY unknown unreadable file')
+    return original(p,*args,**kwargs)
+   with patch.object(stage,'OPAQUE_FILES',expected),patch.object(stage,'file_sha',observed):
+    if variant=='unknown_unreadable':
+     unknown=f.put('web/UNKNOWN_UNREADABLE');refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root));assert str(unknown) in reads;return
+    preserved=f.view.preservation();protected=stage.protected_inventory(f.root)
+    assert set(preserved['opaque_files'])==keys and all(protected[n]==preserved['opaque_files'][n] for n in keys) and not (keys&set(reads))
+    if variant=='known_without_open':pass
+    elif variant=='missing_known':
+     path.unlink();changed=copy.deepcopy(preserved);changed['opaque_files'].pop(str(path))
+     with patch.object(stage,'ROOT',Path(f.root)):
+      refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root));refused(lambda:stage.validate_preservation(changed,f.root))
+    elif variant=='readable_hash_unchanged':
+     normal=Path(f.root)/'source/src/sound.h';before=preserved['files'][str(normal)];normal.write_bytes(b'FIXTURE_ONLY_CHANGED');assert f.view.preservation()['files'][str(normal)]!=before
+    elif variant=='consume_promotion':
+     assert not NATIVE_VIEW.ordinary(f.view,str(path)) and not f.view.consume(str(path));refused(lambda:NATIVE_VIEW.hash(f.view,str(path)))
+     doc={'schema_version':1,'kind':'SOURCE_INPUT_MANIFEST','source_revision':'1'*40,'entries':[{'path':first,'bytes':12,'mode':0o644,'sha256':'0'*64}]}
+     refused(lambda:stage.source_manifest(doc,'1'*40,f.view,f.root))
+     f.view.declared_inputs={str(path):'0'*64};refused(lambda:stage.dependency_paths('/FIXTURE_ONLY.o: '+str(path),'/FIXTURE_ONLY.o',f.view,f.ident))
+    elif variant in ('unknown_path','unknown_field','bool_mode','hashed_promotion'):
+     changed=copy.deepcopy(preserved);row=changed['opaque_files'][str(path)]
+     if variant=='unknown_path':changed['opaque_files'][str(path)+'_UNKNOWN']=changed['opaque_files'].pop(str(path))
+     elif variant=='unknown_field':row['extra']=True
+     elif variant=='bool_mode':row['mode']=False
+     else:changed['files'][str(path)]='0'*64;changed['opaque_files'].pop(str(path))
+     refused(lambda:stage.validate_preservation(changed,f.root))
+    else:
+     info=path.lstat();fields={n:getattr(info,n) for n in ('st_mode','st_dev','st_ino','st_size','st_uid','st_gid','st_nlink','st_mtime_ns','st_ctime_ns')}
+     attribute={'file_type':'st_mode','device':'st_dev','inode':'st_ino','bytes':'st_size','mode':'st_mode','uid':'st_uid','gid':'st_gid','nlink':'st_nlink','mtime_ns':'st_mtime_ns','ctime_ns':'st_ctime_ns'}[variant]
+     fields[attribute]=stat.S_IFDIR if variant=='file_type' else fields[attribute]+1
+     refused(lambda:stage.opaque_row(f.root,path,types.SimpleNamespace(**fields)))
+    f.case_observation={'variant':variant,'opaque_count':len(keys),'known_file_content_reads':len(keys&set(reads)),'classification':'SIMULATED_METADATA'}
+  add('D446_'+variant,opaque_case)
  return rows
 
 def main():
- global stage,build,verify,NATIVE_OPS
+ global stage,build,verify,NATIVE_OPS,NATIVE_VIEW
  start=time.monotonic()
  parser=argparse.ArgumentParser();parser.add_argument('--pass-id',required=True);parser.add_argument('--plan-sha256',required=True);args=parser.parse_args()
  assert re.fullmatch(r'pass-[1-9][0-9]*',args.pass_id)
@@ -710,6 +753,7 @@
    assert name not in sys.modules,'preloaded project module'
    spec=importlib.util.spec_from_file_location(name,OWN/(name+'.py'));module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module);globals()[name]=module
   actual_view=stage.View
+  NATIVE_VIEW=actual_view
   NATIVE_OPS=build.RealOps
   for name,value in actual_view.__dict__.items():
    if callable(value) and name not in FixtureView.__dict__:setattr(FixtureView,name,value)
```

## SCHEMA.md

```diff
--- T167-accepted/SCHEMA.md
+++ T265/SCHEMA.md
@@ -1,6 +1,6 @@
 # Blackwood native preparation schema
 
-Authority: T1671.2 / D443, BLACKWOOD_NATIVE_BUILD_PREPARATION0.1 / D232, with D235's fixed Darwin nonreaping adapter. Source and guarded SIMULATED preparation only. No current actual plan/build/verify/tool/signing/copy/runtime authority.
+Authority: accepted T1671.2/D444 plus T2651.0/D446, BLACKWOOD_NATIVE_BUILD_PREPARATION0.2, with D235's fixed Darwin nonreaping adapter. Source and guarded SIMULATED preparation only. No current actual plan/build/verify/tool/signing/copy/runtime authority.
 
 Every object below has exactly the named fields. Maps have the constrained key/value types stated below, not extension dictionaries. Unknown fields, duplicate JSON keys, nonfinite floats, bool-as-int, noncanonical paths, aliases and overlaps refuse. Generated JSON is sorted-key, indented two spaces, ASCII, LF terminated, with finite numbers. Control/manifest/plan ceilings are32MiB; report/freeze128MiB. Byte counts and integer metadata are nonnegative integers excluding bool; digests are64 lowercase hexadecimal characters. File reads require ordinary single-link data and ordinary ancestors, except the explicitly named installed launcher roles. Successful reports/verification cannot contain partial/null records.
 
@@ -10,7 +10,9 @@
 
 `SourceAcceptance` is exactly `{ticket:"T163",decision:Reference,handoff:Reference,evidence:Reference,files:[FileRef x4]}`. `Reference` is exactly `{path:relative,sha256:SHA}`. The three fixed D223/final-handoff/MAIN-review paths and digests and four sorted source files/hashes are literal stage.py constants from approved BLACKWOOD_BUILD_PREPARATION0.1. All source sizes/modes/current bytes are checked. Native does not have to consume the browser-only private header. Fixture subclasses replace source DATA identities solely inside guarded fakes and remain barred from real authorization.
 
-`Preservation` is exactly `{files:{absolute:SHA},directories:[absolute sorted unique],links:{absolute:{target:string,mode:uint<=4095}},absent_roots:[absolute sorted unique]}`. Kinds are disjoint; no present descendant is hidden by an absent root. Historical links are opaque lstat records, never consumed or traversed. The selected authorization's expected external digest/current ordinary identity is checked independently before/after work; it does not hash itself through observation or source manifest. No general history exemption exists. Only the exact new current attempt and a predeclared absent parent container can differ. Full original protection also includes unconsumed history, not only declared compiler inputs.
+`Preservation` is exactly `{files:{absolute:SHA},directories:[absolute sorted unique],links:{absolute:{target:string,mode:uint<=4095}},opaque_files:{absolute:OpaqueFile},absent_roots:[absolute sorted unique]}`. Kinds are disjoint; no present descendant is hidden by an absent root. Historical links are opaque lstat records, never consumed or traversed. The selected authorization's expected external digest/current ordinary identity is checked independently before/after work; it does not hash itself through observation or source manifest. Only the exact new current attempt and a predeclared absent parent container can differ. Full original protection also includes unconsumed history, not only declared compiler inputs.
+
+D446 `OpaqueFile` is exactly `{kind:"opaque_file",device,inode,bytes,mode,uid,gid,nlink,mtime_ns,ctime_ns}` with every numeric field an integer excluding bool, equal to the literal seven path/metadata records in stage.OPAQUE_FILES and D446. These twelve-byte mode0000 historical fixtures are lstat-only, with no content verification available. The same exact row appears in protected_inventory. Production preservation validation and protected inventory require all seven known paths to remain present; synthetic roots do not require actual inode-bound artifacts. Only exact repository-relative paths qualify; unknown unreadable paths fail normal hashing, with no PermissionError fallback. Altered metadata/type, unknown fields/path, hashed/link/directory/absent-kind promotion or consumed source/header/tool/framework/SDK/dependency use refuses. Readable originals retain byte-hash preservation. No permission or original artifact changes are allowed.
 
 `FrameworkInventory` is a sorted map of relative paths to exactly one of `{kind:"file",mode:uint,bytes:uint,sha256:SHA}`, `{kind:"directory",mode:uint}`, `{kind:"symlink",mode:493,target:relativeRaw,resolved:relativeTerminal}`. It includes all source membership/licenses/Info/headers/binaries and exactly the seven named confined SDL/hidapi links from stage.FRAMEWORK_LINKS. Ordinary members are single-link. Original SDL2/hidapi hashes are fixed unsigned identities; copied post-sign hashes are observed separately. Physical copies have different device/inode identity from originals. Only the two copied binaries plus their exact `_CodeSignature` directories/CodeResources may change; added signature members have their expected directory/file kinds with actual modes recorded, existing kind/mode unchanged. Nested hidapi signing precedes parent SDL2, no --deep and no explicit ac_server signing.
 
```

## README.md

```diff
--- T167-accepted/README.md
+++ T265/README.md
@@ -1,6 +1,8 @@
 # Blackwood native builder preparation
 
 T1671.2 / D443 resumes these six existing files and guarded simulated preparation under D232. D235 adds the fixed lazy Darwin nonreaping adapter. T162 is closed; T149 and QA remain held. Nothing here currently authorizes real project planning, compiler/version/tool inspection, native signing/copy/build/verify, browser/server/network/runtime or Git operations.
+
+T167 preparation is accepted D444. T2651.0/D446 under BLACKWOOD_NATIVE_BUILD_PREPARATION0.2 adds only seven exact historical mode0000 fixture identities as lstat-only preservation rows. Their content cannot be verified; they are never consumed inputs. Unknown unreadable files still refuse; every readable original remains hashed. Targeted guarded pass-7 retains the original202-case definitions and includes the existing full fake build/verifier success. No T264 observation retry, original chmod or actual build is authorized by this correction.
 
 The accepted native recipe is retained as source DATA from the five pinned web/server/candidate baseline files. No old module is imported or run. Baseline byte copies and pins are under preparation-1/baseline. Preparation evidence records bounded source diffs and exact source/authority/fixture pins before each justified fresh pass. The native successor is disjoint from T164's browser implementation and imports none of it.
 
```
