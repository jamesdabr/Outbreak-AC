#!/usr/bin/env python3
"""Inspect T033 objects/dependencies without executing a server binary."""
import hashlib
import json
from pathlib import Path
import shlex
import subprocess

AREA=Path(__file__).resolve().parent
ROOT=AREA.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    report=json.loads((AREA/'build-report.json').read_text())
    dependencies={}
    for dep in (AREA/'out').rglob('*.d'):
        for name in shlex.split(dep.read_text().replace('\\\n',' ').split(': ',1)[1]):
            p=Path(name).resolve()
            dependencies[str(p)]=digest(p)
    mismatches=[]
    for mode in report['modes'].values():
        for compile in mode['compile']:
            for name,value in compile.get('dependencies',{}).items():
                if dependencies[name]!=value: mismatches.append(name)
            if 'object_sha256' in compile:
                obj=Path(compile['argv'][compile['argv'].index('-o')+1])
                assert digest(obj)==compile['object_sha256']
    assert not mismatches
    assert not report['used_input_changes'] and report['outputs_preserved']
    # Only actual compiler dependencies must remain stable. Other workers may
    # change unrelated browser-only sources without invalidating these objects.
    for name,value in report['source_inputs_after'].items():
        absolute=str((ROOT/name).resolve())
        if absolute in dependencies: assert digest(ROOT/name)==value, name
    binary_symbols={}
    for name,mode in report['modes'].items():
        binary=ROOT/mode['binary']
        if 'sha256' in mode:
            assert digest(binary)==mode['sha256']
            nm=subprocess.run(['nm','-g',str(binary)],text=True,capture_output=True,check=True,timeout=20)
            symbols=nm.stdout
            assert '_main' in symbols and '_enet_host_create' in symbols and 'serverslice' in symbols
            (AREA/(name+'-symbols.txt')).write_text(symbols)
            binary_symbols[name]={'sha256':digest(binary),'real_main_enet_serverslice_symbols_present':True}
        else: assert not binary.exists()
    binary=ROOT/report['modes']['release']['binary']
    result={'scope':'binary/source/dependency inspection only','dependency_hashes':dependencies,'dependency_mismatches':mismatches,
            'release_binary_sha256':digest(binary),'real_main_enet_serverslice_symbols_present':True,
            'binary_symbols':binary_symbols,
            'input_changes_during_build':report['input_changes'],'existing_outputs_preserved':report['outputs_preserved'],
            'release':report['modes']['release']['status'],'debug':report['modes']['debug']['status'],'runtime':'NOT RUN'}
    (AREA/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS available binary/input/object/dependency integrity; no server launched')


if __name__=='__main__':
    main()
