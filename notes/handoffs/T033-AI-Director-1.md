# Ticket handoff

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket / revision: T033 / 0.6 RELEASED; no status change by worker
- Phase / contract revisions: BROWSER_FOUNDATION/GOVERNANCE/P0 0.5 with D006 approved execution addendum 0.6; D008 exact header amendment and D008-stable-debug-header.md accepted input
- Base commit: 13f0d8eea4822dee5c976661218d022be74342e3 plus D006-baseline.json dirty source and accepted Engine-owned tools.h update
- Changed files: new web/server/build_native.py, verify_native.py, LOOPBACK_PROPOSAL.md, build-report.json, verification.json, release-symbols.txt, debug-symbols.txt; out/release and out/debug contain real binaries, objects, dependency files and compile/link logs; attempt-1 preserves initial release success/debug failure evidence. New question notes/questions/T033-AI-Director-arm64-debug-assert.md was resolved by subsequent D008/stable-header decision; it remains historical and was not rewritten. This new handoff is the only T033 handoff.
- Source/other outputs: read-only. No source, contract, ticket, decision, existing build driver, native binary or browser artifact was edited by this worker. No commit/push/branch/reset/revert.

## Implementation status

Implemented: an inspected explicit native build driver using the actual eight STANDALONE SERVER_OBJS and eight Unix ENet C units, plus artifact/dependency inspection and a later loopback-launch proposal. Final release and debug executables both compile/link successfully as actual Mach-O arm64 binaries. Neither executable was run, including help/version requests. No socket/listener/server, master/auth operation, config script, download, installer or global/system setup was executed.

Simulations/helpers: none substitute for the server or ENet. The actual upstream standalone `localservertoclient` definition remains as existing native server source; no new fake network/game function was supplied. Inspection scripts read signatures/symbols/dependencies only. Prior Engine assertion fixtures are separate evidence for the accepted header fix, not a T033 server runtime test.

Incomplete: real process startup, loader execution, bound addresses, client join, authentication, map/server state, traffic and shutdown remain NOT RUN. This ticket does not establish multiplayer/browser readiness or accept P0.

## Acceptance evidence

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1 actual server/ENet source inventory and fresh separate objects | PASS | build-report.json derives SERVER_OBJS from source/src/Makefile and ENet from source/enet/Makefile.am; Unix excludes the separately platform-guarded win32.c. Eight real C++ and eight C units compile per mode, no prebuilt ENet archive or dummy socket/server definitions. Complete compile/link argv and hashes saved. |
| 2 installed native tools and compatible dependencies | PASS (inspection/link) | Apple clang 17, macOS SDK 15.5, system zlib/pthread/libSystem and repository SDL2 framework. platform.h selects AC_USE_SDL_THREADS on Apple even for STANDALONE, so SDL2 is actually required. file/otool verify arm64 slices in SDL2 and its nested hidapi dependency; actual SDK/header/library hashes recorded. No dependency was installed/downloaded. Dynamic loader execution remains NOT RUN. |
| 3 real release/debug executables under isolated output | PASS (build) | out/release/ac_server and out/debug/ac_server: 32 final compile commands and both link commands exit 0. Both file signatures are Mach-O 64-bit executable arm64. Initial debug failure was fixed exclusively by Engine under D008; all objects were rebuilt after stable header approval. |
| 4 exact identity/hashes/dependencies/staleness | PASS | build-report.json pins commit/dirty status, all source/header inputs, system SDK libraries/header hashes, framework binaries, every consumed compiler dependency, object signatures/hashes, complete tool argv and diagnostics. Final input_changes=[] and used_input_changes=[]. verify_native.py validates current dependency/object/binary hashes against that build. |
| 5 preserve other outputs and no launches | PASS (build scope) | Before/after hashes for existing source/native/bin_unix/browser output are equal. All writes are web/server or ticket-specific temporary context reads. Only compiler/linker and file/otool/nm inspection tools ran; no resulting executable/config/script was invoked. Runtime and real clients NOT RUN. |
| 6 bounded later loopback proposal and side-effect inventory | PASS (proposal only) | web/server/LOOPBACK_PROPOSAL.md traces actual argument/config parsing, three intended loopback binds, master/DNS/syslog, directories/logs/vita/demo/entropy and real native workers; gives a 15-second owned-process proposal and stop conditions. No launch permission is inferred. |

## Outputs and identity

| Artifact | SHA-256 |
| --- | --- |
| web/server/out/release/ac_server | 296601782e7ff1510b5c9900548bad34c28c97a73d9d571b4d5037c88a9e6005 |
| web/server/out/debug/ac_server | eb2b0c7f9cf75173319dddfa300ec1d54d0c8936426d05de5abfbf776280890a |
| accepted source/src/tools.h input | e53d32d55e5b81ac5e5be3e8a2411a8363dae858631f06cfd3ed11b16eef6fcf |

Host: macOS 26.5.1 / Darwin 25.5.0 arm64. Apple clang 17.0.0 (clang-1700.0.13.5), target arm64-apple-darwin25.5.0. xcrun-selected tools /Library/Developer/CommandLineTools/usr/bin/clang and clang++; SDK /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk, version 15.5. Exact identity outputs, framework file/load commands and full source/dependency hashes are in build-report.json; final independent dependency/binary integrity is in verification.json.

