# D005 Integrating the browser foundation toward the active MVP goal

Authority: human owner set the continuing goal to keep creating and assigning worker work until the eight-player browser MVP is achieved. MAIN continues to own contracts, technical decisions, acceptance and integration. The full MVP scope is unchanged.

## Review

Accept T022 as completed inspect-first SDK planning, T023 as static selected-map inventory, and T024 as real-browser diagnostic fixture work. T023's 29 tests were independently rerun; all 16 SDK inspected-file hashes match the captured report. Accept neither fixture results nor inventory as a playable game. T016/T017/T025 retain incomplete Wasm/runtime requirements. T025 additionally requires actual local rejection cleanup rather than a diagnostic-only call that ignores ST_LOCAL.

## Exact SDK execution authorization

The toolchain is now inspected development tooling necessary within the active project workflow, not an unknown job or another project/service. Authorize T026 to execute the exact bounded local acquisition/install/activation and object probes proposed in web/build/sdk-inspection/REPORT.md, using manager commit 1693ce7359fc9694f198694f902a2cc061239b86, SDK 7.0.0/build 6afbd83493d647051772d491124187d4e9a0cda9 and compiler source 777e6e5db7b4990bcaeb1b9998ed642cc84e6629. This approval is the lead's scoped implementation decision under the owner's continuing build goal; it does not authorize global installs or unrelated systems.

The two exact binary downloads are the mac/6afbd83493d647051772d491124187d4e9a0cda9/wasm-binaries-arm64.tar.xz and deps/node-v24.19.0-darwin-arm64.tar.gz URLs under https://storage.googleapis.com/webassembly/emscripten-releases-builds/. Validate paths/links and record measured hashes before extraction/execution; the manifest provides no publisher checksum and no stronger provenance may be claimed. Copy the previously inspected manager into a fresh /private/tmp/outbreak-web-sdk. Run only explicit component install and local activate commands from REPORT, bypass full SDK meta-package/npm/bootstrap/update/shell profile hooks. Inspect generated config, installed sources/wrappers/recipes/node_modules before compiler execution. The five SHA-512-pinned SDL2, SDL2_image, zlib, Vorbis/Ogg ports in sources-and-artifacts.json may be fetched/built on first use with the report's exact hosts/paths. No additional ports/formats are implicitly approved.

All SDK/config/download writes stay in /private/tmp/outbreak-web-sdk; cache/ports/node cache in web/build/.cache; objects/log/tmp in web/build/generated. No system/user configuration changes, project credential use, other repository jobs, public deployment or database access. Normal network/sandbox approval tools may be used for these exact authorized operations; do not bypass a policy rejection.

## Browser proof profile

Select a minimal original OFFLINE_MAP profile, rather than executing the full inherited menus/docs/autostarts. Retain real client geometry, movement, collision, render, input and bounded local handshake/simulation. No bots, public discovery, native HTTP/autodownload/auth directory, external URI handlers or host profile writes. This is the first rendering proof, not production multiplayer.

Use an original/generated pack rooted at web/assets/original/pack-root, mounted as /outbreak. Canonical paths: config/browser.cfg, config/font.cfg, packages/outbreak/fallback.png, packages/outbreak/font.png, packages/maps/dev_outbreak_browser.cgz and its .cfg. T027 may include other original paths for proven literal bootstrap dependencies. No inherited stock media or native config bundle is included by default. Authored placeholder assets are acceptable for the greybox MVP and must be documented separately from upstream source notices. No geometry/asset engine migration is approved.

Browser proof render may initially omit HUD weapon/local character models and audio while their exact runtime assets/backends are completed; label these omissions in diagnostics. T014/P1/MVP acceptance must still meet their actual required features. These are partial build steps, not waived final criteria.

## Read-only diagnostics contract for QA

T028 publishes window.OUTBREAK_DIAGNOSTICS after actual lifecycle events with schema_version=1, profile='offline-map', phase loading/running/error/stopped, frame_count, rendered_frame_count, map_name, player_position=[x,y,z], input_locked, and runtime_errors array. rendered_frame_count advances only after a real gl_drawframe returns. Use the original map identifier dev_outbreak_browser. Diagnostics never grant state/actions. This is developer observation for the browser proof, not the deferred LLM tester API.

T030 consumes that schema and the explicit web/build/out artifact root/build identity supplied when built. Test yielding frames, actual map identity, fresh-input motion/collision and pointer/focus lifecycle. Distinguish unavailable/missing real artifact as NOT RUN. Fixtures may test harness failure paths only and never satisfy T014.

## Local auth rejection and service policy

T029 finishes T025 before broader service guards: a rejected current ST_LOCAL request must be deleted then call existing disconnect(1,0), which clears local client state without localconnect fallback. Remote current requests use existing DISC_AUTH disconnect; stale jobs do not disconnect a reused client. Queue ownership and absence of continuation must be tested. Native/standalone behavior remains unchanged.

For the single-thread browser offline profile, counted semaphores may preserve acquire/release semantics only when immediately available. Any wait that would block must fail loudly; timed/try waits return truthful unavailability. Thread creation and sleep cannot claim success; excluded native service entry points report unavailable. No blanket no-op successful shim. Stop any hidden background service rather than silently treating it as started.

## Ownership and gates

T026 Engine: SDK/build driver and platform.h/tools.h compile compatibility. T027 World: original pack/generator/manifest. T028 player: main.cpp minimal startup/diagnostics. T029 AI: server.cpp local auth, tools.cpp single-thread primitives, serverms.cpp/http.cpp/serverbrowser.cpp/autodownload.cpp/crypto.cpp native service guards and rendergl.cpp waypoint-think guard only. T030 QA: actual-game observer under web/qa. No overlapping source edits. Exact tickets bound changes further.

No full P0, native/browser multiplayer or gameplay phase is accepted here. The engine/transport selection remains an evidence gate. Continue toward the full eight-player MVP, with LLM testing requirement preserved; do not redefine completion as an offline or fixture-only demo.
