# T065 canonical network model compatibility handoff

- Worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket/revision: T065 revision3.9; unchanged RELEASED on final review. Submitted for MAIN review; no worker status amendment.
- Governing: D053 additive3.9/browser foundation,GOVERNANCE,P0 0.5; T062 accepted main and T041/T049/T053 accepted original data/config permissions. Gameplay/camera/authority remains outside this component.
- Base:13f0d8eea4822dee5c976661218d022be74342e3 plus shared accepted/uncommitted prerequisite work. Exact before copies: mainc1a5cff4b11569bd19bc6f0b7fac713ad0b64f9c573c9a80d1c84e35b5f3f681; rendermodeldab27171ff5c70bb5fdd9846048e39bfc4dc7e18a65a147398b8c8ae70333649.
- Changed source: source/src/main.cpp only guarded model requirements/preload/read-only snapshot/omission text; source/src/rendermodel.cpp only guarded renderclientp selector. Exact __EMSCRIPTEN__ && OUTBREAK_NETWORK_CLIENT && !STANDALONE guards. New evidence under web/runtime/tests/T065-player-1/ and this own handoff. No other source/header/GL/client/audio/build/out/SDK/pack/asset/old note edits, commits/push/reset/dispatch/dependencies/flags.
- Patches/evidence: main.cpp.patch, rendermodel.cpp.patch and before snapshots in task directory. Source frozen in source-freeze.json before handoff; no post-handoff source edits. Later findings require a question.

## Acceptance evidence

All PASS results below are SOURCE/OBJECT/EXTRACTED-HELPER/DATA-IDENTITY scope, not actual running model/render proof.

