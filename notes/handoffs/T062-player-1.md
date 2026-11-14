# T062 network main source handoff

- Worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket: T062 revision3.5, unchanged RELEASED on final inspection. MAIN owns acceptance/status.
- Governing: NETWORK_MAIN0.1/D049 prerequisite3.5, platform0.2, browser foundation/GOVERNANCE/P0 0.5. Client0.2/D048 was the starting interface; MAIN's later D051 coordination explicitly updates read-only client context to0.3/revision2 network map. No main API/path/revision constant or source changed for that context update. Actual T061 implementation remains separately owned/pending acceptance.
- Base: 13f0d8eea4822dee5c976661218d022be74342e3 plus shared accepted prerequisite/prototype edits. Exact main11e1240cfa445472eaf02e68a1742f46919d7d9f3d77e9f334486ab7c04cca1b before copy and initial pins in web/runtime/tests/T062-player-1/.
- Changed source: source/src/main.cpp only explicit __EMSCRIPTEN__ && OUTBREAK_NETWORK_CLIENT && !STANDALONE bootstrap/frame/timing/emitter/shutdown branches. New task-local evidence and this handoff only. Audio, headers, client/parser/backend/server/gateway/SDK/build/out/assets and prior notes/evidence were not edited. No commit/push/reset/revert/branch/dispatch.
- Patch: web/runtime/tests/T062-player-1/main.cpp.patch against accepted T059 main. Final source was frozen before handoff; subsequent findings require a new question, not source mutation.

## Acceptance evidence

Fresh evidence directory: `web/runtime/tests/T062-player-1/`. SOURCE/OBJECT/EXTRACTED-HELPER evidence only.

