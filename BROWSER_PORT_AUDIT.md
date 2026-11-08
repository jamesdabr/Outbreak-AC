# AssaultCube to browser audit for Outbreak

Date: 7 November 2026, America/New_York. Source baseline: `13f0d8eea4822dee5c976661218d022be74342e3`, plus preserved uncommitted local combat prototype changes. This report precedes delegated browser ticket authoring.

## Conclusion

The C++ client is a plausible WebAssembly port candidate, but this checkout has no browser build, browser runtime integration or browser transport. A compiler switch alone will not produce a playable browser game. The largest risks are legacy graphics and the native-network/runtime assumptions distributed throughout startup and client services.

Proceed with an isolated Emscripten compatibility path before any broad rewrite. Preserve the native dedicated server. Start with browser build tooling, frame-loop adaptation, a minimal asset manifest, independent browser verification tooling and a client/server service-separation plan. Then demonstrate a real map in a browser and two actual browser clients connected to a real standalone server. An echo-only WebSocket demo or an HTML mockup cannot satisfy either game gate.

Do not choose another engine based on this static audit alone. Escalate concrete compiler/runtime failures, unsupported rendering or unacceptable network behavior to the owner/lead before broad replacement work. The eight-player gameplay scope and deferred game-state LLM tester requirement remain unchanged.

## Evidence and limits

- Inspected native build targets, startup/main loop, graphics initialization and draw paths, asset and profile filesystem, audio, ENet integration, server browser, HTTP/downloads, threads, authentication hooks and current worker ownership.
- Text searches found no `__EMSCRIPTEN__`, `emscripten_set_main_loop` or WebSocket integration in the inspected `source/src` C++ and header files.
- `emcc`, `emcmake` and `emmake` are not on the current PATH. Node, Python and Apple clang are available. The bundled runtime contains Playwright; installed browser binaries and usable browser graphics still need verification.
- The prior native audit's twelve syntax-only passes are not WebAssembly compilation evidence. No Emscripten build, browser frame capture, browser networking session or browser performance benchmark was run for this report.
- Existing worker chats were identified and read. They share this working directory. The uncommitted local down/revive experiment belongs to earlier player/combat work and must not be reverted or silently counted as browser readiness.
- Counts below are textual matching lines in current `.cpp` files and top-level `.h` files, not dynamic call counts or effort estimates.

## Required work by subsystem

