# T089 — Production MD3 position-only forwarding applied

- Worker: Player / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e.
- Ticket/revision: T0895.12, RELEASED at final read; dependencies D081/D085/D084. MAIN owns acceptance.
- Governing: GOVERNANCE/BROWSER_FOUNDATION/P0 0.5 exact compatibility subset only. No new gameplay/API.
- Base:13f0d8eea4822dee5c976661218d022be74342e3 plus preserved overlay. md3.h had no pre-existing diff and matched the required original full hash. Other dirty/untracked work preserved.
- Changed: `source/src/md3.h` line166 only; NEW `web/player/tests/T089/**`; this NEW handoff. No commits/reset/dispatch/status/contract/old evidence changes.
- Outcome: **SOURCE_APPLIED; APPLIED_PRODUCTION_SOURCE_LINKED_REGRESSION_PASS; FULL_BUILD/ACTUAL_RENDER/GAME_RUNTIME/AUTHORITY NOT RUN.** Source and evidence frozen; Engine T088 may observe the final current header identity. Future modification/rerun requires a new lease, not alteration of this evidence.

## Acceptance evidence

| Criterion | Result and evidence |
| --- | --- |
| Exact approved full-header application | PASS. Before `635f904dafa3bbc63dc13c6f0a09c9cd3d6063d0e2d0dee8a1b95368fe19ec84`; after `f60cdc019579cba4876ff741438934c56b6d626ac55c36c28e8b8ab8abe644be`, byte-identical to T081 accepted full candidate. Only change is `if(a[i].pos) link(NULL, a[i].tag, a[i].pos);`. `source-only.patch` and full original snapshot retained in T089. |
| Cleanup and unrelated source preserved | PASS. Line201 remains two-argument unlink. Extraction hash unchanged `dbbcf6801ca85076d7780b9d8da3c1e60e5383819d317745640aaad68d5e7478`. before/after snapshots differ only in the approved full md3.h hash. No model/vertmodel/GL/asset/API changes. |
| Actual production extraction, original and accepted candidate distinguished | PASS. `extraction.json` records exact full source hashes, byte and line ranges. Production setup extracted from the actual post-application source; original setup separately extracted from own full pre-application snapshot; comparison separately extracted from frozen T081 full candidate. Applied slice equals accepted candidate and exactly one-line-transformed original. Not a renamed old candidate result. |
| T081 helper/control fixture provenance | PASS. `helper-reference.cpp` is byte-identical SHA `58750ac06dabb51c9ed8c027ebb4208a186aa5d1e9f5edcbdea9a20f15cb9c45`. Adapted dispatch/labels/main add separate accepted-candidate comparison and consecutive-frame control; existing fixture/control methods retain their behavior. Real source link/propagation/geom/modelattach slices are hash-validated against T081 and current production. |
| Single compile and native run | PASS. One `/usr/bin/clang++` compile exit0, empty compiler stdout/stderr, one new helper run exit47 intentionally preserving original failure. Driver exit0. No retries. Compiler-version probe exit0 is separately recorded, not a second compile/run. Exact argv/environment/source/tool/executable hashes and actual .d dependencies in result/evidence. |
| Position pointer and independent oracle | PASS applied production: pointer retained, output `(8,21,33)` from fixed parent90°Z+(10,20,30), local(1,2,3). Accepted-candidate comparison also passes. Preserved original drops pointer and leaves sentinel(-77,-88,-99), exactly two expectation failures retained in stderr. |
| Controls and consecutive frames | PASS attached model, missing tag, null output, null attachment, unloaded return, later-part lookup, default unlink and no stale attached/output reuse. New applied-production frame sequence `(8,21,33)` then local(4,5,6)→`(5,24,36)`, repeated unlink, subsequent untouched sentinel; balanced matrix stack. All three paths' retained controls pass. |
| Historical evidence/native/artifacts preservation | PASS snapshot membership/bytes for T074 and T081, full source/ENet, original and signed frameworks, accepted old/offline/network/T070 bundle outputs, native release/debug binaries and lifecycle ledger, AGENTS/ticket/D085. Only approved md3.h differs. Original artifacts, dependencies, old ledgers/pins remain historical and unchanged; no raw-hash exception created. |
| Bounded execution | PASS. Inspected own entry points before execution. Task-owned tmp/module-cache/logs only, minimal environment. No SDK/sanitizer acquisition/execution, actual client/renderer/server/browser/network/ports/full build/game run. |

## Exact evidence and reproduction scope

Evidence root `web/player/tests/T089/`. `evidence-freeze.json` freezes33 owned file members;34 files including the freeze itself. No frozen file edits after freeze.

- result.json SHA256 `cb7075537e621daad3dcd15f285ee685b41d45e666bb8013cbfca843232c63c0`.
- evidence-freeze.json SHA256 `e3331609fe819b6b526cc1436bd8cb06fd1cd7d58a7b1414674fdc489b4a2ae5`.
- regression.cpp SHA256 `bdecd64ae4c98110acd9fa287851f1f2d4c4754ff8811d60c45ad68352e147f4`.
- extraction.json SHA256 `37829204ca74c3ca031293ad06002f569083a012fe62b5c7bc522ca1a5bd7153`.
- new helper executable SHA256 `a392e37d549be0cb674e6a0954be6482a2a128b4c5b901c2bcb5fac159ddb6c4`.

Host macOS26.5.1 arm64. Actual version probe: Apple clang17.0.0 (`clang-1700.0.13.5`), InstalledDir `/Library/Developer/CommandLineTools/usr/bin`. Invoked `/usr/bin/clang++` SHA `179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818`; tool-identities.json separately hashes CLT clang/clang++ targets after the run. Compile uses `-std=c++11 -O0 -Wall -Wextra -MD -MF`, no sanitizer or compatibility workaround. System-header dependency hashes are recorded after compilation and rechecked at freeze; no claim of independent precompile system-header inventory.

Historical commands executed once after inspection, not permission to rerun frozen outputs:

```text
python3 -B web/player/tests/T089/prepare.py
# apply_patch exact source line; full final hash checked before regression
python3 -B web/player/tests/T089/run_once.py
python3 -B web/player/tests/T089/freeze.py
```

The first snapshots/prepares, the second compiles/runs once and preserves the expected baseline failure, the third rehashes/freezes without another compile/helper run. README describes external fixture boundaries and raw receipt interpretation.

## Implementation limits and integration

Production setup now forwards the caller's output pointer. The helper executes real extracted matrix/link/output/cleanup code with external tag pose/container/actor/render-entry fixtures. It does not load MD3 assets, interpolate real animation, render pixels or exercise actual client/server/gameplay. T081's six genuine consumer objects remain historical evidence for these exact candidate bytes; they are not newly linked artifacts from T089.

Existing browser/native binaries and metadata retain their original identities; new full artifacts and complete source/tool/native dependency ledgers/pins need separate releases. No old ledger refresh or D052-style exception was made. No blockers remain for this source/application deliverable. MAIN reviews; no self-acceptance or P0/MVP claim.
