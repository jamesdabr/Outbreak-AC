"""T164 guarded pure preparation; never run a real build or old project module."""
import ast
import argparse
import copy
from contextlib import ExitStack,redirect_stdout,redirect_stderr
import difflib
import hashlib
import importlib.abc
import importlib.util
import io
import json
import os
from pathlib import Path,PurePosixPath
import shutil
import selectors
import signal
import socket
import stat
import subprocess
import sys
import time
from types import SimpleNamespace
from html.parser import HTMLParser
from unittest.mock import patch

sys.dont_write_bytecode=True
HERE=Path(__file__).absolute().parent
ROOT=HERE.parents[2]
PREP=HERE/'tests/preparation-1'
PASS_ID='T211-full-1'
PREPARATION_EXPIRED=[False]
BUDGET_CHECK=lambda:None
class PreparationDeadline(BaseException):pass
CASE_NAMES=('positive-full-graph','read-only-verifier','exclusive-receipt','real-context-refuses-fixture','plan-entrypoint','build-entrypoint','verify-entrypoint','config-define','config-profile','config-unknown','config-bool','unit-order','header-absent','source-changed','acceptance-ref','source-manifest-missing','source-manifest-old-path','source-manifest-self','source-manifest-mode','pins-digest','pins-authority','pins-release','pins-unknown','pins-observation','pins-source-acceptance','pins-decision','pack-79','pack-revision','pack-map-size','pack-virtual','pack-notice','pack-license','pack-source-path','pack-local-rehash','pack-extra','pack-missing','pack-hardlink','pack-symlink','pack-traversal','cfg-order','cfg-allowlist','notice-changed','notice-extra','json-duplicate','json-nan','json-float','json-bool-int','id-traversal','alias-text','alias-extra','native-role-consumed','browser-role-consumed','role-rearm','late-role-hardlink','pre-post-mismatch','system-header-omitted','consumer-header-omitted','undeclared-header','stale-object','late-object','late-input','command-argv','command-env','command-exit','command-reap','command-log','command-order','result-unknown','result-claim','result-fixture','metadata-byte','bundle-ID','slice-79','slice-gap','slice-overlap','slice-hash','slice-suffix','bundle-extra','bundle-extra-directory','publication-missing','phase-new-file','phase-new-directory','phase-removed','phase-link-change','occupied-attempt','occupied-publication','partial-reservation','cache-copy','pre-command','compile-command','link-command','syntax-command','wasm-command','publication-write','result-write','freeze-write','report-failure','report-flush','marker-remove','receipt-wrong-path','receipt-existing-wrong','marker-dominates','freeze-member','freeze-unknown','plan-byte','log-byte')

def sha(data):return hashlib.sha256(data).hexdigest()
def canonical(value):return (json.dumps(value,sort_keys=True,indent=2)+'\n').encode()

class MemoryFS:
    fixture_only=True
    def __init__(self):self.nodes={'/':dict(kind='directory',mode=493,nlink=1,data=b'')};self.whole_end=None;self.fail_write=None;self.fail_mkdir=None;self.fail_remove=False;self._hashes={};self._parents={};self._children=None
    def put(self,p,data=b'',mode=420,kind='file',nlink=1,**extras):
        BUDGET_CHECK()
        for parent in reversed(PurePosixPath(p).parents):self.nodes.setdefault(str(parent),dict(kind='directory',mode=493,nlink=1,data=b''))
        self.nodes[p]=dict(kind=kind,mode=mode,nlink=nlink,data=data,**extras)
        assert len(self.nodes)<=4096,'pinned virtual node cap'
        self._children=None
    def data_hash(self,p):
        data=self.nodes[p]['data'];cached=self._hashes.get(p)
        if cached is None or cached[0] is not data:self._hashes[p]=(data,sha(data))
        return self._hashes[p][1]
    def exists(self,p):return p in self.nodes
    def stat(self,p):
        BUDGET_CHECK()
        if p not in self.nodes:raise FileNotFoundError(p)
        n=self.nodes[p];return dict(kind=n['kind'],mode=n['mode'],nlink=n['nlink'],bytes=len(n['data']),device=n.get('device',17),inode=n.get('inode',31),mtime_ns=n.get('mtime_ns',101),ctime_ns=n.get('ctime_ns',102),identity=(n['kind'],n['mode'],n['nlink'],n['data']))
    def ordinary(self,p,directory=False,launcher=False):
        if p not in self._parents:self._parents[p]=tuple(str(parent) for parent in reversed(PurePosixPath(p).parents))
        for parent in self._parents[p]:assert self.nodes[parent]['kind']=='directory','fixture ancestor alias'
        s=self.stat(p)
        if s['kind']!=('directory' if directory else 'file'):raise ValueError('ordinary kind')
        if not directory and s['nlink']!=1 and not (launcher and p in ('/usr/bin/clang','/usr/bin/clang++','/usr/bin/otool') and s['mode']==493):raise ValueError('single-link consumption')
        return s
    def read(self,p,maximum=32*1024*1024):
        self.ordinary(p)
        if len(self.nodes[p]['data'])>maximum:raise ValueError('read cap')
        return self.nodes[p]['data']
    def record(self,p,launcher=False):
        s=self.ordinary(p,launcher=launcher);return dict(bytes=s['bytes'],sha256=self.nodes[p].get('FIXTURE_ONLY_role_sha256',self.data_hash(p)),mode=s['mode'])
    def hash(self,p,algorithm='sha256'):
        self.ordinary(p);return self.nodes[p].get('FIXTURE_ONLY_'+algorithm,self.data_hash(p) if algorithm=='sha256' else hashlib.new(algorithm,self.nodes[p]['data']).hexdigest())
    def protected_hash(self,p):return self.record(p,launcher=p in ('/usr/bin/clang','/usr/bin/clang++','/usr/bin/otool'))['sha256']
    def list(self,p):
        self.ordinary(p,True)
        if self._children is None:
            self._children={}
            for n in self.nodes:
                if n!='/':self._children.setdefault(str(PurePosixPath(n).parent),[]).append(n)
        return sorted(self._children.get(p,()))
    def link(self,p):
        if self.nodes[p]['kind']!='link':raise ValueError('link kind')
        return self.nodes[p]['data'].decode()
    def mkdir(self,p):
        if self.fail_mkdir and self.fail_mkdir(p):raise OSError('injected mkdir failure')
        if self.exists(p):raise FileExistsError(p)
        self.ordinary(str(PurePosixPath(p).parent),True);self.put(p,kind='directory',mode=493)
    def write_new(self,p,data,cutoff=None):
        if cutoff is not None and time.monotonic()>=cutoff:raise TimeoutError('fixture persistence cutoff')
        if self.fail_write and self.fail_write(p):raise OSError('injected write failure '+p)
        if self.exists(p):raise FileExistsError(p)
        self.ordinary(str(PurePosixPath(p).parent),True);self.put(p,bytes(data))
    def copy_file(self,source,target):self.write_new(target,self.read(source));self.nodes[target]['mode']=self.nodes[source]['mode']
    def sync(self,p):self.ordinary(p,True)
    def remove_marker(self,p):
        if self.fail_remove:raise OSError('injected final marker removal failure')
        self.ordinary(p);del self.nodes[p];self._children=None
    def remove(self,p):
        for n in list(self.nodes):
            if n==p or n.startswith(p+'/'):del self.nodes[n]
        self._children=None
    def dump(self):
        return {p:{**{k:v for k,v in n.items() if k!='data'},'bytes':len(n['data']),'sha256':self.data_hash(p)} for p,n in sorted(self.nodes.items())}

class FakeEffects:
    def __init__(self,module,fs,mutation=None):self.m=module;self.fs=fs;self.mutation=mutation;self.calls=[];self.reported=False;self._used=False
    def copy_cache(self,r,source,target):
        if self.mutation=='cache-copy':raise OSError('fake cache-copy failure; no SDK copy')
        self.fs.mkdir(target);inv=self.m.inventory(self.fs,source)
        for d in sorted(inv['directories'],key=lambda s:(s.count('/'),s)):self.fs.mkdir(target+'/'+d)
        for p in inv['files']:self.fs.copy_file(source+'/'+p,target+'/'+p)
    def report(self,result):
        if self.mutation in ('report-failure','report-flush'):raise OSError('injected report/write-or-flush')
        if self.mutation=='late-report-input':
            p=next(p for p in result['observation']['inputs'] if p.endswith('/source/src/cube.h'));self.fs.nodes[p]['data']+=b'FIXTURE_ONLY late report mutation'
        self.reported=True
    def run(self,r,argv,env,log):
        self.calls.append(argv[:]);a,_=r.paths('fixture');base=PurePosixPath(log).name
        failure={'pre-command':'00-pre.log','compile-command':'00-compile.log','link-command':'link.log','syntax-command':'syntax.log','wasm-command':'wasm_validation.log'}.get(self.mutation)
        if base==failure:raise OSError('injected command failure, no process')
        if '-M' in argv:
            source=argv[-1];dep=argv[argv.index('-MF')+1];obj=argv[argv.index('-MT')+1]
            deps=[source,r.repo('source/src/cube.h'),r.repo('source/enet/include/enet/enet.h'),self.m.SDK+'/upstream/include/FIXTURE_ONLY_system.h',a+'/cache/sysroot/include/FIXTURE_ONLY_cache.h']
            if source in (r.repo('source/src/main.cpp'),r.repo('source/src/client.cpp'),r.repo('source/src/clients2c.cpp')):deps.append(r.repo('source/src/browser_map_profile.h'))
            if self.mutation=='system-header-omitted':deps.remove(self.m.SDK+'/upstream/include/FIXTURE_ONLY_system.h')
            if self.mutation=='consumer-header-omitted' and source==r.repo('source/src/client.cpp'):deps.remove(r.repo('source/src/browser_map_profile.h'))
            if self.mutation=='undeclared-header':deps.append(r.repo('source/src/UNDECLARED.h'))
            self.fs.write_new(dep,(obj+': '+' '.join(deps)+'\n').encode())
            if self.mutation=='stale-object':self.fs.write_new(obj,self.m.MAGIC+b'FIXTURE_ONLY stale')
        elif '-c' in argv:
            source=argv[argv.index('-c')+1];obj=argv[argv.index('-o')+1];post=argv[argv.index('-MF')+1];pre=post.replace('.post.d','.pre.d')
            data=self.fs.read(pre)
            if self.mutation=='system-header-omitted':data=data.rstrip(b'\n')+b' '+(self.m.SDK+'/upstream/include/FIXTURE_ONLY_system.h').encode()+b'\n'
            if self.mutation=='pre-post-mismatch':data=data.replace(r.repo('source/src/cube.h').encode(),r.repo('source/enet/include/enet/enet.h').encode())
            self.fs.write_new(post,data);self.fs.write_new(obj,self.m.MAGIC+b'FIXTURE_ONLY fresh '+source.encode())
            if self.mutation=='late-object' and base=='01-compile.log':self.fs.nodes[a+'/objects/00.o']['data']+=b'changed'
            if self.mutation=='late-input':self.fs.nodes[r.repo('source/src/cube.h')]['data']+=b'changed'
        elif base=='link.log':
            manifest=json.loads(self.fs.read(r.repo('web/assets/blackwood-profile/manifest.json')));data=bytearray();slices=[]
            for e in manifest['entries']:
                start=len(data);data.extend(self.fs.read(r.repo('web/assets/blackwood-profile/pack-root/'+e['path'])));slices.append('{filename:"%s",start:%d,end:%d}'%(e['virtual_path'],start,len(data)))
            self.fs.write_new(a+'/bundle/index.data',bytes(data));self.fs.write_new(a+'/bundle/index.js',('/* FIXTURE_ONLY never executed */\nvar metadata=['+','.join(slices)+'];').encode())
            self.fs.write_new(a+'/bundle/index.html',b'<!doctype html><canvas id="canvas"></canvas><script src="index.js"></script><!-- FIXTURE_ONLY -->');self.fs.write_new(a+'/bundle/index.wasm',self.m.MAGIC)
        output=b'FIXTURE_ONLY simulated command\n'
        supervisor=dict(schema_version=1,kind='BLACKWOOD_COMMAND_SUPERVISOR',fixture_only=True,pid=424242,leader_exit_observed=0,original_handle_reaped=True,exit_code=0,group=dict(anchor_acquired=True,anchor_confirmed_before_signal=True,signal_attempted=True,signal_result='SENT_ANCHORED',closure='ABSENT_AFTER_ANCHORED_CLEANUP',closed=True,permission_observation=None),primary=None,cleanup=[],cleanup_actions=['cached_returncode','confirm_unreaped_anchor','kill_owned_group','wait_original_handle','observe_group_absence','selector_close','stdin_close','stdout_close','stderr_close'],child_log_bytes=len(output),child_log_sha256=sha(output),hard_deadline_ms=120000,work_deadline_ms=115000)
        self.fs.write_new(log,output+self.m.SUPERVISOR_FRAME+self.m.canonical(supervisor))
        record=dict(argv=argv[:],environment=dict(env),exit_code=0,log=log,log_sha256=sha(self.fs.read(log)),log_bytes=len(self.fs.read(log)),elapsed_ms=0,failure=None,owned_process_reaped=True)
        if not self._used:
            if self.mutation=='command-argv':record['argv']+=['FORGED']
            if self.mutation=='command-env':record['environment']['HOME']='FORBIDDEN'
            if self.mutation=='command-exit':record['exit_code']=1
            if self.mutation=='command-reap':record['owned_process_reaped']=False
            if self.mutation=='command-log':record['log_sha256']='0'*64
            self._used=True
        return record

