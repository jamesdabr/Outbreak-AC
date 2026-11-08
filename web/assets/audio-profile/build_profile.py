#!/usr/bin/env python3
"""T053 data-only derivative; no config evaluation or active build mutation."""
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
sys.path.insert(0,str(HERE.parent/'media-profile'))
import assemble as upstream  # Inspected T049 generator; imports only, never __main__.

PIN='9b7a01d6c1c29d0c0c68f95a418488963434ab54ac6b2dd0caa78b4bc21b299a'
SOURCE_MANIFEST='web/assets/media-profile/manifest.json'
SOURCE_ROOT='web/assets/media-profile/pack-root'
BROWSER='config/browser.cfg'
CHANGES=((b'audio 0\n',b'audio 1\n'),(b'soundvol 0\n',b'soundvol 96\n'))


def canonical(value):return json.dumps(value,indent=2,sort_keys=True)+'\n'
def digest(raw):return hashlib.sha256(raw).hexdigest()


def source(manifest_path=None,root=None):
    manifest_path=Path(manifest_path or REPO/SOURCE_MANIFEST);root=Path(root or REPO/SOURCE_ROOT)
    if manifest_path.is_symlink() or root.is_symlink():raise ValueError('source manifest/root symlink')
    data=manifest_path.read_bytes()
    if digest(data)!=PIN:raise ValueError('T049 manifest pin mismatch')
    manifest=json.loads(data);entries=manifest['entries'];names=[e['path'] for e in entries]
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()}
    if len(names)!=79 or names!=sorted(set(names)) or set(names)!=actual:raise ValueError('source exact membership')
    # Recheck original map/audio/model closure read-only with the inspected T049 helper.
    originals=upstream.sources(REPO)
    if manifest['inputs']!=upstream.INPUTS or set(originals)!=set(names):raise ValueError('upstream identities/closure')
    payloads={}
    for entry in entries:
        name=entry['path'];raw=upstream.confined(root,name).read_bytes()
        if len(raw)!=entry['bytes'] or digest(raw)!=entry['sha256']:raise ValueError('source hash/size: '+name)
        original=originals[name][0]
        expected=upstream.derive(original) if name==BROWSER else original
        if raw!=expected:raise ValueError('source original-data/permission closure: '+name)
        if entry['notice'] not in actual or not upstream.confined(root,entry['notice']).is_file():raise ValueError('source notice closure')
        payloads[name]=raw
    return manifest,payloads


def derive(raw):
    lines=raw.splitlines(keepends=True)
    for old,new in CHANGES:
        if lines.count(old)!=1:raise ValueError('exact audio setting count')
        lines[lines.index(old)]=new
    return b''.join(lines)


def build(root,manifest_path=None,source_root=None):
    root=Path(root)
    parent,payloads=source(manifest_path,source_root)
    # Prepare the only transformed content before any output writes.
    derived=derive(payloads[BROWSER])
    if root.is_symlink():raise ValueError('output root symlink')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()} if root.exists() else set()
    if actual-set(payloads):raise ValueError('undeclared output files')
    for name in payloads:upstream.confined(root,name)
    parent_entries={e['path']:e for e in parent['entries']}
    entries=[]
    for name,original in sorted(payloads.items()):
        src=parent_entries[name];raw=derived if name==BROWSER else original
        entry=dict(path=name,virtual_path='/outbreak/'+name,bytes=len(raw),sha256=digest(raw),notice=src['notice'],license=src['license'],provenance=dict(source_root=SOURCE_ROOT,source_manifest=SOURCE_MANIFEST,source_manifest_sha256=PIN,source_path=name,source_sha256=src['sha256'],original_provenance=src['provenance']))
        if name==BROWSER:
            entry['derivation']=dict(changes=[dict(old=old.decode().rstrip('\n'),new=new.decode().rstrip('\n')) for old,new in CHANGES],source_sha256=digest(original),result_sha256=digest(raw),upstream_config_derivation=src['derivation'],all_other_bytes_unchanged=True)
        path=upstream.confined(root,name);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
        entries.append(entry)
    return dict(schema_version=1,ticket='T053 revision2.5',profile='original-audio-enabled-stage',mount='/outbreak',source_manifest=SOURCE_MANIFEST,source_manifest_sha256=PIN,upstream_inputs=parent['inputs'],entries=entries,raw_bytes=sum(e['bytes'] for e in entries),copied_files=78,derived_files=[BROWSER],runtime_verified=False,overlay_performed=False,unresolved_runtime_gates=['actual user-gesture audio backend and sample playback','actual model loading/render/attachments','separately approved build integration'])


if __name__=='__main__':
    result=build(HERE/'pack-root')
    (HERE/'manifest.json').write_text(canonical(result))
    print(f'Built 79 files / {result["raw_bytes"]} bytes; actual runtime NOT RUN')
