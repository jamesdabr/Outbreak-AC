# T081 isolated full-header MD3 candidate handoff

- Worker: Player / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket/revision: T0815.4, RELEASED on final read; MAIN owns acceptance and any future production application.
- Governing: D071/D076 and browser foundation,GOVERNANCE,P0 0.5 candidate-compatibility subset only. No gameplay/API/source-application grant.
- Base/pre-existing work: accepted frozen source, T070 artifacts/T079 baseline, native/framework/SDK/cache inputs and original T074 failed witness preserved. No clean-checkout or actual-render claim.
- Changed files: NEW web/player/tests/T081/** and this own handoff only. No production header/CPP/assets/tooling/SDK/current tests/pins/artifact/old note edits, commits/push/reset/dispatch/install.
- Outcome: **FULL_HEADER_CANDIDATE_COMPONENT_PASS; PRODUCTION_NOT_FIXED; RUNTIME_NOT_RUN.** Candidate/objects/helper/evidence frozen before this handoff; later changes require a new note/lease.

## Acceptance evidence

| Criterion | Result / evidence |
| --- | --- |
| Preserve full current header and genuine affected CPP | PASS baseline/md3.h and baseline/rendermodel.cpp are exact production copies. Candidate CPP is byte-identical to both original and baseline. No stubbed/reimplemented consumer. |
| Precisely one-line full-header candidate | PASS candidate-only.patch changes only guarded position-only setup `link(NULL,a[i].tag)`→`link(NULL,a[i].tag,a[i].pos)`. Full candidate/md3.h otherwise byte-identical. Cleanup unlink remains unchanged. Production md3.h unchanged. No API/asset/renderer GL/authority modification. |
| Actual consumers identified | PASS source include search across CPP/headers finds only source/src/rendermodel.cpp directly including md3.h (line12). Other translation units were not compiled arbitrarily. consumers.json records source/header/copy identities and quoted-include strategy. |
| Exact candidate include resolution | PASS genuine CPP copy resides beside full candidate header. Six actual dependency-discovery/object pairs show candidate/md3.h consumed and production md3.h absent. Production model.h/vertmodel.h and other real source/tool headers remain inputs. Actual -H trace independently names candidate. No shadow stubs or compatibility definitions. |
| Genuine native release/debug objects | PASS two actual Mach-O objects from full affected consumer, not syntax-only. Native release options use inspected Makefile clang/client profile (-O3/fomit-frame-pointer/Wall/signed-char/no-strict-aliasing); debug O0/g/_DEBUG with signed-char/no-strict-aliasing, GNU++11. Exact argv/tool identity recorded. This deliberately corrects native semantics, **no token equivalence to broken code claimed**. |
| Genuine OFFLINE/NETWORK release/debug objects | PASS four real version-1 Wasm objects from same CPP/full candidate. Existing accepted current-profile GNU++11/signed-char/O2 or O0/g/_DEBUG and SDL2/image PNG/zlib/Vorbis settings; existing network macro only. No full client link, extra compatibility flags/error suppression or production artifacts. |
| Actual transitive input membership/hash stability | PASS each profile records preprocessor dependency discovery then actual object .d/-H files. Full resolved transitive file membership/bytes equal before/after object compilation. Counts: native414/904, OFFLINE218/533, NETWORK218/533 release/debug. Dependency-report options -M/-MD/-MF/-H record evidence only; no semantic workaround. |
| Helper tied to exact full candidate | PASS new owned helper.cpp is exact accepted T074 C++ fixture source, compiled/run under T081 only. Candidate setup fragment is independently extracted from the exact full candidate header used by six genuine builds, with source-byte/hash/range checks. Real setup/link/propagation/math plus explicitly external pose/container/render fixtures; no actual GPU/model renderer. |
| Pointer/oracle/attached/missing/null/later-part/unlink | PASS candidate expectations/controls; current-code bug reproduced alongside it. Independent transform(1,2,3)→(8,21,33) versus sentinel(-77,-88,-99). Candidate retains pointer/writes expected result; production-derived setup loses pointer/leaves sentinel. Both copies' controls pass, including repeated cleanup/no stale output or child reuse. |
| Preserve original failing witness | PASS original T07428 files (27 frozen evidence members plus its freeze) byte/membership unchanged. No old driver/binary rerun. New T081 helper exits47 intentionally with two original-code expectation failures, candidate expectations and controls passing. Raw logs remain; this is not a production-fixed result. |
| SDK/cache/native/framework/artifact preservation | PASS before.json==after.json, including source/src97, ENet48, source frameworks114, signed native dependencies85, old offline17, published network17, original T070 bundle17, T07428, SDK24407 and original cache5956 members plus named native binary/ledgers/pins. Original SDK/cache untouched; new physically copied task-owned cache5956 members also unchanged under EM_FROZEN_CACHE=1. Actual system-header dependencies separately hashed per command. |
| Independent T082 preparation not frozen as input | PASS no T082/T067 evolving driver tree in preservation groups or any compilation .d closure. Only fixed existing decision/ledger files and actual source/tool/native/artifact/cache dependencies are captured. No exception for a changed actual compilation input. |
| Exact tools/commands/objects/freeze | PASS result.json records14 commands:6 dependency passes+6 object compiles+1 helper compile+1 helper run; all exit0 except deliberate helper47. Raw stdout/stderr, include/dependency files, command/compiler/source/header/object/executable hashes and environment retained. evidence-freeze.json freezes6032 task members including owned cache. |
| Actual production application/full build/runtime | NOT RUN / NOT APPLIED. No production MD3 edit, native game/client/server/browser/network execution, full game link, actual decode/animation/attachment/GL/GPU/physical pixels or authority acceptance. |

## Exact identities

- Original production full md3.h: `635f904dafa3bbc63dc13c6f0a09c9cd3d6063d0e2d0dee8a1b95368fe19ec84` (unchanged).
- Isolated full candidate md3.h: `f60cdc019579cba4876ff741438934c56b6d626ac55c36c28e8b8ab8abe644be`.
- Original/baseline/candidate-directory rendermodel.cpp: `5d63f8b8e062e835a7f9b25d17a9f74a09bfd6bf66469311288e681512e2c671`.
- Helper CPP: `58750ac06dabb51c9ed8c027ebb4208a186aa5d1e9f5edcbdea9a20f15cb9c45`; new helper executable: `3d0110742e449a5e8724cef80a3d7e823494a542b9394254a45dbd38dc0f07b7`.
- Candidate setup extracted from full header: `00d8b2b66e3840b980454d0cee316aff9d332aec4669181992adc0a8aa9c48ee`.

| Genuine candidate object | SHA-256 |
| --- | --- |
| rendermodel-native-release.o | f7e41c035db6d24d8bfb679c304c8800179415fa136112f58290a5b4886f5d5d |
| rendermodel-native-debug.o | 80ceb3f5c9fafb4dfcac2ae196c37f77f25d9ed1ff6fd548c8892974a5b76f17 |
| rendermodel-offline-release.o | 786b7c3c9421943f66cc6483181193f4070adcbd50fb63c3786824173711193e |
| rendermodel-offline-debug.o | 6a6dbc8ae37926d300d877c9cb03a927d360c31ce15025a62eb30aa2b3b3c64f |
| rendermodel-network-release.o | 0d928e09a1b950c90c83c06534c9c5540d973c4da6905f488759fb242d228e8b |
| rendermodel-network-debug.o | 060b3b51a21542200d7b8d2033fa93987ec96348621b6e44c86ff4a326a056d3 |

result.json SHA-256 `4941575ebcde1fcfbcf8522adf54ed85c51d412c61509a0fbc9276f354a1a266`; evidence-freeze.json `c4ca4a905925d8a845f83abee129c01347173d513e76d3be144d08328962b6b4`. before.json and after.json both `3849db78a1860383d6f106ef1e5d4c35300bde1135ffb1908311a5b32b9c0db2`.

## Commands / environment / evidence location

Executed once after inspecting authored preparation/build/helper code:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/player/tests/T081/prepare.py
PYTHONDONTWRITEBYTECODE=1 python3 web/player/tests/T081/build.py
```

These are historical reproduction commands, not permission to overwrite frozen results. Scripts refuse prior attempts. A further attempt requires a new approved owned directory/release. No T074 entry point was executed.

Host macOS26.5.1 arm64; Apple clang17.0.0 (clang-1700.0.13.5). Reused pinned installed Emscripten7.0.0 compiler777e6e5db7b4990bcaeb1b9998ed642cc84e6629 and existing ports. Native headers/frameworks genuine. All Emscripten ports/cache, temp, Node compile cache and native module cache paths task-owned; original SDK/cache bytes/membership preserved. No install/download/performance claim. Exact absolute commands, environment subset and tool SHA-256 in result.json.

Under web/player/tests/T081: baseline/ and candidate/ full files; consumers.json/candidate-only.patch; extraction.json/extracted/; deps/ before/after actual compiler records; objects/ six real objects; logs/ include/compiler/helper output; before/after.json; cache-before/after.json; result.json; evidence-freeze.json; README.md. No files were placed under web/runtime.

## Implementation status and limits

Prepared/compiled only the isolated complete header and byte-identical genuine consumer copies. Full actual consumer compilation proves the candidate is accepted against real native/profile types/includes; it does not execute its renderer. The helper's candidate slice is tied by exact full-header hash/range to that same candidate, not separately hand-edited to pass.

External helper boundaries remain explicit: fixed animation tag matrix, model/actor/container/frame-pose scaffolding and source-loop part-entry wrapper. Matrix math, pointer methods/setup/unlink/propagation are actual extracted code; no GL calls/model decode execute. Current broken expectations fail with native47 and remain visible; candidate-only expectations succeed. Source application, real tagged animation/material/GPU behavior and native hit/gameplay consequences remain unproven.

## Future application/rebuild/runtime needs — MAIN release required

1. Explicit exclusive lease for production source/src/md3.h position-only setup line only, using this exact one-line candidate. Leave cleanup two-argument unlink unchanged. No model.h/vertmodel.h/API/assets/GL/authority change is indicated. Common native/OFFLINE/network semantics intentionally change; do not demand or fabricate equivalence to broken output.
2. Re-evaluate the complete current source/dependency and artifact authority closure; rebuild affected genuine client consumers and separately released full client/profile artifacts with new metadata/pins. Do not insert candidate objects/header into T070 or overwrite accepted artifacts/receipts. Native dedicated binary/framework identities remain unchanged here; if broad native ledgers conservatively include md3.h, MAIN must explicitly reconcile actual dedicated-server consumers/update the ledger or authorize the appropriate rebuild, never invent another raw-hash exception or reuse D052's sound.h exception.
3. Keep T074 and this pre-application evidence immutable. Recheck actual position-only output, attached-model/null/missing tag/later-part/unlink/consecutive-frame cases under the approved production fix; then real MD3 animation/interpolation/tag_head/attachments/cleanup and normal/impairment browser/native baseline as separately released. Candidate compile/helper success cannot pass pixels, physical audio, authority or P1/MVP. Render-derived head/tag data remains unsuitable as authoritative damage input.

No T081 blocker/question remains. MAIN reviews frozen candidate evidence and decides source application/new build/runtime leases. No production application or runtime is authorized by this handoff.
