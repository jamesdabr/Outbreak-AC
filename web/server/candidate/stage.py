"""T092 fixed native recipe, strict data gates and confined staging. No import effects."""
import hashlib,json,os,re,shlex,stat,struct,sys,shutil,subprocess,selectors,signal
from pathlib import Path,PurePosixPath

ROOT=Path(__file__).resolve().parents[3]
SDK='/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk'
SDK_PTHREAD_ALIAS=(SDK+'/usr/include/pthread.h','pthread/pthread.h',0o755,SDK+'/usr/include/pthread/pthread.h')
SDK_SCHED_ALIAS=(SDK+'/usr/include/sched.h','pthread/sched.h',0o755,SDK+'/usr/include/pthread/sched.h')
SDK_HEADER_ALIASES=(SDK_PTHREAD_ALIAS,SDK_SCHED_ALIAS)
CLT='/Library/Developer/CommandLineTools'
PYTHON='/Library/Frameworks/Python.framework/Versions/3.11'
FRAMEWORK='source/xcode/Frameworks/SDL2.framework'
CPP=['source/src/'+n+'.cpp' for n in ('crypto','log','protocol','serverms','server','stream','tools','wizard')]
C=['source/enet/'+n+'.c' for n in ('callbacks','compress','host','list','packet','peer','protocol','unix')]
TOOLS={'cc':'/usr/bin/clang','cxx':'/usr/bin/clang++','codesign':'/usr/bin/codesign','otool':'/usr/bin/otool','file':'/usr/bin/file'}
SCRIPT_NAMES=('stage.py','build.py','verify.py','test_preparation.py','README.md')
CLAIMS={k:False for k in ('native_runtime','gameplay','multiplayer','authority','P0')}
MAX_LOG=8*1024*1024

class Refused(ValueError):pass
def need(v,why):
 if not v:raise Refused(why)
def exact(v,keys,why):need(type(v) is dict and set(v)==set(keys),why)
def integer(v,lo=0,hi=2**63-1):return type(v) is int and lo<=v<=hi
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(s):need(type(s) is str and re.fullmatch('[0-9a-f]{64}',s),'invalid SHA256');return s
def rel(s):
 need(type(s) is str and s and not any(ord(c)<32 for c in s) and '\\' not in s and not s.startswith('/') and all(p not in ('','.','..') for p in s.split('/')),'noncanonical relative path');return s
def absolute(s):
 need(type(s) is str and s.startswith('/') and str(PurePosixPath(s))==s and all(p not in ('.','..') for p in s.split('/')[1:]) and not any(ord(c)<32 for c in s) and '\\' not in s,'noncanonical absolute path');return s
def identifier(s):need(type(s) is str and re.fullmatch('[A-Za-z0-9_-]{1,48}',s),'invalid candidate ID');return s
def beneath(p,base):return p==base or p.startswith(base+'/')
def loads(data):
 def pairs(rows):
  out={}
  for k,v in rows:need(k not in out,'duplicate JSON key');out[k]=v
  return out
 return json.loads(data,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(Refused('nonfinite JSON')))
def canonical_json(value):return json.dumps(value,sort_keys=True,separators=(',',':'))+'\n'
def attempt(root,ident):return str(Path(root)/'web/server/candidate-attempts'/identifier(ident))
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

def source_manifest(doc,revision,view,root):
 exact(doc,['schema_version','kind','source_revision','entries'],'source manifest fields')
 need(type(doc['schema_version']) is int and doc['schema_version']==1 and doc['kind']=='SOURCE_INPUT_MANIFEST' and doc['source_revision']==revision,'source manifest identity')
 need(type(doc['entries']) is list and doc['entries'],'empty source manifest');paths=[]
 for e in doc['entries']:
  exact(e,['path','bytes','sha256','mode'],'source entry fields');rel(e['path']);digest(e['sha256']);need(integer(e['bytes']) and type(e['mode']) is int and e['mode'] in (420,493),'source entry mode/size')
  need(e['path']!='web/repro/source-manifest.json','manifest self reference');p=root+'/'+e['path'];need(view.ordinary(p) and view.canonical(p)==p and view.hash(p)==e['sha256'] and view.size(p)==e['bytes'] and view.mode(p)==e['mode'],'source entry changed/link');paths.append(e['path'])
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
 required=['Versions/A/SDL2','Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi']
 need(all(p in items and items[p]['kind']=='file' for p in required),'framework binary closure')
 need(any(items[n]['kind']=='file' and re.search('license|copying|authors',n,re.I) for n in items),'framework license/provenance missing')
 return items

