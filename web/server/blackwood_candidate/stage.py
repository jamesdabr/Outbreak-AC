"""T167 fixed native recipe, strict data gates and confined staging. No import effects."""
import hashlib,json,os,re,shlex,stat,struct,sys,shutil,subprocess,selectors,signal,math
from pathlib import Path,PurePosixPath

ROOT=Path(__file__).absolute().parents[3]
SDK='/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk'
SDK_PTHREAD_ALIAS=(SDK+'/usr/include/pthread.h','pthread/pthread.h',0o755,SDK+'/usr/include/pthread/pthread.h')
SDK_SCHED_ALIAS=(SDK+'/usr/include/sched.h','pthread/sched.h',0o755,SDK+'/usr/include/pthread/sched.h')
SDK_HEADER_ALIASES=(SDK_PTHREAD_ALIAS,SDK_SCHED_ALIAS)
SDK_LINK_ALIASES={
 SDK+'/usr/lib/'+leaf:(SDK+'/usr/lib/'+target,tuple((SDK+'/usr/lib/'+edge,raw) for edge,raw in edges))
 for leaf,target,edges in (
 ('libc++.tbd','libc++.1.tbd',(('libc++.tbd','libc++.1.tbd'),)),
 ('libz.tbd','libz.1.tbd',(('libz.tbd','libz.1.tbd'),)),
 ('libSystem.tbd','libSystem.B.tbd',(('libSystem.tbd','libSystem.B.tbd'),)),
 ('libpthread.tbd','libSystem.B.tbd',(('libpthread.tbd','libSystem.tbd'),('libSystem.tbd','libSystem.B.tbd'))))}
CLT='/Library/Developer/CommandLineTools'
PYTHON='/Library/Frameworks/Python.framework/Versions/3.11'
FRAMEWORK='source/xcode/Frameworks/SDL2.framework'
CPP=['source/src/'+n+'.cpp' for n in ('crypto','log','protocol','serverms','server','stream','tools','wizard')]
C=['source/enet/'+n+'.c' for n in ('callbacks','compress','host','list','packet','peer','protocol','unix')]
TOOLS={'cc':'/usr/bin/clang','cxx':'/usr/bin/clang++','codesign':'/usr/bin/codesign','otool':'/usr/bin/otool','file':'/usr/bin/file'}
SCRIPT_NAMES=('stage.py','build.py','verify.py','test_preparation.py','SCHEMA.md','README.md')
CLAIMS={k:False for k in ('native_runtime','gameplay','multiplayer','authority','P0')}
MAX_LOG=8*1024*1024
MAX_CONTROL=32*1024*1024
MAX_RECORD=128*1024*1024
RECIPE='blackwood_native_standalone_v1'
MANIFEST_DIR='web/repro/blackwood-source-manifests'
ASSET_ROOT='web/assets/blackwood-profile'
ASSET_MANIFEST_SHA='8c4f7eef5f0deafb06bec60d62be529a684a30d56bbdc6dc3e5f38dd21c69e60'
ASSET_PROVENANCE_SHA='48b1bbd659fa0193bce88a8d76a9146fa8e84bc981f20c4203c133e26b64b3c3'
ROTATION=b'blackwood_greybox_v1 dm weight:100 repeat:100 time:2 mintime:2 maxtime:2 minplayers:0 maxplayers:8 maxteamsize:8 manual:0\n'
SEED_ROWS=(('packages/maps/blackwood_greybox_v1.cgz','packages/maps/servermaps/blackwood_greybox_v1.cgz',734,'e68314e911130d2822fdfa65d77dfaba302d4f5c3552ff91c698b84768d5ddf1'),('packages/maps/blackwood_greybox_v1.cfg','packages/maps/servermaps/blackwood_greybox_v1.cfg',1677,'289bcb22b29a17443cdf47a936e82edbc47a7a0e0dd034a8b602ce3ec79b76bd'),('notices/blackwood-candidate/LICENSE.txt','notices/blackwood-candidate/LICENSE.txt',1300,'d597a754790e54f9ee13788b3c2f1ded4c0edc60c3d37251c787d5d7f648d47e'),('notices/blackwood-candidate/PROVENANCE.json','notices/blackwood-candidate/PROVENANCE.json',3103,'0da2da2801d55e0afab1abf2ec1d0ed4e25bd4bf41d8a225cad37e5aa8809676'))
SOURCE_HASHES={'source/src/browser_map_profile.h':'614fe93545ea52a4857d7674aae9b92452ba36cac35d952754ca218488aea414','source/src/main.cpp':'1da216b25233639eaaa1f89fb15a6cdbdd6ad3ab90e19989a44ffc77952a07ac','source/src/client.cpp':'0e3be12c5771eb20f4dfb9dbfe5cd239b49a02998d267a0df6b407280fb31b56','source/src/clients2c.cpp':'5368d23331123aa67de430b7c11460efdb5182944b9508f715491b7c6522a4bd'}
SOURCE_REFERENCES={'decision':'notes/decisions/D223-T163-source-helper-acceptance.md','handoff':'notes/handoffs/T163-engine-final-freeze-1.md','evidence':'notes/reviews/MAIN-T163-final-freeze-review-1.json'}
TOOL_HASHES={'cc':'179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818','cxx':'179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818','otool':'179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818','codesign':'214d455584d19abc0d74d02b9cbc7d3da6bdcb0596c235e6156dd9ed2f4e1ba7','file':'a4ba66d26a9cfdc70637c78cdacef920f94147f6aa45ccc73858e493589ef94d'}
FRAMEWORK_LINKS={'Headers':('Versions/Current/Headers','Versions/A/Headers'),'Resources':('Versions/Current/Resources','Versions/A/Resources'),'SDL2':('Versions/Current/SDL2','Versions/A/SDL2'),'Versions/Current':('A','Versions/A'),'Versions/A/Frameworks/hidapi.framework/Resources':('Versions/Current/Resources','Versions/A/Frameworks/hidapi.framework/Versions/A/Resources'),'Versions/A/Frameworks/hidapi.framework/hidapi':('Versions/Current/hidapi','Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi'),'Versions/A/Frameworks/hidapi.framework/Versions/Current':('A','Versions/A/Frameworks/hidapi.framework/Versions/A')}
ADAPTER_HEADER_PINS={'sys/wait.h':'b77f7dd6f592eba8b0d51c15c7b975472fdad50c12ea296f74f062cbf98dcbf7','sys/signal.h':'171af7545ef750627aeba02c1de838c05e2cf396e2f49881ea74dba6990c44a3','sys/_types/_pid_t.h':'052a6dbbec8e30623c2d33dd373992f6c5d0c57c57ed4949d2b48c4ab0976487','sys/_types/_uid_t.h':'d2140a65a17943a857381757c0b73a920f35ade41dc9809437c168be457c276a','sys/_types/_id_t.h':'fb7255c9872e2a805c206796326e21d47146e22c93c09752126d7166bdaba5e5','sys/_types.h':'863c4f07045775002b63b7e616742d9f746e4a02da4441442d8fe1138bbd0ff9','machine/_types.h':'f27264f8fdec9f164b4fc2b556f666ed7c5c0e5b88fd9f23db0b731ffa6cf864','arm/_types.h':'4f0bde85f9a41cc7d30fff22ebd7e8f4eb206a55a926eda012a2e7481e3524fa'}
ADAPTER_STDLIB_ROLES=(PYTHON+'/lib/python3.11/ctypes/__init__.py',PYTHON+'/lib/python3.11/ctypes/_endian.py',PYTHON+'/lib/python3.11/lib-dynload/_ctypes.cpython-311-darwin.so',PYTHON+'/lib/python3.11/platform.py')

# D446: exact historical fixtures, never consumed inputs. No read-error fallback.
OPAQUE_FILES={
 'web/repro/tests/prerequisites/'+name+'/repo/web/build/.cache/bad-mode':
 {'kind':'opaque_file','device':16777232,'inode':inode,'bytes':12,'mode':0,'uid':501,'gid':20,'nlink':1,'mtime_ns':mtime,'ctime_ns':ctime}
 for name,inode,mtime,ctime in (
 ('FIXTURE_ONLY-a6a8xiso',138018950,1794133833737008579,1794133833737028537),
 ('T101/FIXTURE_ONLY-_ul9woy_',138138188,1794136186239760878,1794136186239782419),
 ('FIXTURE_ONLY-am2d_ogp',138048696,1794134709255204182,1794134709255226848),
 ('FIXTURE_ONLY-wxoxh5ho',138002194,1794133651660215054,1794133651660235304),
 ('FIXTURE_ONLY-gx0ewpha',138037844,1794134245530215563,1794134245530245646),
 ('FIXTURE_ONLY-hghnb9_0',138028804,1794134032415877479,1794134032415897853),
 ('FIXTURE_ONLY-ktpjacgc',138010533,1794133723100585246,1794133723100612621))}
