# T046 scoped WebGL1 graphics/targeting compatibility — stable source/object handoff

- Worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T046 1.9 RELEASED; submitted for MAIN review, not self-accepted
- Governing baseline: AGENTS; browser foundation/GOVERNANCE/P0 0.5; D024 additive 1.9 and measured D022 GPU evidence.
- Changed source: `source/src/rendergl.cpp` only gl_init's browser shade/hints and readdepth; `source/src/rendercubes.cpp` only browser strip/client-array rebasing. No other source/headers/build/QA/pack/contracts/decisions/earlier notes edited.
- Evidence root: `/private/tmp/outbreak-t046-player/`: initial source/status/hash snapshots, two narrow patches, exact source/header/tool/command/object hashes, native partial-preprocessed files, target nm logs and extracted helper evidence.
- No commits/push/reset/revert, new dependencies/ports/flags, GL stubs, service/browser/game launch, asset changes or host-profile operations.

## Stable source hashes for Engine

| Source | SHA-256 |
| --- | --- |
| source/src/rendergl.cpp | `b4f2985faa2ff3ac48567b7447e4d2baeeb10ec7b78edbc352ec54da38705c04` |
| source/src/rendercubes.cpp | `46eabe02c06a7d42b93e39fcb6cff125dc396b82abb2ba8e6bbe70a2115bd9b7` |

Prior main/editing/vertmodel/rendertext/worldio submissions and every D003-protected combat file remain unchanged. The existing AI-owned WaypointClass guard is byte-preserved; the source verifier checks rendergl outside the two allowed functions exactly.

## Acceptance evidence

| Requirement | Result | Evidence/limit |
| --- | --- | --- |
| Real CPU center-ray query/projected depth, browser shade/hints only | PASS — source/compile/extracted geometry | Browser unprojects the actual center far point through inverse MVP, invokes existing real intersectgeometry, then projects actual result through MVP into finite [0,1] depth. Validates homogeneous divides/finiteness. Unchanged far endpoint yields exact no-hit depth 1 for existing edit behavior. No fixed target/depth substitute. Browser omits glShadeModel and only fog/line optimization hints; fog and other rendering remain. Native code preserved. |
| Real first-zero strip rebasing with original attributes/draws | PASS — source/array helper | Each browser world/sky/shadow strip points at its actual first vertex and draws first=0 with identical primitive/count/order and attribute stride/data. World colors remain; shadow has the original position/UV-only layout. Invalid capacity fails visibly rather than truncating/omitting a draw. Native multidraw/first-index path unchanged. |
| SDK source mechanism/attribution | PASS — concrete source mechanism; exact 23-warning attribution NOT RUN | Installed libglemu requires quad first%4==0 and computes index byte offset first*3. Engine starts are arbitrary across mixed triangles/strips. Exact counterexample and SDK hash below; source does not disprove this fix. Whether every observed D022 warning came from this path still needs real QA/trace; no runtime-causality claim from helpers. |
| Meaningful bounded geometry/array checks | PASS — helper only | Actual engine matrix/inverse/triangle/corner/geometry query and current readdepth fragments tested against bounded wall/floor/ceiling/miss/orthographic cases; invalid zero/nonfinite divisors fail. Actual strip-rebase fragment with real vertex/shadow layouts preserves positions/UV/colors/count/primitive/index bounds. Details below. No GPU/browser fixture substitutes. |
| Actual native + target release/debug and native preservation | PASS | Four native whole-TU syntax checks and four actual pinned Wasm objects exit 0 with empty diagnostics; all source/header inputs stable. Native partial-preprocessed tokens identical for both sources. Target rendergl lacks glReadPixels/glHint/glShadeModel imports; rendercubes retains real glDrawArrays/glVertexPointer/glColorPointer/glTexCoordPointer imports. |
| Scope/stable handoff/actual GPU gate | PASS — source/object handoff supplied; real GPU/visual/input NOT RUN | Exact source/object/command hashes, patches, tests/logs and limitations supplied here/result.json. MAIN accepts, Engine links same profile/pack, QA checks actual graphics. No suppression, fabricated counts or omitted valid draw. |

## Implementation details

`gl_init`: browser guards omit glShadeModel(GL_SMOOTH) (WebGL shaders already interpolate smoothly) and GL_FOG_HINT/GL_LINE_SMOOTH_HINT calls. Fog enable/configuration and line setup remain. Native calls remain exactly intact.

`readdepth`: browser center clip point `(0,0,1)` is transformed through invmvpmatrix and divided by finite nonzero w. The result is queried from camera1->o with existing intersectgeometry. The actual hit/end is projected through mvpmatrix; finite depth is computed from z/w. An unchanged geometric far endpoint is a real miss, represented exactly as depth 1 so the unchanged editing logic still selects camera-origin behavior on no hit. Other depths are clamped to the valid projected range. Bad matrices/targets fail via existing fatal instead of silently inventing success. Native glReadPixels/depthcorrect code is unchanged. No camera/input/weapon/damage/protocol logic was modified.

`rendercubes`: private browser layout state records world vertex positions/color/UV or shadow position/UV, stride and real vector length. Each strip verifies its actual range, offsets all enabled attributes by original first*stride, then calls real glDrawArrays(original_type,0,original_count). The batch lists still clear exactly after their real draws. The original native multi-draw/nonzero-first macro and paths remain. No vertex bytes are copied/reordered/edited and no count is reduced; unsupported array-size state is a visible error, not a skipped draw.

## SDK mechanism and precise remaining attribution

Read installed `/private/tmp/outbreak-web-sdk/upstream/emscripten/src/lib/libglemu.js`, SHA-256 `5563deb9cae60e2f8f2f463f4d7d31ead65482289309028746c17f388e9418c4` (also pinned in sdk-origin.json):

