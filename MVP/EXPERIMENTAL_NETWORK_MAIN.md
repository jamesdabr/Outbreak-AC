# Experimental remote-client main wiring

Revision:0.1. Status: APPROVED SOURCE COMPONENT under D049 prerequisite3.5/browser foundation,GOVERNANCE,P0 0.5, T062 only. Approved platform0.2 and client0.2 interfaces consumed read-only. Actual T061 implementation pending. Main/audio baseline T059 source accepted D047; no full game link/native traffic under this source ticket.

## Exclusive source and profile

main.cpp only exact __EMSCRIPTEN__ && OUTBREAK_NETWORK_CLIENT && !STANDALONE branches for remote bootstrap/frame/timing/diagnostics/shutdown; all native and OFFLINE_MAP token behavior unchanged. Audio/header/other CPP/build/SDK/pack output read-only. Preserve pointer denial/state generation/input lifecycle/audio proof from accepted T059 exactly in nonnetwork profile; network continues to use same real normal gesture and genuine pointer events, no input/state injection or forced spawn.

Use existing accepted original79file profile, map/SDL/GL/fonts/load/scene setup, no models/stock configs/network downloads/account keys. Network startup sets multiplayer GMODE_DEATHMATCH, default role, clientnum=-1 and CS_SPECTATE before any map load. No initserver(false), localconnect/localdisconnect/server slices, bots/listen-server/master/LAN/auth/download path in NETWORK runtime, including cleanup/failure; leave native/offline intact. Retained compiled unused server code may satisfy linker but never executes as multiplayer substitute. Initialize genuine browser platform/normal client/map, then browsernet_begin exactly once after scene initialization/browser start, before scheduling normal frames. Do not directly set connected/cn/life/alive/map-join milestones; genuine parser does that in T061. Map engine rendering readiness is distinct from native join.

## Main frame and clocks

Raw SDL monotonic elapsed/totalmillis continue, no host clock rewrite. Each frame call browsernet_frame(frame.frames) once per new frame, even while OPENING/JOINING/CLOSING/FAILED and prediction clock0, before game/action handling. NETWORK prediction curtime=min(raw elapsed,50ms) only BN_ACTIVE (server ispaused may zero it); otherwise0. No gamespeed/paused-client/demo skip scaling or retained local-server delta. lastmillis advances only this prediction amount; not authority/server time. OFFLINE_MAP browserlocalelapsed250ms/reset-delta unchanged.

Call network updateworld even when lastmillis==0 so real gets2c/control can progress to WELCOME/SPAWNSTATE; the old if(lastmillis) gate is not sufficient. T061 owns early non-ACTIVE simulation gate and native parser/control polling, including D048 ordinary spawn request eligibility. checkinput still uses real focus/visibility/pointer lifecycle, no automatic rearm/input. After network frame has failed/closed do not simulate/send normal actions even if raw time advances. Network ready-to-play cannot be asserted solely from WS OPEN or rendered frames.

No serverslice call in NETWORK frame. Existing entry gesture's tryrespawn remains an ordinary request subject to T061 eligibility, never forced alive. Preserve handshake/control polling before ACTIVE, finite yielding browser loop and no blocking waits.

## Read-only diagnostics

Preserve original OUTBREAK_DIAGNOSTICS schema1+fields/behavior exactly in OFFLINE_MAP. NETWORK variant has same shape with profile:'network-client', engine phase/frame/map/position/input/runtimeerrors; its running means rendered expected scene only, not native join. Keep real global error/unhandledrejection observer behavior, request-specific expected denials handled by T059, no broad filtering. Private guarded emitter/conditional duplication allowed to preserve old tokens.

Additional frozen window.OUTBREAK_NETWORK_TIMING schema_version1 snapshot: raw_elapsed_ms (actual nonnegative raw frame), prediction_elapsed_ms (actual chosen0..50), frame_id (actual main frame id), lifecycle_state (actual BN numeric), embedded_server_path_compiled:false. Publish immutable/nonwritable/no mutable game refs/no action API, bound errors via existing observer. Last field is a labeled compile-profile fact, not a fabricated runtime call count. T061's window.outbreakNetworkSnapshot remains source-owned there; do not overwrite/reimplement it or add fake zero counters for main/server calls. Actual native/cross-client proof remains separate.

## Safe stop and evidence

On browserstop/explicit shutdown request terminal BNE_CLOSED through existing browsernet_close and one final safe lifecycle pump if required, before canceling loop, without blocking/draining synchronously2s. Respect T061 parser-active deferral: never destroy host/current packet from a nested parser; coordinate any missing safe public operation through a question, no new API/private-state poke. Raw browser close remains0.2 logical-vs-physical observation contract, final owned context teardown belongs supervisor. Preserve normal browser audio cleanup and pointer invalidation; no SDK patch.

Acceptance SOURCE: actual native/OFFLINE_MAP preprocessing-token equivalence; actual main.cpp Wasm release/debug objects in NETWORK and OFFLINE modes, unchanged approved SDK/ports/safe profile/task-local cache. New network macro already approved; no additional symbols/flag/error stubs/fullclient link. Focused extracted main bootstrap/frame tests label fake external calls; verify before-join totalmillis progresses/curtime0/network poll+control stillcalled, after-active50ms clamp/no gamespeed scaling, perframe polling, no local init/connect/slices, expected map loader/errors and real gesture path, failure/stop/deferred cleanup ordering, diagnostics labels/frozen timing, offline preserved. Source audit all executable main paths including unreachable native tail under Emscripten return; no hidden native bootstrap fallthrough.

No browser/game/server/network execution, packed artifact mutation, shared main header/API extension, gameplay/camera/model/weapon changes, commits/push/worker dispatch. Source remains frozen after final checks before handoff; later correction question first. Actual full link/network/running game/audio/headed recovery/performance/P0/MVP all NOT RUN until integrated accepted pins/runtime release.
