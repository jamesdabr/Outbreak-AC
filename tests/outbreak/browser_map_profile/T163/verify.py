"""T163 sole fixed private-helper proof driver; imports are effect-free."""
from pathlib import Path
import ast
import difflib
import hashlib
import io
import json
import os
import re
import selectors
import shlex
import shutil
import signal
import stat
import struct
import subprocess
import sys
import time
import socket
from contextlib import ExitStack
from types import SimpleNamespace
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ATTEMPT=HERE/'attempt-1'
FIXTURES=HERE/'supervisor-fixtures-1'
SDK=Path('/private/tmp/outbreak-web-sdk')
CLEANUP_ACTIVE=False
GUARD_EXPIRED=False
TOOLS={
 '/usr/bin/clang++':'179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818',
 str(SDK/'upstream/bin/clang++'):'9a96f4220eefe21e72a4a9a20a88f4d6c26cad1b047cb02b5b22a96bef49c423',
 str(SDK/'upstream/bin/wasm-ld'):'b851d4f8a53ca2839651b62821a8981fcdb22a51c8c7fc04733ed2f6d050ad5c',
 str(SDK/'node/24.19.0_64bit/bin/node'):'27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1',
 '/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11':'4e28e811a89aeac6eed668ae641c7f85f5831e42e8dc6cd9a85a3bcc032ec46a'}
BASELINES={'main.cpp':'5f51c53b5a6f2be1180252c7aee972ab754bf0abc91d8a3d0f276153a38834f1','client.cpp':'2bbbf548e374ce4adb819400d435c4a6e5ae93bf26b4aaffcbe739028f72ec10','clients2c.cpp':'83a57afb6796c8f76fbe496175f0527e51c431a9d06666d29ee10985ba812686'}
GUARD_DIAGNOSTIC='OUTBREAK_BLACKWOOD_CLIENT requires __EMSCRIPTEN__ and OUTBREAK_NETWORK_CLIENT without STANDALONE'
EXPORTS=('request_address','response_address','request_capacity','response_capacity','run')
LAYOUT=dict(request_bytes=96,response_bytes=192,request=dict(received_name32=0,loaded_name32=32,received_revision_i32=64,loaded_revision_i32=68,loaded_bytes_i32=72,advertised_bytes_i32=76,mode_i32=80,load_result_i32=84,accepted_receipt_u8=88,incompatible_u8=89,null_bits_u8=90,reserved_zero5=91),response=dict(selected_name32=0,cgz_path48=32,cfg_path48=80,selected_revision_u32=128,receipt_name32=132,receipt_revision_u32=164,predicate_bits_u32=168,observation_bits_u32=172,reserved_zero16=176),predicate_bits=['name','loaded','startup','observed','pre_change','post_change','spawn'],observation_bits=['request_unchanged','guards_intact'])
SUPERVISION_PLAN=dict(operation_seconds=60,cleanup_reserve_seconds=5,whole_seconds=300,whole_guard_seconds=295,supervisor_fixture_bytes=4194304,work_deadline='min(start+60,whole)-5',cleanup='independent same-handle signal/wait/selector/each pipe; no new grace or launch after work deadline',receipts='memory first, independent retention, final deadline check, refusal for unresolved/error',expected_compile_refusal='only named invalid-profile probes may expect exit1; exact guard diagnostic separately mandatory',limitations='no hard-real-time arbitrary OS/kernel-stall/process-tree/RSS/performance proof')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dump(value):return (json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
def identity(path):
    s=path.lstat()
    if stat.S_ISLNK(s.st_mode):return dict(link=os.readlink(path),resolved=str(path.resolve()),target=identity(path.resolve()))
    if stat.S_ISREG(s.st_mode):return dict(bytes=s.st_size,sha256=sha(path),mode=stat.S_IMODE(s.st_mode),nlink=s.st_nlink)
    if stat.S_ISDIR(s.st_mode):return dict(directory=True,mode=stat.S_IMODE(s.st_mode))
    raise ValueError('special path')
def snapshot(paths):
    out={}
    for root in paths:
        for path in [root]+(sorted(root.rglob('*')) if root.is_dir() else []):out[str(path)]=identity(path)
    return out
def durable_new(path,data):
    if not path.is_absolute() or '..' in path.parts or not (path.is_relative_to(ATTEMPT) or path.is_relative_to(FIXTURES)):raise ValueError('owned output confinement')
    current=HERE
    for part in path.relative_to(HERE).parts[:-1]:
        current=current/part
        if current.is_symlink() or not current.is_dir():raise ValueError('owned ancestor alias')
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    try:
        os.fchmod(fd,0o644)
        with os.fdopen(fd,'wb',closefd=False) as f:f.write(data);f.flush();os.fsync(fd)
    finally:os.close(fd)
def sync_dir(path):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)

def terminal_pipeline(root,work,report,fixture=False):
    marker=root/'REFUSE';durable_new(marker,b'T163 REFUSE incomplete/failed helper proof\n');sync_dir(root)
    try:
        body=work(dict(attempt=root))
        report.write('T163 helper checks complete; terminal commit pending\n');report.flush()
        roots=[root] if fixture else [ROOT/'source/src'/n for n in (*BASELINES,'browser_map_profile.h')]+[HERE/n for n in ('verify.py','wrapper.cpp','wasm_runner.mjs','SCHEMA.md','README.md')]+[ATTEMPT,FIXTURES]
        inventory=snapshot(roots);inventory.pop(str(marker),None)
        body.update(status='PASS',fixture=fixture,inventory_role='HISTORICAL_RUNTIME_COMPLETION_BEFORE_RESULT_AND_REFUSE_REMOVAL',runtime_completion_inventory=inventory)
        encoded=dump(body)
        if len(encoded)>2097152:raise ValueError('terminal result cap')
        durable_new(root/'result.json',encoded);sync_dir(root)
        marker.unlink()  # Final required driver effect; no required reporting follows.
        return 0
    except BaseException as e:
        durable_new(root/'failure.json',dump(dict(status='REFUSE',fixture=fixture,error=exception_text(e),supervisor_receipt=getattr(e,'receipt',None))))
        return 1