FIXTURE_FORESTS=('web/repro/tests/prerequisites','web/server/blackwood_candidate/supervisor-fixtures-1')

class Refused(ValueError):pass
def need(v,why):
 if not v:raise Refused(why)
def exact(v,keys,why):need(type(v) is dict and set(v)==set(keys),why)
def same_typed(left,right):
 if type(left) is not type(right):return False
 if type(left) is dict:return set(left)==set(right) and all(same_typed(left[k],right[k]) for k in left)
 if type(left) is list:return len(left)==len(right) and all(same_typed(a,b) for a,b in zip(left,right))
 return left==right
def integer(v,lo=0,hi=2**63-1):return type(v) is int and lo<=v<=hi
def sha(b):return hashlib.sha256(b).hexdigest()
def file_sha(path,check=None):
 check=(lambda:None) if check is None else check;check()
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  while True:
   check();block=f.read(1048576);check()
   if not block:break
   h.update(block)
 return h.hexdigest()
def read_bounded(path,limit):
 with Path(path).open('rb') as f:data=f.read(limit+1)
 need(len(data)<=limit,'bounded file read exceeded');return data
def digest(s):need(type(s) is str and re.fullmatch('[0-9a-f]{64}',s),'invalid SHA256');return s
def rel(s):
 need(type(s) is str and s and not any(ord(c)<32 for c in s) and '\\' not in s and not s.startswith('/') and all(p not in ('','.','..') for p in s.split('/')),'noncanonical relative path');return s
def absolute(s):
 need(type(s) is str and s.startswith('/') and str(PurePosixPath(s))==s and all(p not in ('.','..') for p in s.split('/')[1:]) and not any(ord(c)<32 for c in s) and '\\' not in s,'noncanonical absolute path');return s
def identifier(s):need(type(s) is str and re.fullmatch('[A-Za-z0-9_-]{1,48}',s),'invalid candidate ID');return s
def manifest_path(ident):return MANIFEST_DIR+'/'+identifier(ident)+'.json'
def exit0_observation(value,pid):
 return integer(pid,1,2**31-1) and same_typed(value,{'pid':pid,'signo':20,'code':1,'status':0,'errno':0})
def beneath(p,base):return p==base or p.startswith(base+'/')
def fixture_forest(root,path):
 prefix=str(Path(root))+'/';name=str(path)
 if not name.startswith(prefix):return None
 relative=name[len(prefix):]
 return next((forest for forest in FIXTURE_FORESTS if beneath(relative,forest)),None)