def main():
    real_clock=time.monotonic;start=real_clock();path=PREP/PASS_ID
    frozen_raw=(ROOT/'notes/proposals/T211-guarded-source-plan-3.md').read_bytes();assert len(frozen_raw)<8388608
    frozen=json.loads(frozen_raw.decode().split(chr(96)*3+'json\n')[1].split('\n'+chr(96)*3)[0])
    for name,row in frozen['sources'].items():
        raw=(ROOT/name).read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256'],'frozen source changed before full regression'
    for job in ('deadline-1','history-1'):
        focused=HERE/'tests/T211/preparation-1'/job;focused_result=json.loads((focused/'result.json').read_bytes())
        assert focused_result['status']=='PASS_FOCUSED_GUARDED_ONLY' and focused_result['source_hashes']=={p:row['sha256'] for p,row in frozen['sources'].items()} and not (focused/'failure.json').exists(),'T211 focused PASS/source pins required; outer exit0 separately mandatory'
    path.mkdir()
    sources={n:(HERE/n).read_bytes() for n in ('recipe.py','build.py','verify.py','config.json','shell.html','SCHEMA.md','README.md','test_recipe.py')}
    for n,b in sources.items():ast.parse(b,filename=n) if n.endswith('.py') else None
    original_paths=['web/build/candidate_recipe.py','web/build/profile_client.py','web/build/build_candidate.py','web/build/verify_candidate.py','web/build/network-config.json','web/build/network-shell.html','web/runtime/admission_v4/admission.py','source/src/Makefile']
    original_paths+=['tickets/T174.md','MVP/BLACKWOOD_BUILD_PREPARATION.md','MVP/BUILDER_TERMINAL_GROUP_CLOSURE.md','notes/decisions/D263-builder-terminal-group-corrections.md','notes/reviews/MAIN-T174-source-baseline-1/manifest.json']
    original_paths+=['notes/reviews/MAIN-T174-source-baseline-1/'+n for n in sources]
    original_paths+=['tickets/T177.md','notes/decisions/D269-strict-original-reap-builder-correction.md','notes/decisions/D271-builder-original-cutoff-clarification.md','notes/reviews/MAIN-T177-source-baseline-1/manifest.json','tests/outbreak/builder_reap/T177/test_reap.py','notes/proposals/T177-engine-two-job-plan-1.md','notes/reviews/T174-terminal-group-correction-review-1.md']
    original_paths+=['notes/reviews/MAIN-T177-source-baseline-1/'+n for n in sources]
    original_paths+=['source/src/'+n for n in ('main.cpp','client.cpp','clients2c.cpp','browser_map_profile.h')]
    public={}
    roots=['web/assets/blackwood-profile/pack-root','web/assets/network-profile/pack-root','web/assets/blackwood-candidate/pack-root','web/build/notices']
    for root in roots:
        for p in sorted((ROOT/root).rglob('*')):
            if p.is_file():public[str(p.relative_to(ROOT))]=p.read_bytes()
    for name in ('web/assets/blackwood-profile/manifest.json','web/assets/blackwood-profile/PROVENANCE.json','web/assets/network-profile/manifest.json','web/assets/blackwood-candidate/manifest.json','source/src/Makefile','source/src/main.cpp','source/src/client.cpp','source/src/clients2c.cpp','source/src/browser_map_profile.h','web/transport/enet_websocket.c','web/transport/enet_websocket.js','web/transport/enet_ws_bridge.h','source/src/browsernet.h','notes/decisions/D044-approved-sdk-aliases.json','notes/decisions/D046-html-minifier-alias.json','notes/decisions/D223-T163-source-helper-acceptance.md','notes/handoffs/T163-engine-final-freeze-1.md','notes/reviews/MAIN-T163-final-freeze-review-1.json'):public[name]=(ROOT/name).read_bytes()
    public['notes/decisions/D235-Darwin-nonreaping-wait-adapter.md']=(ROOT/'notes/decisions/D235-Darwin-nonreaping-wait-adapter.md').read_bytes()
    require_bytes=sum(map(len,public.values()));assert require_bytes<=8*1024*1024
    protected={n:sha((ROOT/n).read_bytes()) for n in original_paths};protected.update({n:sha(b) for n,b in public.items()})
    (path/'sources').mkdir()
    for n,b in sources.items():(path/'sources'/n).write_bytes(b)
    plan=dict(kind='T211_BLACKWOOD_FULL_GUARDED_REGRESSION',fixture_only=True,pass_id=PASS_ID,cases=list(CASE_NAMES),case_cap=148,whole_seconds=300,stdout_stderr_cap=8388608,retained_bytes_cap=134217728,public_data_bytes=require_bytes,sources={n:sha(b) for n,b in sources.items()},effects='deny all real process/control/network/signing/SDK-copy/version/old-project imports before new module import; writes confined to this fresh pass',production_execution=False)
    plan['supervisor_cases']=list(SUPERVISOR_CASES);plan['virtual_node_cap']=4096;plan['deadline_checks']='every actual recipe require and virtual filesystem stat/put, two-second retention reserve, expiry cannot become expected negative'
    plan['observer_cases']=list(OBSERVER_CASES)
    plan['receipt_race_cases']=list(RECEIPT_RACE_CASES)
    plan['persistence_cases']=list(PERSISTENCE_CASES)
    plan['authority']='T1771.1/D269/D271';plan['baseline_manifest_sha256']='ba722457ad9f005bd67de94ad3b56d9d5be3a7cb03875c60179e151dce8ec1b6'
    plan['terminal_policy_cases']={name:list(variants) for name,variants in TERMINAL_CASES.items()};plan['group_count']=148;plan['leaf_scenario_count']=256;plan['leaf_cap']=256
    (path/'plan.json').write_bytes(canonical(plan));(path/'protected-before.json').write_bytes(canonical(protected))
    (path/'diffs').mkdir()
    for new,old in (('recipe.py','web/build/candidate_recipe.py'),('build.py','web/build/build_candidate.py'),('verify.py','web/build/verify_candidate.py'),('config.json','web/build/network-config.json'),('shell.html','web/build/network-shell.html')):
        (path/'diffs'/(new+'.diff')).write_text(''.join(difflib.unified_diff((ROOT/old).read_text().splitlines(True),sources[new].decode().splitlines(True),fromfile=old,tofile='web/build/blackwood/'+new)))
    for name in ('recipe.py','test_recipe.py','SCHEMA.md','README.md'):
        baseline=ROOT/'notes/reviews/MAIN-T174-source-baseline-1'/name
        (path/'diffs'/(name+'.T174.diff')).write_text(''.join(difflib.unified_diff(baseline.read_text().splitlines(True),sources[name].decode().splitlines(True),fromfile=str(baseline.relative_to(ROOT)),tofile='web/build/blackwood/'+name)))
    for name in ('recipe.py','test_recipe.py','SCHEMA.md','README.md'):
        baseline=ROOT/'notes/reviews/MAIN-T177-source-baseline-1'/name
        (path/'diffs'/(name+'.T177.diff')).write_text(''.join(difflib.unified_diff(baseline.read_text().splitlines(True),sources[name].decode().splitlines(True),fromfile=str(baseline.relative_to(ROOT)),tofile='web/build/blackwood/'+name)))
    denials=[];phase=['import'];active=[True]
    def denied(*args,**kwargs):denials.append('real effect denied');raise AssertionError('T164 forbidden real effect')
    class OldImports(importlib.abc.MetaPathFinder):
        def find_spec(self,fullname,path=None,target=None):
            if fullname in ('candidate_recipe','profile_client') or fullname.startswith(('web.build.','web.server.','web.runtime.')):denials.append('old import denied');raise AssertionError('old project import denied')
    finder=OldImports();sys.meta_path.insert(0,finder)
    def audit(event,args):
        if not active[0]:return
        if event.startswith(('subprocess.','socket.','os.fork','os.exec','os.posix_spawn','os.system','os.kill','shutil.copy','ctypes.')):denials.append(event);raise AssertionError('forbidden audited effect '+event)
        if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
            p=Path(os.fsdecode(args[0])).absolute();flags=args[2] if len(args)>2 and type(args[2]) is int else 0;mode=args[1] if len(args)>1 else ''
            writing=bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)) or (isinstance(mode,str) and any(c in mode for c in 'wax+'))
            if writing and not p.is_relative_to(path):raise AssertionError('write outside fresh fixture pass '+str(p))
            if not writing and p.is_relative_to(ROOT) and p not in [HERE/n for n in sources] and not p.is_relative_to(path):raise AssertionError('unexpected real project read '+str(p))
        if event in ('os.mkdir','os.remove','os.rmdir','os.chmod','os.rename','os.link','os.symlink'):
            candidates=args[:2] if event in ('os.rename','os.link','os.symlink') else args[:1]
            for p in candidates:
                if isinstance(p,(str,bytes,os.PathLike)) and not Path(os.fsdecode(p)).absolute().is_relative_to(path):raise AssertionError('mutation outside fixture pass')
    sys.addaudithook(audit)
    class BoundedCapture(io.StringIO):
        def __init__(self):super().__init__();self.byte_count=0
        def write(self,value):
            count=len(value.encode());assert self.byte_count+count<=8388608,'captured output cap before growth'
            self.byte_count+=count;return super().write(value)
    rows=[];captured=BoundedCapture()
    def deadline_check():
        if real_clock()-start>=298:
            PREPARATION_EXPIRED[0]=True;raise PreparationDeadline('guarded pure in-case deadline; 2s retention reserve')
    global BUDGET_CHECK
    BUDGET_CHECK=deadline_check
    try:
        with ExitStack() as guards,redirect_stdout(captured),redirect_stderr(captured):
            for module,names in ((subprocess,('Popen','run','call','check_call','check_output')),(os,('fork','forkpty','execv','execve','execvp','execvpe','posix_spawn','posix_spawnp','system','kill','killpg','wait','waitpid','waitid','uname')),(time,('sleep',)),(signal,('alarm','setitimer','signal')),(socket,('socket','create_connection')),(shutil,('copy','copy2','copyfile','copytree'))):
                for n in names:
                    if hasattr(module,n):guards.enter_context(patch.object(module,n,denied))
            with ExitStack() as imports:
                for obj,n in ((Path,'open'),(Path,'read_bytes'),(Path,'read_text'),(os,'walk'),(os,'scandir'),(os,'listdir')):imports.enter_context(patch.object(obj,n,denied))
                for name in ('recipe','build','verify'):
                    spec=importlib.util.spec_from_file_location(name,HERE/(name+'.py'))
                    # Compile the already pinned bytes: standard SourceLoader probes
                    # __pycache__ even with bytecode writes disabled.
                    spec.loader.get_code=lambda fullname,data=sources[name+'.py'],filename=str(HERE/(name+'.py')):compile(data,filename,'exec',dont_inherit=True)
                    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
            phase[0]='fixtures';m=sys.modules['recipe']
            original_require=m.require
            def guarded_require(ok,message):deadline_check();return original_require(ok,message)
            m.require=guarded_require
            # Guard proofs occur after all denial boundaries are active.
            for call in (lambda:subprocess.Popen(['FORBIDDEN']),lambda:os.fork(),lambda:os.kill(0,0),lambda:os.waitpid(0,0),lambda:signal.alarm(1),lambda:socket.socket(),lambda:shutil.copytree('/private/tmp/outbreak-web-sdk',str(path/'forbidden')),lambda:importlib.import_module('candidate_recipe')):
                try:call()
                except AssertionError:pass
                else:raise AssertionError('guard did not deny')
            base=make_fixture(m,public,sources)
            positive=clone_recipe(m,base)
            report=positive.execute_candidate('fixture',positive.repo('notes/decisions/FIXTURE_ONLY.json'),positive.fixture_pin)
            assert report['fixture_only'] is True and len(positive.effects.calls)==125
            verified=positive.verify_candidate('fixture',positive.repo('notes/decisions/FIXTURE_ONLY.json'),positive.fixture_pin)
            assert verified['status']=='FIXTURE_ONLY'
            (path/'positive-graph.json').write_bytes(canonical(dict(kind='FIXTURE_ONLY',nodes=positive.fs.dump(),result=report,verification=verified)))
            (path/'positive-raw').mkdir()
            for n in (*m.ARTIFACTS,'build-metadata.json'):(path/'positive-raw'/n).write_bytes(positive.fs.read(positive.paths('fixture')[0]+'/bundle/'+n))
            (path/'positive-raw'/'logs').mkdir()
            for n in ('00-pre.log','00-compile.log','link.log','syntax.log','wasm_validation.log'):(path/'positive-raw'/'logs'/n).write_bytes(positive.fs.read(positive.paths('fixture')[0]+'/logs/'+n))
            for name in CASE_NAMES:
                if PREPARATION_EXPIRED[0] or real_clock()-start>=298:raise PreparationDeadline('guarded pure pass deadline')
                run_case(m,base,positive,name,rows)
            assert len(rows)==len(CASE_NAMES)==148
            leaf_count=sum(len(row['subcases']) if 'subcases' in row else 1 for row in rows);assert leaf_count==256<=256
            assert sum(p.stat().st_size for p in path.rglob('*') if p.is_file())<=134217728
            (path/'cases.json').write_bytes(canonical(rows));(path/'guard.json').write_bytes(canonical(dict(status='PASS',import_effects='DENIED',old_imports='DENIED',real_processes=0,real_tool_probes=0,real_SDK_copies=0,real_network=0,real_FFI_calls=0,denials=denials,fixture_only=True)))
        active[0]=False
        after={n:sha((ROOT/n).read_bytes()) for n in protected};assert after==protected
        assert all((HERE/n).read_bytes()==b for n,b in sources.items()),'current sources changed during guarded pass'
        (path/'protected-after.json').write_bytes(canonical(after))
        text=captured.getvalue().encode();assert len(text)<=8388608;(path/'stdout-stderr.bin').write_bytes(text)
        assert sum(p.stat().st_size for p in path.rglob('*') if p.is_file())<=134217728,'complete retained fixture byte cap'
        result=dict(status='PASS_GUARDED_PREPARATION_ONLY',fixture_only=True,cases=len(rows),leaf_scenarios=leaf_count,source_sha256={n:sha(b) for n,b in sources.items()},real_processes=0,real_compiler_Node_version_signing_network_SDK_copy=0,protected_unchanged=True,elapsed_s=time.monotonic()-start,production_build=False,production_verification=False,runtime=False)
        assert real_clock()-start<300,'complete preparation pass budget'
        (path/'result.json').write_bytes(canonical(result));print(json.dumps(result));return 0
    except BaseException as e:
        active[0]=False;(path/'failure.json').write_bytes(canonical(dict(status='FAIL_PRESERVED',error=repr(e),elapsed_s=real_clock()-start,cases_completed=rows,stdout_stderr=captured.getvalue()[:8388608])));raise
    finally:
        active[0]=False;BUDGET_CHECK=lambda:None
        if finder in sys.meta_path:sys.meta_path.remove(finder)

