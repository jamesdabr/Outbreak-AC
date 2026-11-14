"""One-shot T080 bounded local verification; deny subprocess/network/outside writes."""
import contextlib
import io
import json
import os
from pathlib import Path
import platform
import runpy
import sys
import unittest
sys.dont_write_bytecode=True
import candidate as c
import validate as v
import test_candidate


def audit(event,args):
    if event.startswith(('subprocess.','socket.')) or event in ('os.system','os.posix_spawn','os.fork','os.exec'):
        raise RuntimeError('prohibited process/network operation: '+event)
    paths=[]
    if event=='open':
        path,mode,flags=args
        if isinstance(path,(str,bytes,os.PathLike)) and (flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)):
            paths=[path]
    elif event in ('os.remove','os.rmdir','os.mkdir','os.chmod','os.truncate','os.utime'):paths=[args[0]]
    elif event in ('os.rename','os.link','os.symlink'):paths=list(args[:2])
    for path in paths:
        p=Path(os.fsdecode(path)).absolute()
        if not p.is_relative_to(c.HERE):raise RuntimeError('outside candidate write: '+str(p))


def protected():
    names=set(c.PINS)
    for folder in ('web/assets','source/src'):
        for p in (c.ROOT/folder).rglob('*'):
            if p.is_file() and not p.is_relative_to(c.HERE):names.add(str(p.relative_to(c.ROOT)))
    return {n:c.sha((c.ROOT/n).read_bytes()) for n in sorted(names)}


if __name__=='__main__':
    sys.addaudithook(audit)
    evidence=c.HERE/'evidence';evidence.mkdir(exist_ok=True)
    number=1
    while (evidence/('attempt-%d.json'%number)).exists():number+=1
    prefix=evidence/('attempt-%d'%number)
    before=protected();Path(str(prefix)+'-protected-before.json').write_text(c.canonical(before))
    stream=io.StringIO()
    with contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream):
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_candidate))
    Path(str(prefix)+'-tests.txt').write_text(stream.getvalue())
    receipt=dict(python=sys.version,platform=list(os.uname()),tests_run=result.testsRun,
                 failures=len(result.failures),errors=len(result.errors),test_log=prefix.name+'-tests.txt',
                 subprocess_network_and_outside_candidate_writes='DENIED_BY_AUDIT_HOOK')
    if result.wasSuccessful():
        runpy.run_path(str(c.HERE/'generate.py'),run_name='__main__')
        receipt['validation']=v.validate(c.HERE/'pack-root',json.loads((c.HERE/'manifest.json').read_text()))
        receipt['manifest_sha256']=c.sha((c.HERE/'manifest.json').read_bytes())
        receipt['status']='PASS'
    else:receipt['status']='FAIL';receipt['validation']='NOT RUN'
    after=protected();Path(str(prefix)+'-protected-after.json').write_text(c.canonical(after))
    receipt['protected_files']=len(before)
    receipt['protected_before_sha256']=c.sha(c.canonical(before).encode())
    receipt['protected_after_sha256']=c.sha(c.canonical(after).encode())
    receipt['protected_unchanged']=before==after
    Path(str(prefix)+'.json').write_text(c.canonical(receipt))
    print(c.canonical(receipt))
    if not result.wasSuccessful() or before!=after:raise SystemExit(1)
