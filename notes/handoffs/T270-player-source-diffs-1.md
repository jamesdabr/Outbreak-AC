# T270 four-file source diffs

Baseline: accepted T268 pass8 snapshots. Build/verifier unchanged.

## stage.py

```diff
--- T268-accepted/stage.py
+++ T270/stage.py
@@ -44,15 +44,7 @@
  ('FIXTURE_ONLY-gx0ewpha',138037844,1794134245530215563,1794134245530245646),
  ('FIXTURE_ONLY-hghnb9_0',138028804,1794134032415877479,1794134032415897853),
  ('FIXTURE_ONLY-ktpjacgc',138010533,1794133723100585246,1794133723100612621))}
-# D450: closed roster from accepted plan-pass-7 (a2dfd976...e0faae40).
-OPAQUE_COPY_CASES=(
- '001-D446_known_without_open','002-D446_readable_hash_unchanged',
- '003-D446_unknown_unreadable','004-D446_unknown_path','005-D446_unknown_field',
- '006-D446_bool_mode','007-D446_hashed_promotion','008-D446_consume_promotion',
- '009-D446_missing_known','010-D446_file_type','011-D446_device','012-D446_inode',
- '013-D446_bytes','014-D446_mode','015-D446_uid','016-D446_gid','017-D446_nlink',
- '018-D446_mtime_ns','019-D446_ctime_ns')
-OPAQUE_COPY_PATHS=frozenset('web/server/blackwood_candidate/supervisor-fixtures-1/pass-7/'+case+'/'+suffix for case in OPAQUE_COPY_CASES for suffix in OPAQUE_FILES)
+FIXTURE_FORESTS=('web/repro/tests/prerequisites','web/server/blackwood_candidate/supervisor-fixtures-1')
 
 class Refused(ValueError):pass
 def need(v,why):
@@ -84,23 +76,46 @@
  need(type(s) is str and s.startswith('/') and str(PurePosixPath(s))==s and all(p not in ('.','..') for p in s.split('/')[1:]) and not any(ord(c)<32 for c in s) and '\\' not in s,'noncanonical absolute path');return s
 def identifier(s):need(type(s) is str and re.fullmatch('[A-Za-z0-9_-]{1,48}',s),'invalid candidate ID');return s
 def beneath(p,base):return p==base or p.startswith(base+'/')
-def opaque_key(root,path):
- prefix=str(Path(root))+'/';name=str(path);key=name[len(prefix):] if name.startswith(prefix) else None
- return key if key in OPAQUE_FILES or key in OPAQUE_COPY_PATHS else None
+def fixture_forest(root,path):
+ prefix=str(Path(root))+'/';name=str(path)
+ if not name.startswith(prefix):return None
+ relative=name[len(prefix):]
+ return next((forest for forest in FIXTURE_FORESTS if beneath(relative,forest)),None)
 def opaque_metadata(info):
  return {'kind':'opaque_file','device':info.st_dev,'inode':info.st_ino,'bytes':info.st_size,'mode':stat.S_IMODE(info.st_mode),'uid':info.st_uid,'gid':info.st_gid,'nlink':info.st_nlink,'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns}
-def opaque_row(root,path,info):
- key=opaque_key(root,path)
- if key is None:return None
- row=opaque_metadata(info);need(stat.S_ISREG(info.st_mode),'opaque historical fixture changed type');validate_opaque_identity(root,path,row);return row
-def validate_opaque_identity(root,path,row):
- key=opaque_key(root,path);need(key is not None,'unknown opaque historical fixture path')
- if key in OPAQUE_FILES:need(same_typed(row,OPAQUE_FILES[key]),'D446 historical fixture metadata changed: '+str(path));return
- exact(row,['kind','device','inode','bytes','mode','uid','gid','nlink','mtime_ns','ctime_ns'],'D450 opaque copy fields')
- need(row['kind']=='opaque_file' and all(integer(row[n]) for n in row if n!='kind') and row['inode']>0,'D450 opaque copy integer identity')
- need({n:row[n] for n in ('device','bytes','mode','uid','gid','nlink')}=={'device':16777232,'bytes':12,'mode':0,'uid':501,'gid':20,'nlink':1},'D450 opaque copy metadata policy')
-def require_opaque_presence(root,observed):
- if Path(root)==ROOT:need(all(str(Path(root)/name) in observed for name in OPAQUE_FILES),'known D446 historical fixture missing')
+def fixture_tree(root,base):
+ base=Path(base);need(str(base) in {str(Path(root)/n) for n in FIXTURE_FORESTS},'unknown fixture forest root')
+ need(all(stat.S_ISDIR(parent.lstat().st_mode) for parent in base.parents),'fixture forest ancestors must be ordinary directories')
+ need(stat.S_ISDIR(base.lstat().st_mode),'fixture forest root must remain an ordinary directory')
+ fingerprint=hashlib.sha256();count=0;pending=[(base,'.')];originals=set()
+ while pending:
+  path,name=pending.pop();info=path.lstat();mode=info.st_mode
+  kind=next((label for test,label in ((stat.S_ISDIR,'directory'),(stat.S_ISREG,'file'),(stat.S_ISLNK,'symlink'),(stat.S_ISFIFO,'fifo'),(stat.S_ISSOCK,'socket'),(stat.S_ISCHR,'character'),(stat.S_ISBLK,'block')) if test(mode)),None)
+  need(kind is not None,'unknown fixture metadata node type')
+  row={'name':name,'kind':kind,'mode':stat.S_IMODE(mode),'device':info.st_dev,'inode':info.st_ino,'nlink':info.st_nlink,'uid':info.st_uid,'gid':info.st_gid,'bytes':info.st_size,'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns,'target':os.readlink(path) if kind=='symlink' else None}
+  need(all(integer(row[n]) for n in ('mode','device','inode','nlink','uid','gid','bytes','mtime_ns','ctime_ns')),'invalid fixture metadata integers')
+  if Path(root)==ROOT:
+   relative=str(path.relative_to(root))
+   if relative in OPAQUE_FILES:need(stat.S_ISREG(mode) and same_typed(opaque_metadata(info),OPAQUE_FILES[relative]),'original D446 fixture metadata changed');originals.add(relative)
+  fingerprint.update((json.dumps(row,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode());count+=1
+  if kind=='directory':
+   for child in reversed(sorted(os.listdir(path))):pending.append((path/child,child if name=='.' else name+'/'+child))
+ if Path(root)==ROOT and base==Path(root)/FIXTURE_FORESTS[0]:need(originals==set(OPAQUE_FILES),'original D446 fixture missing')
+ return {'kind':'opaque_fixture_tree','schema_version':1,'entries':count,'metadata_sha256':fingerprint.hexdigest()}
+def validate_fixture_tree(row):
+ exact(row,['kind','schema_version','entries','metadata_sha256'],'fixture tree row fields')
+ need(row['kind']=='opaque_fixture_tree' and type(row['schema_version']) is int and row['schema_version']==1 and integer(row['entries'],1),'fixture tree row identity/count');digest(row['metadata_sha256'])
+def require_fixture_forests(root,observed):
+ if Path(root)==ROOT:need(all(str(Path(root)/name) in observed for name in FIXTURE_FORESTS),'mandatory fixture forest missing')
+def preserved_paths(base,root):
+ # Prune only the two exact forests. Their roots are emitted for metadata capture.
+ closed={str(Path(root)/n) for n in FIXTURE_FORESTS};yield Path(base)
+ def failed(error):raise error
+ for parent,dirs,files in os.walk(base,followlinks=False,onerror=failed):
+  if str(parent) in closed:dirs[:]=[];continue
+  if Path(base)==Path(root) and Path(parent)==Path(root):dirs[:]=[n for n in dirs if n!='.git'];files=[n for n in files if n!='.git']
+  for name in sorted(dirs+files):yield Path(parent)/name
+  dirs[:]=[name for name in dirs if str(Path(parent)/name) not in closed]
 def loads(data,limit=MAX_CONTROL):
  need(type(data) in (bytes,str) and len(data if type(data) is bytes else data.encode())<=limit,'JSON size bound')
  def pairs(rows):
@@ -175,19 +190,19 @@
  need(cpp==CPP and c==C,'fixed ordered16-unit recipe changed');return {'cpp':cpp,'c':c}
 
 def validate_preservation(p,root=ROOT):
- exact(p,['files','directories','links','absent_roots','opaque_files'],'preservation record fields')
+ exact(p,['files','directories','links','absent_roots','opaque_fixture_trees'],'preservation record fields')
  need(type(p['files']) is dict and type(p['links']) is dict,'preservation maps')
- for name,h in p['files'].items():absolute(name);digest(h);need(opaque_key(root,name) is None,'D446 fixture cannot be a hashed input')
- need(type(p['opaque_files']) is dict,'opaque preservation map')
- for name,row in p['opaque_files'].items():
-  absolute(name);validate_opaque_identity(root,name,row)
- require_opaque_presence(root,p['opaque_files'])
+ for name,h in p['files'].items():absolute(name);digest(h);need(fixture_forest(root,name) is None,'D446 fixture cannot be a hashed input')
+ need(type(p['opaque_fixture_trees']) is dict,'fixture tree preservation map')
+ for name,row in p['opaque_fixture_trees'].items():
+  absolute(name);need(name in {str(Path(root)/n) for n in FIXTURE_FORESTS},'unknown fixture forest row');validate_fixture_tree(row)
+ require_fixture_forests(root,p['opaque_fixture_trees'])
  for name,row in p['links'].items():
-  absolute(name);need(opaque_key(root,name) is None,'D446 fixture cannot become a link');exact(row,['target','mode'],'opaque link record');need(type(row['target']) is str and integer(row['mode'],0,0o7777),'opaque link metadata')
+  absolute(name);need(fixture_forest(root,name) is None,'D446 fixture cannot become a link');exact(row,['target','mode'],'opaque link record');need(type(row['target']) is str and integer(row['mode'],0,0o7777),'opaque link metadata')
  for key in ('directories','absent_roots'):
   need(type(p[key]) is list and p[key]==sorted(set(p[key])),'preservation sorted unique paths')
-  for name in p[key]:absolute(name);need(opaque_key(root,name) is None,'D446 fixture changed preservation kind')
- kinds=[set(p['files']),set(p['directories']),set(p['links']),set(p['opaque_files']),set(p['absent_roots'])]
+  for name in p[key]:absolute(name);need(fixture_forest(root,name) is None,'D446 fixture changed preservation kind')
+ kinds=[set(p['files']),set(p['directories']),set(p['links']),set(p['opaque_fixture_trees']),set(p['absent_roots'])]
  need(sum(map(len,kinds))==len(set().union(*kinds)),'preservation kinds overlap')
  for missing in p['absent_roots']:need(not any(beneath(n,missing) for group in kinds[:-1] for n in group),'present member inside absent root')
  return p
@@ -266,7 +281,7 @@
  def __init__(self,root=ROOT):
   need(str(Path(root))==str(ROOT),'fixed installed repository required');self.root=str(ROOT);self.consumed=set();self.armed={}
  def ordinary(self,p):
-  if opaque_key(self.root,p) is not None:return False
+  if fixture_forest(self.root,p) is not None:return False
   try:s=Path(p).lstat();return stat.S_ISREG(s.st_mode) and s.st_nlink==1 and self.ordinary_ancestors(p)
   except OSError:return False
  def consume(self,p):
@@ -297,7 +312,7 @@
  def output_safe(self,ident):
   p=Path(attempt(self.root,ident))
   return all(not q.is_symlink() for q in [p,*p.parents])
- def hash(self,p):need(opaque_key(self.root,p) is None,'D446 fixture cannot be consumed/hashed');return file_sha(p,getattr(self,'deadline_check',None))
+ def hash(self,p):need(fixture_forest(self.root,p) is None,'D446 fixture cannot be consumed/hashed');return file_sha(p,getattr(self,'deadline_check',None))
  def size(self,p):return Path(p).stat().st_size
  def mode(self,p):return stat.S_IMODE(Path(p).stat().st_mode)
  def text(self,p):return read_bounded(p,MAX_CONTROL).decode()
@@ -332,27 +347,25 @@
  """Fixed protected forests. Opaque links are lstat records, never traversed.
  Decision/package docs outside forests are independently stable observation inputs.
  """
- root=Path(root);result={'files':{},'directories':[],'links':{},'absent_roots':[],'opaque_files':{}}
+ root=Path(root);result={'files':{},'directories':[],'links':{},'absent_roots':[],'opaque_fixture_trees':{}}
  roots=[root/n for n in ('source','web','bin_unix','packages','config')]
  if browser_sdk is not None:roots.append(Path(browser_sdk))
  if native_sdk is not None:roots.append(Path(native_sdk))
  for base in roots:
   if not base.exists() and not base.is_symlink():result['absent_roots'].append(str(base));continue
-  paths=[base]
-  if base.is_dir() and not base.is_symlink():
-   for parent,dirs,files in os.walk(base,followlinks=False):paths.extend(Path(parent)/name for name in dirs+files)
+  paths=preserved_paths(base,root)
   for p in paths:
    if active and (p==Path(active) or Path(active) in p.parents):continue
    # Parent container adds no ordinary files and is declared phase metadata.
    if active and omit_container and p==root/'web/server/blackwood-candidate-attempts':continue
-   st=p.lstat();name=str(p);opaque=opaque_row(root,p,st)
-   if opaque is not None:result['opaque_files'][name]=opaque
+   st=p.lstat();name=str(p)
+   if name in {str(root/n) for n in FIXTURE_FORESTS}:result['opaque_fixture_trees'][name]=fixture_tree(root,p)
    elif stat.S_ISLNK(st.st_mode):result['links'][name]={'target':os.readlink(p),'mode':stat.S_IMODE(st.st_mode)}
    elif stat.S_ISREG(st.st_mode):result['files'][name]=file_sha(p)
    elif stat.S_ISDIR(st.st_mode):result['directories'].append(name)
    else:raise Refused('special preserved member')
  for k in ('directories','absent_roots'):result[k]=sorted(set(result[k]))
- for k in ('files','links','opaque_files'):result[k]=dict(sorted(result[k].items()))
+ for k in ('files','links','opaque_fixture_trees'):result[k]=dict(sorted(result[k].items()))
  return validate_preservation(result,root)
 
 def inventory(root,resolve_links=True):
@@ -497,18 +510,19 @@
  out={};root=Path(root)
  for base in [root,*([Path(browser_sdk)] if browser_sdk is not None else []),*([Path(native_sdk)] if native_sdk is not None else [])]:
   if not base.exists():continue
-  for p in base.rglob('*'):
+  for p in preserved_paths(base,root):
+   if p==base:continue
    if base==root and '.git' in p.relative_to(root).parts:continue
    if active and (p==Path(active) or Path(active) in p.parents):continue
    if omit_container and p==root/'web/server/blackwood-candidate-attempts':continue
-   info=p.lstat();row={'mode':stat.S_IMODE(info.st_mode)};opaque=opaque_row(root,p,info)
-   if opaque is not None:row=opaque
+   info=p.lstat();row={'mode':stat.S_IMODE(info.st_mode)}
+   if str(p) in {str(root/n) for n in FIXTURE_FORESTS}:row=fixture_tree(root,p)
    elif stat.S_ISLNK(info.st_mode):row.update(kind='symlink',target=os.readlink(p))
    elif stat.S_ISREG(info.st_mode):row.update(kind='file',bytes=info.st_size,sha256=file_sha(p))
    elif stat.S_ISDIR(info.st_mode):row.update(kind='directory')
    else:raise Refused('special protected file')
    out[str(p)]=row
- require_opaque_presence(root,out)
+ require_fixture_forests(root,out)
  return dict(sorted(out.items()))
 
 def macho(data,kind):
```

