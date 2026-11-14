# T059 pointer denial and audio cleanup handoff

- Worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T059 revision 3.1; RELEASED and unchanged on final inspection. Evidence submitted for MAIN review; no worker status amendment.
- Phase / contract revisions: browser foundation/GOVERNANCE/P0 0.5 plus D040 prerequisite2.9 and D042 prerequisite3.1.
- Base commit / pre-existing edits: 13f0d8eea4822dee5c976661218d022be74342e3 plus shared accepted prerequisite/prototype source. T059 began from main52e77..., audioa874... (D042's unverified cleanup correction), sound.h80f635.... Before copies/start-hashes.json preserve exact baselines. No reset, revert, commit, push, branch, worker dispatch or shared build/out mutation.
- Changed source: source/src/main.cpp browser pointer-request/denial/poll/lifecycle hooks only; source/src/audiomanager.cpp browser proof cleanup ownership and observed audio context diagnostic only. sound.h is unchanged/read-only. New evidence in web/runtime/tests/T059-player-1/ and this own new handoff only.
- Source freeze: web/runtime/tests/T059-player-1/source-freeze.json created after final source review and all matching checks, before this handoff. No further implementation is performed after this submission. A later finding requires a new question.

## Acceptance evidence

Fresh evidence directory: `web/runtime/tests/T059-player-1/`. Every source/object/helper claim below refers to its final source-freeze.json hashes, not to historical T052 reports.

| Criterion | Result and evidence |
| --- | --- |
| Preserve mixed/stale T052 evidence before new writes | PASS. Full current T052-player-1 tree copied before implementation into historical-mixed-T052/, with exact 51-file membership/hashes in historical-mixed-T052-manifest.json. Final inspection proves both snapshot and original tree still match; no T052 paths were overwritten. Snapshot is explicitly historical/mixed/stale and is not proof of current source. Original T052 handoff and conflict note remain untouched; D042 resolves their mismatch. |
| Own the actual normal-gesture request Promise | PASS source/extracted-helper evidence. Replaced the SDK wrapper that discards the return value with a direct call to the existing #canvas.requestPointerLock method in the same valid primary gesture, after existing real audio initialization. No deferred/forced capture or new request timer/retry. Built-in stringToUTF8 dependency declared via EM_JS_DEPS; no new external library, SDK patch, compiler/link flag or exported game action/C callback. Installed tools/emscripten.py inspection confirms EM_JS emits the named helper function used to hold its private request state. Full generated JS/link remains NOT RUN. |
| Expected denials only, genuine reason/retry, unknown errors visible | PASS pointer-js.cjs: all six actual DOMException names (WrongDocumentError, NotAllowedError, NotSupportedError, InvalidStateError, SecurityError, AbortError), both synchronous and rejected Promise forms. Actual concise name/message is recorded privately and copied only during main-thread polling. Unknown Error/TypeError/unlisted DOMException/spoofed name/string exceptions are rethrown. Six unknown async rejections, including after stop, reached a real Node unhandledRejection observer in the isolated test. Production global error/unhandledrejection observer and full OUTBREAK_DIAGNOSTICS emitter are byte-for-byte unchanged; no global filter/preventDefault/classifier exemption. Node test observer exists only in fixture. Actual headed WrongDocumentError recovery NOT RUN. |
| Modern/legacy/missing API; only real event grants input | PASS. Modern Promise resolution does not mark capture; only the existing valid pointerlockchange event sets browserlocked/inputgrab. Legacy void-return request is supported. Missing canvas/API gives visible retryable failure. Tests exercise method receiver, one synchronous request, legacy event failure and no auto retry. |
| Genuine pointerlockerror and Promise ordering | PASS. For an owned modern Promise the actual error event records a failure hint, consumed before frame input: normally its Promise microtask supplies the precise reason; an event-only browser still falls back to its actual event. Legacy error immediately uses loss handling. Rejection-first/event-first/event-only cases tested. Once pending is cleared, a duplicate/stale error event cannot release an already acquired valid lock. No browser denial was filtered globally. |
| Clear held movement/fire/jump/cue and allow later gesture | PASS extracted actual C++ lifecycle/release/inputgrab and entity stopmoving bodies in pointer-cpp.py, with fake external APIs. Denial polls call actual browserloseinput, which invalidates private generation, stops proof audio, ungrabs, releases pressed bindings, clears movement/jumpnext/attacking/crouch, discards queued input and publishes. Real entry handler consumes acquisition click and rejects locked/pending/hidden/unfocused/nonprimary entries. Later explicit canvas gesture retries. Stop/focus/visibility/loss/acquisition/new request invalidate stale expected callbacks. No Wasm pointer is retained by asynchronous handlers. |
| Checked source/buffer deletion and retained backend ownership | PASS extracted audio helper tests and genuine SDK inspection. Proof source delete is checked; alDeleteBuffers is checked explicitly before clearing id/deleting wrapper. Failed deletion retains source/buffer/backend, publishes error and suspends actual context on failed shutdown; repeated shutdown or later gesture can retry without allocating duplicate handles. No clearing ids after context teardown. Test doubles verify source/buffer failures, repeated failed shutdown, failed later gesture, suspended-not-closed retained backend, later successful cleanup, no duplicate backend/wrapper and no double delete. Normal engine exit's soundcleanup may follow browserstop; a narrowly browser-guarded proof-handle check routes it back through proof cleanup rather than bypassing retained ownership. The guard returns on failed deletion and falls through existing engine teardown only after proof handles are released. Native cleanup remains unchanged. |
| Actual observed audio_context_state and existing diagnostics | PASS js-helpers.cjs. Added audio_context_state to frozen OUTBREAK_AUDIO_DIAGNOSTICS schema1: actual owner.audioCtx.state when observable, else null. Tested running/suspended/closed/null independently from AL_PLAYING. Null is never described as closed and AL_PLAYING is not interpreted as AudioContext running or physical audibility. Existing required fields, frozen/nonwritable snapshots, actual async resume/suspend/close errors, stale epoch/registry isolation and persistent close failure remain tested. No new audio backend/sample mechanism or header/interface change. |
| Native preservation / narrow source scope / protected files | PASS check.py + final-evidence.py. Native unifdef -U__EMSCRIPTEN__ token sequences equal for main/audio/header, four native syntax checks pass. Full existing audio prefix/suffix outside the proof block are unchanged except the exact browser proof-handle shutdown guard. inputgrab and actual input-release body are byte-for-byte unchanged. Eight D003 protected prototype files and task-start graphics/world sources/governing files match hashes; sound.h exact unchanged. Owned source git diff --check passes. |
| Real current-profile Wasm objects and stable inputs | PASS check.py: main.cpp and audiomanager.cpp actual release/debug Wasm objects plus native release/debug syntax, eight successful whole-TU invocations. Four version-1 Wasm objects and exact hashes below. Every command records all source/header hashes before/after (stable), argv/environment/tool SHA-256 and log. Frozen accepted SDK cache/ports reused; temp/cache outputs task-local. |
| Full integrated link/build, actual headed recovery, audio playback/audibility | NOT RUN. No browser/server/game launch or shared output integration. No real AudioContext playback/decoding/device or physical audibility claim. No P0/P1/MVP or multiplayer acceptance claim. MAIN must release combined integration separately. |

Environment: Darwin 25.5.0 arm64; Apple clang17.0.0 (clang-1700.0.13.5); Node v24.13.0. Installed Emscripten7.0.0 compiler777e6e5db7b4990bcaeb1b9998ed642cc84e6629 reused at /private/tmp/outbreak-web-sdk; approved current-profile SDL2/SDL_image PNG/zlib/Vorbis ports, existing OpenAL link support left unchanged. Exact SDK inspection hashes/tool versions in final-evidence.json, compiler/input/environment commands in result.json. No benchmark/performance claim. Extracted inputgrab fixture emits its existing unused delay argument warning; all checks exit0.

Reproduce the scoped component/helper verification from repository root (these commands write only the new T059 evidence outputs; they do not link/run a browser game):

```sh
python3 web/runtime/tests/T059-player-1/check.py
python3 web/runtime/tests/T059-player-1/helpers.py
python3 web/runtime/tests/T059-player-1/pointer-cpp.py
node web/runtime/tests/T059-player-1/js-helpers.cjs
node web/runtime/tests/T059-player-1/pointer-js.cjs
python3 web/runtime/tests/T059-player-1/final-evidence.py
```

- result.json and per-TU logs: exact native/Wasm argv, environment, tools, stable complete source/header input hashes, signatures/object hashes.
- helper-result.json and extracted-helper.cpp/logs: actual current C++ proof helper/cleanup guard with fake backend.
- pointer-cpp-result.json and extracted-pointer-lifecycle.cpp/logs: actual current lifecycle/release/inputgrab/stopmoving bodies with external engine/JS API doubles.
- js-helper-result.json, extracted-context.js, extracted-snapshot.js/log: actual current audio EM_JS bodies in fake AL/AudioContext VM.
- pointer-js-result.json, extracted-pointer.js/log: actual current pointer EM_JS in fake document/canvas with genuine Promises/DOMExceptions and observed unknown unhandled rejections.
- final-evidence.json/source-freeze.json: all fresh results match final current sources, immutable historical snapshot, native equivalence, protected files and unchanged global observer/release blocks.
- main.cpp.patch/audiomanager.cpp.patch: exact delta from D042's current source pin. sound.h.patch is empty. audio-full-proof-vs-pre-T052.patch also exposes the full proof code/cleanup amendment relative to preserved pre-T052 audio (not labeled as accepted d839 source).

Final frozen source SHA-256:

- `source/src/main.cpp`: `11e1240cfa445472eaf02e68a1742f46919d7d9f3d77e9f334486ab7c04cca1b`
- `source/src/audiomanager.cpp`: `31ea6bc32aeaaf3264795ba7de91f4a9614883fdbab8e93a165864477f2d1039`
- `source/src/sound.h`: `80f635fd48b40ec61524d52707ba7c6f80eb2ad2d8bead137099bdf462c11655`

Actual Wasm object SHA-256:

- `audiomanager-debug.o`: `df7b11c16496e57ba6991d30a40bc8fe2d89dbdfdc13be12ef956364c7c343a7`
- `audiomanager-release.o`: `a4e033aa9080d05b2d2b1f5bbd2f0b4213a706dac65a04aaf1950c78b9ce56e1`
- `main-debug.o`: `6c7c7787d499e472a8b921ef9ce08b5d09e7c6da3fe81a131a3448e861c41a94`
- `main-release.o`: `cfc2af265c51550aa5223f2f4c2d79df8133bdfdfbfd2b29cd654fb5300e4c1d`

## Implementation status

Implemented: request-specific expected-denial recovery, generation invalidation and normal-gesture retry with real event-controlled capture; checked proof source/buffer ownership across repeated cleanup failures, including the ordinary cleanup caller; actual read-only audio context observation. The inherited proof cue path/configuration remains unchanged; no gameplay sounds, stock audio, input injection or new browser action API is added.

Simulation limits: extracted C++ tests replace external engine/backend/JS APIs; extracted JavaScript uses a fake canvas or fake AudioContext registry. Real source translation units are compiled against actual installed headers/SDK into genuine Wasm objects, but no full link or runtime observation is asserted. The unknown-rejection test's process listener records actual Node unhandled-rejection delivery; production browser observers are preserved unchanged.

Incomplete until separate integration: headed recovery from D034's real WrongDocumentError, actual success/legacy/missing-API browser behavior, focus/visibility/capture reentry with real audio, real context shutdown/cleanup failure behavior, full build/link and human audibility. Retained cleanup failures deliberately remain visible errors; wrapper/context ownership is retained until a successful retry, rather than falsely reporting completed teardown. Previous error text can remain after cleanup retry until a later gesture; resource ownership assertions use actual handles/cleanup outcomes, never phase alone.

## Integration and questions

No new dependency, asset, header declaration or shared core protocol. Rebuild changed main/audio and affected header consumers already required by T052, with original T053 audio profile and other separately accepted integration pieces. Preserve original D034 failure and all earlier output pins; do not substitute fake helper evidence for actual headed acceptance.

Integration should observe expected request denial -> actual input/audio loss and visible precise retry -> later ordinary click; Promise resolution alone must not grant capture. Exercise blur/hidden/stop while request pending, stale expected denial after successful new capture, both pointerlockerror/Promise orderings, no automatic rearm, genuine unknown runtime error reporting, audio_context_state versus OpenAL state and null after no observable backend. Verify source/buffer ownership failure/retry against real backend if injecting failures is separately authorized. Audio playing/count never establishes physical audibility.

D042 resolves the historical T052 baseline question; new fresh evidence here supersedes reused task-local T052 verification for current sources without changing old notes/reports. No open scope question or new human hold. MAIN reviews exact frozen sources/evidence and owns acceptance/integration. No source edits after freeze/handoff; any subsequent finding will be a new question.