| ID | Finding and source evidence | Required browser work | Risk |
| --- | --- | --- | --- |
| B01 Build system | `source/src/Makefile:9` selects clang++; desktop SDL config and native GL/X11/audio/ENet libraries are assembled in its platform branches. Native PCH and executable targets dominate. | A separate pinned Emscripten target, wasm-compatible libraries, isolated objects/output/cache and explicit client/native-server targets. Never link host `.a`, DLL or framework binaries into Wasm. | High |
| B02 Runtime loop | `main.cpp:1522` runs forever; frame limiting calls `SDL_Delay` in `limitfps()` around line 711. The loop owns input, gameplay, embedded server, audio, render and download polling. | Extract one frame callback with persistent state and yield via Emscripten/browser scheduling. Preserve native behavior behind guards; bound long-frame catch-up and clear held inputs on focus loss. | High |
| B03 Graphics | `rendergl.cpp::gl_checkextensions()` loads desktop extension entry points; `gl_init()` enables fixed fog. `rendercubes.cpp` uses client arrays and quads; `vertmodel.h` uses display lists; HUD/particles/text use legacy draws. | First test legacy GL emulation with a documented feature profile. Catalogue actual failures and disable optional reflection/shadow features only in an explicitly logged spike profile. If needed, port the minimal render paths to WebGL-compatible buffers/shaders under a new approved ticket. | High |
| B04 Client networking | `client.cpp::connectserv_()` creates an ENet host and peer; `gets2c()` uses `enet_host_service`. `source/enet/unix.c` implements native sockets/DNS. | Browser-supported message transport and a defined server integration path. Retain message framing, channel semantics and disconnect behavior; do not assume raw UDP works in the browser. | High |
| B05 Embedded server | `main.cpp` calls `initserver(dedicated)`, `localconnect()` and `serverslice(0)`. Client objects include `server.o`, `serverms.o` and bot objects. | Separate local test mode, browser client services and actual standalone server. A map-only demo may explicitly retain an offline local simulation, but multiplayer proof must cross a process boundary to a standalone authority. | High |
| B06 Browser HTTP/services | `http.cpp:94` opens a native stream socket and its connect path creates a thread, waits and sleeps. `serverbrowser.cpp` does DNS, UDP LAN discovery and master-server downloads. | Remove/disable native discovery/autodownload/auth-directory integration in the browser spike. Later replace required content/connection services with asynchronous same-origin Fetch/Web APIs. No public AssaultCube listing or outbound legacy service traffic. | High |
| B07 Thread model | `tools.cpp:826` wraps SDL thread creation and semaphores; `server.cpp` creates config/map/demo workers; `http.cpp:101` and `crypto.cpp:886` create client-related threads. | Start with a clearly bounded single-thread browser profile and stub/disable only identified unused services. If client threads prove necessary, approve a pthread build and required isolation headers; never silently emulate waits as success. Server workers can remain native. | High |
| B08 Assets and startup | `main.cpp:1374-1489` loads icon, missing texture, fonts, config, model attributes, settings/auth files, models and docs. `stream.cpp::findfile()` searches profiles, zip files and working-directory packages. | Explicit preload manifest and browser virtual paths; every required bootstrap asset must be present or produce a clear failure. Separate private development fixtures from assets permitted in shared builds. No whole-checkout preload. | Medium/high |
| B09 Persistence | `main.cpp::quit()` writes settings/history/maps; `stream.cpp:176` configures a host home directory. Native quit/unload is not a dependable browser save event. | Virtual browser profile, optional IndexedDB persistence with explicit sync boundaries, resilient load/save failure handling and memory-only fallback. Do not write to native AssaultCube settings. | Medium |
| B10 Input and lifecycle | `main.cpp::inputgrab()` assumes relative mouse/window grabs; fullscreen/resizing and SDL window events are desktop-oriented. | A click-to-play state, browser pointer capture, Escape/reacquisition, canvas resize, focus/visibility handling, and cleared fire/movement on blur. Desktop keyboard/mouse is the initial experimental target, not a mobile promise. | Medium |
| B11 Audio | `audiomanager.cpp::initsound()` enumerates devices and creates an OpenAL context. `openal.cpp` and `oggstream.cpp` decode Vorbis and queue positional sources. | Verify Emscripten audio support for the actual calls and codecs; activate after user gesture, handle suspend/resume, and distinguish muted loading from a failed audio backend. Positional audio needs real-browser checks. | Medium |
| B12 Native/debug assumptions | `platform.h` includes SDL_syswm and desktop GL headers; `tools.h:17` uses x86 `asm("int $3")` for debug assertions. Logs and helpers include sockets, host paths and time/thread APIs. | Browser-specific header guards, portable debug traps, console diagnostics and an explicit inventory of retained versus unavailable platform functions. Do not declare release-only compilation a debug-ready port. | Medium |
| B13 Distribution | `packages` has 1,762 files and 46,891,737 raw bytes; `config` has 48 files/726,577 bytes; `bot` has 47 files/5,907,757 bytes. These are checkout totals, not browser download estimates. | Reduce startup pack to actual dependencies, measure compressed transfer and decompressed memory, provide progress/errors and content hashes. Browser downloads are distribution; restricted character/weapon assets must not slip into a shared build. | Medium/high |
| B14 Hosting | Native launchers assume local programs/data; no web delivery layout exists. | Serve HTML/JS/Wasm/data with correct MIME types, explicit build versions, cache policy, HTTPS/WSS for hosted deployment and required origin/isolation policy. Local development remains loopback-only unless separately authorized. | Medium |
| B15 Verification | Existing workflow builds Linux executables; `source/tests` has no established browser suite. | Real-browser smoke harness, console/network failures, input/focus tests, runtime errors and browser/OS matrix, plus measured downloads, memory, frame times, network behavior and two-client state agreement. | High |

The graphics scan found 44 matching `glBegin` lines across 10 files, 122 matrix/transform lines across 8 files and 5 display-list lines in `vertmodel.h`. Raw socket calls occur in multiple services beyond the primary client connection. These findings show the port boundary is broader than one renderer or one connect function; they do not prove the renderer must be replaced.

