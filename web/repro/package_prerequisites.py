#!/usr/bin/env python3
"""T095 fixed-source DATA producer; stdlib only, no project/SDK execution."""
import argparse
import hashlib
import gzip
import json
import os
from pathlib import Path,PurePosixPath
import re
import stat
import sys
import tarfile
import time
import zlib
import unicodedata
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
SDK=Path('/private/tmp/outbreak-web-sdk')
SDK_NAME='/private/tmp/outbreak-web-sdk'
NODE_REL='node/24.19.0_64bit/bin/node'
NODE_SHA='27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1'
ALIASES=['notes/decisions/D044-approved-sdk-aliases.json','notes/decisions/D046-html-minifier-alias.json']
METADATA={ALIASES[0]:'7b78d4f0ce74b2e1f24459429409ba9e0350e52902b3b600f07c936b5684154f',
 ALIASES[1]:'3ff2a582732afcda98ef07a43384146f93dc39b22c84dbe16e91ca7ca702f01c',
 'web/build/sdk-inspection/sources-and-artifacts.json':'4821e94178a3ed6c8273566001ff636ee45d557c00a8cf10cb2d911bfaf991b2',
 'web/build/generated/t026/port-integrity.json':'b752e4a753e8dda2e9571076bb74af3835ea13a4d798747427995ade23781ae1',
 'web/build/network-config.json':'8b812996585a268aa79acfc113bdd392af3b87b45486fb92fa3b9882b4dc62ba',
 'web/build/notices/provenance.json':'ce91e13c375ca54eb9663a78158cc165db9bed21ca7e54ecc8d4af499b0e06b0'}
PNG_RECIPE='3dc04566b3e646400f7b180ff3cc5d539146008e3b416bcb3e2e34fe53189911'
PORT_NAMES=['sdl2','sdl2_image','zlib','vorbis','ogg','libpng']
BUNDLE='web/repro/prerequisite-bundles/T095/ports-emscripten-7.0.0.tar.gz'
PRODUCER='web/repro/package_prerequisites.py'
STAGER='web/repro/stage_prerequisites.py'
MANIFEST='web/repro/prerequisites.json'
MAX_MEMBERS=100000
MAX_BYTES=1024**3
MAX_COMPRESSED=512*1024**2
MAX_JSON=64*1024**2
MAX_TAR=MAX_BYTES+MAX_MEMBERS*6144+10240
GZIP=bytes.fromhex('1f8b08000000000002ff')

def require(ok,message):
    if not ok:raise ValueError(message)
def canonical(value):return json.dumps(value,indent=2,sort_keys=True)+'\n'
def digest(data,algorithm='sha256'):return hashlib.new(algorithm,data).hexdigest()
def hash_file(path,algorithm='sha256'):
    h=hashlib.new(algorithm)
    with Path(path).open('rb') as f:
        for data in iter(lambda:f.read(1048576),b''):h.update(data)
    return h.hexdigest()
def path_name(name):
    require(type(name)is str and 0<len(name.encode('utf-8'))<=4096,'bounded path string')
    p=PurePosixPath(name)
    require(bool(p.parts) and not p.is_absolute() and str(p)==name and '..' not in p.parts and '\\' not in name and ':' not in name and all(unicodedata.category(c) not in ('Cc','Cf','Cs') for c in name),'unsafe path')
    return name
def clean(path):
    p=Path(path).absolute()
    require('..' not in p.parts and not any(q.is_symlink() for q in (p,*p.parents)),'linked/escaping path')
    return p
def ordinary(path):
    p=clean(path);s=p.stat()
    require(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'ordinary unlinked file required')
    return p
def keys(value,names):require(type(value)is dict and set(value)==set(names),'exact object keys')
def integer(value,lo,hi):require(type(value)is int and lo<=value<=hi,'bounded integer')
def sha_string(value,length=64):require(type(value)is str and re.fullmatch('[0-9a-f]{%d}'%length,value) is not None,'digest encoding')
def load_json(data):
    require(len(data)<=MAX_JSON,'JSON bound')
    def pairs(rows):
        result={}
        for k,v in rows:require(k not in result,'duplicate JSON key');result[k]=v
        return result
    return json.loads(data,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError('nonfinite JSON')))

