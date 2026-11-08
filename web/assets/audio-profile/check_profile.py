#!/usr/bin/env python3
"""T053 exact target byte/metadata comparison; does not execute configuration."""
import hashlib
import json
from pathlib import Path
from build_profile import HERE,SOURCE_ROOT,SOURCE_MANIFEST,PIN,source,upstream


def validate(root,manifest,source_manifest=None,source_root=None):
    root=Path(root)
    parent,payloads=source(source_manifest,source_root)
    expected_names=sorted(payloads)
    names=[entry['path'] for entry in manifest['entries']]
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()}
    if len(names)!=79 or names!=expected_names or actual!=set(expected_names):raise ValueError('exact derivative membership/order')
    if manifest['source_manifest_sha256']!=PIN or manifest['source_manifest']!=SOURCE_MANIFEST or manifest['upstream_inputs']!=parent['inputs']:raise ValueError('upstream manifest identities')
    parent_entries={entry['path']:entry for entry in parent['entries']}
    copied=derived=0
    for entry in manifest['entries']:
        name=entry['path'];original=payloads[name];src=parent_entries[name]
        expected=original
        if name=='config/browser.cfg':
            # Independent transform: exact full-line byte replacement, not builder derive().
            if original.count(b'\naudio 0\n')!=1 or original.count(b'\nsoundvol 0\n')!=1:raise ValueError('source exact setting lines')
            expected=original.replace(b'\naudio 0\n',b'\naudio 1\n',1).replace(b'\nsoundvol 0\n',b'\nsoundvol 96\n',1)
            recipe=dict(changes=[dict(old='audio 0',new='audio 1'),dict(old='soundvol 0',new='soundvol 96')],source_sha256=hashlib.sha256(original).hexdigest(),result_sha256=hashlib.sha256(expected).hexdigest(),upstream_config_derivation=src['derivation'],all_other_bytes_unchanged=True)
            if entry.get('derivation')!=recipe:raise ValueError('derived config provenance')
            derived+=1
        else:
            if 'derivation' in entry:raise ValueError('extra derived file')
            copied+=1
        raw=upstream.confined(root,name).read_bytes()
        if raw!=expected:raise ValueError('copied/config bytes differ: '+name)
        if entry['bytes']!=len(raw) or entry['sha256']!=hashlib.sha256(raw).hexdigest() or entry['virtual_path']!='/outbreak/'+name:raise ValueError('final size/hash/virtual path')
        provenance=dict(source_root=SOURCE_ROOT,source_manifest=SOURCE_MANIFEST,source_manifest_sha256=PIN,source_path=name,source_sha256=src['sha256'],original_provenance=src['provenance'])
        if entry['provenance']!=provenance or entry['notice']!=src['notice'] or entry['license']!=src['license']:raise ValueError('ownership/notices/provenance')
    if copied!=78 or derived!=1 or manifest['copied_files']!=78 or manifest['derived_files']!=['config/browser.cfg'] or sum(e['bytes'] for e in manifest['entries'])!=manifest['raw_bytes']:raise ValueError('derivative summary')
    if manifest['runtime_verified'] is not False or manifest['overlay_performed'] is not False:raise ValueError('unverified runtime claim')
    return dict(status='PASS',files=79,byte_identical_copies=78,sole_derived_file='config/browser.cfg',sole_config_changes=['audio 0 -> audio 1','soundvol 0 -> soundvol 96'],all_other_bytes_notices_permissions_unchanged=True,source_original_closure_verified=True,raw_bytes=manifest['raw_bytes'],actual_audio_models_runtime='NOT RUN',overlay='NOT PERFORMED')


if __name__=='__main__':
    result=validate(HERE/'pack-root',json.loads((HERE/'manifest.json').read_text()))
    (HERE/'validation.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