## Recommended technical path and alternatives

### Client build and graphics

Use Emscripten to compile the candidate C++ client and its supported library ports. SDL2, zlib, image and Vorbis dependencies must be built for the target rather than taken from macOS frameworks. Prefer a separate browser build description so native make rules and pre-existing prototype changes remain reviewable. [Emscripten build documentation](https://emscripten.org/docs/compiling/Building-Projects.html)

Legacy GL emulation is a feasibility tool, not an accepted performance result. Verify map geometry, models, textures, HUD, fog and particles in a real browser. Emscripten documents legacy emulation and recommends a WebGL-friendly subset for efficiency; whether this particular renderer works is unresolved. [Graphics documentation](https://emscripten.org/docs/porting/multimedia_and_graphics/OpenGL-support.html)

Freeze a toolchain version in generated build metadata before comparison tests. First-party documentation currently includes development-version material; copying a flag from documentation is not evidence that the locally selected SDK supports it. No SDK version has been installed or accepted in this audit.

### Networking

Evaluate a direct WebSocket message adapter or a small per-session gateway to the native server as the initial controlled experiment. A gateway must preserve packet/channel boundaries and client identity, restrict destinations to the local test server, impose bounded queues and handle clean disconnects. It must not become an arbitrary socket proxy. A generic TCP WebSockify bridge alone does not establish compatibility with ENet's UDP protocol.

WebSocket reliability and ordering may introduce latency under loss and backlog. Record it explicitly and avoid stacking unbounded reliable delivery over ENet without measurement. WebRTC data channels or WebTransport datagrams are later alternatives if the experiment shows an actual need; they add endpoint/negotiation/operational work and are not selected by this report. Emscripten describes the available browser networking approaches and native socket limitations. [Networking documentation](https://emscripten.org/docs/porting/networking.html)

First define the experimental packet/transport boundary in a lead-approved ticket. Final game authority remains on the dedicated server. Browser transport conversion cannot turn client-reported hit lists into authoritative hits; that separate combat gap remains in the gameplay backlog.

### Loop, threads and services

Extract a persistent frame callback and browser-controlled scheduling; do not retain a blocking native loop on the browser UI thread. Explicitly track which startup/server/HTTP/auth functions may run in the browser profile. Removing unused native services from a spike is acceptable only when logged and bounded; succeeding with no networking does not satisfy multiplayer acceptance. [SDL2 browser guidance](https://wiki.libsdl.org/SDL2/README-emscripten)

The initial experiment should avoid browser pthread requirements where possible. A pthread build requires deliberate scheduling and cross-origin isolation. This must be a measured follow-up if needed, not a late hosting surprise. [Threading documentation](https://emscripten.org/docs/porting/pthreads.html)

### Files, UI and assets

Preload a small, explicit virtual filesystem layout before C++ startup. Retain synchronous game file reads against that virtual filesystem, not the user's host filesystem. Browser memory files are transient; settings persistence needs a separate synchronization policy if enabled. [Runtime and filesystem documentation](https://emscripten.org/docs/porting/emscripten-runtime-environment.html)

Build a click-to-play shell with loading/error state. Fullscreen is optional; pointer capture and input release/reacquisition must work. Defer browser account services, public matchmaking, service workers and a mobile UI until separately contracted. These are not prerequisites for a private desktop-browser proof.

Inventory transitively loaded configs and their asset references, not just map textures. A source map alone may not include fonts, missing-texture fallback, model configs or sounds required by boot. The browser candidate must distinguish original/permitted assets from personal-use or noncommercial stock media; the prior ENGINE_AUDIT.md identifies concrete notice examples. This is an engineering inclusion policy, not a file-by-file legal clearance.

## Work breakdown and dependency boundaries

### First parallel worker assignments

These assignments can start without a final renderer or network choice. Each receives its own exact write allowlist; all authoritative ticket/contract edits remain with the coordinating lead.

1. **Engine & Multiplayer:** toolchain preflight/bootstrap/build driver in `web/build/` and browser platform includes. Pin and record the locally selected SDK; compile an actual engine translation unit with Wasm tools. Build infrastructure alone must not be reported as a runnable game.
2. **player combat:** guarded browser frame-loop/input adaptation in `source/src/main.cpp`, plus browser event shim only if expressly listed. Preserve the existing native branch and uncommitted combat prototype. No new camera/combat feature work.
3. **World/Match-Systems:** asset/config dependency inventory and deterministic manifest generation in `web/assets/`. No source map edits or stock asset repackaging as cleared output.
4. **QA/Performance:** loopback static serving/preflight and a browser smoke harness in `web/qa/`. Verify the harness with explicit fixtures; report fixture-only results separately from actual game results.
5. **AI-Director:** concrete browser/native service-separation and client bot/perception budget plan in a worker note. No zombie/Director implementation, shared code changes or contract editing.

The initial outputs are prerequisites, not substitutes for the T014 map-in-browser proof. Engine owns build descriptions/platform headers; player owns `main.cpp`; world owns manifests; QA owns harnesses. Shared build inputs are consumed through lead-defined file paths. A worker must raise a question before editing another owner's files.

### Follow-up gates

- **T014 browser runtime and graphics proof:** integrate accepted bootstrap, loop, manifest and QA work; compile/link and launch the actual game/map. Record each feature that is implemented, disabled or simulated. This is the first client-foundation evidence gate.
- **T015 browser/server transport proof:** specify the experimental transport, implement a real browser-to-standalone-server connection and verify two-client state, loss/backlog/timeout behavior and session cleanup. Do not require the full extraction game here.
- **T001 reproducible browser/server build:** stabilize the chosen build after evidence. **T002 interfaces** records the selected shared contracts; **T003 QA profiles** freezes final environment and acceptance thresholds.
- Only then release P1 combat and subsequent gameplay phases. The current eight-player MVP and LLM testing direction do not justify skipping any browser foundation gate.

## Release policy for the first wave

The current documents are drafts. The owner's present instruction explicitly authorizes this audit, subagent ticket drafting and handing ready jobs to worker chats. Record a lead-owned decision approving only the browser-foundation execution subset, not every unresolved gameplay number. Subagents write proposed ticket files under `notes/ticket-proposals/`; the lead reviews and adopts final contracts into `tickets/` and releases exact assignments.

Do not dispatch work that requires a still-unselected production transport/engine. Do not authorize broad system package installation, public hosting, remote project credentials, stock media distribution or commits/pushes through implication. Local toolchain setup/build and loopback test execution must be concretely described by each released ticket; unfamiliar external installation scripts require inspection before execution. A missing SDK or browser dependency should produce a scoped question rather than an unbounded environment change.

## Acceptance evidence and decision triggers

| Gate | Required evidence | What does not count |
| --- | --- | --- |
| Toolchain | Version identity, reproducible driver, actual source-to-Wasm compilation | Native clang syntax pass or a handwritten HTML scene |
| Browser runtime | Actual map/model/HUD draw and control in a real browser, console report and feature profile | Successful link alone, native window or streamed video |
| Assets | Explicit transitive manifest, missing-file failure, size report, permission classification | Copying all packages and calling it cleared |
| Input/audio | User-gesture play, pointer escape/reentry, blur releases input, audible basic cue | Forced browser flags masking normal user behavior |
| Network | Two actual browser instances connected to the actual dedicated server, state comparison and bounded queues | Echo server, fixture-only actors or embedded client-local server |
| Delivery | URL load with correct build/asset versions and clear errors, no native installation | Serving a static mockup |
| Final browser readiness | Approved browser/OS matrix and frozen frame/tick/load/network thresholds met | Desktop constants or anecdotal smoothness |

Return to the owner/lead if: essential map/model rendering requires broad renderer replacement; browser integration needs foundational map/simulation replacement; the proposed transport cannot preserve playable latency/session semantics; or the only workable content path distributes assets without permission. Report the concrete failure, affected source and measured consequences. The owner/lead, not a worker, decides engine migration or changes to player-facing scope.

## Remaining uncertainty

No reliable calendar estimate can be derived from this static inspection. Renderer emulation, startup-service coupling and transport behavior must be tested first. The first wave is deliberately limited to reviewable prerequisites and evidence; it is not a commitment to preserving AssaultCube at any cost.