def environment():
    """Read/hash accepted metadata and SDK leaves; never import or execute them."""
    metadata={}
    for name,pin in METADATA.items():
        data=ordinary(ROOT/path_name(name)).read_bytes();require(digest(data)==pin,'accepted metadata changed: '+name)
        metadata[name]=load_json(data)
    require(ordinary(SDK/'upstream/emscripten/emscripten-version.txt').read_text().strip().strip('"')=='7.0.0','SDK version')
    require(ordinary(SDK/'upstream/emscripten/emscripten-revision.txt').read_text().strip()=='777e6e5db7b4990bcaeb1b9998ed642cc84e6629','compiler revision')
    require(hash_file(ordinary(SDK/NODE_REL))==NODE_SHA,'Node identity')
    for name in ALIASES:
        data=metadata[name];base=clean(Path(data['root']));require(base.is_relative_to(clean(SDK)),'SDK alias root')
        records={r['path']:r for r in data['aliases']}
        for alias,row in records.items():
            current=Path(alias);seen=set()
            require(current.is_relative_to(base),'alias outside root')
            while current.is_symlink():
                clean(current.parent)
                require(str(current) in records and str(current) not in seen,'undeclared alias/cycle')
                seen.add(str(current));record=records[str(current)]
                require(os.readlink(current)==record['link_text'],'alias changed')
                current=Path(os.path.normpath(current.parent/record['link_text']))
                require(current.is_relative_to(base),'alias escape')
            require(str(current)==row['resolved_path'] and hash_file(ordinary(current))==row['resolved_sha256'],'alias target identity')
        for path,pin in data.get('inspected_supporting_files',{}).items():
            require(Path(path).is_relative_to(clean(SDK)) and hash_file(ordinary(Path(path)))==pin,'SDK supporting identity')
    cfg=metadata['web/build/network-config.json']
    require(cfg['sdk_root']==SDK_NAME and cfg['sdk_version']=='7.0.0' and cfg['compiler_revision']=='777e6e5db7b4990bcaeb1b9998ed642cc84e6629','SDK config identity')
    specs=metadata['web/build/sdk-inspection/sources-and-artifacts.json']['ports']
    specs=specs+[dict(name='libpng',expected_sha512=cfg['libpng_sha512'],recipe_sha256=PNG_RECIPE)]
    require([r['name'] for r in specs]==PORT_NAMES,'six fixed ordered ports')
    for row in specs:
        recipe='upstream/emscripten/tools/ports/'+row['name']+'.py'
        require(hash_file(ordinary(SDK/recipe))==row['recipe_sha256'],'recipe identity')
    notices=metadata['web/build/notices/provenance.json'];selected=[];licenses={}
    for row in notices:
        if Path(row['output']).name in ('emscripten.txt','sdl2.txt','sdl2-image.txt','zlib.txt','vorbis.txt','ogg.txt','libpng.txt'):
            name=path_name(row['output']);require(hash_file(ordinary(ROOT/name))==row['sha256'],'notice identity')
            selected.append(dict(path=name,sha256=row['sha256']))
            marker='/web/build/.cache/'
            if marker in row['source']:
                require(row['source'].count(marker)==1,'ambiguous source license provenance')
                licenses[path_name(row['source'].split(marker,1)[1])]=row['sha256']
    require(len(selected)==7 and len(licenses)==6,'seven accepted notices/six source licenses')
    provenance=[dict(path=n,sha256=v) for n,v in METADATA.items()]+selected
    sdk=dict(root=SDK_NAME,version='7.0.0',compiler_revision='777e6e5db7b4990bcaeb1b9998ed642cc84e6629',
             node=dict(path=SDK_NAME+'/'+NODE_REL,sha256=NODE_SHA),alias_decisions=[dict(path=n,sha256=METADATA[n]) for n in ALIASES])
    return sdk,specs,sorted(provenance,key=lambda r:r['path']),licenses