def corpus():
    cases=[]
    def add(row,label):cases.append(dict(row=row,label=label))
    for name,rev,size in (('dev_outbreak_browser',2,561),('blackwood_greybox_v1',1,734)):
        base=[name,name,rev,rev,size,size,2,0,1,0,0]
        add(base[:],'matching-'+name)
        for field,values in ((0,('',name+'x','foreign','/'+name,name.upper())),(1,('',name+'x','foreign')),(2,(-2147483648,-1,0,1,2,3,2147483647)),(3,(-1,0,1,2,3,2147483647)),(4,(-2147483648,-1,0,1,560,561,562,733,734,735,2147483647)),(5,(-1,0,1,560,561,562,733,734,735,2147483647)),(6,(-2147483648,-1,0,1,2,3,2147483647)),(7,(-2147483648,-1,0,1,2,2147483647)),(8,(0,1)),(9,(0,1)),(10,(0,1,2,3))):
            for value in values:
                row=base[:];row[field]=value;add(row,'field-%d'%field)
        # Receipt does not depend on current render/load flags; it records genuine
        # accepted network history, and remains empty before that accepted receipt.
        for receipt in (0,1):
            row=base[:];row[8]=receipt;row[0]='foreign';row[1]='foreign';row[3]=0;row[4]=0;row[7]=-1;add(row,'receipt-versus-current-invalid-state')
        for loaded,advertised in ((1,1),(560,561),(561,734),(734,561),(734,734),(0,0),(-1,-1),(2147483647,2147483647)):
            row=base[:];row[4]=loaded;row[5]=advertised;add(row,'positive-equal-size-semantics')
        for bits in range(32):
            row=base[:];row[2]=0 if bits&1 else rev;row[4]=0 if bits&2 else size;row[6]=3 if bits&4 else 2;row[8]=0 if bits&8 else 1;row[9]=1 if bits&16 else 0;add(row,'combined-gate-state')
    raw=bytearray()
    for c in cases:
        row=c['row'];left=row[0].encode();right=row[1].encode()
        if len(left)>=32 or len(right)>=32:raise ValueError('fixture name bound')
        raw.extend(left+bytes(32-len(left))+right+bytes(32-len(right))+struct.pack('<6i3B5x',*row[2:]))
    if len(cases)>1024 or len(raw)!=96*len(cases) or len(cases)*192*4>1048576:raise ValueError('corpus caps')
    return bytes(raw),cases

def oracle(profile,cases):
    name,rev=('dev_outbreak_browser',2) if profile=='dev' else ('blackwood_greybox_v1',1)
    def field(text,n):
        b=text.encode();assert len(b)<n;return b+bytes(n-len(b))
    out=bytearray()
    for c in cases:
        received,loaded,rrev,lrev,size,advertised,mode,result,receipt,incompatible,nulls=c['row']
        if nulls&1:received=None
        if nulls&2:loaded=None
        named=received==name;valid_loaded=loaded==name and lrev==rev and size>0
        startup=result==0 and valid_loaded
        observed=named and rrev==rev and valid_loaded and mode==2
        pre=observed and advertised>0 and size==advertised
        post=pre and result>=0 and not incompatible
        spawn=bool(receipt) and valid_loaded and mode==2
        bits=sum(int(value)<<i for i,value in enumerate((named,valid_loaded,startup,observed,pre,post,spawn)))
        out.extend(field(name,32)+field('packages/maps/'+name+'.cgz',48)+field('packages/maps/'+name+'.cfg',48)+struct.pack('<I',rev)+field(name if receipt else '',32)+struct.pack('<III',rev if receipt else 0,bits,3)+bytes(16))
    assert len(out)==len(cases)*192
    return bytes(out)

def audit_sources():
    source={n:(ROOT/'source/src'/n).read_text() for n in BASELINES}
    expected_calls={'main.cpp':{'loaded_matches':1,'cgz_path':1,'cfg_path':1,'name':1,'startup_loaded':1},'client.cpp':{'receipt_name':1,'receipt_revision':1,'spawn_matches':2,'observed_matches':1},'clients2c.cpp':{'pre_change':1,'post_change':1}}
    for n,text in source.items():
        if 'dev_outbreak_browser' in text or 'blackwood_greybox_v1' in text:raise ValueError('stray map literal')
        if text.count('#include "browser_map_profile.h"')!=1:raise ValueError('header routing')
        for method,count in expected_calls[n].items():
            if text.count('ob_browser_map::'+method+'(')!=count:raise ValueError('callsite count '+n+' '+method)
    cpp=source['clients2c.cpp'];start=cpp.index('bool changemapserv(');end=cpp.index('    gamemode = mode;',start);block=cpp[start:end]
    tokens=('ob_browser_map::pre_change(','gamemode=mode;','int networkloaded=load_world(name);','ob_browser_map::post_change(','browsernet_map_observed(name,revision);')
    if [block.index(s) for s in tokens]!=sorted(block.index(s) for s in tokens):raise ValueError('real parser load/receipt order')
    if 'if(p.overread()) { browsernet_close(BNE_ENET); return; }' not in cpp or 'if(!browsernet_spawn_expected()) return;' not in cpp or 'browsernet_acknowledge_spawn(player1->lifesequence,player1->weaponsel->type)' not in cpp:raise ValueError('parser/spawn lifecycle lost')
    if source['client.cpp'].count('bnmap=true;')!=1 or 'bnmap=false;' not in source['client.cpp']:raise ValueError('real receipt lifecycle lost')
    if 'void browsernet_map_observed(const char *name,int revision)' not in source['client.cpp']:raise ValueError('actual callback missing')
    if 'putint(p, hdr.maprevision);' not in source['client.cpp']:raise ValueError('real SV_MAPIDENT lost')
    return dict(status='STATIC_CALLSITE_AUDIT',shared_calls=expected_calls,parser_order=list(tokens),actual_runtime_verified=False)