## test_preparation.py

```diff
--- T268-accepted/test_preparation.py
+++ T270/test_preparation.py
@@ -212,7 +212,7 @@
  def exists(self,p):q=self.mapped(p);return q.exists() or q.is_symlink()
  def file_stat(self,p):return self.mapped(p).lstat()
  def ordinary(self,p):
-  if stage.opaque_key(self.root,p) is not None:return False
+  if stage.fixture_forest(self.root,p) is not None:return False
   try:s=self.file_stat(p);return stat.S_ISREG(s.st_mode) and s.st_nlink==1 and self.ordinary_ancestors(p)
   except OSError:return False
  def canonical(self,p):
@@ -690,90 +690,80 @@
     else:ops.kill(child,lambda:None);assert ops.wait(child,1)==0 and events==['signal','wait']
    f.case_observation={'backend':variant,'events':events,'anchor_lost':ops.wait_adapter.anchor_lost,'returncode':child.returncode}
   add('D235_backend_'+variant,backend)
- for variant in ('known_without_open','readable_hash_unchanged','unknown_unreadable','unknown_path','unknown_field','bool_mode','hashed_promotion','consume_promotion','missing_known','file_type','device','inode','bytes','mode','uid','gid','nlink','mtime_ns','ctime_ns'):
-  def opaque_case(f,variant=variant):
-   expected={};metadata={}
-   for name in stage.OPAQUE_FILES:
-    p=f.put(name,b'FIXTURE_ONLY');metadata[str(p)]=opaque_test_stat(p.lstat());expected[name]=stage.opaque_metadata(metadata[str(p)])
-   keys=set(str(Path(f.root)/n) for n in expected);first=next(iter(expected));path=Path(f.root)/first;original=stage.file_sha;reads=[]
-   def observed(p,*args,**kwargs):
-    name=str(p);reads.append(name)
-    if name in keys:raise AssertionError('D446 fixture opened instead of metadata preservation')
-    if name.endswith('/UNKNOWN_UNREADABLE'):raise PermissionError('FIXTURE_ONLY unknown unreadable file')
-    return original(p,*args,**kwargs)
-   with patch.object(stage,'OPAQUE_FILES',expected),patch.object(stage,'file_sha',observed),patch.object(Path,'lstat',injected_lstat(metadata,Path.lstat)):
-    if variant=='unknown_unreadable':
-     unknown=f.put('web/UNKNOWN_UNREADABLE');refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root));assert str(unknown) in reads;return
-    preserved=f.view.preservation();protected=stage.protected_inventory(f.root)
-    assert set(preserved['opaque_files'])==keys and all(protected[n]==preserved['opaque_files'][n] for n in keys) and not (keys&set(reads))
-    if variant=='known_without_open':pass
-    elif variant=='missing_known':
-     path.unlink();changed=copy.deepcopy(preserved);changed['opaque_files'].pop(str(path))
-     with patch.object(stage,'ROOT',Path(f.root)):
-      refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root));refused(lambda:stage.validate_preservation(changed,f.root))
-    elif variant=='readable_hash_unchanged':
-     normal=Path(f.root)/'source/src/sound.h';before=preserved['files'][str(normal)];normal.write_bytes(b'FIXTURE_ONLY_CHANGED');assert f.view.preservation()['files'][str(normal)]!=before
-    elif variant=='consume_promotion':
-     assert not NATIVE_VIEW.ordinary(f.view,str(path)) and not f.view.consume(str(path));refused(lambda:NATIVE_VIEW.hash(f.view,str(path)))
-     doc={'schema_version':1,'kind':'SOURCE_INPUT_MANIFEST','source_revision':'1'*40,'entries':[{'path':first,'bytes':12,'mode':0o644,'sha256':'0'*64}]}
-     refused(lambda:stage.source_manifest(doc,'1'*40,f.view,f.root))
-     f.view.declared_inputs={str(path):'0'*64};refused(lambda:stage.dependency_paths('/FIXTURE_ONLY.o: '+str(path),'/FIXTURE_ONLY.o',f.view,f.ident))
-    elif variant in ('unknown_path','unknown_field','bool_mode','hashed_promotion'):
-     changed=copy.deepcopy(preserved);row=changed['opaque_files'][str(path)]
-     if variant=='unknown_path':changed['opaque_files'][str(path)+'_UNKNOWN']=changed['opaque_files'].pop(str(path))
-     elif variant=='unknown_field':row['extra']=True
-     elif variant=='bool_mode':row['mode']=False
-     else:changed['files'][str(path)]='0'*64;changed['opaque_files'].pop(str(path))
+ # D453 retires the superseded D446/D450 live per-file schema cases.
+ # Their immutable pass7/pass8 snapshots/results remain; original202 cases above stay.
+ for variant in ('deterministic_no_open','injected_node_kinds','add_member','remove_member','inode','mtime','ctime','mode','uid','gid','nlink','bytes','raw_link','row_extra','row_kind','row_version','row_count_bool','row_digest','unknown_root','outside_unreadable','outside_special','consumed_promotion','root_type','missing_forest','missing_original','changed_original'):
+  def tree_case(f,variant=variant):
+   metadata={};tree_paths=[]
+   for forest in stage.FIXTURE_FORESTS:
+    for name in ('readable.txt','nested/leaf.bin','unreadable','fifo','socket','link'):
+     p=f.put(forest+'/'+name,b'FIXTURE_ONLY');tree_paths.append(p)
+     if name in ('unreadable','fifo','socket','link'):
+      info=opaque_test_stat(p.lstat());info.st_mode={'unreadable':stat.S_IFREG,'fifo':stat.S_IFIFO|0o644,'socket':stat.S_IFSOCK|0o644,'link':stat.S_IFLNK|0o755}[name];metadata[str(p)]=info
+   base=Path(f.root)/stage.FIXTURE_FORESTS[0];leaf=base/'unreadable';original_read=stage.file_sha;original_lstat=Path.lstat;original_link=os.readlink;original_list=os.listdir;reads=[];links={'target':'/FIXTURE_ONLY/NO_TRAVERSAL'};expected={}
+   if variant in ('missing_forest','missing_original','changed_original'):
+    for name in stage.OPAQUE_FILES:
+     p=f.put(name,b'FIXTURE_ONLY');metadata[str(p)]=opaque_test_stat(p.lstat());expected[name]=stage.opaque_metadata(metadata[str(p)])
+   outside=f.put('web/OUTSIDE_UNREADABLE') if variant=='outside_unreadable' else f.put('web/OUTSIDE_SPECIAL') if variant=='outside_special' else None
+   if variant=='outside_special':metadata[str(outside)]=opaque_test_stat(outside.lstat());metadata[str(outside)].st_mode=stat.S_IFIFO|0o644
+   def read(path,*args,**kwargs):
+    if stage.fixture_forest(f.root,str(path)) is not None:raise AssertionError('fixture content opened')
+    reads.append(str(path))
+    if path==outside:raise PermissionError('FIXTURE_ONLY outside unreadable')
+    return original_read(path,*args,**kwargs)
+   def link(path,*args,**kwargs):
+    if str(path) in metadata and stat.S_ISLNK(metadata[str(path)].st_mode):return links['target']
+    return original_link(path,*args,**kwargs)
+   def listing(path):
+    if str(path) in metadata and stat.S_ISLNK(metadata[str(path)].st_mode):raise AssertionError('fixture symlink traversed')
+    return original_list(path)
+   with patch.object(Path,'lstat',injected_lstat(metadata,original_lstat)),patch.object(stage,'file_sha',read),patch.object(os,'readlink',link),patch.object(os,'listdir',listing):
+    if outside is not None:
+     refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root));return
+    preserved=f.view.preservation();protected=stage.protected_inventory(f.root);rows=preserved['opaque_fixture_trees'];keys={str(Path(f.root)/n) for n in stage.FIXTURE_FORESTS}
+    assert set(rows)==keys and all(protected[n]==rows[n] for n in keys)
+    assert preserved==f.view.preservation() and protected==stage.protected_inventory(f.root)
+    if variant in ('deterministic_no_open','injected_node_kinds'):assert all(row['entries']==8 for row in rows.values())
+    elif variant=='consumed_promotion':
+     for path in (base,base/'readable.txt'):
+      assert not NATIVE_VIEW.ordinary(f.view,str(path)) and not f.view.consume(str(path));refused(lambda path=path:NATIVE_VIEW.hash(f.view,str(path)))
+     doc={'schema_version':1,'kind':'SOURCE_INPUT_MANIFEST','source_revision':'1'*40,'entries':[{'path':stage.FIXTURE_FORESTS[0]+'/readable.txt','bytes':12,'mode':0o644,'sha256':'0'*64}]};refused(lambda:stage.source_manifest(doc,'1'*40,f.view,f.root))
+     f.view.declared_inputs={str(base/'readable.txt'):'0'*64};refused(lambda:stage.dependency_paths('/FIXTURE_ONLY.o: '+str(base/'readable.txt'),'/FIXTURE_ONLY.o',f.view,f.ident))
+    elif variant.startswith('row_') or variant=='unknown_root':
+     changed=copy.deepcopy(preserved);row=changed['opaque_fixture_trees'][str(base)]
+     if variant=='row_extra':row['unknown']=0
+     elif variant=='row_kind':row['kind']='file'
+     elif variant=='row_version':row['schema_version']=True
+     elif variant=='row_count_bool':row['entries']=True
+     elif variant=='row_digest':row['metadata_sha256']='bad'
+     else:changed['opaque_fixture_trees'][str(base)+'_UNKNOWN']=changed['opaque_fixture_trees'].pop(str(base))
      refused(lambda:stage.validate_preservation(changed,f.root))
+    elif variant in ('missing_forest','missing_original','changed_original'):
+     with patch.object(stage,'ROOT',Path(f.root)),patch.object(stage,'OPAQUE_FILES',expected):
+      f.view.preservation();stage.protected_inventory(f.root)
+      if variant=='missing_forest':
+       missing=copy.deepcopy(preserved);missing['opaque_fixture_trees'].pop(str(base));refused(lambda:stage.validate_preservation(missing,f.root))
+       other=Path(f.root)/stage.FIXTURE_FORESTS[1]
+       for member in sorted(other.rglob('*'),key=lambda p:len(p.parts),reverse=True):
+        if member.is_dir():member.rmdir()
+        else:member.unlink()
+       other.rmdir();refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root));return
+      original=Path(f.root)/next(iter(expected))
+      if variant=='missing_original':original.unlink()
+      else:metadata[str(original)].st_ino+=1
+      refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root))
+    elif variant=='root_type':
+     metadata[str(base)]=opaque_test_stat(original_lstat(base));refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root))
     else:
-     info=path.lstat();fields={n:getattr(info,n) for n in ('st_mode','st_dev','st_ino','st_size','st_uid','st_gid','st_nlink','st_mtime_ns','st_ctime_ns')}
-     attribute={'file_type':'st_mode','device':'st_dev','inode':'st_ino','bytes':'st_size','mode':'st_mode','uid':'st_uid','gid':'st_gid','nlink':'st_nlink','mtime_ns':'st_mtime_ns','ctime_ns':'st_ctime_ns'}[variant]
-     fields[attribute]=stat.S_IFDIR if variant=='file_type' else fields[attribute]+1
-     refused(lambda:stage.opaque_row(f.root,path,types.SimpleNamespace(**fields)))
-    f.case_observation={'variant':variant,'opaque_count':len(keys),'known_file_content_reads':len(keys&set(reads)),'classification':'SIMULATED_METADATA'}
-  add('D446_'+variant,opaque_case)
- for variant in ('known_closed_set','unknown_case','unknown_index','unknown_pass','unknown_suffix','file_type','mode','bytes','uid','gid','device','nlink','bool_inode','negative_time','extra_field','consume_promotion','inode_changed','mtime_changed','ctime_changed'):
-  def copy_case(f,variant=variant):
-   name=sorted(stage.OPAQUE_COPY_PATHS)[0]
-   replacements={'unknown_case':('D446_known_without_open','D446_UNKNOWN'),'unknown_index':('001-D446','099-D446'),'unknown_pass':('/pass-7/','/pass-8/'),'unknown_suffix':('/bad-mode','/UNKNOWN_BAD_MODE')}
-   if variant in replacements:
-    old,new=replacements[variant];name=name.replace(old,new)
-   names=sorted(stage.OPAQUE_COPY_PATHS) if variant=='known_closed_set' else [name];metadata={}
-   for member in names:
-    p=f.put(member,b'FIXTURE_ONLY');metadata[str(p)]=opaque_test_stat(p.lstat())
-   path=Path(f.root)/name;original=stage.file_sha;attempts=[]
-   def read(p,*args,**kwargs):
-    if str(p) in metadata:
-     attempts.append(str(p))
-     if variant in replacements:raise PermissionError('FIXTURE_ONLY unknown unreadable copy')
-     raise AssertionError('known copy opened for content')
-    return original(p,*args,**kwargs)
-   with patch.object(stage,'file_sha',read),patch.object(Path,'lstat',injected_lstat(metadata,Path.lstat)):
-    if variant in replacements:
-     refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root));assert attempts;return
-    preserved=f.view.preservation();protected=stage.protected_inventory(f.root);row=preserved['opaque_files'][str(path)]
-    assert set(preserved['opaque_files'])==set(metadata) and protected[str(path)]==row and not attempts
-    if variant=='known_closed_set':assert len(metadata)==133
-    elif variant=='consume_promotion':
-     assert not NATIVE_VIEW.ordinary(f.view,str(path)) and not f.view.consume(str(path));refused(lambda:NATIVE_VIEW.hash(f.view,str(path)))
-     doc={'schema_version':1,'kind':'SOURCE_INPUT_MANIFEST','source_revision':'1'*40,'entries':[{'path':name,'bytes':12,'mode':0o644,'sha256':'0'*64}]};refused(lambda:stage.source_manifest(doc,'1'*40,f.view,f.root))
-     f.view.declared_inputs={str(path):'0'*64};refused(lambda:stage.dependency_paths('/FIXTURE_ONLY.o: '+str(path),'/FIXTURE_ONLY.o',f.view,f.ident))
-    elif variant in ('inode_changed','mtime_changed','ctime_changed'):
      f.auth['observation']['preservation']=preserved;f.write();f.gate()
-     attribute={'inode_changed':'st_ino','mtime_changed':'st_mtime_ns','ctime_changed':'st_ctime_ns'}[variant];setattr(metadata[str(path)],attribute,getattr(metadata[str(path)],attribute)+1)
-     refused(f.gate);assert stage.protected_inventory(f.root)[str(path)]!=protected[str(path)]
-    elif variant=='file_type':
-     metadata[str(path)].st_mode=stat.S_IFDIR;refused(f.view.preservation);refused(lambda:stage.protected_inventory(f.root))
-    else:
-     changed=copy.deepcopy(preserved);altered=changed['opaque_files'][str(path)]
-     if variant=='extra_field':altered['unknown']=0
-     elif variant=='bool_inode':altered['inode']=True
-     elif variant=='negative_time':altered['ctime_ns']=-1
-     else:altered[variant]+=1
-     refused(lambda:stage.validate_preservation(changed,f.root))
-    assert not attempts
-    f.case_observation={'variant':variant,'known_copy_count':len(metadata),'known_content_reads':len(attempts),'actual_files_readable':True,'metadata_and_read_denial':'INJECTED_ONLY'}
-  add('D450_'+variant,copy_case)
+     if variant=='add_member':f.put(stage.FIXTURE_FORESTS[0]+'/ADDED')
+     elif variant=='remove_member':(base/'readable.txt').unlink()
+     elif variant=='raw_link':links['target']='/FIXTURE_ONLY/CHANGED'
+     else:
+      attribute={'inode':'st_ino','mtime':'st_mtime_ns','ctime':'st_ctime_ns','mode':'st_mode','uid':'st_uid','gid':'st_gid','nlink':'st_nlink','bytes':'st_size'}[variant];setattr(metadata[str(leaf)],attribute,getattr(metadata[str(leaf)],attribute)+1)
+     refused(f.gate);assert stage.protected_inventory(f.root)[str(base)]!=protected[str(base)]
+    f.case_observation={'variant':variant,'tree_rows':rows,'fixture_content_reads':0,'new_physical_files':'READABLE; special/unreadable/link metadata INJECTED'}
+  add('D453_'+variant,tree_case)
  return rows
 
 def main():
```