def read_units(make,enet):
 m=re.search(r'(?m)^SERVER_OBJS=\s*\\\n(.*?)(?=\n\S|\n\n)',make,re.S);need(m,'SERVER_OBJS absent')
 cpp=['source/src/'+x.replace('-standalone.o','.cpp') for x in m.group(1).replace('\\','').split()]
 m=re.search(r'(?m)^libenet_la_SOURCES\s*=\s*(.*)$',enet);need(m,'ENet units absent');c=['source/enet/'+x for x in m.group(1).split() if x!='win32.c']
 need(cpp==CPP and c==C,'fixed ordered16-unit recipe changed');return {'cpp':cpp,'c':c}

def validate_preservation(p):
 exact(p,['files','directories','links','absent_roots'],'preservation record fields')
 need(type(p['files']) is dict and type(p['links']) is dict,'preservation maps')
 for name,h in p['files'].items():absolute(name);digest(h)
 for name,row in p['links'].items():
  absolute(name);exact(row,['target','mode'],'opaque link record');need(type(row['target']) is str and integer(row['mode'],0,0o7777),'opaque link metadata')
 for key in ('directories','absent_roots'):
  need(type(p[key]) is list and p[key]==sorted(set(p[key])),'preservation sorted unique paths')
  for name in p[key]:absolute(name)
 kinds=[set(p['files']),set(p['directories']),set(p['links']),set(p['absent_roots'])]
 need(sum(map(len,kinds))==len(set().union(*kinds)),'preservation kinds overlap')
 for missing in p['absent_roots']:need(not any(beneath(n,missing) for group in kinds[:3] for n in group),'present member inside absent root')
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