| Criterion | Result and evidence |
| --- | --- |
| Genuine existing loader/config/default-skin path | PASS source inspection: loadmodel tries native MD2 then MD3, evaluates existing MD3 config under IEXC_MDLCFG and caches real model. Canonical configs md3load tris.md3, md3skin body skin.png, scale/translation/animation commands. md3skin assigns actual mesh skin via textureload. vertmodel mesh uses tex<0 explicit id, tex>0 texture slot, otherwise configured skin->id; selector passes tex0. Loader/config/vertmodel/direct draw/GL code unchanged. Actual decode/load/draw NOT RUN. |
| Required models and preload ordering | PASS actual source/extracted helper. After GL, texture, config/font and particle setup, before map/remote begin/frame schedule, require all nine canonical mesh/config/PNG files then call actual existing loadmodel exactly for outbreak/survivor,pistol,rifle. All three outcomes collected, published, and any false result causes visible fatal naming the failed canonical model. Missing required file remains genuine visible fatal before a fabricated preload snapshot. No default/stock fallback in new code. |
| Truthful model diagnostics | PASS extracted EM_JS/fake window: OUTBREAK_MODEL_DIAGNOSTICS schema1/profile network-client, exactly three deep-frozen {name,loaded} entries, nonwritable property. Boolean values are real loadmodel pointer outcomes in production; all eight supplied combinations tested. No model pointer/action/counter exported; existing engine/audio/network diagnostics unchanged. loaded does not imply successful pixels/skin/animation/GPU or actual remote visibility. |
| Genuine player/body/skin binding | PASS extracted actual renderclientp/current source: null actor ignored; every existing nonnull actor passed unchanged to renderclient with outbreak/survivor and tex0, bypassing native SKINBASE/custom/team JPG/playermodel resolution only in network profile. No actor allocation/ghost/mannequin or forced local visibility. |
| Exact weapon attachment selection | PASS current extracted selector: actual GUN_PISTOL->outbreak/pistol; GUN_ASSAULT->outbreak/rifle; null, all other native IDs and out-of-range types remain body-only. No world/stock path or misleading other-gun alias. Real renderclient retains tag_weapon handling and dynamic actor pointer. No weapon state/stat/loadout/spawn/physics changes. |
| Existing animation/tag/visibility behavior preserved | PASS strict byte-scope assertion outside renderclientp: actual renderclient animation selection, eyeheight/position/crouch/death/interpolation/dynamic-player object, tag_weapon/tag_head and renderclients code untouched. Extracted actual renderclients tests preserve first-person local living omission, genuine remote spectator/spawning/follow-first filters, follow-third/dead/reflection cases. External renderclient is a recorder in this test; deeper native death/animation/tag rendering is source-preserved, not executed as real rendering. |
| Canonical data/config permissions unchanged | PASS data.py read-only fixed T041 manifest7a232c... identities. All19 original model files identical across models/media-profile/audio-profile/network-profile model subtrees. Mesh/config/PNG bytes and sidecars unchanged; header frame/surface counts and tag_weapon/tag_head names in every survivor frame match accepted data. Actual configured body/skin references match. Three assembled profiles retain exactly five MDLCFG permissions before isolation. No script/config evaluation, data generation or asset mutation; not acceptance of whole pending network pack. |
| Strict source scope and main behavior preserved | PASS check.py: renderer prefix/suffix outside selector exactly before; main reconstructed by removing only preload helper/call and omission text equals before byte-for-byte. Thus T062 bootstrap/frame/timing/shutdown and T059 input/audio path beyond the approved insertion are untouched. No Engine T061 file/header overlap, camera/physics/weapon/global renderer changes. |
| Native/OFFLINE preservation | PASS actual native and OFFLINE unifdef token equivalence for both translation units against before snapshots; real native syntax release/debug and OFFLINE Wasm release/debug pass. Native stock behavior is preserved in those profiles. |
| Current genuine Wasm objects and stable inputs | PASS12 whole-TU checks:4 native syntax plus8 actual OFFLINE/NETWORK release/debug Wasm objects. Same approved installed SDK/ports/flags, approved network macro only, frozen cache/task-local outputs. Complete source/header membership/hashes before/after stable each invocation; exact argv/environment/tool/command SHA-256, logs/object signatures/hashes in result.json. No compatibility/error stubs or full link. |
| Final freeze/readonly pins | PASS final-evidence.py: actual fresh preprocessing matches current source and helper input; all compiler/helper/diagnostic/data reports match final current hashes, readonly audio/header/loader/ticket/data pins stable,8 objects match reports, git diff --check passes. |
| Full integration/real model or remote visuals | NOT RUN. Full link, actual engine MD3/config/PNG decode, real skin/material/culling/animation/tag attachments/direct-draw/GPU/pixels/remote player appearance/headed recovery/audio/performance/P0/P1/MVP all remain separate MAIN integration/runtime gates. |

Reproduce component evidence from repository root:

```sh
python3 web/runtime/tests/T065-player-1/check.py
python3 web/runtime/tests/T065-player-1/helpers.py
node web/runtime/tests/T065-player-1/diagnostics.cjs
python3 web/runtime/tests/T065-player-1/data.py
python3 web/runtime/tests/T065-player-1/final-evidence.py
```

- result.json/per-TU logs/patches/native-offline-network preprocessed before/current files: exact12 real commands, stable full input closure, token hashes, tool/environment identities, eight Wasm objects.
- helper-result.json/extracted-helpers.cpp/logs: actual current network selector/visibility/preload, real native enum declarations, fake filesystem/loader/renderclient; all8 model-outcome combinations,9 missing files, exact selected attachments/no stock calls and visibility cases. Production real translation-unit compilation independently validates genuine interfaces; the fake tests do not decode/load/render models.
- diagnostics-result.json/extracted-model-diagnostics.js/log: current actual immutable emitter with fake window, all outcomes/deep freeze/schema and other snapshots preservation.
- data-result.json/data-before.json: exact manifest/model identities across4 stages, MD3 header/frame/tag metadata and canonical config/MDLCFG permissions, read-only throughout.
- final-evidence.json/source-freeze.json: final current source/object/read-only identities verified before this handoff. All outcomes clearly separated from actual runtime/model/GPU proof.

