#!/usr/bin/env python3
"""T049: copy only pinned original packs; derive exactly five MDLCFG permissions."""
import hashlib
import json
from pathlib import Path,PurePosixPath

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
INPUTS=[dict(id='map',manifest='web/assets/original/manifest.json',root='web/assets/original/pack-root',sha256='1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3',count=41),dict(id='audio',manifest='web/assets/audio/manifest.json',root='web/assets/audio/pack-root',sha256='689941eae651adaef254cb3858f940e673661ef490c63c4821a290e9615907a3',count=19),dict(id='models',manifest='web/assets/models/manifest.json',root='web/assets/models/pack-root',sha256='7a232c7e8e238b29285f452c9e38f31dfc073cc3d0b9568352bb7a233c6b2fd1',count=19)]
PERMISSIONS=('md3load','md3skin','md3anim','mdlscale','mdltrans')
INSERT=b''.join(('scriptcontext MDLCFG '+name+'\n').encode() for name in PERMISSIONS)
MARKER=b'isolatecontext MDLCFG\n'
BROWSER='config/browser.cfg'


def canonical(value):return json.dumps(value,indent=2,sort_keys=True)+'\n'
def digest(raw):return hashlib.sha256(raw).hexdigest()


def confined(root,name):
    p=PurePosixPath(name)
    if not p.parts or p.is_absolute() or '..' in p.parts or str(p)!=name or '\\' in name or ':' in name:
        raise ValueError('non-normalized source path: '+name)
    if name!='LICENSE.txt' and p.parts[0] not in ('config','packages'):
        raise ValueError('unexpected asset path: '+name)
    if any(word in name.lower() for word in ('private','password','authkeys','.git/','saved.cfg','autoexec.cfg')):
        raise ValueError('private/profile path: '+name)
    path=root/name
    if any(item.is_symlink() for item in (root,path,*[root/parent for parent in p.parents])):
        raise ValueError('source/output symlink: '+name)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('source/output escape: '+name)
    return path


def sources(repo,specs=INPUTS,expected_count=79):
    merged={}
    for spec in specs:
        manifest_path=repo/spec['manifest'];root=repo/spec['root']
        if manifest_path.is_symlink() or root.is_symlink():raise ValueError('input manifest/root symlink')
        raw=manifest_path.read_bytes()
        if digest(raw)!=spec['sha256']:raise ValueError('input manifest pin mismatch: '+spec['id'])
        manifest=json.loads(raw)
        entries=manifest['entries'];names=[e['path'] for e in entries]
        actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()}
        if len(entries)!=spec['count'] or len(set(names))!=len(names) or actual!=set(names):raise ValueError('input exact membership: '+spec['id'])
        for entry in entries:
            name=entry['path'];path=confined(root,name)
            if name in merged:raise ValueError('input path collision: '+name)
            raw=path.read_bytes()
            if len(raw)!=entry['bytes'] or digest(raw)!=entry['sha256']:raise ValueError('input file hash/size: '+name)
            if entry['original'] is not True or entry['license']!='MIT':raise ValueError('input original ownership/license')
            notice=entry['notice']
            if notice not in actual or not confined(root,notice).is_file():raise ValueError('input notice path: '+name)
            merged[name]=(raw,dict(input=spec['id'],input_manifest=spec['manifest'],input_manifest_sha256=spec['sha256'],input_root=spec['root'],input_path=name,input_sha256=entry['sha256'],notice=notice,license=entry['license'],original=True))
    if len(merged)!=expected_count:raise ValueError('merged file count')
    return merged


def derive(raw):
    if raw.count(MARKER)!=1:raise ValueError('MDLCFG insertion marker count')
    before,after=raw.split(MARKER)
    return before+INSERT+MARKER+after


def assemble(repo,root,specs=INPUTS,expected_count=79):
    merged=sources(repo,specs,expected_count)
    if BROWSER not in merged or merged[BROWSER][1]['input']!='map':raise ValueError('browser config source')
    if root.is_symlink():raise ValueError('output root symlink')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()} if root.exists() else set()
    if actual-set(merged):raise ValueError('undeclared output files')
    for name in merged:confined(root,name)
    entries=[]
    for name,(source,provenance) in sorted(merged.items()):
        data=derive(source) if name==BROWSER else source
        entry=dict(path=name,virtual_path='/outbreak/'+name,bytes=len(data),sha256=digest(data),provenance=provenance,notice=provenance['notice'],license=provenance['license'])
        if name==BROWSER:
            entry['derivation']=dict(operation='insert literal lines immediately before existing isolatecontext MDLCFG; all other bytes unchanged',marker=MARKER.decode().rstrip('\n'),inserted_lines=INSERT.decode().splitlines(),inserted_bytes_sha256=digest(INSERT),source_sha256=digest(source),result_sha256=digest(data))
        path=confined(root,name);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
        entries.append(entry)
    return dict(schema_version=1,ticket='T049 revision2.1',profile='original-media-stage',mount='/outbreak',inputs=specs,entries=entries,raw_bytes=sum(e['bytes'] for e in entries),copied_files=expected_count-1,derived_files=[BROWSER],runtime_verified=False,unresolved_runtime_gates=['model loading/material/animation/attachment/render','audio backend/sample decode/user-gesture playback','active build/profile integration; no overlay performed'])


if __name__=='__main__':
    result=assemble(REPO,HERE/'pack-root')
    (HERE/'manifest.json').write_text(canonical(result))
    print(f'Assembled {len(result["entries"])} files / {result["raw_bytes"]} bytes; runtime NOT RUN')