def authorize(data,expected_sha,ident,view,existing=False,verify_preservation=True):
 need(sha(data)==digest(expected_sha),'authorization digest mismatch');p=loads(data);root=view.root;identifier(ident)
 exact(p,['schema_version','kind','authority','status','execution_release','recipe','ticket','candidate_id','decision','source_revision','source_manifest','bindings','observation'],'authorization fields')
 need(type(p['schema_version']) is int and p['schema_version']==1 and p['kind']=='CANDIDATE_NATIVE_BUILD_AUTHORIZATION' and p['authority']=='MAIN' and p['status']=='ACCEPTED' and p['execution_release']=='EXPLICIT_CANDIDATE_NATIVE_BUILD_EXECUTION' and p['recipe']=='native_standalone_v1','native execution authority absent')
 need(type(p['ticket']) is str and 1<=len(p['ticket'])<=64 and p['ticket'].isascii() and p['candidate_id']==ident,'ticket/candidate mismatch')
 decision=rel(p['decision']);need(decision.startswith('notes/decisions/') and decision.endswith('.md') and len(PurePosixPath(decision).parts)==3,'decision path')
 need(type(p['source_revision']) is str and re.fullmatch('[0-9a-f]{40}',p['source_revision']) and p['source_revision']==view.head(),'actual HEAD mismatch')
 need(p['bindings']=={'repository':root,'system_sdk':SDK,'source_framework':root+'/'+FRAMEWORK},'root/SDK/framework binding mismatch')
 exact(p['source_manifest'],['path','sha256'],'manifest identity');need(p['source_manifest']['path']=='web/repro/source-manifest.json','source manifest location');manifest=root+'/'+p['source_manifest']['path'];need(view.hash(manifest)==digest(p['source_manifest']['sha256']),'source manifest digest')
 entries=source_manifest(view.json(manifest),p['source_revision'],view,root)
 view.source_entries=entries
 required=set(CPP+C+['source/src/Makefile','source/enet/Makefile.am']+['web/server/candidate/'+n for n in SCRIPT_NAMES]);need(required<=entries,'source manifest incomplete native recipe')
 o=p['observation'];exact(o,['inputs','preservation','source_framework','units','tools','system_sdk','flags','errors'],'observation fields');need(o['errors']==[],'observation error')
 need(o['units']=={'cpp':CPP,'c':C}==read_units(view.text(root+'/source/src/Makefile'),view.text(root+'/source/enet/Makefile.am')),'unit inventory')
 need(o['flags']=={m:flags(root,ident,m) for m in ('release','debug')},'fixed flags changed')
 validate_framework(o['source_framework']);need(view.framework()==o['source_framework'],'source framework changed/membership')
 need(decision in entries and {FRAMEWORK+'/'+n for n,row in o['source_framework'].items() if row['kind']=='file'}<=entries,'source package missing decision/framework input')
 exact(o['tools'],TOOLS,'fixed installed tool roles')
 for role,row in o['tools'].items():exact(row,['path','sha256'],'tool row');need(row['path']==TOOLS[role],'tool launcher path');digest(row['sha256'])
 exact(o['system_sdk'],['root','files'],'SDK fields');need(o['system_sdk']['root']==SDK and type(o['system_sdk']['files']) is dict and o['system_sdk']['files'],'SDK closure missing')
 for name,h in o['system_sdk']['files'].items():rel(name);digest(h);need(view.ordinary(SDK+'/'+name) and view.canonical(SDK+'/'+name)==SDK+'/'+name and view.hash(SDK+'/'+name)==h,'SDK consumed file changed/link')
 need(type(o['inputs']) is dict and o['inputs'],'input map empty')
 for name,h in o['inputs'].items():absolute(name);digest(h);need(view.ordinary(name) and view.canonical(name)==name and view.hash(name)==h,'changed/nonordinary canonical input: '+name)
 validate_preservation(o['preservation'])
 if existing:view.omit_container=str(Path(attempt(root,ident)).parent) not in o['preservation']['directories']
 if verify_preservation:need(view.preservation()==o['preservation'],'protected original membership/link changed')
 need(all(root+'/'+n in o['inputs'] for n in entries) and manifest in o['inputs'] and root+'/'+decision in o['inputs'],'manifest/decision inputs missing')
 need(all(row['path'] in o['inputs'] and o['inputs'][row['path']]==row['sha256'] for row in o['tools'].values()),'tool inputs missing')
 need(all(SDK+'/'+n in o['inputs'] and o['inputs'][SDK+'/'+n]==h for n,h in o['system_sdk']['files'].items()),'SDK inputs missing')
 for alias,_,_,_ in SDK_HEADER_ALIASES:sdk_header_alias(view,o['inputs'],o['system_sdk']['files'],alias)
 view.sdk_files=o['system_sdk']['files']
 for path in (CLT+'/usr/bin/clang',CLT+'/usr/bin/ld',SDK+'/SDKSettings.json',SDK+'/usr/include/zlib.h',SDK+'/usr/include/pthread.h',SDK+'/usr/lib/libz.tbd',SDK+'/usr/lib/libpthread.tbd'):
  physical=view.canonical(path);need(beneath(physical,CLT) and physical in o['inputs'],'actual compiler/SDK/link prerequisite not declared')
 for name,row in o['source_framework'].items():
  if row['kind']=='file':need(root+'/'+FRAMEWORK+'/'+name in o['inputs'] and o['inputs'][root+'/'+FRAMEWORK+'/'+name]==row['sha256'],'framework ordinary closure missing')
 for name,h in view.authoring_files().items():need(name in o['inputs'] and o['inputs'][name]==h,'Python authoring closure missing/changed')
 for name in o['inputs']:need(beneath(name,root) or beneath(name,CLT) or beneath(name,PYTHON) or name in TOOLS.values(),'undeclared external input role')
 need(view.output_safe(ident) and view.exists(attempt(root,ident)) is existing,'attempt existence/unsafe ancestry')
 return p

