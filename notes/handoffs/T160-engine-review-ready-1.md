# T160 Engine corrected authority-data review-ready handoff

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket: T1601.0, APPROVED AUTHORITY_MAP_DATA0.2/D212. Correction requirements SHA256 be384c76ae620b63ec970f432f20b49e3c47830451da2e16416802749abd0c5d.
- State: REVIEW-READY submission; no self-acceptance, final freeze or consumer release.
- Base: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work; no Git operations.
- Changed files: seven new source/harness/docs, exact nine-file data and fresh tests/attempt-1/** only under web/world/authority-p2, plus this own handoff. Existing authority-p1/production importer/assets/tools/original caches/other leases read-only.

## Scope and correction

PASS: Inspected and SHA-pinned original seven sources, retained T158 handoff/result and both review notes before effects. Complete authority-p1 before/after fingerprints agree, including full source/data/proof/cache/fixtures membership and file bytes/hash/mode/nlink. Original source/data/result remain historical, unaccepted and unchanged; no original driver/import/rerun/freeze/repair.

PASS: assemble.py, wrapper.cpp and wasm_runner.mjs are literal root/ticket substitutions only (runner bytes identical). New verify.py changes only literal root/provenance/authority bindings, supervisor/guard/receipt correction and directly necessary preservation/plan bindings. New tests add actual-method guarded regressions; docs explain corrected behavior. Data math/corpus/importer/tool/byte/time/publication caps unchanged. Seven non-provenance/manifest data products match original bytes; PROVENANCE and manifest correctly bind new source paths/pins.

PASS SOURCE CORRECTION: Popen is inside cleanup protection and returned handle retained before selector/pipe setup. Every setup/work failure enters independent same-owned-child cleanup. Cached reaped handles are not signaled. Kill/ESRCH/error does not skip a still-bounded original-handle wait. Selector/each pipe close attempts remain independent; all action/error outcomes retain first primary plus bounded secondary causes. Reaped/exit are observed handle facts; no-returned-handle and unresolved ownership remain explicit.

PASS DEADLINE/RETENTION: Absolute hard deadline=min(start+60s,whole300s deadline); work ends5s earlier. No new launch after work deadline, no positive grace when expired, and wait bounds are recomputed immediately before use. The295s guard raises into cleanup during work and defers during cleanup/receipt protection. Final deadline/guard checks reject late exit0 and late retention. Bounded in-memory receipts precede independent stdout/stderr/process receipt writes; persistence errors propagate receipt to outer failure.json when writable and cannot remove REFUSE. Receipt files are explicit pre-persistence observed-state snapshots, not recursive proof of their own final write.

LIMITATION: Popen, setup/descriptor close and filesystem OS primitives are not proven hard real-time against arbitrary kernel stalls. Timed select/wait plus finite cleanup/guard cooperation do not attest process-tree lifetime/RSS/performance or physical OS blocking. No unresolved cleanup is relabeled successful.

## Verification evidence

PASS ACTUAL: Sole command `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/world/authority-p2/verify.py`, observed **outer exit0** from exec session62502 completion. Both actual native/Wasm targets link unchanged accepted map_import.cpp and the new test wrapper. **30 real decoder cases per target,2 complete cell responses and28 refusals**. Each complete side/revision/entity_count and all65,536 cell bytes agree with independent Python RLE/struct oracle and each other. Raw expected/native/Wasm each131,912 bytes, SHA256 c0e88b05ee28962b07ad3e783c3ceddcf144f4ad06ba1c893844f8ef972bf578. Complete status/error/input/guard/failure-cell/info/capacity-tail observations agree. No real child fault injections or extra driver runs.

PASS INDEPENDENT DATA: All9 products independently reconstructed (bounded chunked inflate, source entities, integer compass mapping/bytewise anchors and geometry, JSON/provenance/manifest/hash encoders) without assembler helpers. Both reproduction trees equal production bytes. Exact map6650/cells65536/anchors608/geometry66151;21 technical source entities (8FFA+13lights) remain distinct from32 exact canonical deployment alternatives. Separate map/cell/anchor/geometry SHA512 scopes preserved; no complete rules/angles MapHashes invented.

PASS BASE ADVERSARIAL: All71 original finite source/tamper/mapping/notices/license/JSON/alias/path/gzip/slot/heading/binary/manifest/hash/membership/terminal obligations pass in new root. Real malformed map cases remain actual decoder outputs. Simulated terminal work/timeout/report/flush/result/marker/partial-publication failures retain refusal, and rename is denied while exclusive-mkdir/per-file publication succeeds.

PASS GUARDED SUPERVISOR: **44 additional cases through actual Supervisor.run**, not a mirrored supervisor. Fake child/selector/pipes/clock/retention boundaries, real launch/fork/exec/signals/wait/network denied and patches restored even on failure. Cases cover no returned Popen handle; selector construction; every nonblocking/register step; initial stdin close; select/read/write/partial/output-cap; ESRCH/other signal failures followed by independent wait; wait timeout/error; selector/each pipe close; combined primary+all secondary errors; exhausted/near/operation/whole/setup/drain/cleanup deadlines; late0; guard work/setup/cleanup; and independent log/receipt persistence failures. Assertions check SAME original handle, bounded counts/order/timeouts, preserved primary/secondary/output observations, reaped versus unresolved, cached terminal no-signal and real terminal refusal. Every failed fixture retains marker/failure receipt; only control succeeds. Simulated identities/timings are not actual decoder/process proofs.

PASS CAPS: **115 total adversarial cases**,5,117,645 fixture bytes (<128 cases/16MiB). All8 actual compile/link/run operations exit0/reaped, primary null/cleanup and retention errors empty, stderr0, <60s each. Aggregate actual child output263,824 bytes (<8MiB), both-target raw263,824 (<2MiB). Work completion2.7472638330655172s precedes terminal capture under295s guard/300s whole limit. No resource/performance calibration claim.

PASS TOOL/PRESERVATION: Same installed Python3.11.9/Apple clang17/Emscripten7.0.0 clang24+wasm-ld/Node24.19.0, Darwin arm64. Exact aliases/resolved identities, native/SDK headers, argv/environment, new and original source/input/corpus/layout/exports/capacities and work/cleanup plan retained before effects. Own verified copied frozen sysroot/cache/tmp/module/Node paths only. Actual direct dependencies captured before target execution and checked unchanged. Eight advisory pins/four original mappings, strong named source/input/authority identities and named original-cache before/after snapshots match. No whole-workspace preservation claim.

PASS TERMINAL: Root result.json canonical PASS, REFUSE/failure.json absent; all comparisons/cleanup/preservation/evidence/reporting+flush precede bounded result+directory sync, then REFUSE removal is final required driver effect. Exclusive data mkdir and no-follow/exclusive file creation, no directory-rename atomic/no-replace claim. Actual outer exit0 captured separately; stdout terminal-pending text is not PASS proof. Later MAIN acceptance/pinned final graph remain required before consumption.

## Exact identities

Paths below relative to web/world/authority-p2.

| Source | SHA256 |
| --- | --- |
| README.md | b240b5cc7ebe4ef1469ef23567870cecb3d7ad709579224502facacc65266b48 |
| SCHEMA.md | be015cb7e32eb6e5376a5308d14c197f58a749691e458047571a7ff814ab7ab8 |
| assemble.py | 97bc7ccc2b31a881539198bec8d5959493c295135a94d19a78dbb97668deae0a |
| test_adversarial.py | af77747fa30cc0a566b382313eeb847aaf3a88a3d42a3c24b9369928fc5ce0e3 |
| verify.py | 720dd8aafb4546907ce73e72ac3bf972156cd67af4357b171ba01481b8d0e26d |
| wasm_runner.mjs | 2ed359db40734cc0b7ac420829f997c7475669e34acb66dd9918701a8d853991 |
| wrapper.cpp | 4fa827c174ab4d3a78ae2fce9456536f81755019f52818cd18045587e3f7808e |

| Data product | Bytes | SHA256 |
| --- | ---: | --- |
| data/PROVENANCE.json | 4159 | 4521a3977c2f40166b71e75189cba7ae7f820368892b25c816ace94695037ed5 |
| data/anchors.bin | 608 | f95e351084d8fb074330583e34f8cc5c872bf43d5b5de38a6390aa13bcec2538 |
| data/anchors.json | 7768 | b13da1a7ddaae4d3e27585a5c5da503e4e73e2500cd8a861c284045987625808 |
| data/cells.bin | 65536 | 67599b72139ac374b36efb192145ca3b779073c524e10fef8bfa16f8b07d9a7d |
| data/geometry.bin | 66151 | 46a2e46dd316213b955c15b7027b847e321a726664f6fbd754cecd3b98241174 |
| data/map-manifest.json | 4408 | e9cd8037b522a55c1578984ab6f285fab2a182ddf7f2e6a9c4df926a7ecdd9d8 |
| data/map.raw | 6650 | a96e70c9ef7f347dcbf36271b8cc7029c583465fa4bad5487f987ddae2f44c0c |
| data/notices/blackwood-candidate/LICENSE.txt | 1300 | d597a754790e54f9ee13788b3c2f1ded4c0edc60c3d37251c787d5d7f648d47e |
| data/notices/blackwood-candidate/PROVENANCE.json | 3103 | 0da2da2801d55e0afab1abf2ec1d0ed4e25bd4bf41d8a225cad37e5aa8809676 |

| Record under tests/attempt-1 | SHA256 |
| --- | --- |
| plan.json | f2384fa6ded203e9ec95decd52ccfd9eb419b9eea79e2f4d1976d39fca57749c |
| result.json | 0edc0edf59108818660839ce5dc887e4d34131c8bcf78fea5f15bb8f4b8f9dad |
| adversarial.json | 6faa975440ac50106b18a581aa3906616d734064a3d07b487967e004b556a2d2 |
| processes.json | 7ccd9193084eca473791a3f912561fd6a09c3be32ddb459a43dab20843a22aec |
| dependencies.json | bdc682280256199b28de2b7dd4e8a29b1977d895b2522fbaa1d89839f3c090a8 |
| corpus.bin | 3b3ffe92406592ac0f3d067b1f9ead7494dcbe2ff407ff5ebf0a87ba96dec9d3 |
| expected.bin | c0e88b05ee28962b07ad3e783c3ceddcf144f4ad06ba1c893844f8ef972bf578 |
| native.bin | c0e88b05ee28962b07ad3e783c3ceddcf144f4ad06ba1c893844f8ef972bf578 |
| wasm.bin | c0e88b05ee28962b07ad3e783c3ceddcf144f4ad06ba1c893844f8ef972bf578 |
| protected-before.json | 42f0c5677ca40aef42dca73176b56d4bf1f8f74b6980543bce29e5b6ccac9fdc |
| protected-after.json | 42f0c5677ca40aef42dca73176b56d4bf1f8f74b6980543bce29e5b6ccac9fdc |
| input-identities-before.json | 87d9dcdec14c07db6db2c2c16cebdc9d995d7c5f1ef31d1b143458c99d7b5a98 |
| input-identities-after.json | 87d9dcdec14c07db6db2c2c16cebdc9d995d7c5f1ef31d1b143458c99d7b5a98 |
| original-root-before.json | 63c7baafcd19a66f20463a51ede7f1139b5bf775bc2a09de3e128e30a3175162 |
| original-root-after.json | 63c7baafcd19a66f20463a51ede7f1139b5bf775bc2a09de3e128e30a3175162 |

Computed separate SHA512 product scopes are retained in result.json/map-manifest.json. Actual binary products match preserved originals and MAIN source-only reference; neither prior record substituted for fresh real decoder execution.

## Inventory and pending review

Current entire owned root: **2507 ordinary nlink1 files**, **326 directories** including root, **0 links/specials**. Historical runtime inventory has2830 members before result/marker commit. Current tree equals that map plus result.json and two otherwise-unlisted ancestor directories (authority-p2 and tests/). Existing inventory members were rechecked without project imports/reruns. Canonical review graph SHA256 85cf3d1876ee370c1d2e0b5ab9f32767dea30d9e8ab5909aef93773eaecbc958: JSON sorted keys/two-space indent/final LF of files(repository-relative bytes/SHA256/mode/nlink records) and directories(sorted repository-relative paths). No additional attempt checkpoint/freeze was appended after terminal commit. This handoff is outside the owned root.

All current source/data/evidence bytes remain immutable pending MAIN review. Runtime inventory remains explicitly historical and will not be silently resealed. Separate clearance is required for final inventory/receipt/freeze append roles. MAIN alone accepts this corrected package and releases consumers; Engine retains writer ownership.

## Unimplemented and gates

NOT RUN / unreleased: query source/API/storage/installers, packet/batch/admission/time/life/window eligibility, map generation/config/startup/client mounting, app/browser/server/service/network, capsule/nav/renderer/balance/grants/gameplay/P0/performance/human acceptance. No original/project driver imports, installs/acquisition, Git or production source edits. Scoped notices and four candidate limitations remain. QA/runtime/RSS/human holds unchanged.

No unresolved data/decoder question raised by this run. Reusable supervisor/source correctness awaits MAIN review; passing observations do not selfaccept it. Occupied attempt must not rerun. Engine stops for REVIEW-READY/standby.
