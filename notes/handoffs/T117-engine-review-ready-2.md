# T117 review-ready checkpoint 2 — D137 corrections

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket: T117 revision1.4, existing RELEASED unfrozen exclusive preparation lease.
- Contracts: CANDIDATE_PAIR_SMOKE0.5, CANDIDATE_RUNTIME_ADMISSION0.4; D134 checkpoint and D137 returned findings. D139 dependency update read.
- State: REVIEW-READY, NOT FROZEN. Explicit MAIN checkpoint clearance remains required; no status/acceptance change is made here.
- Base/pre-existing edits: original repository and separately reviewed compiled artifact source bdaa8df7. No Git commands/mutations, commits, old source/evidence/artifact/SDK/cache/admission changes or unrelated edits.
- Changed: allowlisted pair-smoke policy.py,supervise.py,ownership.py,observe.cjs,test_policy.py,test_observe.cjs,SCHEMA.md,README.md; run.py unchanged but included in the nine-file candidate. New numbered preparation evidence and this own handoff only.

## Acceptance evidence

PASS — final inspected guarded FIXTURE_ONLY builtin commands, cwd /Users/jd1/code/apps/outbreak:

```sh
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node web/runtime/pair-smoke/test_observe.cjs
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B web/runtime/pair-smoke/test_policy.py --review-ready
```

Final results: Python40 tests/0failures/0errors; Node24 tests/0failures. Both record actual_effect_attempts:[], actual_runtime:false, authority:false, P0:false. Audit/patch guards precede project imports. Real subprocess/socket/browser/process-control/effect APIs remain forbidden. Filesystem negatives only use owned preparation fixtures; the outside-attempt sentinel is inside the preparation directory and remains byte-identical. Destructive cleanup of real profiles/entropy and actual image inspection were NOT RUN.

Exact evidence, relative to web/runtime/pair-smoke/preparation-T117-1:

| Record | SHA256 |
| --- | --- |
| review-ready-5.json | 6fb3c97068e983a97b78194fe875b35ce849e037566e636482672abcdd186915 |
| python-result-5.json | 4384b402a90de13f09e43bcfcdae2eda65953e03520982277758073f646c801f |
| node-result-7.json | b256f651d576dfed73a0410d7694e4bbf8141e12141f44cc99b1b0c595775105 |

Full final logs are python-test-5.log and node-test-7.log. The review record binds all nine current hashes, retained preparation file inventory and governing ticket/contract/decision/review hashes. Python result independently binds all nine; Node result binds observer/harness. Earlier review-ready-3.json and receipts/logs remain unchanged. Intermediate Node4/5 failures are retained: the new pending-acquisition wait initially requested beyond the fixture's <=30s operation bound, corrected to <=20s cleanup reserve with the acquisition wait included in cleanup elapsed time. Node6 passed22 tests; Node7 passed the final24 after additional timeout/root-confinement coverage. Python4 passed40 on the intermediate candidate; Python5 is the current complete binding. No earlier result is relabeled or overwritten; no freeze record generated.

## Exact review candidate hashes

All paths relative to web/runtime/pair-smoke:

| File | SHA256 |
| --- | --- |
| policy.py | 1d66a7e4a85786015036b0e3f25ce923f40de51a1d3f14746e8b1d589a0d6f81 |
| supervise.py | eafc4bb88a7894fcc130be19c0e6323fb029b2296da66c615d7bda37f8f06488 |
| ownership.py | 9bbc5880b7252de7515055c814dbca45d5d771c76c85750f8d6266f6bd5b108d |
| observe.cjs | 852c48f1263a517039fb49b1424783b7d99fa47e970a7663b2a91c5294cc3736 |
| run.py | b2d251c2bf071cab4cb93588c0df0ce2143bc89fbf338fe2d2d1fe2a794211bc |
| test_policy.py | ab6d69f9fcbdd8feb539b0f4c708074f579dbb9133d8786b441d6a0d81794037 |
| test_observe.cjs | cccae06049866bc02f9674b59ab210cd47e626d6f18b30827072ad929b4c6e39 |
| SCHEMA.md | cd309cbf0cc9b8c9d1b0150a71e36dad867ef0202faf7b43898f51f2d3a9f7d0 |
| README.md | 85a49f916d8d62f54a20449d1836348d3c7d8bacdeb2f24b032cad496772dde2 |

