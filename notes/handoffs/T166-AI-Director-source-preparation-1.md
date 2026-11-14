# T166 isolated source and guarded pure preparation

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket / revision: T1661.0, RELEASED SOURCE + GUARDED PURE PREPARATION ONLY D231; authoritative status unchanged by worker.
- Governing: RULES_INITIALIZER_FOUNDATION0.1/D231, accepted T165 packet as supplemented by final reviewdc0a52841ed9e00390ea44d7efa27176fe1c6d37b1927997f8805ecaabc751e2, unchanged accepted rules/basis/hash/fixed/table contracts and D196.
- Base / pre-existing work: ticket base bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work; no Git command/mutation. The isolated candidate root was absent. Live rules913ce... and all World inputs/T161 failed evidence stayed read-only.
- Changed files: exactly the eight released files under tests/outbreak/rules_initializer/candidate-1 (baseline/p1_rules.cpp,candidate/p1_rules.cpp,verify.py,test_supervisor.py,wrapper.cpp,wasm_runner.mjs,SCHEMA.md,README.md), five published preparation-1 records and the temporarily created then durably removed FAILURE slot, plus this own new handoff. No actual/fixture namespace or additional candidate-root file.
- Commit / patch reference: none.

## Acceptance evidence

PASS — exact baseline/candidate source authoring: complete9982-byte913ce462a5c3896d766adc66751f278d188462ee6b3b97973269d976b3cf00b2 baseline was preserved FIRST and never edited. Candidate is exact10008-byte333b6d0717fbb9b75b74aa96426f8180ad443b49c1acf5711f2a73a7c218da5e reconstructed from the adopted three-hunk text diff, not retuned source. Its4459-byte suffix remains30bf84eaea9ed7d92e41514280b1e1b69eaf4b0b72f2b40a23eccb566b07eecd. No candidate headers/table/include shadows. Live cpp/header/data unchanged.

PASS — new verifier/wrapper/runner source, not executed target evidence: adopted3 factory+143 validator/mutation+116 basis ordered union; independent70 approved constants,200-byte canonical encoding/SHA512, certified-table reflection/isqrt/trunc basis oracle. Actual wrapper exposes every defined factory byte/hash, actual status/Faults/six basis components, guards/input retention before mutation restoration and pristine state. Four-unit graph correctly uses p1_hash.cpp,fixed.cpp,exact candidate,new wrapper. All18 future object/assembly/link argv,2 target argv,4 version argv and fixed future fixture-child argv are pinned; no historical suite executable/import or108257 replay.

