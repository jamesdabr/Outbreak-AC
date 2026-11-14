# T200 exact textual source corrections

T2001.0/D324 SOURCE ONLY. Before contents are the actual T196 delivered files,
not a rewrite of historical handoffs/reviews. Full unified diffs below were
constructed as text data; no own/project parser/import/control was run.

## tests/outbreak/motion_record/release-1/verify.py

Before 40518/0e95bd71845dc110e1198e45839073e157064a49ec02636c57d179fb70fecadf; after 95700/608a53f128de40d7b375d9d3e7c3ef7e3ab8206903d3b9e2193d89b97b1b15ac.

```diff
--- T196-delivered/tests/outbreak/motion_record/release-1/verify.py
+++ T200-source/tests/outbreak/motion_record/release-1/verify.py
@@ -1,4 +1,4 @@
-"""T196 future controller SOURCE ONLY. Do not import/run under source-only lease.
+"""T196/T200 future controller SOURCE ONLY. Do not import/run under this lease.
 
 Every effect requires a separately MAIN-pinned lease hash and fresh fixed root.
 No default execution, automatic retry, package acquisition or project import.
@@ -38,6 +38,35 @@
 
 class Refusal(RuntimeError):pass
 
+READ_CUTOFF=None # actual main/physical Job.step only; never set by pure fakes.
+RETAINED_READERS=[]
+
+def read_guard():
+    if READ_CUTOFF is not None:require(time.monotonic()<READ_CUTOFF,'read/release original cutoff')
+
+def guarded_file(path,cap,hash_only=False):
+    """Read-only raw FD; even its release cannot start after original cutoff."""
+    fd=None;closing=False;closed=False;parts=[];h=hashlib.sha256();count=0
+    try:
+        read_guard();fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW);read_guard()
+        while True:
+            read_guard();block=os.read(fd,min(1048576,cap-count+1))
+            # Preserve returned facts before a late-read admission check.
+            count+=len(block)
+            if hash_only:h.update(block)
+            else:parts.append(block)
+            read_guard();require(count<=cap,'bounded read')
+            if not block:break
+        read_guard();closing=True;os.close(fd);closed=True;read_guard()
+        return h.hexdigest() if hash_only else b''.join(parts)
+    except BaseException:
+        if fd is not None and not closing:
+            try:read_guard();closing=True;os.close(fd);closed=True;read_guard()
+            except BaseException:pass
+        if fd is not None and not closed:
+            RETAINED_READERS.append({'fd':fd,'path':str(path),'bytes_read':count,'close_ambiguous':closing,'parts':parts})
+        raise
+
 def require(condition,reason):
     if not condition:raise Refusal(reason)
 
@@ -51,8 +80,7 @@
     path=Path(path);s=path.lstat()
     require(path.is_file() and not path.is_symlink() and s.st_nlink==1,'ordinary input file')
     require(s.st_size<=cap,'input byte limit')
-    with path.open('rb') as f:
-        b=f.read(cap+1)
+    b=guarded_file(path,cap)
     require(len(b)<=cap and len(b)==s.st_size,'bounded complete input read')
     return b
 
@@ -68,14 +96,31 @@
                     mtime=s.st_mtime_ns,ctime=s.st_ctime_ns)
     require(p.is_file() and s.st_nlink==1,'ordinary single-link protection member')
     require(s.st_size<=ARTIFACTS,'protected member byte limit')
-    with p.open('rb') as f:
-        h=hashlib.sha256()
-        while True:
-            block=f.read(65536)
-            if not block:break
-            h.update(block)
+    sha=guarded_file(p,ARTIFACTS,hash_only=True)
     return dict(kind='file',mode=s.st_mode&0o7777,nlink=s.st_nlink,bytes=s.st_size,
-                sha256=h.hexdigest(),mtime=s.st_mtime_ns,ctime=s.st_ctime_ns)
+                sha256=sha,mtime=s.st_mtime_ns,ctime=s.st_ctime_ns)
+
+# H3: no source/data/output reader exemption. Only these typed installed roles.
+TOOL_SPECS={
+ '/usr/bin/clang++':('179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818',118928,0o755,78,()),
+ '/private/tmp/outbreak-web-sdk/upstream/bin/clang++':('9a96f4220eefe21e72a4a9a20a88f4d6c26cad1b047cb02b5b22a96bef49c423',165339888,0o755,1,(('clang++','clang'),('clang','clang-24'))),
+ '/private/tmp/outbreak-web-sdk/upstream/bin/wasm-ld':('b851d4f8a53ca2839651b62821a8981fcdb22a51c8c7fc04733ed2f6d050ad5c',69821584,0o755,1,(('wasm-ld','lld'),)),
+ '/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node':('27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1',121306800,0o755,1,()),
+ '/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11':('4e28e811a89aeac6eed668ae641c7f85f5831e42e8dc6cd9a85a3bcc032ec46a',152624,0o775,1,())}
+
+def installed_tool_record(raw):
+    """Exact supported role only; all aliases individually observed, no generic follow."""
+    require(raw in TOOL_SPECS,'unsupported installed tool role')
+    sha,size,mode,nlink,chain=TOOL_SPECS[raw];p=Path(raw);aliases={}
+    for name,target in chain:
+        require(p.name==name and p.is_symlink(),'exact tool alias kind/path')
+        r=file_record(p);require(r['link']==target and r['nlink']==1 and r['mode']==0o755,'exact alias target/mode/link')
+        aliases[str(p)]=r;p=p.parent/target
+    s=p.lstat();require(p.is_file() and not p.is_symlink(),'resolved tool ordinary')
+    require((s.st_size,s.st_mode&0o7777,s.st_nlink)==(size,mode,nlink),'exact installed byte/mode/link role')
+    require(guarded_file(p,size,hash_only=True)==sha,'installed role hash')
+    return {'raw':raw,'aliases':aliases,'resolved':str(p),'resolved_identity':dict(
+        kind='file',bytes=size,mode=mode,nlink=nlink,sha256=sha,mtime=s.st_mtime_ns,ctime=s.st_ctime_ns)}
 
 def inventory(root):
     root=Path(root);require(root.is_dir() and not root.is_symlink(),'inventory root')
@@ -116,6 +161,9 @@
     for p,r in plan['protected_files'].items():require(file_record(p)==r,'changed protected file '+p)
     for p,r in plan['protected_roots'].items():require(inventory(p)==r,'changed protected graph '+p)
     require(source_records()==plan['source_records'],'changed source package')
+    if plan['operation']=='MR-ACTUAL-1':
+        for raw,role in plan['tools'].items():require(installed_tool_record(raw)==role,'changed installed typed role/alias')
+        validate_wait_role(plan)
 
 def terminal_gate(f):
     """Used by the real runner AND pure future control fixtures."""
@@ -129,126 +177,414 @@
     require(isinstance(f.get('whole_elapsed'),(int,float)) and 0<=f['whole_elapsed']<=300,'timely whole')
     require(integer(f.get('capture'),0,CAPTURE),'aggregate captured byte bound')
 
+# H1/H2: all physical boundaries are dormant and injected in pure controls.
+# Strong references are never discarded when an operation is ambiguous/expired.
+UNRESOLVED_HANDLES=[]
+ABI_INPUT_HASHES={
+ '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/sys/wait.h':'b77f7dd6f592eba8b0d51c15c7b975472fdad50c12ea296f74f062cbf98dcbf7',
+ '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/sys/signal.h':'171af7545ef750627aeba02c1de838c05e2cf396e2f49881ea74dba6990c44a3',
+ '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/arm/_types.h':'4f0bde85f9a41cc7d30fff22ebd7e8f4eb206a55a926eda012a2e7481e3524fa',
+ '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/machine/_types.h':'f27264f8fdec9f164b4fc2b556f666ed7c5c0e5b88fd9f23db0b731ffa6cf864',
+ '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/sys/_types.h':'863c4f07045775002b63b7e616742d9f746e4a02da4441442d8fe1138bbd0ff9',
+ '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/sys/_types/_id_t.h':'fb7255c9872e2a805c206796326e21d47146e22c93c09752126d7166bdaba5e5',
+ '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/sys/_types/_pid_t.h':'052a6dbbec8e30623c2d33dd373992f6c5d0c57c57ed4949d2b48c4ab0976487',
+ '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/sys/_types/_uid_t.h':'d2140a65a17943a857381757c0b73a920f35ade41dc9809437c168be457c276a',
+ '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/ctypes/__init__.py':'608671c6b49e5e027e3348fcf492718c33f69f919d99f4ff170522c40bd4c550',
+ '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/ctypes/_endian.py':'38dc998ee2d180a64d4fe561b79287b19850df405f48fe72dede7a65d71de844',
+ '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/lib-dynload/_ctypes.cpython-311-darwin.so':'e5ed138ab1322322bce3dad9d7f9e5bff60ac79cfe09b340a89593ffe3b3add9',
+ '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/struct.py':'9c231f9497caf513a22dee8f790b07f969b0e45854a0bdd6dd84b492e08c2856',
+ '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/lib-dynload/_struct.cpython-311-darwin.so':'9f978a4bc70a3c6ca10c53a1d1d96b52e0dad40f39176e615c0ab5fa58f68f7a'}
+
+def validate_wait_role(plan):
+    role=plan['wait_adapter']
+    require(set(role)=={'schema','system_identifier','symbol','idtype','flags','inputs','python'},'closed fixed wait role')
+    require((role['schema'],role['system_identifier'],role['symbol'],role['idtype'],role['flags'])==
+            ('D235_D260_DARWIN_ARM64','/usr/lib/libSystem.B.dylib','waitid',1,37),'fixed wait ABI selector')
+    require(set(role['inputs'])==set(ABI_INPUT_HASHES),'exact ABI/ctypes/type input union')
+    for path,sha in ABI_INPUT_HASHES.items():
+        r=file_record(path);require(r==role['inputs'][path] and r['sha256']==sha,'exact ABI input '+path)
+    python='/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11'
+    require(installed_tool_record(python)==role['python'] and str(Path(sys.executable).resolve())==python,'canonical supervisor Python')
+    require(sys.platform=='darwin' and sys.byteorder=='little' and os.uname().machine=='arm64'
+            and sys.version_info[:2]==(3,11),'supported wait platform')
+
+def make_observer(plan,clock):
+    # Actual backend ONLY, never called by pure controls. No library at import.
+    validate_wait_role(plan)
+    require(signal.getsignal(signal.SIGCHLD)==signal.SIG_DFL,'default SIGCHLD ownership')
+    prior=sys.dont_write_bytecode;sys.dont_write_bytecode=True
+    try:import ctypes
+    finally:sys.dont_write_bytecode=prior
+    class Sigval(ctypes.Union):
+        _fields_=[('i',ctypes.c_int),('p',ctypes.c_void_p)]
+    class Siginfo(ctypes.Structure):
+        _fields_=[('signo',ctypes.c_int),('error',ctypes.c_int),('code',ctypes.c_int),
+                  ('pid',ctypes.c_int),('uid',ctypes.c_uint),('status',ctypes.c_int),
+                  ('addr',ctypes.c_void_p),('value',Sigval),('band',ctypes.c_long),('pad',ctypes.c_ulong*7)]
+    class Native:
+        widths=[ctypes.sizeof(t) for t in (ctypes.c_int,ctypes.c_uint,ctypes.c_long,ctypes.c_ulong,ctypes.c_void_p)]
+        signs=[ctypes.c_int(-1).value,ctypes.c_uint(-1).value,ctypes.c_ulong(-1).value]
+        layout=[ctypes.sizeof(Sigval),ctypes.alignment(Sigval),ctypes.sizeof(Siginfo),ctypes.alignment(Siginfo)]
+        offsets={k:getattr(Siginfo,k).offset for k in ('signo','error','code','pid','uid','status','addr','value','band','pad')}
+        def zero(self):return Siginfo()
+        def wait(self,idtype,pid,info,flags):return self.call(idtype,pid,ctypes.byref(info),flags)
+        def error(self):return ctypes.get_errno()
+    native=Native()
+    # Validate typed ABI BEFORE loading the one fixed system identifier.
+    validate_native_layout(native)
+    library=ctypes.CDLL('/usr/lib/libSystem.B.dylib',use_errno=True);call=library.waitid
+    call.argtypes=[ctypes.c_int,ctypes.c_uint,ctypes.POINTER(Siginfo),ctypes.c_int];call.restype=ctypes.c_int
+    native.library=library;native.call=call
+    return observer_protocol(native,clock)
+
+def validate_native_layout(native):
+    require(native.widths==[4,4,8,8,8] and native.signs==[-1,0xffffffff,0xffffffffffffffff],'fixed native widths/signedness')
+    require(native.layout==[8,8,104,8] and native.offsets=={'signo':0,'error':4,'code':8,'pid':12,'uid':16,
+            'status':20,'addr':24,'value':32,'band':40,'pad':48},'fixed complete native layout')
+
+def observer_protocol(native,clock):
+    # The ONLY injected native ABI boundary. Real factory above always supplies
+    # exact ctypes types; pure Job.run controls supply in-memory fake records.
+    validate_native_layout(native)
+    def observe(pid,hard):
+        require(integer(pid,2,2**31-1),'original observer PID')
+        while True:
+            require(clock()<hard,'observer original cutoff')
+            info=native.zero() # all104 bytes zeroed for every call/retry.
+            rc=native.wait(1,pid,info,37)
+            require(clock()<hard and type(rc) is int and rc in (-1,0),'timely waitid return')
+            if rc==-1:
+                e=native.error()
+                if e==errno.EINTR:continue
+                raise OSError(e,'original waitid') # ECHILD is never ownership.
+            if info.pid==0:
+                require(info.signo==info.error==info.code==info.status==0,'no-event zero fields');return None
+            require(info.pid==pid and info.signo==signal.SIGCHLD and info.error==0,'exact original siginfo')
+            require(info.code in (1,2,3) and integer(info.status,0,255),'terminal status schema')
+            if info.code==1:return info.status
+            require(integer(info.status,1,127),'terminal signal status');return -info.status
+    observe.native_boundary=native # retains library, typed call and record role.
+    return observe
+
+class RealBoundary:
+    """Only actual separately leased jobs may instantiate effects through this."""
+    physical=True
+    def now(self):return time.monotonic()
+    def prepare(self,plan):return make_observer(plan,self.now)
+    def tool(self,path,plan):
+        if path==str(HERE/'attempt-1'/'native-runner'):
+            require(file_record(path)==plan['owned_executable'],'owned exact link product');return
+        require(installed_tool_record(path)==plan['tools'][path],'exact installed typed tool')
+    def mkdir(self,path):os.mkdir(path,0o700)
+    def open(self,path):return os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
+    def chmod(self,fd):os.fchmod(fd,0o600)
+    def write(self,fd,data):return os.write(fd,data)
+    def sync(self,fd):os.fsync(fd)
+    def close(self,fd):os.close(fd)
+    def spawn(self,argv,env):
+        return subprocess.Popen(argv,cwd=ROOT,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
+                                stderr=subprocess.PIPE,start_new_session=True,bufsize=0,close_fds=True)
+    def selector(self):return selectors.DefaultSelector()
+    def nonblocking(self,pipe):os.set_blocking(pipe.fileno(),False)
+    def register(self,sel,pipe,events):sel.register(pipe,events)
+    def unregister(self,sel,pipe):sel.unregister(pipe)
+    def select(self,sel,seconds):return [(k.fileobj,e) for k,e in sel.select(seconds)]
+    def readpipe(self,pipe):return os.read(pipe.fileno(),65536)
+    def writepipe(self,pipe,data):return os.write(pipe.fileno(),data[:65536])
+    def pipeclose(self,pipe):pipe.close() # FileIO, never a buffered flush.
+    def selectorclose(self,sel):sel.close()
+    def pgid(self,pid):return os.getpgid(pid)
+    def sid(self,pid):return os.getsid(pid)
+    def group(self,pid):
+        try:os.killpg(pid,0)
+        except ProcessLookupError:return 'ABSENT_ESRCH'
+        except PermissionError as e:
+            if e.errno==errno.EPERM:return 'UNKNOWN_EPERM'
+            raise
+        return 'PRESENT'
+    def signal(self,pid):os.killpg(pid,signal.SIGKILL)
+    def reap(self,pid):return os.waitpid(pid,os.WNOHANG)
+    def exitcode(self,status):return os.waitstatus_to_exitcode(status)
+    def pause(self,seconds):time.sleep(seconds)
+
 class Job:
-    def __init__(self,root,started,plan):
+    def __init__(self,root,started,plan,boundary=None,reserve=True):
         self.root=root;self.started=started;self.deadline=started+300;self.plan=plan
-        self.captured=0;self.metadata=0;self.records=[]
+        self.b=boundary if boundary is not None else RealBoundary()
+        self.captured=0;self.metadata=0;self.records=[];self.actions=[];self.owned=[];self.writes=[]
         self.categories={'compile':0,'runner':0,'reports':0,'driver':0}
         self.limits={'compile':2097152,'runner':1048576,'reports':2097152,'driver':1048576}
-        require(not os.path.lexists(root),'fresh operation slot absent')
-        root.mkdir(mode=0o700)
-        self.write('OPERATION.json',encoded({'operation':plan['operation'],'status':'IN_PROGRESS'}))
-    def check(self):require(time.monotonic()<=self.deadline,'whole deadline including persistence')
+        if reserve:
+            require(not os.path.lexists(root),'fresh operation slot absent')
+            self.step('reserve-root',lambda:self.b.mkdir(root),self.deadline)
+            self.write('OPERATION.json',encoded({'operation':plan['operation'],'status':'IN_PROGRESS'}))
+    def check(self,cutoff=None):
+        hard=self.deadline if cutoff is None else min(cutoff,self.deadline)
+        require(self.b.now()<hard,'original absolute cutoff')
+    def step(self,name,fn,cutoff):
+        # No stale event-loop timestamp authorizes the next operation.
+        self.check(cutoff);a={'name':name,'started':self.b.now(),'cutoff':min(cutoff,self.deadline),'returned':False}
+        self.actions.append(a)
+        global READ_CUTOFF
+        prior_read_cutoff=READ_CUTOFF
+        if getattr(self.b,'physical',False):READ_CUTOFF=min(cutoff,self.deadline)
+        try:
+            value=fn();a['returned']=True;a['ended']=self.b.now()
+        except BaseException as e:
+            a['error']=type(e).__name__+': '+str(e);a['ended']=self.b.now();raise
+        finally:READ_CUTOFF=prior_read_cutoff
+        self.check(cutoff);return value
     def charge(self,category,count):
-        require(integer(count,0,CAPTURE),'capture increment')
-        self.captured+=count
+        require(integer(count,0,CAPTURE),'capture increment');self.captured+=count
         if category=='raw':require(self.captured<=CAPTURE,'aggregate capture');return
         self.categories[category]+=count
         require(self.categories[category]<=self.limits[category] and self.captured<=CAPTURE,'capture category/aggregate')
-    def write(self,name,data,category=None):
-        self.check();p=self.root/name
-        require(not p.is_absolute() or p.is_relative_to(self.root),'owned output')
-        require('..' not in Path(name).parts,'no parent escape')
-        require(len(data)<=METADATA,'one output byte bound')
+    def write(self,name,data,category=None,cutoff=None):
+        hard=self.deadline if cutoff is None else min(cutoff,self.deadline)
+        self.check(hard);p=self.root/name
+        require(Path(name).name==name and name not in ('','.','..'),'owned flat output path')
+        require(type(data) is bytes and len(data)<=METADATA,'bounded byte output')
         if category:self.charge(category,len(data))
-        else:
-            self.metadata+=len(data);require(self.metadata<=METADATA,'metadata aggregate')
-        p.parent.mkdir(parents=True,exist_ok=True)
-        with p.open('xb') as f:
-            os.chmod(p,0o600);f.write(data);f.flush();os.fsync(f.fileno())
-        self.check();return p
-    def group_state(self,pid):
-        try:os.killpg(pid,0)
-        except ProcessLookupError:return 'ABSENT_ESRCH'
-        except PermissionError:return 'UNKNOWN_EPERM'
-        except OSError:return 'UNKNOWN_OSERROR'
-        return 'PRESENT'
+        else:self.metadata+=len(data);require(self.metadata<=METADATA,'metadata aggregate')
+        r={'name':name,'cutoff':hard,'planned':len(data),'written':0,'fd':None,
+           'close_attempted':False,'closed':False,'complete':False,'error':None,'write_return_unresolved':False}
+        self.writes.append(r);owner={'kind':'file','receipt':r,'fd':None};self.owned.append(owner)
+        try:
+            # Save the acquired descriptor INSIDE the checked callable, so a late
+            # return cannot lose it when step refuses post-call time admission.
+            def acquire():
+                fd=self.b.open(p);owner['fd']=fd;r['fd']=fd;return fd
+            self.step('file-open:'+name,acquire,hard);fd=owner['fd']
+            self.step('file-chmod:'+name,lambda:self.b.chmod(fd),hard)
+            while r['written']<len(data):
+                offset=r['written']
+                def put():
+                    r['write_return_unresolved']=True
+                    n=self.b.write(fd,data[offset:]);r['write_return_unresolved']=False
+                    require(integer(n,1,len(data)-offset),'positive bounded write')
+                    r['written']+=n;return n
+                self.step('file-write:'+name,put,hard)
+            self.step('file-fsync:'+name,lambda:self.b.sync(fd),hard)
+            def close():
+                r['close_attempted']=True;self.b.close(fd);r['closed']=True
+            self.step('file-close:'+name,close,hard)
+            r['complete']=True;r['completed_at']=self.b.now();return p
+        except BaseException as e:
+            r['error']=type(e).__name__+': '+str(e)
+            # No implicit context exit/flush, no close retry after an ambiguous
+            # close, and no release at/after this ORIGINAL cutoff.
+            if owner['fd'] is not None and not r['close_attempted'] and self.b.now()<hard:
+                try:
+                    def close_failure():
+                        r['close_attempted']=True;self.b.close(owner['fd']);r['closed']=True
+                    self.step('file-failure-close:'+name,close_failure,hard)
+                except BaseException as close_error:r['close_error']=type(close_error).__name__+': '+str(close_error)
+            if not r['closed']:UNRESOLVED_HANDLES.append(owner)
+            raise
+    def stamp(self,f,start):
+        f['elapsed']=self.b.now()-start;f['whole_elapsed']=self.b.now()-self.started;f['capture']=self.captured
     def run(self,label,argv,input_bytes=b'',raw=False):
-        self.check();start=time.monotonic();hard=min(start+60,self.deadline)
-        require(hard-start>=3,'cleanup/persistence reservation inside deadline')
-        tool=Path(argv[0]);role=self.plan['tools'].get(str(tool))
-        require(role is not None and file_record(tool)==role,'exact tool role')
-        environment=dict(self.plan['environment'])
-        require('HOME' not in environment and environment.get('LC_ALL')=='C','closed approved environment')
-        environment['TMPDIR']=str(self.root/'tmp');(self.root/'tmp').mkdir(exist_ok=True)
-        proc=subprocess.Popen(argv,cwd=ROOT,env=environment,stdin=subprocess.PIPE,
-                              stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
-        pid=proc.pid;require(integer(pid,1,2**31-1),'Popen original PID')
-        f=dict(pid=pid,reaped=False,reaped_pid=None,exit_code=None,group='UNKNOWN',
-               stdin_complete=False,stdout_eof=False,stderr_eof=False,primary=None,secondary=[])
-        chunks={'stdout':bytearray(),'stderr':bytearray()};sent=0;signals=[]
-        sel=selectors.DefaultSelector()
-        streams={proc.stdout.fileno():'stdout',proc.stderr.fileno():'stderr'}
-        for fd in streams:os.set_blocking(fd,False);sel.register(fd,selectors.EVENT_READ)
-        os.set_blocking(proc.stdin.fileno(),False)
-        if input_bytes:sel.register(proc.stdin.fileno(),selectors.EVENT_WRITE)
-        else:proc.stdin.close();f['stdin_complete']=True
-        def stop_group(sig):
-            # Only the unreaped ORIGINAL group can be signaled; no ambient discovery.
-            if f['reaped']:return
-            try:os.killpg(pid,sig);signals.append(int(sig))
-            except ProcessLookupError:pass
-            except OSError as e:f['secondary'].append('group signal '+str(e.errno))
+        self.check();start=self.b.now();hard=min(start+60,self.deadline);work=hard-2
+        require(hard-start>=3,'cleanup reserve inside original cutoff')
+        f=dict(pid=None,reaped=False,reaped_pid=None,exit_code=None,group='UNKNOWN',
+               stdin_complete=False,stdout_eof=False,stderr_eof=False,primary=None,secondary=[],
+               anchor_lost=False,permission_observation=None,signals=[],argv=list(argv),
+               cutoff=hard,work_cutoff=work,persistence='NOT_STARTED',actions_start=len(self.actions))
+        self.records.append(f)
+        owned={'kind':'child','process':None,'selector':None,'receipt':f,'closed':set(),'close_attempted':set()}
+        self.owned.append(owned) # provisional ownership BEFORE acquisition.
+        chunks={'stdout':bytearray(),'stderr':bytearray()};pending={};sent=0;observer=None
+        def fault(e):
+            text=type(e).__name__+': '+str(e)
+            if f['primary'] is None:f['primary']=text
+            else:f['secondary'].append(text)
+        def fresh():
+            try:
+                self.check(hard);proc=owned['process'];pid=f['pid']
+                require(proc is not None and integer(pid,2,2**31-1) and proc.pid==pid
+                        and proc.returncode is None and not f['reaped'] and not f['anchor_lost'],'original live handle')
+                require(self.step('getpgid',lambda:self.b.pgid(pid),hard)==pid,'owned pgid')
+                require(self.step('getsid',lambda:self.b.sid(pid),hard)==pid,'owned session')
+                value=self.step('fresh-nonreaping-anchor',lambda:observer(pid,hard),hard)
+                require(value is None or integer(value,-127,255),'typed nonreaping result')
+                return value
+            except BaseException:
+                f['anchor_lost']=True;raise
+        def close_pipe(name):
+            proc=owned['process'];pipe=getattr(proc,name)
+            if name in owned['closed']:return
+            require(name not in owned['close_attempted'],'ambiguous close is not retried')
+            def close():
+                owned['close_attempted'].add(name);self.b.pipeclose(pipe);owned['closed'].add(name)
+            self.step('pipe-close:'+name,close,hard)
+        def consume():
+            # Never consume the anchor before eligible group handling.
+            while True:
+                fresh()
+                def reap():
+                    got,status=self.b.reap(f['pid'])
+                    if got:
+                        require(got==f['pid'],'only original consuming waitpid')
+                        # Truth published before clock/zero admission; cannot
+                        # turn a late/nonzero actual reap back into unreaped.
+                        f['reaped']=True;f['reaped_pid']=got
+                        f['exit_code']=self.b.exitcode(status)
+                        owned['process'].returncode=f['exit_code']
+                    return got
+                try:got=self.step('consume-original-waitpid',reap,hard)
+                except BaseException:
+                    if not f['reaped']:f['anchor_lost']=True
+                    raise
+                if got:return
+                self.step('wait-pause',lambda:self.b.pause(0.005),hard)
+        def closure():
+            anchor_exit=fresh()
+            before=self.step('pre-reap-group-observation',lambda:self.b.group(f['pid']),hard)
+            if before=='UNKNOWN_EPERM':
+                require(type(anchor_exit) is int and anchor_exit==0,'D260 fresh terminal0 only')
+                f['permission_observation']={'phase':'PRE_REAP_PROBE','errno':1,'pid':f['pid'],
+                    'terminal_exit_code':0,'mutating_signal_attempted':False,'resolution':'UNRESOLVED'}
+                # A second fresh exact terminal0 immediately before consuming.
+                require(fresh()==0,'still-owned terminal0 before deferred reap')
+            elif before=='PRESENT':
+                fresh() # last ownership observation before EVERY mutation.
+                def signal_owned():
+                    f['signals'].append('SIGKILL_ANCHORED');self.b.signal(f['pid'])
+                self.step('anchored-group-kill',signal_owned,hard)
+            else:require(before=='ABSENT_ESRCH','strict pre-reap group result')
+            consume()
+            # Distinct read-only post-reap observation. NEVER signal now.
+            after=self.step('post-reap-group-observation',lambda:self.b.group(f['pid']),hard)
+            f['group']=after;require(after=='ABSENT_ESRCH','strict post-reap closure')
+            if f['permission_observation'] is not None:f['permission_observation']['resolution']='POST_REAP_ABSENT'
+        def drain(limit):
+            nonlocal sent
+            sel=owned['selector']
+            while pending:
+                self.check(limit)
+                events=self.step('selector-select',lambda:self.b.select(sel,0.005),limit)
+                for pipe,event in events:
+                    self.check(limit);name=pending.get(pipe);require(name is not None,'registered original pipe')
+                    if event&selectors.EVENT_WRITE:
+                        def write_input():
+                            nonlocal sent
+                            f['stdin_return_unresolved']=True
+                            n=self.b.writepipe(pipe,input_bytes[sent:]);f['stdin_return_unresolved']=False
+                            require(integer(n,1,len(input_bytes)-sent),'bounded stdin write')
+                            sent+=n;f['stdin_bytes_written']=sent;return n
+                        try:n=self.step('stdin-write',write_input,limit)
+                        except BlockingIOError:continue
+                        if sent==len(input_bytes):
+                            self.step('stdin-unregister',lambda:self.b.unregister(sel,pipe),limit)
+                            del pending[pipe];close_pipe('stdin');f['stdin_complete']=True
+                    else:
+                        def read_output():
+                            block=self.b.readpipe(pipe)
+                            require(type(block) is bytes and len(block)<=65536,'bounded pipe bytes')
+                            if block:
+                                chunks[name].extend(block) # preserve returned bytes even if late/over-budget.
+                                self.charge('raw' if raw and name=='stdout' else 'runner' if raw else 'compile',len(block))
+                            return block
+                        try:block=self.step(name+'-read',read_output,limit)
+                        except BlockingIOError:continue
+                        if not block:
+                            self.step(name+'-unregister',lambda:self.b.unregister(sel,pipe),limit)
+                            del pending[pipe];f[name+'_eof']=True
+                if not f['reaped']:
+                    if fresh() is not None:return
+            if not f['reaped']:
+                while fresh() is None:self.step('terminal-pause',lambda:self.b.pause(0.005),limit)
         try:
-            while sel.get_map() or not f['reaped']:
-                now=time.monotonic()
-                if now>=hard-2 and f['primary'] is None:f['primary']='child cleanup cutoff';stop_group(signal.SIGTERM)
-                if now>=hard-1 and not f['reaped'] and int(signal.SIGKILL) not in signals:stop_group(signal.SIGKILL)
-                if now>=hard:raise Refusal('child hard deadline')
-                for key,events in sel.select(min(0.05,max(0,hard-now))):
-                    fd=key.fd
-                    if events&selectors.EVENT_WRITE:
-                        try:n=os.write(fd,input_bytes[sent:sent+65536])
-                        except BlockingIOError:continue
-                        except OSError as e:
-                            f['primary']=f['primary'] or 'stdin '+str(e.errno);sel.unregister(fd);proc.stdin.close();continue
-                        sent+=n
-                        if sent==len(input_bytes):sel.unregister(fd);proc.stdin.close();f['stdin_complete']=True
-                    else:
-                        try:block=os.read(fd,65536)
-                        except BlockingIOError:continue
-                        except OSError as e:f['primary']=f['primary'] or 'read '+str(e.errno);block=b''
-                        name=streams[fd]
-                        if not block:
-                            sel.unregister(fd);f[name+'_eof']=True;continue
-                        self.charge('raw' if raw and name=='stdout' else 'runner' if raw else 'compile',len(block))
-                        chunks[name].extend(block)
-                if not f['reaped']:
-                    try:got,status=os.waitpid(pid,os.WNOHANG)
-                    except ChildProcessError:
-                        f['primary']=f['primary'] or 'lost original reap';raise Refusal('ECHILD is not reap proof')
-                    if got:
-                        require(got==pid,'only original child reap')
-                        # Publish truth BEFORE any later deadline/status admission.
-                        f['reaped']=True;f['reaped_pid']=got;f['exit_code']=os.waitstatus_to_exitcode(status)
-                        proc.returncode=f['exit_code']
-            f['group']=self.group_state(pid) # no mutating post-reap signal.
+            self.step('tool-role',lambda:self.b.tool(argv[0],self.plan),work)
+            def acquire_observer():
+                owned['observer']=self.b.prepare(self.plan);return owned['observer']
+            observer=self.step('prepare-fixed-observer',acquire_observer,work)
+            environment=dict(self.plan['environment'])
+            require('HOME' not in environment and environment.get('LC_ALL')=='C','closed reviewed environment')
+            environment['TMPDIR']=str(self.root/(label+'-tmp'))
+            environment['CLANG_MODULE_CACHE_PATH']=str(self.root/(label+'-cache'));f['environment']=environment
+            self.step('child-owned-tmp',lambda:self.b.mkdir(environment['TMPDIR']),work)
+            self.step('child-owned-cache',lambda:self.b.mkdir(environment['CLANG_MODULE_CACHE_PATH']),work)
+            def acquire():
+                owned['process']=self.b.spawn(argv,environment);return owned['process']
+            self.step('spawn-original',acquire,work)
+            proc=owned['process'];f['pid']=proc.pid;require(integer(f['pid'],2,2**31-1),'valid original PID')
+            def acquire_selector():
+                owned['selector']=self.b.selector();return owned['selector']
+            self.step('selector-create',acquire_selector,work)
+            for name in ('stdout','stderr','stdin'):
+                pipe=getattr(proc,name)
+                self.step('nonblocking:'+name,lambda p=pipe:self.b.nonblocking(p),work)
+                if name=='stdin' and not input_bytes:close_pipe(name);f['stdin_complete']=True;continue
+                events=selectors.EVENT_WRITE if name=='stdin' else selectors.EVENT_READ
+                self.step('register:'+name,lambda p=pipe,e=events:self.b.register(owned['selector'],p,e),work)
+                pending[pipe]=name
+            drain(work)
+        except BaseException as e:fault(e)
+        # All acquisition/setup/IO failures flow through this same ownership path.
+        if owned['process'] is not None:
+            if f['pid'] is None:
+                try:f['pid']=owned['process'].pid
+                except BaseException as e:f['anchor_lost']=True;fault(e)
+            try:
+                if observer is not None and not f['anchor_lost'] and not f['reaped']:closure()
+                else:raise Refusal('no eligible original anchor for cleanup')
+            except BaseException as e:fault(e)
+            if f['reaped'] and pending and owned['selector'] is not None:
+                try:drain(hard)
+                except BaseException as e:fault(e)
+            for name in ('stdin','stdout','stderr'):
+                if name in owned['closed'] or name in owned['close_attempted']:continue
+                try:close_pipe(name)
+                except BaseException as e:fault(e)
+        if owned['selector'] is not None:
+            try:
+                def selector_close():
+                    owned['close_attempted'].add('selector');self.b.selectorclose(owned['selector']);owned['closed'].add('selector')
+                self.step('selector-close',selector_close,hard)
+            except BaseException as e:fault(e)
+        self.stamp(f,start)
+        owned['chunks']=chunks
+        f['captured_streams']={name:{'bytes':len(data),'sha256':digest(data)} for name,data in chunks.items()}
+        unresolved=(owned['process'] is not None and
+                    (not f['reaped'] or f['group']!='ABSENT_ESRCH' or
+                     not {'stdin','stdout','stderr'}<=owned['closed'])) or (
+                    owned['selector'] is not None and 'selector' not in owned['closed'])
+        f['retained_unresolved']=bool(unresolved)
+        if unresolved:UNRESOLVED_HANDLES.append(owned)
+        try:
+            # Every child log/receipt substep retains its ORIGINAL hard cutoff.
+            self.write(label+'.stdout.bin',bytes(chunks['stdout']),cutoff=hard)
+            self.write(label+'.stderr.bin',bytes(chunks['stderr']),cutoff=hard)
+            f['persistence']='LOGS_CLOSED'
+            self.stamp(f,start)
+            self.write(label+'.receipt.json',encoded(f),'driver',cutoff=hard)
+            # The durable child receipt is explicitly a candidate. Final admission
+            # after its close is in the outer ledger; it cannot self-attest its
+            # own fsync/close time. No candidate presence implies admission.
+            f['persistence']='CANDIDATE_RECEIPT_CLOSED';self.stamp(f,start)
+            terminal_gate(f)
+            require(not f['retained_unresolved'],'all owned handles resolved')
+            self.check(hard);f['admitted_at']=self.b.now();return bytes(chunks['stdout'])
         except BaseException as e:
-            f['primary']=f['primary'] or type(e).__name__+': '+str(e)
-            stop_group(signal.SIGKILL)
-            while not f['reaped'] and time.monotonic()<hard:
-                try:got,status=os.waitpid(pid,os.WNOHANG)
-                except ChildProcessError:break
-                if got==pid:
-                    f['reaped']=True;f['reaped_pid']=got;f['exit_code']=os.waitstatus_to_exitcode(status);proc.returncode=f['exit_code']
-                else:time.sleep(0.005)
-            if f['reaped']:f['group']=self.group_state(pid)
-        finally:
-            sel.close()
-            for pipe in (proc.stdin,proc.stdout,proc.stderr):
-                try:pipe.close()
-                except OSError as e:f['secondary'].append('pipe close '+str(e.errno))
-        f['elapsed']=time.monotonic()-start;f['whole_elapsed']=time.monotonic()-self.started;f['capture']=self.captured
-        f['signals']=signals;f['argv']=argv;self.records.append(f)
-        # Bytes already charged on capture; persistence must not charge twice.
-        self.write(label+'.stdout.bin',bytes(chunks['stdout']))
-        self.write(label+'.stderr.bin',bytes(chunks['stderr']))
-        self.write(label+'.receipt.json',encoded(f),'driver')
-        f['elapsed']=time.monotonic()-start;f['whole_elapsed']=time.monotonic()-self.started
-        terminal_gate(f);self.check()
-        return bytes(chunks['stdout'])
-
-def parse_su(text,source_hashes):
+            fault(e);self.stamp(f,start)
+            UNRESOLVED_HANDLES.append(owned) # also preserve unpersisted captured bytes.
+            raise Refusal('child refused; original receipt/handles retained') from e
+
+
+def verify_definition(symbol,definition):
+    d=definition
+    require(d['accepted_by']=='MAIN' and d['symbol']==symbol,'independently qualified definition symbol')
+    data=read_bytes(d['source'],ARTIFACTS);require(digest(data)==d['source_sha256'],'definition source identity')
+    lines=data.splitlines(keepends=True)
+    require(integer(d['line'],1,len(lines)) and integer(d['end_line'],d['line'],len(lines)),'complete definition span')
+    span=b''.join(lines[d['line']-1:d['end_line']])
+    require(digest(span)==d['span_sha256'] and type(d['signature']) is str
+            and d['signature'].encode() in span and b'{' in span and b'}' in span,'exact reviewed definition bytes/signature/body')
+    require(file_record(d['evidence'])['sha256']==d['evidence_sha256'],'independent symbol-to-definition qualification')
+    return d
+
+def parse_su(text,source_hashes,definitions):
     result={}
     for line in text.splitlines():
         parts=line.split('\t');require(len(parts)==3,'complete SU record')
@@ -258,11 +594,16 @@
         path,number,_,symbol=match.groups()
         path=str(Path(path).resolve());require(number.isdecimal() and path in source_hashes,'source-bound SU role')
         require(symbol not in result,'unambiguous SU symbol')
-        result[symbol]=dict(bytes=int(count),source=path,line=int(number),sha256=source_hashes[path])
+        require(symbol in definitions,'no numeric-line-only SU ownership')
+        d=verify_definition(symbol,definitions[symbol])
+        require(path==d['source'] and d['line']<=int(number)<=d['end_line']
+                and source_hashes[path]==d['source_sha256'],'SU inside exact qualified definition')
+        result[symbol]=dict(bytes=int(count),source=path,line=int(number),sha256=source_hashes[path],
+                            span_sha256=d['span_sha256'],definition_start=d['line'],definition_end=d['end_line'])
     return result
 
 def assembly_graph(text,frames,native):
-    edges={name:set() for name in frames};current=None;code=False
+    edges={};current=None;code=False
     def norm(s):return s[1:] if native and s.startswith('_') else s
     for line in text.splitlines():
         if re.search(r'^\s*\.text\b|^\s*\.section\s+.*(?:__text|\.text)',line):code=True
@@ -270,7 +611,8 @@
         m=re.match(r'^([A-Za-z_.$][\w.$]*):',line)
         if code and m:
             name=norm(m.group(1))
-            if name in frames:current=name
+            if name in frames:
+                require(name not in edges,'unique emitted definition');current=name;edges[name]=set()
             elif not name.startswith(('L','.L')):raise Refusal('defined function lacks SU '+name)
         if not current:continue
         if re.search(r'\b(?:blr|call_indirect|return_call_indirect)\b',line):raise Refusal('indirect normal edge')
@@ -280,7 +622,45 @@
             name=norm(m.group(1))
             if not name.startswith(('L','.L')):edges[current].add(name)
         if re.search(r'\.cfi_endproc|end_function|\.endfunc',line):current=None
+    require(set(edges)==set(frames),'every SU definition has an actual emitted body')
     return edges
+
+def assembly_bodies(text,frames,native):
+    """Saved NORMAL producer assembly versus separately emitted diagnostic bodies."""
+    bodies={};current=None;local={};file_ids={};locations={};code=False
+    for raw in text.splitlines():
+        line=raw.split('//',1)[0].strip() if native else raw.split('#',1)[0].strip()
+        if re.match(r'\.text\b|\.section\s+.*(?:__text|\.text)',line):code=True
+        elif line.startswith('.section'):code=False;current=None
+        m=re.match(r'\.file\s+(\d+)\s+"([^"]+)"(?:\s+"([^"]+)")?',line)
+        if m:
+            path=Path(m[2])/m[3] if m[3] else Path(m[2]);file_ids[int(m[1])]=str(path.resolve());continue
+        m=re.match(r'([A-Za-z_.$][\w.$]*):',line)
+        if code and m:
+            name=m[1][1:] if native and m[1].startswith('_') else m[1]
+            if name in frames:
+                require(name not in bodies,'one normal body per definition')
+                current=name;bodies[name]=[];locations[name]=[];local={}
+        if current is None:continue
+        if line.startswith('.loc'):
+            loc=re.match(r'\.loc\s+(\d+)\s+(\d+)',line);require(loc is not None,'qualified location syntax')
+            fid,number=int(loc[1]),int(loc[2]);require(fid in file_ids,'location source role')
+            locations[current].append((file_ids[fid],number));continue
+        if line.startswith(('.file','.type','.size','.globl','.hidden','.p2align','.functype')):continue
+        # Local block IDs may change across output stems; preserve their complete
+        # per-function reference/definition structure with deterministic renaming.
+        def rename(match):
+            key=match[0]
+            if key not in local:local[key]='LOCAL'+str(len(local))
+            return local[key]
+        line=re.sub(r'(?<![\w.$])(?:\.L|L)(?:BB|tmp|func|loh|CPI)[\w.$]*',rename,line)
+        if line:bodies[current].append(line)
+        if re.search(r'\.cfi_endproc|end_function|\.endfunc',line):current=None
+    require(set(bodies)==set(frames),'complete normal/diagnostic body union')
+    for name,frame in frames.items():
+        require(any(p==frame['source'] and frame['definition_start']<=n<=frame['definition_end']
+                    for p,n in locations[name]),'actual body location in qualified definition')
+    return {n:{'body':v,'sha256':digest(encoded(v)),'locations':locations[n]} for n,v in bodies.items()}
 
 class WasmReader:
     def __init__(self,data):self.data=data;self.at=0
@@ -298,9 +678,53 @@
         n=self.leb();require(n<=4096,'Wasm name bound');return self.take(n).decode('utf-8')
     def done(self):require(self.at==len(self.data),'complete Wasm section')
 
+WASM_OPS={0:'unreachable',1:'nop',2:'block',3:'loop',4:'if',5:'else',11:'end',12:'br',13:'br_if',
+          14:'br_table',15:'return',16:'call',18:'return_call',26:'drop',27:'select',
+          32:'local.get',33:'local.set',34:'local.tee',35:'global.get',36:'global.set',
+          63:'memory.size',64:'memory.grow',65:'i32.const',66:'i64.const'}
+for _base,_names in (
+ (0x28,'i32.load i64.load f32.load f64.load i32.load8_s i32.load8_u i32.load16_s i32.load16_u i64.load8_s i64.load8_u i64.load16_s i64.load16_u i64.load32_s i64.load32_u i32.store i64.store f32.store f64.store i32.store8 i32.store16 i64.store8 i64.store16 i64.store32'),
+ (0x45,'i32.eqz i32.eq i32.ne i32.lt_s i32.lt_u i32.gt_s i32.gt_u i32.le_s i32.le_u i32.ge_s i32.ge_u i64.eqz i64.eq i64.ne i64.lt_s i64.lt_u i64.gt_s i64.gt_u i64.le_s i64.le_u i64.ge_s i64.ge_u'),
+ (0x67,'i32.clz i32.ctz i32.popcnt i32.add i32.sub i32.mul i32.div_s i32.div_u i32.rem_s i32.rem_u i32.and i32.or i32.xor i32.shl i32.shr_s i32.shr_u i32.rotl i32.rotr i64.clz i64.ctz i64.popcnt i64.add i64.sub i64.mul i64.div_s i64.div_u i64.rem_s i64.rem_u i64.and i64.or i64.xor i64.shl i64.shr_s i64.shr_u i64.rotl i64.rotr'),
+ (0xa7,'i32.wrap_i64 i32.trunc_f32_s i32.trunc_f32_u i32.trunc_f64_s i32.trunc_f64_u i64.extend_i32_s i64.extend_i32_u i64.trunc_f32_s i64.trunc_f32_u i64.trunc_f64_s i64.trunc_f64_u')):
+    for _index,_name in enumerate(_names.split()):WASM_OPS[_base+_index]=_name
+WASM_OPS.update({0xc0:'i32.extend8_s',0xc1:'i32.extend16_s',0xc2:'i64.extend8_s',0xc3:'i64.extend16_s',0xc4:'i64.extend32_s'})
+
+def wasm_assembly_instructions(body):
+    instructions=[];locals_found=[]
+    reverse={name:op for op,name in WASM_OPS.items()}
+    widths={'i32':0x7f,'i64':0x7e,'f32':0x7d,'f64':0x7c}
+    for line in body:
+        if line.endswith(':'):continue
+        if line.startswith('.local'):
+            for name in line.split(None,1)[1].replace(',',' ').split():
+                require(name in widths,'declared assembly local type');locals_found.append(widths[name])
+            continue
+        if line.startswith('.'):continue
+        parts=line.split(None,1);name=parts[0];text=parts[1].strip() if len(parts)>1 else ''
+        if name in ('end_block','end_loop','end_if','end_function'):name='end'
+        require(name in reverse,'qualified normal assembly opcode '+name);op=reverse[name]
+        if op in (2,3,4):
+            require(text in ('','i32','i64','f32','f64'),'qualified block signature')
+            args=[{'':-64,'i32':-1,'i64':-2,'f32':-3,'f64':-4}[text]]
+        elif op in (16,18,35,36):args=[text]
+        elif op in (12,13,14,32,33,34,65,66):
+            values=text.replace('$','').replace(',',' ').replace('{',' ').replace('}',' ').split()
+            args=[int(v,0) for v in values]
+        elif 0x28<=op<=0x3e:
+            match=re.fullmatch(r'(\d+)(?::p2align=(\d+))?',text);require(match is not None,'normal memory operand')
+            natural=3 if name.startswith(('i64.load','i64.store','f64.')) else 2
+            if '8' in name:natural=0
+            elif '16' in name:natural=1
+            elif '32' in name and name.startswith('i64'):natural=2
+            args=[int(match[2]) if match[2] else natural,int(match[1])]
+        else:require(not text,'zero operand instruction');args=[]
+        instructions.append([name,args])
+    return instructions,locals_found
+
 def wasm_module(data):
     r=WasmReader(data);require(r.take(8)==b'\0asm\1\0\0\0','Wasm header')
-    types=[];functions=[];names={};exports={};bodies=[];seen=set();imports=0
+    types=[];functions=[];names={};global_names={};exports={};bodies=[];seen=set();imports=0;initialization=[]
     while r.at<len(data):
         tag=r.byte();s=WasmReader(r.take(r.leb()))
         if tag:require(tag not in seen,'duplicate Wasm section');seen.add(tag)
@@ -309,10 +733,11 @@
             if name=='name':
                 while s.at<len(s.data):
                     sub=s.byte();z=WasmReader(s.take(s.leb()))
-                    if sub==1:
+                    if sub in (1,7):
                         count=z.leb();require(count<=1024,'function name count')
                         for _ in range(count):
-                            i=z.leb();n=z.name();require(i not in names,'duplicate function name');names[i]=n
+                            i=z.leb();n=z.name();table=names if sub==1 else global_names
+                            require(i not in table,'duplicate function/global name');table[i]=n
                         z.done()
             else:s.take(len(s.data)-s.at)
         elif tag==1:
@@ -326,59 +751,83 @@
         elif tag==2:imports=s.leb();require(imports==0,'import-free module')
         elif tag==3:
             n=s.leb();require(n<=1024,'defined function bound');functions=[s.leb() for _ in range(n)]
+        elif tag==5:
+            require(s.leb()==1 and s.leb()==1 and s.leb()==4 and s.leb()==4,'fixed bounded memory declaration')
+        elif tag==6:
+            count=s.leb();require(count<=64,'bounded constant global initializers')
+            for index in range(count):
+                typ,mutable,op=s.byte(),s.byte(),s.byte()
+                require(mutable in (0,1) and (typ,op) in ((0x7f,0x41),(0x7e,0x42)),'static integer global initializer only')
+                value=s.leb(signed=True,maxbytes=5 if typ==0x7f else 10);require(s.byte()==11,'closed constant expression')
+                initialization.append({'global':index,'type':typ,'mutable':mutable,'value':value})
+        elif tag==8:raise Refusal('unqualified Wasm start/initializer function')
+        elif tag==9:raise Refusal('unqualified Wasm element/function-pointer initialization')
         elif tag==7:
             n=s.leb();require(n<=16,'export count')
             for _ in range(n):
                 name=s.name();kind=s.byte();index=s.leb();require(name not in exports,'unique export');exports[name]=(kind,index)
         elif tag==10:
             n=s.leb();require(n<=1024,'code count');bodies=[s.take(s.leb()) for _ in range(n)]
+        elif tag==11:
+            count=s.leb();require(count<=128,'bounded active data initializers')
+            for index in range(count):
+                require(s.leb()==0 and s.byte()==0x41,'memory0 constant active segment only')
+                offset=s.leb(signed=True);require(s.byte()==11,'closed data offset expression')
+                payload=s.take(s.leb());require(0<=offset<=262144 and len(payload)<=262144-offset,'bounded static data extent')
+                initialization.append({'data':index,'offset':offset,'bytes':len(payload),'sha256':digest(payload)})
         else:s.take(len(s.data)-s.at) # non-code section bytes remain in pinned module.
         s.done()
-    require(imports==0 and set(exports)==EXPORTS,'exact module exports/imports')
+    require(imports==0 and set(exports)==EXPORTS and exports['memory']==(2,0),'exact module exports/imports')
     require(len(functions)==len(bodies) and set(names)==set(range(len(functions))),'complete linked name/function join')
     nodes={};width={0x7f:4,0x7e:8,0x7d:4,0x7c:8}
     for i,(typeid,body) in enumerate(zip(functions,bodies)):
         require(typeid<len(types),'valid function type index');b=WasmReader(body)
-        n=b.leb();require(n<=4096,'local group bound');locals_bytes=sum(width[t] for t in types[typeid][0]);calls=[]
+        n=b.leb();require(n<=4096,'local group bound');locals_bytes=sum(width[t] for t in types[typeid][0]);calls=[];local_types=[];instructions=[]
         for _ in range(n):
-            count=b.leb();t=b.byte();require(t in width and count<=65536,'declared local bound');locals_bytes+=count*width[t]
+            count=b.leb();t=b.byte();require(t in width and count<=65536,'declared local bound');locals_bytes+=count*width[t];local_types.extend([t]*count)
         while b.at<len(body):
-            op=b.byte()
-            if op in (0x02,0x03,0x04):b.leb(signed=True)
-            elif op in (0x0c,0x0d,0x20,0x21,0x22,0x23,0x24):b.leb()
+            op=b.byte();args=[]
+            if op in (0x02,0x03,0x04):args=[b.leb(signed=True)]
+            elif op in (0x0c,0x0d,0x20,0x21,0x22):args=[b.leb()]
+            elif op in (0x23,0x24):
+                index=b.leb();require(index in global_names,'named linked global operand');args=[global_names[index]]
             elif op==0x0e:
                 count=b.leb();require(count<=4096,'branch table bound')
-                for _ in range(count+1):b.leb()
-            elif op in (0x10,0x12):calls.append(b.leb())
+                args=[b.leb() for _ in range(count+1)]
+            elif op in (0x10,0x12):
+                index=b.leb();calls.append(index);require(index in names,'named linked call operand');args=[names[index]]
             elif op in (0x11,0x13):raise Refusal('linked indirect call')
-            elif 0x28<=op<=0x3e:b.leb();b.leb()
+            elif 0x28<=op<=0x3e:args=[b.leb(),b.leb()]
             elif op in (0x3f,0x40):require(b.byte()==0,'MVP memory index')
-            elif op==0x41:b.leb(signed=True)
-            elif op==0x42:b.leb(signed=True,maxbytes=10)
-            elif op==0x43:b.take(4)
-            elif op==0x44:b.take(8)
+            elif op==0x41:args=[b.leb(signed=True)]
+            elif op==0x42:args=[b.leb(signed=True,maxbytes=10)]
+            elif op in (0x43,0x44):raise Refusal('unqualified floating constant correspondence')
             elif op==0xfc:
                 sub=b.leb()
-                if sub==10:require(b.byte()==0 and b.byte()==0,'memory.copy indexes')
-                elif sub==11:require(b.byte()==0,'memory.fill index')
-                elif sub>7:raise Refusal('unqualified extended opcode')
+                raise Refusal('unqualified extended body correspondence '+str(sub))
             elif not (op in (0x00,0x01,0x05,0x0b,0x0f,0x1a,0x1b) or 0x45<=op<=0xc4):
                 raise Refusal('unqualified linked opcode '+hex(op))
+            require(op in WASM_OPS,'qualified instruction spelling');instructions.append([WASM_OPS[op],args])
         require(body and body[-1]==0x0b,'complete function body')
         require(all(j<len(functions) for j in calls),'defined call indices')
         require(names[i] not in nodes,'unique linked symbol')
-        nodes[names[i]]={'locals':locals_bytes,'calls':set(names[j] for j in calls),'index':i}
-    return nodes,exports
+        nodes[names[i]]={'locals':locals_bytes,'calls':set(names[j] for j in calls),'index':i,
+                         'params':types[typeid][0],'returns':types[typeid][1],'local_types':local_types,'instructions':instructions,'body_sha256':digest(body)}
+    return nodes,exports,initialization
 
 def frame_gate(frames,edges,external,roots,full_root,locals_map=None):
     """Real SU/assembly/linked facts; no zero default for a missing role."""
     costs={name:f['bytes']+(locals_map or {}).get(name,0) for name,f in frames.items()}
     for name,f in external.items():
+        require(set(f)=={'accepted_by','scope','bytes','source','line','end_line','source_sha256',
+                        'span_sha256','signature','symbol','evidence','evidence_sha256','calls'},'closed external definition/call schema')
         require(name not in costs and f.get('accepted_by')=='MAIN' and f.get('scope')=='normal','qualified external role')
-        require(integer(f.get('bytes'),0,65536) and f.get('source') and f.get('line') and f.get('source_sha256'),'source-bound external cost')
-        require(file_record(f['source'])['sha256']==f['source_sha256'],'external definition identity')
+        require(integer(f.get('bytes'),0,65536),'bounded external frame')
+        verify_definition(name,f)
         require(file_record(f['evidence'])['sha256']==f['evidence_sha256'],'external proof identity')
-        costs[name]=f['bytes'];edges[name]=set(f.get('calls',[]))
+        require(type(f['calls']) is list and all(type(n) is str and n for n in f['calls'])
+                and len(set(f['calls']))==len(f['calls']),'explicit complete transitive calls; no omitted leaf')
+        costs[name]=f['bytes'];edges[name]=set(f['calls'])
     require(len(costs)<=2048,'frame graph bound')
     cache={}
     def walk(name,path):
@@ -457,62 +906,234 @@
             'adopted_entry_ceilings':{'loops':256,'scalar':4096},
             'obligation':'MAIN line-by-line source review; not runtime counters or emitted-cost evidence'}
 
+class FakePipe:
+    def __init__(self,name):self.name=name;self.closed=False
+
+class FakeProcess:
+    def __init__(self,pid=123):
+        self.pid=pid;self.returncode=None
+        self.stdin=FakePipe('stdin');self.stdout=FakePipe('stdout');self.stderr=FakePipe('stderr')
+
+class FakeInfo:pass
+
+class FakeNative:
+    def __init__(self,b):
+        self.b=b;self.widths=[4,4,8,8,8];self.signs=[-1,0xffffffff,0xffffffffffffffff];self.layout=[8,8,104,8]
+        self.offsets={'signo':0,'error':4,'code':8,'pid':12,'uid':16,'status':20,'addr':24,'value':32,'band':40,'pad':48}
+        if b.scenario=='adapter-width':self.widths[0]=8
+        if b.scenario=='adapter-sign':self.signs[0]=0xffffffff
+        if b.scenario=='adapter-layout':self.layout[2]=128
+        if b.scenario=='adapter-offset':self.offsets['pid']=16
+    def zero(self):
+        info=FakeInfo()
+        for key in self.offsets:setattr(info,key,0)
+        return info
+    def wait(self,idtype,pid,info,flags):
+        self.b.event('native-wait')
+        require(idtype==1 and flags==37 and pid==123,'fixed injected native selector')
+        require(all(getattr(info,key)==0 for key in self.offsets),'zero whole fake record every call/retry')
+        if self.b.scenario=='adapter-ECHILD':self.last_errno=errno.ECHILD;return -1
+        if self.b.scenario=='adapter-EINTRdeadline':
+            self.b.time+=1;self.last_errno=errno.EINTR;return -1
+        if self.b.scenario=='adapter-noevent' and not self.b.signals:return 0
+        info.pid=124 if self.b.scenario=='adapter-identity' else pid
+        info.signo=signal.SIGCHLD;info.code=2 if self.b.scenario in ('adapter-signal','adapter-noevent') else 99 if self.b.scenario=='adapter-code' else 1
+        info.status=9 if self.b.scenario in ('adapter-signal','adapter-noevent') else 0;return 0
+    def error(self):return self.last_errno
+
+class FakeBoundary:
+    """No filesystem/process/FFI. Drives the SAME Job.run/write methods."""
+    def __init__(self,scenario,write_only=False):
+        self.scenario=scenario;self.time=0.0;self.events=[];self.fired=False;self.proc=None
+        self.pending={};self.files={};self.fds={};self.nextfd=10;self.observe_count=0
+        self.signals=[];self.reaps=[];self.pre_group=True;self.write_only=write_only
+        self.closed=[];self.payload_done=False
+    def now(self):return self.time
+    def event(self,name):
+        self.events.append((name,self.time));self.time+=0.001
+        trigger=self.scenario.split(':',1)[1] if ':' in self.scenario else ''
+        if not self.fired and name==trigger:
+            self.fired=True
+            if self.scenario.startswith('error:'):raise OSError(errno.EIO,'injected '+name)
+            if self.scenario.startswith('late:'):self.time+=61 if not self.write_only else 11
+            if self.scenario.startswith('worklate:'):self.time+=59
+            if self.scenario.startswith('wholelate:'):self.time=301
+    def prepare(self,plan):
+        self.event('prepare')
+        return observer_protocol(FakeNative(self),self.now) if self.scenario.startswith('adapter-') else self.observe
+    def tool(self,path,plan):self.event('tool')
+    def mkdir(self,path):self.event('mkdir')
+    def open(self,path):
+        self.event('open');name=str(path);require(name not in self.files,'fake exclusive output')
+        self.nextfd+=1;self.fds[self.nextfd]=name;self.files[name]=bytearray();return self.nextfd
+    def chmod(self,fd):self.event('chmod')
+    def write(self,fd,data):
+        self.event('write')
+        if self.scenario=='zero-write':return 0
+        if self.scenario=='bad-write':return len(data)+1
+        n=min(2,len(data)) if self.scenario in ('short-write','short-persistence') else len(data)
+        self.files[self.fds[fd]].extend(data[:n]);return n
+    def sync(self,fd):self.event('fsync')
+    def close(self,fd):
+        self.event('fileclose');require(fd not in self.closed,'no ambiguous close retry');self.closed.append(fd)
+    def spawn(self,argv,env):
+        self.event('spawn');self.proc=FakeProcess(0 if self.scenario=='invalid-pid' else 123)
+        if self.scenario=='cached-reap':self.proc.returncode=0
+        return self.proc
+    def selector(self):self.event('selector');return object()
+    def nonblocking(self,pipe):self.event('nonblocking-'+pipe.name)
+    def register(self,sel,pipe,events):self.event('register-'+pipe.name);self.pending[pipe]=events
+    def unregister(self,sel,pipe):self.event('unregister-'+pipe.name);del self.pending[pipe]
+    def select(self,sel,seconds):
+        self.event('select');return list(self.pending.items())
+    def readpipe(self,pipe):
+        self.event('read-'+pipe.name)
+        if self.scenario in ('payload','overflow','late:write','late:fsync','late:chmod','error:fileclose') and pipe.name=='stdout' and not self.payload_done:
+            self.payload_done=True;return b'x'*65536
+        return b''
+    def writepipe(self,pipe,data):
+        self.event('stdinwrite')
+        if self.scenario=='zero-stdin':return 0
+        if self.scenario=='bad-stdin':return len(data)+1
+        return min(2,len(data)) if self.scenario=='short-stdin' else len(data)
+    def pipeclose(self,pipe):
+        self.event('close-'+pipe.name);require(not pipe.closed,'pipe not closed twice');pipe.closed=True
+    def selectorclose(self,sel):self.event('selectorclose')
+    def pgid(self,pid):self.event('pgid');return 124 if self.scenario=='wrong-group' else pid
+    def sid(self,pid):self.event('sid');return 124 if self.scenario=='wrong-session' else pid
+    def observe(self,pid,hard):
+        self.event('observe');self.observe_count+=1
+        if self.scenario=='anchor-echild':raise ChildProcessError(errno.ECHILD,'injected ECHILD')
+        if self.scenario=='anchor-unknown':raise OSError(errno.EPERM,'injected unknown anchor')
+        if self.scenario=='loss-before-signal' and self.observe_count>=3:raise ChildProcessError(errno.ECHILD,'lost before signal')
+        if self.scenario=='bad-observer':return False
+        if self.scenario in ('nonzero','eperm-nonzero'):return 7
+        if self.scenario=='eperm-running':return None
+        if self.scenario=='running':return None if not self.signals else -9
+        return 0
+    def group(self,pid):
+        self.event('group-pre' if self.pre_group else 'group-post')
+        if self.pre_group:
+            self.pre_group=False
+            if self.scenario.startswith('eperm'):return 'UNKNOWN_EPERM'
+            if self.scenario=='pre-unknown':return 'UNKNOWN_OSERROR'
+            return 'PRESENT'
+        if self.scenario in ('post-present','eperm-post-present'):return 'PRESENT'
+        if self.scenario in ('post-eperm','eperm-post-eperm'):return 'UNKNOWN_EPERM'
+        return 'ABSENT_ESRCH'
+    def signal(self,pid):
+        self.event('signal');require(self.proc.returncode is None and not self.reaps,'signal only before original reap')
+        self.signals.append(pid)
+    def reap(self,pid):
+        self.event('reap')
+        if self.scenario=='reap-echild':raise ChildProcessError(errno.ECHILD,'lost original consuming wait')
+        self.reaps.append(pid)
+        status=-9 if (self.scenario in ('running','adapter-noevent') and self.signals) or self.scenario=='adapter-signal' else 7 if self.scenario in ('nonzero','eperm-nonzero') else 0
+        return (pid+1 if self.scenario=='wrong-reap' else pid,status)
+    def exitcode(self,status):return status
+    def pause(self,seconds):self.event('pause');self.time+=max(seconds,0.01)
+
+# Exactly64 supervisor cases +32 persistence cases =96; no extra target row.
+RUN_CONTROLS=(
+ ('ordinary','normal',True),('D260-noevent','eperm-running',False),('short-stdin','short-stdin',True),
+ ('payload','payload',True),('running-work-deadline','running',False),
+ ('selector-after-spawn','error:selector',False),('register-stdout','error:register-stdout',False),
+ ('register-stderr','error:register-stderr',False),('register-stdin','error:register-stdin',False),
+ ('initial-stdin-close','error:close-stdin',False),('adapter-width','adapter-width',False),
+ ('adapter-sign','adapter-sign',False),('adapter-layout','adapter-layout',False),
+ ('select-error','error:select',False),('late-selector-return','late:select',False),
+ ('late-work-selector','worklate:select',False),('stdin-write-error','error:stdinwrite',False),
+ ('late-stdin-write','late:stdinwrite',False),('zero-stdin','zero-stdin',False),('bad-stdin','bad-stdin',False),
+ ('adapter-offset','adapter-offset',False),('adapter-identity','adapter-identity',False),
+ ('adapter-ECHILD','adapter-ECHILD',False),('adapter-EINTRdeadline','adapter-EINTRdeadline',False),
+ ('unregister-stdout','error:unregister-stdout',False),('unregister-stderr','error:unregister-stderr',False),
+ ('unregister-stdin','error:unregister-stdin',False),('anchor-echild','anchor-echild',False),
+ ('anchor-unknown','anchor-unknown',False),('loss-immediately-before-signal','loss-before-signal',False),
+ ('wrong-group','wrong-group',False),('wrong-session','wrong-session',False),('cached-reap','cached-reap',False),
+ ('invalid-pid','invalid-pid',False),('terminal-leader-owned-descendant','descendant',True),
+ ('signal-failure','error:signal',False),('consuming-ECHILD','reap-echild',False),('wrong-consuming-pid','wrong-reap',False),
+ ('nonzero-terminal','nonzero',False),('post-present','post-present',False),('post-eperm','post-eperm',False),
+ ('D260-resolved','eperm-ok',True),('D260-post-present','eperm-post-present',False),
+ ('D260-post-eperm','eperm-post-eperm',False),('D260-nonzero','eperm-nonzero',False),
+ ('unknown-pre-group','pre-unknown',False),('late-spawn-acquisition','late:spawn',False),
+ ('late-selector-acquisition','late:selector',False),('late-reap-return','late:reap',False),
+ ('late-pre-group','late:group-pre',False),('late-post-group','late:group-post',False),
+ ('ambiguous-stdout-close','error:close-stdout',False),('ambiguous-stderr-close','error:close-stderr',False),
+ ('ambiguous-selector-close','error:selectorclose',False),('late-selector-close','late:selectorclose',False),
+ ('child-log-crosses60','late:write',False),('child-fsync-crosses60','late:fsync',False),
+ ('child-preclose-crosses60','late:chmod',False),('child-ambiguous-file-close','error:fileclose',False),
+ ('adapter-normal','adapter-normal',True),('adapter-signal','adapter-signal',False),
+ ('spawn-rejection','error:spawn',False),('adapter-noevent','adapter-noevent',False),
+ ('adapter-code','adapter-code',False))
+WRITE_CONTROLS=(
+ ('ordinary','normal',b'abc',True,False),('empty','normal',b'',True,False),
+ ('short','short-write',b'abcdef',True,False),('zero','zero-write',b'abc',False,False),
+ ('oversized-return','bad-write',b'abc',False,False),('open-error','error:open',b'a',False,False),
+ ('chmod-error','error:chmod',b'a',False,False),('write-error','error:write',b'a',False,False),
+ ('fsync-error','error:fsync',b'a',False,False),('ambiguous-close','error:fileclose',b'a',False,False),
+ ('late-open','late:open',b'a',False,False),('late-chmod','late:chmod',b'a',False,False),
+ ('late-write','late:write',b'a',False,False),('late-fsync-preclose','late:fsync',b'a',False,False),
+ ('late-close','late:fileclose',b'a',False,False),('whole-open','wholelate:open',b'a',False,False),
+ ('whole-chmod','wholelate:chmod',b'a',False,False),('whole-write','wholelate:write',b'a',False,False),
+ ('whole-fsync','wholelate:fsync',b'a',False,False),('whole-close','wholelate:fileclose',b'a',False,False),
+ ('expired-before-open','expired',b'a',False,False),('whole-expired','whole-expired',b'a',False,False),
+ ('traversal','normal',b'a',False,True),('absolute','normal',b'a',False,True),
+ ('nested','normal',b'a',False,True),('metadata-cap','metadata-cap',b'a',False,False),
+ ('capture-cap','capture-cap',b'a',False,False),('driver-cap','driver-cap',b'a',False,False),
+ ('empty-late-fsync','late:fsync',b'',False,False),
+ ('empty-ambiguous-close','error:fileclose',b'',False,False),
+ ('short-owned-byte-prefix','short-write',b'abcdefghij',True,False),
+ ('normal-original-whole','normal',b'a',True,False))
+
 def run_controls():
-    """Exactly96 future pure controller controls; no subprocess or SUT calls."""
-    results=[]
-    def control(name,fn,accept):
-        try:fn();observed=True
-        except Refusal:observed=False
-        require(observed==accept,'controller control '+name)
-        results.append({'name':name,'expected':'ADMIT' if accept else 'REFUSE','matched':True})
-    good=dict(pid=123,reaped=True,reaped_pid=123,exit_code=0,group='ABSENT_ESRCH',
-              stdin_complete=True,stdout_eof=True,stderr_eof=True,primary=None,secondary=[],
-              elapsed=1,whole_elapsed=2,capture=0)
-    control('terminal-good',lambda:terminal_gate(good),True)
-    changes=[('pid',0),('pid',-1),('pid',2**31),('pid',True),
-             ('reaped',False),('reaped',None),('reaped_pid',124),('reaped_pid',None),
-             ('exit_code',1),('exit_code',-9),('exit_code',None),('exit_code',False),
-             ('group','PRESENT'),('group','UNKNOWN_EPERM'),('group','UNKNOWN_OSERROR'),
-             ('stdin_complete',False),('stdout_eof',False),('stderr_eof',False),
-             ('primary','timeout'),('primary','write failed'),('secondary',['close failed']),
-             ('elapsed',-1),('elapsed',60.01),('elapsed',None),
-             ('whole_elapsed',-1),('whole_elapsed',300.01),('whole_elapsed',None),
-             ('capture',-1),('capture',CAPTURE+1),('capture',False),('capture',None)]
-    require(len(changes)==31,'terminal fixture count')
-    for i,(key,value) in enumerate(changes):
-        control('terminal-refuse-'+str(i+1),lambda k=key,v=value:terminal_gate(dict(good,**{k:v})),False)
-    # Sixteen golden-byte controls and sixteen masked representation controls.
-    for i,offset in enumerate((0,4,9,12,20,24,28,32,34,36,38,40,112,944,1520,1648)):
-        raw=bytearray(2048);raw[offset]=1
-        control('golden-byte-'+str(i+1),lambda b=bytes(raw):compare_row({'id':1,'op':1},b,bytes(2048),bytes([1])*2048),False)
-    for op,okay in ((1,0),(2,0),(3,0),(3,1)):
-        for label,offset in (('source',240),('payload',560),('descriptor',848),('guard',1296)):
-            raw=bytearray(2048);raw[9]=okay;raw[offset]=1
-            # Successful decode may change its native output; this one is admitted.
-            accept=op==3 and okay==1 and label=='source'
-            control('masked-'+str(op)+'-'+str(okay)+'-'+label,
-                    lambda b=bytes(raw),o=op:compare_row({'id':1,'op':o},b,bytes(2048),bytes(2048)),accept)
-    # Eight admitted frame boundary/locals profiles;24 distinct bad graphs.
-    for value in (0,1,255,256,2048,4095,4096,65536):
-        frames={'codec':{'bytes':min(value,4096)},'caller':{'bytes':max(0,value-4096)}}
-        control('frame-boundary-'+str(value),lambda f=frames:frame_gate(f,{'codec':set(),'caller':{'codec'}},{},('codec',),'caller'),True)
-    for i in range(8):
-        frames={'codec':{'bytes':4097+i},'caller':{'bytes':1}}
-        control('codec-over-'+str(i),lambda f=frames:frame_gate(f,{'codec':set(),'caller':{'codec'}},{},('codec',),'caller'),False)
-    for i in range(8):
-        frames={'codec':{'bytes':1},'caller':{'bytes':65536+i}}
-        control('caller-over-'+str(i),lambda f=frames:frame_gate(f,{'codec':set(),'caller':{'codec'}},{},('codec',),'caller'),False)
-    bad=[({'codec':{'bytes':0}}, {'codec':{'missing'}}),
-         ({'codec':{'bytes':0}}, {'codec':{'codec'}}),
-         ({'codec':{'bytes':0},'a':{'bytes':0}}, {'codec':{'a'},'a':{'codec'}}),
-         ({'codec':{'bytes':0}}, {}),
-         ({}, {'codec':set()}),
-         ({'codec':{'bytes':0},'a':{'bytes':0}}, {'codec':{'a'}}),
-         ({'codec':{'bytes':4096},'a':{'bytes':1}}, {'codec':{'a'},'a':set()}),
-         ({'codec':{'bytes':4096}}, {'codec':{'unqualified-libcall'}})]
-    for i,(frames,edges) in enumerate(bad):
-        control('frame-graph-'+str(i),lambda f=frames,e=edges:frame_gate(f,e,{},('codec',),'codec'),False)
-    require(len(results)==96,'exact controller-control count');return results
+    """Future catalog only: inject fake boundaries BEFORE calling actual methods."""
+    require(len(RUN_CONTROLS)==64 and len(WRITE_CONTROLS)==32,'literal96 control map')
+    results=[];baseline_retained=len(UNRESOLVED_HANDLES)
+    def finish(name,okay,expected,job,b):
+        require(okay==expected,'control admission '+name)
+        require(all(a['started']<a['cutoff'] for a in job.actions),'no step starts at/after cutoff '+name)
+        # Signal events must have a fresh successful nonreaping observation, and
+        # no preceding consuming reap. Lost/ECHILD/unknown cases never signal.
+        if b.scenario in ('anchor-echild','anchor-unknown','loss-before-signal','wrong-group','wrong-session',
+                          'cached-reap','invalid-pid','bad-observer','adapter-identity','adapter-ECHILD','adapter-code','adapter-EINTRdeadline'):
+            require(not b.signals,'lost ownership cannot authorize signal')
+        if b.scenario.startswith('eperm'):require(not b.signals,'D260 is nonmutating deferral')
+        if b.proc is not None and any(a['name']=='spawn-original' and a['returned'] for a in job.actions):
+            require(job.owned[0]['kind']=='child' and job.owned[0]['process'] is b.proc,'original acquired handle retained')
+        for write in job.writes:
+            if write['error'] is not None and not write['closed']:
+                require(any(o.get('receipt') is write for o in UNRESOLVED_HANDLES),'unresolved FD retained')
+        results.append({'name':name,'expected':'ADMIT' if expected else 'REFUSE','matched':True,
+                        'method':'Job.run' if name.startswith('run/') else 'Job.write'})
+    for name,scenario,expected in RUN_CONTROLS:
+        b=FakeBoundary(scenario);job=Job(Path('/FAKE_MR'),0,{'environment':{'LC_ALL':'C'}},b,reserve=False)
+        okay=True
+        try:job.run('control',['FAKE_TOOL'],b'abcdef' if name in (
+            'input','short-stdin','register-stdin','stdin-write-error','late-stdin-write',
+            'zero-stdin','bad-stdin','unregister-stdin') else b'')
+        except Refusal:okay=False
+        finish('run/'+name,okay,expected,job,b)
+        if scenario=='descendant':
+            require(b.signals==[123] and b.reaps==[123],'owned descendant killed before consuming leader')
+            names=[n for n,_ in b.events];require(names.index('signal')<names.index('reap'),'pre-reap group cleanup')
+    for index,(name,scenario,data,expected,badpath) in enumerate(WRITE_CONTROLS):
+        b=FakeBoundary(scenario,write_only=True);job=Job(Path('/FAKE_MR'),0,{},b,reserve=False)
+        if scenario=='expired':b.time=10
+        if scenario=='whole-expired':b.time=300
+        if scenario=='metadata-cap':job.metadata=METADATA
+        if scenario=='capture-cap':job.captured=CAPTURE
+        if scenario=='driver-cap':job.categories['driver']=job.limits['driver']
+        path=('../escape','/absolute','nested/path')[index-22] if badpath else 'control.bin'
+        okay=True
+        try:job.write(path,data,'driver' if scenario in ('capture-cap','driver-cap') else None,
+                      cutoff=None if name.startswith('whole') or name=='normal-original-whole' else 10)
+        except (Refusal,OSError):okay=False
+        finish('write/'+name,okay,expected,job,b)
+    require(len(results)==96,'exact controls')
+    # Only fake in-memory handles; discard after assertions, never real release.
+    del UNRESOLVED_HANDLES[baseline_retained:]
+    return results
+
 
 def build_steps(plan,root):
     """Fixed ten-child shape. Tools/sysroot/link facts are separate MAIN inputs."""
@@ -520,14 +1141,14 @@
     require(set(p['tool_roles'])=={'native_cxx','wasm_cxx','wasm_ld','node'},'four exact tool roles')
     for target in ('native','wasm'):
         compiler=p['tool_roles'][target+'_cxx']
-        common=['-std=c++17','-O0','-fno-inline','-fno-exceptions','-fno-rtti','-fno-stack-protector',
+        common=['-std=c++17','-O0','-gline-tables-only','-fno-inline','-fno-exceptions','-fno-rtti','-fno-stack-protector',
                 '-fno-builtin','-fno-omit-frame-pointer','-fstack-usage','-I'+str(ROOT/'source/outbreak')]
         if target=='native':common+=['-target','arm64-apple-macos13','-DMR_NATIVE','-isysroot',p['native_sysroot']]
         else:common+=['--target=wasm32-unknown-unknown','-nostdlib']
         objects=[]
         for unit,source in (('record',ROOT/SOURCES[1]),('wrapper',HERE/'wrapper.cpp')):
-            stem=root/(target+'-'+unit);objects.append(str(stem)+'.o')
-            steps.append((target+'-'+unit+'-object',[compiler,*common,'-MD','-MF',str(stem)+'.d','-c',str(source),'-o',str(stem)+'.o']))
+            stem=root/(target+'-'+unit+'-normal');objects.append(str(stem)+'.o')
+            steps.append((target+'-'+unit+'-object',[compiler,*common,'-save-temps=obj','-MD','-MF',str(stem)+'.d','-c',str(source),'-o',str(stem)+'.o']))
         if target=='native':
             link=[compiler,'-target','arm64-apple-macos13','-isysroot',p['native_sysroot'],*objects,'-o',str(root/'native-runner')]
         else:
@@ -536,21 +1157,157 @@
                   *objects,'-o',str(root/'record.wasm')]
         steps.append((target+'-link',link))
         for unit,source in (('record',ROOT/SOURCES[1]),('wrapper',HERE/'wrapper.cpp')):
-            steps.append((target+'-'+unit+'-assembly',[compiler,*common,'-S',str(source),'-o',str(root/(target+'-'+unit+'.s'))]))
+            stem=root/(target+'-'+unit+'-diagnostic')
+            steps.append((target+'-'+unit+'-assembly',[compiler,*common,'-MD','-MF',str(stem)+'.d','-S',str(source),'-o',str(stem)+'.s']))
     require(len(steps)==10,'exact diagnostic/build child count')
     require(p.get('build_steps')==[[label,argv] for label,argv in steps],'MAIN frozen exact argv')
     return steps
 
+def macho(data):
+    """Bounded arm64 little-endian normal object/image reader; no host tool."""
+    require(len(data)>=32 and struct.unpack_from('<II',data)==(0xfeedfacf,0x100000c),'arm64 MachO64')
+    _,_,_,kind,ncmds,cmdbytes,_,_=struct.unpack_from('<8I',data)
+    require(kind in (1,2) and ncmds<=256 and 32+cmdbytes<=len(data),'fixed object/executable image')
+    sections=[];symbols=[];symtab=None;indirect=None;loads=[];at=32
+    def region(offset,count):
+        require(integer(offset,0,len(data)) and integer(count,0,len(data)-offset),'MachO bounded region')
+        return data[offset:offset+count]
+    for _ in range(ncmds):
+        cmd,size=struct.unpack('<II',region(at,8));require(size>=8 and at+size<=32+cmdbytes,'load command region')
+        b=region(at,size)
+        if cmd==0x19:
+            require(size>=72,'segment64');count=struct.unpack_from('<I',b,64)[0]
+            require(count<=128 and 72+80*count<=size,'section64 union')
+            for i in range(count):
+                s=b[72+80*i:152+80*i];name=s[:16].split(b'\0')[0].decode();segment=s[16:32].split(b'\0')[0].decode()
+                addr,length,offset,align,reloff,nreloc,flags,reserved1,reserved2,_=struct.unpack_from('<QQ8I',s,32)
+                require(name not in ('__mod_init_func','__mod_term_func','__thread_init','__init_offsets'),
+                        'unqualified native initializer/terminator')
+                sections.append(dict(name=name,segment=segment,addr=addr,bytes=length,offset=offset,
+                    reloff=reloff,nreloc=nreloc,flags=flags,indirect=reserved1,stride=reserved2,index=len(sections)+1))
+        elif cmd==2:
+            require(symtab is None and size==24,'unique symbol table');symtab=struct.unpack_from('<4I',b,8)
+        elif cmd==11:
+            require(size==80,'dysymtab shape');d=struct.unpack_from('<18I',b,8);indirect=(d[12],d[13])
+        elif cmd in (0xc,0x18,0x80000018,0x1f,0x8000001f,0x80000023):
+            require(size>=24,'dylib role');off=struct.unpack_from('<I',b,8)[0];require(24<=off<size,'dylib name offset')
+            loads.append(b[off:].split(b'\0')[0].decode())
+        elif cmd in (0x8000001c,0x11,0x1a):raise Refusal('unqualified rpath/routine initializer')
+        at+=size
+    require(at==32+cmdbytes and symtab is not None,'complete load-command union')
+    off,count,stroff,strbytes=symtab;require(count<=65536 and strbytes<=8388608,'symbol limits')
+    strings=region(stroff,strbytes)
+    for i in range(count):
+        name,typ,section,desc,value=struct.unpack('<IBBHQ',region(off+16*i,16));require(name<len(strings),'symbol string index')
+        raw=strings[name:].split(b'\0')[0].decode();normalized=raw[1:] if raw.startswith('_') else raw
+        symbols.append(dict(name=normalized,raw=raw,type=typ,section=section,value=value))
+    stub_names={};pointer_names={}
+    if indirect is not None:
+        io,ic=indirect;require(ic<=65536,'indirect table bound');table=struct.unpack('<'+'I'*ic,region(io,4*ic))
+        for s in sections:
+            section_type=s['flags']&255
+            if section_type not in (6,7,8):continue
+            stride=s['stride'] if section_type==8 else 8
+            require(stride>0 and s['bytes']%stride==0,'exact symbol stub/GOT slots')
+            for i in range(s['bytes']//stride):
+                index=s['indirect']+i;require(index<len(table) and table[index]<len(symbols),'qualified stub symbol')
+                (stub_names if section_type==8 else pointer_names)[s['addr']+i*stride]=symbols[table[index]]['name']
+    relocs={}
+    for s in sections:
+        if s['name']!='__text':continue
+        require(s['nreloc']<=65536,'normal text relocation bound')
+        rows=[]
+        for i in range(s['nreloc']):
+            address,info=struct.unpack('<iI',region(s['reloff']+8*i,8))
+            number=info&0xffffff;external=(info>>27)&1;kind=(info>>28)&15;length=(info>>25)&3
+            require(0<=address<s['bytes'] and external==1 and number<len(symbols),'explicit named text relocation')
+            require(kind in (2,3,4,5,6) and length==2,'qualified branch/page/GOT text relocation only')
+            rows.append({'offset':address,'kind':kind,'symbol':symbols[number]['name']})
+        relocs[s['index']]=rows
+    return {'kind':struct.unpack_from('<I',data,12)[0],
+            'sections':sections,'symbols':symbols,'relocations':relocs,'loads':loads,'stubs':stub_names,'pointers':pointer_names,'data':data}
+
+def native_body_join(root,frames,plan):
+    linked=macho(read_bytes(root/'native-runner',ARTIFACTS))
+    require(linked['kind']==2 and sorted(linked['loads'])==sorted(plan['native_dylibs']),'exact native load roles')
+    symbols={s['name']:s for s in linked['symbols'] if not s['type']&0xe0 and s['section']}
+    report={}
+    for unit in ('record','wrapper'):
+        obj=macho(read_bytes(root/('native-'+unit+'-normal.o'),ARTIFACTS));require(obj['kind']==1,'normal producer object')
+        for section in obj['sections']:
+            if section['name']!='__text':continue
+            defs=[s for s in obj['symbols'] if s['section']==section['index'] and not s['type']&0xe0 and s['name'] in frames]
+            defs.sort(key=lambda s:s['value'])
+            require(defs,'normal object definitions')
+            unknown=[s['name'] for s in obj['symbols'] if s['section']==section['index'] and
+                     not s['type']&0xe0 and s['name'] not in frames and not s['raw'].startswith(('ltmp','L'))]
+            require(not unknown,'no unqualified native object text definition')
+            for index,definition in enumerate(defs):
+                name=definition['name'];require(name in symbols and name not in report,'unique linked native definition')
+                start=definition['value']-section['addr'];end=(defs[index+1]['value']-section['addr']) if index+1<len(defs) else section['bytes']
+                require(0<=start<end<=section['bytes'] and (end-start)%4==0,'bounded arm64 body')
+                destination=symbols[name];ls=next(s for s in linked['sections'] if s['index']==destination['section'])
+                require(ls['name']=='__text','linked native body section')
+                lo=ls['offset']+destination['value']-ls['addr'];normal=obj['data'][section['offset']+start:section['offset']+end]
+                actual=linked['data'][lo:lo+len(normal)];require(len(actual)==len(normal),'complete linked body bytes')
+                wanted=bytearray(normal);relations=[]
+                for reloc in obj['relocations'].get(section['index'],[]):
+                    if not start<=reloc['offset']<end:continue
+                    at=reloc['offset']-start;word=struct.unpack_from('<I',normal,at)[0]
+                    live=struct.unpack_from('<I',actual,at)[0];target=reloc['symbol'];kind=reloc['kind']
+                    if kind==2:
+                        require((word&0x7c000000)==0x14000000 and word&0x03ffffff==0,'branch26 exact symbol entry')
+                        delta=live&0x03ffffff;delta=delta-(1<<26) if delta&(1<<25) else delta
+                        address=destination['value']+at+4*delta
+                        named=next((n for n,s in symbols.items() if s['value']==address),linked['stubs'].get(address))
+                        require(named==target,'exact linked native direct-call target')
+                        mask=0x03ffffff
+                    else:
+                        addresses=[a for a,n in linked['pointers'].items() if n==target] if kind in (5,6) else [symbols[target]['value']] if target in symbols else []
+                        require(addresses,'qualified native data/function/GOT target')
+                        if kind in (3,5):
+                            require(word&0x9f000000==0x90000000,'ADRP relocation instruction')
+                            imm=((live>>5)&0x7ffff)<<2|((live>>29)&3)
+                            imm=imm-(1<<21) if imm&(1<<20) else imm
+                            require(any(((destination['value']+at)&~4095)+(imm<<12)==address&~4095 for address in addresses),'exact native page binding');mask=0x60ffffe0
+                        else:
+                            if word&0x1f000000==0x11000000:scale=0
+                            else:
+                                require(word&0x3b000000==0x39000000,'qualified unsigned load/store offset');scale=(word>>30)&3
+                            addend=(word>>10)&0xfff
+                            require(any(((live>>10)&0xfff)<<scale==(address+(addend<<scale))&4095 for address in addresses),'exact native page offset');mask=0x003ffc00
+                    require(word&~mask==live&~mask,'unchanged instruction outside relocation')
+                    struct.pack_into('<I',wanted,at,live);relations.append(reloc)
+                require(bytes(wanted)==actual,'exact normal-object/linked native body bytes')
+                report[name]={'normal_sha256':digest(normal),'linked_sha256':digest(actual),'bytes':len(actual),'relocations':relations}
+    require(set(report)==set(frames),'every native source frame has actual normal/linked body')
+    return report
+
 def target_proof(job,target):
-    p=job.plan;frames={};edges={};dependencies={}
+    p=job.plan;frames={};edges={};dependencies={};pairs={};normal_bodies={};normal_text={}
     hashes={path:role['sha256'] for path,role in p['dependencies'].items() if role.get('kind')=='file'}
     for unit in ('record','wrapper'):
-        stem=job.root/(target+'-'+unit)
-        dependencies[unit]=verify_dependencies(str(stem)+'.d',p['dependencies'])
-        part=parse_su(read_bytes(str(stem)+'.su',1048576).decode(),hashes)
-        require(not (set(part)&set(frames)),'separate translation-unit definitions')
-        graph=assembly_graph(read_bytes(str(stem)+'.s',2097152).decode(),part,target=='native')
-        frames.update(part);edges.update(graph)
+        evidence={}
+        for role in ('normal','diagnostic'):
+            stem=job.root/(target+'-'+unit+'-'+role)
+            deps=verify_dependencies(str(stem)+'.d',p['dependencies'])
+            part=parse_su(read_bytes(str(stem)+'.su',1048576).decode(),hashes,p['definitions'][target])
+            text=read_bytes(str(stem)+'.s',2097152).decode()
+            graph=assembly_graph(text,part,target=='native');bodies=assembly_bodies(text,part,target=='native')
+            evidence[role]={'deps':deps,'frames':part,'graph':graph,'bodies':bodies,'text':text,
+                'artifacts':{suffix:file_record(str(stem)+suffix) for suffix in ('.d','.su','.s')}}
+        normal,diagnostic=evidence['normal'],evidence['diagnostic']
+        require(normal['deps']==diagnostic['deps'] and normal['frames']==diagnostic['frames'],
+                'distinct normal/diagnostic exact dependencies and SU definition spans/frames')
+        require(normal['graph']==diagnostic['graph'],'complete normal/diagnostic calls')
+        require({n:b['body'] for n,b in normal['bodies'].items()}=={n:b['body'] for n,b in diagnostic['bodies'].items()},
+                'exact saved normal-producer/diagnostic bodies')
+        part=normal['frames'];require(not (set(part)&set(frames)),'separate translation-unit definitions')
+        frames.update(part);edges.update(normal['graph']);normal_bodies.update(normal['bodies'])
+        for name in part:normal_text[name]=normal['text']
+        dependencies[unit]=normal['deps']
+        pairs[unit]={role:{'artifacts':e['artifacts'],'frames':e['frames'],
+                    'body_hashes':{n:b['sha256'] for n,b in e['bodies'].items()}} for role,e in evidence.items()}
     require(all(r in frames for r in ROOTS),'three actual production definitions')
     record_path=str((ROOT/SOURCES[1]).resolve());wrapper_path=str((HERE/'wrapper.cpp').resolve())
     require(all(frames[r]['source']==record_path for r in ROOTS),'production roots bound to actual codec source')
@@ -558,20 +1315,31 @@
     # No codec definition may call a wrapper definition or use external unqualified costs.
     wrapper_names={n for n,f in frames.items() if f['source']==wrapper_path}
     require(all(not (edges[n]&wrapper_names) for n,f in frames.items() if f['source']==record_path),'one-way wrapper/production role graph')
-    locals_map=None;linked=None
+    locals_map=None;linked=None;native_join=None;initialization=None
     if target=='wasm':
-        linked,exports=wasm_module(read_bytes(job.root/'record.wasm',8388608))
-        require(all(name in frames for name in linked),'all linked definitions have source-bound normal SU roles')
+        linked,exports,initialization=wasm_module(read_bytes(job.root/'record.wasm',8388608))
+        require(set(linked)==set(frames),'exact linked/normal definition union')
         for name,node in linked.items():
             require(node['calls']==edges[name],'linked/assembly direct-call closure')
+            instructions,local_types=wasm_assembly_instructions(normal_bodies[name]['body'])
+            require(instructions==node['instructions'] and local_types==node['local_types'],
+                    'exact linked body operands/normal instructions and declared locals')
+            match=re.search(r'\.functype\s+'+re.escape(name)+r'\s+\(([^)]*)\)\s*->\s*\(([^)]*)\)',normal_text[name])
+            require(match is not None,'normal function parameter type declaration')
+            widths={'i32':0x7f,'i64':0x7e,'f32':0x7d,'f64':0x7c}
+            require([widths[x.strip()] for x in match[1].split(',') if x.strip()]==node['params'],'exact actual parameter types')
+            require([widths[x.strip()] for x in match[2].split(',') if x.strip()]==node['returns'],'exact actual result types')
         require(all(exports[x][0]==0 and linked.get(x,{}).get('index')==exports[x][1]
                     for x in EXPORTS-{'memory'}),'export function/source identity')
         locals_map={name:node['locals'] for name,node in linked.items()}
         require(all(r in locals_map for r in (*ROOTS,'run')),'linked production/root local roles')
+    else:native_join=native_body_join(job.root,frames,p)
     full_root=p['full_roots'][target]
     require(full_root==('main' if target=='native' else 'run'),'fixed whole wrapper root')
     proof=frame_gate(frames,edges,p['external_frames'][target],ROOTS,full_root,locals_map)
-    job.write(target+'-proof.json',encoded({'dependencies':dependencies,'frames':frames,
+    job.write(target+'-proof.json',encoded({'dependencies':dependencies,'normal_diagnostic':pairs,
+              'image':file_record(job.root/('record.wasm' if target=='wasm' else 'native-runner')),
+              'static_module_initialization':initialization,'native_body_join':native_join,'frames':frames,
               'edges':{n:sorted(v) for n,v in edges.items()},'linked':None if linked is None else {
               n:dict(v,calls=sorted(v['calls'])) for n,v in linked.items()},'proof':proof}),'reports')
 
@@ -604,9 +1372,12 @@
     artifacts=inventory(job.root)
     require(sum(r.get('bytes',0) for r in artifacts.values())<=ARTIFACTS,'artifact aggregate64MiB')
     for target in ('native','wasm'):target_proof(job,target)
+    products={str(job.root/name):file_record(job.root/name) for name in (
+        'native-runner','record.wasm','native-record-normal.o','native-wrapper-normal.o',
+        'wasm-record-normal.o','wasm-wrapper-normal.o')}
     native_path=job.root/'native-runner'
     # This executable did not exist at preflight: bind ONLY this owned link product.
-    job.plan['tools'][str(native_path)]=file_record(native_path)
+    job.plan['owned_executable']=file_record(native_path)
     for target,argv,wanted in (
         ('native',[str(native_path)],native),
         ('wasm',[job.plan['tool_roles']['node'],str(HERE/'wasm_runner.mjs'),str(job.root/'record.wasm')],wasm)):
@@ -614,16 +1385,20 @@
         require(len(raw)==1048576,'exact target response stream')
         for i,c in enumerate(rows):compare_row(c,raw[i*2048:(i+1)*2048],wanted[i*2048:(i+1)*2048],mask[i*2048:(i+1)*2048])
     require(len(job.records)==12,'exact actual job children')
+    for path,record in products.items():require(file_record(path)==record,'normal linked product preserved')
     verify_protection(job.plan)
     job.write('review.json',encoded({'status':'REVIEW_READY_NOT_ACCEPTED','children':12,'rows_per_target':512,
-              'source_work':work_certificate(),'process_records':job.records,'capture':job.captured}),'driver')
+              'source_work':work_certificate(),'process_records':job.records,'capture':job.captured,
+              'actions':job.actions,'persistence_candidates':job.writes}),'driver')
     job.check()
 
 def main():
+    global READ_CUTOFF
+    started=time.monotonic();READ_CUTOFF=started+300
     parser=argparse.ArgumentParser(description=__doc__)
     parser.add_argument('operation',choices=('MR-CATALOG-1','MR-ACTUAL-1'))
     parser.add_argument('--lease',required=True);parser.add_argument('--lease-sha256',required=True)
-    args=parser.parse_args();started=time.monotonic()
+    args=parser.parse_args()
     lease_bytes=read_bytes(args.lease,METADATA)
     require(re.fullmatch('[0-9a-f]{64}',args.lease_sha256) is not None and digest(lease_bytes)==args.lease_sha256,'explicit exact lease hash')
     plan=json.loads(lease_bytes);root=validate_lease(plan,args.operation)
@@ -631,7 +1406,11 @@
     if args.operation=='MR-ACTUAL-1':
         require(isinstance(plan.get('tools'),dict) and isinstance(plan.get('dependencies'),dict),'frozen installed roles')
         for path,role in plan['tools'].items():
-            require(role.get('kind')=='file' and file_record(path)==role,'ordinary installed tool identity')
+            require(installed_tool_record(path)==role,'typed installed role/complete aliases')
+        validate_wait_role(plan) # hashes/platform only; no ctypes resolution in preflight.
+        require(set(plan['definitions'])=={'native','wasm'} and type(plan['native_dylibs']) is list,'qualified target definition/image roles')
+        for definitions in plan['definitions'].values():
+            for symbol,definition in definitions.items():verify_definition(symbol,definition)
         for path,role in plan['dependencies'].items():require(file_record(path)==role,'installed dependency identity')
         build_steps(plan,root) # exact shape/argv validation precedes even root creation.
         require(all(path in plan['tools'] for path in plan['tool_roles'].values()),'all tool roles pinned')
@@ -645,9 +1424,11 @@
     except BaseException as error:
         # A deadline is not extended to manufacture a final report. Earlier receipts
         # remain authoritative if the bounded failure receipt cannot be persisted.
-        if time.monotonic()<=job.deadline:
+        if job.b.now()<job.deadline:
             try:job.write('failure.json',encoded({'status':'REFUSED_NOT_ACCEPTED','error':type(error).__name__+': '+str(error),
-                         'records':job.records,'capture':job.captured}))
+                         'records':job.records,'capture':job.captured,'actions':job.actions,'writes':job.writes,
+                         'unresolved_handles_retained':len(UNRESOLVED_HANDLES),
+                         'unresolved_reader_count':len(RETAINED_READERS)}),cutoff=job.deadline)
             except BaseException:pass
         raise
 
```

