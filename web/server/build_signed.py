#!/usr/bin/env python3
"""T039: sign contained framework COPIES, build servers, never launch them."""
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess

ROOT=Path(__file__).resolve().parents[2]
AREA=Path(__file__).resolve().parent
ORIGINAL=ROOT/'source/xcode/Frameworks/SDL2.framework'
DEPS=AREA/'deps-signed'
COPY=DEPS/'SDL2.framework'
OUT=AREA/'out-signed'
REPORT=AREA/'T039-build-report.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    result={}
    for base,dirs,files in os.walk(root,followlinks=False):
        for name in sorted([*dirs,*files]):
            p=Path(base)/name
            info=p.lstat()
            item={'mode':stat.S_IMODE(info.st_mode)}
            if stat.S_ISLNK(info.st_mode):
                target=os.readlink(p)
                assert not os.path.isabs(target) and p.resolve(strict=True).is_relative_to(root.resolve()),'escaping symlink'
                item.update(type='symlink',target=target)
            elif stat.S_ISREG(info.st_mode): item.update(type='file',size=info.st_size,sha256=sha(p))
            elif stat.S_ISDIR(info.st_mode): item.update(type='directory')
            else: raise RuntimeError('special file rejected: '+str(p))
            result[str(p.relative_to(root))]=item
    return result


def prior_outputs():
    paths=[AREA/'build-report.json',AREA/'verification.json',AREA/'release-symbols.txt',AREA/'debug-symbols.txt']
    for directory in [AREA/'out',AREA/'attempt-1',AREA/'run']:
        if directory.exists(): paths.extend(p for p in directory.rglob('*') if p.is_file() and not p.is_symlink())
    paths.extend(AREA.glob('T036-*.json'))
    return {str(p.relative_to(ROOT)):sha(p) for p in paths if p.is_file()}