- glDrawArrays around 3420 prepares count attributes and sets firstVertex=first, lastVertex=first+count for client arrays.
- prepareClientAttributes around 2834/2934 sets interleaved origin/stride and vertexCounter from count.
- flush around 3000 converts GL_QUADS using the global pattern `(0,1,2,0,2,3),(4,5,6,4,6,7),...`, asserts first%4==0, and computes **index byte offset = first*3**.
- Renderer prepare around 2478/2509 allocates/uploads the corresponding first/last vertex byte range.

The engine's `firstindex=verts.length()` and triangle generation do not guarantee quad first%4==0. For concrete first=2,count=4, that SDK index offset selects `[0,2,3,4,5,6]`; highest index 6 is outside lastVertex-exclusive 6. Odd starts additionally produce odd UNSIGNED_SHORT offsets. Rebasing actual attributes to original vertex 2 and drawing first=0 selects `[0,1,2,0,2,3]`, entirely within count 4 and the intended original four vertices. sdk-origin.json records these exact values. This confirms the source incompatibility; it does not identify all 23 individual D022 calls without real draw tracing. If warnings remain after the scoped fix, MAIN/QA should retain them and identify those calls rather than infer they were harmless.

## Helper evidence and limits

`geometry-helper.cpp` uses cube.h's actual types, extracted real matrix determinant/adjoint/invert, real physics cornertest, real weapon triangle/corner/intersectgeometry code, and the current readdepth source. A bounded 64×64 SPACE world includes a SOLID wall at x[26,28),y[24,30), floor0/ceiling12. Tests verify center wall hit at x26 and expected perspective depth, open route/no hit, vertical floor/ceiling queries, orthographic miss with exact depth1, and visible failure for zero/nonfinite inverse/projection w. The first no-hit ideal-coordinate assertion used a too-tight 0.0001-unit tolerance; inspection measured float-inverse far x=52.0003166 versus ideal52 while depth remained exactly1. The fixture now explicitly allows 0.001 unit only for that far-plane coordinate; wall/depth checks retain 0.0001. No source behavior was changed to satisfy it.

`array-helper.cpp` extracts actual browserdrawstrip and uses real vertex plus source shadowvertex layout, with fake GL calls capturing supplied attributes/count/type. Eighteen quad cases span starts0/1/2/3/6/15 and counts4/8/12; every position/UV/color byte maps to its original vertex. Quad triangulation indices stay within original count; triangle/triangle-strip modes/counts are unchanged; shadow uses its real20-byte stride without color calls; world uses24-byte stride. Invalid capacity/negative-first cases fail without a fabricated partial draw.

These are CPU/source/captured-API tests, not an actual renderer, GPU, screenshot, actual-map playtest, collision acceptance or browser input verification. No GL no-op implementation was added to game code.

## Commands and actual object identity

Host: Darwin arm64, Apple clang17.0.0. Target: inspected Emscripten7.0.0/compiler777e6e5db7b4990bcaeb1b9998ed642cc84e6629. From repository root:

```sh
python3 /private/tmp/outbreak-t046-player/check.py
python3 /private/tmp/outbreak-t046-player/make-helpers.py
clang++ -std=gnu++11 -D__EMSCRIPTEN__ -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers -Isource/xcode/Frameworks/SDL2_image.framework/Headers -Fsource/xcode/Frameworks -idirafter source/include /private/tmp/outbreak-t046-player/geometry-helper.cpp -o /private/tmp/outbreak-t046-player/geometry-helper
/private/tmp/outbreak-t046-player/geometry-helper
clang++ -std=gnu++11 -D__EMSCRIPTEN__ -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers -Isource/xcode/Frameworks/SDL2_image.framework/Headers -Fsource/xcode/Frameworks -idirafter source/include /private/tmp/outbreak-t046-player/array-helper.cpp -o /private/tmp/outbreak-t046-player/array-helper
/private/tmp/outbreak-t046-player/array-helper
git diff --check -- source/src/rendergl.cpp source/src/rendercubes.cpp
```

All final checks exit0. Authored entry points were read before execution. `check.py` records all actual complete-TU native/target subprocesses, exact argv/environment and command/tool/source/header/object hashes. Native checks use existing framework includes with -fsyntax-only and optional -D_DEBUG. Actual target checks use pinned em++, existing `--target=wasm32-unknown-emscripten -std=gnu++11 -fsigned-char`, approved SDL2/SDL2_image PNG/zlib/Vorbis flags, release-O2 or debug-O0/-g/-D_DEBUG, source/bot/enet includes, -c and own outputs. EM_FROZEN_CACHE=1; temp/TMPDIR/Node cache remain owned under the task root. No flags/ports/profile/pack changes. Target nm logs verify actual symbol imports.

| Actual whole-TU target object | SHA-256 |
| --- | --- |
| rendergl-release.o | `8a5694969da16224c79497fb6f2fadb9b37e2070c546ea292e331c1d14c76c63` |
| rendergl-debug.o | `b92c846ec408ed954266b7783110640691846286a36b0caf00baf3af756eea46` |
| rendercubes-release.o | `aff869bc7d62b2fa9a58f29024ccd468919f9e5d384130af21b3144cc8f1814a` |
| rendercubes-debug.o | `2883828ec2a75602dde79e9e1bb373c32eb491cae4939d3ed161cee4989948f9` |

## Integration

Source is stable at the hashes above. MAIN can relay them for Engine's unchanged-profile rebuild/link, then pin actual artifacts for QA. No actual browser was launched by this worker. Prior strict D022 failure remains immutable. Zero graphics errors, correct pixels and runtime behavior still require the next actual QA run; no T014/P0/MVP pass or warning reclassification is inferred here. No additional source fix was attempted beyond T046.
