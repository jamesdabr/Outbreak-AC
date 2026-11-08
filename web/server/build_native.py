#!/usr/bin/env python3
"""T033 explicit native STANDALONE build. Never executes the resulting server."""
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
AREA = Path(__file__).resolve().parent
OUT = AREA/'out'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, env=None):
    p = subprocess.run(argv, cwd=ROOT, env=env, text=True, capture_output=True, timeout=120)
    return {'argv':list(map(str,argv)), 'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}


def inputs():
    paths = list((ROOT/'source/src').rglob('*.h')) + list((ROOT/'source/src').rglob('*.cpp'))
    paths += list((ROOT/'source/enet').rglob('*.h')) + list((ROOT/'source/enet').glob('*.c'))
    paths += list((ROOT/'source/xcode/Frameworks/SDL2.framework/Versions/A/Headers').glob('*.h'))
    paths += [ROOT/'source/src/Makefile',ROOT/'source/enet/Makefile.am',
              ROOT/'source/xcode/Frameworks/SDL2.framework/Versions/A/SDL2',
              ROOT/'source/xcode/Frameworks/SDL2.framework/Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi']
    return {str(p.relative_to(ROOT)):digest(p) for p in paths if p.is_file()}


def preserved_outputs():
    candidates = list((ROOT/'source').rglob('*.o')) + list((ROOT/'source').rglob('*.a')) + list((ROOT/'source').rglob('*.gch'))
    candidates += list((ROOT/'bin_unix').glob('*')) + list((ROOT/'web/build/out').rglob('*'))
    candidates += [ROOT/'source/src'/n for n in ['ac_client','ac_server','ac_master']]
    return {str(p.relative_to(ROOT)):digest(p) for p in candidates if p.is_file()}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    tmp=AREA/'tmp'
    tmp.mkdir(exist_ok=True)
    env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','TMPDIR':str(tmp),'CLANG_MODULE_CACHE_PATH':str(tmp/'modules')}
    sdk=Path(subprocess.check_output(['xcrun','--show-sdk-path'],text=True).strip())
    cc=subprocess.check_output(['xcrun','--find','clang'],text=True).strip()
    cxx=subprocess.check_output(['xcrun','--find','clang++'],text=True).strip()
    make=(ROOT/'source/src/Makefile').read_text()
    objects=re.search(r'(?m)^SERVER_OBJS=\s*\\\n(.*?)(?=\n\S|\n\n)',make,re.S).group(1)
    sources=[ROOT/'source/src'/(n.replace('-standalone.o','.cpp')) for n in objects.replace('\\','').split()]
    enetline=re.search(r'(?m)^libenet_la_SOURCES\s*=\s*(.*)$',(ROOT/'source/enet/Makefile.am').read_text()).group(1)
    enet=[ROOT/'source/enet'/n for n in enetline.split() if n!='win32.c']
    assert len(sources)==len(enet)==8
    before=inputs()
    preserve=preserved_outputs()
    report={'scope':'real native build only; never launch', 'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'dirty_status':subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True), 'source_inputs_before':before,
            'compiler':run([cxx,'--version'],env),'sdk':str(sdk),'sdk_identity':run(['xcrun','--show-sdk-version'],env),
            'host':run(['uname','-srm'],env),'os':run(['sw_vers'],env),'sources':[str(p.relative_to(ROOT)) for p in sources],
            'enet_sources':[str(p.relative_to(ROOT)) for p in enet],'modes':{},'system_dependencies':{},'frameworks':{}}
    framework=ROOT/'source/xcode/Frameworks'
    for name in ['SDL2.framework/Versions/A/SDL2','SDL2.framework/Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi']:
        p=framework/name
        report['frameworks'][name]={'sha256':digest(p),'signature':run(['file',str(p)],env),'dependencies':run(['otool','-L',str(p)],env),'load_commands':run(['otool','-l',str(p)],env)}
    for name in ['usr/lib/libz.tbd','usr/lib/libpthread.tbd','usr/include/zlib.h','usr/include/pthread.h','SDKSettings.json']:
        p=sdk/name
        report['system_dependencies'][str(p.resolve())]=digest(p)
    common=['-arch','arm64','-isysroot',str(sdk),'-fsigned-char']
    includes=['-I'+str(ROOT/'source/src'),'-I'+str(ROOT/'source/src/bot'),'-I'+str(ROOT/'source/enet/include'),
              '-I'+str(framework/'SDL2.framework/Headers'),'-F'+str(framework)]
    for mode,opts in [('release',['-O3','-fomit-frame-pointer']),('debug',['-O0','-g','-D_DEBUG'])]:
        directory=OUT/mode
        directory.mkdir(exist_ok=True)
        binary=directory/'ac_server'
        binary.unlink(missing_ok=True)
        mode_report={'compile':[],'binary':str(binary.relative_to(ROOT)),'link':None,'status':'incomplete'}
        report['modes'][mode]=mode_report
        native_objects=[]
        for source in [*sources,*enet]:
            isc=source.suffix=='.c'
            obj=directory/(('enet-' if isc else '')+source.stem+'.o')
            dep=obj.with_suffix('.d')
            obj.unlink(missing_ok=True)
            command=[cc if isc else cxx,*common,'-std=gnu99' if isc else '-std=gnu++11',*opts,*includes,
                     *([] if isc else ['-DSTANDALONE']),'-MD','-MF',str(dep),'-c',str(source),'-o',str(obj)]
            record=run(command,env)
            log=directory/(obj.stem+'.compile.log')
            log.write_text(record['stdout']+record['stderr'])
            record.update(source=str(source.relative_to(ROOT)),log=str(log.relative_to(ROOT)))
            if record['exit']==0:
                record.update(object_sha256=digest(obj),signature=run(['file',str(obj)],env))
            if dep.is_file():
                dependencies=shlex.split(dep.read_text().replace('\\\n',' ').split(': ',1)[1])
                record['dependencies']={str(Path(p).resolve()):digest(Path(p)) for p in dependencies}
            mode_report['compile'].append(record)
            native_objects.append(str(obj))
            print(mode,source.name,record['exit'],flush=True)
        if all(r['exit']==0 for r in mode_report['compile']):
            command=[cxx,*common,*opts,*native_objects,'-F'+str(framework),'-framework','SDL2','-lz','-lpthread',
                     '-Wl,-rpath,'+str(framework),'-Wl,-rpath,'+str(framework/'SDL2.framework/Versions/A/Frameworks'),'-o',str(binary)]
            link=run(command,env)
            (directory/'link.log').write_text(link['stdout']+link['stderr'])
            mode_report['link']=link
            if link['exit']==0:
                mode_report.update(status='PASS build only',sha256=digest(binary),signature=run(['file',str(binary)],env),
                                   dependencies=run(['otool','-L',str(binary)],env),load_commands=run(['otool','-l',str(binary)],env))
            print(mode,'link',link['exit'],flush=True)
    after=inputs()
    report.update(source_inputs_after=after,input_changes=[p for p in set(before)|set(after) if before.get(p)!=after.get(p)],
                  preserved_outputs_before=preserve,preserved_outputs_after=preserved_outputs(),runtime='NOT RUN')
    report['outputs_preserved']=preserve==report['preserved_outputs_after']
    # All source changes are detected; main.cpp/browser work is concurrent but
    # unused by STANDALONE. Compile dependency hashes identify relevant headers.
    used={str(p.relative_to(ROOT)) for p in [*sources,*enet]}
    for m in report['modes'].values():
        for c in m['compile']:
            for path in c.get('dependencies',{}):
                p=Path(path)
                if p.is_relative_to(ROOT): used.add(str(p.relative_to(ROOT)))
    report['used_input_changes']=sorted(set(report['input_changes'])&used)
    report['pass']=all(m['status']=='PASS build only' for m in report['modes'].values()) and not report['used_input_changes'] and report['outputs_preserved']
    (AREA/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'pass':report['pass'],'input_changes':report['input_changes'],'used_input_changes':report['used_input_changes'],'outputs_preserved':report['outputs_preserved']},indent=2))
    return 0 if report['pass'] else 1


if __name__=='__main__':
    raise SystemExit(main())
