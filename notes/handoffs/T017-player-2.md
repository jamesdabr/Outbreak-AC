# T017 revision 0.4 clock follow-up — partial pending Wasm

- Worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T017 0.4 RELEASED; submission remains **PARTIAL**, not accepted
- Phase / contract revisions: P0 0.4 prerequisite subset; BROWSER_FOUNDATION 0.4; GOVERNANCE 0.4; MVP/README 0.4; AGENTS.md; D004. Draft gameplay contracts remain context only.
- Base commit and pre-existing edits: `13f0d8eea4822dee5c976661218d022be74342e3` plus D004's pinned dirty source. Before editing, main.cpp matched D004 SHA-256 `79b1e415a58c9c25bb5fc46f38ea19911905f424ce29d8bd7d596828943c3075` exactly. Continued from the existing T017 source without resetting. Initial status is `/private/tmp/outbreak-t017-r04/status-before.txt`.
- Changed source: `source/src/main.cpp` only, inside `mainloopframe`.
- New notes: this handoff and `notes/questions/T017-player-r04-wasm-not-ready.md`. Earlier handoffs/questions were not edited.
- Generated evidence: `/private/tmp/outbreak-t017-r04/`; its lifecycle fixture reuses read-only helper stubs/tests from `/private/tmp/outbreak-t017-checks/`.
- Patch: `/private/tmp/outbreak-t017-r04/revision-04.patch` is the exact delta from D004. Final main.cpp SHA-256: `8f63349ad9a84d199c483f26aacb0b929f1441e3a479da642358a8916fb173f7`.
- No commit, branch, push, reset/revert, service launch, dependency install or external SDK execution.

## Acceptance evidence

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1. Native syntax and ordering | PASS — source/syntax only | Release and `_DEBUG` main.cpp syntax checks exit 0, no diagnostics (`native-release.log`, `native-debug.log`). Native frame tokens match the D004 version after removing the new identity alias and normalizing its reads; no native timing/order change. `source-checks.log` records this. |
| 2. Yielding guarded callback and persistent state | PASS — source/helper only | Existing guarded `emscripten_set_main_loop(mainloopframe, 0, true)` and file-static `mainframestate` remain; native-only limiter remains guarded. No new scheduling or repeated initialization. |
| 3. Callback lifetime and cancellation | PASS — source/helper only | Callback/state reference globals, not main's expired stack. Existing stop-before-cleanup and unregistration remain. The extracted current frame invoked after `browserstop()` performs no calls or clock updates. Lifecycle fixture also confirms stopped handlers cannot reactivate play. |
| 4. Wired 250 ms bound, reset, input release | PASS — extracted actual frame/helper code | Current `mainloopframe` now invokes `browserlocalelapsed(elapsed)` and uses its result for gameplay `curtime`/scaledtime. Fixture checks reset-to-zero, 16/250/251/5000 ms deltas, focus/visibility resume, gamespeed/remainder, pause, wall diagnostics, ordering and once-only auth. Lifecycle release/reacquisition fixture also passes. These are fake-platform/engine helper checks, not game/browser execution. |
| 5. Actual main.cpp Wasm TU | NOT RUN / BLOCKED | Read-only SDK preflight exit 1: pinned Emscripten 7.0.0 tools/version/config remain absent. `wasm-preflight.json` records errors. No reviewed ready SDK/compiler invocation was supplied; no compiler, installer or port acquisition executed. New question: `T017-player-r04-wasm-not-ready.md`. |
| 6. T014 checklist | PASS — supplied; all actual-game checks NOT RUN | Checklist below remains mandatory for integrated-game acceptance. No fixture is presented as a real game or network pass. |
| 7. Existing combat preserved | PASS | All eight D003-protected combat hashes match exactly (`protected-hashes.json`, `source-checks.log`). This worker changed main.cpp only, with no balance/protocol/camera/revive additions and no server.cpp edits. T025 owns server.cpp independently. |

## Implementation status

Implemented: `gameplayelapsed` starts as the raw frame delta; only the browser branch replaces it with the reset/capped helper result. Gameplay uses this value before the existing local gamespeed multiplier. Raw `elapsed` continues to feed FPS, entropy and render elapsed diagnostics; raw `millis` continues to update `totalmillis` and debug-flush timing. Native builds retain the same delta values and behavior.

Under D004, the retained **offline** embedded simulation deliberately follows bounded `lastmillis`, as the unchanged server slice already does. This resolves the historical shared-clock question for OFFLINE_MAP only. Native/separate-server clock source is untouched. No future network-browser timing policy or standalone authority claim is added. Existing demo seeking and gamespeed mechanisms are preserved; the tests target the approved offline map path with `watchingdemo=false`.

