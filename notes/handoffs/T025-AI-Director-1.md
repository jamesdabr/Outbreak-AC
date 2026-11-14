# Ticket handoff

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket / revision: T025 / 0.4 RELEASED; worker has not changed status
- Phase / contract revisions: P0, BROWSER_FOUNDATION and GOVERNANCE 0.4 under D004; gameplay contracts remain draft 0.2 context
- Base commit and pre-existing edits: 13f0d8eea4822dee5c976661218d022be74342e3 plus D004-review-baseline.json. server.cpp matched its pinned hash before editing. Existing combat and first-wave edits preserved.
- Changed files: source/src/server.cpp; new web/runtime/tests/offline_auth_fixture.py, offline_auth_fixture.cpp.in, offline_auth_source_check.py, offline_auth_fixture_report.json, offline_auth_source_report.json, offline_auth_native_client_release.log, offline_auth_native_client_debug.log, offline_auth_native_server_release.log, offline_auth_native_server_debug.log; this handoff and notes/questions/T025-AI-Director-local-auth-failure.md.
- Commit or patch reference: no commit/branch/push authorized or performed; inspect `git diff -- source/src/server.cpp`.

## Implementation status

Implemented: narrow `__EMSCRIPTEN__ && !STANDALONE` same-thread queue processing. Each poll dequeues at most one request; stale/removed/null/out-of-range slots are discarded. Current jobs require the exact response type, matching sequence, ST_LOCAL identity, wantauth=0 and current needsauth=false. Success is recomputed rather than trusting the job's prior success field. Eligible jobs use the original continued-handshake completion code unchanged. Ineligible current jobs receive an explicit DISC_AUTH diagnostic and the existing disconnect_client(cn, DISC_AUTH) call; no continuation or signature success is produced.

The browser branch excludes this queue's semaphore object, worker function, creation and semaphore post. Native client and standalone branches retain their original preprocessed auth code. Normal parsing, staging, capacity checks and all source after this auth section are unchanged. The ringbuf's 16-element storage has **15 usable pending entries**, preserving its existing SIZE-1 convention.

Simulations/test doubles: the helper fixture compiles the actual ringbuf, auth helper functions and entire polldeferredprocessing implementation extracted from current source. It adds fixture-only job construction/destruction counters. Client containers/fields, logging, sendf, disconnect_client and unreachable vita/signature-related dependencies are mocks. No worker/semaphore/signature implementation is supplied, so accidental browser-branch references to them fail fixture compilation. This is helper evidence, not the real engine parser or an executed game handshake.

Incomplete/ambiguous: local failure teardown. The real disconnect_client immediately returns for ST_LOCAL. The adapter reports and rejects the request but does not invent local teardown/reset semantics. Question T025-AI-Director-local-auth-failure asks the lead to confirm whether this existing failure behavior plus diagnostic is sufficient or release a specific local teardown policy. No new client teardown/reset is implemented. No remote browser auth, service removal or transport is implemented. Actual Wasm TU verification, browser startup/map load, real local handshake and runtime traffic observations are NOT RUN. Submission is partial pending the local failure-policy review and SDK verification, not accepted browser readiness.

## Acceptance evidence

| Criterion | Result | Evidence and limits |
| --- | --- | --- |
| 1 guarded bounded poll, no queue worker/wait, native retained | PASS (source/helper) | offline_auth_fixture_report.json verifies one-per-poll for success, stale and rejection with work behind it. offline_auth_source_report.json verifies no thread/semaphore symbols in preprocessed browser auth section and token-equivalent native/client/standalone auth sections. Not a whole-browser no-thread claim. |
| 2 eligibility, stale safety and explicit auth failures | PASS for eligibility/discard/no-grant checks; FAIL to establish complete local failure teardown policy | Fixture covers type, wantauth, needsauth, remote identity, sequence reuse, removed/null/out-of-range slots; current failures log DISC_AUTH and invoke existing auth rejection. Actual ST_LOCAL disconnect is unsupported by the existing function. Open question; no successful remote/auth-required completion. |
| 3 existing completion, parser and ownership | PASS (source/helper) | Common completion text and parser/following source exactly unchanged; fixture tracks zero live jobs after every drain, with no continued reply on stale/rejected jobs. Each path deletes its removed job once. No new public symbols/header/wire messages. Real parser/handshake NOT RUN. |
| 4 helper/queue coverage | PASS (helper only) | Extracted fixture tests eligible local, wrong type, wantauth, needsauth, remote identity, reused sequence, removed/null slots, negative/equal-size/large out-of-range indices, empty queue, full capacity, wraparound and at-most-one drain. Stage/commit producer API used for capacity test. |
| 5 native syntax and pinned Wasm TU | PASS native syntax; NOT RUN Wasm | Four real server.cpp syntax checks exit 0 with empty diagnostics (client/standalone, release/debug). emcc absent on PATH; no separately accepted ready SDK setup supplied. No host compiler macro fixture counts as Wasm TU verification. |
| 6 remaining dependencies and limits | PASS (inventory documentation) | Listed below; no assertion of complete service separation or T014 completion. |