## tests/outbreak/motion_record/release-1/SCHEMA.md

Before 7657/b3b9d7c45eb97e4ebab49f99d03de52f3d6af04d7f4891c2c583ef2fcfba9391; after 12497/5c3e6d4236ce7428a8fbdfa3f9d5e3d893b9fd686a331cbd6c4b54622a2d3474.

```diff
--- T196-delivered/tests/outbreak/motion_record/release-1/SCHEMA.md
+++ T200-source/tests/outbreak/motion_record/release-1/SCHEMA.md
@@ -1,6 +1,8 @@
 # Motion record release-1 private evidence schema
 
-T196/D315 SOURCE ONLY: NOT_COMPILED / NOT_EXECUTED / NOT_ACCEPTED.
+T200/D324 HARNESS SOURCE CORRECTION ONLY: NOT_IMPORTED / NOT_PARSED /
+NOT_EXECUTED / NOT_ACCEPTED. T199's separate syntax result does not qualify this
+controller. T196 request/response/wire/catalog layouts below are unchanged.
 All integer fields below are little endian. These private observations are not a
 parent protocol, production API, actor authentication or portable native layout.
 
@@ -118,12 +120,45 @@
 source_records for all eight files, protected_files exact file records and
 protected_roots complete inventories, rows512/requests262144/responses1048576,
 whole_seconds300/child_seconds60/capture_bytes8388608/metadata_bytes67108864.
-Actual additionally freezes tools(path->record), four tool_roles, environment,
+Actual additionally freezes tools(path->typed installed role), four tool_roles, environment,
 native_sysroot, dependencies(path->record), ten exact build_steps(label/argv),
 full_roots(native main/Wasm run), external_frames per target and exact
 preparation_manifest record. Each external frame needs MAIN normal-scope approval,
-source/line/source_sha256, evidence/evidence_sha256, bytes and complete calls.
+source/line/end_line/source_sha256/span_sha256/signature/symbol,
+evidence/evidence_sha256, bytes and an explicit complete calls list. Closed exact
+external keys are checked; omitted calls is not an empty leaf. `definitions`
+separately binds native/Wasm symbols to independently MAIN-qualified source spans,
+signatures and evidence hashes. SU must locate within that exact definition and
+both normal/diagnostic records must agree. `native_dylibs` pins the complete
+actual MachO load-role list; no unqualified initializer/rpath is accepted.
 Neither a role label nor an unknown cost supplies zero.
+
+Installed roles are NOT generic FileRefs. TOOL_SPECS fixes the actual native
+0755/nlink78 launcher/hash, Wasm raw two-alias chain, wasm-ld alias, fixed Node and
+canonical Python. installed_tool_record retains raw/resolved path, each alias
+link text/mode/nlink/mtime/ctime, resolved size/mode/nlink/hash/times. Later MAIN
+selects only these exact supported records; no arbitrary multi-link exception.
+Source/data/dependency/output read_bytes/file_record remain strict single-link.
+
+`wait_adapter` has EXACT keys schema/system_identifier/symbol/idtype/flags/inputs/
+python: D235_D260_DARWIN_ARM64,/usr/lib/libSystem.B.dylib,waitid,1,37; exact thirteen
+ABI_INPUT_HASHES files and canonical Python typed role. System library is a dyld
+identifier, never a fictitious ordinary FileRef. Lazy real setup checks Darwin/
+arm64/little-endian/LP64, default SIGCHLD, scalar signedness/width and104-byte/
+alignment8 siginfo with all ten exact offsets. Each call zeroes the record;
+no-event differs from terminal, EINTR stays within original cutoff, ECHILD loses
+ownership. Pure controls inject FakeBoundary and never call this real setup.
+
+Normal object stems end `-normal`; distinct diagnostic stems end `-diagnostic`.
+Each has its OWN .su/.d/.s. Normal objects retain producer assembly with
+-save-temps=obj; diagnostic -S also emits its own -MD/-MF pair. C++17/O0/
+gline-tables-only and functional options/source/target match; artifact differences
+are explicit in the frozen ten argv. Both frame/span/dependency unions and actual
+bodies/calls must match. Native normal object bytes join actual linked text with
+explicit named branch/page/GOT relocations. Wasm body opcodes/operands/call/global
+names, parameters/results/locals join actual linked module. Actual static global/
+data initialization is recorded, starts/elements/unknown forms refuse. Source and
+compiler capability qualifications remain future prerequisites, not passed gates.
 
 File records retain kind/mode/nlink/bytes/hash/mtime/ctime; symlinks retain target,
 directories retain metadata. Inventories walk without following symlinks,<=8192
@@ -131,7 +166,38 @@
 the separately reviewed lease. No active World/AI source is implicitly frozen.
 Each controller child record retains original pid, actual waitpid/reaped_pid,
 exit, group observation, complete stdin/stdout/stderr facts, primary and secondary
-errors, signals, exact argv, time and aggregate capture. Original reap truth is
-recorded before admission. Unknown/EPERM/present group, ECHILD, late persistence,
+errors, signals, exact argv/environment, original work/hard cutoffs, time,
+captured stream byte counts/hashes and aggregate capture. Owned provisional
+process/selector/pipe/fd handles and captured bytes stay strong-referenced on
+unresolved failures; no destructor-driven success/closure is assumed. Every
+post-acquisition setup path is inside the same owned orchestration. Fresh
+nonreaping handle/PID/pgid/sid observation authorizes every mutating group action;
+no cached boolean or ECHILD supplies an anchor. Group handling precedes consuming
+original waitpid; actual consumed truth is recorded before time/zero admission.
+No post-reap mutating signal is issued. D260 permits ONLY fresh terminal0 plus
+pre-reap EPERM1 UNKNOWN with no signal, consuming original0 and a distinct timely
+post-reap ESRCH. Required permission_observation is null or exact phase/errno/pid/
+terminal_exit_code/mutating_signal_attempted/resolution record. UNKNOWN remains
+visible even if later resolved. Post-reap present/EPERM, ECHILD, late persistence,
 incomplete IO, nonzero exit and any prior error refuse. No post-reap mutating
 signal or retry; failure receipts never extend deadlines.
+
+Every step records name/start/end/returned/error/original cutoff. Checks precede
+and follow each boundary. Original min(childStart+60,wholeEnd) covers every child
+IO/signal/fs step/release, including log and candidate receipt persistence.
+Unbuffered pipes/raw exclusive file descriptors avoid implicit flush/close.
+Write receipts retain planned/known written bytes, unresolved write-return flag,
+fd, close attempted/closed, completion and errors; ambiguous close never retries.
+Late returns keep acquired handles/actual returned facts but refuse subsequent
+mutations. Expired child operations remain skipped/retained; an outer failure
+ledger can use only the original remaining whole budget. Child receipt files
+describe candidates; outer records admit only after their closes and all final
+cutoff gates. Original terminal outer completion plus MAIN review remains
+necessary; no file can self-prove its own final persistence time.
+
+Controls remain exactly96: RUN_CONTROLS64 calls actual Job.run, WRITE_CONTROLS32
+calls actual Job.write. Injected in-memory fake clock/OS/process/selector/storage
+boundaries precede calls; zero real process/FFI/project/SUT activity. The old
+32/32/32 dictionary controls are replaced. Every literal name/expected outcome is
+in source and the corrected T196 plan; controls.json still stores96 compact
+results within65536 setup bytes. No extra512-row case or12-child allowance.
```

