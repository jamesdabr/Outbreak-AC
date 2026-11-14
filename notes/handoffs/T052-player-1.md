# T052 browser original audio proof handoff

- Worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T052 revision 2.5; unchanged RELEASED on final inspection. Submission evidence only; MAIN owns acceptance/status.
- Phase / contract revisions: browser foundation/GOVERNANCE/P0 0.5; D033 prerequisite 2.5; continuation clarified by D038. Gameplay remains draft.
- Base commit and pre-existing edits: 13f0d8eea4822dee5c976661218d022be74342e3 plus shared uncommitted accepted prerequisite/prototype edits. Task-start status and source copies are preserved under web/runtime/tests/T052-player-1/. No reset, revert, commit, branch, push or worker dispatch.
- Changed source files: source/src/main.cpp; source/src/audiomanager.cpp; source/src/sound.h. Only browser non-STANDALONE audio hooks/helpers/configuration/omission text changed. New task fixtures/results under web/runtime/tests/T052-player-1/ and own notes only.
- Patch reference: main.cpp.patch, audiomanager.cpp.patch, sound.h.patch in the evidence directory are deltas against preserved pre-T052 source, not Git HEAD.

## Acceptance evidence

Evidence directory: `web/runtime/tests/T052-player-1/`. Commands below run from repository root. This is source/object/helper evidence, not a browser/audio acceptance claim.

| Criterion | Result and evidence |
| --- | --- |
| Inspect genuine SDK OpenAL initialization/resume/cleanup | PASS inspection: installed SDK creates an actual AudioContext in alcCreateContext, registers autoResume gesture listeners, stores it at AL.contexts[handle].audioCtx. alcSuspendContext/alcProcessContext are no-ops; alcDestroyContext deletes registry/timer but does not close AudioContext. This implementation resumes/suspends that actual context and defers its close until native engine teardown has released nodes. SDK source hashes in final-evidence.json pin this internal SDK dependency. No second AudioContext/oscillator is created by proof helpers. |
| Genuine backend and original sample/source path | PASS source inspection and compilation: gesture invokes existing initsound(), sbuffer::load(false) with extensionless outbreak/proof_tone, and real source configuration/play/query. Existing loader resolves packages/audio/outbreak/proof_tone.wav via SDL WAV decoding and alBufferData. Dedicated proof handles never register a game/map sound ID. Original WAV hash/format verified read-only in final-evidence.json: PCM16 mono 22050 Hz, 6615 frames, 300ms. Actual decoding/playback in browser NOT RUN. |
| No pregesture/autoplay cue; one nonlooping cue per valid capture-entry | PASS source plus extracted input/backend helpers. Startup enables audio1/soundvol96/musicvol0 after browser.cfg and publishes an uninitialized snapshot without allocating a backend. Audio initialization/play runs synchronously before pointer-lock request. Entry is consumed; locked/pending/hidden/unfocused/nonprimary inputs do not play; per-frame polling never starts playback. Looping false, source relative, position zero, gain/pitch one. |
| Failures visible and later-gesture retry; ownership/no duplicate resources | PASS isolated extracted C++ helper tests: init, missing sample, source creation, play, query, non-PLAYING result, gain, context failure; later-gesture retry; same successful backend reused; failed source deletion retains ownership rather than allocating another source/buffer; repeated errors do not retry/log every frame. JS tests cover actual observed async/sync resume/suspend failures and recovery. These are test doubles, not actual backend failure injection. |
| Loss/stop/shutdown release and idempotence | PASS source and helpers: focus/visibility/pointer-loss path stops/releases proof handles and suspends actual SDK context; explicit browser stop releases proof handles, calls existing engine soundcleanup, resets its stale member fields/nosound, and closes actual AudioContext after teardown. Repeated startup loss/shutdown, natural cue completion and failed-delete shutdown tested with doubles. SDK close rejection is surfaced and persists across stopped snapshots; stale close failure cannot overwrite a later gesture. Real browser shutdown NOT RUN. |
| Separate frozen truthful diagnostics | PASS extracted EM_JS tests: exact required schema_version1/phase/gesture_count/sample_loaded/play_count/openal_source_state/error fields; frozen snapshot, nonwritable property; actual OpenAL queried state or null; error strings from helper/backend outcomes, including async failures. Epoch/registry identity isolates stale Promise rejections. No exported action/state injection API or unbounded history. OUTBREAK_DIAGNOSTICS code/schema unchanged. No AudioContext-running or physical audibility inference. |
| Narrow source delta/native preservation | PASS `python3 web/runtime/tests/T052-player-1/check.py` and `final-evidence.py`: unifdef -U__EMSCRIPTEN__ native token equivalence for all three source files; entire existing audiomanager prefix/suffix preserved outside appended browser block; owned-source git diff --check passes. All eight D003 protected prototype files match baseline hashes; task-start rendergl/rendercubes/editing/vertmodel/rendertext/worldio/governing files still match. |
| Native release/debug checks and real Wasm objects | PASS eight whole-translation-unit checks: main.cpp and audiomanager.cpp native syntax release/debug plus actual Wasm release/debug compilation, same accepted current-profile flags/ports and frozen cache. Four real version-1 Wasm objects and exact hashes below. Every invocation records all source/header input hashes before/after, stable. Exact argv/environment/tool hashes in result.json; individual logs in evidence directory. |
| Full rebuild, integrated browser audio, human audibility | NOT RUN by scope. No browser/server/game launch, integration/shared build mutation, actual AudioContext/AL sample execution or physical audibility observation. No MVP/P1 or gameplay acceptance claim. |