| Criterion | Result and evidence |
| --- | --- |
| Native/OFFLINE preserved | PASS check.py/final-evidence.py: native and OFFLINE unifdef token sequences exactly equal before. Actual native release/debug syntax and OFFLINE release/debug Wasm pass. Original OFFLINE250ms/reset clock, native/local path, diagnostic/input/pointer/audio semantics remain. |
| Remote bootstrap before map | PASS extracted actual browsermain with external fakes: genuine normal client/DM/nextmode setup then cn=-1/CS_SPECTATE/default role before empty_world/load_world. Existing original scene assets/SDL/GL/font/map/error paths reused. No connected/life/alive/join assignment. browsernet_begin exactly once after browserstart/scene, before yielding frame schedule. Loader/asset failures remain real fatal paths, no invented success/fallback. |
| No local server/bootstrap/failure path | PASS complete preprocessed NETWORK main source audit: no executable initserver, serverslice, localconnect, localdisconnect, cleanupserver or connectserv call sites. Network int main contains only return browsermain(); native tail is actually preprocessor-excluded. Mock local calls assert if reached, never reached in bootstrap/frame/cleanup checks. Not reported as a fabricated runtime zero counter. |
| Lifecycle/frame/control at lastmillis0 | PASS actual extracted mainloopframe. Raw totalmillis advances before browsernet_frame(frame.frames), once per new main frame and before game/action handling. Opening/joining prediction0 still calls updateworld at lastmillis0 for actual client control/parsers. CLOSING/FAILED still poll/control while prediction remains0. Actual client admission/control/simulation gate is T061-owned and modeled in these tests, not accepted or executed as real network here. |
| ACTIVE-only unscaled prediction | PASS: min(nonnegative raw elapsed,50) only BN_ACTIVE and not server ispaused; lastmillis advances that prediction only. Tests cover long/small/negative-tick-clamped0 raw deltas, server pause, prejoin/terminal states and gamespeed999/client-paused/demo-skip settings that cannot scale network time. Existing raw/frame/FPS/render clocks preserved. |
| Real gesture/no fake spawn | PASS source/profile inspection: unchanged T059 normal gesture/real capture event/request-specific denial/loss/audio path reused. Existing getclientnum/tryrespawn remains ordinary client request; T061/D048 handles native initial eligibility/rate limit/SPAWNSTATE. Main never calls game_observed or fabricates join/life/ACTIVE. |
| Safe stop/parser deferral | PASS extracted actual stop/cleanup/order. First stop after begin latches browsernet_close(BNE_CLOSED), schedules one emscripten_async_call(...,NULL,0), then original audio/pointer/loop cancellation. Static callback pumps next unused main frame id after stack unwind; never nested parser pumping, blocking2s drain or extra retries. Repeated stop/cleanup schedules once. No invented pump/session for failure before begin. No private client state or new public API. Current T061 cleanupclient latches close without destroying nested parser packet; actual integration remains separate. |
| SDK scheduler inspection | PASS source inspection: pinned libeventloop.js async_call0 uses safeSetTimeout, runtime keepalive and callUserCallback after yielding. Existing runtime API/internal static callback only; no exported game callback/action interface or new flags. Final callback scheduling is not proof it runs on hard page teardown; supervisor owns final physical cleanup. SDK hashes recorded. |
| Engine diagnostics preserved/labeled | PASS diagnostics.cjs: OFFLINE emitter byte-identical to before; NETWORK differs only profile:'network-client', same schema1/fields/frozen nested data/global real error/unhandledrejection behavior. Render-running means expected scene rendered, not native join. Tested running engine while timing JOINING/prediction0. No global filter. |
| Frozen network timing | PASS actual extracted JS/fake window: schema1/raw_elapsed_ms/prediction_elapsed_ms/frame_id/actual BN lifecycle_state/embedded_server_path_compiled:false; immutable nonwritable snapshot replacement/no game refs/action API. False is the approved compile-profile source fact, not a runtime call count. No T061 outbreakNetworkSnapshot replacement. |
| Real native/profile objects and current inputs | PASS six whole-TU invocations: native release/debug syntax; four actual OFFLINE/NETWORK release/debug version-1 Wasm objects. Same approved tools/ports/flags plus already-approved network macro; frozen cache/task-local output. Every command records complete source/header membership/hashes before/after (stable), argv/environment/tool hashes/log/object hash. No stubs/error bypass/full link. |
| Final source/readonly identity | PASS final-evidence/source-freeze: exact actual preprocessing input equals current source, helpers/diagnostics/results match source, audio/header/API/ticket/main contract pins unchanged. Client contract doc changed by MAIN D051 only; old/new hashes and authority in D051-context-update.json, previous evidence freeze preserved as pre-D051-* (same compiled source/object identities). |
| Full link/game/browser/network/audio/performance/P0/MVP | NOT RUN. No browser/game/server/network launch, native peer/game handshake/spawn/movement, packed artifact/shared build mutation or physical audibility proof. Requires separately accepted full source/data pins and integration release. |

Reproduce scoped component evidence from repository root:

```sh
python3 web/runtime/tests/T062-player-1/check.py
python3 web/runtime/tests/T062-player-1/helpers.py
node web/runtime/tests/T062-player-1/diagnostics.cjs
python3 web/runtime/tests/T062-player-1/final-evidence.py
```

- result.json / per-check logs: exact native/profile Wasm commands, full stable input hashes, tool/environment/object identities; before/current preprocessed profile text and native/OFFLINE normalized token hashes.
- helper-result.json / extracted-main.cpp / helper logs: actual current preprocessed bootstrap/frame/stop/cleanup/helper/frame-state bodies, fake external engine/client/SDL/scheduler calls. Tests cover bootstrap/load errors, zero-time control,50ms clock, terminal states, no local calls and once-only safe final pump outside fake parser stack.
- diagnostics-result.json / extracted emitter files / log: actual JS in fake window, prior/offline exact preservation, network label and real-error behavior, frozen timing/render-vs-join distinction.
- final-evidence.json / source-freeze.json: all current identities, six stable real compiler checks, readonly pins/approved context update, SDK scheduler hashes and whitespace check.
- D051-context-update.json / client-contract-0.3-reading.txt / pre-D051-* preserve approved external context change without relabeling stale docs or recompiling unchanged code. Initial source/object freeze and final freeze have identical main/object hashes. Current future game map revision2/package is T064/T061-owned, pending data acceptance; OFFLINE/audio/T063 originalrev1 unaffected.