## SCHEMA.md

```diff
--- T268-accepted/SCHEMA.md
+++ T270/SCHEMA.md
@@ -1,6 +1,6 @@
 # Blackwood native preparation schema
 
-Authority: accepted T1671.2/D444 and T265/D448 plus T2681.0/D450, BLACKWOOD_NATIVE_BUILD_PREPARATION0.3, with D235's fixed Darwin nonreaping adapter. Source and guarded SIMULATED preparation only. No current actual plan/build/verify/tool/signing/copy/runtime authority.
+Authority: accepted prior preparations plus T2701.0/D453, BLACKWOOD_NATIVE_BUILD_PREPARATION0.4, with D235's fixed Darwin nonreaping adapter. Source and guarded SIMULATED preparation only. No current actual plan/build/verify/tool/signing/copy/runtime authority.
 
 Every object below has exactly the named fields. Maps have the constrained key/value types stated below, not extension dictionaries. Unknown fields, duplicate JSON keys, nonfinite floats, bool-as-int, noncanonical paths, aliases and overlaps refuse. Generated JSON is sorted-key, indented two spaces, ASCII, LF terminated, with finite numbers. Control/manifest/plan ceilings are32MiB; report/freeze128MiB. Byte counts and integer metadata are nonnegative integers excluding bool; digests are64 lowercase hexadecimal characters. File reads require ordinary single-link data and ordinary ancestors, except the explicitly named installed launcher roles. Successful reports/verification cannot contain partial/null records.
 
@@ -10,11 +10,13 @@
 
 `SourceAcceptance` is exactly `{ticket:"T163",decision:Reference,handoff:Reference,evidence:Reference,files:[FileRef x4]}`. `Reference` is exactly `{path:relative,sha256:SHA}`. The three fixed D223/final-handoff/MAIN-review paths and digests and four sorted source files/hashes are literal stage.py constants from approved BLACKWOOD_BUILD_PREPARATION0.1. All source sizes/modes/current bytes are checked. Native does not have to consume the browser-only private header. Fixture subclasses replace source DATA identities solely inside guarded fakes and remain barred from real authorization.
 
-`Preservation` is exactly `{files:{absolute:SHA},directories:[absolute sorted unique],links:{absolute:{target:string,mode:uint<=4095}},opaque_files:{absolute:OpaqueFile},absent_roots:[absolute sorted unique]}`. Kinds are disjoint; no present descendant is hidden by an absent root. Historical links are opaque lstat records, never consumed or traversed. The selected authorization's expected external digest/current ordinary identity is checked independently before/after work; it does not hash itself through observation or source manifest. Only the exact new current attempt and a predeclared absent parent container can differ. Full original protection also includes unconsumed history, not only declared compiler inputs.
+`Preservation` is exactly `{files:{absolute:SHA},directories:[absolute sorted unique],links:{absolute:{target:string,mode:uint<=4095}},opaque_fixture_trees:{absolute:FixtureTree},absent_roots:[absolute sorted unique]}`. Kinds are disjoint; no present descendant is hidden by an absent root. Outside the two exact fixture forests, readable files retain content hashes and historical symlinks retain opaque raw metadata, never traversed; unreadable/special nodes refuse. Full original protection includes unconsumed history. The control is independently digested and does not reference itself. Only the current owned attempt and a predeclared absent parent container may differ.
 
-D446 `OpaqueFile` is exactly `{kind:"opaque_file",device,inode,bytes,mode,uid,gid,nlink,mtime_ns,ctime_ns}` with every numeric field an integer excluding bool, equal to the literal seven path/metadata records in stage.OPAQUE_FILES and D446. These twelve-byte mode0000 historical fixtures are lstat-only, with no content verification available. The same exact row appears in protected_inventory. Production preservation validation and protected inventory require all seven known paths to remain present; synthetic roots do not require actual inode-bound artifacts. Only exact repository-relative paths qualify; unknown unreadable paths fail normal hashing, with no PermissionError fallback. Altered metadata/type, unknown fields/path, hashed/link/directory/absent-kind promotion or consumed source/header/tool/framework/SDK/dependency use refuses. Readable originals retain byte-hash preservation. No permission or original artifact changes are allowed.
+D453 `FixtureTree` is exactly `{kind:"opaque_fixture_tree",schema_version:1,entries:positiveUInt,metadata_sha256:SHA}`. It replaces all individual descendant preservation rows for exactly `web/repro/tests/prerequisites` and `web/server/blackwood_candidate/supervisor-fixtures-1`. The same compact row appears in protected_inventory. Actual repository observation requires both ordinary roots; synthetic roots may omit them. No other root/path qualifies. Both roots and every descendant are forbidden consumed source/header/tool/SDK/framework/manifest/dependency roles even when readable. D446's seven original literal metadata records and presence are checked inside the first production forest; D450's per-copy roster and the per-file opaque schema are superseded. Old snapshots/results stay intact.
 
-D450 extends this same row type only to `web/server/blackwood_candidate/supervisor-fixtures-1/pass-7/` + one of the19 literal `OPAQUE_COPY_CASES` directory strings + one of the seven exact D446 suffixes. The roster is pinned by accepted plan-pass-7 SHA256a2dfd976759128145ae861390cb98473efbd77af7e3ab8185a22aed4e0faae40; at most133 paths, with no presence requirement for copies. Original seven mandatory identities/presence remain unchanged. Copy rows require ordinary files, device16777232/bytes12/mode0/uid501/gid20/nlink1. All numeric fields exclude bool, fit0..2^63-1, and inode is positive. Actual observation/control binds each inode/mtime/ctime; full before/after equality detects changes. Unknown pass/index/case/suffix and consumed promotion refuse. No generic unreadable-prefix or PermissionError exemption exists. New targeted tests use readable files and injected lstat/read denial, never new physical mode0000 copies.
+The metadata fingerprint streams the root (`name:"."`) and every descendant in sorted depth-first order without following symlinks or opening file contents. Each entry is one compact sorted-key ASCII JSON object plus LF, exactly `{name,kind,mode,device,inode,nlink,uid,gid,bytes,mtime_ns,ctime_ns,target}`. Names are root-relative; target is raw symlink text or null. Kinds are directory/file/symlink/fifo/socket/character/block; numeric metadata are integers excluding bool in0..2^63-1. Entry count includes the root. SHA256 is over this complete ordered stream; rows are discarded after hashing. Root ancestors must be ordinary directories. Inaccessible directory membership refuses. Full before/after tree-row equality detects membership/type/identity/mode/ownership/link/size/time/raw-target changes. Fixture content integrity is explicitly unavailable; same-size content changes with unchanged metadata are not claimed detectable. All actual build inputs retain SHA256 content checks.
+
+New targeted tests retain readable physical files only and inject lstat/raw-link/read-denial boundaries, including FIFO/socket/unreadable observations. The original202 general native cases remain live; obsolete D446/D450 per-file schema cases are retired from the live harness only, preserving pass7/pass8 evidence. No runtime/build effect follows.
 
 `FrameworkInventory` is a sorted map of relative paths to exactly one of `{kind:"file",mode:uint,bytes:uint,sha256:SHA}`, `{kind:"directory",mode:uint}`, `{kind:"symlink",mode:493,target:relativeRaw,resolved:relativeTerminal}`. It includes all source membership/licenses/Info/headers/binaries and exactly the seven named confined SDL/hidapi links from stage.FRAMEWORK_LINKS. Ordinary members are single-link. Original SDL2/hidapi hashes are fixed unsigned identities; copied post-sign hashes are observed separately. Physical copies have different device/inode identity from originals. Only the two copied binaries plus their exact `_CodeSignature` directories/CodeResources may change; added signature members have their expected directory/file kinds with actual modes recorded, existing kind/mode unchanged. Nested hidapi signing precedes parent SDL2, no --deep and no explicit ac_server signing.
 
```

