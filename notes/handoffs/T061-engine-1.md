# T061 remote-client source component — frozen submission

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket: T0613.7 RELEASED; network-client contract0.3; backend API0.2; D045/D048/D051 and approved browser foundation/GOVERNANCE/P0 prerequisite subset. Submitted, no self-acceptance/status edit.
- Base commit:13f0d8eea4822dee5c976661218d022be74342e3. Shared pre-existing edits preserved. No commit/push/reset/dispatch.
- Writes: ONLY exact OUTBREAK_NETWORK_CLIENT && __EMSCRIPTEN__ && !STANDALONE regions in client.cpp,clients2c.cpp,clientgame.cpp,packetqueue.cpp; NEW browsernet_observer.h and web/runtime/tests/T061-source/**; this handoff. No main/audio/backend/gateway/build/output/QA/server/asset/contract/ticket edits.
- Final source is frozen. Future correction requires a question/release, not an unrecorded mutation.

## Frozen identities

| Source | SHA-256 |
| --- | --- |
| source/src/client.cpp | 9cad6a9d0acd65dd3c4902ebea805b1a7807bdc55dd31f2f9dcc606b13578183 |
| source/src/clients2c.cpp | 83a57afb6796c8f76fbe496175f0527e51c431a9d06666d29ee10985ba812686 |
| source/src/clientgame.cpp | 6f394da0969de59ab1bfc26c3ca6e535b8e7126457e2dc039676aa5abdcbd6b9 |
| source/src/packetqueue.cpp | c6fe0c9800a52b2afdae6b0e2d94f22eaf051f9f83de0d2670bdb1b5998b806b |
| source/src/browsernet_observer.h | 7c88755861fec0cf5523e9005ee02755cd8a001b49a4be32da73042a5bfd987c |

Evidence root: web/runtime/tests/T061-source/. Exact submitted source/header
copies, source-pins.json, verification.json and SHA256.json are in submission/.
Final actual compile report: compile-attempt-4/report.json. Final extracted
mock report: mocks-attempt-8/report.json. Prior attempts remain unchanged.

## Acceptance evidence

| Criterion | Result and boundary |
| --- | --- |
| Baseline/guard ownership | PASS: all four exact approved baseline hashes checked before mutation and bytes retained in before/. guards-freeze.json proves removing only the exact guarded network branches restores baseline C++ tokens for every file, including protected Outbreak prototype. |
| Native/offline behavior preservation | PASS at source/compile level: actual native and offline Wasm release objects for all4 CPPs; before/after expanded preprocessing equal in all8 comparisons. No native/offline runtime claim. |
| Real Wasm network objects | PASS: all4 CPPs actual release-O2 and debug-O0/-g/-D_DEBUG objects with -DOUTBREAK_NETWORK_CLIENT. Wasm magic/output hashes/logs/toolchain/argv/environment retained. No full client link or main execution. |
| Header/source stability | PASS: full50-entry source/ENet/bridge/config header membership/hashes before/after every final command identical. Current CPP/header inputs match final object/helper pins and retained snapshots. Other worker files were never edited. |
| Six-function lifecycle | IMPLEMENTED; extracted mocks PASS. One consumed boot/host,1 peer/3 channels, OPENING status cannot connect; real status1 then enet_host_connect exact127.0.0.1:29863; genuine CONNECT event peer promoted without destroying its host. No resolver/LAN/auth menu/native connect fallback. Repeated begin and close-before-begin cannot start another session. |
| Ordered native milestones | IMPLEMENTED; extracted mocks PASS. Post-success parser callbacks1/2/3/4, genuine cn/life/map/current-peer checks. No ACTIVE from transport/open/connect/own position. life=-1 before first spawn; later parsed life observation preserved. Protocol/auth/map/parser rejections remain failures. |
| D048 spectator-first control | IMPLEMENTED; extracted mocks PASS. Read-only fourth observer query true only for valid current peer/cn, first3 milestones and server-observed expected map in JOINING, or valid ACTIVE. Early false is side-effect free and does not consume a later request. Ordinary SV_TRYSPAWN uses enet_time_get unsigned elapsed<=1 request/1000ms, no timer/automatic retry/local alive state. |
| ACK before ACTIVE | IMPLEMENTED; extracted mocks PASS. SPAWNSTATE retains native state/weapon/spawn parsing. Guarded ACK builds genuine reliable SV_SPAWN/life/weapon using existing putint/packetbuf, verifies ENet queue admission, flushes and polls backend error before milestone4/ACTIVE. Missing/failed ACK cannot promote ACTIVE. |
| Polling/budget/errors | IMPLEMENTED; extracted mocks PASS.<=64 actual ENet events shared across gets2c/c2skeepalive per new frame ID; ob_ws_frame once per new ID. No recursive gets2c during parser/map keepalive. Negative host_service and void-flush/backend errors latch terminal.15s raw join deadline plus retained native bucket attempts, no reconnect loop. Backend quotas unchanged. |
| No pre-ACTIVE local gameplay | IMPLEMENTED; extracted mocks PASS. updateworld keeps polling/control at lastmillis0 but skips physics/shoot/movement/sleeps/bots/updateoutbreak before ACTIVE/after close. Channel0 positions require ACTIVE; queued/direct channel1 messages use approved control gates. Network outbreakactive=false, editing denied, map/demo/file/vote-map paths blocked before owned handler effects. |
| Packet/logger ownership | IMPLEMENTED; extracted mocks PASS. Every reachable finalized send in the three owned sender CPPs explicitly detaches packetbuf ownership before sendpackettoserv. Unsent referenceCount0 packets destroyed once; failed queue admission terminal. Receive logger owns queued packets; current payload is not separately destroyed. Nested error/log-clear/frame pump cannot free it; cleanup occurs after parser returns. |
| Host/actor cleanup | IMPLEMENTED; extracted mocks PASS. First error wins, no localconnect/localdisconnect/localclienttoserver; clear messages/logger/remotes/peers/host and reset own spectator/cn/default role. Normal reason0 disconnect drains<=2s by monotonic time; failure can clean at frame safe point or after returning from active parser, including shutdown before another main frame. |
| Map revision2 | IMPLEMENTED; extracted mocks PASS. Only exact dev_outbreak_browser/revision2/DM; reported size must match preloaded map before load_world. Negative/incompatible/revision/size error is retained; no fallback/download/empty-world/menu success. Revision1 rejected before mocked load. No T064 data actually loaded or consumed. |
| Remote observation/CDIS | IMPLEMENTED; extracted decoded-receipt mocks PASS. Observe after native decode/overread/client/life-parity checks before collision/smoothing; eye z=decoded foot z+existing eyeheight. Count/timestamp receipts, genuine removal clears remote. Capture departing cn before zapplayer and use captured cn in original hook in this guard only. |
| Snapshot | IMPLEMENTED; actual current EM_JS body with current C++ mock observation PASS in Node. Function property nonwritable; each result a deep-frozen clone. Own prediction and remote parsed receipts distinct, no cap/key/socket/mutable game references/action setter.<=MAXCLIENTS remotes and512 events; overflow terminal without repeated teardown loop. |
| Integrated/native/game proof | NOT RUN: no actual native peer/parser/browser/game/server/network run or full61-unit link. Mock events/decoded values are simulations, not real server milestones. Actual T064 data, genuine native spawn/join, two-browser motion, close, layout/audio/model/performance/authority/P0/MVP remain separate gates. |

## Object/helper execution details

Host Darwin arm64. Emscripten7.0.0/compiler777e6e5db7b4990bcaeb1b9998ed642cc84e6629,
em++ hash33857101ce8e022ca9c427422154a11c21f03e03439ab2baa1690cbbcc829343;
resolved clang-24 hash9a96f4220eefe21e72a4a9a20a88f4d6c26cad1b047cb02b5b22a96bef49c423.
Node24.19.0 hash27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1.
Native /usr/bin/clang++ identity/resolved path recorded. No new dependency,
download, compatibility suppression or linker flag. Same accepted SDL2,
SDL2_image/png,zlib,Vorbis ports and -std=gnu++11/-fsigned-char; task-local
copy of existing frozen cache/ports, compiler temp and Node/clang caches.
EM_FROZEN_CACHE=1; exact clean env/argv in report.

Final compile pass executes32 commands:16 actual object compiles (8 network
Wasm,4 offline Wasm,4 native) plus16 preprocess calls yielding8 equivalent
before/after expanded-source pairs. Every command exit0; no stale header set;
no linked full client. Earlier compile passes also retained, but only attempt4
matches final source.

Mock harness extracts current lifecycle/send/event/logger/map/decoded-position/
CDIS/auth/updateworld source and actual packetbuf cleanup, using explicitly
mocked ENet/platform/game/clock objects and native SV/GMODE enums. It never
injects bytes into genuine ENet/game receive parsers.26 process cases pass,
including nested parser shutdown/payload lifetime,64-event shared cap,15000ms
join/2000ms drain,1-second spectator spawn throttle,failed ACK/ownership,
revision1 rejection and512-event overflow. Current EM_JS getter separately
evaluated against generated C++ mock JSON; no browser or public game setter.

Historical helper attempt1 failed compiling a C++11 mock aggregate constructor;
fixture-only constructor fixed in attempt2. Original report/stderr retained.
Attempts2–8 correspond to changed implementation/approved contracts/regressions,
not identical blind retries. Parser edit helper initially asserted before any
CPP write; corrected before execution. Historical edit helpers are not replay
drivers and must not be rerun against the frozen source.

Commands already executed after inspecting own drivers:

```sh
python3 -B web/runtime/tests/T061-source/check_guards.py
python3 -B web/runtime/tests/T061-source/mocks.py
python3 -B web/runtime/tests/T061-source/compile.py
python3 -B web/runtime/tests/T061-source/finalize.py
git diff --check
```

Final successful outputs are specified above. Compile/mock drivers always
allocate fresh numbered attempts; finalization refuses to overwrite its
verification. These are historical reproduction commands, not authorization
for further execution/mutation after this freeze.

## Lifecycle/interface notes for integration

All six browsernet.h declarations/BN/BNE values unchanged. Observer header
declares exactly three observations plus browsernet_spawn_request_allowed.
Private CPP helpers implement packet detachment/control ACK/parser guard;
there is no new public setter, injector or game action API. Backend logical
close versus physical WebSocket CLOSED semantics remain0.2; BN_CLOSING after
normal client teardown is terminal, not a claim that a browser socket is
physically closed. No in-page fresh boot/reconnect.

packetbuf.finalize() alone retains ownership. Guarded send sites now detach
its packet/buf before calling sendpackettoserv, so rejecting/freeing an unsent
packet cannot cause packetbuf destructor reuse/double-free. The only external
sender site found is editing.cpp/netblockpaste, read-only/outside this scope;
network editmode starts false, allowedittoggle denies entering it, and incoming
edit messages reject before effects, so that editor path is excluded. Full
future caller audit must retain that exclusion or obtain source ownership
before introducing any new sender.

gets2c cannot recursively dispatch while parser depth>0. A nested shutdown
frame only latches pending cleanup; after servertoclient returns, terminal
failure cleanup completes at the safe control point. Normal owner-close0 can
instead drain via future frames up to2s. Player's main loop must keep polling
and JOINING control at lastmillis0, use raw monotonic network time and its
approved50ms prediction clamp, skip initserver/serverslice/local bootstrap,
and use the eligible ordinary spawn gesture/query. These main changes belong
to T062 and are NOT implemented/accepted by T061.

## Exact snapshot schema/counters

window.outbreakNetworkSnapshot() returns schema_version1/profile network-client,
state string BN_IDLE/BN_OPENING/BN_OPEN/BN_JOINING/BN_ACTIVE/BN_CLOSING/BN_FAILED,
numeric error(BNE),map_name/map_revision (empty/0 before successful server map
receipt or after teardown),own{cn,life,state,position[3]},remotes bounded256,
counters,coverage string,events bounded512. own.state is actual CS numeric;
own.position is player1->o at publication. Own life=-1 until actual spawn and
after teardown. Remote entries are{cn,life,position[3],parse_count,last_parse_ms}
with decoded eye-coordinate receipts before prediction; no native clientsequence
or authoritative server cache is exposed.

Counter keys: begin_calls,repeated_begin,frame_calls,frame_advances,ws_frames,
service_calls,game_events,receive_packets,send_queued,send_rejected,
owned_local_attempts,milestones,life_observations,position_receipts,
remove_receipts,map_receipts,join_timeouts,spawn_requests,
spawn_acknowledgments,teardowns. send_queued counts ENet queue admission;
spawn_acknowledgments counts admitted genuine ACK+no latched backend flush
failure, not remote delivery. owned_local_attempts increments at owned no-peer
send/local-receive attempts and does NOT observe main/serverslice paths;
coverage explicitly says those are unobserved. No hardcoded global-local-zero
proof. Event keys kind,milestone,cn,life,error,at_ms; kind0 lifecycle observation,
1 genuine parse milestone/life observation,2 close latch,3 safe teardown.
Timestamps use emscripten_get_now, not prediction time.

## Protected-file evidence and remaining gates

Initial four baseline CPP bytes and protected source-header/output hashes
retained. All17 existing runtime files remain byte-identical. Player's main.cpp
changed concurrently under T062; earlier/new read-only observations retained,
not frozen or consumed as T061 object input. No affected compile header changed.

Evidence limitation disclosed: initial protected manifest mistakenly requested
nonexistent sound.cpp and therefore omitted audiomanager.cpp. sound.h was in
the initial header manifest. Final audio CPP independently matches MAIN's exact
D047 accepted31ea6bc3…477f2d1039 pin and has a read-only byte snapshot; no audio
write occurred. This is an audio baseline evidence correction, not a fabricated
initial snapshot. One finalization attempt also noticed Player main changed
between read-only observations; preserved old and new snapshots rather than
requiring another worker's unrelated source to stay frozen. Owned source and
actual compile/header inputs stayed stable throughout final verification.

No unresolved implementation scope question. MAIN owns review/acceptance and
the future complete source/data pin set, full build and actual runtime. T064
revision2/eight-FFA data is an approved expected interface only here; it was
not loaded/validated or bypassed. Existing revision1 offline/audio/T063 data
unchanged. Native ENet reassembly/untrusted-map debt, actual native parsed
clientsequence/cache, two-browser remote movement/authority, full lifecycle,
audio/layout/model/performance and MVP acceptance remain outside this handoff.
