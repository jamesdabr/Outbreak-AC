# Browser foundation measurement observations

Revision:0.1. Status: APPROVED MAIN D087, isolated P0 read-only instrumentation prerequisite. No gameplay/tester action API or runtime authorization.

## Exclusive source change

Only Player under T091 may extend source/src/main.cpp with a browser/network-only publication of a NEW window.OUTBREAK_FOUNDATION_METRICS. Compile guard: __EMSCRIPTEN__ && OUTBREAK_NETWORK_CLIENT && !STANDALONE. Publish alongside existing browserpublish observations, after reading current C++ player/frame/viewport values. Existing OUTBREAK_DIAGNOSTICS/NETWORK_TIMING/model/audio/network snapshots and their schema/version/behavior stay unchanged.

No new input handlers, subscriptions, timers, setters, exported callable action functions, game loop/physics/clock/audio/network/auth changes, game-state writes, extra render calls or local fallback. Native/offline builds preprocess to their prior behavior. The observation must never be used as gameplay authority. A later LLM state/action interface remains separately deferred.

## Exact new snapshot

Property descriptor: writable:false, enumerable:true, configurable:true (engine may republish). Value and nested objects Object.freeze. Exact fields:

- schema_version:1
- profile:"network-client"
- frame_count: current nonnegative native frame.frames integer
- rendered_frame_count: current browserrenderedframes integer
- actor_present: whether player1 exists
- yaw_degrees: current player1 yaw as finite number, or null if absent
- pitch_degrees: current player1 pitch as finite number, or null if absent
- held: object with EXACT keys move,strafe,attack,jump_next,jump_held,crouch_try. move/strafe are signed numeric current player1->move/strafe (normally−1/0/1), remaining booleans from attacking/jumpnext/jumpd/trycrouch. Absent actor yields0/false. Do not infer server-applied actions or claim these are the browser's physical key state.
- wasm_heap_bytes: HEAPU8.buffer.byteLength integer at publication; this is actual committed Wasm memory only, not JS heap/process RSS/peak.
- logical_viewport:{width,height}: current screenw/screenh integers, without changing canvas/GL dimensions.
- document:{focused,visibility,pointer_is_canvas}: actual document.hasFocus(), document.visibilityState and document.pointerLockElement===document.querySelector('#canvas'), observed without spoofing or changing focus/visibility/capture.

Do not clamp/normalize/predict yaw or conceal nonfinite source values. If an invariant is unavailable/nonfinite, fail the instrumented test/report explicitly rather than supply invented values or alter game state. Snapshot frame/native values are taken in one thread at the existing publication boundary; external focus can change between observations, so this is not a cross-process atomicity claim.

## Preparation/source acceptance

Inspect own tests before execution. Tests must validate exact property/field types, freeze/deep-freeze, real source-to-field mapping, absent-actor behavior, negative invalid inputs and unchanged existing snapshot schemas. Use extracted actual EM_JS publisher in an isolated Node fake document/heap fixture; label fixtures, no browser/game/pointer/network/package imports or mutated visibility claims. Native/client and STANDALONE preprocessing comparison must show the delta is absent under native/offline targets. Build one actual network-profile main.cpp Wasm object with unchanged accepted flags/ports/includes and a fresh task-owned frozen cache; record genuine dependencies/hashes/command/tool/exit. No full linking/runtime or original SDK/cache writes.

Fixture startup/input/yaw/held/memory values are not proof of actual input or rendering. A new full candidate and separately authorized ordinary-input browser measurement run must later exercise the snapshot, relative mouse, held release/blur, load/frame/heap/RSS metrics, canvas aspect and gesture audio. Physical pixels/audibility/human acceptance remain separate. This source prerequisite must be terminal before Engine's real source observation/MAIN manifest freeze.