def manifest_schema(m):
    keys(m,('schema_version','kind','recipe','sdk','ports','cache','producer'))
    integer(m['schema_version'],1,1);require(m['kind']=='FROZEN_BROWSER_PREREQUISITES' and m['recipe']=='network_v1','manifest identity')
    keys(m['sdk'],('root','version','compiler_revision','node','alias_decisions'))
    keys(m['sdk']['node'],('path','sha256'));sha_string(m['sdk']['node']['sha256'])
    require(type(m['sdk']['alias_decisions'])is list and len(m['sdk']['alias_decisions'])==2,'alias array')
    for row in m['sdk']['alias_decisions']:keys(row,('path','sha256'));path_name(row['path']);sha_string(row['sha256'])
    require(type(m['ports'])is list and len(m['ports'])==6,'port array')
    for row in m['ports']:
        keys(row,('name','archive','archive_sha256','archive_sha512','recipe','recipe_sha256'))
        path_name(row['archive']);path_name(row['recipe'])
        for name in ('archive_sha256','recipe_sha256'):sha_string(row[name])
        sha_string(row['archive_sha512'],128)
    keys(m['cache'],('bundle','expanded_bytes','members'));keys(m['cache']['bundle'],('path','bytes','sha256'))
    require(m['cache']['bundle']['path']==BUNDLE,'fixed bundle identity');integer(m['cache']['bundle']['bytes'],1,MAX_COMPRESSED);sha_string(m['cache']['bundle']['sha256'])
    integer(m['cache']['expanded_bytes'],1,MAX_BYTES)
    members=m['cache']['members'];require(type(members)is list and 0<len(members)<=MAX_MEMBERS,'bounded member array')
    names=[];folded=set();total=0;table={}
    for row in members:
        require(type(row)is dict and row.get('kind') in ('file','directory'),'ordinary member type')
        keys(row,('path','kind','mode','bytes','sha256') if row['kind']=='file' else ('path','kind','mode'))
        name=path_name(row['path']);integer(row['mode'],420,493);require(row['mode'] in (420,493),'canonical mode')
        if row['kind']=='directory':require(row['mode']==493,'directory searchability')
        require(name.casefold() not in folded,'case collision/duplicate member');folded.add(name.casefold());names.append(name);table[name]=row
        if row['kind']=='file':integer(row['bytes'],0,MAX_BYTES);sha_string(row['sha256']);total+=row['bytes'];require(total<=MAX_BYTES,'expanded size overflow')
    require(names==sorted(names) and total==m['cache']['expanded_bytes'],'member order/total')
    for name in names:
        for parent in PurePosixPath(name).parents:
            if str(parent)!='.':require(str(parent) in table and table[str(parent)]['kind']=='directory','missing/non-directory ancestor')
    keys(m['producer'],('source','stager','provenance'))
    for key,path in (('source',PRODUCER),('stager',STAGER)):
        keys(m['producer'][key],('path','sha256'));require(m['producer'][key]['path']==path,'code identity path');sha_string(m['producer'][key]['sha256'])
    require(type(m['producer']['provenance'])is list and len(m['producer']['provenance'])<=128,'bounded provenance')
    for row in m['producer']['provenance']:keys(row,('path','sha256'));path_name(row['path']);sha_string(row['sha256'])
    return table

def tar_header(row):
    info=tarfile.TarInfo(row['path']);info.type=tarfile.REGTYPE if row['kind']=='file' else tarfile.DIRTYPE
    info.mode=row['mode'];info.size=row.get('bytes',0);info.uid=info.gid=info.mtime=0;info.uname=info.gname=''
    return info.tobuf(format=tarfile.PAX_FORMAT,encoding='utf-8',errors='strict')

class GzipReader:
    def __init__(self,stream):
        self.stream=stream;self.z=zlib.decompressobj(31);self.pending=b'';self.buf=bytearray();self.total=0;self.end=False;self.h=hashlib.sha256()
    def pump(self):
        require(not self.end,'truncated tar')
        if not self.pending:
            self.pending=self.stream.read(65536);require(self.pending,'truncated gzip');self.h.update(self.pending)
        data=self.z.decompress(self.pending,65536);self.pending=self.z.unconsumed_tail
        self.total+=len(data);require(self.total<=MAX_TAR,'decompression expansion bound');self.buf.extend(data)
        if self.z.eof:
            require(not self.z.unused_data and not self.pending and not self.stream.read(1),'trailing/concatenated gzip')
            self.end=True
    def take(self,size):
        require(0<=size<=65536,'bounded tar read')
        while len(self.buf)<size:self.pump()
        data=bytes(self.buf[:size]);del self.buf[:size];return data
    def finish(self):
        while not self.end:self.pump()
        require(not self.buf,'trailing tar payload')