def make_fixture(m,public,sources):
    MemoryFS.cutoff=m.FileSystem.cutoff
    fs=MemoryFS();root=m.HISTORICAL_ROOT
    class FixtureRecipe(m.Recipe):fixture_only=True
    r=FixtureRecipe();r.ROOT=root;r.HERE=root+'/web/build/blackwood';r.fs=fs;r.gate=m.Gate(fs);r.control_paths=set()
    for n,b in public.items():fs.put(root+'/'+n,b)
    for n,b in sources.items():fs.put(r.HERE+'/'+n,b)
    for n in m.UNITS:
        if not fs.exists(root+'/'+n):fs.put(root+'/'+n,b'// FIXTURE_ONLY uncompiled unit\n')
    for n in ('source/src/cube.h','source/src/ge25519_base.data','source/enet/include/enet/enet.h'):fs.put(root+'/'+n,b'// FIXTURE_ONLY header/data\n')
    fs.put(root+'/.git/HEAD',b'0'*40+b'\n');fs.put(root+'/notes/decisions/FIXTURE_ONLY.md',b'FIXTURE_ONLY authority never accepted by a real context\n')
    fs.put(root+'/web/FIXTURE_ONLY_history.link',b'../missing-original-history',kind='link',mode=511)
    fs.put(root+'/web/FIXTURE_ONLY_history.bin',b'FIXTURE_ONLY opaque unconsumed history')
    for index,p in enumerate((*m.HISTORICAL_FIFOS,*m.HISTORICAL_UNREADABLE)):
        fs.put(p,b'' if p in m.HISTORICAL_FIFOS else b'FIXTURE_ONLY',kind='fifo' if p in m.HISTORICAL_FIFOS else 'file',mode=420 if p in m.HISTORICAL_FIFOS else 0,device=17,inode=1000+index,mtime_ns=101,ctime_ns=102)
    fs.put(r.HERE+'/tests',kind='directory',mode=493);fs.put(root+'/tests',kind='directory',mode=493)
    for n in ('bin','lib','include','share','emscripten'):fs.put(m.SDK+'/upstream/'+n,kind='directory',mode=493)
    fs.put(m.SDK+'/.emscripten',b'FIXTURE_ONLY SDK config\n');fs.put(m.SDK+'/upstream/emscripten/emscripten-version.txt',b'"7.0.0"\n');fs.put(m.SDK+'/upstream/emscripten/emscripten-revision.txt',b'777e6e5db7b4990bcaeb1b9998ed642cc84e6629\n')
    fs.put(m.SDK+'/upstream/include/FIXTURE_ONLY_system.h',b'FIXTURE_ONLY system header\n');fs.put(root+'/web/build/.cache/sysroot/include/FIXTURE_ONLY_cache.h',b'FIXTURE_ONLY copied cache dependency\n')
    fs.put('/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11',b'FIXTURE_ONLY Python role, not executable',mode=493,FIXTURE_ONLY_role_sha256='4e28e811a89aeac6eed668ae641c7f85f5831e42e8dc6cd9a85a3bcc032ec46a')
    fs.put(m.SDK+'/node/24.19.0_64bit/bin/node',b'FIXTURE_ONLY Node role, not executable',mode=493,FIXTURE_ONLY_role_sha256='27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1')
    for name in ('em++','emcc'):fs.put(m.SDK+'/upstream/emscripten/'+name,b'FIXTURE_ONLY compiler, never launched',mode=493)
    for p,h in m.DARWIN_WAIT_HEADERS.items():fs.put(p,b'FIXTURE_ONLY ABI header role; not a real SDK copy',FIXTURE_ONLY_role_sha256=h)
    for p,h in m.CTYPES_INPUTS.items():fs.put(p,b'FIXTURE_ONLY ctypes input role; never imported',FIXTURE_ONLY_role_sha256=h)
    for n in m.ALIAS_PINS:
        doc=json.loads(public[n])
        for a in doc['aliases']:
            fs.put(a['path'],a['link_text'].encode(),kind='link',mode=511);fs.put(a['resolved_path'],b'FIXTURE_ONLY named tool target',mode=493,FIXTURE_ONLY_role_sha256=a['resolved_sha256'])
        for p,h in doc.get('inspected_supporting_files',{}).items():fs.put(p,b'FIXTURE_ONLY supporting tool',FIXTURE_ONLY_role_sha256=h)
    for s in m.PORT_SPECS:
        fs.put(m.SDK+'/upstream/emscripten/tools/ports/'+s['name']+'.py',b'FIXTURE_ONLY port recipe',FIXTURE_ONLY_role_sha256=s['recipe_sha256'])
        fs.put(root+'/web/build/.cache/ports/'+s['name']+'.FIXTURE_ONLY.zip',b'FIXTURE_ONLY archive '+s['name'].encode(),FIXTURE_ONLY_sha512=s['expected_sha512'])
    r.effects=FakeEffects(m,fs)
    # Enumerate the actual consumed source subset, then author only FICTIONAL control.
    cfg=r.config();r.units();r.pack(cfg);r.notices();consumed=r.repository_inputs()
    entries=[dict(path=p[len(root)+1:],**fs.record(p)) for p in sorted(consumed)]
    decision='notes/decisions/FIXTURE_ONLY.md';entries.append(dict(path=decision,**fs.record(root+'/'+decision)));entries.sort(key=lambda e:e['path'])
    fs.put(root+'/'+m.SOURCE_MANIFEST,canonical(dict(schema_version=1,kind='SOURCE_INPUT_MANIFEST',source_revision='0'*40,entries=entries)))
    cfg,manifest,observed,rev,source,acceptance=r.observe()
    auth=dict(schema_version=1,kind='CANDIDATE_BLACKWOOD_BUILD_AUTHORIZATION',authority='MAIN',status='ACCEPTED',execution_release='EXPLICIT_BLACKWOOD_NETWORK_BUILD_EXECUTION',recipe=m.RECIPE,ticket='FIXTURE_ONLY T164 never real execution',candidate_id='fixture',decision=decision,source_revision=rev,source_manifest=source,bindings=dict(repository=root,sdk=m.SDK,ports_cache=root+'/web/build/.cache'),source_acceptance=acceptance,observation=observed)
    pinpath=root+'/notes/decisions/FIXTURE_ONLY.json';fs.put(pinpath,canonical(auth));r.fixture_pin=sha(canonical(auth))
    r.gate=m.Gate(fs);return r

def clone_recipe(m,base,mutation=None):
    cls=type(base);r=cls();r.ROOT=base.ROOT;r.HERE=base.HERE;r.fs=copy.deepcopy(base.fs);r.gate=m.Gate(r.fs);r.control_paths=set();r.fixture_pin=base.fixture_pin;r.effects=FakeEffects(m,r.fs,mutation);return r

OBSERVER_CASES=('exit-zero','running','killed','dumped','wrong-pid','wrong-code','errno','wrong-ABI','binding-failure','symbol-missing','wrong-size','wrong-alignment','wrong-offset','wrong-signo','siginfo-errno','dirty-no-event','wrong-status','signal-zero','unexpected-return','wrong-platform','wrong-arch','wrong-endian','deadline','late-zero','EINTR-once','EINTR-deadline')