def opaque_metadata(info):
 return {'kind':'opaque_file','device':info.st_dev,'inode':info.st_ino,'bytes':info.st_size,'mode':stat.S_IMODE(info.st_mode),'uid':info.st_uid,'gid':info.st_gid,'nlink':info.st_nlink,'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns}
def fixture_tree(root,base):
 base=Path(base);need(str(base) in {str(Path(root)/n) for n in FIXTURE_FORESTS},'unknown fixture forest root')
 need(all(stat.S_ISDIR(parent.lstat().st_mode) for parent in base.parents),'fixture forest ancestors must be ordinary directories')
 need(stat.S_ISDIR(base.lstat().st_mode),'fixture forest root must remain an ordinary directory')
 fingerprint=hashlib.sha256();count=0;pending=[(base,'.')];originals=set()
 while pending:
  path,name=pending.pop();info=path.lstat();mode=info.st_mode
  kind=next((label for test,label in ((stat.S_ISDIR,'directory'),(stat.S_ISREG,'file'),(stat.S_ISLNK,'symlink'),(stat.S_ISFIFO,'fifo'),(stat.S_ISSOCK,'socket'),(stat.S_ISCHR,'character'),(stat.S_ISBLK,'block')) if test(mode)),None)
  need(kind is not None,'unknown fixture metadata node type')
  row={'name':name,'kind':kind,'mode':stat.S_IMODE(mode),'device':info.st_dev,'inode':info.st_ino,'nlink':info.st_nlink,'uid':info.st_uid,'gid':info.st_gid,'bytes':info.st_size,'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns,'target':os.readlink(path) if kind=='symlink' else None}
  need(all(integer(row[n]) for n in ('mode','device','inode','nlink','uid','gid','bytes','mtime_ns','ctime_ns')),'invalid fixture metadata integers')
  if Path(root)==ROOT:
   relative=str(path.relative_to(root))
   if relative in OPAQUE_FILES:need(stat.S_ISREG(mode) and same_typed(opaque_metadata(info),OPAQUE_FILES[relative]),'original D446 fixture metadata changed');originals.add(relative)
  fingerprint.update((json.dumps(row,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode());count+=1
  if kind=='directory':
   for child in reversed(sorted(os.listdir(path))):pending.append((path/child,child if name=='.' else name+'/'+child))
 if Path(root)==ROOT and base==Path(root)/FIXTURE_FORESTS[0]:need(originals==set(OPAQUE_FILES),'original D446 fixture missing')
 return {'kind':'opaque_fixture_tree','schema_version':1,'entries':count,'metadata_sha256':fingerprint.hexdigest()}
def validate_fixture_tree(row):
 exact(row,['kind','schema_version','entries','metadata_sha256'],'fixture tree row fields')
 need(row['kind']=='opaque_fixture_tree' and type(row['schema_version']) is int and row['schema_version']==1 and integer(row['entries'],1),'fixture tree row identity/count');digest(row['metadata_sha256'])
def require_fixture_forests(root,observed):
 if Path(root)==ROOT:need(all(str(Path(root)/name) in observed for name in FIXTURE_FORESTS),'mandatory fixture forest missing')
def preserved_paths(base,root):
 # Prune only the two exact forests. Their roots are emitted for metadata capture.
 closed={str(Path(root)/n) for n in FIXTURE_FORESTS};yield Path(base)
 def failed(error):raise error
 for parent,dirs,files in os.walk(base,followlinks=False,onerror=failed):
  if str(parent) in closed:dirs[:]=[];continue
  if Path(base)==Path(root) and Path(parent)==Path(root):dirs[:]=[n for n in dirs if n!='.git'];files=[n for n in files if n!='.git']
  for name in sorted(dirs+files):yield Path(parent)/name
  dirs[:]=[name for name in dirs if str(Path(parent)/name) not in closed]
def loads(data,limit=MAX_CONTROL):
 need(type(data) in (bytes,str) and len(data if type(data) is bytes else data.encode())<=limit,'JSON size bound')
 def pairs(rows):
  out={}
  for k,v in rows:need(k not in out,'duplicate JSON key');out[k]=v
  return out
 def floating(text):
  value=float(text);need(math.isfinite(value),'nonfinite JSON float');return value
 return json.loads(data,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda _:(_ for _ in ()).throw(Refused('nonfinite JSON')))
def canonical_json(value):return json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n'
def attempt(root,ident):return str(Path(root)/'web/server/blackwood-candidate-attempts'/identifier(ident))
def flags(root,ident,mode):
 need(mode in ('release','debug'),'fixed mode only');base=attempt(root,ident)+'/deps-signed'
 return ['-arch','arm64','-isysroot',SDK,'-fsigned-char',*(['-O3','-fomit-frame-pointer'] if mode=='release' else ['-O0','-g','-D_DEBUG']),'-I'+root+'/source/src','-I'+root+'/source/src/bot','-I'+root+'/source/enet/include','-I'+base+'/SDL2.framework/Headers','-F'+base]
def unit_paths(root,ident,mode,unit):
 need(unit in CPP+C,'unknown native unit');base=attempt(root,ident)+'/'+mode;stem=('enet-' if unit in C else '')+Path(unit).stem
 return base+'/'+stem+'.o',base+'/'+stem+'.d',base+'/'+stem+'.pre.d'
def commands(root,ident):
 """Commands are generated constants, never read from authorization data."""
 base=attempt(root,ident);copy=base+'/deps-signed/SDL2.framework';nested=copy+'/Versions/A/Frameworks/hidapi.framework'
 signing=[[TOOLS['codesign'],'--force','--sign','-','--timestamp=none',p] for p in (nested,copy)]
 signature=[[TOOLS['codesign'],'--verify','--verbose=4',p] for p in (nested,nested+'/Versions/A/hidapi',copy,copy+'/Versions/A/SDL2')]
 modes={}
 for mode in ('release','debug'):
  rows=[];objects=[];f=flags(root,ident,mode)
  for unit in CPP+C:
   obj,dep,pre=unit_paths(root,ident,mode,unit);isc=unit in C
   # Preserve lifecycle order: common, language, optimization, includes, standalone.
   args=[TOOLS['cc' if isc else 'cxx'],*f[:5],'-std=gnu99' if isc else '-std=gnu++11',*f[5:],*([] if isc else ['-DSTANDALONE'])]
   rows.append({'unit':unit,'object':obj,'dep':dep,'pre_dep':pre,'discover':[*args,'-M','-MF',pre,'-MT',obj,root+'/'+unit],'compile':[*args,'-MD','-MF',dep,'-c',root+'/'+unit,'-o',obj]});objects.append(obj)
  modes[mode]={'units':rows,'binary':base+'/'+mode+'/ac_server'}
  opt=['-O3','-fomit-frame-pointer'] if mode=='release' else ['-O0','-g','-D_DEBUG']
  modes[mode]['link']=[TOOLS['cxx'],*f[:5],*opt,*objects,'-F'+base+'/deps-signed','-framework','SDL2','-lz','-lpthread','-Wl,-t','-Wl,-rpath,'+base+'/deps-signed','-Wl,-rpath,'+copy+'/Versions/A/Frameworks','-o',modes[mode]['binary']]
 return {'sign':signing,'signature':signature,'modes':modes}

def source_manifest(doc,revision,view,root,manifest_relative=None):
 exact(doc,['schema_version','kind','source_revision','entries'],'source manifest fields')
 need(type(doc['schema_version']) is int and doc['schema_version']==1 and doc['kind']=='SOURCE_INPUT_MANIFEST' and doc['source_revision']==revision,'source manifest identity')
 need(type(doc['entries']) is list and doc['entries'],'empty source manifest');paths=[]
 for e in doc['entries']:
  exact(e,['path','bytes','sha256','mode'],'source entry fields');rel(e['path']);digest(e['sha256']);need(integer(e['bytes']) and type(e['mode']) is int and e['mode'] in (420,493),'source entry mode/size')
  need(e['path']!=(manifest_relative or 'web/repro/blackwood-source-manifest.json'),'manifest self reference');p=root+'/'+e['path'];need(view.ordinary(p) and view.canonical(p)==p and view.hash(p)==e['sha256'] and view.size(p)==e['bytes'] and view.mode(p)==e['mode'],'source entry changed/link');paths.append(e['path'])
 need(paths==sorted(set(paths)),'source entries unique/sorted');return set(paths)

def validate_framework(items):
 need(type(items) is dict and items,'framework inventory required')
 for name,row in items.items():
  rel(name);need(type(row) is dict and integer(row.get('mode'),0,0o7777),'framework mode')
  kind=row.get('kind')
  if kind=='file':exact(row,['kind','mode','bytes','sha256'],'framework file');need(integer(row['bytes']),'framework bytes');digest(row['sha256'])
  elif kind=='directory':exact(row,['kind','mode'],'framework directory')
  elif kind=='symlink':
   exact(row,['kind','mode','target','resolved'],'framework symlink');need(type(row['target']) is str and not row['target'].startswith('/') and '\\' not in row['target'] and row['target'],'absolute/invalid framework link');rel(row['resolved'])
   parts=list(PurePosixPath(name).parent.parts)
   for p in row['target'].split('/'):
    if p in ('','.'):continue
    if p=='..':need(parts,'escaping framework link');parts.pop()
    else:parts.append(p)
   need(row['resolved'] in items and items[row['resolved']]['kind'] in ('file','directory'),'link resolved target undeclared')
  else:raise Refused('special framework entry')
 need({n for n,v in items.items() if v['kind']=='symlink'}==set(FRAMEWORK_LINKS),'exact seven framework links required')
 for name,(target,resolved) in FRAMEWORK_LINKS.items():need(items[name]=={'kind':'symlink','mode':0o755,'target':target,'resolved':resolved},'framework raw link role changed')
 required=['Versions/A/SDL2','Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi']
 need(all(p in items and items[p]['kind']=='file' for p in required),'framework binary closure')
 need(any(items[n]['kind']=='file' and re.search('license|copying|authors',n,re.I) for n in items),'framework license/provenance missing')
 return items

def read_units(make,enet):
 m=re.search(r'(?m)^SERVER_OBJS=\s*\\\n(.*?)(?=\n\S|\n\n)',make,re.S);need(m,'SERVER_OBJS absent')
 cpp=['source/src/'+x.replace('-standalone.o','.cpp') for x in m.group(1).replace('\\','').split()]
 m=re.search(r'(?m)^libenet_la_SOURCES\s*=\s*(.*)$',enet);need(m,'ENet units absent');c=['source/enet/'+x for x in m.group(1).split() if x!='win32.c']
 need(cpp==CPP and c==C,'fixed ordered16-unit recipe changed');return {'cpp':cpp,'c':c}

def validate_preservation(p,root=ROOT):
 exact(p,['files','directories','links','absent_roots','opaque_fixture_trees'],'preservation record fields')
 need(type(p['files']) is dict and type(p['links']) is dict,'preservation maps')
 for name,h in p['files'].items():absolute(name);digest(h);need(fixture_forest(root,name) is None,'D446 fixture cannot be a hashed input')
 need(type(p['opaque_fixture_trees']) is dict,'fixture tree preservation map')
 for name,row in p['opaque_fixture_trees'].items():
  absolute(name);need(name in {str(Path(root)/n) for n in FIXTURE_FORESTS},'unknown fixture forest row');validate_fixture_tree(row)
 require_fixture_forests(root,p['opaque_fixture_trees'])
 for name,row in p['links'].items():
  absolute(name);need(fixture_forest(root,name) is None,'D446 fixture cannot become a link');exact(row,['target','mode'],'opaque link record');need(type(row['target']) is str and integer(row['mode'],0,0o7777),'opaque link metadata')
 for key in ('directories','absent_roots'):
  need(type(p[key]) is list and p[key]==sorted(set(p[key])),'preservation sorted unique paths')
  for name in p[key]:absolute(name);need(fixture_forest(root,name) is None,'D446 fixture changed preservation kind')
 kinds=[set(p['files']),set(p['directories']),set(p['links']),set(p['opaque_fixture_trees']),set(p['absent_roots'])]
 need(sum(map(len,kinds))==len(set().union(*kinds)),'preservation kinds overlap')
 for missing in p['absent_roots']:need(not any(beneath(n,missing) for group in kinds[:-1] for n in group),'present member inside absent root')
 return p

def sdk_header_alias(view,inputs,sdk_files,name):
 """D107/D111: exactly two fixed leaf aliases, never a supplied alias map."""
 row=next((r for r in SDK_HEADER_ALIASES if r[0]==name),None);need(row is not None,'unknown SDK header alias')
 alias,text,mode,target=row;relative=target[len(SDK)+1:]
 need(view.ordinary_ancestors(alias) and view.ordinary_ancestors(target),'SDK header alias ancestors must be ordinary')
 need(view.link_identity(alias)=={'target':text,'mode':mode},'fixed SDK header alias raw text/mode/type changed')
 need(view.ordinary(target) and view.canonical(target)==target and view.canonical(alias)==target,'SDK header target must be exact canonical ordinary file')
 need(target in inputs and relative in sdk_files and alias not in inputs and alias[len(SDK)+1:] not in sdk_files,'SDK header canonical target not declared')
 need(digest(inputs[target])==digest(sdk_files[relative])==view.hash(target),'SDK header target bytes changed')
 return target

def sdk_link_path(view,path):
 """D462 fixed linker spellings only; never adopt a discovered alias."""
 absolute(path)
 if path not in SDK_LINK_ALIASES:
  physical=view.canonical(path);need(path==physical,'unknown external linker alias');return physical
 target,edges=SDK_LINK_ALIASES[path]
 for alias,raw in edges:
  need(view.ordinary_ancestors(alias) and view.link_identity(alias)=={'target':raw,'mode':0o755},'fixed SDK linker edge text/mode/type changed')
 need(view.ordinary_ancestors(target) and view.ordinary(target) and view.canonical(target)==target and view.canonical(path)==target,'SDK linker target must remain canonical ordinary single-link')
 relative=target[len(SDK)+1:]
 need(target in view.declared_inputs and relative in view.sdk_files and digest(view.declared_inputs[target])==digest(view.sdk_files[relative])==view.hash(target),'SDK linker canonical target declaration/hash changed')
 return target

def authorize(data,expected_sha,ident,view,existing=False,verify_preservation=True):
 need(sha(data)==digest(expected_sha),'authorization digest mismatch');p=loads(data);root=view.root;identifier(ident)
 exact(p,['schema_version','kind','authority','status','execution_release','recipe','ticket','candidate_id','decision','source_revision','source_manifest','bindings','source_acceptance','observation'],'authorization fields')
 need(type(p['schema_version']) is int and p['schema_version']==1 and p['kind']=='BLACKWOOD_NATIVE_BUILD_AUTHORIZATION' and p['authority']=='MAIN' and p['status']=='ACCEPTED' and p['execution_release']=='EXPLICIT_BLACKWOOD_NATIVE_BUILD_EXECUTION' and p['recipe']=='blackwood_native_standalone_v1','native execution authority absent')
 need(type(p['ticket']) is str and 1<=len(p['ticket'])<=64 and p['ticket'].isascii() and p['candidate_id']==ident,'ticket/candidate mismatch')
 need(('FIXTURE_ONLY' in p['ticket'])==bool(view.fixture_only),'fixture authorization cannot cross real boundary')
 decision=rel(p['decision']);need(decision.startswith('notes/decisions/') and decision.endswith('.md') and len(PurePosixPath(decision).parts)==3,'decision path')
 need(type(p['source_revision']) is str and re.fullmatch('[0-9a-f]{40}',p['source_revision']) and p['source_revision']==view.head(),'actual HEAD mismatch')
 need(p['bindings']=={'repository':root,'system_sdk':SDK,'source_framework':root+'/'+FRAMEWORK},'root/SDK/framework binding mismatch')
 exact(p['source_manifest'],['path','sha256'],'manifest identity');need(p['source_manifest']['path']==manifest_path(ident),'candidate-bound source manifest location');manifest=root+'/'+p['source_manifest']['path'];need(view.hash(manifest)==digest(p['source_manifest']['sha256']),'source manifest digest')
 entries=source_manifest(view.json(manifest),p['source_revision'],view,root,manifest_path(ident))
 view.source_entries=entries
 source_acceptance(p['source_acceptance'],view,entries)
 required=set(CPP+C+['source/src/Makefile','source/enet/Makefile.am']+['web/server/blackwood_candidate/'+n for n in SCRIPT_NAMES]);need(required<=entries,'source manifest incomplete native recipe')
 o=p['observation'];exact(o,['inputs','preservation','source_framework','units','tools','system_sdk','flags','errors','map_seed'],'observation fields');need(o['errors']==[],'observation error')
 validate_map_seed(o['map_seed'],view)
 need(o['units']=={'cpp':CPP,'c':C}==read_units(view.text(root+'/source/src/Makefile'),view.text(root+'/source/enet/Makefile.am')),'unit inventory')
 need(o['flags']=={m:flags(root,ident,m) for m in ('release','debug')},'fixed flags changed')
 validate_framework(o['source_framework']);need(view.framework()==o['source_framework'],'source framework changed/membership')
 if not view.fixture_only:
  need(o['source_framework']['Versions/A/SDL2']['sha256']=='1b11de3d606e85fed9cad1f54bc2a833e99e6fc1e67fb2e748cdb666dbd0f681' and o['source_framework']['Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi']['sha256']=='91530ffddb401bbc72d40c97313c0da25c67db209753b6aec5c8556b59930e00','unsigned original framework identities')
 need(decision in entries and {FRAMEWORK+'/'+n for n,row in o['source_framework'].items() if row['kind']=='file'}<=entries,'source package missing decision/framework input')
 exact(o['tools'],TOOLS,'fixed installed tool roles')
 for role,row in o['tools'].items():
  exact(row,['path','sha256'],'tool row');need(row['path']==TOOLS[role],'tool launcher path');digest(row['sha256']);view.arm_tool(role,row['sha256'])
 exact(o['system_sdk'],['root','files'],'SDK fields');need(o['system_sdk']['root']==SDK and type(o['system_sdk']['files']) is dict and o['system_sdk']['files'],'SDK closure missing')
 for name,h in o['system_sdk']['files'].items():rel(name);digest(h);need(view.ordinary(SDK+'/'+name) and view.canonical(SDK+'/'+name)==SDK+'/'+name and view.hash(SDK+'/'+name)==h,'SDK consumed file changed/link')
 need(type(o['inputs']) is dict and o['inputs'],'input map empty')
 for name,h in o['inputs'].items():
  absolute(name);digest(h)
  need(beneath(name,root) or beneath(name,CLT) or beneath(name,PYTHON) or name in TOOLS.values(),'undeclared external input role before filesystem access')
  if name in TOOLS.values():view.arm_tool(next(k for k,v in TOOLS.items() if v==name),h)
  else:need(view.consume(name) and view.canonical(name)==name and view.hash(name)==h,'changed/nonordinary canonical input: '+name)
 validate_preservation(o['preservation'],root)
 if existing:view.omit_container=str(Path(attempt(root,ident)).parent) not in o['preservation']['directories']
 if verify_preservation:need(view.preservation()==o['preservation'],'protected original membership/link changed')
 need(all(root+'/'+n in o['inputs'] for n in entries) and manifest in o['inputs'] and root+'/'+decision in o['inputs'],'manifest/decision inputs missing')
 need(all(row['path'] in o['inputs'] and o['inputs'][row['path']]==row['sha256'] for row in o['tools'].values()),'tool inputs missing')
 need(all(SDK+'/'+n in o['inputs'] and o['inputs'][SDK+'/'+n]==h for n,h in o['system_sdk']['files'].items()),'SDK inputs missing')
 for name,h in view.abi_headers().items():need(SDK+'/usr/include/'+name in o['inputs'] and o['inputs'][SDK+'/usr/include/'+name]==h,'D235 source ABI header role missing/changed')
 for name in ADAPTER_STDLIB_ROLES:
  need(name in o['inputs'],'declared lazy ctypes module/extension role missing')
  if name.endswith('.py'):
   cached=str(Path(name).parent/'__pycache__'/(Path(name).stem+'.cpython-311.pyc'))
   if view.exists(cached):need(cached in o['inputs'],'existing lazy ctypes bytecode input missing')
 for alias,_,_,_ in SDK_HEADER_ALIASES:sdk_header_alias(view,o['inputs'],o['system_sdk']['files'],alias)
 view.sdk_files=o['system_sdk']['files']
 for path in (CLT+'/usr/bin/clang',CLT+'/usr/bin/ld',SDK+'/SDKSettings.json',SDK+'/usr/include/zlib.h',SDK+'/usr/include/pthread.h',SDK+'/usr/lib/libz.tbd',SDK+'/usr/lib/libpthread.tbd',SDK+'/usr/lib/libc++.1.tbd',CLT+'/usr/lib/clang/17/lib/darwin/libclang_rt.osx.a'):
  physical=view.canonical(path);need(beneath(physical,CLT) and physical in o['inputs'],'actual compiler/SDK/link prerequisite not declared')
 for name,row in o['source_framework'].items():
  if row['kind']=='file':need(root+'/'+FRAMEWORK+'/'+name in o['inputs'] and o['inputs'][root+'/'+FRAMEWORK+'/'+name]==row['sha256'],'framework ordinary closure missing')
 for name,h in view.authoring_files().items():need(name in o['inputs'] and o['inputs'][name]==h,'Python authoring closure missing/changed')
 for name in o['inputs']:need(beneath(name,root) or beneath(name,CLT) or beneath(name,PYTHON) or name in TOOLS.values(),'undeclared external input role')
 need(all(n in o['inputs'] or existing and beneath(n,attempt(root,ident)) for n in view.consumed),'consumed source/asset/authoring input missing from declaration')
 need(view.output_safe(ident) and view.exists(attempt(root,ident)) is existing,'attempt existence/unsafe ancestry')
 return p

class View:
 """Read-only filesystem implementation. No tools/compiler probes."""
 fixture_only=False
 def __init__(self,root=ROOT):
  need(str(Path(root))==str(ROOT),'fixed installed repository required');self.root=str(ROOT);self.consumed=set();self.armed={}
 def ordinary(self,p):
  if fixture_forest(self.root,p) is not None:return False
  try:s=Path(p).lstat();return stat.S_ISREG(s.st_mode) and s.st_nlink==1 and self.ordinary_ancestors(p)
  except OSError:return False
 def consume(self,p):
  self.consumed.add(p);return p not in TOOLS.values() and self.ordinary(p)
 def source_hashes(self):return SOURCE_HASHES
 def source_references(self):return SOURCE_REFERENCE_HASHES
 def seed_rows(self):return SEED_ROWS
 def asset_hashes(self):return ASSET_MANIFEST_SHA,ASSET_PROVENANCE_SHA
 def file_stat(self,p):return Path(p).lstat()
 def tool_hashes(self):return TOOL_HASHES
 def abi_headers(self):return ADAPTER_HEADER_PINS
 def arm_tool(self,role,expected):
  p=TOOLS[role];s=self.file_stat(p);need(stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o755 and self.ordinary_ancestors(p) and self.canonical(p)==p,'named tool role identity')
  need(role in ('cc','cxx','otool') or s.st_nlink==1,'multi-link exception is limited to named installed launcher roles')
  need(expected==self.tool_hashes()[role] and self.hash(p)==expected and p not in self.consumed,'tool role/hash or consumed-header conflict')
  now=(s.st_dev,s.st_ino,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns,expected)
  need(role not in self.armed or self.armed[role]==now,'tool rearming identity changed');self.armed[role]=now
  return {'role':role,'path':p,'sha256':expected,'mode':stat.S_IMODE(s.st_mode),'device':s.st_dev,'inode':s.st_ino,'nlink':s.st_nlink,'bytes':s.st_size,'mtime_ns':s.st_mtime_ns,'ctime_ns':s.st_ctime_ns}
 def ordinary_ancestors(self,p):
  try:return all(stat.S_ISDIR(q.lstat().st_mode) for q in Path(p).parents)
  except OSError:return False
 def link_identity(self,p):
  try:info=Path(p).lstat()
  except FileNotFoundError:return None
  return {'target':os.readlink(p),'mode':stat.S_IMODE(info.st_mode)} if stat.S_ISLNK(info.st_mode) else None
 def canonical(self,p):return str(Path(p).resolve(strict=True))
 def exists(self,p):return Path(p).exists() or Path(p).is_symlink()
 def output_safe(self,ident):
  p=Path(attempt(self.root,ident))
  return all(not q.is_symlink() for q in [p,*p.parents])
 def hash(self,p):need(fixture_forest(self.root,p) is None,'D446 fixture cannot be consumed/hashed');return file_sha(p,getattr(self,'deadline_check',None))
 def size(self,p):return Path(p).stat().st_size
 def mode(self,p):return stat.S_IMODE(Path(p).stat().st_mode)
 def text(self,p):return read_bounded(p,MAX_CONTROL).decode()
 def json(self,p):
  limit=MAX_RECORD if str(p).endswith(('/report.json','/freeze.json')) else MAX_CONTROL;return loads(read_bounded(p,limit),limit)
 def head(self):
  git=Path(self.root)/'.git';need(git.is_dir() and not git.is_symlink(),'ordinary .git directory required')
  def metadata(path):need(self.ordinary(str(path)),'ordinary single-link HEAD metadata');return read_bounded(path,MAX_CONTROL).decode()
  text=metadata(git/'HEAD').strip()
  if text.startswith('ref: '):
   ref=rel(text[5:]);need(ref.startswith('refs/'),'HEAD ref')
   if (git/ref).exists() or (git/ref).is_symlink():text=metadata(git/ref).strip()
   else:
    rows=[line.split() for line in metadata(git/'packed-refs').splitlines() if line and not line.startswith(('#','^'))];need(all(len(row)==2 for row in rows),'HEAD packed-ref shape');found=[h for h,r in rows if r==ref];need(len(found)==1,'HEAD packed ref');text=found[0]
  need(re.fullmatch('[0-9a-f]{40}',text),'HEAD identity');return text
 def framework(self):return inventory(Path(self.root)/FRAMEWORK)
 def preservation(self):return preservation_record(self.root,getattr(self,'active',None),omit_container=getattr(self,'omit_container',False))
 def authoring_files(self):
  need(sys.version_info[:3]==(3,11,9),'required existing Python3.11.9')
  executable=str(Path(sys.executable).resolve());need(executable==PYTHON+'/bin/python3.11' and self.hash(executable)=='4e28e811a89aeac6eed668ae641c7f85f5831e42e8dc6cd9a85a3bcc032ec46a','Python authoring executable binding')
  paths={executable}
  for module in tuple(sys.modules.values()):
   name=getattr(module,'__file__',None)
   if name:
    p=Path(name)
    if p.is_file():
     actual=str(p.resolve())
     if beneath(actual,PYTHON) and '/site-packages/' not in actual and '/dist-packages/' not in actual:paths.add(actual)
  return {name:self.hash(name) for name in sorted(paths)}

def preservation_record(root,active=None,browser_sdk='/private/tmp/outbreak-web-sdk',omit_container=False,native_sdk=SDK):
 """Fixed protected forests. Opaque links are lstat records, never traversed.
 Decision/package docs outside forests are independently stable observation inputs.
 """
 root=Path(root);result={'files':{},'directories':[],'links':{},'absent_roots':[],'opaque_fixture_trees':{}}
 roots=[root/n for n in ('source','web','bin_unix','packages','config')]
 if browser_sdk is not None:roots.append(Path(browser_sdk))
 if native_sdk is not None:roots.append(Path(native_sdk))
 for base in roots:
  if not base.exists() and not base.is_symlink():result['absent_roots'].append(str(base));continue
  paths=preserved_paths(base,root)
  for p in paths:
   if active and (p==Path(active) or Path(active) in p.parents):continue
   # Parent container adds no ordinary files and is declared phase metadata.
   if active and omit_container and p==root/'web/server/blackwood-candidate-attempts':continue
   st=p.lstat();name=str(p)
   if name in {str(root/n) for n in FIXTURE_FORESTS}:result['opaque_fixture_trees'][name]=fixture_tree(root,p)
   elif stat.S_ISLNK(st.st_mode):result['links'][name]={'target':os.readlink(p),'mode':stat.S_IMODE(st.st_mode)}
   elif stat.S_ISREG(st.st_mode):result['files'][name]=file_sha(p)
   elif stat.S_ISDIR(st.st_mode):result['directories'].append(name)
   else:raise Refused('special preserved member')
 for k in ('directories','absent_roots'):result[k]=sorted(set(result[k]))
 for k in ('files','links','opaque_fixture_trees'):result[k]=dict(sorted(result[k].items()))
 return validate_preservation(result,root)

def inventory(root,resolve_links=True):
 root=Path(root);need(root.is_dir() and not root.is_symlink(),'ordinary inventory root required');out={}
 for base,dirs,files in os.walk(root,followlinks=False):
  for name in sorted(dirs+files):
   p=Path(base)/name;info=p.lstat();row={'mode':stat.S_IMODE(info.st_mode)}
   if stat.S_ISLNK(info.st_mode):
    target=os.readlink(p);row.update(kind='symlink',target=target)
    if resolve_links:
     try:resolved=p.resolve(strict=True)
     except (OSError,RuntimeError) as e:raise Refused('dangling/cyclic consumed framework link') from e
     need(not os.path.isabs(target) and resolved.is_relative_to(root.resolve()),'escaping inventory link');row['resolved']=str(resolved.relative_to(root.resolve()))
   elif stat.S_ISREG(info.st_mode):
    need(info.st_nlink==1,'multilink consumed inventory file');row.update(kind='file',bytes=info.st_size,sha256=file_sha(p))
   elif stat.S_ISDIR(info.st_mode):row.update(kind='directory')
   else:raise Refused('special inventory file')
   out[str(p.relative_to(root))]=row
 return dict(sorted(out.items()))

def otool_dependencies(text,path):
 """Validate thin or FAT2 otool -L sections; diagnostics remain in raw logs."""
 absolute(path);need(type(text) is str and text.endswith('\n'),'otool dependency output shape')
 sections={};current=None;thin=False
 for line in text.rstrip('\n').splitlines():
  if line==path+':':
   need(not sections,'repeated/mixed thin dependency header');thin=True;current='thin';sections[current]=[]
  elif line.startswith(path+' (architecture '):
   m=re.fullmatch(re.escape(path)+r' \(architecture (x86_64|arm64)\):',line)
   need(m and not thin and m[1] not in sections,'unknown/repeated/mixed architecture header');current=m[1];sections[current]=[]
  else:
   m=re.fullmatch(r'\t([^\s]+) \(compatibility version \d+\.\d+\.\d+, current version \d+\.\d+\.\d+(?:, weak)?\)',line)
   need(m and current is not None,'malformed dependency line/header');need(m[1] not in sections[current],'duplicate dependency in section');sections[current].append(m[1])
 need(set(sections)==({'thin'} if thin else {'x86_64','arm64'}) and all(sections.values()),'missing/empty inspected architecture sections')
 return [name for names in sections.values() for name in names]

def owned_path(base,path,kind='file',absent=False):
 """No symlink in an owned ordinary file/directory path, including ancestors."""
 base=Path(absolute(str(base)));path=Path(absolute(str(path)));need(beneath(str(path),str(base)),'owned path outside attempt')
 for parent in reversed(path.parents):need(stat.S_ISDIR(parent.lstat().st_mode),'nonordinary owned ancestor')
 if absent:
  need(not path.exists() and not path.is_symlink(),'owned output already exists');return path
 info=path.lstat();need((stat.S_ISREG(info.st_mode) and info.st_nlink==1) if kind=='file' else stat.S_ISDIR(info.st_mode),'nonordinary/multilink owned '+kind)
 need(str(path.resolve(strict=True))==str(path),'owned path alias');return path

def owned_paths(base,source_framework):
 """New owned links are ONLY exact approved framework links, never opaque."""
 base=owned_path(base,base,'directory');copy=base/'deps-signed/SDL2.framework';links=[]
 directories={'deps-signed','release','debug','tmp','logs','verification','runtime-seed'};files={'plan.json','report.json','freeze.json','failure.json'}
 for path in base.iterdir():
  need(path.name in directories|files,'unknown owned root role');owned_path(base,path,'directory' if path.name in directories else 'file')
 if (base/'deps-signed').exists():need({p.name for p in (base/'deps-signed').iterdir()}<={'SDL2.framework'},'unknown staged framework root')
 for mode in ('release','debug'):
  if (base/mode).exists():
   allowed={'ac_server'}|{('enet-' if unit in C else '')+Path(unit).stem+suffix for unit in CPP+C for suffix in ('.o','.d','.pre.d')}
   need({p.name for p in (base/mode).iterdir()}<=allowed,'unknown native mode output')
 if (base/'logs').exists():
  for p in (base/'logs').iterdir():
   match=re.fullmatch(r'(\d{3})\.(stdout|stderr|receipt\.json)',p.name);need(match and int(match[1])<126,'unknown command log role')
 if (base/'verification').exists():need({p.name for p in (base/'verification').iterdir()}<={'receipt.json'},'unknown verification role')
 # Validate all entry kinds before hashing files or resolving approved links.
 for parent,dirs,files in os.walk(base,followlinks=False):
  for name in dirs+files:
   path=Path(parent)/name;info=path.lstat()
   if stat.S_ISLNK(info.st_mode):
    need(path.is_relative_to(copy),'unapproved owned link outside staged framework');relative=str(path.relative_to(copy));row=source_framework.get(relative)
    need(row and row['kind']=='symlink' and os.readlink(path)==row['target'] and stat.S_IMODE(info.st_mode)==row['mode'],'extra/changed owned framework link');links.append((path,row))
   else:need((stat.S_ISREG(info.st_mode) and info.st_nlink==1) or stat.S_ISDIR(info.st_mode),'special/multilink owned member')
 for path,row in links:
  try:resolved=path.resolve(strict=True)
  except (OSError,RuntimeError) as e:raise Refused('dangling/cyclic owned framework link') from e
  need(resolved==copy/row['resolved'],'owned framework resolved chain differs');owned_path(base,resolved,'directory' if source_framework[row['resolved']]['kind']=='directory' else 'file')
 return base

def owned_inventory(base,source_framework):
 return inventory(owned_paths(base,source_framework),False)

def reserve(root,ident,check=None):
 """Exclusive dirfd reservation; never overwrite/unlink a prior attempt."""
 check=(lambda:None) if check is None else check;identifier(ident);check();fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:
  for part in ('web','server'):
   check()
   nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
  check()
  try:os.mkdir('blackwood-candidate-attempts',0o700,dir_fd=fd)
  except FileExistsError:pass
  nxt=os.open('blackwood-candidate-attempts',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
  check();os.mkdir(ident,0o700,dir_fd=fd)
 finally:os.close(fd)
 base=Path(attempt(root,ident));need(str(base.resolve())==str(base),'reserved root identity')
 durable_new(base/'failure.json',canonical_json({'status':'RESERVED_INCOMPLETE','fixture_only':False}).encode(),check=check)
 for name in ('deps-signed','release','debug','tmp','logs','verification','runtime-seed'):check();(base/name).mkdir(mode=0o700)
 return base

def stage_copy(root,ident,expected,check=None):
 """Called only after the complete real execution gate and attempt reservation."""
 import shutil
 src=Path(root)/FRAMEWORK;dest=Path(attempt(root,ident))/'deps-signed/SDL2.framework'
 need(inventory(src)==validate_framework(expected),'framework changed before copy')
 need(not dest.exists() and not dest.is_symlink(),'staging destination exists')
 physical_copy(src,dest,check,expected)
 need(inventory(dest)==expected,'physical stage inventory differs')
 for name,row in expected.items():
  if row['kind']=='file':
   original,copied=(src/name).stat(),(dest/name).stat()
   need(copied.st_nlink==1 and (original.st_dev,original.st_ino)!=(copied.st_dev,copied.st_ino),'hardlinked stage rejected')
 return dest

SIGN_MUTABLE={'Versions/A/SDL2','Versions/A/_CodeSignature','Versions/A/_CodeSignature/CodeResources','Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi','Versions/A/Frameworks/hidapi.framework/Versions/A/_CodeSignature','Versions/A/Frameworks/hidapi.framework/Versions/A/_CodeSignature/CodeResources'}
def signed_inventory(before,after):
 validate_framework(after)
 need(set(after)-set(before)<=SIGN_MUTABLE and not set(before)-set(after),'unexpected signing membership change')
 for name,row in before.items():
  if name not in SIGN_MUTABLE:need(after[name]==row,'signing changed non-signature original')
  else:need(after[name]['kind']==row['kind'] and after[name]['mode']==row['mode'],'signing changed kind/mode')
 for name in set(after)-set(before):
  need(after[name]['kind']==('file' if name.endswith('/CodeResources') else 'directory'),'new signing member kind')
 return after

def dependency_paths(text,target,view,ident):
 """Normalize only declared framework links and D107's exact pthread alias.
 No sound/MD3/native-token exception or implicit discovered-input adoption.
 """
 need(type(text) is str and ':' in text,'malformed dependency file');left,right=text.replace('\\\n',' ').split(':',1);need(left.strip()==target,'dependency target mismatch')
 raw=shlex.split(right);need(raw and len(raw)==len(set(raw)),'empty/duplicate dependency file');result={};root=view.root;copy=attempt(root,ident)+'/deps-signed/SDL2.framework'
 for name in raw:
  absolute(name)
  if name in (SDK_PTHREAD_ALIAS[0],SDK_SCHED_ALIAS[0]):canonical=sdk_header_alias(view,view.declared_inputs,view.sdk_files,name);origin=canonical
  elif beneath(name,copy):
   canonical=view.canonical(name)
   need(beneath(canonical,copy),'staged dependency escapes');origin=root+'/'+FRAMEWORK+canonical[len(copy):]
   need('/Headers/' in canonical,'unexpected staged non-header compiler dependency')
  else:canonical=view.canonical(name);need(name==canonical,'undeclared dependency alias');origin=canonical
  need(view.consume(canonical) and origin in view.declared_inputs and view.hash(canonical)==view.declared_inputs[origin],'undeclared/changed actual consumed dependency')
  if beneath(origin,root):need(origin[len(root)+1:] in view.source_entries,'consumed project header absent from source package')
  result[canonical]={'origin':origin,'sha256':view.hash(canonical)}
 return dict(sorted(result.items()))

def protected_inventory(root,active=None,omit_container=False,browser_sdk='/private/tmp/outbreak-web-sdk',native_sdk=SDK):
 """Private before/after membership/mode/link ledger, not a source manifest."""
 out={};root=Path(root)
 for base in [root,*([Path(browser_sdk)] if browser_sdk is not None else []),*([Path(native_sdk)] if native_sdk is not None else [])]:
  if not base.exists():continue
  for p in preserved_paths(base,root):
   if p==base:continue
   if base==root and '.git' in p.relative_to(root).parts:continue
   if active and (p==Path(active) or Path(active) in p.parents):continue
   if omit_container and p==root/'web/server/blackwood-candidate-attempts':continue
   info=p.lstat();row={'mode':stat.S_IMODE(info.st_mode)}
   if str(p) in {str(root/n) for n in FIXTURE_FORESTS}:row=fixture_tree(root,p)
   elif stat.S_ISLNK(info.st_mode):row.update(kind='symlink',target=os.readlink(p))
   elif stat.S_ISREG(info.st_mode):row.update(kind='file',bytes=info.st_size,sha256=file_sha(p))
   elif stat.S_ISDIR(info.st_mode):row.update(kind='directory')
   else:raise Refused('special protected file')
   out[str(p)]=row
 require_fixture_forests(root,out)
 return dict(sorted(out.items()))

def macho(data,kind):
 """Structural arm64 Mach-O validation; never execute an object or binary."""
 need(len(data)>=32,'short Mach-O');magic=struct.unpack_from('>I',data)[0]
 if magic in (0xcafebabe,0xcafebabf):
  count=struct.unpack_from('>I',data,4)[0];need(1<=count<=8,'fat architecture bound');width=20 if magic==0xcafebabe else 32;need(len(data)>=8+count*width,'fat table short');matches=[];ranges=[]
  for i in range(count):
   offset=8+i*width;cpu=struct.unpack_from('>I',data,offset)[0]
   start,size=struct.unpack_from('>II' if width==20 else '>QQ',data,offset+8)
   need(start>=8+count*width and size>=32 and start+size<=len(data),'fat slice out of range')
   align=struct.unpack_from('>I',data,offset+(16 if width==20 else 24))[0];need(align<=31 and start%(1<<align)==0,'fat slice alignment');ranges.append((start,start+size))
   if cpu==0x100000c:matches.append(data[start:start+size])
  ordered=sorted(ranges);need(all(ordered[i][1]<=ordered[i+1][0] for i in range(len(ordered)-1)),'overlapping fat slices');need(len(matches)==1,'one arm64 slice required');return macho(matches[0],kind)
 magic,cpu,subtype,filetype,ncmds,sizeofcmds,flags,reserved=struct.unpack_from('<8I',data)
 need(magic==0xfeedfacf and cpu==0x100000c and filetype==kind and ncmds<=4096 and 32+sizeofcmds<=len(data),'Mach-O type/architecture/load bounds')
 offset=32;loads=[]
 for _ in range(ncmds):
  need(offset+8<=32+sizeofcmds,'load command truncated');cmd,size=struct.unpack_from('<II',data,offset);need(size>=8 and size%4==0 and offset+size<=32+sizeofcmds,'load command size');loads.append((cmd,data[offset:offset+size]));offset+=size
 need(offset==32+sizeofcmds,'load command total mismatch')
 if kind in (2,6):
  sigs=[body for c,body in loads if c==0x1d];need(len(sigs)==1 and len(sigs[0])==16,'code signature load command missing/malformed');offset,size=struct.unpack_from('<II',sigs[0],8);need(offset>=32+sizeofcmds and size>0 and offset+size<=len(data),'signature payload bounds')
 return loads

def rpaths(text,expected):
 found=re.findall(r'cmd LC_RPATH\n\s*cmdsize \d+\n\s*path (.*?) \(offset',text)
 need(len(found)==2 and set(found)==set(expected),'exact candidate RPATHs required');return found

SOURCE_REFERENCE_HASHES={'decision':'1e1f3f748188190e2524451bfe38aae89d58a4aaa195f9afe3b46e058da69af1','handoff':'38a6f1ad28400cd7436ba09e48b7a60d37529971d84f0fb0b0b580365a0b44d7','evidence':'b26493bb41564a65ef9884f325cc10838ffa02cf124fe34006240882e891a7f9'}

def source_acceptance(value,view,entries):
 exact(value,['ticket','decision','handoff','evidence','files'],'source acceptance fields');need(value['ticket']=='T163','source acceptance ticket')
 for role,path in SOURCE_REFERENCES.items():
  row=value[role];exact(row,['path','sha256'],'source acceptance reference');need(row['path']==path and digest(row['sha256'])==view.source_references()[role],'source acceptance pinned reference')
  actual=view.root+'/'+path;need(view.consume(actual) and view.hash(actual)==row['sha256'],'source acceptance current reference')
 need(type(value['files']) is list and len(value['files'])==4,'four accepted source files required');names=[]
 for row in value['files']:
  exact(row,['path','bytes','sha256','mode'],'accepted source FileRef');path=rel(row['path']);names.append(path);need(path in view.source_hashes() and row['sha256']==view.source_hashes()[path] and path in entries,'accepted source hash/package')
  p=view.root+'/'+path;need(integer(row['bytes']) and row['mode']==0o644 and type(row['mode']) is int and view.consume(p) and view.size(p)==row['bytes'] and view.mode(p)==row['mode'] and view.hash(p)==row['sha256'],'accepted source current bytes/mode/link')
 need(names==sorted(view.source_hashes()),'accepted source sorted exact membership')

def map_declaration(view):
 mh,ph=view.asset_hashes()
 return {'manifest':{'path':ASSET_ROOT+'/manifest.json','sha256':mh},'provenance':{'path':ASSET_ROOT+'/PROVENANCE.json','sha256':ph},'files':sorted([{'source':ASSET_ROOT+'/pack-root/'+s,'target':t,'bytes':n,'sha256':h,'mode':0o644} for s,t,n,h in view.seed_rows()],key=lambda x:x['target']),'rotation':{'target':'config/maprot.cfg','bytes':len(ROTATION),'sha256':sha(ROTATION)}}

def validate_map_seed(value,view):
 exact(value,['manifest','provenance','files','rotation'],'map seed fields');need(same_typed(value,map_declaration(view)),'fixed Blackwood seed mapping/hash/rotation changed')
 for role in ('manifest','provenance'):
  row=value[role];exact(row,['path','sha256'],'asset reference');p=view.root+'/'+row['path'];need(view.consume(p) and view.hash(p)==row['sha256'],'accepted asset reference changed')
 doc=view.json(view.root+'/'+value['manifest']['path']);need(type(doc.get('entries')) is list and len(doc['entries'])==84,'accepted complete84 asset mapping required')
 entries={};order=[]
 for row in doc['entries']:
  need(type(row) is dict,'asset row');name=rel(row['path']);order.append(name);need(name not in entries,'duplicate asset member');entries[name]=row
 need(order==sorted(order),'asset member order')
 for name,row in entries.items():
  p=view.root+'/'+ASSET_ROOT+'/pack-root/'+name;need(integer(row['bytes']) and view.consume(p) and view.size(p)==row['bytes'] and view.mode(p)==0o644 and view.hash(p)==digest(row['sha256']),'accepted source pack member changed')
  need(rel(row['notice']) in entries and type(row['source_manifest']) is str and row['source_manifest'].startswith('web/assets/') and rel(row['source_path']) and row['source_sha256']==row['sha256'],'asset source/notice association')
 for row in value['files']:
  exact(row,['source','target','bytes','sha256','mode'],'seed FileRef');name=row['source'][len(ASSET_ROOT+'/pack-root/'):];entry=entries.get(name)
  need(entry and entry['bytes']==row['bytes'] and entry['sha256']==row['sha256'] and entry['notice']=='notices/blackwood-candidate/LICENSE.txt','seed accepted source association')
 cfg=view.text(view.root+'/'+ASSET_ROOT+'/pack-root/packages/maps/blackwood_greybox_v1.cfg')
 for line in cfg.splitlines():
  line=line.split('//',1)[0].strip()
  if not line:continue
  if line in ('mapmodelreset','mapsoundreset','texturereset','fog 256','fogcolour 0x18232B'):continue
  match=re.fullmatch(r'texture 0 "(outbreak/(?:ceiling|ground|wall)\.png)"',line);need(match and 'packages/textures/'+match[1] in entries,'opaque CFG pure command/texture closure')
 return value

_HELD_FILE_HANDLES=[] # Strong unresolved ownership; no destructor or automatic retry.
class HeldFile:
 def __init__(self,number,path,kind,backend):
  self.number=number;self.path=str(path);self.kind=kind;self.backend=backend;self.state='OPEN';self.close_attempted=False;_HELD_FILE_HANDLES.append(self)
 def describe(self):return {'fd':self.number,'path':self.path,'kind':self.kind,'state':self.state,'close_attempted':self.close_attempted}

class DurabilityFailure(Refused):
 def __init__(self,primary,secondary,actions,handles):
  self.primary=primary;self.secondary=secondary;self.actions=actions;self.handles=tuple(h for h in handles if h.state!='CLOSED')
  super().__init__('held='+str([h.describe() for h in self.handles])[:512]+' primary='+str(primary)[:256]+' secondary='+str(secondary)[:256]+' actions='+str(actions[-12:]))

class DurableOps:
 def open_file(self,path):return os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
 def chmod(self,fd):os.fchmod(fd,0o644)
 def write(self,fd,data):return os.write(fd,data)
 def flush(self,fd):pass # Unbuffered descriptor: no Python buffer, including on close.
 def fsync(self,fd):os.fsync(fd)
 def close(self,fd):os.close(fd)
 def open_directory(self,path):return os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)

def durable_new(path,data,limit=MAX_RECORD,check=None,fs=None):
 path=Path(path);need(type(data) is bytes and len(data)<=limit,'bounded evidence bytes')
 check=(lambda:None) if check is None else check;fs=DurableOps() if fs is None else fs
 primary=None;secondary=[];actions=[];file_owner=None;directory_owner=None;handles=[]
 def fail(error):
  nonlocal primary
  if primary is None:primary=error
  else:secondary.append(str(error)[:256])
 def effect(name,fn):
  check();actions.append(name);value=fn();check();return value
 def release(owner):
  try:check()
  except BaseException as e:owner.state='SKIPPED_EXPIRED';fail(e);return
  owner.close_attempted=True;actions.append('close_'+owner.kind)
  try:fs.close(owner.number);owner.state='CLOSED';_HELD_FILE_HANDLES.remove(owner)
  except BaseException as e:owner.state='UNRESOLVED_CLOSE_ERROR';fail(e)
  try:check()
  except BaseException as e:fail(e)
 try:
  check();actions.append('open_file');fd=fs.open_file(path);file_owner=HeldFile(fd,path,'file',fs);handles.append(file_owner);check()
  effect('chmod',lambda:fs.chmod(fd));at=0
  while at<len(data):
   amount=effect('write',lambda:fs.write(fd,data[at:at+65536]));need(type(amount) is int and 0<amount<=min(65536,len(data)-at),'file write progress');at+=amount
  effect('flush_unbuffered_noop',lambda:fs.flush(fd));effect('fsync_file',lambda:fs.fsync(fd))
 except BaseException as e:fail(e)
 finally:
  if file_owner is not None:release(file_owner)
 if primary is None:
  try:
   check();actions.append('open_directory');fd=fs.open_directory(path.parent);directory_owner=HeldFile(fd,path.parent,'directory',fs);handles.append(directory_owner);check();effect('fsync_directory',lambda:fs.fsync(fd))
  except BaseException as e:fail(e)
  finally:
   if directory_owner is not None:release(directory_owner)
 if primary is not None:raise DurabilityFailure(primary,secondary,actions,handles)
 check()

def physical_copy(src,dest,check=None,expected=None):
 check=(lambda:None) if check is None else check;src=Path(src);dest=Path(dest);root_mode=stat.S_IMODE(src.stat().st_mode);check();dest.mkdir(mode=root_mode);check();dest.chmod(root_mode);check()
 for parent,dirs,files in os.walk(src,followlinks=False):
  check();target=dest/Path(parent).relative_to(src)
  for name in sorted(dirs+files):
   check();source=Path(parent)/name;out=target/name;info=source.lstat();mode=stat.S_IMODE(info.st_mode)
   key=str(source.relative_to(src));need(expected is not None and key in expected and expected[key]['mode']==mode,'undeclared/changed copy member before effects');row=expected[key]
   if stat.S_ISLNK(info.st_mode):need(row['kind']=='symlink' and os.readlink(source)==row['target'],'copy raw link changed');check();out.symlink_to(row['target']);check();os.lchmod(out,mode);check()
   elif stat.S_ISDIR(info.st_mode):need(row['kind']=='directory','copy directory kind changed');check();out.mkdir(mode=mode);check();out.chmod(mode);check()
   else:
    need(row['kind']=='file' and stat.S_ISREG(info.st_mode) and info.st_nlink==1 and info.st_size==row['bytes'],'ordinary original copy member');data=read_bounded(source,row['bytes']);need(sha(data)==row['sha256'],'copy source changed before publication');check();durable_new(out,data,limit=row['bytes'],check=check);check();out.chmod(mode);check()

def seed_record(base,declaration):
 base=Path(base);seed=base/'runtime-seed';owned_path(base,seed,'directory');items=inventory(seed,False)
 files=sorted([{'target':n,'bytes':v['bytes'],'sha256':v['sha256'],'mode':v['mode']} for n,v in items.items() if v['kind']=='file'],key=lambda x:x['target'])
 expected=sorted([{k:v for k,v in row.items() if k!='source'} for row in declaration['files']]+[{'target':'config/maprot.cfg','bytes':len(ROTATION),'sha256':sha(ROTATION),'mode':0o644}],key=lambda x:x['target'])
 need(files==expected and all(row['kind'] in ('file','directory') for row in items.values()),'actual complete seed file identity/kind changed')
 directories=sorted({str(parent) for row in expected for parent in PurePosixPath(row['target']).parents if str(parent)!='.'})
 need([n for n,v in items.items() if v['kind']=='directory']==directories,'exact runtime-seed parent membership')
 return {'declaration':declaration,'files':files,'directories':directories}

def stage_seed(view,base,declaration,check):
 validate_map_seed(declaration,view);base=Path(base);seed=base/'runtime-seed'
 for row in declaration['files']:
  check();source=view.root+'/'+row['source'];need(view.consume(source),'ordinary seed source');data=read_bounded(source,row['bytes']);need(len(data)==row['bytes'] and sha(data)==row['sha256'],'seed changed before copy')
  dest=seed/row['target'];dest.parent.mkdir(parents=True,exist_ok=True);owned_path(base,dest,absent=True);check();durable_new(dest,data,check=check);need(dest.stat().st_nlink==1 and (Path(source).stat().st_dev,Path(source).stat().st_ino)!=(dest.stat().st_dev,dest.stat().st_ino),'seed physical copy required')
 check();dest=seed/'config/maprot.cfg';dest.parent.mkdir(parents=True,exist_ok=True);owned_path(base,dest,absent=True);durable_new(dest,ROTATION,check=check)
 return seed_record(base,declaration)

def command_plan(root,ident):
 base=Path(attempt(root,ident));recipe=commands(root,ident);rows=[]
 def add(kind,argv):rows.append({'index':len(rows),'kind':kind,'argv':argv})
 def inspect(path):
  for kind,argv in [('file',[TOOLS['file'],path]),('dependencies',[TOOLS['otool'],'-L',path]),('load_commands',[TOOLS['otool'],'-l',path]),('signature',[TOOLS['codesign'],'--verify','--verbose=4',path]),('adhoc',[TOOLS['codesign'],'--display','--verbose=4',path])]:add(kind,argv)
 for role in ('cc','cxx'):add('compiler_identity',[TOOLS[role],'--version'])
 for argv in recipe['sign']:add('adhoc_sign_copy',argv)
 for argv in recipe['signature']:add('verify_copy_signature',argv)
 copy=str(base/'deps-signed/SDL2.framework')
 for path in (copy+'/Versions/A/SDL2',copy+'/Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi'):inspect(path)
 for spec in recipe['modes'].values():
  for row in spec['units']:
   add('discover_dependencies',row['discover']);add('compile',row['compile']);add('object_file',[TOOLS['file'],row['object']])
  add('link',spec['link']);inspect(spec['binary'])
 need(len(rows)==126,'fixed126 command plan');return rows

STEP_KEYS=('index','kind','argv','environment','tool_role','timeout_s','pid','returned_handle','ownership','exit','child_reaped','nonreaping','native_last','group_empty','group_signal','timed_out','overflow','primary','secondary','cleanup_attempts','io_unresolved','elapsed_ms','stdout_path','stderr_path','stdout_sha256','stderr_sha256','stdout_bytes','stderr_bytes','publication','status')
def validate_step(row,index,kind,argv,env):
 exact(row,STEP_KEYS,'corrected bounded step fields')
 need(integer(row['index'],0,125) and row['index']==index and row['kind']==kind and row['argv']==argv and row['environment']==env,'fixed step identity')
 tool=row['tool_role'];exact(tool,['role','path','sha256','mode','device','inode','nlink','bytes','mtime_ns','ctime_ns'],'armed tool identity fields');need(type(tool['role']) is str and tool['role'] in TOOLS and tool['path']==TOOLS[tool['role']]==argv[0] and type(tool['mode']) is int and tool['mode']==0o755 and all(integer(tool[k]) for k in ('device','inode','nlink','bytes','mtime_ns','ctime_ns')) and tool['nlink']>=1,'armed named tool identity');digest(tool['sha256'])
 need(tool['role'] in ('cc','cxx','otool') or tool['nlink']==1,'named launcher hardlink exception only')
 need(type(row['timeout_s']) is int and row['timeout_s']==120 and integer(row['pid'],1,2**31-1) and row['returned_handle'] is True and row['ownership']=='REAPED' and type(row['exit']) is int and row['exit']==0 and row['child_reaped'] is True and row['group_empty'] is True,'original child and group closure facts')
 exact(row['nonreaping'],['pid','signo','code','status','errno'],'nonreaping terminal record');need(all(type(v) is int for v in row['nonreaping'].values()) and row['nonreaping']=={'pid':row['pid'],'signo':20,'code':1,'status':0,'errno':0},'nonreaping exit0 observation')
 native=row['native_last'];exact(native,['pid','result','errno','record_bytes','record_hex'],'bounded last native observation');need(type(native['pid']) is int and native['pid']==row['pid'] and type(native['result']) is int and native['result']==0 and type(native['errno']) is int and native['errno']==0 and type(native['record_bytes']) is int and native['record_bytes']==104 and type(native['record_hex']) is str and re.fullmatch('[0-9a-f]{208}',native['record_hex']),'native observation shape')
 signo,association,code,pid,uid,status=struct.unpack_from('<iiiiIi',bytes.fromhex(native['record_hex']));need((signo,association,code,pid,status)==(20,0,1,row['pid'],0),'native observation differs from successful child event')
 need(row['group_signal'] in ('SIGKILL_SENT_WHILE_ANCHORED','ESRCH_WHILE_ANCHORED','EPERM_DENIED_WHILE_ANCHORED') and row['timed_out'] is False and row['overflow'] is False and row['primary'] is None and row['secondary']==[],'step cleanup/failure facts')
 need(row['status']=='PASS' and row['publication']=='CONFIRMED' and type(row['elapsed_ms']) in (int,float) and math.isfinite(row['elapsed_ms']) and 0<=row['elapsed_ms']<=120000,'step terminal/publication/time')
 need(row['io_unresolved']==[],'unresolved command persistence handle')
 need(type(row['cleanup_attempts']) is list and row['cleanup_attempts']==['signal_anchored_group','wait_original_handle','observe_group_empty_readonly','selector_close','stdout_close','stderr_close'],'independent normal cleanup sequence')
 for name in ('stdout','stderr'):
  need(row[name+'_path']==f'logs/{index:03d}.'+name and integer(row[name+'_bytes'],0,MAX_LOG),'fixed bounded log identity');digest(row[name+'_sha256'])
 need(row['stdout_bytes']+row['stderr_bytes']<=MAX_LOG,'combined command log bound')