## Implementation status against MAIN's five findings

1. Private confinement — parent pins device/inode identities for ordinary canonical ancestors, attempt roots/native/private and both precreated profile roots before child launch. Cleanup walks O_DIRECTORY/O_NOFOLLOW descriptors and checks pinned identities, then performs descriptor-relative operations. Entropy requires ordinary single-link fstat identity before bounded chunk overwrite/fsync/unlink; profile traversal never follows links and rejects hardlinked/special files. Replaced ordinary profile roots also refuse. Deadline checks occur during traversal/chunks. Guarded test36 covers hardlinked entropy, linked entropy/ancestor/profile root and same-name ordinary ancestor/profile replacement, preserving sentinel bytes.
2. Actual mapped images — lsof -Fftn parsing now honors process/file record boundaries. Both admitted copies require txt/REG mapping records; numeric open FDs do not prove loading. Any foreign mapped SDL2.framework or hidapi.framework refuses. System and unrelated mappings are retained honestly; system bytes remain NOT ATTESTED. Tests33/38 cover valid record shapes, FD-only/type negatives, foreign mapped frameworks and unrelated observations.
3. Owned single-link ledger — every newly owned ordinary file requires exact {bytes,sha256,mode,nlink}, valid finite types/hash/mode and nlink1. The same additions gate runs on initial/final/prospective receipt inventories, covering ledger/receipt slots. Test37 rejects nlink2 native.log, bool link/size values and invalid mode/hash.
4. Failed early gateway cleanup — gateway_observations retains structured bounded snapshots independently of trace, including acquisition/admission and pre/post close. Final state is sampled even when bounded close rejects/times out. Parent unions valid tuples from every retained snapshot plus receipt/final; empty/missing final state cannot erase A's earlier UDP tuple. Python39 and two full observer Node cases cover one-admission/second-launch failure with rejected and timed-out close and continued static cleanup.
5. Deferred/late ownership — all work ops use thunks checked before invocation and again after deferral. Acquisition scope registers pending ownership before factory invocation for gateway/static/launchServer/browser/context/page, retains settlement handlers through timeout and cleanup timeout, waits within the20s/absolute180s cleanup reserve, and bounds disposal of late results. Late launch PID/control/profile facts are retained before close, even if ownership persistence fails. Failed/unresolved disposal is explicit failure; parent proof rejects any non-owned acquisition row. Node regressions cover direct/deferred cutoff, delayed results for all six resource roles, disposal rejection, unresolved cleanup then late settlement, and full late launch ownership/reaping. Python40 rejects pending/disposing/disposed/failed/rejected acquisition rows for a purported successful proof.

Private schema now documents gateway_observations and acquisitions and the confinement/mapping/ledger rules. Existing five T118 fixes, D126 native evidence, D129 self-row, D132 narrow tool-role rule, literal admission_v4 seam, ordinary-input movement/timing and false-claim gates remain. No new dependencies/assets/public API/schema/wire/gameplay changes.

## Integration and limitations

All new process/Page/port/gateway/admission results are FIXTURE_ONLY doubles. Future effectful source is authored but uninvoked. Guarded negative filesystem fixtures do not establish actual OS cleanup/browser process integration. D137 accepts the separate v4 component and D139 accepts T125's separate actual read-only validation; those records are not this controller's own current admission call or a reusable execution token. This task made no actual v4 import/call, CLI/service/browser/native/inspector/socket/network/compile/install invocation. Actual two-way smoke, loaded-image/cleanup/deadline observation and performance/human/P0/MVP remain NOT RUN; no build/performance hardware claim is made.

Requested MAIN action: review this exact corrected candidate and evidence before freeze; return further in-scope findings or grant explicit checkpoint clearance. Controller acceptance, exact current source/tool/tree/preservation pins and explicit one-use effect release remain later gates. Player/QA/T103 holds remain unchanged.