def observer_matrix(m):
    evidence=[]
    for name in OBSERVER_CASES:
        calls=[];clock=[102.0 if name=='deadline' else 100.0];error_number=[10];created={}
        class Array:
            def __init__(self,element,count):self.element=element;self.count=count;self.size=element.size*count;self.align=8
        class Scalar:
            def __init__(self,size,signed=False):self.size=size;self.align=size;self.signed=signed
            def __mul__(self,count):return Array(self,count)
            def __call__(self,value):return SimpleNamespace(value=value if self.signed else value%(1<<(self.size*8)))
        class Layout(type):
            def __new__(meta,clsname,bases,attrs):
                fields=attrs.get('_fields_',[])
                if fields:
                    if clsname=='Sigval':
                        assert fields==[('sival_int',fake.c_int),('sival_ptr',fake.c_void_p)]
                        offsets=dict(sival_int=0,sival_ptr=0);size=8;align=8
                    else:
                        assert clsname=='Siginfo'
                        offsets=dict(si_signo=0,si_errno=4,si_code=8,si_pid=12,si_uid=16,si_status=20,si_addr=24,si_value=32,si_band=40,si_pad=48)
                        assert [n for n,t in fields]==list(offsets)
                        assert [t for n,t in fields[:-1]]==[fake.c_int,fake.c_int,fake.c_int,fake.c_int,fake.c_uint,fake.c_int,fake.c_void_p,created['Sigval'],fake.c_long]
                        assert fields[-1][1].element is fake.c_ulong and fields[-1][1].count==7
                        if name=='wrong-offset':offsets['si_status']=24
                        size=112 if name=='wrong-size' else 104;align=16 if name=='wrong-alignment' else 8
                    attrs.update(_size=size,_align=align,_field_names=[n for n,t in fields])
                    for n,offset in offsets.items():attrs[n]=SimpleNamespace(offset=offset)
                cls=super().__new__(meta,clsname,bases,attrs);created[clsname]=cls;return cls
        class Base(metaclass=Layout):
            def __init__(self):
                for field in self._field_names:setattr(self,field,0)
        class Wait:
            def __call__(self,kind,pid,info,flags):
                assert kind==1 and pid==424242 and flags==0x25
                assert all(getattr(info,n)==0 for n in info._field_names),'whole fake record must be zeroed for every call/retry'
                calls.append(dict(idtype=kind,pid=pid,flags=flags,buffer_type=type(info).__name__,zero_before_call=True))
                if name=='errno':error_number[0]=10;return -1
                if name in ('EINTR-once','EINTR-deadline') and (name=='EINTR-deadline' or len(calls)==1):
                    info.si_pid=999;error_number[0]=4
                    if name=='EINTR-deadline':clock[0]+=.6
                    return -1
                if name=='unexpected-return':return 1
                if name not in ('running','dirty-no-event'):
                    info.si_signo=1 if name=='wrong-signo' else signal.SIGCHLD;info.si_errno=1 if name=='siginfo-errno' else 0
                    info.si_code=9 if name=='wrong-code' else 2 if name in ('killed','signal-zero') else 3 if name=='dumped' else 1
                    info.si_pid=424243 if name=='wrong-pid' else pid
                    info.si_status=9 if name=='killed' else 6 if name=='dumped' else 256 if name=='wrong-status' else 0
                if name=='dirty-no-event':info.si_code=1
                if name=='late-zero':clock[0]=102
                return 0
        wait=Wait()
        def dll(path,**kwargs):
            assert path=='/usr/lib/libSystem.B.dylib' and kwargs==dict(use_errno=True)
            if name=='binding-failure':raise OSError('FIXTURE_ONLY binding refusal')
            return SimpleNamespace() if name=='symbol-missing' else SimpleNamespace(waitid=wait)
        fake=SimpleNamespace(c_int=Scalar(8 if name=='wrong-ABI' else 4,True),c_uint=Scalar(4),c_void_p=Scalar(8),c_long=Scalar(8,True),c_ulong=Scalar(8),Union=Base,Structure=Base,CDLL=dll,sizeof=lambda t:t._size if isinstance(t,type) else t.size,alignment=lambda t:t._align if isinstance(t,type) else t.align,POINTER=lambda t:SimpleNamespace(_type_=t),byref=lambda info:info,get_errno=lambda:error_number[0])
        error=None;value='NOT_CALLED'
        with patch.dict(sys.modules,{'ctypes':fake}),patch.object(m.os,'uname',lambda:SimpleNamespace(machine='x86_64' if name=='wrong-arch' else 'arm64')),patch.object(m.sys,'platform','linux' if name=='wrong-platform' else 'darwin'),patch.object(m.sys,'byteorder','big' if name=='wrong-endian' else 'little'),patch.object(m.time,'monotonic',lambda:clock[0]):
            try:value=m.make_nonreaping_observer()(424242,101.0)
            except (ValueError,OSError,AttributeError) as e:error=str(e)
        expected={'exit-zero':0,'running':None,'killed':-9,'dumped':-6,'EINTR-once':0}
        if name in expected:assert error is None and value==expected[name],(name,error)
        else:assert error is not None,name
        if calls:
            assert wait.argtypes[0] is fake.c_int and wait.argtypes[1] is fake.c_uint and wait.argtypes[2]._type_ is created['Siginfo'] and wait.argtypes[3] is fake.c_int and wait.restype is fake.c_int
        if name=='EINTR-once':assert len(calls)==2
        if name=='EINTR-deadline':assert len(calls)==2 and clock[0]>101
        if name=='deadline':assert not calls
        evidence.append(dict(name=name,fictional_calls=calls,value=value,error=error,fixture_only=True,real_FFI_calls=0))
    return evidence

SUPERVISOR_CASES=('success','popen','pid','selector','blocking','register','select','read','unregister','observe-leader','cached-returncode','confirm-anchor','kill','wait','selector-close','stdin-close','stdout-close','stderr-close','combined','deadline','late-zero','overflow','log-write','leader-exited-descendant-open','leader-exited-descendant-eof','group-kill-failure','group-remains','anchor-lost','already-reaped','signal-esrch','probe-failure','whole-deadline')

def supervisor_matrix(m,base):
    evidence=[]
    for fault in SUPERVISOR_CASES:
        r=clone_recipe(m,base);r.started=100 if fault!='whole-deadline' else -3498;clock=[100.0];events=[];waits=[];signals=[];alive=[True];confirmed=[False]
        def fail(label):
            events.append(label)
            if fault==label or (fault=='combined' and label in ('read','cached-returncode','kill','wait','selector-close','stdin-close','stdout-close','stderr-close')):raise OSError('FIXTURE_ONLY '+label)
        class Pipe:
            closed=False
            def __init__(self,name):self.name=name
            def fileno(self):return 99
            def close(self):fail(self.name+'-close');self.closed=True
        class Process:
            def __init__(self):self.stdin=Pipe('stdin');self.stdout=Pipe('stdout');self.stderr=Pipe('stderr');self.reaped=False
            @property
            def pid(self):fail('pid');return 424242
            @property
            def returncode(self):
                fail('cached-returncode')
                if fault=='already-reaped':self.reaped=True;return 0
                return getattr(self,'consumed_code',0) if self.reaped else None
            def poll(self):raise AssertionError('must not reap ownership anchor using poll')
            @returncode.setter
            def returncode(self,value):self.consumed_code=value
            def wait(self,*args,**kwargs):raise AssertionError('Popen.wait forbidden; strict waitpid required')
        proc=Process()
        def popen(*args,**kwargs):fail('popen');assert kwargs['start_new_session'] is True;return proc
        class Selector:
            def __init__(self):fail('selector');self.mapped=True
            def register(self,*args):fail('register')
            def get_map(self):return {1:1} if self.mapped else {}
            def select(self,timeout):fail('select');return [(type('Key',(),{'fileobj':proc.stdout})(),1)]
            def unregister(self,*args):fail('unregister');self.mapped=False
            def close(self):fail('selector-close')
        def read(*args):
            events.append('read')
            if fault in ('read','combined'):raise OSError('FIXTURE_ONLY primary read')
            if fault in ('deadline','leader-exited-descendant-open'):
                clock[0]=221 if fault=='deadline' else 215.01;raise TimeoutError('FIXTURE_ONLY open descendant pipe/work deadline')
            return b'X'*16385 if fault=='overflow' else b''
        def waitid(pid,deadline):
            assert pid==424242 and clock[0]<deadline
            assert not proc.reaped,'nonreaping observation after lost anchor'
            label='confirm-anchor' if 'cached-returncode' in events else 'observe-leader';fail(label)
            if label=='confirm-anchor':
                if fault=='anchor-lost':raise ChildProcessError('FIXTURE_ONLY ECHILD')
                confirmed[0]=True
            return 0
        def kill(pid,sig):
            assert pid==424242;signals.append(sig)
            if sig==signal.SIGKILL:
                assert not proc.reaped and confirmed[0],'kill without unreaped confirmed anchor'
                fail('kill')
                if fault=='group-kill-failure':raise PermissionError('FIXTURE_ONLY denied group cleanup')
                if fault=='signal-esrch':alive[0]=False;raise ProcessLookupError('FIXTURE_ONLY anchored ESRCH')
                if fault not in ('group-remains',):alive[0]=False
            else:
                assert sig==0 and proc.reaped;events.append('probe-group')
                if fault=='probe-failure':raise OSError('FIXTURE_ONLY read-only group probe failure')
                if not alive[0]:raise ProcessLookupError('FIXTURE_ONLY group absent')
        def sleep(seconds):assert 0<=seconds<=.01;clock[0]+=max(.001,seconds)
        def blocking(*args):fail('blocking')
        log=r.repo('FIXTURE_ONLY.log')
        if fault=='log-write':r.fs.fail_write=lambda p:p==log
        def consuming_waitpid(pid,options):
            assert pid==424242 and options==m.os.WNOHANG and not proc.reaped
            waits.append(220-clock[0]);fail('wait');proc.reaped=True
            if fault=='late-zero':clock[0]=221
            return pid,0
        record=None
        with ExitStack() as patches:
            for obj,key,value in ((m.subprocess,'Popen',popen),(m.selectors,'DefaultSelector',Selector),(m.os,'set_blocking',blocking),(m.os,'read',read),(m,'make_nonreaping_observer',lambda:waitid),(m.os,'waitpid',consuming_waitpid),(m.os,'killpg',kill),(m.time,'monotonic',lambda:clock[0]),(m.time,'sleep',sleep),(m.signal,'getsignal',lambda sig:signal.SIG_DFL),(m,'MAX_LOG',32768)):
                patches.enter_context(patch.object(obj,key,value))
            try:record=m.Effects().run(r,['FIXTURE_ONLY never launched'],{},log)
            except m.ProcessRefusal as e:record=e.record
            if fault in ('success','leader-exited-descendant-eof','signal-esrch'):
                assert record['failure'] is None and record['owned_process_reaped'] is True
                m.inspect_command_log(r.fs.read(log),True)
        assert record is not None
        if fault not in ('success','leader-exited-descendant-eof','signal-esrch'):
            assert record['failure'] is not None,fault
            state=json.loads(record['failure']);assert set(state)>=set(('primary','cleanup','cleanup_actions','original_handle_reaped','group','child_log_bytes','child_log_sha256'))
            if fault not in ('popen','whole-deadline'):
                if clock[0]<220:assert all(n+'-close' in events for n in ('stdin','stdout','stderr')),(fault,events)
                else:assert all(n+'-close' not in events for n in ('stdin','stdout','stderr')) and any(e['error']=='SKIPPED_EXPIRED_UNRESOLVED' for e in state['cleanup']),(fault,events)
            if fault=='combined':assert len(state['cleanup'])>=6 and state['primary'] is not None
            if fault in ('deadline','anchor-lost','already-reaped','whole-deadline'):assert signal.SIGKILL not in signals
            if fault=='deadline':assert not waits
            if fault=='late-zero':assert record['owned_process_reaped'] is True and record['exit_code']==0
            if fault=='overflow':assert state['child_log_bytes']==0
            if fault=='log-write':assert 'retention' in state and record['owned_process_reaped'] is True
            if fault=='leader-exited-descendant-open':assert state['group']['closed'] is True and record['owned_process_reaped'] is True
            if fault in ('group-remains','group-kill-failure'):assert state['group']['closed'] is False
        assert all(sig in (0,signal.SIGKILL) for sig in signals)
        evidence.append(dict(fault=fault,events=events,signals=signals,wait_timeouts=waits,record=record,retained_log=r.fs.read(log).decode() if r.fs.exists(log) else None,fixture_only=True))
    return evidence

