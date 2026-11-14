# T140 World terminal handoff — D165-pair-1

- Worker: World/Match Systems, chat 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket/revision: T140 1.0; conditional release D165 completed by MAIN's exact pins SHA and explicit dispatch after four worker no-write/no-live-process ACKs.
- Contracts: smoke 0.9, admission 0.4, browser foundation/governance/P0 prerequisite 0.5. Ticket and contract revisions re-read before submission.
- Source/artifacts: accepted common source bdaa8df7ec39d9408f97feda4560832d7ef26c3c; /private/tmp/outbreak-clean-D120-1, D121-native-1 and D121-web-1. Existing shared dirty workspace preserved; no Git operation or source edit.
- Writes: controller-owned web/transport/results/candidate-pair/runtime-D165-pair-1/** and web/server/run/candidate-pair-D165-pair-1/** only during call; this own new handoff only after authoritative terminal. No source, contract, decision, ticket, earlier attempt or tool changes.
- Result: actual single normal_pair CLI and atomic terminal receipt PASS; MAIN acceptance remains pending. No second invocation, repair, reseal or retry.

## Identity and inspected authorization

Original cwd /Users/jd1/code/apps/outbreak. Exact externally supplied pins:
notes/decisions/D165-candidate-pair-runtime-pins.json, 55,108,496 bytes, SHA256 9bc78e0057418732e047b2928151b38bb4a955d6eaa18d9eb4f6b7a73ab85635.
Read-only pre-call check matched bytes/digest, fixed attempt, accepted admission, all nine current v4 source digests and their pins rows, checkpoint4 d0f81e58248c74b30f134433220949cfce59a6762d4aa0e0a58af405d54d7a63, accepted freeze 8b93f7fa0c376a6b47653304fb515a15710c74844cafed430fe5853552e4514e, and two absent exact output roots. 1,364 input rows; preservation 163,681 files / 47,224 directories / 9,695 opaque links / 14 metadata-only historical specials / 2 absent roots.

Admission SHA256 94b6a89ff876e31551658120c395eb046877dbd460934ec99ebf55b78695bc4a. Only original administrative .git is mode-only opaque; artifact .git and application/history graphs remain protected. Seven historical unreadable fixtures' 84 bytes are NOT ATTESTED; no reads or permission changes to them/FIFOs.

Inspected run.py fixed CLI, admission seam, supervisor authorization/effects/atomic terminal closure, owned native/Node/Chrome launch/capture/cleanup paths, and ordinary-input observer. Named script effects match explicit MAIN dispatch and previously applied confirm-cross-system-execution skill scope. Normal platform require_escalated review approved the exact runtime request. No rejected request or fallback caller.

## Exact single call and outer supervision

```text
env -u PYTHONPATH -u PYTHONHOME PYTHONNOUSERSITE=1 /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B /Users/jd1/code/apps/outbreak/web/runtime/pair-smoke-v4/run.py --pins /Users/jd1/code/apps/outbreak/notes/decisions/D165-candidate-pair-runtime-pins.json --pins-sha256 9bc78e0057418732e047b2928151b38bb4a955d6eaa18d9eb4f6b7a73ab85635
```

The inspected stdlib Python3.11.9 -B outer supervisor used one Popen with exact argv/cwd, stdin DEVNULL, separate nonblocking stdout/stderr, inherited environment except the unset/set policy above, start_new_session=True. Absolute whole-CLI cap600s, read/work cutoff590s with up to10s for owned-group TERM5s/KILL5s if needed; combined output cap8MiB. Supervisor made no workspace writes. Tool session13909 was retained and polled to authoritative exit0; no observation timeout treated as terminal. No controller/gate/admission/probe rerun.

Supervision: calls1, elapsed147.10116358299274s, fault:null, child_reaped:true, supervisor_signals:[], exit0. stdout1227bytes SHA256 f4dbf356c868a6604c40569b72bc0724424ebf8de1d0515d713ad7c704305aba; stderr0bytes SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855. No timeout, output overflow or supervisory cleanup signal.

Exact outer supervisor source used:
```sh
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B - <<'PY'
import os,sys,time,json,hashlib,selectors,subprocess,signal
argv=['/Library/Frameworks/Python.framework/Versions/3.11/bin/python3','-B','/Users/jd1/code/apps/outbreak/web/runtime/pair-smoke-v4/run.py','--pins','/Users/jd1/code/apps/outbreak/notes/decisions/D165-candidate-pair-runtime-pins.json','--pins-sha256','9bc78e0057418732e047b2928151b38bb4a955d6eaa18d9eb4f6b7a73ab85635']
env=os.environ.copy()
env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None);env['PYTHONNOUSERSITE']='1'
start=time.monotonic(); cap=8*1024*1024; buffers={'stdout':bytearray(),'stderr':bytearray()};fault=None;signals=[]
p=subprocess.Popen(argv,cwd='/Users/jd1/code/apps/outbreak',env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
selector=selectors.DefaultSelector()
for stream,name in ((p.stdout,'stdout'),(p.stderr,'stderr')):
 os.set_blocking(stream.fileno(),False);selector.register(stream,selectors.EVENT_READ,name)
try:
 while selector.get_map() or p.poll() is None:
  if time.monotonic()-start>=590:fault='whole_cli_timeout';break
  for key,_ in selector.select(.1):
   chunk=os.read(key.fd,65536)
   if not chunk:selector.unregister(key.fileobj);continue
   if sum(map(len,buffers.values()))+len(chunk)>cap:fault='combined_output_overflow';break
   buffers[key.data].extend(chunk)
  if fault:break
 if fault and p.poll() is None:
  os.killpg(p.pid,signal.SIGTERM);signals.append('SIGTERM')
  try:p.wait(timeout=5)
  except subprocess.TimeoutExpired:
   os.killpg(p.pid,signal.SIGKILL);signals.append('SIGKILL');p.wait(timeout=5)
 else:p.wait(timeout=max(.001,600-(time.monotonic()-start)))
finally:
 selector.close()
 p.stdout.close();p.stderr.close()
result={'calls':1,'argv':argv,'cwd':'/Users/jd1/code/apps/outbreak','env_policy':{'unset':['PYTHONPATH','PYTHONHOME'],'set':{'PYTHONNOUSERSITE':'1'},'other':'inherited'},'supervisor_python':sys.version.split()[0],'elapsed_seconds':time.monotonic()-start,'limit_seconds':600,'work_limit_seconds':590,'output_limit_bytes':cap,'fault':fault,'exit':p.returncode,'child_reaped':p.poll() is not None,'supervisor_signals':signals,'streams':{k:{'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest(),'text':v.decode('utf8',errors='replace')} for k,v in buffers.items()}}
print(json.dumps(result,sort_keys=True))
sys.exit(p.returncode if p.returncode is not None else 125)
PY
```

Exact parsed controller stdout:
```json
{
  "P0": false,
  "authority": false,
  "captures": [
    {
      "bytes": 877224,
      "client": "A",
      "height": 675,
      "path": "/Users/jd1/code/apps/outbreak/web/transport/results/candidate-pair/runtime-D165-pair-1/view-A.png",
      "sha256": "40b1c6025d9a458edc7a67b7fd98fed8c7852ed126675c964838cad36b36b8f2",
      "width": 1200
    },
    {
      "bytes": 890254,
      "client": "B",
      "height": 675,
      "path": "/Users/jd1/code/apps/outbreak/web/transport/results/candidate-pair/runtime-D165-pair-1/view-B.png",
      "sha256": "25db42764aed4f2b46bf59e53585d55025b1414f1d97a2e96a51fee9ac43f8b3",
      "width": 1200
    }
  ],
  "final_inventory_sha256": "3b12065fc4958707a2a3cbcd266b9c0177cad2fa4edb1e7f934ce14650715444",
  "ledger": {
    "path": "/Users/jd1/code/apps/outbreak/web/transport/results/candidate-pair/runtime-D165-pair-1/ledger.json",
    "sha256": "655e43e24e77cc4a7f9a216659679e8ed4ced605efbeb8416f3528e7d03fd606"
  },
  "receipt": {
    "path": "/Users/jd1/code/apps/outbreak/web/transport/results/candidate-pair/runtime-D165-pair-1/receipt.json",
    "sha256": "502dabec1278aaa4b3c6d01a2f25e48c92aaa8034fe7d848fa193512edf69d55"
  },
  "runtime_started": true,
  "status": "PASS"
}
```

## Actual observed proof and accepted controller closure

PASS: actual native startup, two loopback connections/two logins/map rev2 and two distinct gateway UDP sessions53485/58336. Both real C++ browser clients BN_ACTIVE: A cn0/life1, B cn1/life0. Child OBSERVATIONS_COMPLETE, errors[], sample_faults{}, evidence_complete:true; two active clients/two movement directions/two real captures. Parent evidence_validated:true, errors[], no evidence overflow; proof movement_directions2. No fixture, replay, mockup, state injection or controller-generated peer echo substitutes for this run.

Ordinary W250ms then release, without action retry:
- A to B: own XY displacement4.076726426579651 units; receiving parsed XY error0.010863110645664916; parse_count47→60 and last_parse_ms2500.8→3216.2; observation372.2196670000012ms after release.
- B to A: displacement3.916223084939468 units; error0.02713578841345672; parse_count17→30 and last_parse_ms3785→4419; observation374.41912500000035ms after release.

Both captures occur after both movement proofs with stable current actor/life and advancing public timing/rendered counters. A capture279.77379199999996ms, frame259→272/rendered257→270; B268.16095900000073ms, frame241→252/rendered239→250. PNG signature/dimensions/size/hash and ordinary0600/single-link metadata checked in read-only retained-file inspection; parent performed full capture validation. A877224bytes and B890254bytes, both1200×675, combined1767478bytes. Actual paths:
- /Users/jd1/code/apps/outbreak/web/transport/results/candidate-pair/runtime-D165-pair-1/view-A.png
- /Users/jd1/code/apps/outbreak/web/transport/results/candidate-pair/runtime-D165-pair-1/view-B.png

Report intentionally remains OBSERVATIONS_COMPLETE_PENDING_CLOSURE: source only lets the last atomic receipt announce PASS. Final receipt PASS/errors[] links report SHA664d86b81ed58902692896c7a0aecbe774ff689e3c249958bdaf314f14e3d725 and ledger SHA655e43e24e77cc4a7f9a216659679e8ed4ced605efbeb8416f3528e7d03fd606; both match retained raw files, as do receipt capture refs. Returned receipt SHA502dabec1278aaa4b3c6d01a2f25e48c92aaa8034fe7d848fa193512edf69d55 matches raw file. Final prospective inventory SHA3b12065fc4958707a2a3cbcd266b9c0177cad2fa4edb1e7f934ce14650715444. Ledger original SHA70fa375a6e9a6b3ae4ce7da0f28429d8fcbdb016220286fa67b38f4f688d23f6, terminal slots ledger.json/receipt.json. Controller source requires original-UNION checks, final pure admission revalidation, capture inventory and cleanup before atomic seal; worker did not repeat these gates.

Whole CLI147.101s includes preflight pure checks; receipt effect/terminal interval81410.14733305201ms is below180s, report runtime/cleanup13319.150708033703ms, child5678.717625ms. These intervals are distinct.

## Retained hashes

All entries below are under /Users/jd1/code/apps/outbreak/web/transport/results/candidate-pair/runtime-D165-pair-1/, ordinary0600/single-link.

| File | Bytes | SHA256 |
| --- | ---: | --- |
| receipt.json | 1207 | 502dabec1278aaa4b3c6d01a2f25e48c92aaa8034fe7d848fa193512edf69d55 |
| report.json | 216432 | 664d86b81ed58902692896c7a0aecbe774ff689e3c249958bdaf314f14e3d725 |
| ledger.json | 7870 | 655e43e24e77cc4a7f9a216659679e8ed4ced605efbeb8416f3528e7d03fd606 |
| validated-plan.json | 57269456 | 932bcee7bdcf7da5325651f4c98af92f4b5a5301116540c57d57075837a97f62 |
| native.log | 1168 | 34ee7b83b2a177072fbfb48c117383bfcd95bca8b6b7aaf7d832a67e772b3c09 |
| stdout.log | 60177 | 4f362d3cac331dd27393587b17f5ceb9b00534b2443d3d4a88373d0b043373eb |
| stderr.log | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| view-A.png | 877224 | 40b1c6025d9a458edc7a67b7fd98fed8c7852ed126675c964838cad36b36b8f2 |
| view-B.png | 890254 | 25db42764aed4f2b46bf59e53585d55025b1414f1d97a2e96a51fee9ac43f8b3 |
| browser-ownership.json | 376 | 1034530d3339846eda766a05baa5cfa7f47c56039819e85ec08dcf82169fd1df |

Native sandbox: /Users/jd1/code/apps/outbreak/web/server/run/candidate-pair-D165-pair-1/.

## Recorded cleanup and limitations

PASS recorded cleanup: native SIGINT exit0 in56.330875027924776ms; no kill fallback; groups_reaped/ownership_complete:true. All134 inspector handles reaped. Keys released, contexts closed, browsers stopped, gateway/static closed, handles empty, ports released, profiles/private entropy removed. Gateway close0.8866669999988517ms. Targeted post-terminal lexists confirmed both browser-temp roots and native private/entropy.dat absent. No manual live ps/lsof/socket probe or extra signal. These are retained controller records and exact private-path absence checks, not a fresh system-wide process attestation. No owned process remains live according to authoritative completed/reaped controller and cleanup records.

Actual loaded private SDL2 and nested hidapi paths are exactly admitted D121-native-1 deps-signed paths, with controller signature/hash checks. Other mappings include admitted release/ac_server and /usr/lib/dyld; system image bytes explicitly NOT ATTESTED. macOS Darwin Kernel25.5.0 ARM64_T6031 recorded, no hardware/performance result.

After terminal, read-only pins size/digest and all nine current source hashes rechecked unchanged; report/ledger/capture hashes cross-linked to receipt. An initial retained-data tool wrapper ended with a JavaScript TypeError after the successful read-only command had returned JSON; this affected no files/runtime/result, and a subsequent retained-file summary read completed normally. No runtime retry occurred.

Runtime behavior and images are actual; automated PNG/proof acceptance is distinct from MAIN visual review and owner/human acceptance. Native per-position logs NOT OBSERVED; no server-authority, damage, gameplay, reconnect, performance, hardware, full system-image, P0/MVP or human acceptance claim. T136's separate approved probe remains consumed FAIL/no retry; QA stays paused. MAIN owns actual image review, ticket acceptance and quiescence lift. World stops after this handoff; no further execution or workspace changes authorized.

