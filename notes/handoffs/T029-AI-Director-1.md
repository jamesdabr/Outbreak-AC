# Ticket handoff

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket / revision: T029 / 0.5 RELEASED, unchanged by worker
- Phase / contract revisions: P0, BROWSER_FOUNDATION and GOVERNANCE 0.5; D005. Gameplay documents remain draft context.
- Base commit and pre-existing edits: 13f0d8eea4822dee5c976661218d022be74342e3 plus D005-baseline.json. T025's existing guarded server.cpp adapter is preserved and completed. All seven other owned modules matched D005 before edits. Protected combat edits and other workers' files were preserved.
- Changed source files: source/src/server.cpp, tools.cpp, serverms.cpp, http.cpp, serverbrowser.cpp, autodownload.cpp, crypto.cpp; rendergl.cpp only around WaypointClass.Think.
- New verification files: web/runtime/tests/services_check.py, services_wasm_check.py, services_symbols.py, services_submission.py; services_report.json, services_wasm_report.json, services_wasm_report-tools.cpp.json, services_symbols_report.json, services_submission_report.json; services_wasm/ contains the 16 actual Wasm objects and corresponding logs. Prior T025 reports/handoffs/questions were not overwritten. This handoff is new.
- Commit/branch/push: none authorized or performed. Temporary authored edit driver and owned source snapshots are /private/tmp/t029-apply-services.py and /private/tmp/outbreak-t029-before/; no other worker's changes were reset or reverted.

## Implementation status

Implemented actual browser service boundaries, not a proposal-only inventory:

- Current invalid ST_LOCAL auth jobs are deleted before `disconnect(1,0)`. This uses real cleanup without localconnect fallback. Remote invalid jobs use DISC_AUTH; stale/removed/reused jobs do not disconnect current identities. One request is still consumed per poll, using the real parser queue and unchanged successful completion block.
- Browser master registration/connections/info polling, server-browser refresh/list/DNS/LAN ping, native HTTP, package ping/updater/download/install, certificate file/directory loading and deferred/authsetup passphrase paths are unavailable. Functions with results return false/-1/null/no data according to their semantics and provide errors/diagnostics. Void polling functions have no worker/results to poll and fabricate no completion. Package download returns zero actual bytes; missing-media checks remain in the real map loader. No new source fetch or successful auth/download is fabricated.
- Single-thread browser semaphores store an actual integer resource count, with immediate acquire/release and nonblocking try/timed acquire. No SDL subsystem is used in their constructors. A would-block void wait, negative count, overflow, unsupported thread creation/join/poll/detach or sleep emits a diagnostic and aborts rather than allowing execution to continue as if successful. A null detach is only cleanup of no thread. The browser profile has one execution thread, so ismainthread returns true. Native/standalone implementations remain unchanged.
- `%H` hostname formatting reports `unavailable` instead of doing a hidden native reverse-DNS query in the browser. Numeric address formatting remains available.
- Browser dedicated startup fails explicitly before native host creation. Real offline initserver(false), local protocol, common data/simulation, parser, map and movement dependencies are retained. Browser rendering does not run WaypointClass.Think/flooding; no fake path result or AI feature was added.

Simulations/test doubles: extracted helper fixtures mock clients, sends, logging and service containers; their compile/run results are helper evidence. Semaphore implementations, queue, eligibility and poll bodies are extracted from actual source. Native syntax checks and target objects compile actual complete source modules. No complete game has been linked/launched by this worker. Actual map movement, real handshake, browser graphics/input and traffic capture remain NOT RUN.

## Acceptance evidence

| Criterion | Result | Evidence / limits |
| --- | --- | --- |
| 1 local cleanup, remote failure and stale safety | PASS (source/extracted helper) | services_report.json auth_cleanup run exits 0. Fixture asserts removed job is deleted before cleanup, parameters are exactly (1,0), ST_LOCAL is invalidated, queued stale work never continues, current remote uses DISC_AUTH, and stale/removed/null/out-of-range/reused identities never disconnect. Actual client cleanup/handshake runtime NOT RUN. |
| 2 unavailable native services, no worker/socket activation in guarded entries | PASS (source/helper/objects) | Actual disabled function bodies compile without declared native socket/thread/filesystem APIs in fixture and return failures/no data. Release objects for HTTP, serverbrowser, autodownload, serverms, crypto and tools contain no identified native socket/DNS/SDL-thread/semaphore imports. Whole-client traffic NOT RUN; residual server symbols listed below. |
| 3 counted immediate synchronization, visible failures, native preservation | PASS (helper/native/target compile) | Static semaphore before main, acquire/post resource preservation, empty try/timed immediate failure, nested wait failure, thread/create/join/poll/detach and sleep failure, count underflow prevention/overflow and invalid initial count tested. All eight intentional fatal scenarios emit the diagnostic and exit nonzero. Native TU token equivalence passes. |
| 4 retained bounded real local protocol, disabled waypoint work | PASS (source/objects) | Common completion and parser retained; normal local simulation functions remain. rendergl has only the browser guard around waypoint Think. Actual map loading/movement NOT RUN. |
| 5 meaningful tests, native syntax and real Wasm objects | PASS (helper/compile) | All helper/source checks pass; 24 actual native syntax checks exit 0; all eight native full-TU preprocess comparisons match original baseline; 16 real release/debug Wasm object builds exit 0 with correct magic, current-source hashes and object hashes. services_submission_report.json validates final evidence, including later rebuilt tools objects. Not a linked runtime pass. |
| 6 remaining symbols and service graph | PASS (inventory) | Exact llvm-nm output in services_symbols_report.json and graph below. Future transport/auth/NETWORK_CLIENT and T014 remain unimplemented/unaccepted. |