def validate_archive(stream,m,writer=None):
    stream.seek(0);require(stream.read(10)==GZIP,'canonical gzip header');stream.seek(0)
    reader=GzipReader(stream);offset=0;archive512={row['archive']:row['archive_sha512'] for row in m['ports']}
    for row in m['cache']['members']:
        expected=tar_header(row);require(len(expected)<=65536,'bounded PAX header')
        require(reader.take(len(expected))==expected,'noncanonical/undeclared/missing tar header or PAX metadata');offset+=len(expected)
        if row['kind']=='directory':
            if writer:writer(row,None)
            continue
        h=hashlib.sha256();h512=hashlib.sha512();remaining=row['bytes']
        target=writer(row,'BEGIN') if writer else None
        try:
            while remaining:
                data=reader.take(min(65536,remaining));remaining-=len(data);h.update(data);h512.update(data)
                if target:target.write(data)
            require(h.hexdigest()==row['sha256'],'tar member hash')
            if row['path'] in archive512:require(h512.hexdigest()==archive512[row['path']],'port archive SHA512')
        finally:
            if target:target.close()
        padding=(-row['bytes'])%512;require(reader.take(padding)==bytes(padding),'nonzero tar file padding');offset+=row['bytes']+padding
    require(reader.take(1024)==bytes(1024),'tar EOF');offset+=1024
    padding=(-offset)%10240;require(reader.take(padding)==bytes(padding),'tar final padding');reader.finish()
    require(reader.h.hexdigest()==m['cache']['bundle']['sha256'],'compressed bytes changed/late mutation')

def validate_context(m):
    table=manifest_schema(m);sdk,specs,provenance,licenses=environment()
    require(m['sdk']==sdk and m['producer']['provenance']==provenance,'SDK/provenance identity')
    for key in ('source','stager'):
        record=m['producer'][key];require(hash_file(ordinary(ROOT/record['path']))==record['sha256'],'producer/stager source identity')
    for row,spec in zip(m['ports'],specs):
        require(row['name']==spec['name'] and row['recipe']=='upstream/emscripten/tools/ports/'+spec['name']+'.py' and row['recipe_sha256']==spec['recipe_sha256'] and row['archive_sha512']==spec['expected_sha512'],'port/recipe identity')
        require(row['archive'].startswith('ports/'+row['name']+'.') and row['archive'].endswith(('.zip','.tar.gz')) and '/' not in row['archive'][6:],'retained source archive path')
        require(row['archive'] in table and table[row['archive']]['kind']=='file' and table[row['archive']]['sha256']==row['archive_sha256'],'retained source archive member')
    for name,pin in licenses.items():require(name in table and table[name].get('sha256')==pin,'source license preservation')
    return table

def tree_snapshot(root):
    root=clean(root);rows=[];folded=set();total=0
    def walk(directory):
        nonlocal total
        for child in sorted(directory.iterdir(),key=lambda p:p.name):
            name=path_name(str(child.relative_to(root)));s=child.lstat();mode=stat.S_IMODE(s.st_mode)
            require(name.casefold() not in folded,'cache case collision');folded.add(name.casefold())
            require(mode in (420,493),'unsupported cache mode')
            if stat.S_ISDIR(s.st_mode):
                require(mode==493,'directory searchability');rows.append(dict(path=name,kind='directory',mode=mode));walk(child)
            else:
                require(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'cache link/special/hardlink')
                total+=s.st_size;require(total<=MAX_BYTES,'cache expanded bound')
                rows.append(dict(path=name,kind='file',mode=mode,bytes=s.st_size,sha256=hash_file(child)))
            require(len(rows)<=MAX_MEMBERS,'cache member bound')
    walk(root);return sorted(rows,key=lambda r:r['path'])

SOURCE_MODES={0o644:0o644,0o755:0o755,0o600:0o644,0o664:0o644,0o775:0o755}
PRIVATE='web/repro/prerequisite-bundles/T095'

def source_inventory(source):
    """Full raw identity; D094 normalization applies only to new package records."""
    source=clean(source);rows=[];folded=set();total=0
    def walk(directory):
        nonlocal total
        for p in sorted(directory.iterdir(),key=lambda q:q.name):
            name=path_name(str(p.relative_to(source)));s=p.lstat();mode=stat.S_IMODE(s.st_mode)
            require(name.casefold() not in folded,'source case collision');folded.add(name.casefold())
            require(mode in SOURCE_MODES,'unapproved source mode')
            if stat.S_ISDIR(s.st_mode):
                require(SOURCE_MODES[mode]==0o755,'source directory searchability')
                rows.append(dict(path=name,kind='directory',mode=mode));walk(p)
            else:
                require(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'source link/hardlink/special')
                total+=s.st_size;require(total<=MAX_BYTES,'source expanded bound')
                rows.append(dict(path=name,kind='file',mode=mode,bytes=s.st_size,sha256=hash_file(p)))
            require(len(rows)<=MAX_MEMBERS,'source member bound')
    walk(source);require(total>0,'empty source cache')
    return sorted(rows,key=lambda r:r['path'])