Actual C++ sources: crypto.cpp, log.cpp, protocol.cpp, serverms.cpp, server.cpp, stream.cpp, tools.cpp, wizard.cpp. Actual C sources: callbacks.c, compress.c, host.c, list.c, packet.c, peer.c, protocol.c, unix.c from source/enet. ENet's Unix source explicitly configures Apple socket/fcntl/inet/socklen support; no configure script was run.

Each C++ source is compiled `-DSTANDALONE -std=gnu++11 -arch arm64 -isysroot <SDK> -fsigned-char`; C uses `-std=gnu99` and actual ENet headers, without STANDALONE. Release uses `-O3 -fomit-frame-pointer`, debug `-O0 -g -D_DEBUG`. Release follows the actual Makefile optimizer choice; debug explicitly preserves unoptimized code and assertions rather than relying on the inherited Makefile's later CXXFLAGS overwrite. No assertion suppression or false __EMSCRIPTEN__ define was used for native compilation.

Link includes all 16 fresh mode-specific objects and `-framework SDL2 -lz -lpthread`. macOS pthread is supplied by libSystem; the SDK libpthread.tbd resolves there. The inherited non-mac Makefile `-lrt` was not copied: macOS supplies clock/system functionality through its system runtime. No source or validation semantics were changed to achieve linkage. Full exact argv is recorded, including two repository-local rpaths for SDL2 and its nested hidapi.framework. This is a checkout-local developer build, not a relocatable server package.

Both executables' otool -L list repository `@rpath/SDL2.framework/Versions/A/SDL2`, system libz.1, libSystem.B and libc++. SDL2 and nested hidapi are universal binaries containing arm64, and all their inspected system dependencies/load commands are saved. file validates each object as native arm64. nm verifies actual `_main`, `_enet_host_create` and real serverslice symbols in both binaries (release-symbols.txt and debug-symbols.txt). No binary was executed to inspect it.

## Commands and source-failure resolution

Reproduction from repository root, after the exact approved header/dependencies are present:

```sh
python3 web/server/build_native.py
python3 web/server/verify_native.py
file web/server/out/release/ac_server web/server/out/debug/ac_server
otool -L web/server/out/release/ac_server
otool -L web/server/out/debug/ac_server
```

Final driver and verifier exit 0. The driver records all 32 actual compile argv, dependency files via -MD/-MF, 2 link argv and their logs under out/<mode>/*.compile.log and link.log; no Make/configure/install hooks are executed. Drivers were read before running. Environment contains only bounded PATH, TMPDIR and CLANG_MODULE_CACHE_PATH in web/server/tmp. No user shell/profile setup or DYLD search override is used.

Initial attempt linked the real release server, but every C++ debug unit failed assembling tools.h's native `asm("int $3")` on arm64. This was measured code generation, not a library guess. Question T033-AI-Director-arm64-debug-assert.md reported exact diagnostics; no source workaround was attempted. MAIN approved D008 and its exclusive Engine owner supplied the architecture-correct builtin trap header, reviewed with native ARM brk/x86 int3 fixtures. MAIN relayed its stable SHA and authorized the rebuild. attempt-1 preserves that initial report/log/binary evidence; final out/build-report reflect the subsequent clean build.

The final driver deletes only its own prior objects/executables and recompiles **all 32 objects**, including every header consumer and ENet, before linking both modes. Final source/header input hashes remain unchanged during the build, so no stale units remain. verify_native.py checks actual compiler dependencies again before handoff; unrelated browser-only source edits are not treated as standalone dependencies. No native source/header fix was made by this worker.

## Launch proposal summary

Full unexecuted proposal is web/server/LOOPBACK_PROPOSAL.md. It requires a future released runtime ticket, fresh isolated cwd and reviewed configs/map bytes, a supervisor owning only the child PID/process group and a 15-second cap. Proposed `-i127.0.0.1 -f29863 -c1 -LS5 -LF5` selects game UDP 29863, info UDP 29864 and fixed LAN-info UDP 28762, all intended loopback. All three must be checked; -f does not relocate LAN-info. A resolution failure/wildcard bind is a hard stop.

Do not pass -m, -Y, -C or service arguments or import native/user configs. Default master=NULL and private-key option absent keep registration disabled, but capture actual traffic in that later scope. Native syslog can otherwise create UDP localhost/514 traffic; disable it before logging initialization. File logs, map reader/mode logs, debug docs, servervita backups/updates, demo files and private/entropy.dat must remain inside sandbox paths. Native workers/atexit/signal shutdown are real runtime behavior to verify, not stubbed services. No client-profile writes are called by standalone main, but relative file IO still exists.

This proposal is not a launched listener, approved account/authentication change, browser transport or two-client proof. In particular, no help command was run because standalone main would enter the server.

## Integration and outstanding work

All T033 build/inspection/proposal work is complete within its allowlist. The source blocker question was resolved by accepted D008-stable-debug-header evidence; historical note remains unchanged. No new concrete blocker remains for this build-only ticket.

Before future runtime use, freeze the selected binary/config/map hashes and address/traffic/file policy, then separately release real process/client tests. Loader startup, actual thread behavior, server authority, maps/collision/gameplay and real network joins remain NOT RUN. No browser, P0 or MVP readiness is claimed. Only MAIN accepts this ticket's authoritative status.
