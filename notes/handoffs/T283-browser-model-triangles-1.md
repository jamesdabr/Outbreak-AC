# T283 — Browser model submission correction

Engine /01a1b92b-53f9-7132-aeb9-72b637ac3a90; T2831.0 / STOCK_FIRST_PROTOTYPE0.2 / D481. Changed only `source/src/vertmodel.h` plus this handoff. Other allowed sources did not need changes. No asset, decoder, SDK, candidate, history or Git mutation.

## Evidence and confidence

Inspected actual `notes/previews/T280-stock-player-first-runtime.jpg`: BN_ACTIVE/error0, malformed thin/stretched geometry and floor-like shards. Model preload success and this image do not prove valid draw submission. No regular-Chrome comparison or movement was observed; embedded pointer lock failed independently.

Existing `mesh::render` uses separate position/UV/color arrays with indexed strip/fan draw calls. Cached SDK `/private/tmp/outbreak-web-sdk/upstream/emscripten/src/lib/libglemu.js:3437+` explicitly warns that DrawElements does not prepare client attributes properly and passes **index count** to `prepareClientAttributes`. That function's planar path (`2834–2933`) copies that many vertices, rewrites attribute pointers into its restrided buffer, and can reuse the prepared attributes on subsequent draws. A strip's index count does not describe the full referenced vertex range; this is a concrete compatibility hazard for the actual model submission path. Immediate begin/end uses its own generated layout instead.

Confidence: high that this avoids that specific indexed/planar emulation hazard; moderate that it explains all observed distortion. Root cause is not runtime-confirmed. Same malformed class with both MD2 and MD3 supports a shared draw-path investigation, not mesh redesign.

## Minimal correction

Added one network-browser-only branch after existing interpolation, skin/state setup and vertex lighting, before indexed strip/fan submission. It emits `GL_TRIANGLES` in original `tris[i].vert[j]` order, reads positions from the actual interpolated `buf`, and uses corresponding original UVs and computed vertex-light RGBA. No synthetic geometry or pose.

Before immediate submission it saves current color, disables position/UV/color client arrays and clears the matching engine pointer caches. Arrays remain consistently disabled afterward so the next mesh re-establishes them; current color is restored after glEnd. Existing model matrices/scale/animation, texture selection, depth/culling/alpha and surrounding renderer state remain. Existing no-skin UV behavior is preserved. Native/offline indexed drawing and the stencil-volume path are unchanged. Submitted-vertex accounting reflects the actual three vertices per triangle.

## Verification boundary

Source readback only: checked guard, original triangle/UV/lighting indices, vec float-array access, current-color restoration, cache/client-array consistency and native/offline fallback. **No compiler, test/helper, game/browser, service/network, FFI or runtime execution.** No new fixture/proof framework.

MAIN must build and compare actual output: recognizable correctly skinned player without shards, existing animation/pose/transforms, floor/world state after drawing, and near-wall view. Movement/pointer capture remain separate unverified checks. Immediate submission is a compatibility fallback, with unmeasured performance; no final renderer/MVP acceptance implied. Stable source submitted; stopping before guns or further repair.
