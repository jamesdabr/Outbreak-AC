# T168 fixed-dev preparation — REVIEW-READY UNFROZEN

- Worker: /root/review_native_candidate, MAIN-delegated fixed-dev build worker.
- Ticket / revision: T1681.0, RELEASED SOURCE + GUARDED SIMULATED PREPARATION ONLY D234. Authoritative status was not edited.
- Phase / contract: DEFAULT_DEV_BUILD_PREPARATION0.1, D234; D235 fixed lazy Darwin adapter; D236/D238 clarifications, including MAIN's retained-descriptor resolution recorded in notes/questions/T168-D238-retained-descriptor-1.md.
- Base: raw read-only HEAD/ref bdaa8df7ec39d9408f97feda4560832d7ef26c3c, with preserved shared work and accepted T163 overlay. No Git command or clean-checkout claim.
- Changed files: only six NEW web/build/dev_regression/{recipe.py,build.py,verify.py,SCHEMA.md,README.md,test_recipe.py}, owned tests/preparation-1/**, this new handoff and the new T168 question note. No existing/shared/authority/asset/tool/source-manifest edit.
- Commit: none. Baseline source archives and exact final diffs are under tests/preparation-1/baseline/ and diffs/pass-8-*.patch. No T164 source was imported or copied.

## Stable review packet

`web/build/dev_regression/tests/preparation-1/review-ready-1.json`

SHA256 **84baffedaecbae48ba9f97f544aabae0d6e86c074c2f322efceb9ec463166da1**.

The index pins all six current sources and1,906 preparation files/21,918,658 bytes, excluding only its own index bytes. This is a review inventory, not a freeze or acceptance record. No source edits follow the final pass.

| Source | SHA256 |
| --- | --- |
| recipe.py | 37d9e37805f34f5dcde144a3429b68c85a96b75d0b5ed085903c610aee42de55 |
| build.py | 1e47f5fed2ea414405f1ad816e0aae7007bb41d4165cb553225fee2788209a7b |
| verify.py | 3ec91f59208df47eded9d931d8a39ffd0f476a156312bd2312afdad94506c549 |
| SCHEMA.md | 69aef2131fc19309aa91429f7d489ff97d7780c1e4f1b63dbf504760f4ffa7ae |
| README.md | c77653dbcef8d22887358032502517a7c2b9e93a3ab04344159e9885763e781b |
| test_recipe.py | b19fcbfe504587a9bb4044d451f182fce3459dd2bae23ceb972960d95a4b381c |

## Acceptance evidence

**PASS — guarded preparation only.** Inspected then executed the new harness:

```text
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/build/dev_regression/test_recipe.py --pass-id pass-8
```

Final pass: **193 cases,123.3249691670062 seconds,4,043,335 retained bytes**, seven explicit guard-denial self-checks. Result `pass-8/result.json` SHA256 **450efb906b5e9518cae93316bee5a6103f150c3806953548fbe178f8c8b76aa4**. Sources equal the plan/source snapshots; named original public inputs unchanged. Per-pass ceiling256 cases/300s/8MiB captured output/128MiB retained files. Work has295s plus5s terminal reserve inside300s; failure storage has1MiB reserved inside128MiB. Final stdout was one bounded JSON summary. OS/tool/hardware build or performance claims: **NOT RUN**; these durations describe only the guarded fixture interpreter.

The actual new orchestration/verifier methods cover:

- Fixed default_dev_network_v1: actual accepted Makefile order53 C+++8 C,125 generated commands, no Blackwood define, accepted three T163 header consumers, original79 files/388791 bytes/derived revision2 map, exact17 outer files and12 notices. Positive graph uses actual public payload bytes; fake compiler objects/SDK/authority remain explicitly FIXTURE_ONLY.
- Closed source/authorization/plan/result/freeze/receipt schemas and paths; accepted T163 four-file/reference pins; common MAIN manifest binding; independent command/environment/dependency/log/object/slice/metadata/bundle reconstruction. Wrong84-pack/profile/define/control/source/alias/context/late closure refuses.
- Original-handle anchored group cleanup, nonreaping D235 adapter methods with fake backend, leader-exit/open-pipe/EOF cases, separate original reaping/group absence, independent secondary cleanup errors, output/deadline/retention/late-zero/nonzero faults. Real ctypes import/load/native calls are denied.
- Actual raw persistence methods with fake primitives: already-expired/open/chmod/partial-write/fsync/close lateness; ambiguous close never retried; independently eligible descriptor cleanup; original whole cutoff for copy iterations/directory sync/mode preservation. Expired descriptors remain strongly retained/unresolved. Compact descriptor summaries precede long paths in bounded failure text.
- Outer FAIL ledger uses remaining original whole time while the refusal marker remains; whole expiry grants no ledger-write grace or resumed child IO. Full current original/owned/freeze gates precede marker removal.
- Actual verifier final marker/history/owned mutations, canonical ordinary receipt slot and stable identity/presence after lengthy final observation, default read-only behavior, requested receipts and late create/replace/delete/mode/IO; no occupied overwrite.
- Guards installed before tested module loading deny process/fork/exec/signals/wait/compiler/Node/tool/version/network/SDK-copy/old project/ctypes effects; raw FD primitives are denied outside explicit mocks. Write confinement canonicalizes dot-dot/links before checking the fresh pass root.

**PASS — preservation/source boundary.** `submission-input-preservation-1.json` confirms accepted archived baseline originals and released T168/contract remain byte-identical, current six sources match final pass snapshots, raw Git metadata read only, actual attempts/ and candidates/ absent. `D235-source-abi-inspection-1.json` records nine matching read-only installed ABI/stdlib hashes; no library resolution/native call/SDK copy. No MAIN manifest or controls were authored.

**Preserved failures, no unchanged retry.** Pass1 refused fractional accepted anchor DATA incorrectly sent to the control parser; corrected to pinned raw DATA. Pass2 retained67 rows then exposed malformed-command fixture dispatch; corrected exact dispatch. Pass3 reached300s during redundant fake builds; the same hard cutoff prevented its failure writer. Its source/plan snapshots and `pass-3-observed-failure.json` are retained honestly; completed rows were not recovered/invented. Corrected work/terminal/storage reserves and positive-graph cloning. Pass4 PASS146, pass5 PASS152, pass6 PASS169, pass7 PASS186 are historical results before justified subsequent source/guard corrections. All eight named pass trees remain; no overwrite or automatic unchanged retry.

## Implementation status

Implemented six-file fixed successor, complete private schema, independent verifier and guarded preparation. No loader/profile/gameplay/public API/asset permission change. Dependencies remain inspected accepted dev sources/data/T163 and standard library, including D235's explicitly authorized lazy ctypes source route. Old runners/T164/old project helpers are not imported or executed.

**NOT RUN:** real project plan-only/build/verification, compiler/link/Node/Wasm validation, actual tool/version/FFI/native wait/group behavior, SDK/cache copy, actual candidate/admission/runtime. The fixture actor SDK/interpreter/tool/authority identities are synthetic and cannot satisfy production filesystem context. Nine ABI hashes are source evidence, not native support proof. Actual large-forest metadata fit (private JSON guard32MiB), kernel-call timing and installed platform behavior remain unmeasured. No universal syscall preemption or external post-return race guarantee is claimed; CLI-exit OS resource cleanup is not counted as bounded command cleanup.

## Integration and questions

T168 ticket and DEFAULT_DEV_BUILD_PREPARATION0.1 were re-read/rechecked unchanged before submission. The D238 release question is resolved by MAIN and recorded separately; no worker amendment or accepted exception was made.

MAIN must independently review this unfrozen packet before any final freeze. Actual default-dev125-command full-client regression still requires a separate accepted source/current common-manifest/control/tool/effect release, serialization with Blackwood/native builds and independent actual verification. It remains mandatory and is not replaced by these fixtures. Blackwood matched native/browser admission, map/load/ACK/current-life reciprocal movement/rendering/cleanup, P0/gameplay/platform/performance/RSS/human/QA/T149 gates remain unchanged.

Stopped at REVIEW-READY; no freeze, acceptance, dispatch or real-effect permission inferred.
