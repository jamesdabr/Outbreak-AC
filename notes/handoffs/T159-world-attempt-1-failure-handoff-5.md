# T1591.9 actual attempt-1 failure handoff

- Worker: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Lease: T1591.9/D258/WORLD_QUERY_FOUNDATION0.6, ONE fixed actual invocation; no repair/retry/source modification.
- Base: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work; no Git invocation/mutation.
- Writes: the fixed caller created NEW tests/outbreak/geometry/G1/attempt-1/** including its owned SDK copy/partial compiler evidence; this own NEW post-terminal handoff. All source/docs/dependencies/preparation/history and MAIN caller remained read-only.
- Disposition: **ACTUAL FAILURE, preserved and stopped. Outer exit1 after child0 supervision refusal. Not REVIEW-READY, accepted or frozen.**

## Authorized fixed invocation and observed terminal outcome

Read D258, ticket1.9/foundation0.6, fixed-caller review and final preparation preflight before execution. Revalidated source6b11f5a003eafe0d53a2ec727e3730e59f7ddb81d8a8c0c5d6673c3376ebe736, all12 prepared artifact hashes, installed rules333b6d0717fbb9b75b74aa96426f8180ad443b49c1acf5711f2a73a7c218da5e, fixed Python/compiler/linker/Node hashes, no preparation refusal marker and absent attempt-1. Fixed caller is1527bytes/0644/single-link, SHA25676d18838a44d1aa9432f4ed39031b63864a686af2ceb4d90c050e086219a733b. No alternate caller or source entry was used.

Exactly once from `/Users/jd1/code/apps/outbreak`:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -B /private/tmp/outbreak-T159-approved-caller-1.py
```

Initial tool chunk8b86e6 returned running session22367 with empty output. The SAME handle was polled; final chunkc339d7 reported **exit_code1**, with the traceback ending `RuntimeError: actual child refused: 0` at verify.py2604. No observation timeout/restart, second caller invocation, diagnostic probe, retry, repair, alternate flags/entry or source change. Subsequent actions were read-only file inspection/hashing and this new handoff.

Caller binds D258 SHA2569845d3796b093779ba0be3c704c46b501dd1089fbf7004c6763cc4dbeba7fdd8, prepared manifest7b17533605648a6064e582de288c1f4677c70a991db5cd7619cd59618928d862, accepted installed rules333b..., and observed successful prior preparation. MAIN caller review is1b9ecea9dbd321d80d9979a351e0263130bc52fe9723e568437f3af2a4f83eb0; MAIN preflight receipt8024318ce36c830d5c2fec16b9148832ba56c0f9533e13c41d6ff3b5ef829ce5; independent preflighta2af42791b9cee28636a38552a8b929a2e672b649e2eb26ad1a9025d265b5504. These identities were inspected, not amended.

## Concrete failure and original ownership facts

The first prepared command was the native object compilation of source/outbreak/p1_geometry.cpp, exactly:

```
/usr/bin/clang++ -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk -std=c++11 -O2 -Wall -Wextra -Werror -I /Users/jd1/code/apps/outbreak/source/outbreak -fstack-usage -MD -MF /Users/jd1/code/apps/outbreak/tests/outbreak/geometry/G1/attempt-1/native/geometry.d -c /Users/jd1/code/apps/outbreak/source/outbreak/p1_geometry.cpp -o /Users/jd1/code/apps/outbreak/tests/outbreak/geometry/G1/attempt-1/native/geometry.o
```

Compiler exited0 and produced geometry.o, geometry.d and geometry.su. Stdout/stderr are both0 bytes. The refusal is therefore an actual supervision/platform error, not a compiler diagnostic or a discovered geometry mathematical counterexample.

Final receipt in failure.json reports:

| Fact | Observed retained value |
| --- | --- |
| Original PID / owned process group | 60416 /60416 |
| Nonreaping anchor bound / confirmed before cleanup | true /true |
| Last native waitid result /errno | 0 /0 |
| Terminal waitid event | SIGCHLD20,CLD_EXITED1,PID60416,status0,returncode0 |
| Primary supervisor error | group-probe,PermissionError,`[Errno 1] Operation not permitted` |
| Mutating group signal attempted | false |
| Original handle reaped /wait attempts /returncode | true /1 /0 |
| Later owned group observed quiescent | true |
| Close attempts and completed closes | stdin,stdout,stderr,selector; all four |
| Release skipped | none |
| Child output seen /retained | 0 /0 |
| Retention complete | true |
| Final receipt ok /state | false /FINAL_REFUSAL |
| Child elapsed including cleanup/retention | 0.672243042034097 seconds |

The reviewed backend's group-probe operation is the nonmutating `os.killpg(original_pid,0)`. The pre-reap probe raised the recorded PermissionError; unknown group state correctly did not trigger a mutating signal. The source subsequently reobserved the anchored child, reaped that original handle, and reported later nonmutating group absence. No independent process discovery/attachment/group test was executed after failure. The receipt's quiescence/reaping facts do not erase the earlier refusal.

The fixed D235 lazy adapter/library boundary genuinely ran for this owned child and retained a valid104-byte terminal record. This establishes only the observed terminal call outcome in this failed operation, not blanket platform support, all no-event/signal/error paths or complete descendant cleanup proof. No separate FFI capability probe, library selector, helper process or fallback was used. The runtime PermissionError is not represented as an automatic approval-review rejection; no such rejection was returned by the execution tool.

Outer failure ledger records phase timing2.069148375070654 seconds, sampled before failure.json durability; it is NOT a separately measured complete outer elapsed value. The original300-second whole/60-second child cutoffs were not reset, and no timeout or output cap overflow caused this failure. The later outer exit1 is the terminal observation. No graceful-success claim is made from those partial timings or from the retained object.

## Retained failure and partial artifacts

Prefix tests/outbreak/geometry/G1/attempt-1/. Read-only hashes/sizes:

| Member | Bytes | SHA256 |
| --- | ---: | --- |
| FAILURE | 54 | 02ff810742b776a8f03757fc4db1a7ac8702984f60602a10e97aaa6213f56933 |
| failure.json, final process receipt | 2355 | 160218d7a3508cde03f94b67bfd5d6b6204ee12dfc180ecd7030a40cf7a5da3e |
| logs/00.provisional-receipt.json | 1797 | 418bbec6ed8a6c907fe5a507a74a8695848ed339cae7e344e9986687dafd6cb2 |
| logs/00.stdout | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| logs/00.stderr | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| native/geometry.o | 56528 | ef8abc9443727c88f7af24469c5dde88b756ab15a7caf0956b2282a619bcb44c |
| native/geometry.d | 19179 | 6f199fc45c90451fce0c6386a81e24f7a95ed7f5cabdff460caccc37f549c62b |
| native/geometry.su | 4469 | c993e69ee70fb2bfc6ba1570da66b808ef9f2e5909252b32fc415862875c530d |
| inspected-plan.json | 32815 | 6766921616b05342864fea861a692abefcc3a14db4849290334d5452630a77d2 |
| setup.bin | 915564 | b96adfac57cc4a3b51768d86a9a92206d92199ea9359ca08c9b4e1f2bb2064a9 |
| corpus.bin | 2709120 | d6f1a202961c82cccde81a003aca448aa54942c5f077055907482d46b0d6a642 |
| expected.bin | 2686976 | 580ead76672dce81f30b50cee37b70f59a87c62008e2d9b61a16803aa55d3ad5 |

Owned attempt-1/cache/sysroot copy and task-owned tmp/xcrun_db are also preserved. The preparer verified copied membership/kind/mode/bytes/hash/exact accepted symlink targets before launching child0; this is not a final freeze inventory. tmp/xcrun_db hashes202037e35b49daf10bd7159bf5f1b54c0c738799a2be1891894d78fa0b2eeef9. No original SDK/cache was copied over or repaired.

`rg --files --hidden --no-ignore` was used for the partial non-cache inventory so the ignored geometry.o was included. All observed native artifacts/logs/FAILURE/failure.json are ordinary0644/single-link files. Provisional receipt intentionally says BEFORE_FINAL_RETENTION_CHECK; final retention/elapsed/ok/state are in failure.json. Do not substitute the provisional receipt for final success. FAILURE text is `T159 incomplete/failed actual attempt; do not consume` and remains present.

No manifest.json, processes.json, frame-analysis.json, actual-dependencies.json, review-ready-owned-graph.json, native.responses.bin or wasm.responses.bin was produced by the run. It stopped on the first run_child refusal before the remaining25 prepared commands and both targets. No actual expected-response comparison occurred. The partial depfile and stack-usage file are raw compiler evidence, not a completed dependency closure, full normal-call-chain proof or a largest-frame substitute.

## Protected input observations and limits of the failed run

Before attempt creation, the fixed actual entry successfully checked its reviewed clearance, prepared identities, full accepted G0 binding, exact source/dependency/tool/argv/environment records, D235 inputs, target-separated header candidates/SDK aliases, original SDK graph, full schema and semantic coverage. It then created refusal marker, owned directories, verified owned SDK copy and retained exact prepared setup/corpus/expected bytes. The failure occurred at first child supervision, so the workflow's final protected after-graph/full normal-frame/dependency/export/ABI/oracle checks were **NOT REACHED**. No final all-protection PASS is claimed.

Read-only post-terminal hashing independently confirms the immutable5 harness/docs,3 production geometry/store files, live rules/header/angles, all12 preparation2 artifacts and fixed caller stayed hash-identical. Key pins remain verify6b11f5a003eafe0d53a2ec727e3730e59f7ddb81d8a8c0c5d6673c3376ebe736; geometry.h8bfa5558899bcbaa172ce8a4ab38df3f48cae8468e9b43c976ad0e047e096a90; geometry.cppbf30f77b8c9e7d51a641c27597484cec58c005569178551dd8e744d3e4fbf385; store.h7a7b185ddba685cfdf313398c24558e54abb1ca674d2e305793e27420d4c0bc3; installed rules333b...; preparation manifest7b175...; caller76d188.... No post-failure project helper, generic graph verifier, symbol/ABI/system/process probe or alternate native command was run.

## Acceptance evidence and next gate

| Obligation | Result |
| --- | --- |
| Fixed reviewed caller once | EXECUTED; observed outer exit1 |
| First native geometry compilation | Compiler exit0; partial artifacts retained |
| Child0 supervisor/ownership proof | FAILED group-probe PermissionError; original reap/close/later quiescence reported |
| Remaining25 compiler/link/version commands | NOT RUN |
| Both16384-row native/Wasm targets and oracle equality | NOT RUN |
| Full frame/normal-helper/caller/ABI/export/dependency proof | NOT RUN /INCOMPLETE |
| Final protected graph and REVIEW_READY terminal | NOT REACHED |
| Failure root and marker | PRESERVED |
| Repairs/retry/source changes/freeze/acceptance | NONE |

No numerical/API/row/stack/time/output limit was relaxed and no production counterexample was inferred from the platform refusal. MAIN must review the retained error and decide any future environment/lease/path; this worker does not repair or retry under D258. All actual artifacts/source/preparation/caller remain stable for that review. Full G1/G2/caller/gameplay/runtime/P0/MVP/RSS/performance/human/Player/QA/T149 holds remain unchanged. Worker stops here.