Environment: Darwin 25.5.0 arm64, Apple clang 17.0.0 (clang-1700.0.13.5); installed Emscripten SDK 7.0.0 under /private/tmp/outbreak-web-sdk, compiler revision 777e6e5db7b4990bcaeb1b9998ed642cc84e6629; Node v24.13.0 for isolated JS tests. No performance claim or new dependency/SDK download/flag is introduced. Approved ports/cache reused frozen, temp/object outputs task-local.

Reproduce the scoped evidence:

```sh
python3 web/runtime/tests/T052-player-1/check.py
python3 web/runtime/tests/T052-player-1/helpers.py
node web/runtime/tests/T052-player-1/js-helpers.cjs
python3 web/runtime/tests/T052-player-1/final-evidence.py
```

check.py performs native preprocessing/token checks, full native syntax checks and actual Wasm object compilation; it does not link/run the engine. helpers.py extracts current C++ audio/input helpers and compiles/runs them against fake interfaces. js-helpers.cjs executes the actual extracted EM_JS bodies in a fake AL registry/AudioContext sandbox; it creates no audio/browser. Per-test commands/results are stored in result.json, helper-result.json, js-helper-result.json and logs. proof-block.txt is an early authoring snapshot; the extracted-* fixtures and final source hashes describe tested current code.

Final source SHA-256:

- `source/src/main.cpp`: `52e77d11e586bbe9736455fa791ce018e54712de0b437e836f00e2a8bb7ea143`
- `source/src/audiomanager.cpp`: `d8396e5ce2c381a90e7b59cd1606f0c0c176c247a13ec7e085804ff3e4de9a45`
- `source/src/sound.h`: `80f635fd48b40ec61524d52707ba7c6f80eb2ad2d8bead137099bdf462c11655`

Actual Wasm object SHA-256:

- `audiomanager-debug.o`: `37218733bff0ce1acfe49e9e465226c406251f42e0c7c3568c241a7b3262e5d1`
- `audiomanager-release.o`: `d827829b5356b38fd71e9ba8fb28779eff8739304ad705a7d275c87aa9871964`
- `main-debug.o`: `80b5124d36f15857e500a7f498e4a66d35f1d9dcdbc0d3541d87a3473ca688b4`
- `main-release.o`: `bacc81db9316016e04d05d86dfc6ff159efab15e11b77130fea56365a6a1f651`

## Implementation status

Implemented: real engine backend/sample/source proof path, gesture/loss/shutdown wiring, backend resource ownership and separate audio diagnostics as described above. The nonlooping original tone is a prerequisite proof cue, never an inherited gameplay sound. The omission message now accurately states gameplay sound mapping is absent and cue initialization waits for canvas gesture.

Simulated verification: C++ backend/resource/input controls and JS AudioContext/AL registry tests deliberately use fakes around extracted current production helper bodies. They verify control flow, state/error reporting and ownership, not device behavior or physical sound. Full actual CPP compilation validates interfaces against engine and SDK headers.

Incomplete: integrated link/rebuild, real browser WAV load/play, actual source-state/AudioContext observations, loss/reentry behavior under a real browser, and physical audibility. Those require MAIN acceptance and a separate integration release. No stock/default sound mappings or gameplay behavior are added. Existing D034 pointer-lock Promise rejection remains unchanged and outside this ticket.

## Integration and questions

Browser-only audiomanager layout and three public methods change under __EMSCRIPTEN__ && !STANDALONE. Integration must rebuild all affected header consumers, retain existing OpenAL link support, include the genuine original proof WAV and browser audio configuration (World's separate T053 profile), and exercise the existing normal primary canvas gesture. The $AL dependency is declared through inspected SDK EM_JS_DEPS; use the pinned SDK. Full linking is deliberately unclaimed until integrated.

Observe OUTBREAK_AUDIO_DIAGNOSTICS before any gesture (uninitialized, zero counts/no sample/source state), then a valid canvas entry gesture (backend and sample outcome/error), completion, focus/visibility/pointer loss, reentry and shutdown. Missing sample/backend/play and rejected resume/suspend/close should remain visible and retried only through later authorized gesture. Counts/AL_PLAYING must never be reported as proof of physical audibility. No console-error filtering or pointer-lock rejection suppression was added.

Historical hold-status ambiguity in notes/questions/T052-player-hold-status.md was resolved by MAIN's D038 explicit continuation; no new human hold arrived during this continuation. No unresolved T052 scope question remains. Other tickets, build assets and contracts are preserved. MAIN reviews acceptance and authorizes any integration.