Environment: macOS26.5.1/Darwin25.5.0 arm64, Apple clang17.0.0 (clang-1700.0.13.5), Node v24.13.0. Reused installed Emscripten7.0.0 compiler777e6e5db7b4990bcaeb1b9998ed642cc84e6629 at /private/tmp/outbreak-web-sdk, accepted ports and frozen cache. No dependency/download/SDK patch/new compatibility or link flags. No performance claim.

Final frozen source SHA-256:

- `source/src/main.cpp`: `c1a5cff4b11569bd19bc6f0b7fac713ad0b64f9c573c9a80d1c84e35b5f3f681`

Actual Wasm object SHA-256:

- `main-network-debug.o`: `2e8dd6cc925fe8e0b66eb6bd7b2fd27e241c260d191f7606d072fdf0fc18baa3`
- `main-network-release.o`: `9fe866556b9bf02e2dcb63f31578517365a26fa2a13c54c85bd058047365788f`
- `main-offline-debug.o`: `b631f26cbb884f81fcd3707edc27abd5aae91c074cc3c03e48afecfa2da4fedd`
- `main-offline-release.o`: `cfc2af265c51550aa5223f2f4c2d79df8133bdfdfbfd2b29cd654fb5300e4c1d`

Preserved audio/interface source SHA-256:

- `source/src/audiomanager.cpp`: `31ea6bc32aeaaf3264795ba7de91f4a9614883fdbab8e93a165864477f2d1039`
- `source/src/sound.h`: `80f635fd48b40ec61524d52707ba7c6f80eb2ad2d8bead137099bdf462c11655`
- `source/src/browsernet.h`: `0a7f522f26d6a29c1956e15a69d601e481790d69091071622f9db73c759e6b44`
- `source/src/browsernet_observer.h`: `7c88755861fec0cf5523e9005ee02755cd8a001b49a4be32da73042a5bfd987c`

## Implementation status

Implemented only in explicit NETWORK profile: remote-only scene/bootstrap, public lifecycle polling with prejoin zero-time control, ACTIVE-only bounded prediction, separate render/timing labels, terminal close and one yielded safe pump. Native/OFFLINE token behavior preserved.

Simulated: external engine/SDL/client state/control/admission, fake parser/scheduler and fake diagnostic window in extracted tests. Actual production main.cpp compiles against actual engine/SDK headers into genuine profile objects; no linked/running game or native handshake proof. T061 runtime semantics remain its owner's separate evidence.

Incomplete until separate integration: full client link, genuine WebSocket/ENet/game join/SPAWNSTATE/remote receipts/movement/close, real headed pointer recovery/audio/layout/performance/P0/MVP. No local fallback or fake living player supplied.

## Integration and questions

Main consumes existing browsernet_begin/frame/state/close only, no header/private-state/API extension. T061 owns frame budgeting/dedup, JOINING control/spawn eligibility, actual map0.3/revision2 validation, parser milestones/ACTIVE/error admission and safe deferred host/logger/actor cleanup. Its public contract can be consumed for source composition but not declared accepted by this handoff.

Future combined integration must use accepted platform implementation in place of unix.c only for network recipe, accepted T061/current main, accepted T064 network79file pack and supervisor boot/context ownership; old OFFLINE/audio/T063 artifact profiles remain separate. No pack/source/build edits or launch were performed here. Exact map path remains dev_outbreak_browser with no main revision constant/validation bypass.

Observe raw totalmillis advancing with prejoin lastmillis0/control progress, real native milestones before ACTIVE,50ms max prediction only ACTIVE, true server pause/failure, and no embedded-server path. Network timing lifecycle is the actual state at prediction choice; later parser transition may update T061 snapshot that frame. Engine running alone cannot prove join. embedded_server_path_compiled:false is a labeled profile fact.

Shutdown latches terminal BNE_CLOSED then yields one safe final lifecycle pump, no parser-active destruction or synchronous drain. Actual callback delivery and physical close under hard page teardown remain unproven; final supervisor context cleanup remains required.

No unresolved scope question/new human hold. MAIN reviews frozen exact source/component evidence and owns acceptance/integration. Source is frozen before handoff and unchanged afterward; later findings require a new question.
