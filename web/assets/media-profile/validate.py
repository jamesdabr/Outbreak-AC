#!/usr/bin/env python3
"""Independent T049 exact-merge validator; no config evaluation or media decoding."""
import hashlib
import json
from pathlib import Path,PurePosixPath
from assemble import HERE,REPO,INPUTS


def checked(root,name):
    path=PurePosixPath(name)
    if not path.parts or path.is_absolute() or '..' in path.parts or str(path)!=name or '\\' in name or ':' in name:
        raise ValueError('validator rejected path: '+name)
    target=root/name
    if root.is_symlink() or any((root/p).is_symlink() for p in (path,*path.parents)) or not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('validator rejected symlink/escape: '+name)
    return target


def validate(repo,root,manifest,specs=INPUTS,expected_count=79):
    expected={}
    for spec in specs:
        mp=repo/spec['manifest'];source_root=repo/spec['root']
        if mp.is_symlink() or source_root.is_symlink():raise ValueError('validator input symlink')
        content=mp.read_bytes()
        if hashlib.sha256(content).hexdigest()!=spec['sha256']:raise ValueError('validator input manifest pin')
        source=json.loads(content)
        files=[e['path'] for e in source['entries']]
        actual={p.relative_to(source_root).as_posix() for p in source_root.rglob('*') if p.is_file() or p.is_symlink()}
        if len(files)!=spec['count'] or len(set(files))!=len(files) or set(files)!=actual:raise ValueError('validator input membership')
        for entry in source['entries']:
            name=entry['path']
            if entry['original'] is not True or entry['license']!='MIT':raise ValueError('validator source ownership/license')
            if name in expected:raise ValueError('validator source collision')
            data=checked(source_root,name).read_bytes()
            if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:raise ValueError('validator input file hash')
            if entry['notice'] not in actual:raise ValueError('validator input notice')
            expected[name]=(data,spec,entry)
    entries=manifest['entries'];names=[e['path'] for e in entries]
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()}
    if len(expected)!=expected_count or names!=sorted(expected) or actual!=set(expected):raise ValueError('validator exact output membership/order')
    if manifest['inputs']!=specs:raise ValueError('validator manifest input identities')
    copied=derived=0
    for entry in entries:
        name=entry['path'];original,spec,src=expected[name]
        desired=original
        if name=='config/browser.cfg':
            lines=original.splitlines(keepends=True)
            markers=[i for i,line in enumerate(lines) if line==b'isolatecontext MDLCFG\n']
            if len(markers)!=1 or spec['id']!='map':raise ValueError('validator config insertion marker/source')
            commands=[b'scriptcontext MDLCFG md3load\n',b'scriptcontext MDLCFG md3skin\n',b'scriptcontext MDLCFG md3anim\n',b'scriptcontext MDLCFG mdlscale\n',b'scriptcontext MDLCFG mdltrans\n']
            desired=b''.join(lines[:markers[0]]+commands+lines[markers[0]:])
            recipe=entry.get('derivation',{})
            expected_recipe=dict(operation='insert literal lines immediately before existing isolatecontext MDLCFG; all other bytes unchanged',marker='isolatecontext MDLCFG',inserted_lines=[c.decode().rstrip('\n') for c in commands],inserted_bytes_sha256=hashlib.sha256(b''.join(commands)).hexdigest(),source_sha256=src['sha256'],result_sha256=hashlib.sha256(desired).hexdigest())
            if recipe!=expected_recipe:raise ValueError('validator exact derived recipe')
            derived+=1
        else:
            if 'derivation' in entry:raise ValueError('validator unexpected derivation')
            copied+=1
        raw=checked(root,name).read_bytes()
        if raw!=desired:raise ValueError('validator copied/derived bytes or extra command mismatch: '+name)
        if entry['sha256']!=hashlib.sha256(raw).hexdigest() or entry['bytes']!=len(raw) or entry['virtual_path']!='/outbreak/'+name:raise ValueError('validator final hash/size/virtual path')
        expected_provenance=dict(input=spec['id'],input_manifest=spec['manifest'],input_manifest_sha256=spec['sha256'],input_root=spec['root'],input_path=name,input_sha256=src['sha256'],notice=src['notice'],license=src['license'],original=True)
        if entry['provenance']!=expected_provenance or entry['notice']!=src['notice'] or entry['license']!=src['license']:raise ValueError('validator notice/provenance')
    if copied!=expected_count-1 or derived!=1 or manifest['copied_files']!=copied or manifest['derived_files']!=['config/browser.cfg'] or sum(e['bytes'] for e in entries)!=manifest['raw_bytes']:raise ValueError('validator summary counts')
    if manifest['runtime_verified'] is not False:raise ValueError('validator runtime claim')
    return dict(status='PASS',files=expected_count,copied_byte_identical=copied,derived_browser_cfg=derived,exact_five_MDLCFG_lines=True,all_other_config_bytes_unchanged=True,all_notices_preserved=True,raw_bytes=manifest['raw_bytes'],actual_media_load_render_playback='NOT RUN',active_overlay='NOT PERFORMED')


if __name__=='__main__':
    result=validate(REPO,HERE/'pack-root',json.loads((HERE/'manifest.json').read_text()))
    (HERE/'validation.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
