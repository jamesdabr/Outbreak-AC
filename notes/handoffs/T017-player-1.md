# T017 partial source-adaptation handoff

- Worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T017 revision 0.3 RELEASED; submitted as **PARTIAL**, not accepted
- Phase / contract revisions: P0 0.3 prerequisite subset; BROWSER_FOUNDATION 0.3; GOVERNANCE 0.3; MVP/README 0.3; AGENTS.md. Draft product/parameters/interfaces 0.2 were read as context only.
- Base commit and pre-existing edits: `13f0d8eea4822dee5c976661218d022be74342e3`; pinned dirty tree from `notes/decisions/D003-source-baseline.json`. `main.cpp` initially matched SHA-256 `1fd8c33a834680c96b54bf8529c633f98956a54187742cbe21a6251e43b20556` and had no pre-existing delta. Initial dirty status is saved in `/private/tmp/outbreak-t017-checks/status-before.txt`.
- Changed source: `source/src/main.cpp` only.
- New worker notes: this handoff; `notes/questions/T017-player-shared-embedded-clock.md`; `notes/questions/T017-player-wasm-prerequisite.md`.
- Generated files: task-owned evidence, extraction fixture and compiler artifacts only under `/private/tmp/outbreak-t017-checks/`.
- Commit or patch reference: no commit/branch/push/reset/revert performed. Review `git diff -- source/src/main.cpp`.
- Environment: Darwin arm64, Apple clang 17.0.0 (`clang-1700.0.13.5`), arm64-apple-darwin25.5.0. No browser/graphics/performance claims are made.

## Acceptance evidence

| Criterion | Result | Evidence and limitations |
| --- | --- | --- |
| 1. Native syntax and control flow/order | PASS (syntax/source evidence) | Release and `_DEBUG` `main.cpp` syntax checks exited 0 with empty diagnostics. Extracted old/native-new frame token streams match exactly after removing old static declarations and normalizing persistent member names. Native startup, limiter, loop and shutdown remain. Logs: `native-release.log`, `native-debug.log`, `source-checks.log` in the task temp directory. No native game was linked/launched. |
| 2. Yielding browser callback, persistent state, no native limiter | PASS (source/helper evidence) | Browser startup registers `emscripten_set_main_loop(mainloopframe, 0, true)`; only native frames call `limitfps`. Browser APIs/includes are guarded. `mainframestate` owns FPS smoothing, frame count, scaled-time remainder, authentication-once and debug flush state. Actual Wasm compile is still missing under criterion 5. |
| 3. Lifetime and stop/cancel | PASS (source/helper evidence) | File-static callback/state reference no startup stack variables. Initialization remains outside the frame. `quit` and `cleanup` stop the browser loop before resource cleanup; stop cancels scheduling and unregisters lifecycle handlers. Frame entry and return from input check `browserrunning`. Helper verifies callbacks cannot reactivate play after stop. Actual browser cancellation remains T014 evidence. |
| 4. 250 ms cap, resume reset, release paths | FAIL / PARTIAL | Extracted `browserlocalelapsed` helper tests pass for startup/reset, negative/normal/250/251/long deltas. Focus/visibility/acquisition set reset state; release helper/queue tests pass. **The cap/reset helper is deliberately NOT wired into the runtime clock**, because the unchanged embedded server consumes `lastmillis`. Wiring it would change server-owned deadlines contrary to the frozen clause. See shared-clock question. This criterion is not complete. |
| 5. Actual Wasm main.cpp translation unit | NOT RUN / BLOCKED | Read-only inspected T016 preflight returned `missing_prerequisites` (exit 1): SDK 7.0.0 tools/version/config absent. No accepted ready T016 main.cpp compiler invocation was available. `wasm-preflight.json` records exact flags/paths/errors. No SDK install/acquisition or host-header pseudo-Wasm check was substituted. See Wasm prerequisite question. |
| 6. T014 integration checklist | PASS (checklist supplied); runtime cases NOT RUN | Mandatory actual-game cases are listed below. There is no approved integrated T014 URL/build to consume. Fixture/source results do not exercise the game in Chromium. |
| 7. Protected combat changes preserved | PASS | All eight protected pre-existing combat source hashes match D003 exactly; `protected-hashes.json` and `source-checks.log` record verification. No source outside main.cpp was written by this ticket. No gameplay/balance/protocol/camera/revive additions were made. |

### Reproduction commands

Run from `/Users/jd1/code/apps/outbreak`. Compiler checks parse only and neither launch the game nor write an application profile:

```sh
clang++ -fsyntax-only -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers -Isource/xcode/Frameworks/SDL2_image.framework/Headers -Fsource/xcode/Frameworks -idirafter source/include source/src/main.cpp
clang++ -D_DEBUG -fsyntax-only -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers -Isource/xcode/Frameworks/SDL2_image.framework/Headers -Fsource/xcode/Frameworks -idirafter source/include source/src/main.cpp
python3 /private/tmp/outbreak-t017-checks/verify.py
clang++ -std=c++11 -Wall -Wextra /private/tmp/outbreak-t017-checks/helper.cpp -o /private/tmp/outbreak-t017-checks/helper-plain
/private/tmp/outbreak-t017-checks/helper-plain
PYTHONDONTWRITEBYTECODE=1 python3 web/build/preflight.py --json
git diff --check -- source/src/main.cpp
```