def exception_text(error):
    try:return (type(error).__name__+': '+str(error))[:512]
    except BaseException:return 'exception text unavailable'

def whole_alarm(*_):
    global GUARD_EXPIRED
    GUARD_EXPIRED=True
    if not CLEANUP_ACTIVE:raise TimeoutError('295s driver guard; enter owned cleanup')

class SupervisionRefusal(RuntimeError):
    def __init__(self,receipt):
        self.receipt=receipt
        super().__init__('owned-child supervision refused: '+str(receipt['primary'] or receipt['cleanup_errors'] or receipt['retention_errors']))

class Supervisor:
    def __init__(self,env,deadline):self.env=env;self.deadline=deadline;self.total=0;self.receipts=[]
    def run(self,label,argv,payload=b'',expected_profile_guard=False):
        global CLEANUP_ACTIVE
        start=time.monotonic();hard=min(start+60,self.deadline);work_end=hard-5
        # All receipt/state allocations precede launch. Popen itself is inside the
        # cleanup scope, and a returned handle is retained before any setup.
        p=None;pid=None;sel=None;sent=0;primary=None;cleanup=[];actions=[];retention=[]
        streams={'stdout':bytearray(),'stderr':bytearray()};observed=None;reaped=False
        previous_cleanup=CLEANUP_ACTIVE
        def fail(error):
            nonlocal primary
            if primary is None:primary=exception_text(error)
            else:cleanup.append(dict(action='additional_exception',error=exception_text(error)))
        def work_budget():
            left=work_end-time.monotonic()
            if left<=0 or GUARD_EXPIRED:raise TimeoutError('work deadline/whole guard')
            return left
        def attempt(name,call):
            row=dict(action=name,outcome='attempted');actions.append(row)
            try:
                value=call();row['outcome']='completed';return value
            except BaseException as e:
                row['outcome']='error';row['error']=exception_text(e);cleanup.append(dict(action=name,error=row['error']));return None
        try:
            try:
                work_budget()
                p=subprocess.Popen(argv,cwd=ROOT,env=self.env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
                pid=p.pid
                work_budget();sel=selectors.DefaultSelector()
                for name in ('stdout','stderr'):
                    work_budget();pipe=getattr(p,name);os.set_blocking(pipe.fileno(),False)
                    work_budget();sel.register(pipe,selectors.EVENT_READ,name)
                work_budget()
                if payload:
                    os.set_blocking(p.stdin.fileno(),False);work_budget();sel.register(p.stdin,selectors.EVENT_WRITE,'stdin')
                else:p.stdin.close()
                work_budget()
                while sel.get_map():
                    interval=min(.05,work_budget())
                    for k,_ in sel.select(interval):
                        work_budget()
                        if k.data=='stdin':
                            try:sent+=os.write(k.fd,payload[sent:sent+65536])
                            except BrokenPipeError:sel.unregister(k.fileobj);k.fileobj.close();continue
                            if sent==len(payload):sel.unregister(k.fileobj);k.fileobj.close()
                        else:
                            block=os.read(k.fd,65536)
                            if not block:sel.unregister(k.fileobj);k.fileobj.close();continue
                            if self.total+len(block)>8388608:raise ValueError('aggregate8MiB cap')
                            self.total+=len(block);streams[k.data].extend(block)
                observed=p.wait(timeout=work_budget());reaped=True
                work_budget()  # Exit0 observed after a work deadline is refusal.
                if observed!=(1 if expected_profile_guard else 0):raise RuntimeError('unexpected child exit '+str(observed))
            except BaseException as e:fail(e)
            finally:
                # The whole guard is deferred here; every cleanup is independent.
                CLEANUP_ACTIVE=True
                if p is not None:
                    def cached():return p.returncode
                    cached_code=attempt('cached_returncode',cached)
                    if cached_code is not None:observed=cached_code;reaped=True
                    if not reaped:
                        remaining=hard-time.monotonic()
                        if remaining>0:
                            def signal_owned():
                                if time.monotonic()>=hard:raise TimeoutError('no remaining signal budget')
                                os.killpg(pid,signal.SIGKILL)
                            if pid is not None:attempt('kill_owned_group',signal_owned)
                            else:cleanup.append(dict(action='kill_owned_group',error='owned PID unavailable'))
                        else:cleanup.append(dict(action='kill_owned_group',error='hard deadline exhausted; not signaled'))
                        remaining=hard-time.monotonic()
                        if remaining>0:
                            def reap():
                                nonlocal observed,reaped
                                bound=hard-time.monotonic()
                                if bound<=0:raise TimeoutError('no positive bounded wait budget')
                                observed=p.wait(timeout=bound);reaped=True
                            attempt('wait_owned_handle',reap)
                        else:cleanup.append(dict(action='wait_owned_handle',error='no positive bounded wait budget; unresolved'))
                if sel is not None:attempt('selector_close',sel.close)
                if p is not None:
                    for name in ('stdin','stdout','stderr'):
                        def close_pipe(name=name):
                            pipe=getattr(p,name)
                            if pipe is not None and not pipe.closed:pipe.close()
                        attempt(name+'_close',close_pipe)
            ended=time.monotonic()
            if ended>=hard:fail(TimeoutError('operation hard deadline including cleanup'))
            if GUARD_EXPIRED:fail(TimeoutError('whole guard expired'))
            if p is not None and not reaped and primary is None:fail(RuntimeError('owned handle unresolved'))
            receipt=dict(label=label,argv=argv,expected_profile_guard=expected_profile_guard,launched=p is not None,pid=pid,exit=observed,reaped=reaped if p is not None else None,ownership='reaped' if reaped else ('unresolved' if p is not None else 'no_returned_handle'),primary=primary,cleanup_errors=cleanup,cleanup_actions=actions,retention_errors=retention,elapsed_s=ended-start,operation_deadline=hard,work_deadline=work_end,whole_deadline=self.deadline,cleanup_finished_at=ended,stream_bytes={n:len(b) for n,b in streams.items()},stream_sha256={n:hashlib.sha256(b).hexdigest() for n,b in streams.items()},aggregate_output_bytes=self.total,receipt_role='bounded observed-state snapshot before fallible independent retention')
            self.receipts.append(receipt)  # Formed before any fallible log write.
            for name,raw in streams.items():
                try:(ATTEMPT/'logs'/(label+'.'+name)).write_bytes(raw)
                except BaseException as e:retention.append(dict(action=name+'_log',error=exception_text(e)))
            receipt['elapsed_s']=time.monotonic()-start
            if time.monotonic()>=hard or GUARD_EXPIRED:
                if receipt['primary'] is None:receipt['primary']='TimeoutError: deadline during log retention'
            try:(ATTEMPT/'processes.json').write_bytes(dump(self.receipts))
            except BaseException as e:retention.append(dict(action='process_receipts',error=exception_text(e)))
            # Receipt-file write can itself cross a deadline: never accept late0.
            if time.monotonic()>=hard or GUARD_EXPIRED:
                if receipt['primary'] is None:receipt['primary']='TimeoutError: deadline during receipt retention'
            if receipt['primary'] or cleanup or retention or (p is not None and not reaped):raise SupervisionRefusal(receipt)
            return bytes(streams['stdout']),bytes(streams['stderr'])
        finally:
            CLEANUP_ACTIVE=previous_cleanup

SUPERVISOR_CASES=('control','popen-refusal','selector-construction','nonblock-stdout','nonblock-stderr','nonblock-stdin','register-stdout','register-stderr','register-stdin','initial-stdin-close','select-error','read-error','write-error','output-cap','partial-read-error','kill-esrch','kill-error','wait-timeout','wait-error','selector-close','close-stdin','close-stdout','close-stderr','combined','no-budget','near-budget','setup-deadline','drain-deadline','wait-late-zero','wait-hard-late-zero','guard-work','guard-cleanup','stdout-log','stderr-log','receipt-write','all-retention','late-log','late-receipt','known-reaped-setup','nonzero-exit','kill-exhausts-budget','wait-cleanup-late-zero','guard-setup','cleanup-near-deadline')

def supervisor_regressions(v,root):
    """Actual Supervisor.run, fake owned handles only; every real effect denied."""
    rows=[]
    def deny(*args,**kwargs):raise AssertionError('real process/signal/wait/network forbidden in supervisor fixture')
    with ExitStack() as guards:
        for module,names in ((os,('fork','forkpty','posix_spawn','posix_spawnp','execv','execve','execvp','execvpe','system','kill','killpg','wait','waitpid')),(subprocess,('Popen','run','call','check_call','check_output')),(socket,('socket','create_connection'))):
            for name in names:
                if hasattr(module,name):guards.enter_context(patch.object(module,name,deny))
        for name in SUPERVISOR_CASES:
            case=root/('supervisor-'+name);case.mkdir();(case/'logs').mkdir()
            events=[];now=[100.0];waits=[];persist=[];reads=[b'abc',b''];holder={}
            payload=b'xyz' if name in ('nonblock-stdin','register-stdin','write-error','close-stdin') else b''
            force_setup=name in ('selector-construction','kill-esrch','kill-error','wait-timeout','wait-error','near-budget','guard-cleanup','known-reaped-setup','kill-exhausts-budget','wait-cleanup-late-zero')
            class Pipe:
                def __init__(self,label,fd):self.label=label;self.fd=fd;self.closed=False
                def fileno(self):return self.fd
                def close(self):
                    events.append('close:'+self.label)
                    if name=='initial-stdin-close' and self.label=='stdin':raise OSError('initial stdin-close injected')
                    if name=='close-'+self.label or name=='combined':raise OSError('secondary '+self.label+' close injected')
                    self.closed=True
            class Child:
                def __init__(self):
                    self.pid=424242;self.returncode=0 if name=='known-reaped-setup' else None
                    self.stdin=Pipe('stdin',10);self.stdout=Pipe('stdout',11);self.stderr=Pipe('stderr',12)
                def wait(self,timeout):
                    assert self is holder['child']
                    events.append('wait');waits.append(dict(timeout=timeout,at=now[0]))
                    if name in ('wait-timeout','combined'):raise subprocess.TimeoutExpired(['FAKE'],timeout)
                    if name=='wait-error':raise OSError('wait injected')
                    if name=='wait-late-zero':now[0]=155.01
                    if name in ('wait-hard-late-zero','wait-cleanup-late-zero'):now[0]=160.01
                    self.returncode=9 if name=='nonzero-exit' else 0
                    return self.returncode
            def popen(*args,**kwargs):
                events.append('popen')
                if name=='popen-refusal':raise OSError('Popen refused; no returned handle')
                p=Child();holder['child']=p;return p
            def nonblock(fd,blocking):
                label={10:'stdin',11:'stdout',12:'stderr'}[fd];events.append('nonblock:'+label)
                if name=='nonblock-'+label:raise OSError('set_blocking '+label+' injected')
            class Selector:
                def __init__(self):
                    events.append('selector')
                    if name=='guard-setup':v.whole_alarm()
                    if force_setup:raise OSError('selector construction injected')
                    self.items={}
                    if name=='setup-deadline':now[0]=160.01
                def register(self,pipe,mask,label):
                    events.append('register:'+label)
                    if name=='register-'+label:raise OSError('register '+label+' injected')
                    self.items[pipe.fd]=SimpleNamespace(fd=pipe.fd,fileobj=pipe,data=label)
                def unregister(self,pipe):del self.items[pipe.fd]
                def get_map(self):return self.items
                def select(self,timeout):
                    events.append('select');assert 0<timeout<=.05
                    if name in ('select-error','combined'):raise OSError('select injected')
                    if name=='cleanup-near-deadline':now[0]=159.9;raise TimeoutError('drain crossed work deadline')
                    if name in ('drain-deadline',):now[0]=155.01
                    if name=='guard-work':v.whole_alarm()
                    return [(key,0) for key in list(self.items.values())]
                def close(self):
                    events.append('selector-close')
                    if name in ('selector-close','combined'):raise OSError('selector close injected')
                    self.items.clear()
            def read(fd,size):
                events.append('read:'+str(fd));assert size<=65536
                if name=='read-error':raise OSError('read injected')
                if fd==12:return b''
                if name=='partial-read-error':
                    if len(reads)==2:return reads.pop(0)
                    raise OSError('read after partial injected')
                return reads.pop(0) if reads else b''
            def write(fd,data):
                events.append('write');assert fd==10
                if name=='write-error':raise OSError('write injected')
                return len(data)
            def kill(pid,sig):
                events.append('kill');assert pid==holder['child'].pid and sig==v.signal.SIGKILL
                if name=='kill-esrch':raise ProcessLookupError('ESRCH injected')
                if name in ('kill-error','combined'):raise OSError('signal injected')
                if name=='guard-cleanup':
                    assert v.CLEANUP_ACTIVE;v.whole_alarm()
                if name=='kill-exhausts-budget':now[0]=160.01
            original_write=Path.write_bytes
            def persist_write(path,data):
                persist.append(path.name)
                if name=='all-retention' or (name=='stdout-log' and path.suffix=='.stdout') or (name=='stderr-log' and path.suffix=='.stderr') or (name=='receipt-write' and path.name=='processes.json'):raise OSError('retention injected '+path.name)
                result=original_write(path,data)
                if name=='late-log' and path.suffix=='.stderr':now[0]=160.01
                if name=='late-receipt' and path.name=='processes.json':now[0]=160.01
                return result
            whole=104.0 if name=='no-budget' else (105.1 if name=='near-budget' else 400.0)
            supervisor=v.Supervisor({},whole)
            if name=='output-cap':supervisor.total=8388607
            def work(ctx):
                supervisor.run('fake',['FAKE_OWNED_CHILD_ONLY'],payload)
                pass  # No decoder/product side effects in private-helper fixtures.
                return dict(fixture=True,simulated_effects=True,actual_decoder_execution=False)
            with ExitStack() as patches:
                for module,attr,value in ((v,'ATTEMPT',case),(v,'CLEANUP_ACTIVE',False),(v,'GUARD_EXPIRED',False),(v.time,'monotonic',lambda:now[0]),(v.subprocess,'Popen',popen),(v.selectors,'DefaultSelector',Selector),(v.os,'set_blocking',nonblock),(v.os,'read',read),(v.os,'write',write),(v.os,'killpg',kill),(Path,'write_bytes',persist_write)):
                    patches.enter_context(patch.object(module,attr,value))
                status=v.terminal_pipeline(case,work,io.StringIO(),fixture=True)
                assert not v.CLEANUP_ACTIVE
            assert len(supervisor.receipts)==1
            receipt=supervisor.receipts[0];launched=name not in ('popen-refusal','no-budget')
            assert receipt['launched']==launched and receipt['pid']==(424242 if launched else None)
            assert events.count('popen')==(0 if name=='no-budget' else 1)
            assert events.count('kill')<=1 and events.count('wait')<=2
            for call in waits:assert 0<call['timeout']<=min(160.0,whole)-call['at']
            assert receipt['aggregate_output_bytes']<=8388608
            assert receipt['stream_bytes']['stdout']<=3
            if launched:
                for label in ('stdin','stdout','stderr'):assert 'close:'+label in events
                actions=[r['action'] for r in receipt['cleanup_actions']]
                assert actions[0]=='cached_returncode' and actions[-3:]==['stdin_close','stdout_close','stderr_close']
                assert actions.count('kill_owned_group')<=1 and actions.count('wait_owned_handle')<=1
                if 'selector_close' in actions:assert actions.index('selector_close')<actions.index('stdin_close')
                if 'kill_owned_group' in actions and 'wait_owned_handle' in actions:assert actions.index('kill_owned_group')<actions.index('wait_owned_handle')
            if name=='control':
                assert status==0 and receipt['reaped'] and not receipt['cleanup_errors'] and not receipt['retention_errors'] and not (case/'REFUSE').exists()
            else:
                assert status==1 and (case/'REFUSE').exists() and not (case/'result.json').exists()
                failure=json.loads((case/'failure.json').read_text());assert failure['supervisor_receipt']==receipt
            if name in ('wait-timeout','wait-error','combined','setup-deadline','kill-exhausts-budget'):
                assert receipt['reaped'] is False and receipt['ownership']=='unresolved' and receipt['exit'] is None
            elif launched:assert receipt['reaped'] is True
            else:assert receipt['reaped'] is None and receipt['ownership']=='no_returned_handle'
            if name in ('kill-esrch','kill-error','guard-cleanup'):assert 'wait' in events and events.index('kill')<events.index('wait')
            if name in ('wait-late-zero','wait-hard-late-zero','known-reaped-setup'):assert 'kill' not in events
            if name=='partial-read-error':assert receipt['stream_bytes']['stdout']==3 and receipt['stream_sha256']['stdout']==v.hashlib.sha256(b'abc').hexdigest()
            if name=='combined':
                assert receipt['primary'] and len(receipt['cleanup_errors'])>=4
                assert all(label+'_close' in [r['action'] for r in receipt['cleanup_errors']] for label in ('stdin','stdout','stderr'))
            assert persist==['fake.stdout','fake.stderr','processes.json']
            rows.append(dict(name='supervisor-'+name,status='PASS',simulated_handles=True,actual_process_launch=False,outer_fixture_status=status,receipt=receipt,events=events,wait_bounds=waits,persistence_attempts=persist))
    return rows


def main():
    if len(sys.argv)!=1:raise ValueError('no selectors')
    # This attempt was exclusively reserved for mandatory pre-edit snapshots.
    # Exactly those preparation members are permitted before the sole invocation.
    prepared={'baseline.json','baseline','baseline/main.cpp','baseline/client.cpp','baseline/clients2c.cpp'}
    if {str(p.relative_to(ATTEMPT)) for p in ATTEMPT.rglob('*')}!=prepared or FIXTURES.exists() or FIXTURES.is_symlink():raise ValueError('occupied or unrecognized preparation')
    for n,h in BASELINES.items():
        p=ATTEMPT/'baseline'/n;s=p.lstat()
        if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or sha(p)!=h:raise ValueError('baseline snapshot pin')
    durable_new(ATTEMPT/'STARTED',b'T163 sole helper proof; occupied attempts never rerun\n')
    start=time.monotonic();deadline=start+300
    signal.signal(signal.SIGALRM,whole_alarm);signal.alarm(295)
    def work(ctx):
        if sys.version_info[:3]!=(3,11,9) or str(Path(sys.executable).resolve()) not in TOOLS or {p:sha(p) for p in TOOLS}!=TOOLS:raise ValueError('installed tool pins')
        for n,value in (('emscripten-version.txt','"7.0.0"'),('emscripten-revision.txt','777e6e5db7b4990bcaeb1b9998ed642cc84e6629')):
            if (SDK/'upstream/emscripten'/n).read_text().strip()!=value:raise ValueError('SDK metadata')
        baseline_record=json.loads((ATTEMPT/'baseline.json').read_text())
        if baseline_record['status']!='PRE_EDIT_BASELINE_ONLY_NOT_EXECUTED' or {n:m['sha256'] for n,m in baseline_record['sources'].items()}!=BASELINES:raise ValueError('baseline authority')
        production=[ROOT/'source/src'/n for n in (*BASELINES,'browser_map_profile.h')]
        own=production+[HERE/n for n in ('verify.py','wrapper.cpp','wasm_runner.mjs','SCHEMA.md','README.md')]
        for p in own:
            s=p.lstat()
            if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1:raise ValueError('own source alias')
        authorities=[ROOT/n for n in ('AGENTS.md','tickets/T163.md','MVP/BLACKWOOD_CLIENT_FOUNDATION.md','notes/decisions/D217-Blackwood-source-profile-adoption.md','notes/decisions/D219-Blackwood-source-profile-release.md','notes/proposals/MAIN-Blackwood-client-integration-plan-1.md','notes/reviews/MAIN-Blackwood-client-integration-plan-review-1.md','notes/decisions/D212-corrected-authority-data-successor.md')]
        if sha(authorities[5])!='e89f8f9252e659a8b525b2eb0f03cfb3837515c1201d5871f2eaf9d0c8388133' or sha(authorities[6])!='f6b2b3c5cdf28ace1cc84d6e194f62f28ab31f770a3965c2370432b1c0e349e8':raise ValueError('adopted plan/review pins')
        supervisor_refs={ROOT/'web/world/authority-p2/verify.py':'720dd8aafb4546907ce73e72ac3bf972156cd67af4357b171ba01481b8d0e26d',ROOT/'web/world/authority-p2/test_adversarial.py':'af77747fa30cc0a566b382313eeb847aaf3a88a3d42a3c24b9369928fc5ce0e3'}
        for p,h in supervisor_refs.items():
            if sha(p)!=h:raise ValueError('accepted supervision source pin')
        assets=ROOT/'web/assets/blackwood-profile';manifest=assets/'manifest.json'
        if sha(manifest)!='8c4f7eef5f0deafb06bec60d62be529a684a30d56bbdc6dc3e5f38dd21c69e60':raise ValueError('accepted asset manifest pin')
        entries=json.loads(manifest.read_text())['entries'];pack=assets/'pack-root'
        if len(entries)!=84 or sorted(e['path'] for e in entries)!=sorted(str(p.relative_to(pack)) for p in pack.rglob('*') if p.is_file()):raise ValueError('asset membership')
        for e in entries:
            p=pack/e['path'];s=p.lstat()
            if not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or s.st_size!=e['bytes'] or sha(p)!=e['sha256']:raise ValueError('accepted asset changed')
        protected=[ROOT/'source/src',manifest,pack]+authorities+list(supervisor_refs)+[ROOT/'web/build/.cache/sysroot']+[HERE/n for n in ('verify.py','wrapper.cpp','wasm_runner.mjs','SCHEMA.md','README.md')]+[ATTEMPT/'baseline',ATTEMPT/'baseline.json']
        before=snapshot(protected);(ATTEMPT/'protected-before.json').write_bytes(dump(before))
        audit=audit_sources();(ATTEMPT/'source-audit.json').write_bytes(dump(audit))
        patches=[]
        for n in BASELINES:
            old=(ATTEMPT/'baseline'/n).read_text();new=(ROOT/'source/src'/n).read_text()
            patches.extend(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='baseline/'+n,tofile='source/src/'+n))
        (ATTEMPT/'source.patch').write_text(''.join(patches))
        raw,cases=corpus();expected={p:oracle(p,cases) for p in ('dev','blackwood')}
        env=dict(PATH='/usr/bin:/bin:/usr/sbin:/sbin',TMPDIR=str(ATTEMPT/'tmp'),EM_CACHE=str(ATTEMPT/'cache'),EM_PORTS=str(ATTEMPT/'cache/ports'),EM_FROZEN_CACHE='1',EMCC_TEMP_DIR=str(ATTEMPT/'tmp'),CLANG_MODULE_CACHE_PATH=str(ATTEMPT/'module-cache'),NODE_COMPILE_CACHE=str(ATTEMPT/'node-cache'),PYTHONDONTWRITEBYTECODE='1')
        for n in ('tmp','module-cache','node-cache','logs'):(ATTEMPT/n).mkdir()
        FIXTURES.mkdir()
        native='/usr/bin/clang++';clang=str(SDK/'upstream/bin/clang++');linker=str(SDK/'upstream/bin/wasm-ld');node=str(SDK/'node/24.19.0_64bit/bin/node')
        common=['-std=c++11','-O2','-Wall','-Wextra','-Werror','-fno-builtin','-I',str(ROOT/'source/src')]
        commands=[];executions=[];invalid=[]
        for target,compiler,flags in (('native',native,['-DT163_NATIVE','-D__EMSCRIPTEN__']),('wasm',clang,['--target=wasm32-unknown-emscripten','--sysroot='+str(ATTEMPT/'cache/sysroot'),'-D__EMSCRIPTEN__'])):
            for profile in ('dev','blackwood'):
                label=target+'-'+profile;profile_flags=['-DOUTBREAK_NETWORK_CLIENT']+(['-DOUTBREAK_BLACKWOOD_CLIENT'] if profile=='blackwood' else [])
                commands.append((label+'-compile',[compiler]+common+flags+profile_flags+['-MD','-MF',str(ATTEMPT/(label+'.d')),'-c',str(HERE/'wrapper.cpp'),'-o',str(ATTEMPT/(label+'.o'))]))
                if target=='native':
                    commands.append((label+'-link',[native,str(ATTEMPT/(label+'.o')),'-o',str(ATTEMPT/label)]));executions.append((label,[str(ATTEMPT/label)],profile))
                else:
                    commands.append((label+'-link',[linker,'--no-entry']+['--export='+n for n in EXPORTS]+[str(ATTEMPT/(label+'.o')),'-o',str(ATTEMPT/(label+'.wasm'))]));executions.append((label,[node,str(HERE/'wasm_runner.mjs'),str(ATTEMPT/(label+'.wasm'))],profile))
            for em in (0,1):
                for network in (0,1):
                    for standalone in (0,1):
                        if (em,network,standalone)==(1,1,0):continue
                        bits=[('-D' if value else '-U')+name for name,value in (('__EMSCRIPTEN__',em),('OUTBREAK_NETWORK_CLIENT',network),('STANDALONE',standalone))]
                        invalid.append((target+'-invalid-%d%d%d'%(em,network,standalone),[compiler]+common+([] if target=='native' else ['--target=wasm32-unknown-emscripten','--sysroot='+str(ATTEMPT/'cache/sysroot')])+bits+['-DOUTBREAK_BLACKWOOD_CLIENT','-DT163_GUARD_ONLY','-fsyntax-only',str(HERE/'wrapper.cpp')]))
        accepted_deps=json.loads((ROOT/'web/world/authority-p2/tests/attempt-1/dependencies.json').read_text())
        sdk_inputs={p:identity(Path(p)) for p in accepted_deps if p.startswith('/Library/Developer/CommandLineTools/') or p.startswith(str(SDK))}
        for p in sdk_inputs:
            if sha(p)!=accepted_deps[p]['sha256']:raise ValueError('accepted SDK drift')
        source_pins={str(p.relative_to(ROOT)):sha(p) for p in own}
        plan=dict(scope='PRIVATE_HELPER_ONLY_NOT_FULL_CLIENT_OR_RUNTIME',baseline_pins=BASELINES,baseline_record_sha256=sha(ATTEMPT/'baseline.json'),patch_sha256=sha(ATTEMPT/'source.patch'),source_pins=source_pins,authority=snapshot(authorities),accepted_supervisor_references={str(p):h for p,h in supervisor_refs.items()},supervision=SUPERVISION_PLAN,supervisor_fixtures=list(SUPERVISOR_CASES),tools={p:identity(Path(p)) for p in TOOLS},accepted_sdk_inputs=sdk_inputs,environment=env,commands=commands,executions=executions,invalid_profile_commands=invalid,expected_guard_diagnostic=GUARD_DIAGNOSTIC,layout=LAYOUT,exports=list(EXPORTS),cases=cases,case_count_per_profile=len(cases),corpus_sha256=hashlib.sha256(raw).hexdigest(),oracle_sha256={p:hashlib.sha256(b).hexdigest() for p,b in expected.items()},four_target_raw_bytes=4*len(expected['dev']),caps=dict(whole_seconds=300,operation_seconds=60,child_output_bytes=8388608,cases_per_profile_target=1024,response_bytes=256,four_target_raw_bytes=1048576),native_macro_emulation=True,full_client_build=False,runtime=False)
        (ATTEMPT/'plan.json').write_bytes(dump(plan));(ATTEMPT/'corpus.bin').write_bytes(raw)
        for profile,b in expected.items():(ATTEMPT/(profile+'-expected.bin')).write_bytes(b)
        shutil.copytree(ROOT/'web/build/.cache/sysroot',ATTEMPT/'cache/sysroot',symlinks=True)
        copied={str(ROOT/'web/build/.cache/sysroot'/Path(p).relative_to(ATTEMPT/'cache/sysroot')):v for p,v in snapshot([ATTEMPT/'cache/sysroot']).items()}
        if copied!=snapshot([ROOT/'web/build/.cache/sysroot']):raise ValueError('copied sysroot')
        supervisor=Supervisor(env,deadline)
        for label,argv in commands:supervisor.run(label,argv)
        deps=set()
        for target in ('native','wasm'):
            for profile in ('dev','blackwood'):
                body=(ATTEMPT/(target+'-'+profile+'.d')).read_text().replace(chr(92)+chr(10),' ')
                for n in shlex.split(body.split(': ',1)[1]):deps.add(Path(n) if Path(n).is_absolute() else ROOT/n)
        for p in deps:
            if p not in (ROOT/'source/src/browser_map_profile.h',HERE/'wrapper.cpp') and not str(p).startswith('/Library/Developer/CommandLineTools/') and not p.is_relative_to(ATTEMPT/'cache/sysroot') and not p.is_relative_to(SDK/'upstream/lib/clang/24/include'):raise ValueError('unexpected helper dependency')
        dependency_snapshot=snapshot(sorted(deps));(ATTEMPT/'dependencies.json').write_bytes(dump(dependency_snapshot))
        outputs={}
        for label,argv,profile in executions:
            actual,stderr=supervisor.run(label,argv,raw);(ATTEMPT/(label+'.bin')).write_bytes(actual)
            if stderr or actual!=expected[profile]:raise ValueError('complete helper oracle mismatch '+label)
            outputs[label]=hashlib.sha256(actual).hexdigest()
        diagnostics=[]
        for label,argv in invalid:
            stdout,stderr=supervisor.run(label,argv,expected_profile_guard=True);message=stderr.decode('utf-8',errors='strict')
            errors=re.findall(r'^.*?:\d+:\d+: (?:fatal )?error: (.*)$',message,re.MULTILINE)
            if stdout or errors!=[GUARD_DIAGNOSTIC] or 'warning:' in message or '1 error generated.' not in message:raise ValueError('unrelated or missing expected profile diagnostic '+label)
            diagnostics.append(dict(label=label,status='EXPECTED_EXACT_PROFILE_GUARD',stderr_sha256=hashlib.sha256(stderr).hexdigest()))
        (ATTEMPT/'invalid-profile-results.json').write_bytes(dump(diagnostics))
        fixtures=supervisor_regressions(sys.modules[__name__],FIXTURES)
        fixture_bytes=sum(p.stat().st_size for p in FIXTURES.rglob('*') if p.is_file())
        if len(fixtures)!=44 or fixture_bytes>4194304:raise ValueError('finite supervisor fixture bound')
        (ATTEMPT/'supervisor-fixtures.json').write_bytes(dump(dict(status='PASS',cases=fixtures,fixture_bytes=fixture_bytes,maximum_fixture_bytes=4194304,actual_process_fault_injections=0)))
        after=snapshot(protected);(ATTEMPT/'protected-after.json').write_bytes(dump(after))
        if before!=after or dependency_snapshot!=snapshot(sorted(deps)) or {p:sha(p) for p in TOOLS}!=TOOLS or sdk_inputs!={p:identity(Path(p)) for p in sdk_inputs}:raise ValueError('source/input/tool preservation')
        if time.monotonic()>=deadline or GUARD_EXPIRED:raise TimeoutError('whole deadline')
        return dict(scope='COMPILED_PRIVATE_PROFILE_HELPERS_PLUS_STATIC_SOURCE_GATE_AUDIT',actual_helper_targets=4,cases_per_profile_target=len(cases),expected_guard_compiles=len(diagnostics),guarded_simulated_supervisor_cases=len(fixtures),outputs=outputs,source_pins=source_pins,baseline_pins=BASELINES,static_gate_audit=True,native_macro_emulation=True,all_actual_children_reaped=all(p['reaped'] for p in supervisor.receipts),combined_child_output_bytes=supervisor.total,elapsed_s=time.monotonic()-start,assets_unchanged=True,other_sources_unchanged=True,full_client_build=False,native_engine=False,browser_runtime=False,network=False,P0=False)
    return terminal_pipeline(ATTEMPT,work,sys.stdout)


if __name__=='__main__':raise SystemExit(main())
