"""Independent read-only T095 verification. No producer/stager/project imports."""
import gzip
import hashlib
import json
import os
from pathlib import Path,PurePosixPath
import stat
import sys
import tarfile
import zlib
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'web/repro/prerequisite-bundles/T095'
SDK=Path('/private/tmp/outbreak-web-sdk')
SDK_LITERAL='/private/tmp/outbreak-web-sdk'
NODE_REL='node/24.19.0_64bit/bin/node'
NODE_SHA='27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1'
MAPPING={0o644:0o644,0o755:0o755,0o600:0o644,0o664:0o644,0o775:0o755}
def sha(path,algorithm='sha256'):
    h=hashlib.new(algorithm)
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(65536),b''):h.update(b)
    return h.hexdigest()
def pairs(rows):
    d={}
    for key,value in rows:
        assert key not in d,'duplicate JSON key';d[key]=value
    return d
def load(path):return json.loads(Path(path).read_bytes(),object_pairs_hook=pairs)
def snapshot():
    cache=ROOT/'web/build/.cache';rows=[]
    for p in sorted(cache.rglob('*')):
        s=p.lstat();mode=stat.S_IMODE(s.st_mode);assert mode in MAPPING
        path=str(p.relative_to(cache));assert not p.is_symlink()
        if stat.S_ISDIR(s.st_mode):rows.append(dict(path=path,kind='directory',mode=mode))
        else:
            assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
            rows.append(dict(path=path,kind='file',mode=mode,bytes=s.st_size,sha256=sha(p)))
    return sorted(rows,key=lambda r:r['path'])
def guard(event,args):
    if event.startswith(('subprocess.','socket.')) or event in ('os.system','os.posix_spawn','os.fork','os.exec'):raise RuntimeError('verification is DATA only')
    paths=[]
    if event=='open':
        p,mode,flags=args
        if isinstance(p,(str,bytes,os.PathLike)) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):paths=[p]
    elif event in ('os.mkdir','os.chmod','os.remove','os.rmdir','os.truncate','os.utime'):paths=[args[0]]
    for path in paths:assert Path(os.fsdecode(path)).absolute()==OUT/'independent-real-verification.json','verification write outside own receipt'