def package_members(raw):return [dict(row,mode=SOURCE_MODES[row['mode']]) for row in raw]

def dependency_provenance(source,raw):
    allowed={'build','js_output','node_compile_cache','ports','sanity.txt','symbol_lists','sysroot','sysroot_install.stamp'}
    require({PurePosixPath(r['path']).parts[0] for r in raw}<=allowed,'unknown/game cache root')
    names={row['path'] for row in raw if row['kind']=='file'};objects=[]
    for row in raw:
        name=row['path'];parts=PurePosixPath(name).parts
        if row['kind']=='file' and name.endswith(('.o','.obj')):
            require(len(parts)>3 and parts[0]=='build' and parts[1] in PORT_NAMES and name.endswith('.o'),'game/unknown object refused')
            basename=PurePosixPath(name[:-2]).name
            require(any(p.startswith('ports/'+parts[1]+'/') and PurePosixPath(p).name==basename for p in names),'port object source provenance absent')
            with ordinary(source/name).open('rb') as f:require(f.read(8)==b'\0asm\x01\0\0\0','port object is not expected Wasm')
            objects.append(dict(path=name,sha256=row['sha256'],origin='SDK recipe port build; retained source basename '+basename))
    return dict(dependency_objects=objects,source_archives_retained=True,sysroot='Frozen installed Emscripten SDK headers/libraries',
                compiler_caches='Retained Emscripten JS support/symbol and Node compiled-code caches; DATA only, not executed by packaging',
                game_object_reuse=False,license_interpretation='Existing accepted provenance/notices retained; no relicense or public redistribution claim')

def bundle_write(source,bundle,members):
    started=time.monotonic();offset=0
    def timed():require(time.monotonic()-started<=120,'compression deadline exceeded')
    with bundle.open('xb') as raw:
        with gzip.GzipFile(filename='',fileobj=raw,mode='wb',compresslevel=9,mtime=0) as stream:
            for row in members:
                timed();header=tar_header(row);stream.write(header);offset+=len(header)
                if row['kind']=='file':
                    h=hashlib.sha256();size=0
                    with ordinary(source/row['path']).open('rb') as f:
                        while True:
                            timed();data=f.read(65536)
                            if not data:break
                            stream.write(data);h.update(data);size+=len(data)
                            require(size<=row['bytes'],'source changed during read')
                    require(size==row['bytes'] and h.hexdigest()==row['sha256'],'late source mutation')
                    padding=(-size)%512;stream.write(bytes(padding));offset+=size+padding
                require(raw.tell()<=MAX_COMPRESSED,'compressed size bound')
            stream.write(bytes(1024));offset+=1024;stream.write(bytes((-offset)%10240))
    require(bundle.stat().st_size<=MAX_COMPRESSED,'compressed size bound');timed()
    return time.monotonic()-started