## Commands, identity and reproducibility

Working directory /Users/jd1/code/apps/outbreak. Host macOS 26.5.1, Darwin 25.5.0 arm64. Native compiler Apple clang 17.0.0 (clang-1700.0.13.5), arm64-apple-darwin25.5.0. Target compiler actual `em++` reports Emscripten 7.0.0, compiler source 777e6e5db7b4990bcaeb1b9998ed642cc84e6629, from /private/tmp/outbreak-web-sdk/upstream/emscripten. SDK release pin remains 6afbd83493d647051772d491124187d4e9a0cda9.

Read D005 SDK authorization, T026 installed-identity/config/port-integrity/probe evidence, installed em++ wrapper and em++.py before target execution. Installed wrapper hashes match the inspected T026 identities; installed source/recipe comparison evidence and five port hashes were verified by T026 and required by this worker's target driver. No SDK installation/activation, extra ports, network download or compiler bootstrap was performed by this worker. Target environment uses the approved config/cache and EM_FROZEN_CACHE=1 to prevent cache construction; outputs and temporary compiler files are beneath this worker's test directory. No host framework headers enter target commands.

```sh
python3 web/runtime/tests/services_check.py
python3 web/runtime/tests/services_wasm_check.py
python3 web/runtime/tests/services_wasm_check.py --units tools.cpp
python3 web/runtime/tests/services_symbols.py
python3 web/runtime/tests/services_submission.py
git diff --check -- source/src
```

Final commands above exit 0. Full target compile was followed by a tools-only rebuild after removing the reverse-DNS dependency; services_submission_report.json selects actual current-source/current-object records from full and subset reports and validates all 16 results. An earlier server-only rebuild after the dedicated-startup guard was subsequently superseded by the full 16-object pass. No stale successful object is counted: compiler drivers delete each own target object before building, and the submission checker matches source and object hashes.

services_check.py runs extracted helper executables in an owned temporary directory and removes it, then actual native syntax with:

```text
clang++ [-D_DEBUG] -fsyntax-only
  -Isource/src -Isource/enet/include
  -Isource/xcode/Frameworks/SDL2.framework/Headers
  -Isource/xcode/Frameworks/SDL2_image.framework/Headers
  -Fsource/xcode/Frameworks -idirafter source/include source/src/<owned-module>.cpp
```

Eight client modules each release/debug (16 commands); server/tools/serverms/crypto each STANDALONE release/debug (8 commands). services_report.json records every complete argv, exit and diagnostics. Native preprocessing uses `clang++ -E -P -x c++` with both current and `git show 13f0d8...:source/src/<module>` inputs named stdin and identical includes; all eight release token outputs are equal after whitespace normalization. These source-equivalence checks do not assert native runtime behavior beyond preserved token paths.

Actual Wasm compilation uses:

```text
/private/tmp/outbreak-web-sdk/upstream/emscripten/em++
  --target=wasm32-unknown-emscripten -std=gnu++11 -fsigned-char
  -sUSE_SDL=2 -sUSE_SDL_IMAGE=2 -sUSE_ZLIB=1 -sUSE_VORBIS=1
  -sLEGACY_GL_EMULATION=1 [-O2 | -O0 -g -D_DEBUG]
  -I<repo>/source/src -I<repo>/source/src/bot -I<repo>/source/enet/include
  -c <actual-owned-source> -o <tests>/services_wasm/<module>-<mode>.o
```

Exact commands, environment, source/object SHA-256, magic verification and log paths are in services_submission_report.json and its referenced target reports. That report contains every current source hash; services_report.json also pins all eight. Native and Wasm logs include normal existing source/compiler warnings; no warning was silenced to claim success.

Two initial fixture failures were corrected before final evidence: the new real local cleanup correctly invalidated a subsequent queued job, unlike T025's old diagnostic-only behavior, so the fixture now expects a stale discard rather than a continuation; function extraction was anchored to column-zero definitions to avoid collecting an inner `extern authsetup` declaration and unrelated functions. No product behavior was weakened to satisfy either test. T025's historical helper driver/record remain historical; services_check.py supersedes it for D005 cleanup semantics.

## Exact service graph and remaining integration dependencies