The prior persistent callback/input lifecycle adaptation remains. Test doubles exist only in temporary fixtures: fake SDL/Emscripten, player/key bindings and subsystem calls. The frame fixture extracts the current real `mainframestate`/`mainloopframe` and lifecycle functions, then substitutes subsystem APIs; its fake server records the clock presented to the retained slice. It does not run real server simulation.

Incomplete: actual Wasm compilation, linking and real browser map/input/audio/storage/runtime evidence. New audio activation/suspend and storage persistence/IndexedDB behavior remain unimplemented, as in the prior handoff; closing/unloading a browser has no new save guarantee. Other startup/native service separation remains separate work. No full browser readiness, multiplayer or P0 acceptance is asserted.

## Reproduction and results

Environment: Darwin arm64, Apple clang 17.0.0 (`clang-1700.0.13.5`). From `/Users/jd1/code/apps/outbreak`:

```sh
clang++ -fsyntax-only -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers -Isource/xcode/Frameworks/SDL2_image.framework/Headers -Fsource/xcode/Frameworks -idirafter source/include source/src/main.cpp
clang++ -D_DEBUG -fsyntax-only -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers -Isource/xcode/Frameworks/SDL2_image.framework/Headers -Fsource/xcode/Frameworks -idirafter source/include source/src/main.cpp
python3 /private/tmp/outbreak-t017-r04/verify.py
clang++ -std=c++11 -D__EMSCRIPTEN__ -Wall -Wextra /private/tmp/outbreak-t017-r04/frame-helper.cpp -o /private/tmp/outbreak-t017-r04/frame-helper
/private/tmp/outbreak-t017-r04/frame-helper
clang++ -std=c++11 -Wall -Wextra /private/tmp/outbreak-t017-r04/lifecycle-helper.cpp -o /private/tmp/outbreak-t017-r04/lifecycle-helper
/private/tmp/outbreak-t017-r04/lifecycle-helper
PYTHONDONTWRITEBYTECODE=1 python3 web/build/preflight.py --json
git diff --check -- source/src/main.cpp
```

Syntax, verifier, fixture compilation/execution and whitespace check exit 0. Helper compiles each have one existing unused-parameter warning for browser `inputgrab`'s native-compatible `delay` parameter. Logs: `source-checks.log`, `frame-compile.log`, `frame-helper-run.log`, `lifecycle-compile.log`, `lifecycle-helper-run.log`, `native-release.log`, `native-debug.log`. SDK preflight alone exits 1 (`missing_prerequisites`). Defining `__EMSCRIPTEN__` for the host fixture selects extracted source branches against fake APIs; it is explicitly **not** a Wasm translation-unit check.

The actual wired-frame fixture proves, within those doubles: initial 9000 ms wall advance yields 0 gameplay advance; a later 5000 ms wall advance yields 250 gameplay ms; raw wall totals/FPS/entropy/render deltas still advance by full amounts; focus and visibility return reset gameplay to zero; 150% gamespeed yields 375 ms from a 250 ms capped input; fractional scaling and pause remain; auth runs once; frame call order is unchanged; cancellation prevents further work.

## T014 mandatory integrated-game checklist

Every runtime item below is **NOT RUN** in T017:

- Record real Chromium executable/version, macOS/build/toolchain identity and actual game URL; render/control the real map.
- Acquire pointer lock through a canvas click and verify the entry click does not fire; test denied capture diagnostics.
- Escape unlocks and clears held movement/fire/jump; passive focus/motion cannot recapture; another click reacquires with fresh input.
- Blur and tab hide while holding controls; on resume no stale movement/fire/jump repeats or clicks restart play. Verify the wired delta reset/cap in the real offline embedded simulation and preserve raw wall diagnostics.
- Observe continuous yielding frames, resize and real render/audio/service behavior; inspect console/runtime failures and ensure no blocking native limiter runs.
- Quit/cancel cleanly and verify no later frame/input callback accesses cleaned resources; do not infer unload-save guarantees.
- Standalone multiplayer requires its own released timing/transport/server proof. This bounded offline simulation is not standalone multiplayer evidence.

## Integration and questions

D004 resolves the historical embedded-clock contradiction for this offline experiment. The remaining SDK dependency is recorded in the new revision-0.4 question and routed through D004/T022. Actual Wasm must still pass before full T017 acceptance. Ticket/contracts were re-read before submission; their SHA-256 values still match the start snapshot (`contracts-start.json`), with revision 0.4 unchanged. No authoritative status was changed by this worker.