## Exact verification commands and tool identity

Repository: /Users/jd1/code/apps/outbreak. macOS 26.5.1, Darwin 25.5.0 arm64. Compiler: Apple clang 17.0.0 (clang-1700.0.13.5), target arm64-apple-darwin25.5.0, installed under /Library/Developer/CommandLineTools/usr/bin. No new dependency, tool installation, user-profile access or service launch.

Authored fixture and checker were read in full before execution, along with the extracted source, ringbuf definition and production disconnect guard. The confirm-cross-system-execution skill was read/applied; these inspected local checks fall within T025's explicit execution authorization and touch no external system.

```sh
python3 web/runtime/tests/offline_auth_fixture.py
python3 web/runtime/tests/offline_auth_source_check.py
clang++ -fsyntax-only -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers -Isource/xcode/Frameworks/SDL2_image.framework/Headers -Fsource/xcode/Frameworks -idirafter source/include source/src/server.cpp
clang++ -D_DEBUG -fsyntax-only -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers -Isource/xcode/Frameworks/SDL2_image.framework/Headers -Fsource/xcode/Frameworks -idirafter source/include source/src/server.cpp
clang++ -DSTANDALONE -fsyntax-only -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers source/src/server.cpp
clang++ -DSTANDALONE -D_DEBUG -fsyntax-only -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers source/src/server.cpp
git diff --check -- source/src/server.cpp
```

All commands above exited 0. Syntax stdout/stderr were redirected into the four corresponding offline_auth_native_*.log files (empty on success). The Python fixture compiles with `clang++ -std=c++11 -Wall -Wextra -pedantic` in a new /private/tmp/offline_auth-* temporary directory, runs only the extracted helper executable with a 10-second timeout and removes its temporary directory. Exact generated compile command and result are saved in offline_auth_fixture_report.json. Both scripts write only their named reports.

offline_auth_source_check.py obtains the baseline server.cpp with read-only `git show`, verifies that original text matches D004's pinned SHA-256 and uses `clang++ -E -P -x c++` on the extracted auth section. It compares native-client, STANDALONE and STANDALONE+EMSCRIPTEN token outputs to baseline, then checks the browser auth section's absent worker/semaphore symbols. These are host preprocessing checks, not target compilation. It also hashes every D004 source entry: only main.cpp (concurrent T017 owner) and server.cpp differ at submission; all other pinned source files match. No overlapping server.cpp edits were observed.

Source SHA-256 submitted: `8aa30baf2f6f6ae44cf53f65d08c3c02d57582d313affee73c42d9dbc4e04cda`. Tests/report hashes refer to that source. T025 and governing contract revisions were re-read before submission and remain 0.4. The native syntax commands use existing host headers only; no Wasm SDK headers or binaries were substituted.

## Remaining dependencies not removed

- `server.cpp` still contains demo semaphores/workers and dedicated config/map workers; `serverfiles.h` and `log.cpp` retain synchronization and log-worker paths. This patch removes only the deferred-auth queue semaphore/worker in the non-STANDALONE browser branch.
- `clientgame.cpp` command sleeps still create and wait on sleepssemaphore; tools.cpp keeps SDL/POSIX synchronization. No global no-op/success shim was added.
- main startup still calls initserver, localconnect and setupautodownload; frame still runs serverslice and download polling. Common server initialization still calls servermsinit, with master/config/global dependencies. T017 owns main.cpp and its bounded offline clock, not this worker.
- Native HTTP sockets/resolver waits, server browser/master discovery, package updater and download queues remain. Setting autodownload=0 alone is not complete exclusion of its updater thread.
- Profile/auth config loading, certificate directories, deferred passphrase work, connect-protocol hooks and host settings/log paths remain outside this adapter.
- Bot lifecycle/perception/pathfinding remain client coupled; updateworld can run BotManager.Think in botmode and rendergl calls WaypointClass.Think. No AI budget measurement or zombie/Director feature was added.
- Browser network transport, transport-independent mode predicates and prevention of local reconnect fallback remain unreleased follow-up work. This local-only auth adapter does not make networked browser authority safe.

## Integration and questions

No shared header, interface, wire schema, asset or dependency was added. Only server.cpp's deferred auth section was changed. main.cpp, platform.h, tools.h, protected combat prototype files, contracts/tickets/decisions and historical notes were not edited by this worker. No game was linked or launched; no native/browser server, public API or external service was contacted.

Open question: notes/questions/T025-AI-Director-local-auth-failure.md. Lead should review the explicit rejection/no-continuation behavior against criterion 2 before accepting this micro-adapter. Pinned Wasm TU and real offline map/handshake checks must remain NOT RUN until their actual prerequisites and execution scopes are available. No ticket/P0 acceptance is asserted here.