def create():
    began=time.monotonic();source=clean(ROOT/'web/build/.cache');out=clean(ROOT/PRIVATE)
    bundle=clean(ROOT/BUNDLE);manifest_path=clean(ROOT/MANIFEST)
    require(not bundle.exists() and not manifest_path.exists() and not (out/'create-receipt.json').exists(),'prior output/operation refused')
    freeze=load_json(ordinary(out/'source-freeze.json').read_bytes())
    keys(freeze,('schema_version','scope','producer_sha256','stager_sha256','contract_sha256','fixtures_receipt_sha256'))
    require(type(freeze['schema_version'])is int and freeze['schema_version']==1 and freeze['scope']=='FROZEN_T095_PRODUCER_STAGER','source freeze identity')
    require(hash_file(ordinary(ROOT/PRODUCER))==freeze['producer_sha256'] and hash_file(ordinary(ROOT/STAGER))==freeze['stager_sha256'],'source changed after freeze')
    require(hash_file(ordinary(ROOT/'MVP/PREREQUISITE_PACKAGE.md'))==freeze['contract_sha256'],'contract changed after freeze')
    fixture_path=ROOT/'web/repro/tests/prerequisites/FIXTURE_PASS.json'
    require(hash_file(ordinary(fixture_path))==freeze['fixtures_receipt_sha256'],'fixture receipt changed')
    fixture=load_json(fixture_path.read_bytes());require(fixture['status']=='PASS' and fixture['scope']=='FIXTURE_ONLY','fixtures did not pass')
    require(fixture['producer_sha256']==freeze['producer_sha256'] and fixture['stager_sha256']==freeze['stager_sha256'],'stale fixture/source binding')
    sdk,specs,provenance,licenses=environment();before=source_inventory(source);members=package_members(before)
    mapping={oct(mode):dict(package_mode=oct(target),entries=sum(row['mode']==mode for row in before)) for mode,target in SOURCE_MODES.items()}
    dependency=dependency_provenance(source,before);table={row['path']:row for row in members};ports=[]
    for spec in specs:
        name=spec['name'];candidates=[n for n in table if n.startswith('ports/'+name+'.') and '/' not in n[6:] and n.endswith(('.zip','.tar.gz'))]
        require(len(candidates)==1,'exact retained archive required: '+name);archive=candidates[0]
        require(hash_file(ordinary(source/archive),'sha512')==spec['expected_sha512'],'source archive SHA512')
        ports.append(dict(name=name,archive=archive,archive_sha256=table[archive]['sha256'],archive_sha512=spec['expected_sha512'],
                          recipe='upstream/emscripten/tools/ports/'+name+'.py',recipe_sha256=spec['recipe_sha256']))
    for name,pin in licenses.items():require(name in table and table[name].get('sha256')==pin,'source license absent/changed')
    for name,value in [('source-before.json',before),('mode-mapping.json',mapping),('dependency-provenance.json',dependency)]:
        target=out/name;require(not target.exists(),'prior evidence refused')
        with target.open('x') as f:f.write(canonical(value))
    receipt=dict(schema_version=1,operation='CREATE',status='STARTED',manifest_sha256=None,bundle_sha256=None,
                 source_before_sha256=hash_file(out/'source-before.json'),source_after_sha256=None,source_unchanged=None,
                 members=len(members),expanded_bytes=sum(row.get('bytes',0) for row in members),compression_seconds=None,total_seconds=None,error=None)
    report=out/'create-receipt.json'
    with report.open('x') as f:f.write(canonical(receipt))
    try:
        receipt['compression_seconds']=bundle_write(source,bundle,members)
        m=dict(schema_version=1,kind='FROZEN_BROWSER_PREREQUISITES',recipe='network_v1',sdk=sdk,ports=ports,
               cache=dict(bundle=dict(path=BUNDLE,bytes=bundle.stat().st_size,sha256=hash_file(bundle)),expanded_bytes=receipt['expanded_bytes'],members=members),
               producer=dict(source=dict(path=PRODUCER,sha256=freeze['producer_sha256']),stager=dict(path=STAGER,sha256=freeze['stager_sha256']),provenance=provenance))
        validate_context(m)
        with bundle.open('rb') as f:validate_archive(f,m)
        after=source_inventory(source)
        with (out/'source-after.json').open('x') as f:f.write(canonical(after))
        receipt['source_after_sha256']=hash_file(out/'source-after.json');receipt['source_unchanged']=before==after
        require(before==after,'original cache changed');environment()
        require(time.monotonic()-began<=180,'full package deadline exceeded')
        with manifest_path.open('x') as f:f.write(canonical(m))
        receipt['manifest_sha256']=hash_file(manifest_path);receipt['bundle_sha256']=m['cache']['bundle']['sha256'];receipt['status']='PASS'
    except Exception as error:
        receipt['status']='FAIL';receipt['error']=type(error).__name__+': '+str(error);raise
    finally:
        receipt['total_seconds']=time.monotonic()-began;report.write_text(canonical(receipt))
    return receipt

def boundary_guard(event,args):
    if event.startswith(('subprocess.','socket.')) or event in ('os.system','os.posix_spawn','os.fork','os.exec'):
        raise RuntimeError('producer process/network boundary forbidden')
    paths=[]
    if event=='open':
        path,mode,flags=args
        if isinstance(path,(str,bytes,os.PathLike)) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):paths=[path]
    elif event in ('os.mkdir','os.chmod','os.remove','os.rmdir','os.truncate','os.utime'):paths=[args[0]]
    elif event in ('os.rename','os.link'):paths=list(args[:2])
    elif event=='os.symlink':paths=[args[1]]
    for path in paths:
        p=clean(Path(os.fsdecode(path)))
        require(p==ROOT/MANIFEST or p.is_relative_to(ROOT/PRIVATE),'producer write outside new package/manifest')

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--create',action='store_true',required=True);parser.parse_args()
    sys.addaudithook(boundary_guard)
    print(canonical(create()))
if __name__=='__main__':main()

