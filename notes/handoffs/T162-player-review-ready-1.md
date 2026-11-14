# T162 Player review-ready handoff 1

- Worker: Player / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T162 1.0 RELEASED; REVIEW-READY submission only, no authoritative status change.
- Phase / contract revisions: INPUT_BATCH_CODEC_FOUNDATION0.1 / D215; D226 continuation clarification.
- Base commit and pre-existing edits: bdaa8df7ec39d9408f97feda4560832d7ef26c3c; extensive shared working-tree edits preserved. No Git mutation, branch or commit.
- Changed files: eight new files below; fresh attempt-1/** and supervisor-fixtures-1/**; own T162 hold chronology, preflight and this handoff. No accepted source, old driver, capability, contract, ticket or lead decision edits.
- Commit or patch reference: none authorized; current files plus pinned preflight/plan are the review surface. Final freeze NOT CREATED; await MAIN review.

## Acceptance evidence

PASS (isolated unit scope): actual new production batch codec composed unchanged accepted encode_active_input/decode_active_input on native and direct import-free Wasm. Both returned 6769 exact112-byte responses matching the independent Python struct/integer oracle: 3593 decode and 3176 encode per target. Each output is 758128 bytes, SHA256 d525b99b888572c66306e3ba935ef19df1778c7fa029057bb50614be2f9c5c0a, identical to expected.bin. No roundtrip-only substitution. Every actual status/Fault/all-three-output-frame/used/window/guard/prefix/suffix assertion passed. Counts, reserved, ACK freedoms, per-frame error priorities, late errors, sequence ordering, unused fields, atomicity, backing extents and unaligned origins are covered by the pinned finite family union in plan.json/cases.json.

PASS: exact header declarations/member types/array extent/double-include compile checks; C++11 O2 warnings-as-errors; production header includes only accepted p1_input.h. Accepted core/input SHA pins were checked before and after. Production codec adds only the adopted record/API, bounded staging and field publication. No stateful integration or changed active-input validation.

PASS (SIMULATED, separate): 42 guarded fake cases (35 supervisor and 7 terminal), four real-boundary guard self-checks, zero unexpected host boundary attempts. They exercise actual Supervisor.run/whole_guard and Terminal.finish with fake process/selector/pipes/clock/persistence. They cover spawn refusal, partial setup, guard during acquisition/setup, drain/read/write/output overflow, kill ESRCH/error, wait failure/late zero, each close, combined errors, deadline exhaustion and publication/gate failure. Fixture evidence is 110300 bytes. No actual fake-induced process, signal, wait, network or compiler effect occurred.

PASS: all20 actual child operations have confirmed publication in terminal-receipt.json, known zero return codes, REAPED ownership and no secondary cleanup errors. Largest supervised elapsed time was 0.3216904579894617 seconds. Aggregate observed child/fake output was 1516948 bytes (under8388608). Whole driver summary after terminal gate was 9.832324166898616 seconds (under300). Guard timer and handler were restored without error before terminal publication. REFUSE is absent; result.json is conditional PASS_IF_REFUSE_ABSENT. The single attempt is consumed; no retry or compiler rerun occurred. Per-operation self-written receipts retain PENDING_PUBLICATION by design; the independent terminal ledger confirms each actual completion. No necessary evidence or comparison was deferred until after REFUSE removal.

PASS (qualified resource scope): object and assembly stack-usage records match at the same O2 for every unit/target. Complete reachable normal call-chain maxima below65536 bytes:

| Root | Native bytes | Wasm linear ABI + declared parameter/local charge bytes |
| --- | ---: | ---: |
| encode_input_batch | 256 | 480 |
| decode_input_batch | 160 | 432 |
| run through codec | 1792 | 2144 |

Actual native compiler frames: batch encode192 + active encode64, batch decode160 + active decode0/publication0; run1536. Native wrapper emits a memcpy call, whose actual same-link helper frame is0. This zero is compiler evidence, not an omitted unknown callee. Wasm encode112 ABI +144 locals/params plus active encode32 ABI +192 locals/params =480; decode128+112 plus active decode0+192 =432; wrapper1344+320 plus maxAPI480 =2144. Inlined read/write/finish/order/validation code contributes within the compiler frames. Publication and every out-of-line normal helper are in the retained graph. Test-link memcpy/memset/bzero are explicitly described/pinned/measured byte-loop helpers; this is not a future system-libc bound. Three emitted native canary failure edges remain D196 unmeasured corruption-abort exclusions. Physical VM operand/control/JIT/OS stacks, native main stdio and arbitrary future callers are outside this defined invocation-chain claim. No optimization/protection/threshold relaxation.

PASS: original SDK/cache, accepted T156/T157 source/evidence, T103/T143 capability evidence and named accepted input files have identical protected-before/after snapshots. Actual compiler dependencies were recorded before targets and rechecked after targets; all own sources/authorities stayed unchanged. Historical native dependency symlink kinds/targets were validated separately from regular-file digests and the two explicit ordinary SDK referents, with no generic alias relaxation. No broad concurrent whole-workspace preservation claim.

The input/fixture envelope used866432 corpus +758128 expected +1234749 case metadata +110300 fixture evidence =2969609 bytes, below8388608. Protection ledgers each occupy9958467 bytes of metadata; they are retained evidence inventories, outside the request/fixture payload calculation. Their sizes are disclosed rather than described as part of that8MiB payload. Compiler artifacts and copied sysroot likewise are not request/fixture payload or child stdout.

NOT RUN / unreleased: packet/envelope/admission/auth/life/clock/scope integration, client/server/multiplayer/gameplay, browser/capability T149, QA, P0/performance/RSS and human acceptance. No such claim follows from unit success. No final freeze or ticket acceptance.

Exact actual invocation from /Users/jd1/code/apps/outbreak:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B tests/outbreak/input_batch/T162/verify.py 69d72a9f9a4aa386e2fccd9f970e3f740904a6238c7f27c28791ba10c7c03278
```

Reproduction means review the pinned corpus/oracle/raw outputs/commands/evidence; do NOT rerun this occupied driver. A new execution would require fresh MAIN authority. Tools: Python3.11.9, Apple clang17.0.0 clang-1700.0.13.5 targeting arm64-apple-darwin25.5.0; Emscripten7.0.0 installed clang24/LLD24 revision84ba7b37f02df5a5567e31a1bcfa0f607e578f12; Node24.19.0. The preflight records macOS/arm64 platform, executable digests, exact observed aliases, argv/environment/native SDK role and dependency context. No tool acquisition or original cache mutation.

## Implementation status

Implemented: atomic batch header/selected child composition; total adopted Size/Null/count/reserved/per-frame/Sequence ordering; ACK bit freedom; unused decode zeros; unused encode values ignored; Fault stage/detail normalization; whole-record/append atomicity. Synthetic requests exercise actual compiled production code on both targets.

Simulated: only labeled supervisor/terminal boundary fixtures, not codec results. Their fake clocks/processes do not establish browser or production behavior.

Incomplete/unreleased: integration and full phase work listed above. OS spawn/close/filesystem primitives are not universally preemptibly bounded by Python clocks/signals; this limitation was pinned before execution. Actual observed operations completed inside the caps with known ownership; no unresolved process is hidden as success. Crash-restored REFUSE would fail closed. Final freeze awaits MAIN.

## Integration and questions

No new dependency/asset, existing shared header change or production recipe change. The exact new header/API is the only approved production interface addition. D226 separately resolves the historical hold replay; notes/questions/T162-player-hold-chronology-1.md is preserved. No new stop was inferred from the T149/QA reminder. No current affected-scope question remains; this review-ready handoff does not self-accept routine choices or evidence. Stop work pending MAIN review.

## Source and preparation identities

| File | Bytes | SHA256 |
| --- | ---: | --- |
| `source/outbreak/p1_input_batch.h` | 328 | `683674269a669c77be4a6f5fe51f65e8dcc9f23810c4cc9bdf398e19368d7452` |
| `source/outbreak/p1_input_batch.cpp` | 2909 | `9b1f543ce23b441511b773b39db37b4d64cbb3359c48d85be1ba72b5c7f70d0b` |
| `tests/outbreak/input_batch/T162/verify.py` | 42876 | `ccac7b2d4f6b4784ff951f956e67df44e4d7bbab1420974643ddac22b0b2fa5d` |
| `tests/outbreak/input_batch/T162/test_supervisor.py` | 11111 | `f4f7c60ca9fffade96d6d413385736066aebcbea0666c1afc7158dee273449e1` |
| `tests/outbreak/input_batch/T162/wrapper.cpp` | 7846 | `038c52ba5fe4ea63193058c7176774b5c48e07e1256ac571c0c5f4f3dec03e61` |
| `tests/outbreak/input_batch/T162/wasm_runner.mjs` | 1090 | `9323702ee0ed8a83f26c4d9a84ff2a097db4c9fb6ce568aa79d7f29fa1a7ed7a` |
| `tests/outbreak/input_batch/T162/SCHEMA.md` | 4590 | `dbd5ac2626dc310a785e91fca8ef0867e8a06553f2ba5b229a9023a4b7412c9a` |
| `tests/outbreak/input_batch/T162/README.md` | 4879 | `3ce62fb7a253879c6c73bf8743c38092e2f9833ad93a86c293e2c5c627c5a0a5` |
| `notes/handoffs/T162-player-preflight-1.md` | 22143 | `69d72a9f9a4aa386e2fccd9f970e3f740904a6238c7f27c28791ba10c7c03278` |

## Principal actual evidence identities

| File | Bytes | SHA256 |
| --- | ---: | --- |
| `tests/outbreak/input_batch/T162/attempt-1/plan.json` | 22277 | `863f0e00a83aac6b7608d3bb8c2dccdb431e0de859c1dba62c060a9732686226` |
| `tests/outbreak/input_batch/T162/attempt-1/result.json` | 28538 | `c1d080489ecb211281d1475b04ec7c01468d808fec19b4e58d8205fc6c50ae63` |
| `tests/outbreak/input_batch/T162/attempt-1/terminal-receipt.json` | 25862 | `10f38d73e63916b84427a8e1ed7ba4845e9685507cd1c64ce2394afae2ad26d0` |
| `tests/outbreak/input_batch/T162/attempt-1/frame-proof.json` | 9926 | `f06212fbd868ed813beed6cca674bd7b3ae544394230c2f32310b86e48ae7a44` |
| `tests/outbreak/input_batch/T162/attempt-1/dependencies-before-targets.json` | 15574 | `552c69397fa6ba8b8abf1dfa5c39b2165d6274479f87b429fcb91f4f7d744405` |
| `tests/outbreak/input_batch/T162/attempt-1/native-dependency-context.json` | 200670 | `76bace2cf1643da22043f6277a0915b89b4ecd221df0855c80916a5f13be1bee` |
| `tests/outbreak/input_batch/T162/attempt-1/protected-before.json` | 9958467 | `b3c5035be6df47d9c46d91a1231a3ffd51fc4f699680ccbd30e8957df287fedb` |
| `tests/outbreak/input_batch/T162/attempt-1/protected-after.json` | 9958467 | `b3c5035be6df47d9c46d91a1231a3ffd51fc4f699680ccbd30e8957df287fedb` |
| `tests/outbreak/input_batch/T162/attempt-1/corpus.bin` | 866432 | `7c9a74409f6a5be24ed994da1836a71eb719cfe0841647a0f6047a96e96ae727` |
| `tests/outbreak/input_batch/T162/attempt-1/expected.bin` | 758128 | `d525b99b888572c66306e3ba935ef19df1778c7fa029057bb50614be2f9c5c0a` |
| `tests/outbreak/input_batch/T162/attempt-1/cases.json` | 1234749 | `9a0ab2628dee508de3ef4f8fc794836cb208919921982d2de65a4ac11dbe805c` |
| `tests/outbreak/input_batch/T162/attempt-1/supervisor-fixture-result.json` | 58171 | `58654b7d58592d820a9f87e9867b818c047a20103ff2adfbf55e5c37b29b3d13` |
| `tests/outbreak/input_batch/T162/attempt-1/native-target.stdout.bin` | 758128 | `d525b99b888572c66306e3ba935ef19df1778c7fa029057bb50614be2f9c5c0a` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-target.stdout.bin` | 758128 | `d525b99b888572c66306e3ba935ef19df1778c7fa029057bb50614be2f9c5c0a` |
| `tests/outbreak/input_batch/T162/attempt-1/native` | 35064 | `a87c684827b550b35af437ac8abe90313d44de01e85288426bee78ed63eee8e7` |
| `tests/outbreak/input_batch/T162/attempt-1/batch.wasm` | 8605 | `018cf466c12850438d8bc16eb84165fa22272c24ef3c875ac5b91a1f0becf08f` |

## Compiler and process evidence identities

All generated dependency files, object files, same-O2 assembly/stack ledgers and per-operation receipts are retained below. Raw target stdout identities are above; every child stderr is retained (target stderr empty).

| File | Bytes | SHA256 |
| --- | ---: | --- |
| `tests/outbreak/input_batch/T162/attempt-1/native-batch-compile.receipt.json` | 1235 | `036283f9f83353bf4ec5b20b9bc610e8e0509666244a74e8a288ee0227127210` |
| `tests/outbreak/input_batch/T162/attempt-1/native-batch-diag.d` | 3018 | `dcfe2d59e2e03cf4108ff09d929861a893858fd06a7b42345df1b60208c7bb22` |
| `tests/outbreak/input_batch/T162/attempt-1/native-batch-diag.s` | 9290 | `c8191ee0c3a5bf1ae6070e8259389aa65ddb6e84b4e8994ea583c50a7b2dac05` |
| `tests/outbreak/input_batch/T162/attempt-1/native-batch-diag.su` | 343 | `95c852f339a7a29c10313a3c98f83931a6a74326dc49fa81bb01108c639089d0` |
| `tests/outbreak/input_batch/T162/attempt-1/native-batch-diagnostic.receipt.json` | 1249 | `9846caddcc83b5c57c9af3ab5d3521c4100b0331811358f83b9c5b6f58290c2a` |
| `tests/outbreak/input_batch/T162/attempt-1/native-batch.d` | 3013 | `35cb618b7d616ee6f4d38b6515f0fb073765d7a2a15840c5c23db38e9386e4ff` |
| `tests/outbreak/input_batch/T162/attempt-1/native-batch.o` | 2296 | `02ba6c65aeeab90a08975a02c1eafc454733f329bea79f66d0113bbfc5cd049a` |
| `tests/outbreak/input_batch/T162/attempt-1/native-batch.su` | 343 | `95c852f339a7a29c10313a3c98f83931a6a74326dc49fa81bb01108c639089d0` |
| `tests/outbreak/input_batch/T162/attempt-1/native-input-compile.receipt.json` | 1230 | `f6bdc4b8771b1abad22ed137d587a7fd429f49ef7783a96de56badc205464ac4` |
| `tests/outbreak/input_batch/T162/attempt-1/native-input-diag.d` | 2945 | `907e0893ad554d41507c15e5bd7b1720eff8a74b1b96321b941c063c3a96529c` |
| `tests/outbreak/input_batch/T162/attempt-1/native-input-diag.s` | 5432 | `ac529319dcd0d69c031af77e995e7286a53d66e528524b0aa078ff636d39d705` |
| `tests/outbreak/input_batch/T162/attempt-1/native-input-diag.su` | 228 | `472c481c55e2e923a398bcd9b1ef8c4d1c7cadf5708824f25bfd66fd32691004` |
| `tests/outbreak/input_batch/T162/attempt-1/native-input-diagnostic.receipt.json` | 1243 | `5d6a2da5c75a4dbf062ab6f27b9bdffdbcd534a3d95fc9573abf3bf166279b0d` |
| `tests/outbreak/input_batch/T162/attempt-1/native-input.d` | 2940 | `91987731c0221ef3a547c425fb65add24eab9527e95591109d02fb2e014f079d` |
| `tests/outbreak/input_batch/T162/attempt-1/native-input.o` | 1552 | `2e6429d02e3efb259389b6bb7905f380ffef74b9a5ba3a2b8e92e99238134eb3` |
| `tests/outbreak/input_batch/T162/attempt-1/native-input.su` | 228 | `472c481c55e2e923a398bcd9b1ef8c4d1c7cadf5708824f25bfd66fd32691004` |
| `tests/outbreak/input_batch/T162/attempt-1/native-link.receipt.json` | 1072 | `c9145e6fa207946cac7992bf5ef743028118d128025b2c1c140296f80d6ad06d` |
| `tests/outbreak/input_batch/T162/attempt-1/native-target.receipt.json` | 761 | `ccb522ef8b5285769718f6d3bc503370e62b51f37a5c1c66a396b9b5341fa386` |
| `tests/outbreak/input_batch/T162/attempt-1/native-version.receipt.json` | 715 | `40a6dc542b8e5684b4d309b30be802f94ced7c85b26112d8ed33c9c18649feee` |
| `tests/outbreak/input_batch/T162/attempt-1/native-wrapper-compile.receipt.json` | 1271 | `7c3518663d2c70f6499abb7d24e94f1e2a335d533829272f9584382b73eaf092` |
| `tests/outbreak/input_batch/T162/attempt-1/native-wrapper-diag.d` | 5085 | `c20328d3b053f8a7755a2a6c3e062380ed6a2c75a5c146cfaff2eca102f8df3e` |
| `tests/outbreak/input_batch/T162/attempt-1/native-wrapper-diag.s` | 46841 | `d2e2ecd9245360c8abb9f50216564c47d15d39a89bafdb9fa83909c35ba176be` |
| `tests/outbreak/input_batch/T162/attempt-1/native-wrapper-diag.su` | 805 | `26215e94fcb04e5186062c360c5d62b7992face7af0cc1d9d01b54e527ffb417` |
| `tests/outbreak/input_batch/T162/attempt-1/native-wrapper-diagnostic.receipt.json` | 1284 | `d54b488699e05a575e7cf111c6529363169aa0c724d5f2a605540fb55272abce` |
| `tests/outbreak/input_batch/T162/attempt-1/native-wrapper.d` | 5080 | `9b4bc406b08c41650c4b5e00fb37858f73a317f6f95af062901f27e76fbb61ca` |
| `tests/outbreak/input_batch/T162/attempt-1/native-wrapper.o` | 8400 | `dd438e0fb2a25cc21c8e49a36904b650a8fa5610f1218ad750efe1b5c6e8e16e` |
| `tests/outbreak/input_batch/T162/attempt-1/native-wrapper.su` | 805 | `26215e94fcb04e5186062c360c5d62b7992face7af0cc1d9d01b54e527ffb417` |
| `tests/outbreak/input_batch/T162/attempt-1/node-version.receipt.json` | 752 | `f7415ff9b98bc17a7918ef4fff058b9a099c53d08a23409b26c4d381d59dec0d` |
| `tests/outbreak/input_batch/T162/attempt-1/sdk-clang-version.receipt.json` | 752 | `fbb79bf90fc75c7cddcffca8e874ef1119807318be82837ff3ad613272de6d09` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-batch-compile.receipt.json` | 1333 | `ed09c71d5b164c215bc1737110a67731b21e7adf4e12a0116b88ca540b5a23f4` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-batch-diag.d` | 643 | `d3acedc891a2db3869329fa2d43302eb81c665a3a194ce86b93a6c71f750e425` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-batch-diag.s` | 14920 | `024c303efacb19dc3842a853bbbbcd7b43d210f3ffc043ce9df156bd5a5e27ae` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-batch-diag.su` | 343 | `3485a1d7a38d1f599f2e6323ca2b064ab5bdd1a70831b193fe1d1fbf0224ab29` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-batch-diagnostic.receipt.json` | 1346 | `e6e3efb4fd5701ee0b6a3f7e8c573705e2877ca83d48b769c84f4465fa88b56c` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-batch.d` | 638 | `8bed2bc8ba80def00c7ba0c0c2272d534192134c6b0e1dd107f76b443d75406a` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-batch.o` | 2019 | `f1f07565f4d871d28ef4c24c2aa43f8fe2d3e2e31ae10f74ef670564fe0693f0` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-batch.su` | 343 | `3485a1d7a38d1f599f2e6323ca2b064ab5bdd1a70831b193fe1d1fbf0224ab29` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-input-compile.receipt.json` | 1326 | `d52d8a37132614170671e0f17d404993a07e31748dbbeb4c2138350689117d46` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-input-diag.d` | 570 | `84f41ab5761195688adf16e10bc0f92007d091741aa0fca7fc80033458b8e451` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-input-diag.s` | 10207 | `a9ea85e0cdcf4978ceb75c69e5e1fa108a0a70d8dd6723eace5973247984c5ef` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-input-diag.su` | 228 | `0af95eb58a7e59a45c321ae209fef2194e14cae1467f2215041c9f3970816742` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-input-diagnostic.receipt.json` | 1339 | `6c1df7986c817f8965a10a0b4484f0cf7f3504554b9233a299ce0b9346757679` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-input.d` | 565 | `a9e228814916c4043842687169bf1abe53133bfc20682c8cdb83c4361585b256` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-input.o` | 1473 | `8d6829284fe4d815adf953f36e455b710576685285683a1265ecdb0b1a2f91e4` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-input.su` | 228 | `0af95eb58a7e59a45c321ae209fef2194e14cae1467f2215041c9f3970816742` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-ld-version.receipt.json` | 750 | `afa2fef47c7b39d4cf2786cc3d350a31872a36dad93f53ae2d8018f9de16d724` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-link.receipt.json` | 1273 | `a12767fca189ec7cbd5feac78ad42b0cde781c78c065cf567aa8cba05c3e069b` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-target.receipt.json` | 913 | `4d9add0c7aed99ac17fa8607e1650f5860aecbf4eb1bd6ae35583a49a8fd0e8d` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-wrapper-compile.receipt.json` | 1346 | `9ba468790ae47d8d4bd8139352a8b46b36426229e85a1498e23708c6dda77f38` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-wrapper-diag.d` | 654 | `a37a1c02efae0ebb1940f0a6dfa979ff50867df72f8d5970706eb63e6213051f` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-wrapper-diag.s` | 57596 | `39f50d1528afd58003af9f574611f2c5a1b925de77bc84bd277bb0532ea4111a` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-wrapper-diag.su` | 742 | `f321c3f7040843342c62fb2848055aba9b14ac3dfbcb3241447010deaebcf4c3` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-wrapper-diagnostic.receipt.json` | 1360 | `05202b1812f71c26393e14849716ea20522ec7066310b049cb4f942d8344e7e1` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-wrapper.d` | 649 | `392148096c2c007ca562846fa3d92ac4ea088cf93c4588bea948dda2e77ba3d6` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-wrapper.o` | 7679 | `29ad86c8a2143033d123db31a59f43a66fb2f2b8040b88d52e67c45199350394` |
| `tests/outbreak/input_batch/T162/attempt-1/wasm-wrapper.su` | 742 | `f321c3f7040843342c62fb2848055aba9b14ac3dfbcb3241447010deaebcf4c3` |

## Finite rejection observations per target

| Operation | None | Null | Size | Flags | Identity | Sequence | Range |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| decode | 2490 | 15 | 852 | 156 | 19 | 17 | 44 |
| encode | 2591 | 9 | 412 | 81 | 22 | 17 | 44 |
