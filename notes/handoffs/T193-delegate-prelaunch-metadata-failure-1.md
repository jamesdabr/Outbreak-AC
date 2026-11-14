# T193 prelaunch metadata failure receipt

- Worker: MAIN delegate /root/review_head_equality.
- Ticket: T1931.0 / D309; no compiler invocation consumed.
- Status: stopped for MAIN disposition. NEW own notes only; no output-root creation or source/header/SDK change.
- Companion question: notes/questions/T193-delegate-preflight-bookkeeping-refusal-1.md.

## Original tool invocation

Tool: exec_command via functions.exec; cwd `/Users/jd1/code/apps/outbreak`; max_output_tokens2000; default login/sandbox settings. Its original returned object is:

```json
{"chunk_id":"de06e9","wall_time_seconds":0.0000135,"exit_code":1,"original_token_count":23,"output":"Traceback (most recent call last):\n  File \"<stdin>\", line 29, in <module>\nAssertionError\n"}
```

Exact command text:

```sh
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -B - <<'PY'
import hashlib,json,os,re,stat,time
from pathlib import Path
repo=Path('/Users/jd1/code/apps/outbreak'); root=repo/'tests/outbreak/geometry/T193/check-1'; source=repo/'source/outbreak/p1_geometry.cpp'
assert not root.exists(), 'output root occupied'
def ident(p):
 p=Path(p); s=p.lstat(); d=dict(mode=stat.S_IMODE(s.st_mode),nlink=s.st_nlink,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
 if stat.S_ISREG(s.st_mode): d.update(kind='file',bytes=s.st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 elif stat.S_ISLNK(s.st_mode): d.update(kind='symlink',bytes=s.st_size,target=os.readlink(p))
 elif stat.S_ISDIR(s.st_mode): d.update(kind='directory')
 else: raise ValueError('unsupported file kind '+str(p))
 return d
si=ident(source); assert si['bytes']==74169 and si['sha256']=='0d999988280531d74ded6bfa27ae35e032233886267ddb1deb5def276cc4bf3b'
assert hashlib.sha256(source.read_bytes()[:31382]).hexdigest()=='c232100352425092561f6fc9701c77db17f643893510fde780839db21be17d21'
project={}; pending=[source]
while pending:
 p=pending.pop()
 if str(p) in project: continue
 project[str(p)]=ident(p)
 for n in re.findall(r'^\s*#\s*include\s*"([^"]+)"',p.read_text(),re.M):
  q=p.parent/n; assert q.parent==source.parent and q.is_file(); pending.append(q)
assert {Path(p).name for p in project}=={'p1_geometry.cpp','p1_store.h','p1_geometry.h','p1_types.h','p1_rules.h','map_import.h','p1_hash.h','p1_query_wide.h'}
old=repo/'tests/outbreak/geometry/G1/attempt-4'; dependencies=json.loads((old/'actual-dependencies.json').read_bytes())
sdkrefs={}; original_sysroot=str(repo/'web/build/.cache/sysroot'); copied_sysroot=str(old/'cache/sysroot')
for target in ('native','wasm'):
 sdkrefs[target]=[]
 for entry in dependencies[target+'/geometry.d']:
  oldpath=entry['compiler_path']; path=oldpath.replace(copied_sysroot,original_sysroot)
  if str(repo/'source/outbreak') in path: 
   assert project[path]==entry['identity']; continue
  current=ident(path)
  if path==oldpath: assert current==entry['identity'], 'SDK reference mismatch '+path
  else:
   assert current['kind']=='file' and all(current[k]==entry['identity'][k] for k in ('bytes','sha256','mode','nlink')), 'original/copied sysroot content role mismatch '+path
  sdkrefs[target].append(dict(path=path,identity=current,accepted_geometry_dependency=entry))
tool_hashes={'/usr/bin/clang++':'179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818','/private/tmp/outbreak-web-sdk/upstream/bin/clang++':'9a96f4220eefe21e72a4a9a20a88f4d6c26cad1b047cb02b5b22a96bef49c423'}
tools={}
for name,digest in tool_hashes.items():
 p=Path(name); chain=[]
 while p.is_symlink():
  chain.append(dict(path=str(p),identity=ident(p))); target=os.readlink(p); p=Path(target) if target.startswith('/') else p.parent/target
 resolved=p.resolve(); ri=ident(resolved); assert ri['kind']=='file' and ri['sha256']==digest
 assert ri['nlink']==(78 if name=='/usr/bin/clang++' else 1)
 tools[name]=dict(raw=ident(name),chain=chain,resolved=str(resolved),resolved_identity=ri)
controls={str(repo/p):ident(repo/p) for p in ('tickets/T193.md','notes/decisions/D309-G2-frontend-check.md','MVP/G2_FOUNDATION.md','tickets/T187.md')}
sdkroots={p:ident(p) for p in ('/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk',original_sysroot)}
for target in ('native','wasm'):
 for name in ('tmp','cache','log'): (root/target/name).mkdir(parents=True,exist_ok=False)
commands={}
common=['-std=c++11','-O2','-Wall','-Wextra','-Werror','-I',str(source.parent),'-fsyntax-only',str(source)]
for target,compiler,options in (('native','/usr/bin/clang++',['-isysroot','/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk']),('wasm','/private/tmp/outbreak-web-sdk/upstream/bin/clang++',['--target=wasm32-unknown-emscripten','--sysroot='+original_sysroot])):
 env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','TMPDIR':str(root/target/'tmp'),'CLANG_MODULE_CACHE_PATH':str(root/target/'cache')}
 commands[target]=dict(argv=[compiler]+options+common,env=env,cwd=str(repo),stdout=str(root/target/'log/stdout.txt'),stderr=str(root/target/'log/stderr.txt'))
pre=dict(scope='T193_SYNTAX_ONLY',executions_started=0,project=project,tools=tools,sdk_roots=sdkroots,sdk_header_reference_closure=sdkrefs,authorities=controls,commands=commands,monotonic_preflight_complete=time.monotonic(),wall_preflight_complete=time.time(),sdk_reference_note='Accepted actual G1 geometry.d closure as DATA with current seven-header include graph. Copied Wasm sysroot paths rebound to original read-only sysroot with exact ordinary byte/hash/mode/nlink comparison. Not a fresh dependency trace or whole SDK inventory.',limits={'whole_seconds':300,'child_seconds':60,'aggregate_diagnostic_bytes':8388608})
for name,data in (('preflight.json',pre),('commands.json',commands)):
 with (root/name).open('x') as f: json.dump(data,f,indent=2,sort_keys=True); f.write('\n')
print(json.dumps({'status':'PREFLIGHT_PASS','project_inputs':len(project),'native_sdk_refs':len(sdkrefs['native']),'wasm_sdk_refs':len(sdkrefs['wasm']),'root':str(root),'source_sha256':si['sha256']}))
PY
```

No subprocess/compiler/project import was present in this metadata command. The failure occurred before all mkdir/write statements. Both compiler argv arrays were future metadata construction only, never invoked; their construction statements were not even reached.

## Read-only postfailure observation

A separate inline stdlib-only read showed output_root_exists:false; live source74169/current SHA0d999988280531d74ded6bfa27ae35e032233886267ddb1deb5def276cc4bf3b; prefix SHA c232100352425092561f6fc9701c77db17f643893510fde780839db21be17d21; seven header hashes equal their archived G1 entries. Its tool chunkb1f439 returned exit0. Historical geometry source entry is31382/c232100352425092561f6fc9701c77db17f643893510fde780839db21be17d21, explaining the assertion rather than indicating a source corruption.

Correct role distinction for MAIN disposition: archived geometry is HISTORICAL_SOURCE_AT_G1_PROOF; live geometry is CURRENT_T193_SOURCE plus preserved-prefix identity; only unchanged header roles compare whole identities across that boundary. No generic hash rebasing or compiler retry is proposed. Both compiler calls remain0, remaining metadata construction is paused, and the production protected interval has not been closed by this failure receipt.
