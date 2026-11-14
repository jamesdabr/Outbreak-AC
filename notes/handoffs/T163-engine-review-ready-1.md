# T163 Engine fixed browser map-profile review-ready handoff

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket/contracts: T1631.1, BLACKWOOD_CLIENT_FOUNDATION0.1/D217/D219; Package A source/helper subset only.
- State: REVIEW-READY submission, no authoritative status change, freeze or build/runtime/consumer release.
- Base: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work. No Git commands/mutation.
- Changed: only source/src/main.cpp,client.cpp,clients2c.cpp; new browser_map_profile.h; five new T163 harness/docs plus fresh attempt-1 and supervisor-fixtures-1; this own handoff. No server/render/model/physics/weapon/protocol/binding/asset/build/runtime edits.

## Acceptance evidence

PASS BASELINE: Before source edits all three exact contract hashes matched, new header/test root were absent, and exact old files were exclusively snapshotted into attempt-1/baseline. baseline.json records historical pre-edit bytes/hash/mode/nlink/device/inode/mtime/ctime. Driver accepts only that prep membership and exclusively creates STARTED, preventing occupied rerun. Current baseline copies retain every pinned old byte. Complete source.patch identifies all source modifications; no broad formatting or unrelated rewrite.

PASS SOURCE ROUTING: Private browser_map_profile.h is included before cube.h in all3 source files so invalid Blackwood combinations fail at the private profile guard. Valid Blackwood define requires __EMSCRIPTEN__+OUTBREAK_NETWORK_CLIENT and !STANDALONE; selects blackwood_greybox_v1/revision1/itsCGZ+CFG only. Absent define selects dev_outbreak_browser/revision2/old paths. No JS/URL selector, protocol negotiation or fallback.

PASS COMPLETE CALLSITE AUDIT: main startup required CGZ/CFG and clientmap selection use fixed header paths/name, genuine load_world then startup result/loaded-header/name checks. Actual rendered-running transition uses loaded profile identity/revision/positive bytes after draw. client public snapshot uses accepted bnmap receipt-bound identity (empty/0 before receipt), both spawn expected/request gates use receipt+actual loaded name/revision/bytes/mode, preserving outer peer/client/lifecycle/current-life checks. Real map callback validates received AND loaded identity/revision/mode/bytes before setting bnmap, and original teardown clears it. clients2c pre-change rejects mismatches BEFORE load_world; actual post-load result/incompatible/name/revision/local-vs-advertised bytes are checked BEFORE real callback. Packet overread, actual generic SV_MAPIDENT, player spawn selection/reliable ACK and milestone path remain intact. Static audit and exact patch are retained; parser runtime is NOT claimed.

PASS COMPARATIVE SIZE SEMANTICS: Header preserves positive exact actual-local versus server-advertised length matching, including734-versus561 mismatches. It does not replace load_world or attest a file hash from length. Equal positive lengths are explicitly tested as accepted per the original rule; selected immutable assets and later full packaging/native reader/map handshake must attest real734/561 lengths. Startup requires real load_result0, post-server-load preserves original>=0 rule plus incompatiblemap refusal.

PASS ACTUAL HELPERS: Sole command `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/browser_map_profile/T163/verify.py` observed **outer exit0** from exec session60944 completion. Four actual private-helper targets: native dev/Blackwood macro-emulation fixtures, and import-free Wasm dev/Blackwood. **212 cases/profile/target,848 total actual helper responses**; each full192-byte response matches independent explicit Python string/integer expectations including selected identity/paths/revisions, receipt empty/0 versus accepted, all7 predicate bits, full input preservation/guards and reserved bytes. Cases cover both/foreign/empty/prefix/case/null names, signed revision/size extrema, modes/load/incompatibility/receipt and combined gate states. Native emulation is not native engine/browser execution.

PASS GUARD DIAGNOSTICS: **14 separately named expected-failing compile commands**, seven invalid macro combinations on each native/Wasm compiler. Each actual exit1 has exactly one exact profile diagnostic, no warnings, empty stdout and normal observed reaping. Unrelated errors/exit codes would refuse; no generic compile failure was counted as expected. Header double inclusion also compiled on all four valid targets.

PASS SUPERVISION: Copied accepted D212/T160 supervisor and44 finite actual-method guarded fixtures as inspected source DATA, not an old project import. Only direct necessary expected_profile_guard flag handles the named exit1 compiles, with exact diagnostic checks outside supervisor before success. All44 simulated cases passed; fake process/pipe/selector/clock/persistence boundaries deny actual launch/fork/exec/signals/wait/network and restore patches. Ownership/independent cleanup/primary+secondary/unresolved/reaping/output/deadline/guard/retention semantics preserved; no real child fault injection. Fixture bytes137,596 <4MiB own bound.