Environment: macOS26.5.1/Darwin25.5.0 arm64; Apple clang17.0.0 (clang-1700.0.13.5), Node v24.13.0; reused installed Emscripten7.0.0 compiler777e6e5db7b4990bcaeb1b9998ed642cc84e6629 under /private/tmp/outbreak-web-sdk, accepted SDL2/image PNG/zlib/Vorbis ports and frozen SDK cache. No installs/dependencies/SDK changes/new build flags. Task-local temp/node caches. No performance claim.

Final frozen source SHA-256:

- `source/src/main.cpp`: `ec652351aa25219a2c1d8e88d2b2aae2319703e08bcd5900242a8398c9df803f`
- `source/src/rendermodel.cpp`: `5d63f8b8e062e835a7f9b25d17a9f74a09bfd6bf66469311288e681512e2c671`

Actual Wasm object SHA-256:

- `main-network-debug.o`: `0dbf3478dabe5a4cc7f77df1790173bccc9ffd58f25e9cc67216908eabb133e5`
- `main-network-release.o`: `ee35a406caa72e0cf4b96aae52e801c6bc41e4d87d3ed26914beac783d1cf55c`
- `main-offline-debug.o`: `48d63640a65420b83ac2ac9bfce60cb05ace1d0ce76ebd4414e7e88c7a462b90`
- `main-offline-release.o`: `cfc2af265c51550aa5223f2f4c2d79df8133bdfdfbfd2b29cd654fb5300e4c1d`
- `rendermodel-network-debug.o`: `3ba81399f21795f7af5c54000aef616994ef23b9a73fa1e740a61291fab5d82b`
- `rendermodel-network-release.o`: `3e7f2969c871105b52512e1d4672fa9d35d756ee6c49e77d2b8a082191357138`
- `rendermodel-offline-debug.o`: `7926d982119222302538fc9c14ed8b0e497ab082ebf8d4ea285b37df99739cb4`
- `rendermodel-offline-release.o`: `94a016edac5ba80c316755152007c0aaf357a2a5c6ae53465d0c9323ce3db7bd`

## Implementation status

Implemented source compatibility only: real canonical model preloading and immutable outcome diagnostics, genuine actor render path body/default-skin binding and exactly two supported attachment IDs. Existing animation/tag/visibility and native/OFFLINE behavior preserved. HUDgun remains0. No always-visible local body, ghost actor, physical pixel or P1 shoulder-camera/aim-alignment/authority implementation.

Simulated: external preload loader/filesystem/renderclient calls and fake window. Data inspection reads actual accepted binary/config/PNG identities and bounded header/tag metadata; it does not execute native decode or evaluate configuration. Actual CPPs compile into genuine profile Wasm objects, but no engine/game/browser run or full link.

Incomplete: runtime MD3/skin/config decoding success, pixels/culling/material/shadow/direct draw, animation interpolation/attachment pose alignment, genuine remote appearance and actual load failure handling in a running browser. loaded is the actual loadmodel result only; required-file/byte validation does not establish those runtime gates.

## Integration and questions

No new headers/shared API/assets/dependencies. MAIN must pin/rebuild both changed translation units in combined accepted network recipe with accepted original model bytes and five MDLCFG commands; T064 network map derivative preserves these model bytes, but its map/data acceptance remains separately owned. Preserve old OFFLINE/audio builds and earlier evidence.

Observe exactly three canonical preload outcomes after real GL/config init, no stock body/team skin/unsupported world gun requests through renderclientp, actual native actor animation/tag behavior and existing local/spectator visibility. Verify pistol/rifle attachments and unsupported body-only selections without injecting extra actors, forcing state/visibility or treating loadmodel success as GPU proof. All third-person camera/gameplay authority work remains later scope.

No unresolved T065 scope question/new human hold. MAIN reviews exact frozen source/evidence and owns acceptance/integration. Source remains frozen after this handoff; later findings require a new question.