class View:
 """Read-only filesystem implementation. No tools/compiler probes."""
 def __init__(self,root=ROOT):self.root=str(Path(root).resolve())
 def ordinary(self,p):return Path(p).is_file() and not Path(p).is_symlink()
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
 def hash(self,p):return sha(Path(p).read_bytes())
 def size(self,p):return Path(p).stat().st_size
 def mode(self,p):return stat.S_IMODE(Path(p).stat().st_mode)
 def text(self,p):return Path(p).read_text()
 def json(self,p):return loads(Path(p).read_bytes())
 def head(self):
  git=Path(self.root)/'.git';need(git.is_dir() and not git.is_symlink(),'ordinary .git directory required')
  text=(git/'HEAD').read_text().strip()
  if text.startswith('ref: '):
   ref=rel(text[5:]);need(ref.startswith('refs/'),'HEAD ref')
   if (git/ref).is_file():text=(git/ref).read_text().strip()
   else:
    rows=[line.split() for line in (git/'packed-refs').read_text().splitlines() if line and not line.startswith(('#','^'))];found=[h for h,r in rows if r==ref];need(len(found)==1,'HEAD packed ref');text=found[0]
  need(re.fullmatch('[0-9a-f]{40}',text),'HEAD identity');return text
 def framework(self):return inventory(Path(self.root)/FRAMEWORK)
 def preservation(self):return preservation_record(self.root,getattr(self,'active',None),omit_container=getattr(self,'omit_container',False))
 def authoring_files(self):
  need(sys.version_info[:3]==(3,11,9),'required existing Python3.11.9')
  executable=str(Path(sys.executable).resolve());need(beneath(executable,PYTHON),'Python authoring executable binding')
  paths={executable}
  for module in tuple(sys.modules.values()):
   name=getattr(module,'__file__',None)
   if name:
    p=Path(name)
    if p.is_file():
     actual=str(p.resolve())
     if beneath(actual,PYTHON) and '/site-packages/' not in actual and '/dist-packages/' not in actual:paths.add(actual)
  return {name:self.hash(name) for name in sorted(paths)}

def preservation_record(root,active=None,browser_sdk='/private/tmp/outbreak-web-sdk',omit_container=False):
 """Fixed protected forests. Opaque links are lstat records, never traversed.
 Decision/package docs outside forests are independently stable observation inputs.
 """
 root=Path(root);result={'files':{},'directories':[],'links':{},'absent_roots':[]}
 roots=[root/n for n in ('source','web','bin_unix','packages','config')]
 if browser_sdk is not None:roots.append(Path(browser_sdk))
 for base in roots:
  if not base.exists() and not base.is_symlink():result['absent_roots'].append(str(base));continue
  paths=[base]
  if base.is_dir() and not base.is_symlink():
   for parent,dirs,files in os.walk(base,followlinks=False):paths.extend(Path(parent)/name for name in dirs+files)
  for p in paths:
   if active and (p==Path(active) or Path(active) in p.parents):continue
   # Parent container adds no ordinary files and is declared phase metadata.
   if active and omit_container and p==root/'web/server/candidate-attempts':continue
   st=p.lstat();name=str(p)
   if stat.S_ISLNK(st.st_mode):result['links'][name]={'target':os.readlink(p),'mode':stat.S_IMODE(st.st_mode)}
   elif stat.S_ISREG(st.st_mode):result['files'][name]=sha(p.read_bytes())
   elif stat.S_ISDIR(st.st_mode):result['directories'].append(name)
   else:raise Refused('special preserved member')
 for k in ('directories','absent_roots'):result[k]=sorted(set(result[k]))
 for k in ('files','links'):result[k]=dict(sorted(result[k].items()))
 return validate_preservation(result)

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
   elif stat.S_ISREG(info.st_mode):row.update(kind='file',bytes=info.st_size,sha256=sha(p.read_bytes()))
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
 info=path.lstat();need(stat.S_ISREG(info.st_mode) if kind=='file' else stat.S_ISDIR(info.st_mode),'nonordinary owned '+kind)
 need(str(path.resolve(strict=True))==str(path),'owned path alias');return path