PASS BOUNDS/TOOLS: Installed pinned Python3.11.9/Apple clang17/Emscripten7.0.0 clang24+wasm-ld/Node24.19.0 on Darwin arm64; exact role aliases/targets/nativeSDK inputs, source/baseline/patch/authorities/corpus/layout/exports/argv/environment/cleanup plan pinned before compile/runtime effects. Direct dependencies are only actual private header/wrapper and allowed installed/copied SDK headers, captured before target runs and rechecked. Own verified copied frozen sysroot/cache/tmp/module/Node storage. All26 actual children reaped, null primary/no cleanup or retention errors:12 normal exit0 (8 compile/link+4 helper),14 exact expected exit1 guards. Each<60s including cleanup, work reserves5s inside original hard deadline and295s guard/300s whole applies. Combined all-child output168,710 bytes <8MiB; four raw streams162,816 bytes <1MiB. Recorded work2.508972957963124s precedes terminal inventory commit. No calibrated performance/RSS or hard-real-time arbitrary OS/Popen/descriptor/filesystem-stall claim.

PASS PRESERVATION/TERMINAL: Accepted T148 manifest and84-member pack bytes/hash/mode/nlink preserved read-only, including original dev/Blackwood CGZ/CFG/sidecar/scoped notices. No asset copied/mounted/executed/regenerated here. All classic source/src current files, other named source/helper/authority/accepted supervisor/original-cache inputs match before/after the closed proof interval; current3 intended edits and new header are pinned separately. No whole-workspace preservation claim. All report/flush/check/cleanup/evidence precede bounded canonical historical-inventory PASS result+directory sync; REFUSE removal is final required driver effect. Root REFUSE/failure.json absent and actual outer exit0 captured separately. Nested fake refusal markers remain explicit simulated evidence.

## Exact source and proof identities

| Source | SHA256 |
| --- | --- |
| source/src/browser_map_profile.h | 614fe93545ea52a4857d7674aae9b92452ba36cac35d952754ca218488aea414 |
| source/src/client.cpp | 0e3be12c5771eb20f4dfb9dbfe5cd239b49a02998d267a0df6b407280fb31b56 |
| source/src/clients2c.cpp | 5368d23331123aa67de430b7c11460efdb5182944b9508f715491b7c6522a4bd |
| source/src/main.cpp | 1da216b25233639eaaa1f89fb15a6cdbdd6ad3ab90e19989a44ffc77952a07ac |
| tests/outbreak/browser_map_profile/T163/README.md | bad0b27f23a05a8a76bffa212896da1e65721a37ca5029501718f6029e1fb24f |
| tests/outbreak/browser_map_profile/T163/SCHEMA.md | fdeeaf05add92ef4d6611aecd05fa7973cf5b94fc8915df4abc379b2910e97b3 |
| tests/outbreak/browser_map_profile/T163/verify.py | 068ef8a5c1a2e085e1c37ab8e6acd0a438c0032d44fdc386dc3ffd1ed6c7ac71 |
| tests/outbreak/browser_map_profile/T163/wasm_runner.mjs | 36bff34f7833b3da4e9eccb6af33de86cf12c655b2fe912417422b6e73511bd3 |
| tests/outbreak/browser_map_profile/T163/wrapper.cpp | 6d576f1b1167210035cb1d322b45fb514484b6158d23be8067a8d7f95ac23be3 |

| Original baseline | SHA256 |
| --- | --- |
| client.cpp | 2bbbf548e374ce4adb819400d435c4a6e5ae93bf26b4aaffcbe739028f72ec10 |
| clients2c.cpp | 83a57afb6796c8f76fbe496175f0527e51c431a9d06666d29ee10985ba812686 |
| main.cpp | 5f51c53b5a6f2be1180252c7aee972ab754bf0abc91d8a3d0f276153a38834f1 |