The source verifier exits 0 and extracts the current authored helper functions into `helper.cpp` with explicitly fake SDL/Emscripten/key-binding APIs. The plain helper exits 0. Its single compile warning is the unused browser `inputgrab` delay parameter, retained for the existing native signature. Tests cover startup not capturing; pending/successful/denied/error/unsolicited lock; consumed entry click; Escape/capture loss; blur/focus; hidden/visible; fresh gesture reacquisition; clearing movement/fire/jump/crouch requests and pressed bindings; preserving quit/window events while discarding stale queued inputs; reset/bound arithmetic; and inert stopped callbacks. They are **helper/code checks, not real engine, SDL, Wasm or browser runtime evidence**.

An optional sanitizer attempt used `clang++ -std=c++11 -Wall -Wextra -fsanitize=address,undefined .../helper.cpp -o .../helper`. The sanitized executable did not complete in this environment. The first session was interrupted (exit 130); a second bounded subprocess with `ASAN_OPTIONS=symbolize=0` timed out after 8 seconds and was terminated. `helper-sanitized-run.log` records timeout. No sanitizer pass is claimed; plain-helper results above are separate. No extra dependencies were installed.

## Implementation status

Implemented source adaptation:

- `mainframestate` and `mainloopframe`: persistent common frame body; same native clock/input → world → embedded server → FPS/audio → ray table/render → screenshot → debug flush → download polling → one-time auth ordering.
- Browser-only `inputgrab` behavior prevents capture requests from startup, motion, focus and fullscreen paths. Only the direct left-button canvas DOM handler requests lock, with deferral disabled; rejection is reported and requires another click.
- Browser focus/visibility/pointer-lock handlers use existing key-release dispatch for pressed bindings, then clear direct movement/fire/jump/crouch requests. Stale custom/SDL input queues are discarded while window/quit events survive.
- `checkinput` ignores unlocked gameplay input and repeats of keys not newly pressed; Escape releases capture. SDL loss events also release; browser mouse movement bypasses desktop warp/center-position filtering.
- `browserstart` installs callbacks and `browserstop` cancels/unregisters before cleanup. The integration shell must provide SDL's default `#canvas` target; test that explicitly in T014.

Test doubles: only the temporary helper fixture's browser, SDL queue, player and key-binding APIs. No simulated game result is presented as gameplay.

Incomplete: runtime cap/resume-delta application; actual Wasm TU compilation; all linked-game/browser behavior. Existing embedded server/localconnect, HTTP/download/auth services and startup calls were retained. Their browser viability and service separation need the accepted T020 plan and later integration authorization. New audio activation/suspend handling, storage persistence/IndexedDB sync, browser unload save guarantees and broader startup integration are unimplemented. Existing native shutdown writes were not redesigned; no new persistence guarantee is claimed.

## T014 mandatory integrated-game checklist

All items are **NOT RUN** here and mandatory for the later integrated game:

- Record actual Chromium version/path, macOS version, build/toolchain identity and real game URL. Render/control an actual map; fixture HTML is insufficient.
- Click the real SDL `#canvas`: acquire pointer lock, enter play, and verify the acquisition click does not fire. Keyboard/mouse input must work after fresh input.
- Escape: unlock and clear held movement/fire/jump; passive focus/motion must not reacquire. Click again to reenter; test browser-denied requests and visible diagnostics.
- While holding movement/fire/jump, blur the window and hide the tab separately. On return, held inputs remain released until fresh input following a user-initiated return to play; stale repeats/queued clicks must not reactivate them.
- After lead resolution of the shared-clock question, verify the actual client delta cap/reset after long stalls and focus/visibility resume while independently verifying server-owned deadlines.
- Observe continuous yielding frame scheduling, HUD/render/audio/service behavior, console/runtime errors and window/canvas resize. Confirm native-frame limiting does not block the browser.
- Trigger clean game shutdown/cancellation; verify no subsequent frame/input callback accesses destroyed engine/SDL resources. Do not infer native-save guarantees from closing/unloading the tab.
- Separately demonstrate standalone-server multiplayer under its released contract; retained offline local simulation is not that evidence.

## Integration and questions

Open: `T017-player-shared-embedded-clock.md` and `T017-player-wasm-prerequisite.md`. Only affected clock integration/Wasm steps are paused; independent authorized source and native/helper work is submitted. No authoritative ticket state was changed and no waiver is requested by this handoff.

The ticket and governing revision markers were re-read before submission and remain 0.3. Revision/source hashes are saved in `submission-hashes.json`; the full relevant reread snapshot is `contracts-before-submission.txt`. Other workers' files and generated outputs may change concurrently; they were neither edited nor claimed by this worker. The lead must review this as partial, not accept T017 as complete or infer T014/P0 readiness.

API reference used for source adaptation: [Emscripten main-loop API](https://emscripten.org/docs/api_reference/emscripten.h.html#c.emscripten_set_main_loop) and [Emscripten browser event API](https://emscripten.org/docs/api_reference/html5.h.html). These currently describe development documentation; they do not replace compilation against the pinned 7.0.0 SDK.
