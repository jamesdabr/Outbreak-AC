# T045 real standalone worker lifecycle — build/helper handoff

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket: T045 revision 1.8 RELEASED; D023 additive1.8; governing browser foundation/GOVERNANCE/P0 revision 0.5. Re-read T045 and D023 before submission; no authoritative status changed.
- Base commit: `13f0d8eea4822dee5c976661218d022be74342e3`. Shared tree was already dirty; full initial status and inputs are in build-report.json. Preserved previous browser guards and unrelated work. No commit, branch operation, push, worker dispatch, service or browser launch.
- Changed source: STANDALONE lifecycle regions in `source/src/server.cpp`, `serverfiles.h`, `log.cpp`; STANDALONE atomic completion fields in `tools.cpp`; NEW `source/src/serverlifecycle.h`. No protos.h/tools.h edits.
- New owned artifacts: `web/server/lifecycle/**` (drivers, before snapshots, real-worker fixture, reports, isolated helper directories, target objects/preprocessed evidence); `web/server/out-lifecycle/{release,debug}/**` real native objects/binaries/logs; this handoff.
- Source/header bytes are now stable. D028's independently reviewed non-STANDALONE boundary remains the same; no subsequent source fix was needed during helpers.

## Acceptance evidence

1. **PASS source implementation / NOT RUN full native server shutdown.** Signal handler only reads/writes a `volatile sig_atomic_t` request and returns. Main observes it and performs cleanup. Map/config/demo/auth handles are retained; producer stop is atomic, semaphore waits are explicitly woken, true atomic completion is polled and each real handle joined once. Main transfers log buffers while waiting. After producers finish, owned results are cancelled, logger drains/stops/joins, then sinks, host/service and dynamic semaphores close. Repeated cleanup is a no-op. No fake completion, abrupt exit shortcut or disabled worker. Normal SIGINT return is success; other recorded termination signals return failure. Worker-fatal limitation below is unresolved, not covered by this PASS.

2. **PASS controlled helper scope.** `python3 web/server/lifecycle/test_workers.py` compiles the actual server.cpp worker/controller implementation into an isolated fixture and links the other real native server/ENet objects. Eleven cases exit0: empty, partial, idle, map-dropbox, auth-cancel, auth-inflight, auth-consumed-alias, config-vita, demo-finish, demo-discard, logger-full. Repeated cleanup and logger stop are checked in each case. Idle uses all real worker functions and logger; dropbox case executes real updateservermap while occupied. Actual deferred worker computes an unapplied no-auth result; cancellation uses deliberately invalid client IDs without effects/client dereferences. Actual config worker completes an owned empty vita save. Actual demo worker compresses/finalizes buffered data or discards a short recording under existing policy. Logging fixture supplies a controlled finite producer to the real queue/logger: it blocks at 31 records, main cleanup unblocks it, all 256 records appear before exit. This synthetic producer is explicitly a fixture, not a replacement production worker. No native main/initserver/ENet host/listener is called. Commands, outputs and per-case directories: `web/server/lifecycle/worker-tests.json` and each helper-run observer.json. Case watchdog is 5 seconds; no timeout occurred.

3. **PASS builds, identities and preservation.** `python3 web/server/lifecycle/build.py`: all 32 genuine C/C++ compilation commands and both full native links pass; no input changes, no used-input changes, old outputs preserved. Host arm64 macOS26.5.1/Darwin25.5; Apple clang17; SDK15.5. Release O3/fomit-frame-pointer and debug O0/g/_DEBUG, signed char and gnu++11/gnu99. Copied accepted SDL2/hidapi dependencies verify unchanged signatures/hashes. Native binaries contain only copied dependency rpaths (`web/server/deps-signed`, its nested SDL2 Frameworks); system zlib/libSystem/libc++ remain system loads. Real object hashes, compile dependency hashes, commands, logs, binary load commands and SDK identities are in build-report.json.

   `python3 web/server/lifecycle/verify_guards.py`: six actual wasm32 objects pass, release O2 and debug O0/g/_DEBUG for server.cpp/log.cpp/tools.cpp. Existing Emscripten7.0.0 revision777e6e5db7b4990bcaeb1b9998ed642cc84e6629, existing selected ports, EM_FROZEN_CACHE=1; no downloads/new dependencies. Release preprocessing compares token streams against pre-T045 snapshots (including baseline serverfiles.h): all three modules equal for browser and native embedded-client. Original framework headers are read only for native-client preprocessing; they are not linked. Target commands, diagnostics, preprocessed files, object/source hashes and environment are in guard-verification.json. Debug compilation passes; exact debug token equality is not claimed because physical line movement changes diagnostic line constants.