## tests/outbreak/motion_record/release-1/README.md

Before 6012/18ea19043e64e0719238f88b98e17c0530514e9bc1de9043455abbdbfa46d861; after 10673/0654d5db9913b711d204df79cc5b084d5ad49f05ad780790a61e15e3ea330e9c.

```diff
--- T196-delivered/tests/outbreak/motion_record/release-1/README.md
+++ T200-source/tests/outbreak/motion_record/release-1/README.md
@@ -1,7 +1,9 @@
 # Future isolated record harness source
 
-T196/D315 authorizes authoring only. NOT_COMPILED / NOT_EXECUTED / NOT_ACCEPTED.
-Do not import, parse, generate, compile or run this package under T196. No result
+T2001.0/D324 authorizes these exact controller/schema/readme corrections only.
+NOT_IMPORTED / NOT_PARSED / NOT_EXECUTED / NOT_ACCEPTED for this harness delivery.
+T199 syntax evidence is separately accepted; it does not qualify this harness.
+Do not import, parse, generate, compile or run this package under T200. No result
 root exists as part of this delivery. [SCHEMA.md](SCHEMA.md) defines all bytes.
 
 Production source has no consumer/build change. The wrapper includes the real
@@ -16,7 +18,9 @@
 1. MAIN first reviews all eight sources and the source maps/handoff. Resolve the
    native normal runtime/entry qualification question. Freeze an exact lease as
    data with source identities, installed tool/header/library graph, argv,
-   ownership/protections, deadlines and complete external frame evidence.
+   ownership/protections, deadlines and complete external frame evidence. Typed
+   installed tool aliases/identities, fixed D235 wait ABI inputs and independent
+   symbol-to-definition span qualifications are required. No current lease exists.
 2. Only a separate MR-CATALOG-1 release permits `verify.py MR-CATALOG-1 --lease
    <reviewed-file> --lease-sha256 <exact-approved-hash>`. Fixed fresh slot
    `preparation-1`; zero children. It imports only its independent oracle after
@@ -41,44 +45,84 @@
 and stderr are drained through bounded nonblocking reads. Original waitpid truth
 and group ESRCH are mandatory. Deadlines do not reset between children.
 
+Acquisition, all setup, IO, signals, wait/close and each log persistence substep
+use the original min(child start+60,whole end). Popen pipes are unbuffered. Fresh
+nonreaping original child/pgid/sid identity immediately authorizes each group
+mutation. ECHILD/unknown/cached reap/lost ownership never authorizes a signal.
+The terminal original remains unreaped until eligible group handling. D260's
+pre-reap EPERM is UNKNOWN and can defer without signal only with fresh exact
+terminal0, original consuming waitpid and a distinct timely post-reap ESRCH.
+No post-reap numeric mutation or unknown-to-zero status conversion exists.
+
+Every write uses raw exclusive fd open/chmod/write/fsync/close steps, each checked
+before AND after against the same original cutoff. A late syscall cannot be
+preempted universally; its returned facts are retained, the next mutation is
+skipped, and the operation refuses. Ambiguous closes are not retried. Expired
+child persistence is not resumed under the whole budget. Strong process,
+selector/pipe, fd and unpersisted-byte references remain on unresolved paths.
+The outer failure ledger alone may use remaining original whole time; it records
+partial/ambiguous/skipped facts and supplies no cleanup grace. Child receipt files
+are candidates; final post-close admission is in outer records. MAIN additionally
+needs the original terminal outer handle, not candidate file presence.
+
 Capture8MiB is raw targets2MiB + compiler/link/assembly2MiB + runner diagnostics
 1MiB + proof reports2MiB + driver/receipts1MiB. Metadata64MiB is separately bounded;
 compiler/binary artifacts have a64MiB aggregate inventory gate. Individual module
 read cap8MiB. Existing archives/source/tool graphs are protected before and after;
 fresh owned outputs only. No writable shared cache or package installation.
 
-## Exact96 future controller controls
+## Exact96 future actual-method controls (reallocated under T200)
 
-The same terminal_gate, compare_row and frame_gate functions used by the actual
-controller receive bounded synthetic metadata/bytes; no process or SUT is run.
+The old32 terminal-dictionary/32 response/32 frame controls are replaced, not
+retained as an additional union. Every case calls actual Job.run or Job.write
+with FakeBoundary injected BEFORE effects. No process/filesystem/ctypes/FFI/SUT
+boundary is real. These are future source definitions, none executed under T200.
 
 | Group | Count | Meaning |
 |---|---:|---|
-|terminal|32|one admit;31 refusals: invalid pid4,reap2,reaped identity2,exit4,group3,IO3,primary2,secondary1,childtime3,wholetime3,capture4|
-|response|32|16 golden section mutations;16 masked representation mutations across V failure,E failure,D failure,D success (successful-D native output change alone admits)|
-|frames|32|eight admitted exact boundaries; eight codec overflows; eight whole caller overflows; eight unknown/missing/cyclic/nonzero nested helper graphs|
+|supervisor|64|actual Job.run through setup/acquisition/IO/anchor/group/reap/release/log persistence, including D260, ordinary success and owned descendants|
+|persistence|32|actual Job.write through short/failed/late/ambiguous writes, original child/whole cutoffs, traversal/exclusive ownership and caps|
 
-Names and mutations are finite literals in run_controls; exceptions other than
-Refusal are failures, never expected refusal. These96 controls are separate from
+RUN_CONTROLS and WRITE_CONTROLS contain the exact names/mutations/expectations;
+source case/lifetime maps are in the corrected T196 source plan. Fake storage
+errors are expected only where specified; unexpected exceptions fail preparation.
+Assertions also inspect actual action cutoffs, retained original handles/fds,
+signal absence after lost anchors, D260 nonmutation and kill-before-reap ordering.
+Eleven supervisor cases also invoke actual observer_protocol and
+validate_native_layout with fake native records/calls: widths, signedness, layout,
+offsets, PID, ECHILD, bounded EINTR, terminal0, signal, no-event and bad code.
+Fixed idtype1/flags37 and zero-on-each-call are asserted without ctypes.
+These96 controls are separate from
 the original512 real rows and add no target entry or child. They exercise real
-guards, not a second model of a controller. They do not replace review of process
-implementation, filesystem protection, SU parser or Wasm decoder.
+methods, not a second model of their decisions. Boundary event logs are synthetic
+inputs/observations, not fabricated production outputs. They do not establish
+real ABI/call support, ownership, emitted parser correctness or timing acceptance.
 
 ## Evidence gates and limitations
 
-Both translation units use C++17/O0/no-inline/no-exceptions/no-rtti/no-stack-
+Both translation units use C++17/O0/gline-tables-only/no-inline/no-exceptions/no-rtti/no-stack-
 protector/no-builtin/frame-pointer/stack-usage and the same target options in
-object and assembly commands. Native target is arm64-apple-macos13 with separately
+object and diagnostic assembly commands. Normal objects use -save-temps=obj and
+retain their actual producer assembly; diagnostic assembly has its OWN distinct
+stem plus .d and .su. No shared stem overwrite. Ten children remain unchanged
+in count. Installed capability/format qualification is required before release;
+no successful evidence is assumed from a flag's spelling. Native target is arm64-apple-macos13 with separately
 pinned installed sysroot; Wasm is wasm32-unknown-unknown/nostdlib. No exports or
 hooks are added to production. Wasm link exports memory plus request_address,
 request_capacity,response_address,response_capacity,run; no export-all/imports.
 
-Dependency files bind every actual header to the preapproved graph. Normal SU
-records bind source path/line/symbol/frame to source hashes; assembly defines
-direct-call closure, refuses indirect/unknown roles. Wasm binary parsing binds
-linked function/type/name/call indices and declared parameter/local bytes to
-the same normal assembly/SU functions. Unknown opcodes/definitions/normal callees
-refuse. All three production roots need full chain<=4096; full wrapper<=65536,
+Both dependency/SU records must match, including complete symbol ownership in
+independently MAIN-qualified exact definition spans/signatures/source and evidence
+hashes. Both saved normal-producer and diagnostic complete bodies/call graphs
+must match. A numeric line in a hashed file is insufficient. Native arm64 MachO
+normal-object body bytes join actual linked bytes with explicit branch/page/GOT
+relocations and exact named targets/stubs, load-role/initializer restrictions;
+unknown relocation/lowering refuses. Wasm linked body instructions/operands,
+function params/results, globals/calls and declared locals join normal assembly
+exactly; starts/elements/unknown initialization/code forms refuse. No guessed
+normal callee or missing calls-as-leaf default. External definitions require a
+closed explicit complete transitive call list and real span/evidence qualification.
+All three production roots need full chain<=4096; full wrapper<=65536,
 including real normal I/O/helper/runtime costs. Wasm adds declared locals to linear
 ABI frames; no claim about physical JIT/control stack. Normal external frames
 need source-backed MAIN-qualified facts and transitive calls; no guessed zero,
@@ -88,4 +132,24 @@
 introduce helpers. A source controller that refuses those unknown roles is not
 an accepted executable proof. Do not run to discover unpriced roles. MAIN must
 resolve the exact question and frozen plan first, within12 children. See the NEW
-T196 source plan/handoff for source work/callee/lifetime maps and open question.
+T196 source plan/T200 handoff for current source maps. The NEW T200 native host
+proposal is notes-only: current wrapper/runner/compiler boundary/main remain
+unchanged and the controller does not implement/adopt a shared module or host.
+
+## Exact future installed roles
+
+installed_tool_record is separate from strict file_record/read_bytes. It supports
+only later MAIN-selected actual /usr/bin/clang++0755/nlink78/118928/hash179301...c1818;
+Wasm clang++->clang->clang-24/hash9a96...c423; wasm-ld->lld/hashb851...ad5c;
+fixed Node24.19.0/hash27db...b5b1 and canonical Python3.11/hash4e28...c46a. Full
+paths, raw alias targets/modes/links/times and resolved sizes/hashes are retained.
+Others refuse; source/dependency/output files still require ordinary nlink1.
+Read-only hashing uses raw guarded fds; read/release each honors original whole
+or physical child cutoff, retaining late/ambiguous readers without implicit
+context-manager close. No preemption of an already-started syscall is claimed.
+RealBoundary.prepare lazily uses only pinned Darwin arm64 LP64 waitid P_PID1/
+flags37/libSystem fixed identifier with typed104-byte siginfo. Exact thirteen
+SDK type/ABI/ctypes/struct source/extension hashes and canonical Python role must
+match first; supported width/signedness/offsets, SIGCHLD, zero no-event/terminal,
+EINTR bounded retry and ECHILD rejection are explicit. Nothing loads at import
+or through fake preparation; no generic FFI/tool alias exception is introduced.
```