1. Player-owned browser startup -> `initclient`/client world initialization -> `initserver(false)` -> server parameter/data/key setup -> `servermsinit(false)` now sets usemaster=false without master/LAN sockets -> local server reset. Dedicated=true now fails before startup.
2. `localconnect` -> ST_LOCAL client/sendservinfo -> `localservertoclient` -> client parser -> SV_SERVINFO_RESPONSE -> `sendpackettoserv` -> `localclienttoserver/process` -> bounded servinfoauths staging -> `serverslice/polldeferredprocessing` -> one current eligible local/no-auth completion -> existing SV_SERVINFO_CONTD/sendintro. Invalid current local deletes its job then `disconnect(1,0)` -> client cleanup/localdisconnect, no localconnect. Remote current failures use DISC_AUTH; stale jobs only delete.
3. Real frame -> updateworld's command-sleep semaphore, physics/movement, receive/send -> common serverslice -> demo transmission polling (no demo job in proof) -> render. Counted semaphore immediately preserves command queue locking. render no longer runs waypoint Think. Main/clientgame remain other owners; T029 neither edits their frame nor claims that botmode/weapon code has been removed there.
4. Legacy package path from worldio/load_world -> requirepackage=false with diagnostic; downloadpackages=0 real bytes. Required texture/model/audio/map checks still run; packaged original manifest is the real content source, not an invented download. setupautodownload reports unavailable and creates no updater; response poll has no worker. dlpackage/processdownload likewise unavailable.
5. Server/menu callbacks -> refreshservers/retrieveservers/updatefrommaster/resolver/query/pings are unavailable or no-data. HTTP set_host/connect return false with err, get returns -1 with err; no native connect worker. `serverms`/flush calls have no master/listener buffers to service. Auth setup returns intret(0), clears sk and never starts passdeferred. loadcert/loadcertdir do not access files/directories. `%H` formatter does not perform reverse DNS.

Release llvm-nm inventory of actual objects: HTTP, serverbrowser, serverms, autodownload and tools have no native DNS/socket/SDL thread/semaphore imports; crypto retains SDL_GetTicks for existing timing, not a worker. rendergl retains real GL compatibility functions and SDL_GL_GetProcAddress, which still require full-client link/renderer proof.

server.cpp remains a real dual-use server module, not a blanket stub. Its object still imports ENet host/packet/peer/time functions, numeric enet_address_get_host_ip, enet_address_set_host, enet_socket_send and sl_createthread. The named residual native calls are dedicated setup (`initserver` guarded against browser dedicated startup), dedicated portions of serverslice, and `extinfo_statsbuf` (normally reached by excluded serverms info polling). Their mere symbol presence is not observed traffic, but full linkage still needs compatible ENet/library symbols; no full-link or dead-code elimination result is claimed. Full exact undefined names are saved in services_symbols_report.json.

Other live integration boundaries outside this allowlist:

- client.cpp still defines ENet connect/LAN/admin/mod connection commands and local fallback, plus remote packet receive/send paths; they are not browser transport. DNS-backed connect now fails via resolverwait, but direct LAN command paths are not proven absent from the linked client. The minimal Player-owned startup/config must not expose or call native connection flows; a future explicit client transport/profile ticket must guard them before NETWORK_CLIENT. No whole-client no-network guarantee is inferred from these module tests.
- log.cpp has a native logging worker if initlogging is invoked. initserver(false) does not call dedicated restartlogging; unexpected thread use now aborts visibly. serverfiles/demo worker functions remain compiled but are not launched by the offline path. Demo recording/replay is not enabled by this ticket.
- Protected clientgame.cpp retains BotManager.Think under botmode, local prototype combat and command scheduler; Player-owned minimal startup must choose the frozen offline profile. Only render waypoint execution was disabled here. No authoritative zombie/combat logic was moved.
- Stream/profile/settings paths, main boot/auth/URI/config selection, original asset mount/media dependencies and GL/audio runtime are other owners' integration work. No host profile or inherited private config was accessed by this worker.
- Legacy GL and other unresolved library/game symbols are link inputs, not automatically link errors. Actual full-client link, browser yielding frames, real map/collision/input, handshake and no-unwanted-traffic capture must be performed in the corresponding released integration scope before T014 acceptance.

## Integration and questions

No new dependency, public header, wire message or shared schema was introduced. Native and STANDALONE policy is preserved behind guards. D005 resolves the earlier T025 local rejection question; no new clarification blocks the implemented T029 source/helper/object work.

Final preservation check against D005: only these eight owned source paths and concurrently Player-owned main.cpp differ. Other pinned sources, including all protected combat files and T026-owned platform.h/tools.h, match their D005 hashes at this check. No overlapping edit to this worker's paths was observed. AGENTS/contracts/ticket/decision revisions were re-read before submission and remain 0.5; none was edited. Source hashes/current objects are pinned in services_submission_report.json.

Outstanding: full link/runtime/traffic verification and the external client/profile/library boundaries above. These are not waived by native syntax, extracted fixtures or actual Wasm objects. Only MAIN reviews and accepts ticket/P0 status.