| Record under tests/outbreak/browser_map_profile/T163/attempt-1 | SHA256 |
| --- | --- |
| baseline.json | 7bdb226fdb47fbfe9e2596d3dd338664bd029fb9a8b5c870da53594461da25c0 |
| source.patch | 87af0e231c8625d8b61dde4dd1d11265804430e784f48f8b0ff7f5d7b30e9283 |
| source-audit.json | 2d72482f7528683ea26554241eadc3cba5520408f572e28bd9b25faed938d9dd |
| plan.json | 92056c9348b199b8e64b936648df4bc314fd07821931f64510e7aef709873f43 |
| result.json | 30adfcab0ce14a57990961e8e95af56ff766e87044b988893e24fc82ed2ce33f |
| processes.json | d38ebd662493f813823829b095be8ed915b2e1a15c13a5af36ec5e7513139896 |
| dependencies.json | d227fcf05789c62760d4afa78961ee8c825b414d24a787485952a7e7d9f7e2ca |
| corpus.bin | e40599b0a868c8eb82f2c49cd1da319da5f38baf873d48b3dfdeed4a6c3a7a7b |
| dev-expected.bin | d766285406785c730b60cccbb83e630e82f97ed355f636a9d1b5f3c217783f35 |
| blackwood-expected.bin | 4a2af75ab00bbd7a96e51da1244ac4675bf51663a6c37263038c4e59715647a2 |
| native-dev.bin | d766285406785c730b60cccbb83e630e82f97ed355f636a9d1b5f3c217783f35 |
| native-blackwood.bin | 4a2af75ab00bbd7a96e51da1244ac4675bf51663a6c37263038c4e59715647a2 |
| wasm-dev.bin | d766285406785c730b60cccbb83e630e82f97ed355f636a9d1b5f3c217783f35 |
| wasm-blackwood.bin | 4a2af75ab00bbd7a96e51da1244ac4675bf51663a6c37263038c4e59715647a2 |
| invalid-profile-results.json | edce06c4bd6641cb821d45664f890735caf0af07db0933821f745500318683c5 |
| supervisor-fixtures.json | 24af531ac0bfac75c85d5c2fffeb361356f1cec4624729fa9f4ab7d674891957 |
| protected-before.json | 5c6fbc6c781d532ad70e0292f33d0f5630e5f522d14cc1baf223d0287b05ee53 |
| protected-after.json | 5c6fbc6c781d532ad70e0292f33d0f5630e5f522d14cc1baf223d0287b05ee53 |

Each dev target40704bytes/SHA256d766285406785c730b60cccbb83e630e82f97ed355f636a9d1b5f3c217783f35; each Blackwood target40704bytes/SHA2564a2af75ab00bbd7a96e51da1244ac4675bf51663a6c37263038c4e59715647a2. Each equals its retained independent oracle byte-for-byte.

## Inventory and limits

Current owned union is complete T163 test tree PLUS exactly main.cpp/client.cpp/clients2c.cpp/browser_map_profile.h: **2211 ordinary nlink1 files**, **207 owned directories**, **0 links/specials**. Runtime inventory is explicitly historical (2416 members before result/REFUSE commit); current union equals that map plus result.json and otherwise-unlisted T163 root directory. All retained inventory members rechecked using only stdlib read/hash/JSON, no project imports/reruns. Canonical review graph SHA256 2fe1c228d1d1347334443472712d61063a7ba18a9c4a119990cc979cfa64e70c: JSON sorted keys/two-space indent/final LF of files(repository-relative bytes/SHA256/mode/nlink records) and directories(sorted Path-component-order repository-relative list). No post-terminal checkpoint/freeze records appended; this handoff is external.

Implemented: fixed source routing and actual compiled production-helper proof with static genuine callsite/lifecycle audit. Simulated fixtures are separate. NOT RUN: full53+8 browser build, native standalone candidate/build/signing/staging,84-member packaging/payload-slice verification, admission/controller preparation, app/browser/server/network or real two-browser Blackwood load/render/mapident/spawn/ACK/reciprocal movement/cleanup. Those serialized successors remain mandatory, including old-dev whole-build regression and accepted v4-derived runtime safety. Plan1 Package C v3 baselines remain unadopted.

No map/CFG/source asset rewrite,32 canonical deployment interpretation/grants or authority/third-person/physics/combat/survival/extraction/8-player/P0/performance/RSS/human acceptance. Canonical32 alternatives and8 technical FFA starts remain distinct with all Blackwood candidate limitations/scoped notices. QA/T149/runtime holds unchanged.

## Pending MAIN review

No unresolved helper/callsite issue identified by this scoped run; full source correctness awaits MAIN review. Engine retains exclusive source ownership pending review/freeze and later explicit transfer. Occupied proof must not rerun. No source/harness/evidence changes while awaiting review. Submit REVIEW-READY, stop for MAIN clearance before final freeze.
