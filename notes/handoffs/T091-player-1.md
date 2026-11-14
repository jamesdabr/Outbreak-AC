# T091 — Foundation observation source/component handoff

- Worker: Player / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e.
- Ticket/revision: T0915.14, RELEASED at final read; D087, approved FOUNDATION_OBSERVATION0.1 and PLATFORM_DECISION0.1; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5 isolated observation prerequisite only. MAIN owns review/acceptance.
- Base:13f0d8eea4822dee5c976661218d022be74342e3 plus accepted dirty overlay. Existing main.cpp hash matched D053/D055 `ec652351aa25219a2c1d8e88d2b2aae2319703e08bcd5900242a8398c9df803f`. Existing broad Git diff is historical; own `source-only.patch` compares the actual accepted pre-task source.
- Changed: source/src/main.cpp only guarded new publisher/call; NEW web/player/tests/T091/** and this own handoff. No other production/header/schema/driver/artifact/pin/contract/status/SDK/cache edits, commits/reset/dispatch/install.
- Outcome: **SOURCE_APPLIED; EXTRACTED_PUBLISHER_FIXTURES_AND_GENUINE_NETWORK_MAIN_OBJECT_PASS. FULL_BUILD/ACTUAL_BROWSER/GAME/INPUT/RENDER/MEMORY/PERFORMANCE/AUTHORITY NOT RUN.** Source and6012-member evidence frozen before this handoff; ready for Engine/AI's separately released real-source observations. No further edits/runs against this evidence.

## Acceptance evidence

| Criterion | Result / evidence |
| --- | --- |
| Exact compile guard/publication boundary | PASS. New function and call both guarded by `__EMSCRIPTEN__ && OUTBREAK_NETWORK_CLIENT && !STANDALONE`; call immediately after existing browserpublishjs at browserpublish boundary. No new handlers/timers/exported actions/setters/game-state writes/extra draws. Removing those two exact guarded blocks reproduces the complete accepted pre-task source byte-for-byte. |
| Exact new immutable snapshot | PASS source/23 extracted-actual-EM_JS fixtures. window.OUTBREAK_FOUNDATION_METRICS property writable:false/enumerable:true/configurable:true; exact schema/profile/frames/actor/angles/held/heap/logical_viewport/document fields, all nested objects frozen. Republish preserves old snapshot and exposes no setter. |
| Genuine source mappings | PASS extraction.json pins source full hash and actual JS body byte/line range; fixture adapter checks the exact C++ argument list/order. frames→frame.frames, rendered→browserrenderedframes, actor→player1 presence, yaw/pitch unnormalized; move/strafe signed ints, attack/jump_next/jump_held/crouch_try→attacking/jumpnext/jumpd/trycrouch. Current screenw/screenh; actual JS HEAPU8.buffer.byteLength and document focus/visibility/pointer comparison read at publication. No physical input or server-applied action inference. |
| Absent actor and invalid source | PASS. Absent actor yields null angles and zero/false held; finite yaw725.25/-900 retained without normalization. Negative/fractional counters, invalid actor/axes/flags/viewport/nonfinite angles/heap and unavailable document values throw explicitly before new publication; previous snapshot remains unchanged. No clamping/state repair/fallback. |
| Existing diagnostics unchanged | PASS. All four existing void EM_JS definitions/bodies byte-identical; exact source removal comparison covers all other old code as well. No OUTBREAK_DIAGNOSTICS/NETWORK_TIMING/model/audio/network schema/action/input/clock/lifecycle modification. |
| Independent native/offline delta absence | PASS conditional source preprocessing using real `/usr/bin/unifdef` before/after for native client, native NETWORK client, native STANDALONE, offline browser, browser STANDALONE. Three native pairs raw byte-identical; offline/browser-STANDALONE differ only one empty separator line. All retained nonblank source lines byte-identical; new publisher/call absent. This does not expand includes or claim five full builds. Raw outputs/exits retained. |
| Genuine actual main.cpp network object | PASS exactly one real production main.cpp Wasm v1 object, not copied/stubbed/syntax-only. O2/gnu++11/signed-char and exact accepted network SDL2/image-PNG/zlib/Vorbis flags/includes. One dependency discovery then one object compilation, both exit0; actual231-member dependency map/bytes identical before/after, include trace retained. No object reuse/full link. |
| Tool/cache/environment isolation | PASS existing Emscripten7.0.0 compiler777e6e5db7b4990bcaeb1b9998ed642cc84e6629, pinned Node24.19.0, explicit Python/config/tools hashed. Fresh physical copied frozen cache, own temp/module/Node cache paths, EM_FROZEN_CACHE1. Original full SDK/original cache and owned frozen cache membership/bytes unchanged. |
| Preserve T089 and unrelated inputs | PASS before/after protected snapshots differ only current main.cpp hash: source/src/ENet/frameworks, signed copies, native release/debug binaries/ledger, old offline/network/T070 bundle, T074/T081/T089 evidence, SDK/cache and named config/contract/ticket records. MD3 remains applied accepted hash f60cdc019579cba4876ff741438934c56b6d626ac55c36c28e8b8ab8abe644be. No old ledger/pin rewrite or hash exception. |

## Exact source/evidence identities

- Before main.cpp: `ec652351aa25219a2c1d8e88d2b2aae2319703e08bcd5900242a8398c9df803f`.
- **Final main.cpp: `5f51c53b5a6f2be1180252c7aee972ab754bf0abc91d8a3d0f276153a38834f1`.**
- Actual extracted JS body including saved trailing newline: `6bb680c0c32bcf13dea68a593f60b7e30001e78a261017093c59d9230454d52d`.
- Actual main-network.o: `8e1d29cfa4173e13a925d80a176182e5c04ad0304b16c7f7cd3c6c439c8d065f`.
- result.json: `cccda1645da3bef18742e333a9818957a2a7ecec9a61bc2bbf857dd2dbc5d1b7`.
- evidence-freeze.json: `7248c0f386fc597c0e879d6945fafe9984b32bd01cae8630062ad57fda2d5a0f`,6012 frozen members including owned cache,6013 files with freeze itself.

Evidence root web/player/tests/T091: main-before.cpp; source-only.patch; publisher.js/extraction.json/publisher.cjs; guards/ before/after conditional outputs; deps/ discovery and actual .d; main-network.o; exact tools/environment/13 command argv+exits in result.json; raw logs; before/after snapshots; cache-before/after; evidence freeze/README/inspected own entry points. Fixture stdout reports23 PASS, classification EXTRACTED_EM_JS_FAKE_DOCUMENT_HEAP_FIXTURES_ONLY. All13 subprocesses succeeded (unifdef exit1 denotes conditional removal, not failure); no source change/retry after pass.

Historical executed commands, each once after inspection; frozen paths cannot be reused:

```text
python3 -B web/player/tests/T091/prepare.py
# apply_patch exact new guarded observation and call
python3 -B web/player/tests/T091/check_once.py
python3 -B web/player/tests/T091/freeze.py
```

Preparation performs standard-library snapshot/copy only. Check performs one Node fixture,10 unifdef passes, one Emscripten dependency pass and one genuine object compile. Freeze rehashes only; no repeated tests/build. No SDK/native/browser/game/server/network/sanitizer runtime. Host local macOS26.5.1 arm64; no hardware/performance inference.

## Integration and limitations

Only approved read-only foundation observation is implemented. Fake document/input/heap data proves publisher behavior, not real relative mouse, focus/held release, pointer capture, gesture audio, pixels or measured memory/frame/RSS targets. unifdef conditional evidence is not native/offline compilation/runtime equivalence. Genuine object is not a linked game or browser instantiation. A fresh accepted full candidate plus separately released ordinary-input/browser measurement remain required. Existing old artifacts/metadata retain their original source identities; no automatic repin or authority claim.

No blocking question/dependency remains for this source/component deliverable. MAIN reviews and updates authoritative status; Engine/AI work requires their own existing releases. QA human hold remains untouched.