PERSISTENCE_CASES=('command-expired-before-log','receipt-preparation-late','open-late','chmod-late','fdopen-late','write-late','flush-late','fsync-late','raw-close-late','fd-close-late','raw-close-error','fd-close-error','write-partial-late','write-error','flush-error','fsync-error','short-write-success','retention-inclusive-success','full-child-expired-outer-ledger','full-whole-expired-no-ledger','outer-ledger-write-late','helper-already-expired')

class FakePersistence:
    """Only fake descriptor integers and memory nodes; actual helper control flow."""
    def __init__(self,m,fs,clock,name):self.m=m;self.fs=fs;self.clock=clock;self.name=name;self.contexts=[];self.events=[];self.active=None;self.descriptors={}
    def begin(self,stage):
        c=self.active;assert c['cutoff'] is None or self.clock[0]<c['cutoff'],('new expired persistence effect',self.name,stage,c)
        assert self.clock[0]<3700,('new expired whole-attempt effect',stage)
        self.events.append(dict(stage=stage,phase=c['phase'],at=self.clock[0],cutoff=c['cutoff']))
        if self.name==stage.replace('_','-')+'-error' and c['phase']=='CHILD_LOG':raise OSError('FIXTURE_ONLY '+stage+' failure')
    def finish(self,stage):
        c=self.active
        if c['phase']=='CHILD_LOG':
            late=self.name==stage.replace('_','-')+'-late' or (stage=='write' and self.name in ('write-partial-late','full-child-expired-outer-ledger','full-whole-expired-no-ledger','outer-ledger-write-late'))
            if late:self.clock[0]=3701 if self.name=='full-whole-expired-no-ledger' else c['cutoff']+.125
            elif self.name=='retention-inclusive-success':self.clock[0]+=.01
        elif c['phase']=='OUTER_FAIL_LEDGER' and stage=='write' and self.name=='outer-ledger-write-late':self.clock[0]=c['cutoff']+.125
    def open(self,path,flags,mode):
        self.begin('open');assert flags==(self.m.os.O_WRONLY|self.m.os.O_CREAT|self.m.os.O_EXCL|self.m.os.O_NOFOLLOW) and mode==420
        assert path==self.active['path'] and not self.fs.exists(path)
        self.fs.put(path,b'');fd=7700+len(self.descriptors);self.descriptors[fd]=self.active;self.active['fd']=fd;self.finish('open');return fd
    def chmod(self,fd,mode):self.begin('chmod');assert fd==self.active['fd'] and mode==420;self.finish('chmod')
    def fdopen(self,fd,mode,buffering,closefd):
        self.begin('fdopen');assert fd==self.active['fd'] and mode=='wb' and buffering==0 and closefd is False
        outer=self
        class Raw:
            closed=False
            def write(self,data):
                outer.begin('write');c=outer.active;n=7 if outer.name in ('short-write-success','write-partial-late') and c['writes']==0 else len(data);n=min(n,len(data))
                outer.fs.nodes[c['path']]['data']+=bytes(data[:n]);c['writes']+=1;outer.finish('write');return n
            def flush(self):outer.begin('flush');outer.finish('flush')
            def close(self):outer.begin('raw_close');self.closed=True;outer.active['raw_closed']=True;outer.finish('raw_close')
        raw=Raw();self.active['raw']=raw;self.finish('fdopen');return raw
    def fsync(self,fd):self.begin('fsync');assert fd==self.active['fd'];self.finish('fsync')
    def close(self,fd):self.begin('fd_close');assert fd==self.active['fd'];self.active['fd_closed']=True;self.finish('fd_close')
    def write_new(self,path,data,cutoff=None):
        phase='OUTER_FAIL_LEDGER' if path.endswith('/result.json') else 'CHILD_LOG' if '/logs/' in path or path.endswith('/FIXTURE_ONLY.log') else 'BUILD_SETUP'
        c=dict(path=path,phase=phase,cutoff=cutoff,writes=0,raw_closed=False,fd_closed=False);self.contexts.append(c);self.active=c
        try:
            receipt=self.m.FileSystem.write_new(self.fs,path,data,cutoff=cutoff);c['receipt']=receipt;return receipt
        except self.m.PersistenceRefusal as e:c['receipt']=e.receipt;raise
    def summary(self):return [{k:v for k,v in c.items() if k!='raw'} for c in self.contexts]

def persistence_matrix(m,base):
    evidence=[]
    for name in PERSISTENCE_CASES:
        r=clone_recipe(m,base);r.started=100;clock=[100.0];proc_events=[];alive=[True];record=None;failure=None;ledger=None;late_receipt=[False]
        writer=FakePersistence(m,r.fs,clock,name);r.fs.write_new=writer.write_new
        class Pipe:
            closed=False
            def fileno(self):return 99
            def close(self):
                assert clock[0]<220,'expired process close';proc_events.append('pipe_close');self.closed=True
                if name=='command-expired-before-log' and self is proc.stderr:clock[0]=221
        class Process:
            pid=424242;returncode=None
            def __init__(self):self.stdin=Pipe();self.stdout=Pipe();self.stderr=Pipe()
            def wait(self,*args,**kwargs):raise AssertionError('Popen.wait forbidden')
            def poll(self):raise AssertionError('Popen.poll forbidden')
        proc=Process()
        class Selector:
            mapped=True
            def register(self,*args):pass
            def get_map(self):return {1:1} if self.mapped else {}
            def select(self,timeout):return [(SimpleNamespace(fileobj=proc.stdout),1)]
            def unregister(self,*args):self.mapped=False
            def close(self):assert clock[0]<220;proc_events.append('selector_close')
        def kill(pid,sig):
            assert pid==424242 and clock[0]<220
            if sig==signal.SIGKILL:alive[0]=False
            else:assert sig==0;raise ProcessLookupError('FIXTURE_ONLY absent group')
        def observer(pid,deadline):assert pid==424242 and clock[0]<deadline and proc.returncode is None;return 0
        canonical=m.canonical
        def encode(value):
            data=canonical(value)
            if name=='receipt-preparation-late' and type(value) is dict and value.get('kind')=='BLACKWOOD_COMMAND_SUPERVISOR' and not late_receipt[0]:late_receipt[0]=True;clock[0]=221
            return data
        full=name in ('full-child-expired-outer-ledger','full-whole-expired-no-ledger','outer-ledger-write-late')
        with ExitStack() as patches:
            for obj,key,value in ((m.subprocess,'Popen',lambda *a,**k:proc),(m.selectors,'DefaultSelector',Selector),(m.os,'set_blocking',lambda *a:None),(m.os,'read',lambda *a:b''),(m.os,'waitpid',lambda pid,flags:(pid,0) if pid==424242 and flags==m.os.WNOHANG else (_ for _ in ()).throw(AssertionError('original waitpid only'))),(m.os,'killpg',kill),(m,'make_nonreaping_observer',lambda:observer),(m.signal,'getsignal',lambda sig:signal.SIG_DFL),(m.time,'monotonic',lambda:clock[0]),(m.os,'open',writer.open),(m.os,'fchmod',writer.chmod),(m.os,'fdopen',writer.fdopen),(m.os,'fsync',writer.fsync),(m.os,'close',writer.close),(m,'canonical',encode)):
                patches.enter_context(patch.object(obj,key,value))
            try:
                if name=='helper-already-expired':
                    clock[0]=221;writer.write_new(r.repo('FIXTURE_ONLY.log'),b'FIXTURE_ONLY',cutoff=220)
                elif full:
                    r.effects.run=lambda recipe,argv,env,log:m.Effects().run(recipe,argv,env,log)
                    r.execute_candidate('fixture',r.repo('notes/decisions/FIXTURE_ONLY.json'),r.fixture_pin)
                else:record=m.Effects().run(r,['FIXTURE_ONLY never launched'],{},r.repo('FIXTURE_ONLY.log'))
            except m.ProcessRefusal as e:record=e.record;failure=json.loads(record['failure']);ledger=getattr(e,'outer_ledger',None)
            except m.PersistenceRefusal as e:failure=e.receipt
            finally:
                if PREPARATION_EXPIRED[0]:raise PreparationDeadline('deadline cannot become persistence refusal')
            if name in ('short-write-success','retention-inclusive-success'):
                assert record['failure'] is None and failure is None;m.inspect_command_log(r.fs.read(r.repo('FIXTURE_ONLY.log')),True)
                assert all(c['receipt']['raw_released'] and c['receipt']['fd_released'] for c in writer.contexts)
                if name=='short-write-success':assert writer.contexts[0]['writes']==2
                if name=='retention-inclusive-success':assert record['elapsed_ms']>=70 and record['elapsed_ms']==int((clock[0]-100)*1000)
            else:assert failure is not None,('accepted persistence fault',name)
        child=[c for c in writer.contexts if c['phase']=='CHILD_LOG'];outer=[c for c in writer.contexts if c['phase']=='OUTER_FAIL_LEDGER']
        if name in ('command-expired-before-log','receipt-preparation-late'):
            assert not child and not writer.events and failure['retention']['status']=='SKIPPED_COMMAND_CUTOFF'
        if name=='helper-already-expired':assert not writer.events and not r.fs.exists(r.repo('FIXTURE_ONLY.log'))
        for c in child:
            receipt=c['receipt'];assert c['cutoff']==220
            if receipt['late'] and record is not None:
                assert record['failure'] is not None and record['elapsed_ms']>=120000
                assert not receipt['opened'] or any(x['status']=='SKIPPED_EXPIRED_UNRESOLVED' for x in receipt['releases']) or receipt['fd_released']
        if name=='write-partial-late':assert child[0]['receipt']['written_bytes']==7 and child[0]['writes']==1
        if name in ('write-late','write-partial-late','full-child-expired-outer-ledger','full-whole-expired-no-ledger','outer-ledger-write-late'):
            assert not any(e['phase']=='CHILD_LOG' and e['stage'] in ('flush','fsync','raw_close','fd_close') for e in writer.events)
        if name=='flush-late':assert not any(e['stage'] in ('fsync','raw_close','fd_close') for e in writer.events)
        if name=='fsync-late':assert not any(e['stage'] in ('raw_close','fd_close') for e in writer.events)
        if name=='raw-close-late':assert not any(e['stage']=='fd_close' for e in writer.events)
        if name=='raw-close-error':assert child[0]['receipt']['fd_released'] and not child[0]['receipt']['raw_released']
        if name=='fd-close-error':assert child[0]['receipt']['raw_released'] and not child[0]['receipt']['fd_released']
        if full:
            a,p=r.paths('fixture');assert r.fs.exists(a+'/failure.json') and ledger['phase']=='OUTER_FAIL_LEDGER' and ledger['cutoff_ms']==3700000
            if name=='full-child-expired-outer-ledger':assert ledger['status']=='WRITTEN' and len(outer)==1 and outer[0]['cutoff']==3700 and json.loads(r.fs.read(a+'/result.json'))['status']=='FAIL'
            elif name=='full-whole-expired-no-ledger':assert ledger['status']=='SKIPPED' and ledger['reason']=='WHOLE_CUTOFF' and not outer and not r.fs.exists(a+'/result.json')
            else:assert ledger['status']=='REFUSED' and outer[0]['receipt']['late'] and not any(e['phase']=='OUTER_FAIL_LEDGER' and e['stage'] in ('flush','fsync','raw_close','fd_close') for e in writer.events)
        evidence.append(dict(name=name,status='PASS' if failure is None else 'EXPECTED_REFUSAL',record=record,failure=failure,outer_ledger=ledger,events=writer.events,persistence=writer.summary(),process_release_events=proc_events,fixture_only=True))
    return evidence