def main():
    sys.addaudithook(guard)
    assert not (OUT/'independent-real-verification.json').exists()
    before=load(OUT/'source-before.json');assert before==load(OUT/'source-after.json')==snapshot()
    manifest=ROOT/'web/repro/prerequisites.json';m=load(manifest)
    assert set(m)=={'schema_version','kind','recipe','sdk','ports','cache','producer'}
    assert type(m['schema_version'])is int and m['schema_version']==1 and m['kind']=='FROZEN_BROWSER_PREREQUISITES' and m['recipe']=='network_v1'
    assert m['sdk']['root']==SDK_LITERAL and m['sdk']['version']=='7.0.0' and m['sdk']['compiler_revision']=='777e6e5db7b4990bcaeb1b9998ed642cc84e6629'
    node=m['sdk']['node'];assert node['path']==SDK_LITERAL+'/'+NODE_REL and node['sha256']==NODE_SHA and sha(SDK/NODE_REL)==node['sha256']
    for row in m['sdk']['alias_decisions']:assert sha(ROOT/row['path'])==row['sha256']
    for key in ('source','stager'):
        row=m['producer'][key];assert sha(ROOT/row['path'])==row['sha256']
    for row in m['producer']['provenance']:assert sha(ROOT/row['path'])==row['sha256']
    members=m['cache']['members'];expected=[dict(r,mode=MAPPING[r['mode']]) for r in before]
    assert members==expected and len(members)<=100000
    assert [r['path'] for r in members]==sorted(r['path'] for r in members)
    assert len({r['path'].casefold() for r in members})==len(members)
    expanded=sum(r.get('bytes',0) for r in members);assert 0<expanded<=1024**3 and expanded==m['cache']['expanded_bytes']
    b=m['cache']['bundle'];assert b['path']=='web/repro/prerequisite-bundles/T095/ports-emscripten-7.0.0.tar.gz'
    archive=ROOT/b['path'];assert archive.stat().st_size==b['bytes']<=512*1024**2 and sha(archive)==b['sha256']
    with archive.open('rb') as stream:assert stream.read(10)==bytes.fromhex('1f8b08000000000002ff')
    # Independent streaming gzip EOF/CRC/ISIZE/trailing validation.
    dec=zlib.decompressobj(31);raw_bytes=0;pending=b''
    with archive.open('rb') as stream:
        while not dec.eof:
            if not pending:pending=stream.read(65536);assert pending,'truncated gzip'
            data=dec.decompress(pending,65536);pending=dec.unconsumed_tail;raw_bytes+=len(data)
            assert raw_bytes<=1024**3+100000*6144+10240
        assert not pending and not dec.unused_data and not stream.read(1),'gzip trailing/concatenated member'
    ports={r['archive']:r for r in m['ports']};assert [r['name'] for r in m['ports']]==['sdl2','sdl2_image','zlib','vorbis','ogg','libpng']
    end=0;count=0;pax=0
    with gzip.open(archive,'rb') as gz:
        with tarfile.open(fileobj=gz,mode='r:') as tar:
            for info in tar:
                assert count<len(members);row=members[count];count+=1
                name=info.name.rstrip('/') if info.isdir() else info.name
                assert name==row['path'] and name and str(PurePosixPath(name))==name and not PurePosixPath(name).is_absolute() and '..' not in PurePosixPath(name).parts
                assert info.uid==info.gid==info.mtime==0 and info.uname==info.gname=='' and info.mode==row['mode'] and info.linkname==''
                assert set(info.pax_headers)<= {'path'};pax+=bool(info.pax_headers)
                assert (info.isdir() and row['kind']=='directory' and info.size==0) or (info.isreg() and row['kind']=='file' and info.size==row['bytes'])
                if info.isreg():
                    h=hashlib.sha256();h512=hashlib.sha512();total=0
                    with tar.extractfile(info) as payload,(ROOT/'web/build/.cache'/name).open('rb') as source:
                        while True:
                            data=payload.read(65536)
                            if not data:break
                            assert data==source.read(len(data));h.update(data);h512.update(data);total+=len(data)
                        assert not source.read(1)
                    assert total==row['bytes'] and h.hexdigest()==row['sha256']
                    if name in ports:assert h512.hexdigest()==ports[name]['archive_sha512'] and h.hexdigest()==ports[name]['archive_sha256']
                end=max(end,info.offset_data+((info.size+511)//512)*512)
            assert not tar.pax_headers
        gz.seek(end);tail=gz.read(10241)
        expected_tail=1024+(-(end+1024))%10240
        assert tail==bytes(expected_tail) and not gz.read(1) and raw_bytes==end+expected_tail,'canonical tar EOF/padding/trailing'
    assert count==len(members) and before==snapshot()
    for row in m['ports']:assert sha(SDK/row['recipe'])==row['recipe_sha256']
    receipt=load(OUT/'create-receipt.json');assert receipt['status']=='PASS' and receipt['source_unchanged'] and receipt['manifest_sha256']==sha(manifest)
    mapping_counts={oct(k):dict(package_mode=oct(v),entries=sum(row['mode']==k for row in before)) for k,v in MAPPING.items()}
    assert mapping_counts==load(OUT/'mode-mapping.json')
    value=dict(schema_version=1,scope='ACTUAL_READ_ONLY_PACKAGE_REVIEW_NOT_REAL_STAGING',status='PASS',
               manifest_sha256=sha(manifest),bundle_sha256=sha(archive),bundle_bytes=b['bytes'],members=count,
               expanded_bytes=expanded,gzip_crc_isize_eof_and_single_member=True,tar_zero_tail_bytes=expected_tail,pax_member_count=pax,
               full_member_source_bytes_modes_provenance_equal=True,raw_source_unchanged=True,mapping_counts=mapping_counts,
               real_stager_execution='NOT RUN',compiler_sdk_node_process_network_execution=False,helper_sha256=sha(Path(__file__)))
    (OUT/'independent-real-verification.json').write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps(value))
if __name__=='__main__':main()
