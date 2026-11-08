#!/usr/bin/env python3
"""T039 copied-signature and real-build inspection; never starts a server."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode=True
from build_signed import AREA, ROOT, ORIGINAL, COPY, DEPS, inventory, prior_outputs


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    report=json.loads((AREA/'T039-build-report.json').read_text())
    assert report['pass'] and not report['errors'] and report['build_inputs_stable']
    assert inventory(ORIGINAL)==report['original_framework_before']
    assert prior_outputs()==report['prior_outputs_before']
    copied=inventory(COPY)
    assert copied==report['copy_after_sign']
    system=json.loads((AREA/'build-report.json').read_text())['system_dependencies']
    for name,value in system.items(): assert sha(Path(name))==value,name
    checked={}
    for name,value in report['source_before'].items(): assert sha(ROOT/name)==value,name
    for mode in report['modes'].values():
        for unit in mode['compile']:
            assert unit['exit']==0
            obj=Path(unit['argv'][unit['argv'].index('-o')+1])
            assert sha(obj)==unit['object_sha256']
            for name,value in unit['dependencies'].items():
                assert sha(Path(name))==value,name
                checked[name]=value
        binary=ROOT/mode['binary']
        assert sha(binary)==mode['sha256']
        assert mode['link']['exit']==0 and mode['codesign']['exit']==0
        commands=mode['load_commands']['stdout']
        rpaths=re.findall(r'cmd LC_RPATH\n\s*cmdsize \d+\n\s*path (.*?) \(offset',commands)
        assert set(rpaths)=={str(DEPS),str(COPY/'Versions/A/Frameworks')},rpaths
        assert str(ORIGINAL) not in commands
    checks=[]
    for path in [COPY/'Versions/A/Frameworks/hidapi.framework',COPY/'Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi',COPY,COPY/'Versions/A/SDL2',
                 *[ROOT/mode['binary'] for mode in report['modes'].values()]]:
        command=['/usr/bin/codesign','--verify','--verbose=4',str(path)]
        result=subprocess.run(command,capture_output=True,text=True,timeout=15)
        checks.append({'argv':command,'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
        assert result.returncode==0
    displays=[]
    for path in [COPY/'Versions/A/SDL2',COPY/'Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi']:
        command=['/usr/bin/codesign','--display','--verbose=4',str(path)]
        result=subprocess.run(command,capture_output=True,text=True,timeout=15)
        assert result.returncode==0 and 'Signature=adhoc' in result.stderr
        displays.append({'argv':command,'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    licenses={name:item for name,item in copied.items() if any(word in Path(name).name.lower() for word in ['license','copying','authors'])}
    summary={'ticket':'T039 1.2','scope':'actual copies/signatures/native builds; no server execution','pass':True,
             'original_framework_preserved':True,'T033_T036_outputs_preserved':True,'signature_checks':checks,'signature_display':displays,
             'original_inventory':report['original_framework_before'],'signed_inventory':copied,'license_inventory':licenses,
             'source_header_dependencies':checked,'signed_changes':report['signed_changes'],
             'system_dependencies':system,
             'artifacts':{name:{'binary':mode['binary'],'sha256':mode['sha256'],'rpaths':re.findall(r'cmd LC_RPATH\n\s*cmdsize \d+\n\s*path (.*?) \(offset',mode['load_commands']['stdout'])} for name,mode in report['modes'].items()},
             'framework_hashes':{name:sha(COPY/name) for name in ['Versions/A/SDL2','Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi']},
             'runtime':'NOT RUN','shutdown_causality':'NOT RUN; signing is not evidence of a shutdown fix'}
    (AREA/'T039-verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'pass':True,'artifacts':summary['artifacts'],'framework_hashes':summary['framework_hashes'],'signed_changes':summary['signed_changes']},indent=2))


if __name__=='__main__':
    main()