RECEIPT_RACE_CASES=('default-late-create-wrong','default-late-replace-wrong','default-late-delete-observed','requested-late-create-wrong','requested-late-replace-wrong','requested-late-delete-after-publish','requested-publication-replace-wrong','requested-publication-delete','default-late-create-symlink','default-late-create-hardlink','default-late-create-mode','default-late-create-correct','requested-late-delete-observed','default-late-create-during-recheck')

def receipt_race_matrix(m,positive):
    evidence=[]
    for name in RECEIPT_RACE_CASES:
        r=clone_recipe(m,positive);pinpath=r.repo('notes/decisions/FIXTURE_ONLY.json');a,p=r.paths('fixture');target=p+'/verification/receipt.json'
        expected=canonical(r.verify_candidate('fixture',pinpath,r.fixture_pin))
        existing=('replace' in name and 'publication-' not in name) or 'delete-observed' in name
        if existing:r.fs.put(target,expected)
        observe=r.observe;read=r.fs.read;write=r.fs.write_new;recheck=r.gate.recheck;checks=[0];calls=[0];in_final=[False];published=[False];used=[False];writes=[]
        def mutate():
            if 'delete' in name:r.fs.remove(target)
            elif 'symlink' in name:r.fs.put(target,b'../FIXTURE_ONLY',kind='link',mode=511)
            elif 'hardlink' in name:r.fs.put(target,expected,nlink=2)
            elif 'mode' in name:r.fs.put(target,expected,mode=493)
            else:r.fs.put(target,expected if name.endswith('-correct') else b'{"FIXTURE_ONLY":"wrong receipt"}')
            used[0]=True
        def late_read(path,*args,**kwargs):
            data=read(path,*args,**kwargs)
            if not used[0] and in_final[0] and path==r.HERE+'/config.json' and 'publication-' not in name and 'during-recheck' not in name:
                if name!='requested-late-delete-after-publish' or published[0]:mutate()
            return data
        def late_observe(*args,**kwargs):
            calls[0]+=1;in_final[0]=calls[0]>=2
            try:return observe(*args,**kwargs)
            finally:in_final[0]=False
        def late_write(path,data):
            writes.append(path);write(path,data)
            if path==target:
                published[0]=True
                if 'publication-' in name:mutate()
        def late_recheck():
            recheck();checks[0]+=1
            if name.endswith('during-recheck') and checks[0]==2:mutate()
        r.observe=late_observe;r.fs.read=late_read;r.fs.write_new=late_write;r.gate.recheck=late_recheck
        error=None
        try:r.verify_candidate('fixture',pinpath,r.fixture_pin,target if name.startswith('requested-') else None)
        except (ValueError,OSError,KeyError,TypeError) as e:error=str(e)[:512]
        finally:
            if PREPARATION_EXPIRED[0]:raise PreparationDeadline('deadline cannot become receipt refusal')
        assert used[0],('late receipt injection not reached',name,calls)
        assert (error is None)==name.endswith('-correct'),('receipt race outcome',name,error)
        if name.startswith('default-'):assert writes==[],'default verifier wrote during receipt race'
        if name=='requested-late-delete-after-publish':assert published[0] and not r.fs.exists(target)
        evidence.append(dict(name=name,status='PASS' if error is None else 'EXPECTED_REFUSAL',error=error,observe_calls=calls[0],publication_performed=published[0],verifier_writes=writes,receipt_present=r.fs.exists(target),fixture_only=True))
    return evidence

TERMINAL_CASES={
 'terminal-eperm-success':('terminal-zero',),
 'terminal-eperm-post-eperm':('post-eperm',),
 'terminal-eperm-post-present':('post-present',),
 'terminal-eperm-no-event-running':('fresh-none','initial-running-then-fresh-none'),
 'terminal-eperm-nonzero':('fresh-nonzero','fresh-signaled','reap-nonzero'),
 'terminal-eperm-anchor-loss':('fresh-echild','already-reaped'),
 'terminal-eperm-pid-mismatch':('pid-mismatch',),
 'terminal-eperm-cutoff-before-reap':('before-reap',),
 'terminal-eperm-late-reap':('late-reap',),
 'terminal-eperm-cutoff-before-closure':('before-closure','late-closure'),
 'terminal-eperm-primary':('primary',),
 'terminal-eperm-persistence-close':('log-write','stdout-close'),
 'terminal-schema-missing':('permission_observation','phase','errno','pid','terminal_exit_code','mutating_signal_attempted','message','resolution'),
 'terminal-schema-unknown':('extra',),
 'terminal-schema-null-normal':('nonnull-normal','null-deferred'),
 'terminal-schema-phase':('wrong-phase',),
 'terminal-schema-errno':('wrong-errno',),
 'terminal-schema-bool-int':('errno','pid','terminal_exit_code'),
 'terminal-schema-pid':('wrong-pid',),
 'terminal-schema-exit':('wrong-terminal-code',),
 'terminal-schema-mutation':('wrong-mutation-flag',),
 'terminal-schema-resolution':('UNRESOLVED','wrong-resolution'),
 'terminal-schema-message':('wrong-type','too-long'),
 'terminal-schema-type':('not-object',),
}
TERMINAL_SUCCESS=[]  # Actual new supervisor output, reused only as schema DATA.

def terminal_behavior(m,base,variant):
    r=clone_recipe(m,base);r.started=100.0;clock=[100.0];events=[];signals=[];waits=[];observations=[];after_permission=[0];after_reap=[0]
    class Pipe:
        closed=False
        def __init__(self,name):self.name=name
        def fileno(self):return 99
        def close(self):
            events.append(self.name+'-close')
            if variant=='stdout-close' and self.name=='stdout':raise OSError('FIXTURE_ONLY close persistence fault')
            self.closed=True
    class Process:
        def __init__(self):self.current_pid=424242;self.reaped=False;self.stdin=Pipe('stdin');self.stdout=Pipe('stdout');self.stderr=Pipe('stderr')
        @property
        def pid(self):return self.current_pid
        @property
        def returncode(self):events.append('cached-returncode');return getattr(self,'consumed_code',0) if self.reaped or variant=='already-reaped' else None
        def poll(self):raise AssertionError('no poll or premature reap')
        @returncode.setter
        def returncode(self,value):self.consumed_code=value
        def wait(self,*args,**kwargs):raise AssertionError('Popen.wait forbidden')
    proc=Process()
    class Selector:
        def __init__(self):self.mapped=True
        def register(self,*args):pass
        def get_map(self):return {1:1} if self.mapped else {}
        def select(self,timeout):assert 0<timeout<=.05;return [(SimpleNamespace(fileobj=proc.stdout),1)]
        def unregister(self,*args):self.mapped=False
        def close(self):events.append('selector-close')
    def observe(pid,deadline):
        assert pid==424242 and not proc.reaped and clock[0]<deadline
        observations.append(dict(pid=pid,deadline=deadline))
        initial_calls=2 if variant=='initial-running-then-fresh-none' else 1
        if 'cached-returncode' not in events:
            return None if initial_calls==2 and len(observations)==1 else 0
        events.append('fresh-native-observation')
        if variant=='fresh-echild':raise ChildProcessError('FIXTURE_ONLY ECHILD ownership loss')
        if variant=='pid-mismatch':proc.current_pid=424243
        return None if variant in ('fresh-none','initial-running-then-fresh-none') else (1 if variant=='fresh-nonzero' else (-9 if variant=='fresh-signaled' else 0))
    def kill(pid,sig):
        assert pid==424242;signals.append(sig)
        if sig==signal.SIGKILL:
            assert not proc.reaped and proc.current_pid==pid and events[-1]=='fresh-native-observation'
            events.append('one-anchored-sigkill')
            raise PermissionError(1,'FIXTURE_ONLY observed terminal permission '+('x'*300))
        assert sig==0 and proc.reaped;events.append('first-post-reap-observation')
        if variant=='post-eperm':raise PermissionError(1,'FIXTURE_ONLY first post-reap EPERM')
        if variant=='post-present':return None
        if variant=='late-closure':clock[0]=221.0
        raise ProcessLookupError(3,'FIXTURE_ONLY first post-reap ESRCH')
    def now():
        if variant=='before-reap' and signal.SIGKILL in signals:
            after_permission[0]+=1;clock[0]=219.0 if after_permission[0]==1 else 220.0
        if variant=='before-closure' and proc.reaped:
            after_reap[0]+=1;clock[0]=219.0 if after_reap[0]==1 else 220.0
        return clock[0]
    def read(*args):
        if variant=='primary':raise OSError('FIXTURE_ONLY unrelated primary read fault')
        return b''
    def sleep(seconds):assert 0<=seconds<=.01;clock[0]+=seconds
    def consuming_waitpid(pid,options):
        assert pid==424242 and options==m.os.WNOHANG and proc.current_pid==pid and not proc.reaped
        waits.append(220-clock[0]);events.append('wait-original');proc.reaped=True
        if variant=='late-reap':clock[0]=221.0
        return pid,256 if variant=='reap-nonzero' else 0
    log=r.repo('FIXTURE_ONLY-terminal.log')
    if variant=='log-write':r.fs.fail_write=lambda path:path==log
    with ExitStack() as patches:
        for obj,key,value in ((m.subprocess,'Popen',lambda *a,**kw:proc),(m.selectors,'DefaultSelector',Selector),(m.os,'set_blocking',lambda *a:None),(m.os,'read',read),(m,'make_nonreaping_observer',lambda:observe),(m.os,'waitpid',consuming_waitpid),(m.os,'killpg',kill),(m.time,'monotonic',now),(m.time,'sleep',sleep),(m.signal,'getsignal',lambda sig:signal.SIG_DFL)):
            patches.enter_context(patch.object(obj,key,value))
        try:record=m.Effects().run(r,['FIXTURE_ONLY no process'],{},log)
        except m.ProcessRefusal as error:record=error.record
        success=variant=='terminal-zero'
        assert (record['failure'] is None)==success,(variant,record)
        raw=r.fs.read(log) if r.fs.exists(log) else None
        state=json.loads(record['failure']) if record['failure'] is not None else m.inspect_command_log(raw,True)
        if success:
            assert state['group']['signal_result']=='TERMINAL_EPERM_UNKNOWN' and state['group']['closure']=='ABSENT_AFTER_TERMINAL_EPERM'
            permission=state['group']['permission_observation'];assert permission['resolution']=='POST_REAP_ABSENT' and len(permission['message'])==240
            assert signals==[signal.SIGKILL,0] and len(waits)==1
            assert events.index('one-anchored-sigkill')<events.index('wait-original')<events.index('first-post-reap-observation')
            TERMINAL_SUCCESS.append(raw)
        else:
            try:m.inspect_command_log(raw,True) if raw is not None else m.inspect_command_log(m.SUPERVISOR_FRAME+m.canonical(state),True)
            except (ValueError,TypeError,KeyError):pass
            else:raise AssertionError('independent reader accepted failed terminal path '+variant)
        assert signals.count(signal.SIGKILL)<=1 and signals.count(0)<=1,'no repeated mutation or deferred closure retry'
        if variant in ('already-reaped','fresh-echild','pid-mismatch'):assert signal.SIGKILL not in signals
        if variant=='before-reap':assert not waits and state['group']['permission_observation']['resolution']=='UNRESOLVED'
        if variant in ('post-eperm','post-present'):assert state['group']['permission_observation']['resolution']=='UNRESOLVED' and signals==[signal.SIGKILL,0]
        if variant=='primary':assert state['primary'] is not None and state['group']['permission_observation']['resolution']=='POST_REAP_ABSENT'
        if variant=='stdout-close':assert state['cleanup'] and state['group']['permission_observation']['resolution']=='POST_REAP_ABSENT'
        if variant=='log-write':assert 'retention' in state and state['group']['permission_observation']['resolution']=='POST_REAP_ABSENT'
    return dict(variant=variant,fixture_only=True,record=record,raw_log=raw.decode() if raw else None,signals=signals,waits=waits,events=events,native_observations=observations,actual_effects=0)