## notes/proposals/T196-motion-record-source-and-preparation-plan-1.md

Before 11025/638425ea1548e513695453822be9994e6c8754e4a24f9f57b5b7a4b423987bbf; after 18755/9509894521008dec19c48fa7b3841c1c9e73ccbdfe0b03f326212bff4c199a1f.

```diff
--- T196-delivered/notes/proposals/T196-motion-record-source-and-preparation-plan-1.md
+++ T200-source/notes/proposals/T196-motion-record-source-and-preparation-plan-1.md
@@ -2,13 +2,19 @@
 
 Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90. T1961.0/D315,
 MOTION_RECORD_FOUNDATION0.1, selected corrected T191 sections1–5.
-SOURCE_ONLY / NOT_COMPILED / NOT_EXECUTED / NOT_ACCEPTED.
+Initial T196 source delivery is historical. This OWN plan is corrected under
+T2001.0/D324; T199 separately accepted syntax only. Current harness corrections:
+NOT_IMPORTED / NOT_PARSED / NOT_EXECUTED / NOT_ACCEPTED. No T196/T199 write or
+execution permission survives. Production/oracle/wrapper/runner remain immutable.
 
 ## New-file diff scope
 
-Eight paths were absent before construction; the entire content at each is its
-addition diff. No existing source, test, header, ticket, authority, archive, tool
-or cache is edited. No Git operation/patch commit is authorized or performed.
+Eight paths were absent before INITIAL T196 construction; its new contents were
+addition diffs. T200 now edits ONLY own verify.py/SCHEMA.md/README.md and THIS plan,
+plus its NEW proposal/handoff/questions/diff note. Exact before/after textual
+diffs are in the NEW T200 handoff companion. Historical T196 handoff/reviews and
+hashes remain immutable; no production/oracle/wrapper/runner/authority/old proof/
+tool/cache edit or Git operation is authorized or performed.
 
 | New source | Role |
 |---|---|
@@ -131,10 +137,10 @@
 
 ## Finite preparation and actual proof plan
 
-Precisely96 future pure controls: terminal32,response32,frame32; literal mutations
-and expected admission/refusal in run_controls, README gives every group/count.
-They call actual controller guards with synthetic bounded metadata; zero SUT
-entries, processes, probes or extra corpus rows. None has run.
+Precisely96 future pure controls, REALLOCATED under T200:64 actual Job.run +32
+actual Job.write. Old terminal32/response32/frame32 dictionary controls are
+replaced, not added. FakeBoundary is injected before methods, so no real OS,
+process, FFI, filesystem, project/SUT entry or additional corpus row. None has run.
 
 MR-CATALOG-1 and MR-ACTUAL-1 are DISTINCT separately reviewed future operations,
 not continuation/retry leases. Fixed fresh preparation-1/attempt-1 roots, absent
@@ -146,8 +152,17 @@
 executions. No version/test discovery/extra tool invocation. See README and
 SCHEMA for exact argv construction, role/ABI, capture and deadline controls.
 
-Actual normal evidence joins .d source-role graph, source-bound .su static frames,
-same-option .s direct edges and linked Wasm names/types/locals/direct calls.
+Actual normal evidence now retains distinct target-unit-normal and -diagnostic
+.d/.su/.s. The actual object child saves its producer assembly (-save-temps=obj);
+the diagnostic child has its own -MD/-MF and stem. Both retain the same source,
+C++17/O0/gline-tables-only and functional/target flags. Both complete dependency,
+SU frame/span and body/call unions must match. Independently MAIN-qualified
+exact definition spans/signatures/body hashes and evidence bind symbol ownership;
+a numeric line alone is insufficient. Native normal object text joins linked
+MachO body bytes, explicit named branch/page/GOT relocations/stubs and exact load/
+initialization roles. Wasm normal instructions/operands/params/results/locals
+join actual linked bodies, calls/globals and recorded constant initialization.
+Unsupported forms refuse; no extra parser/tool/probe/compiler child is introduced.
 Three production chains<=4096,full wrapper<=65536. Wasm linear ABI plus declared
 locals; native normal costs plus qualified source-backed transitive external
 facts; no unbound zero, no physical JIT stack claim. OPEN question
@@ -156,6 +171,16 @@
 
 Whole operation300s,child60s including cleanup/IO/persistence; original waitpid
 truth retained before later admission. Known group absence requires ESRCH.
+Every acquired process has provisional ownership before any fallible setup;
+every group mutation requires fresh D235 nonreaping original/PID/pgid/sid proof.
+Eligible group handling precedes consuming anchor. ECHILD/unknown/lost/cached reap
+prevents signals. D260 permits only exact fresh terminal0/EPERM1 no-signal deferral,
+original0 reap and distinct timely post-reap ESRCH. All other failures stay fatal.
+All mutating IO, persistence, fsync and release steps check ORIGINAL effective
+cutoff before and after. Handles are unbuffered; ambiguous closes never retry;
+late/unknown acquisitions, skipped closures, partial writes and unpersisted bytes
+stay strongly retained. Outer remaining-whole failure ledger cannot resume child
+operations. Candidate receipts do not claim their own final close/admission.
 Capture8MiB with both raw streams2MiB and category limits; metadata64MiB;
 artifacts64MiB separately inventoried. Refusal keeps truthful failed receipts
 within the original deadline, no overwrite/automatic retry. Complete protection
@@ -167,3 +192,80 @@
 paper reasoning and read-only text/identity inspection support this delivery.
 All full-MVP/M4/motor/parent/owner/G2/current-G1/camera/shot/tick/browser/native/
 Player/QA/T149 gates remain. Stop after this source handoff for MAIN review.
+
+## T200 exact96 source-case map
+
+RUN_CONTROLS (64, in literal order):
+
+1–16: ordinary; D260-noevent; short-stdin; payload; running-work-deadline;
+selector-after-spawn; register-stdout; register-stderr; register-stdin;
+initial-stdin-close; adapter-width; adapter-sign; adapter-layout;
+select-error; late-selector-return; late-work-selector.
+
+17–32: stdin-write-error; late-stdin-write; zero-stdin; bad-stdin; adapter-offset;
+adapter-identity; adapter-ECHILD; adapter-EINTRdeadline; unregister-stdout;
+unregister-stderr; unregister-stdin; anchor-echild; anchor-unknown;
+loss-immediately-before-signal; wrong-group; wrong-session.
+
+33–48: cached-reap; invalid-pid; terminal-leader-owned-descendant; signal-failure;
+consuming-ECHILD; wrong-consuming-pid; nonzero-terminal; post-present; post-eperm;
+D260-resolved; D260-post-present; D260-post-eperm; D260-nonzero; unknown-pre-group;
+late-spawn-acquisition; late-selector-acquisition.
+
+49–64: late-reap-return; late-pre-group; late-post-group; ambiguous-stdout-close;
+ambiguous-stderr-close; ambiguous-selector-close; late-selector-close;
+child-log-crosses60; child-fsync-crosses60; child-preclose-crosses60;
+child-ambiguous-file-close; adapter-normal; adapter-signal; spawn-rejection;
+adapter-noevent; adapter-code.
+
+Admits are ordinary, short-stdin, payload, terminal-leader-owned-descendant,
+D260-resolved, adapter-normal. All remaining58 refuse, even if eligible cleanup later succeeds.
+Injected exceptions/events exercise actual setup/ownership/IO/release/persistence
+branches. Assertions check signal absence on lost/unknown anchors, D260 no signal,
+original handle retention, no late initiated step, unresolved-fd retention and
+kill-before-consuming-reap order for the owned-descendant case.
+Eleven supervisor cases also call actual observer_protocol/validate_native_layout
+through FakeBoundary.prepare with fake native records, BEFORE any real ctypes
+import/load/call. They cover width/signedness/layout/offset mismatches, wrong PID,
+ECHILD, EINTR to original cutoff, exact terminal0, signal exit, no-event and invalid
+terminal code; fake native wait asserts P_PID1/flags37 and every zero record.
+
+WRITE_CONTROLS (32, in literal order):
+
+1–16: ordinary; empty; short; zero; oversized-return; open-error; chmod-error;
+write-error; fsync-error; ambiguous-close; late-open; late-chmod; late-write;
+late-fsync-preclose; late-close; whole-open.
+
+17–32: whole-chmod; whole-write; whole-fsync; whole-close; expired-before-open;
+whole-expired; traversal; absolute; nested; metadata-cap; capture-cap; driver-cap;
+empty-late-fsync; empty-ambiguous-close; short-owned-byte-prefix;
+normal-original-whole.
+
+Admits ordinary, empty, short, short-owned-byte-prefix, normal-original-whole.
+All remaining27 refuse. Partial/late syscall return facts are recorded before
+post-step admission; no next write/fsync/close starts after original cutoff.
+These are specified source expectations, not observed test outcomes.
+
+## T200 lifetime/cutoff/role/emitted ledger
+
+| Resource or fact | Source owner / cutoff / terminal treatment |
+|---|---|
+|process|Job.owned provisional record before spawn; actual acquired object assigned inside checked call; original child60/whole300; unresolved strong references, never fabricated reaping|
+|selector/pipes|assigned under same try; all setup/IO/close checked at original effective cutoff; unbuffered; ambiguous closes skipped rather than retried|
+|group anchor|fresh lazy D235 exact supported ABI; pgid/sid/original PID/cache checks; no consuming poll before cleanup; loss/unknown disables mutation irrevocably|
+|permission observation|D260 closed fields retain UNKNOWN at pre-reap; only fresh terminal0/no signal/original reap0/post-ESRCH resolves|
+|file fd|assigned inside checked open; explicit chmod/write/fsync/close; known-byte count/unresolved-return/ambiguous-close facts; original child cutoff for logs/receipt, whole for outer ledger|
+|read fd|guarded_file raw O_RDONLY/NOFOLLOW; every read and release checks whole/physical-child cutoff; late/ambiguous reader handles retained separately; no context-manager late close|
+|candidate receipt|actual post-close admission in outer Job records; original terminal caller plus MAIN review required; no self-persistence PASS|
+|installed tool|installed_tool_record fixed explicit tool/alias schema; native nlink78 only exact accepted role; tool/alias/current timestamps retained pre/post; strict source/data/dependency readers unchanged|
+|ABI dependencies|thirteen fixed SDK type/wait/signal/ctypes/struct inputs and canonical Python role; exact source hash/typed layout before lazy actual setup; fake controls never resolve library|
+|normal evidence|actual object plus saved producer .s/.su/.d and artifact identities; distinct -normal stem; complete body/frame/definition/dependency/call union|
+|diagnostic evidence|distinct -diagnostic .s/.su/.d; same functional options/source; independent exact normal comparison, no overwritten evidence|
+|native emitted|bounded arm64 MachO object/image bytes/symbols/stubs/relocations/load/init reader; unknown relocation/initializer/normal helper refuses|
+|Wasm emitted|exact linked function/global names, complete instructions/operands/calls/types/locals and constant initialization; unsupported starts/elements/opcodes refuse|
+
+Current native full root stays main. NEW T200-native-host-boundary-plan-1.md
+proposes a future callable shared-module/Python host boundary; it is NOT adopted
+or implemented by these corrections. Existing wrapper's uint32 native address
+accessors require explicit pointer-width resolution before such a host is safe.
+See the NEW T200 exact question and handoff for unresolved capability/ABI gates.
```
