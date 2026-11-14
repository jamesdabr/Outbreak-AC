# T074 position-only MD3 tag regression handoff

- Worker: Player / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket/revision: T0744.7, RELEASED on final read. MAIN owns acceptance/status and any later production lease.
- Governing: D066/browser foundation,GOVERNANCE,P0 0.5 isolated source-derived regression; no gameplay/renderer-interface implementation authority.
- Base/pre-existing work: shared frozen accepted source and T070 published/original bundle. No production edits, source resets, build changes or clean-checkout claim.
- New files only: web/player/tests/T074/** and this own handoff. No additions under web/runtime or existing source/header/assets/tooling/SDK/build roots. No commits/push/dispatch/dependencies.
- Final outcome: **BUG_REPRODUCED in source-derived helper. Production NOT FIXED. Actual engine/render/GPU/game NOT RUN.** Evidence frozen before this handoff; later corrections require a new note/release.

## Result and cause

Current exact MD3 setup loses the nonnull output pointer when attached model is NULL. Its call `link(NULL, a[i].tag)` selects the default `pos=NULL`. Actual outer vertmodel::link forwards that NULL; actual part::link stores it in linkedpart.pos. The actual tag-propagation loop then skips an empty link and never writes the caller's output. The existing attached-model branch already forwards a[i].pos and works in the same fixture.

Independent oracle: tag-local translation(1,2,3), fixed parent +90° Z rotation and translation(10,20,30) gives `(8,21,33)`. The initial output is the distinct sentinel `(-77,-88,-99)`. Oracle is manually calculated, not obtained by calling the implementation under test.

| Case | Actual result |
| --- | --- |
| Current position-only setup | Output pointer not retained; output stays(-77,-88,-99), not(8,21,33). **Two independent expected-position assertions fail.** |
| Candidate isolated copy only | Changing the guarded setup call to `link(NULL,a[i].tag,a[i].pos)` retains the pointer and the real matrix/propagation logic writes(8,21,33). No production header changed. |
| Current and candidate attached-model+output | Both pointers retained, child index assigned by actual code, output(8,21,33), child entry observed. No GL draw claim. |
| Both copies' controls | Missing tag/no fabricated output/index; attached model with null output; null model/output; null attachment array; unloaded setup return; later-part lookup through both actual link methods; repeated unlink and no later stale output/child use all pass. |

The **single native executable exits47**, preserving the current-code failure. stdout records CURRENT_EXPECTATIONS_PASS=0 / CURRENT_FAILING_ASSERTIONS=2 / ISOLATED_CANDIDATE_EXPECTATIONS_PASS=1 / CONTROL_CASES_PASS=1 / CLASSIFICATION=BUG_REPRODUCED. stderr preserves both ASSERTION_FAILED CURRENT_PRODUCTION_LOGIC messages. The driver exits0 only because it successfully recorded the deliberate nonzero regression result; it does not report the broken production expectations as passed. No second compile or executable run occurred.

## Acceptance evidence

| Criterion | Result / evidence |
| --- | --- |
| Required governance/ticket/D066/question inspected | PASS read-only AGENTS/required MVP/D066/T071 tag question and actual MD3/vertmodel/model/geometry code. |
| Real MD3 setup and both real link methods | PASS exact extracted source bytes under extracted/*.inc. Runner checks original full-file SHA-256, byte range equality and extracted hash before compile. No replacement implementation of the link decision. |
| Real position propagation / independent oracle | PASS source-derived causal evidence: exact complete tag propagation loop and entire actual geom.h matrix/vec implementation used. Local pose matrix is an explicitly fixed fixture input; expected world position calculated independently. Current and attached-model contrast show fixture can propagate the expected result when the pointer survives. |
| Current failure preserved, not relabeled success | **BUG_REPRODUCED**; native exit47 and two failing expectation messages preserved in raw logs. Source-derived regression outcome only, not a real rendered defect observation. |
| Candidate correction isolated | PASS evaluation only: exactly one setup-line difference in extracted/md3-setup-candidate.inc/candidate-only.patch. Original cleanup remains two-argument unlink, clearing both pointers. No shared/production fix applied. |
| Contrasts and cleanup semantics | PASS controls in both copies listed above. Cleanup is repeated; a new sentinel/next propagation proves no retained output write or attached-child entry after unlink. Missing lookup leaves unrelated tag state alone; later-part search exercises both methods. |
| One inspected local native C++11 compile/run | PASS compiler exit0, empty compiler stderr; one executable run exit47. Exact argv/tool/version/hash, owned temp/cache environment, executable/source/extract identities in result.json. No SDK/Node/Wasm/full client/GL/browser/game/server/network/install. |
| Frozen source/artifact membership and bytes | PASS before.json == after.json, identical SHA-256 below. Captures97 source/src files,9 ENet headers,17 historical offline-output files,17 published network-output files,17 original T070 bundle files, plus named T070 terminal freeze/audit/ticket/AGENTS files. No current runtime-closure source was written. This is not a rerun of T070's whole23474-input evaluator. |
| Evidence frozen | PASS evidence-freeze.json hashes27 evidence/input/executable/log files, including exact extracted current/candidate code. Native failure/candidate/control receipts immutable; run_once.py prevents a second invocation. |
| Actual full renderer/model/animation/GPU/browser proof | NOT RUN. No real MD3 decode/config/mesh/tag interpolation/GL/render/actor/game or production profile compilation/link after a fix. No P1, authority or gameplay acceptance. |

### Exact source anchors and identities

extraction.json contains source byte offsets, one-based line cursors and extract SHA-256 for11 records. `byte_end_exclusive` is authoritative; `line_end` names the exclusive cursor's line and may be the following line after a newline.

- source/src/md3.h setup at159+, dropped optional pointer at166; cleanup unlink at201. Full file SHA-256 `635f904dafa3bbc63dc13c6f0a09c9cd3d6063d0e2d0dee8a1b95368fe19ec84`.
- source/src/vertmodel.h part::link at716, model::link at1267, linkedpart at671, actual propagation loop915–964. Full file SHA-256 `1466a707c8eb7a3b76c098f0babff87baf4c6903657f7ddea93c3e0c419e1c98`.
- source/src/model.h modelattach at29+ and ANIM_PARTICLE definition; full SHA-256 `208f14beb457e7529c1cbb75ddd9ee8757cb195284be0dacfe7459cf6ae180d9`.
- source/src/geom.h entire actual native math, SHA-256 `2e6360980d3b891c04aebd443f9ba20edffd604bf6eec11b74eb37674ff404b2`.
- source/src/tools.h actual RAD definition at88; full SHA-256 `e53d32d55e5b81ac5e5be3e8a2411a8363dae858631f06cfd3ed11b16eef6fcf`.

Current extracted setup SHA-256 `06d1d06e468c33621691fdaea2b14704e34ca652c8052dfeac18d66ec3abfe43`; isolated candidate `00d8b2b66e3840b980454d0cee316aff9d332aec4669181992adc0a8aa9c48ee`.

### Commands and tool identity

Commands actually executed from repository root after reading the extractor/harness/runner:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/player/tests/T074/prepare.py
PYTHONDONTWRITEBYTECODE=1 python3 web/player/tests/T074/run_once.py
```

One native compilation (actual argv, not a second invocation):

```sh
/usr/bin/clang++ -std=c++11 -O0 -Wall -Wextra /Users/jd1/code/apps/outbreak/web/player/tests/T074/regression.cpp -o /Users/jd1/code/apps/outbreak/web/player/tests/T074/regression
```

One run: `/Users/jd1/code/apps/outbreak/web/player/tests/T074/regression` →47. Do not rerun this frozen directory; a future attempt needs new scoped authority/output path.

Apple clang17.0.0 (clang-1700.0.13.5), target arm64-apple-darwin25.5.0; host macOS26.5.1 arm64. Compiler binary SHA-256 `179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818`; regression.cpp `58750ac06dabb51c9ed8c027ebb4208a186aa5d1e9f5edcbdea9a20f15cb9c45`; executable `178efad020a5e510fd077306e28dc6ce936f9afe59f63d11207888318767be74`. Compiler version query is metadata, not another compilation. TMPDIR/CLANG_MODULE_CACHE_PATH and all generated files are task-local. No performance claim.

result.json SHA-256 `15d4b97abefc0399e8b824646b9154a42ed90ddcf2f849becaf7e1a3c7e90694`; evidence-freeze.json `60eec9a1ef458e049d713fe36031d6328cbad2fd7531e1e6a2524c890226fa9d`.

### Frozen artifacts preserved

before.json and after.json both SHA-256 `ab9afdc62df841c3b8c212b99b336da5c9767d8ef50de210566e796e67a7d46d`. Full memberships/notices/hashes retained there, not just runtime extensions.

Published network-out and original T070 bundle have the same unchanged four files: html `23f2ee9f9a86f7877ba9125d5fb9b79d94426c00e7692d0de74da022bf2b1775`; js `c102855d8ec1cf74f9bef7ec8ae05203d8334094b0f416578fe0d0243653fad0`; wasm `b8cafcb5915ce0a6b199dcb724d12bb943567eb05449c4406cbb518bd5630b39`; data `dcc9b311beae85a4c20945ca55e94c914b16b1694c00870b36d52a8afb4a78a8`; metadata `5447bdcc68e3f732ba37bdaf2c03b8ec0f2258e45d4dc6f336acfa39b1eef037`. Original T070 bundle_id remains `35bad2ff04cdc17df5193ca026969380e7c9dc4176596601972b4af163b90e0a`.

Historical offline output unchanged: html `22b4e8d79b6032639783f075a2d7bed69dde780476b2889ae80cff19f34a1725`; js `bce8c3163cb96cbc6cf2baf9d5036cba5ba73611c205b5b60962c667420e6c89`; wasm `1bce63028e054a43e70441769bf4dcbd8b3173ae792ce608de17822424b4f633`; data `66574ce6af122f6c10fdfa51c7030c6f25511bd0936f09d292e07f316cd30877`; metadata `0a5af803868724911dc27cfc7db76c7e026a619a063421944c59fa65d65d703c`.

## Implementation status and limits

Implemented only new isolated extraction/harness/receipts; production bug remains present. Actual setup/link/propagation logic and native math were compiled and exercised; the full original MD3/vertmodel classes/translation unit were not linked into a game.

External fixtures replace model/actor base types, vector/tag storage and animation-pose generator with fixed matrix inputs; particle callbacks throw if reached and stenciling/particles are disabled. The part entry wrapper contains the real propagation loop; no mesh renderer/GL is invoked. Fixture child-entry counts are not real GPU draws/frames. No actual MD3 loader/config/animation interpolation, GPU/head-tag/pixel correctness claim is made.

## Future narrow production recommendation — not authorization

If MAIN releases a fix, lease only source/src/md3.h's guarded position-only setup call plus new appropriately owned tests: forward `a[i].pos` as the third argument. Leave cleanup's two-argument `link(NULL,tag)` unchanged so it still clears the pointer. No model.h/vertmodel.h/shared API/assets/wire/physics/damage change is indicated by this regression. A common-header fix intentionally changes valid native position-output behavior too; do not claim native token equivalence for that approved semantic correction.

Future evidence must retain this original failing witness, repeat pointer/output/attached/missing/null/later-part/unlink cases under the new authorized attempt, compile affected genuine native/OFFLINE/NETWORK consumers and re-evaluate dependency/header closure. MAIN must pin/rebuild a new artifact separately without altering T070/current baseline receipts. Actual MD3 pose/interpolation/tag_head and attached-model behavior on real rendering, across consecutive frames and cleanup, remain necessary runtime checks; no broad renderer/GL suppression or authority based on render head positions.

No T074 scope blocker remains. MAIN reviews exact frozen evidence and decides any later fix/integration release. Current T067 baseline remains independently pinned/authorized; this handoff does not waive its real media/authority gates or authorize a rerun.