4. **PASS identity/handoff scope / NOT RUN actual startup rerun.** `python3 web/server/lifecycle/verify_final.py`: pass=true; current dependency/source hashes match build records, no stale build inputs, no prior outputs changed, both binaries verify codesign, git diff --check passes. Exact source/API and candidate binary identities below. MAIN must review and pin a candidate before any separately authorized same-policy bounded real server run. This handoff does not claim multiplayer, authority, P0/MVP or crash-resolution runtime acceptance.

## Ownership and implementation status

Before stop, the main thread marks the active demo via existing enddemorecord (including minimum-duration policy), then release-publishes producer stop under a private publication mutex. The map worker deletes any not-yet-published result on stop. Map/auth publication shares the stop boundary; nothing publishes after it. Only after joins does main delete the published pending map, completed owned auth result and remaining queue entries. Auth's false-done borrowed alias is nulled without a second delete. No client result is applied during cancellation.

Config finishes an existing owned vita save using its existing write/backup policy; unstarted config reload/update work is cancelled at boundaries. If a vita snapshot exists without a completing config worker, cleanup explicitly logs cancellation and frees it. Buffered config/update data is freed after joins. Demo runs a final full pass after stop, so finite queued compression and finalization complete under existing save/discard rules. Logger uses a separate stop flag and exits only after queued records drain, after all producers joined.

New header's entire guarded public surface is exactly:

```cpp
#ifdef STANDALONE
bool serverworkersstopping();
void stopserverlogworker();
#endif
```

All other new lifecycle state/helpers are private. No dependency, protocol, gameplay, movement, balance or asset change.

## Limits and pending review

- Full native server startup/shutdown with this candidate is **NOT RUN**, per T045. Prior T036/T043 failures remain immutable.
- Fatal-from-worker is explicitly unsupported: cleanup reports that it cannot self-join and returns; the existing fatal caller may still exit the process unsafely. No new worker fatal/abort policy was invented. Full crash-signal handling is not claimed safe.
- Partial fixtures exercise absent/not-started handles, not forced SDL/POSIX creation failure. Existing sl_createthread wrapper failure behavior is unchanged; in particular an SDL creation failure can leave a non-null wrapper with done=false and therefore prevent cooperative cleanup completion. Changing wrapper failure policy exceeds tools.cpp's atomic-visibility allowance and needs separate scope if required.
- Existing normal-operation volatile queues/flags are not broadly converted to a new concurrency design. New stop/publication/completion ordering is scoped to shutdown. No TSAN/stress/platform-matrix claim.
- Persistence remains best effort under existing policies: config-vita fixture tests an empty snapshot, demo fixtures do not test a disk save, and no disk-full, write-error, fsync, blocked filesystem or cryptographic-auth stress behavior is claimed. Cooperative joins can wait for real in-flight filesystem/crypto work.

## Stable identities

SHA-256 of current source/header:

| Path | SHA-256 |
|---|---|
| source/src/server.cpp | 51c1423c76d83ab36d42e3fca376792d96d194979c2aec7bc502a723edffcb48 |
| source/src/serverfiles.h | efca26aaefb9d33cc8623bc84dcf06f3a1f10d0b9d9664fff78790dab2bed75f |
| source/src/log.cpp | bf32f817bf970d5c916ab806cea431399228ed076bcd80dd569f307657427a82 |
| source/src/tools.cpp | fe7055c0ce7ac986ff632f22e887de6b621fe85a3d601b6dcbfd6851b724ec5c |
| source/src/serverlifecycle.h | 7084526181078395c64b0bc03dbaaaeea3fa9e41ff1a8dd9ed33f5fa6cb9c8ad |

Candidate binaries, not launched:

- `web/server/out-lifecycle/release/ac_server`: `49a1d28a6251213e27464afb36b6d974215c9886045a38d00a9cfe66befb096a`
- `web/server/out-lifecycle/debug/ac_server`: `df4728a98c5fa1ebc03de88a8549e6dba05a25c4c04310673ded3ba009fa1995`

Report SHA-256:

- build-report.json: `f099c3511d18ab844734a3118daaad77b10366aa9dca0b7a96dfa1da45a470e4`
- guard-verification.json: `333c6f0e1eb705f148f9c8e36deaafd13e0072f98e728ac8f024fc2a5b48a1de`
- worker-tests.json: `efa394bde1bf72ca9bf30f1f39715160c9e03bd54c597e94b4ac9716a801a07a`
- final-verification.json: `15ef0784889fa442c40a31f8eb256bce43c1cce23095cf3a98efa234cf285148`

All report paths are under `web/server/lifecycle/`. Reproduction uses the four Python commands above, in their listed order, from repository root. They rebuild/overwrite only this ticket's owned outputs; they never launch the resulting game server.