def terminal_policy_case(m,base,name):
    if name.startswith('terminal-eperm-'):return [terminal_behavior(m,base,v) for v in TERMINAL_CASES[name]]
    assert len(TERMINAL_SUCCESS)==1,'schema input is actual fresh deferred supervisor success'
    raw=TERMINAL_SUCCESS[0];output,encoded=raw.rsplit(m.SUPERVISOR_FRAME,1);original=json.loads(encoded);evidence=[]
    for variant in TERMINAL_CASES[name]:
        state=copy.deepcopy(original);g=state['group'];o=g['permission_observation']
        if name=='terminal-schema-missing':
            if variant=='permission_observation':del g[variant]
            else:del o[variant]
        elif name=='terminal-schema-unknown':o['extra']=1
        elif name=='terminal-schema-null-normal':
            if variant=='nonnull-normal':g['signal_result']='SENT_ANCHORED';g['closure']='ABSENT_AFTER_ANCHORED_CLEANUP'
            else:g['permission_observation']=None
        elif name=='terminal-schema-phase':o['phase']='POST_REAP_SIGNAL'
        elif name=='terminal-schema-errno':o['errno']=2
        elif name=='terminal-schema-bool-int':o[variant]=True if variant!='terminal_exit_code' else False
        elif name=='terminal-schema-pid':o['pid']+=1
        elif name=='terminal-schema-exit':o['terminal_exit_code']=1
        elif name=='terminal-schema-mutation':o['mutating_signal_attempted']=1
        elif name=='terminal-schema-resolution':o['resolution']=variant
        elif name=='terminal-schema-message':o['message']=1 if variant=='wrong-type' else 'x'*241
        elif name=='terminal-schema-type':g['permission_observation']=[]
        else:raise AssertionError('unknown terminal schema group')
        changed=output+m.SUPERVISOR_FRAME+m.canonical(state);error=None
        try:m.inspect_command_log(changed,True)
        except (ValueError,TypeError,KeyError) as e:error=str(e)
        assert error is not None,(name,variant)
        evidence.append(dict(variant=variant,fixture_only=True,reader_refusal=error,raw_log=changed.decode(),actual_effects=0))
    return evidence

CASE_NAMES=CASE_NAMES+('late-report-input','pack-duplicate','verify-late-history-change','verify-late-history-add','verify-late-history-remove','verify-late-marker','verify-receipt-late-marker','log-group-unclosed','log-anchor-lost','log-forged-fixture','log-child-digest','deadline-control','actual-copy-cache-method','supervisor-orchestration-popen-refusal','observer-matrix','supervisor-matrix','receipt-race-matrix','persistence-matrix',)+tuple(TERMINAL_CASES)