PASS — ONE inspected guarded pure generation, observed process exit0:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/rules_initializer/candidate-1/verify.py --prepare
```

It returned prepared:true,actual_proof:false,rows262,requests4192,expected7864 and the pins digest below. This was the sole preparation invocation; no retry/overwrite/source change after publication. FAILURE was created/flushed/fsynced before generation; file/parent-directory durability operations returned successfully, five complete records were re-read/hashed before final unlink+directory fsync. Source/data role bytes1591157 plus generated record bytes104627=1695784, below8388608; tool-role binaries separately streamed for exact hashes without executing them. Elapsed before final publication~0.364s within original300s. Final output was one small JSON summary, below8MiB. Named reads103, no broad SDK/unrelated-tree scan; all103 ordinary inputs plus tools/alias context checked unchanged during generation and rehashed unchanged after terminal observation.

EXACT prepared counts/bytes:3 factory,143 mutation,116 basis=262 rows,4192 request bytes,7864 expected response bytes/target15728 both, one target batch. Family counts:84 boundary basis,16 fixed cross,8 invalid pitch,8 corrupt-table priority; one pristine validator,70 scalar mutations,64 rule-hash mutations,6 numeric table mutations,2 table-hash mutations;3 poison factories. All independent expected material generated under stdlib-only/process-network-signal-wait-tool-SDK-copy/old-import guards. The preparer only AST-reads the literal42 future fixture names; no own supervisor module import or fixture call.

PASS — stable source/preflight publication: preparation-1 contains ONLY pins.json,plan.json,corpus.bin,expected.bin,cases.json; FAILURE absent after successful durable final gate. Neither attempt-1 nor supervisor-fixtures-1 exists. Preparer/source inputs were not edited during/after the call. Missing marker alone is not evidence of success: the observed exit0/prepared:true gate and exact records jointly establish this limited preparation result.

NOT RUN — actual compiler/link/tool/version/supervisor fixture/target/SDK-copy/project import or live installation: all corresponding invocation counters0. Forty-two mocked boundary cases are AUTHORED/PINNED FUTURE PLAN ONLY, not passing fixture evidence. No actual native/Wasm output, emitted-code/callee/frame/zero-init/readonly/timing proof exists for this candidate. No actual REVIEW-READY/final freeze acceptance claimed.

## Preliminary review disposition

Read provisional notes/reviews/T166-preliminary-source-review-1.md SHA3ef98f24855825aafb8b56fbb9a6b9adc254bf2e7488f8b6aeb9ca29fe7ad12b; it names earlier evolving pins and is not final-source clearance. All three findings were addressed BEFORE consuming the one generation:

1. Durability: confined prep helpers use unbuffered writes, explicit flush/fsync, parent-directory fsync (including candidate-root parent for new preparation directory), durable initial FAILURE and durable final removal. Primary and secondary close/durability errors retained without fresh budgets. Future Files/Terminal and fixture publication use the same explicit file+directory durability operations, with original cutoff and retained unresolved original handles. Future fake FileIO boundaries cover flush/file-fsync/directory-fsync/close/late-fsync, without invoking real FS effects for scenarios.
2. Whole clock: BOOT_STARTED is taken before remaining stdlib setup/function definitions; prepare and actual use that same original deadline. Future actual prepared-input/tool hashing, own helper import, reservations, fixture/build/target/protection/guard/terminal phases no longer obtain a new300s envelope after setup. Before further mutating reservations/actions, original positive reserve is checked.
3. Guard lifecycle: new factored SignalGuard backs up prior handler/timer, refuses a preexisting nonzero timer without alteration, records every attempted acquisition inside the actual protected try, independently attempts bounded restoration of each attempted resource, and durably records guard facts. Restoration must succeed BEFORE final success result/marker removal. Finally is idempotent and performs no repeated/post-publication mutation. Acquisition, restoration failure/late deadline and untouched preexisting-timer scenarios are included in the42 future fake methods. No actual signal/timer/fixture was used in preparation.

These are source/preparation dispositions; future actual-method mocks, emitted objects, real process receipts and final acceptance remain separately gated. No request to waive any existing contract or repeat the preliminary mathematical audit.

## Stable SHA256 identities

Under tests/outbreak/rules_initializer/candidate-1:

- verify.py44841B:d38ea43727b7c14daa1ecf3676445efa6231e41cdaaa0933499235c08e22711b
- test_supervisor.py31015B:05535daa3745350d243d34071bd0d7b688a2842fcbcd938e324bf68301b88a26
- wrapper.cpp20445B:2c917b4363d66f71a759ef7c8acd3bbfc4a00358f090ddc81c54cd8f3668d862
- wasm_runner.mjs1279B:84f8646ac35f3101ec7d2c5bb347eaeabbdcb5acd78f14172491f81bd344ca2b
- SCHEMA.md13406B:3e77fd6ecd90497e49ba791d5c0a72b98af7ac3b6d3c908d54f36c280139e2ae
- README.md3781B:32371b04172f889d9658f0c734eb1e09df2b811195ad4d8510486e4052929818
- preparation-1/pins.json28326B:e8037e25ce15fae4dcfbf901eab501c250996d2bf8b358b816f4813cb66c2dda
- preparation-1/plan.json30394B:a77c3183877e96d8d7894d3ebe0a06ab0f3a5276a44607c730f32514608d72b4
- preparation-1/corpus.bin4192B:00143098f1f8c4889b14ed10011c14c9748d5f6775699fcadf118c5b48e6fdd4
- preparation-1/expected.bin7864B:b0efcfd86cb818d3de1f1f906b2783619a946cfe07a0131b9b84621ba60d65bf
- preparation-1/cases.json33851B:620820c431803270b10fc01130a87802b25b42d0911339d0fe3a8a1217fbf8f0

Baseline/candidate/suffix pins are stated above and bound in generated input records; pins self-hash is externally bound here, not a self-referential JSON row. No final inventory/freeze file was created.

## Implementation status and remaining gate

Exact isolated candidate and future verification/controller source are authored; only pure expected-data preparation actually ran. Current new source contains complete future same-O2 four-root normal-callee graphs for both targets, partial-failure retention, unknown/indirect/recursion refusal, native/Wasm complete conservative frames plus local charges, D196 explicit corruption-abort qualification, actual object/assembly readonly/constant-elimination/zero-init/old-copy checks. All remain unexecuted. No guessed system-helper cost, fake memory shim, source/flag/cap tuning or claimed stack reduction.

Future supervisor retains original process/FS handles, checks original absolute deadlines before eligible mutation/wait, independently retains primary/secondary/late/unresolved facts, caps before byte retention and restores signal ownership before terminal publication. Future artifact result is evidence-only passed:false; final observed exit0+stdout gate remains required, so late unlink/write or missing marker alone cannot fabricate a pass. Kernel stalls/OS/VM/JIT physical limits are qualified rather than certified. This is source design, not real cleanup proof.

## Integration and authority

Ticket/contract reread before submission, still authoring+pure preparation only. Live p1_rules.cpp remains913ce... and the preserved T161 attempt-2 failure still35ab9c8af2bc0d514f5f8dcf7277721c88dcdd6b34bf958d6497c2e67cf900ab; no World/G1 source pin retargeted or other worker dispatched. MAIN may review these stable pins and separately release any actual fixture/compiler/target proof. Current source/preparation will remain unchanged; no actual/fixture root creation or second generation without further authority. Candidate acceptance would still require separate exact-file installation/source-path qualification and new consumer pins, then full unchanged97755-case T161 proof. QA/T149/runtime/RSS/gameplay/P0/performance/full-phase/human holds unchanged.
