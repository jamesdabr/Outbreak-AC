# T169 retained rules controller and guarded preparation

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket / revision: T1691.0, RELEASED SOURCE + ONE GUARDED PURE PREPARATION ONLY / D242. Worker did not change authoritative status.
- Phase / contract: RULES_RETAINED_COMPLETION0.1; unchanged source/numeric/frame contracts and D196 qualifications.
- Base and pre-existing edits: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work. No Git commands/mutations.
- Changed files: NEW tests/outbreak/rules_initializer/retained-proof-1/{verify.py,SCHEMA.md,README.md}, NEW preparation-1/{pins.json,plan.json,branch-proof.json,retained-manifest.json}, and this own NEW handoff. The authorized initial FAILURE was durably removed on successful preparation; actual root remains absent. No old file was edited.
- Commit / patch reference: none.

## Acceptance evidence

PASS — source scope and inspection: initially absent retained-proof-1 was created under the exact allowlist. Fixed new controller implements only --prepare and separately gated future --actual PREPARATION_SHA256. Own source was inspected, parsed with ast without executing it, and the immutable supervisor source pin/top-level structure inspected before the one preparation. No original verify.py, main/fixture entrypoint, compiler, target or version was imported/executed. The sole explicitly authorized source exception reads test_supervisor.py6acaf1f7b98b93ef21b592630131d6b61f6270ca55ab71f424c3ebf78da9c4ae, verifies bytes and execs them in private non-main namespace under the preparation guard. No bytecode/path lookup or fixture execution. Only positive Files/FileIO methods publish preparation.