def run_case(m,base,positive,name,rows):
    if name in TERMINAL_CASES:
        rows.append(dict(name=name,status='PASS',fixture_only=True,subcases=terminal_policy_case(m,base,name)));return
    if name=='persistence-matrix':
        rows.append(dict(name=name,status='PASS',fixture_only=True,subcases=persistence_matrix(m,base)));return
    if name=='receipt-race-matrix':
        rows.append(dict(name=name,status='PASS',fixture_only=True,subcases=receipt_race_matrix(m,positive)));return
    if name=='observer-matrix':
        rows.append(dict(name=name,status='PASS',fixture_only=True,subcases=observer_matrix(m)));return
    if name=='supervisor-matrix':
        rows.append(dict(name=name,status='PASS',fixture_only=True,subcases=supervisor_matrix(m,base)));return
    r=clone_recipe(m,base);pinpath=r.repo('notes/decisions/FIXTURE_ONLY.json');a,p=r.paths('fixture');operation=lambda:r.execute_candidate('fixture',pinpath,r.fixture_pin);expected_refusal=True
    def edit_json(path,fn):
        doc=json.loads(r.fs.read(path));fn(doc);r.fs.nodes[path]['data']=canonical(doc)
    def reseal_result():
        result=json.loads(r.fs.read(a+'/result.json'));metadata=dict(result);metadata.pop('metadata_sha256');encoded=canonical(metadata);result['metadata_sha256']=sha(encoded)
        for root in (a+'/bundle',p):r.fs.nodes[root+'/build-metadata.json']['data']=encoded
        r.fs.nodes[a+'/result.json']['data']=canonical(result)
        freeze=json.loads(r.fs.read(a+'/freeze.json'));freeze['attempt']=m.inventory(r.fs,a,('freeze.json','failure.json'));freeze['publication']=m.inventory(r.fs,p,('verification/receipt.json',));r.fs.nodes[a+'/freeze.json']['data']=canonical(freeze)
    if name in ('positive-full-graph','read-only-verifier','exclusive-receipt','real-context-refuses-fixture','verify-entrypoint'):
        r=clone_recipe(m,positive);pinpath=r.repo('notes/decisions/FIXTURE_ONLY.json');a,p=r.paths('fixture')
        operation=lambda:r.verify_candidate('fixture',pinpath,r.fixture_pin);expected_refusal=False
        if name=='read-only-verifier':
            def readonly():
                before=r.fs.dump();r.verify_candidate('fixture',pinpath,r.fixture_pin);assert r.fs.dump()==before
            operation=readonly
        if name=='exclusive-receipt':
            def receipt():
                target=p+'/verification/receipt.json';r.verify_candidate('fixture',pinpath,r.fixture_pin,target);before=r.fs.dump();r.verify_candidate('fixture',pinpath,r.fixture_pin,target);assert before==r.fs.dump()
            operation=receipt
        if name=='real-context-refuses-fixture':r.fixture_only=False;expected_refusal=True
        if name=='verify-entrypoint':
            def verify_cli():
                with patch.object(m,'Recipe',lambda:r):assert sys.modules['verify'].verify_main(['--candidate-id','fixture','--pins',pinpath,'--pins-sha256',r.fixture_pin])==0
            operation=verify_cli
    elif name=='plan-entrypoint':
        expected_refusal=False
        def plan_cli():
            with patch.object(m,'Recipe',lambda:r):assert sys.modules['build'].build_main(['--plan-only','--candidate-id','pure'])==0
            assert not r.fs.exists(a) and not r.fs.exists(p) and not r.effects.calls
            doc=json.loads(r.fs.read(r.HERE+'/tests/preparation-pure/plan.json'));assert doc['pending']==['EXECUTION_PINS_NOT_SUPPLIED'] and doc['kind']=='BLACKWOOD_BUILD_PLAN'
        operation=plan_cli
    elif name=='build-entrypoint':
        expected_refusal=False
        def build_cli():
            with patch.object(m,'Recipe',lambda:r):assert sys.modules['build'].build_main(['--execute','--candidate-id','fixture','--pins',pinpath,'--pins-sha256',r.fixture_pin])==0
            assert len(r.effects.calls)==125 and r.verify_candidate('fixture',pinpath,r.fixture_pin)['fixture_only']
        operation=build_cli
    elif name.startswith('config-'):
        changes={'config-define':lambda d:d['common_cxx'].remove('-DOUTBREAK_BLACKWOOD_CLIENT'),'config-profile':lambda d:d.__setitem__('profile','DEV'),'config-unknown':lambda d:d.__setitem__('command',['FORGED']),'config-bool':lambda d:d.__setitem__('schema_version',True)}
        edit_json(r.HERE+'/config.json',changes[name])
    elif name=='unit-order':r.fs.nodes[r.repo('source/src/Makefile')]['data']=r.fs.read(r.repo('source/src/Makefile')).replace(b'crypto.o',b'TEMP.o').replace(b'audiomanager.o',b'crypto.o').replace(b'TEMP.o',b'audiomanager.o')
    elif name=='header-absent':r.fs.remove(r.repo('source/src/browser_map_profile.h'))
    elif name=='source-changed':r.fs.nodes[r.repo('source/src/main.cpp')]['data']+=b'\n// FIXTURE_ONLY changed source'
    elif name=='acceptance-ref':r.fs.nodes[r.repo(next(iter(m.ACCEPTANCE_PINS)))]['data']+=b'changed'
    elif name in ('source-manifest-missing','source-manifest-old-path'):
        data=r.fs.read(r.repo(m.SOURCE_MANIFEST));r.fs.remove(r.repo(m.SOURCE_MANIFEST))
        if name.endswith('old-path'):r.fs.put(r.repo('web/repro/source-manifest.json'),data)
        def missing_manifest():
            assert 'MAIN_SOURCE_MANIFEST_MISSING' in r.plan('pure')['pending'];r.execute_candidate('fixture',pinpath,r.fixture_pin)
        operation=missing_manifest
    elif name=='source-manifest-self':edit_json(r.repo(m.SOURCE_MANIFEST),lambda d:d['entries'].append(dict(path=m.SOURCE_MANIFEST,bytes=1,sha256='0'*64,mode=420)))
    elif name=='source-manifest-mode':edit_json(r.repo(m.SOURCE_MANIFEST),lambda d:d['entries'][0].__setitem__('mode',493))
    elif name.startswith('pins-'):
        changes={'pins-authority':lambda d:d.__setitem__('authority','WORKER'),'pins-release':lambda d:d.__setitem__('execution_release','NONE'),'pins-unknown':lambda d:d.__setitem__('argv',['FORGED']),'pins-observation':lambda d:d['observation']['inputs'].pop(r.repo('source/src/browser_map_profile.h')),'pins-source-acceptance':lambda d:d['source_acceptance']['files'][0].__setitem__('sha256','0'*64),'pins-decision':lambda d:d.__setitem__('decision','../bad.md')}
        if name=='pins-digest':r.fixture_pin='0'*64
        else:edit_json(pinpath,changes[name]);r.fixture_pin=sha(r.fs.read(pinpath))
    elif name.startswith('pack-'):
        manifest=r.repo('web/assets/blackwood-profile/manifest.json');root=r.repo('web/assets/blackwood-profile/pack-root')
        changes={'pack-duplicate':lambda d:d['entries'].__setitem__(1,d['entries'][0]),'pack-79':lambda d:d.__setitem__('entries',d['entries'][:79]),'pack-revision':lambda d:d.__setitem__('map_revision',2),'pack-map-size':lambda d:d['entries'][0].__setitem__('bytes',734),'pack-virtual':lambda d:d['entries'][0].__setitem__('virtual_path','/wrong'),'pack-notice':lambda d:d['entries'][0].__setitem__('notice','missing'),'pack-license':lambda d:d['entries'][0].__setitem__('license','FORGED'),'pack-source-path':lambda d:d['entries'][0].__setitem__('source_path','../bad'),'pack-traversal':lambda d:d['entries'][0].__setitem__('path','../bad')}
        first=json.loads(r.fs.read(manifest))['entries'][0]['path']
        if name in changes:edit_json(manifest,changes[name])
        elif name=='pack-local-rehash':
            r.fs.nodes[root+'/'+first]['data']+=b'changed';edit_json(manifest,lambda d:d['entries'][0].update(bytes=len(r.fs.read(root+'/'+first)),sha256=sha(r.fs.read(root+'/'+first)),source_sha256=sha(r.fs.read(root+'/'+first))))
        elif name=='pack-extra':r.fs.put(root+'/extra.bin',b'FIXTURE_ONLY')
        elif name=='pack-missing':r.fs.remove(root+'/'+first)
        elif name=='pack-hardlink':r.fs.nodes[root+'/'+first]['nlink']=2
        elif name=='pack-symlink':r.fs.nodes[root+'/'+first].update(kind='link',data=b'../target')
        else:raise AssertionError(name)
    elif name=='cfg-order':r.fs.nodes[r.repo('web/assets/blackwood-profile/pack-root/packages/maps/blackwood_greybox_v1.cfg')]['data']+=b'fog 1\n'
    elif name=='cfg-allowlist':
        node=r.fs.nodes[r.repo('web/assets/blackwood-profile/pack-root/config/browser.cfg')];node['data']=node['data'].replace(b'scriptcontext MAPCFG texture',b'scriptcontext MAPCFG FORGED',1);operation=lambda:r.cfg_closure(m.FIXED_CONFIG)
    elif name=='notice-changed':r.fs.nodes[r.repo('web/build/notices/libpng.txt')]['data']+=b'changed'
    elif name=='notice-extra':r.fs.put(r.repo('web/build/notices/extra'),b'FIXTURE_ONLY')
    elif name in ('json-duplicate','json-nan','json-float','json-bool-int','id-traversal'):
        operation={'json-duplicate':lambda:m.parse_json(b'{"x":1,"x":2}'),'json-nan':lambda:m.parse_json(b'{"x":NaN}'),'json-float':lambda:m.parse_json(b'{"x":1.5}'),'json-bool-int':lambda:m.integer(True),'id-traversal':lambda:m.identifier('../bad')}[name]
    elif name=='alias-text':r.fs.nodes[next(iter(m.ALIAS_TEXT))]['data']=b'../escape'
    elif name=='alias-extra':edit_json(r.repo(next(iter(m.ALIAS_PINS))),lambda d:d['aliases'].append(dict(path='/FORGED',link_text='x',resolved_path='/x',resolved_sha256='0'*64)))
    elif name in ('native-role-consumed','browser-role-consumed','role-rearm','late-role-hardlink'):
        native='/usr/bin/clang++';r.fs.put(native,b'FIXTURE_ONLY native launcher',mode=493,nlink=1 if name=='late-role-hardlink' else 2);pin=sha(r.fs.read(native)) if name=='late-role-hardlink' else sha(r.fs.nodes[native]['data']);r.gate.arm_launcher(native,pin)
        if name=='late-role-hardlink':r.gate.dependency_record(native);r.fs.nodes[native]['nlink']=2;operation=r.gate.recheck
        elif name=='role-rearm':
            try:r.gate.dependency_record(native)
            except ValueError:pass
            assert native in r.gate.dependency_files;operation=lambda:r.gate.arm_launcher(native,pin)
        elif name=='browser-role-consumed':
            dep=a+'/deps/FIXTURE_ONLY.d';r.fs.put(dep,('x.o: '+native+'\n').encode());operation=lambda:r.dependencies(dep,a,dict(inputs={native:pin}))
        else:operation=lambda:r.gate.dependency_record(native)
    elif name in ('late-report-input','pre-post-mismatch','system-header-omitted','consumer-header-omitted','undeclared-header','stale-object','late-object','late-input','command-argv','command-env','command-exit','command-reap','command-log','cache-copy','pre-command','compile-command','link-command','syntax-command','wasm-command','report-failure','report-flush'):
        r.effects.mutation=name
    elif name=='partial-reservation':r.fs.fail_mkdir=lambda target:target==p
    elif name in ('occupied-attempt','occupied-publication'):
        r.fs.put(a if name.endswith('attempt') else p,kind='directory',mode=493)
    elif name in ('publication-write','result-write','freeze-write'):
        r.fs.fail_write=lambda target:target.startswith(p+'/') if name=='publication-write' else target==a+('/result.json' if name=='result-write' else '/freeze.json')
    elif name=='marker-remove':r.fs.fail_remove=True
    elif name=='deadline-control':
        expected_refusal=False
        def deadline_control():
            caught=False;PREPARATION_EXPIRED[0]=True
            try:run_case(m,base,positive,'json-bool-int',[])
            except PreparationDeadline:caught=True
            finally:PREPARATION_EXPIRED[0]=False
            assert caught,'preparation expiry must not become an expected negative'
        operation=deadline_control
    elif name=='actual-copy-cache-method':
        expected_refusal=False
        def cache_method():
            r.started=time.monotonic();source=r.repo('web/build/.cache');target=r.repo('FIXTURE_ONLY_cache_copy');m.Effects().copy_cache(r,source,target)
            assert m.inventory(r.fs,source)==m.inventory(r.fs,target)
        operation=cache_method
    elif name=='supervisor-orchestration-popen-refusal':
        def refused_launch(*args,**kwargs):raise OSError('FIXTURE_ONLY no real Popen')
        r.effects.run=lambda recipe,argv,env,log:m.Effects().run(recipe,argv,env,log)
        def supervisor_refusal():
            with patch.object(m.subprocess,'Popen',refused_launch),patch.object(m.signal,'getsignal',lambda sig:signal.SIG_DFL),patch.object(m,'make_nonreaping_observer',lambda:lambda pid,deadline:0):r.execute_candidate('fixture',pinpath,r.fixture_pin)
        operation=supervisor_refusal
    elif name.startswith('verify-late-') or name=='verify-receipt-late-marker':
        r=clone_recipe(m,positive);pinpath=r.repo('notes/decisions/FIXTURE_ONLY.json');a,p=r.paths('fixture');used=[False];original=r.fs.read;write=r.fs.write_new
        def late_read(target,*args,**kwargs):
            data=original(target,*args,**kwargs)
            if not used[0] and target==a+'/bundle/index.data':
                used[0]=True
                if name=='verify-late-history-change':r.fs.nodes[r.repo('web/FIXTURE_ONLY_history.bin')]['data']+=b'late'
                elif name=='verify-late-history-add':r.fs.put(r.repo('web/FIXTURE_ONLY_added_history'),b'late')
                elif name=='verify-late-history-remove':r.fs.remove(r.repo('web/FIXTURE_ONLY_history.bin'))
                elif name=='verify-late-marker':r.fs.put(a+'/failure.json',b'FIXTURE_ONLY late refusal')
            return data
        def late_write(target,data):
            write(target,data)
            if target==p+'/verification/receipt.json':r.fs.put(a+'/failure.json',b'FIXTURE_ONLY refusal during receipt publication')
        if name=='verify-receipt-late-marker':r.fs.write_new=late_write
        else:r.fs.read=late_read
        operation=lambda:r.verify_candidate('fixture',pinpath,r.fixture_pin,p+'/verification/receipt.json' if name=='verify-receipt-late-marker' else None)
    else:
        r=clone_recipe(m,positive);pinpath=r.repo('notes/decisions/FIXTURE_ONLY.json');a,p=r.paths('fixture');operation=lambda:r.verify_candidate('fixture',pinpath,r.fixture_pin)
        result_path=a+'/result.json';result=json.loads(r.fs.read(result_path));reseal=False
        if name in ('log-group-unclosed','log-anchor-lost','log-forged-fixture','log-child-digest'):
            log=a+'/logs/00-pre.log';output,encoded=r.fs.read(log).rsplit(m.SUPERVISOR_FRAME,1);state=json.loads(encoded)
            if name=='log-group-unclosed':state['group']['closed']=False
            elif name=='log-anchor-lost':state['group']['anchor_confirmed_before_signal']=False
            elif name=='log-forged-fixture':state['fixture_only']=False
            elif name=='log-child-digest':state['child_log_sha256']='0'*64
            r.fs.nodes[log]['data']=output+m.SUPERVISOR_FRAME+canonical(state);command=result['compiles'][0]['pre_scan'];command['log_bytes']=len(r.fs.read(log));command['log_sha256']=sha(r.fs.read(log));reseal=True
        elif name=='command-order':result['compiles'].reverse();reseal=True
        elif name=='result-unknown':result['FORGED']=True;reseal=True
        elif name=='result-claim':result['claims']['runtime']=True;reseal=True
        elif name=='result-fixture':result['fixture_only']=False;reseal=True
        elif name=='metadata-byte':r.fs.nodes[p+'/build-metadata.json']['data']+=b'changed'
        elif name=='bundle-ID':result['bundle_id']='0'*64;reseal=True
        elif name.startswith('slice-'):
            js=a+'/bundle/index.js';data=a+'/bundle/index.data'
            if name=='slice-79':r.fs.nodes[js]['data']=r.fs.read(js).replace(b'{filename:',b'{REMOVED_filename:',1)
            elif name=='slice-gap':r.fs.nodes[js]['data']=r.fs.read(js).replace(b'start:0',b'start:1',1)
            elif name=='slice-overlap':r.fs.nodes[js]['data']=r.fs.read(js).replace(b'start:1318',b'start:0',1)
            elif name=='slice-hash':r.fs.nodes[data]['data']=b'X'+r.fs.read(data)[1:]
            elif name=='slice-suffix':r.fs.nodes[data]['data']+=b'X'
            for n in m.ARTIFACTS:r.fs.nodes[p+'/'+n]['data']=r.fs.read(a+'/bundle/'+n);result['outputs'][n]=sha(r.fs.read(a+'/bundle/'+n))
            reseal=True
        elif name=='bundle-extra':r.fs.put(p+'/extra.bin',b'FIXTURE_ONLY');reseal=True
        elif name=='bundle-extra-directory':r.fs.put(p+'/extra-empty',kind='directory',mode=493);reseal=True
        elif name=='publication-missing':r.fs.remove(p+'/index.js')
        elif name=='phase-new-file':r.fs.put(r.repo('web/extra-protected'),b'FIXTURE_ONLY')
        elif name=='phase-new-directory':r.fs.put(r.repo('web/extra-directory'),kind='directory',mode=493)
        elif name=='phase-removed':r.fs.remove(r.repo('web/assets/network-profile/pack-root/LICENSE.txt'))
        elif name=='phase-link-change':r.fs.nodes[r.repo('web/FIXTURE_ONLY_history.link')]['data']=b'changed'
        elif name=='receipt-wrong-path':operation=lambda:r.verify_candidate('fixture',pinpath,r.fixture_pin,p+'/verification/WRONG.json')
        elif name=='receipt-existing-wrong':r.fs.put(p+'/verification/receipt.json',b'{}')
        elif name=='marker-dominates':r.fs.put(a+'/failure.json',b'{"status":"REFUSE"}')
        elif name=='freeze-member':edit_json(a+'/freeze.json',lambda d:d['attempt']['files'].pop('plan.json'))
        elif name=='freeze-unknown':edit_json(a+'/freeze.json',lambda d:d.__setitem__('FORGED',True))
        elif name=='plan-byte':edit_json(a+'/plan.json',lambda d:d.__setitem__('status','EXECUTED'))
        elif name=='log-byte':r.fs.nodes[a+'/logs/00-compile.log']['data']+=b'changed'
        else:raise AssertionError('unimplemented fixture '+name)
        if reseal:
            r.fs.nodes[result_path]['data']=canonical(result);reseal_result()
    before=r.fs.dump();error=None
    try:operation()
    except (ValueError,OSError,KeyError,TypeError,m.ProcessRefusal) as e:error=str(e)[:512]
    finally:
        if PREPARATION_EXPIRED[0]:raise PreparationDeadline('deadline cannot become an expected refusal')
    if expected_refusal:assert error is not None,'accepted negative '+name
    else:assert error is None,(name,error)
    if expected_refusal and a not in before and r.fs.exists(a):assert r.fs.exists(a+'/failure.json'),'new failed attempt lost refusal marker'
    rows.append(dict(name=name,status='EXPECTED_REFUSAL' if expected_refusal else 'PASS',fixture_only=True,error=error,simulated_commands=len(r.effects.calls),before_sha256=sha(canonical(before)),after_sha256=sha(canonical(r.fs.dump()))))

if __name__=='__main__':raise SystemExit(main())