def owned_paths(base,source_framework):
 """New owned links are ONLY exact approved framework links, never opaque."""
 base=owned_path(base,base,'directory');copy=base/'deps-signed/SDL2.framework';links=[]
 # Validate all entry kinds before hashing files or resolving approved links.
 for parent,dirs,files in os.walk(base,followlinks=False):
  for name in dirs+files:
   path=Path(parent)/name;info=path.lstat()
   if stat.S_ISLNK(info.st_mode):
    need(path.is_relative_to(copy),'unapproved owned link outside staged framework');relative=str(path.relative_to(copy));row=source_framework.get(relative)
    need(row and row['kind']=='symlink' and os.readlink(path)==row['target'] and stat.S_IMODE(info.st_mode)==row['mode'],'extra/changed owned framework link');links.append((path,row))
   else:need(stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode),'special owned member')
 for path,row in links:
  try:resolved=path.resolve(strict=True)
  except (OSError,RuntimeError) as e:raise Refused('dangling/cyclic owned framework link') from e
  need(resolved==copy/row['resolved'],'owned framework resolved chain differs');owned_path(base,resolved,'directory' if source_framework[row['resolved']]['kind']=='directory' else 'file')
 return base

def owned_inventory(base,source_framework):
 return inventory(owned_paths(base,source_framework),False)

def reserve(root,ident):
 """Exclusive dirfd reservation; never overwrite/unlink a prior attempt."""
 identifier(ident);fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:
  for part in ('web','server'):
   nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
  try:os.mkdir('candidate-attempts',0o700,dir_fd=fd)
  except FileExistsError:pass
  nxt=os.open('candidate-attempts',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
  os.mkdir(ident,0o700,dir_fd=fd)
 finally:os.close(fd)
 base=Path(attempt(root,ident));need(str(base.resolve())==str(base),'reserved root identity')
 for name in ('deps-signed','release','debug','tmp','logs','verification'):(base/name).mkdir(mode=0o700)
 return base

def stage_copy(root,ident,expected):
 """Called only after the complete real execution gate and attempt reservation."""
 import shutil
 src=Path(root)/FRAMEWORK;dest=Path(attempt(root,ident))/'deps-signed/SDL2.framework'
 need(inventory(src)==validate_framework(expected),'framework changed before copy')
 need(not dest.exists() and not dest.is_symlink(),'staging destination exists')
 shutil.copytree(src,dest,symlinks=True,copy_function=shutil.copy2)
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
  need(origin in view.declared_inputs and view.hash(canonical)==view.declared_inputs[origin],'undeclared/changed actual consumed dependency')
  if beneath(origin,root):need(origin[len(root)+1:] in view.source_entries,'consumed project header absent from source package')
  result[canonical]={'origin':origin,'sha256':view.hash(canonical)}
 return dict(sorted(result.items()))

def protected_inventory(root,active=None,omit_container=False,browser_sdk='/private/tmp/outbreak-web-sdk'):
 """Private before/after membership/mode/link ledger, not a source manifest."""
 out={};root=Path(root)
 for base in [root,*([Path(browser_sdk)] if browser_sdk is not None else [])]:
  if not base.exists():continue
  for p in base.rglob('*'):
   if base==root and '.git' in p.relative_to(root).parts:continue
   if active and (p==Path(active) or Path(active) in p.parents):continue
   if omit_container and p==root/'web/server/candidate-attempts':continue
   info=p.lstat();row={'mode':stat.S_IMODE(info.st_mode)}
   if stat.S_ISLNK(info.st_mode):row.update(kind='symlink',target=os.readlink(p))
   elif stat.S_ISREG(info.st_mode):row.update(kind='file',bytes=info.st_size,sha256=sha(p.read_bytes()))
   elif stat.S_ISDIR(info.st_mode):row.update(kind='directory')
   else:raise Refused('special protected file')
   out[str(p)]=row
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