PASS — ONE guarded pure preparation: exact command from /Users/jd1/code/apps/outbreak:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B tests/outbreak/rules_initializer/retained-proof-1/verify.py --prepare
```

Returned session92391 was retained/polled to observed exit0, stdout PREPARATION_REVIEW_READY/passed true/requires_observed_exit0 true. Externally reported pins SHA256fb4e0cbd39ba13b1557eb59ed8ade6601dafcad77336311c2cf84611eb95ae08. No second invocation or repair/regeneration. Guards deny process/fork/exec, signals/waits, socket/FFI, project imports, unnamed reads/unrelated scans and writes outside the five literal preparation slots. Initial durable FAILURE precedes proof/data generation. All four final data records were written with file/parent fsync, rehashed, then FAILURE durably removed under the original clock. No original clock restart or fresh grace. Preparation artifact passed:false/actual_proof:false explicitly distinguishes it from the positive observed preparation terminal gate.

PASS — exact local control-flow/object proof: full object61e8e1739b712ff5497876f55a7b143425a99dbc09c6b56962bf58a89655dd90 and asmfd15561de23c80a0f39f0fd695562062a78f35b137ffea8a2a641c34c5661586 bind the adopted review7e066136694e2389be89c68acb3c9da743241d6c65119bea368992c8ff42b47e. Parser verifies arm64 Mach-O headers/sections/nlist, function0xb60..0x144c and text file0x328, table0x2798/file0x2ac0/140 bytes, defined readonly local table symbol, exact PAGE21/PAGEOFF12 relocations and all nine dispatch instruction words. Independently counted ASM labels reconcile ALL70 unsigned object halfwords, exact unsigned<=69 index/base/load/scale/default, distinct local targets and571-instruction function extent. Closed path traversal reaches ret on both paths of every case/default, rejects unknown call/tail/indirect/SP/LR/cycle/escape and matches the adopted whole function/table slice hashes. Existing paired .su measures the local leaf0 static bytes. No unknown callee is guessed or omitted by a pattern/name exemption.

PASS — finite discriminating pure tests:30 outcomes: actual positive,25 malformed ASM/object cases,4 graph-binding negatives. Every mutation applied and refused for the intended structural/binding reason; every outcome is retained in branch-proof.json. Examples: wrong bound/base/load scale, missing/duplicate/external table entry/label, object halfword mismatch, relocation/symbol/section mismatch, SP/LR mutation, extra unapproved error, unknown edge and changed measured frame/bound. No host child/signal/wait/fixture entrypoint was used. Sparse in-memory patches share baseline bytes; no expanded copied suite.

PASS — complete NEW resolved frame records: reconstruct both targets' same-O2 normal frame/call graphs and Wasm local/parameter charges from all eight retained diagnostics/paired .su files, compare every graph and reachable root/sum with old evidence. Resolve ONLY the adopted local native br x10. Unknown/recursive/other indirect edges still refuse. Native factory/validator/basis/run bounds1424/1872/160/2656; qualified Wasm1776/2216/168/3144, all<=65536. Original D196 corruption-abort edges remain null/unmeasured. No physical native I/O/VM/JIT/OS stack attestation. Both retained zero-init/old-copy checks and actual rules object/assembly hashes are bound independently; compiler Wasm .rodata is not hardware immutable memory. Old frames.json and original REFUSE remain verbatim.

PASS — exact retained source/build/process/fixture protection: compact manifest has94 nonoverlapping roots and44783 entries, including complete candidate1 source/preparation/build/cache/fixture/failure graph, accepted source/data, protected SDK/original cache, dependencies and new three sources. Records include exact membership, mode, regular byte length/SHA256 and opaque link/special kinds. Links/specials are never opened during manifest traversal. Exact named tool/SDK alias roles are separately verified. The old19-child ledger matches fixture plus18 build argv, zero exits, original handles reaped/group absent, no errors or original-deadline expiry. Original54 mocked results remain data with zero actual children/signals/waits inside fake cases. Original before/after protection identities match; historical controls stay opaque and are not retargeted. Current preparation authority hashes are bound separately and rechecked unchanged before publication and post-terminal inspection.

PASS — resource accounting:5,310,295 unique semantic/parser/case/generated bytes including final pins, below8,388,608. Compact manifest4,295,452 bytes. Identity-only streamed hashing3,130,431,163 bytes; recorded reads before publication3,139,404,464 bytes. These provenance reads are separate from semantic data/output, not target payload or copied caches. Explicit limits60000 entries,512MiB/blob,16GiB cumulative hash work,32GiB all streamed reads,1MiB hash blocks,64KiB ASM lines/4MiB ASM artifact and300s whole clock. Elapsed before publication6.533691333024763s; observed terminal exit0 occurred after publication in the same run, no claim that the earlier elapsed field includes final fsync. One small stdout JSON record only. Kernel stalls remain an honest limitation; late-return checks refuse.

PASS — exact future six-child plan: plan.json binds original four version argv then retained native binary and Node/unchanged runner/retained rules.wasm, with no compiler/link/fixture command. All tool/alias roles match old prepared pins. Closed environment preserves fixed PATH/PYTHONDONTWRITEBYTECODE/EM_FROZEN_CACHE and redirects TMPDIR,EMCC_TEMP_DIR,EM_CACHE,EM_PORTS,CLANG_MODULE_CACHE_PATH,NODE_COMPILE_CACHE to NEW retained-proof-1/attempt-1. Future operation/controller reuse is unchanged source-library Supervisor/Real/SignalGuard/Terminal: original handles,60s inclusive operation,300s original whole,8MiB aggregate child output, eligible independent cleanup, per-I/O cutoffs, signal restoration before terminal publication, durable refusal plus observed-exit0/stdout gate. Actual branch refuses current ticket and requires separate explicit MAIN actual release.

NOT RUN — all six future children, actual root, any target response comparison, target timing, candidate acceptance/freeze/live installation/consumer pin change. Both targets remain obligated to the unchanged4192-byte262-row corpus and exact7864 expected bytes each; neither is substituted by this data-only proof. No compiler, version, target, SDK copy, fixture replay, old entrypoint, game/browser/server/network/Git/FFI effect now. Current effects counters record0 for those categories and1 for the explicitly permitted pinned source-library load.

## Immutable delivery identities

All below relative to tests/outbreak/rules_initializer/retained-proof-1:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| verify.py | 41566 | 96a33ae8d24ca9c2f13615d8f552fd109410863b7391324fbf32ddb1ebb2f7df |
| SCHEMA.md | 11800 | bdc66da47291f28c0e6e3f6b3d89f779c14e01919c1c42ed195e63ce5ca990db |
| README.md | 4352 | 41000a0ed7d85c64aa4ecf9a48fe430b78bee2cc5c44b0ce48b294a7cf608d9e |
| preparation-1/pins.json | 1769 | fb4e0cbd39ba13b1557eb59ed8ade6601dafcad77336311c2cf84611eb95ae08 |
| preparation-1/plan.json | 24896 | dd82ee833e1f0cf5d2f34833e92decf2a23ddef30fa2a5b3c1ec1690ab66cce5 |
| preparation-1/branch-proof.json | 16158 | d0a46b153089f4f5f97d15afcbfa8465d0ff63a6d667d982e943d53bec45b7f8 |
| preparation-1/retained-manifest.json | 4295452 | a9f0ec2c776e3153ab44b5951b001889c0467a517553e804c752dc61dbb9e2db |

## Implementation status

Implemented new narrow data checker, compact retained binding, resolved frame record and future controller source. Pure in-memory checker outcomes and guarded positive publication completed. Old54 simulated cases and18 builds/19 process closures are retained historical facts, not new executions. Runtime behavior is incomplete until separately reviewed/released first targets produce both exact outputs. Old T166 remains consumed REFUSE; new preparation does not reclassify that terminal outcome.

## Integration and questions

T1691.0 and RULES_RETAINED_COMPLETION0.1/D242 reread before submission; preparation authorities rechecked unchanged. No public interface, dependency, C++, flag, old source/metadata/history or live installation changed. Stable source/preparation submitted for MAIN review. Stopping now: no actual invocation, further source correction, regeneration, alternate entrypoint, final freeze or dependent work under this lease. Later actual completion/candidate acceptance/install/consumer pins/full97755-row cone/G1 and all QA/T149/gameplay/P0/performance/RSS/human gates remain separately required.