def main():
    assert not any(p.exists() or p.is_symlink() for p in [DEPS,OUT,REPORT]),'new output roots required; preserve prior attempts'
    assert not any(p.is_symlink() for p in [AREA,*AREA.parents]),'unsafe output ancestry'
    original=inventory(ORIGINAL)
    preserved=prior_outputs()
    build=json.loads((AREA/'build-report.json').read_text())
    assert build['pass'] and build['modes']['release']['sha256']=='296601782e7ff1510b5c9900548bad34c28c97a73d9d571b4d5037c88a9e6005'
    accepted={}
    for item in build['modes']['release']['compile']:
        accepted.update(item['dependencies'])
    for name,digest in accepted.items(): assert sha(Path(name))==digest,'accepted input changed: '+name
    OUT.mkdir(parents=True)
    tmp=OUT/'tmp';tmp.mkdir()
    env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','TMPDIR':str(tmp),'CLANG_MODULE_CACHE_PATH':str(tmp/'modules')}
    report={'ticket':'T039 1.2','scope':'contained signing and actual native builds; NO server launch',
            'original_framework_before':original,'prior_outputs_before':preserved,'accepted_inputs':accepted,
            'steps':[],'modes':{},'errors':[],'environment':env}

    def run(argv):
        p=subprocess.run(argv,cwd=ROOT,env=env,text=True,capture_output=True,timeout=120)
        return {'argv':argv,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}

    try:
        DEPS.mkdir()
        shutil.copytree(ORIGINAL,COPY,symlinks=True,copy_function=shutil.copy2)
        report['copy_before_sign']=inventory(COPY)
        assert report['copy_before_sign']==original,'copy membership/content/mode mismatch'
        nested=COPY/'Versions/A/Frameworks/hidapi.framework'
        for bundle in [nested,COPY]:
            step=run(['/usr/bin/codesign','--force','--sign','-','--timestamp=none',str(bundle)])
            report['steps'].append(step)
            assert step['exit']==0,'ad-hoc signing failed; no fallback identity'
        report['signature_checks']=[]
        for p in [nested,nested/'Versions/A/hidapi',COPY,COPY/'Versions/A/SDL2']:
            step=run(['/usr/bin/codesign','--verify','--verbose=4',str(p)])
            report['signature_checks'].append(step)
            assert step['exit']==0,'copied signature validation failed'
        report['copy_after_sign']=inventory(COPY)
        report['signed_changes']=[name for name in set(report['copy_before_sign'])|set(report['copy_after_sign']) if report['copy_before_sign'].get(name)!=report['copy_after_sign'].get(name)]
        for name,item in original.items():
            if any(word in Path(name).name.lower() for word in ['license','copying','authors']) or name.endswith('Info.plist') or '/Headers/' in name:
                assert item==report['copy_after_sign'][name],'license/header/Info changed'
        cc=subprocess.check_output(['xcrun','--find','clang'],text=True).strip()
        cxx=subprocess.check_output(['xcrun','--find','clang++'],text=True).strip()
        sdk=subprocess.check_output(['xcrun','--show-sdk-path'],text=True).strip()
        report['toolchain']=run([cxx,'--version'])
        report['sdk']=sdk
        make=(ROOT/'source/src/Makefile').read_text()
        names=re.search(r'(?m)^SERVER_OBJS=\s*\\\n(.*?)(?=\n\S|\n\n)',make,re.S).group(1).replace('\\','').split()
        cpp=[ROOT/'source/src'/name.replace('-standalone.o','.cpp') for name in names]
        enetline=re.search(r'(?m)^libenet_la_SOURCES\s*=\s*(.*)$',(ROOT/'source/enet/Makefile.am').read_text()).group(1)
        c=[ROOT/'source/enet'/name for name in enetline.split() if name!='win32.c']
        assert len(cpp)==len(c)==8
        report['sources']=[str(p.relative_to(ROOT)) for p in [*cpp,*c]]
        source_before={str(p.relative_to(ROOT)):sha(p) for p in [*cpp,*c]}
        report['source_before']=source_before
        common=['-arch','arm64','-isysroot',sdk,'-fsigned-char']
        includes=['-I'+str(ROOT/'source/src'),'-I'+str(ROOT/'source/src/bot'),'-I'+str(ROOT/'source/enet/include'),'-I'+str(COPY/'Headers'),'-F'+str(DEPS)]
        for mode,flags in [('release',['-O3','-fomit-frame-pointer']),('debug',['-O0','-g','-D_DEBUG'])]:
            directory=OUT/mode;directory.mkdir()
            result={'compile':[],'link':None,'pass':False}
            report['modes'][mode]=result
            objects=[]
            for source in [*cpp,*c]:
                isc=source.suffix=='.c'
                obj=directory/(('enet-' if isc else '')+source.stem+'.o')
                dep=obj.with_suffix('.d')
                command=[cc if isc else cxx,*common,'-std=gnu99' if isc else '-std=gnu++11',*flags,*includes,
                         *([] if isc else ['-DSTANDALONE']),'-MD','-MF',str(dep),'-c',str(source),'-o',str(obj)]
                step=run(command)
                (directory/(obj.stem+'.compile.log')).write_text(step['stdout']+step['stderr'])
                step['source']=str(source.relative_to(ROOT))
                if dep.exists():
                    paths=shlex.split(dep.read_text().replace('\\\n',' ').split(': ',1)[1])
                    step['dependencies']={str(Path(p).resolve()):sha(Path(p)) for p in paths}
                if step['exit']==0: step.update(object_sha256=sha(obj),object_signature=run(['/usr/bin/file',str(obj)]))
                result['compile'].append(step);objects.append(str(obj))
                print(mode,source.name,step['exit'],flush=True)
            if all(step['exit']==0 for step in result['compile']):
                binary=directory/'ac_server'
                command=[cxx,*common,*flags,*objects,'-F'+str(DEPS),'-framework','SDL2','-lz','-lpthread','-Wl,-t',
                         '-Wl,-rpath,'+str(DEPS),'-Wl,-rpath,'+str(COPY/'Versions/A/Frameworks'),'-o',str(binary)]
                step=run(command)
                (directory/'link.log').write_text(step['stdout']+step['stderr'])
                result['link']=step
                if step['exit']==0:
                    result.update(binary=str(binary.relative_to(ROOT)),sha256=sha(binary),file=run(['/usr/bin/file',str(binary)]),
                                  dependencies=run(['/usr/bin/otool','-L',str(binary)]),load_commands=run(['/usr/bin/otool','-l',str(binary)]),
                                  codesign=run(['/usr/bin/codesign','--verify','--verbose=4',str(binary)]))
                    assert str(ORIGINAL) not in result['load_commands']['stdout'],'original dependency rpath leaked'
                    assert str(COPY/'SDL2') in step['stdout'] or str(COPY/'Versions/A/SDL2') in step['stdout'],'link trace does not prove copied SDL input'
                    result['pass']=result['codesign']['exit']==0
                print(mode,'link',step['exit'],flush=True)
        report['source_after']={name:sha(ROOT/name) for name in source_before}
        assert report['source_after']==source_before,'source changed during build'
        for mode in report['modes'].values():
            for step in mode['compile']:
                for name,digest in step.get('dependencies',{}).items(): assert sha(Path(name))==digest,'compiled dependency changed'
        report['build_inputs_stable']=True
    except Exception as error:
        report['errors'].append(type(error).__name__+': '+str(error))
    finally:
        report['original_framework_after']=inventory(ORIGINAL)
        report['prior_outputs_after']=prior_outputs()
        report['originals_preserved']=report['original_framework_after']==original and report['prior_outputs_after']==preserved
        report['pass']=bool(not report['errors'] and report['originals_preserved'] and len(report['modes'])==2 and all(m['pass'] for m in report['modes'].values()))
        report['runtime']='NOT RUN; signing does not prove shutdown causality'
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'pass':report['pass'],'errors':report['errors'],'originals_preserved':report['originals_preserved']},indent=2))
    return 0 if report['pass'] else 1


if __name__=='__main__':
    raise SystemExit(main())