## README.md

```diff
--- T268-accepted/README.md
+++ T270/README.md
@@ -2,9 +2,9 @@
 
 T1671.2 / D443 resumes these six existing files and guarded simulated preparation under D232. D235 adds the fixed lazy Darwin nonreaping adapter. T162 is closed; T149 and QA remain held. Nothing here currently authorizes real project planning, compiler/version/tool inspection, native signing/copy/build/verify, browser/server/network/runtime or Git operations.
 
-T167 preparation is accepted D444. T2651.0/D446 under BLACKWOOD_NATIVE_BUILD_PREPARATION0.2 adds only seven exact historical mode0000 fixture identities as lstat-only preservation rows. Their content cannot be verified; they are never consumed inputs. Unknown unreadable files still refuse; every readable original remains hashed. Targeted guarded pass-7 retains the original202-case definitions and includes the existing full fake build/verifier success. No T264 observation retry, original chmod or actual build is authorized by this correction.
+T2701.0/D453 under BLACKWOOD_NATIVE_BUILD_PREPARATION0.4 replaces the superseded per-file fixture exceptions with two exact non-consumed forests: web/repro/tests/prerequisites and web/server/blackwood_candidate/supervisor-fixtures-1. Complete sorted lstat metadata is streamed into a compact fingerprint/count per tree; no fixture contents are opened or symlinks followed. Both production roots and the seven original fixed D446 identities remain required. Outside those roots, readable hashes and unknown unreadable/special refusals remain. Every forest descendant is forbidden as a consumed input, including readable files. Fixture content proof is unavailable.
 
-T2681.0/D450 under preparation0.3 additionally recognizes only the finite retained pass-7 D446 case copies of those seven suffixes (19 exact indexed directory names, at most133 paths). Copy inode/timestamps are bound by the observed control and before/after equality; original seven literal pins and mandatory presence are unchanged. Guarded pass-8 uses readable synthetic files with injected lstat/read denial, preventing new unreadable retained artifacts. Old pass-7 data stays unchanged; no T267 retry or actual build follows from this correction.
+Targeted guarded pass-9 uses readable synthetic files and injected metadata/read-denial boundaries. It includes complete fake build/verifier success plus tree membership/metadata/shape/promotion refusals. Only obsolete D446/D450 live per-file schema cases are retired; all original202 native cases and old snapshots/results stay intact. No actual observation retry, original mutation or build is authorized here.
 
 The accepted native recipe is retained as source DATA from the five pinned web/server/candidate baseline files. No old module is imported or run. Baseline byte copies and pins are under preparation-1/baseline. Preparation evidence records bounded source diffs and exact source/authority/fixture pins before each justified fresh pass. The native successor is disjoint from T164's browser implementation and imports none of it.
 
```
