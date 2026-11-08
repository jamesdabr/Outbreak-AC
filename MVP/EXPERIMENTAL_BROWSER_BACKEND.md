# Experimental browser ENet platform contract

Revision:0.2. Status: APPROVED PLATFORM COMPONENT ONLY under D039 prerequisite2.8 plus D043 prerequisite3.2 to browser foundation/GOVERNANCE/P0 0.5. Individually RELEASED T058 only. Gateway0.2/T057 controls compatible browser extension-offer admission; gameplay interfaces remain draft. Trusted local normal-client feasibility, no public/hostile/malformed ENet/game admission or whole-process memory claim.

## Source and target boundary

New web/transport/enet_websocket.c replaces ONLY enet/unix.c in the future network browser recipe, flag OUTBREAK_NETWORK_CLIENT together with __EMSCRIPTEN__ and !STANDALONE. Implement all genuine platform exports/signatures declared in enet.h468–479 plus initialize/deinitialize/time/address functions, no duplicate core protocol/host/peer/packet routines, patched ENet wire/core constants or Emscripten stream-socket shim. Native and OFFLINE_MAP keep unix.c/their existing recipes. Use existing enet.h/unix.h types unchanged. New headers browsernet.h (C++ lifecycle declarations only) and enet_ws_bridge.h (C bridge declarations/guards/error numbers) are owned solely by T058 initially; future consumer reads them until MAIN records ownership transfer.

## Exact bridge and lifecycle declarations

JS-library addToLibrary exports ob_ws_open/status/send/recv/frame/close plus one approved readiness extension (proposal's six functions cannot otherwise expose pending queue readiness without consuming a message):

```c
int ob_ws_open(void);
int ob_ws_status(int handle);
int ob_ws_send(int handle,const void *bytes,int length);
int ob_ws_recv(int handle,void *bytes,int capacity);
void ob_ws_frame(unsigned frameId);
void ob_ws_close(int handle,int reason);
int ob_ws_readiness(int handle,int conditions);
```

Private $OutbreakWS state dependency explicitly declared by each relevant JS entry. Wasm32 pointer/length/handle/frame arguments i32, void no value. No JS-to-C async callbacks, raw function pointers, Asyncify, worker proxy, embind/global monkey patch or export-all. Snapshot/game diagnostic publication belongs to later lifecycle ticket, not this backend.

C++ browsernet.h guards OUTBREAK_NETWORK_CLIENT + __EMSCRIPTEN__ + !STANDALONE; declare exactly:

```cpp
enum BrowserNetState { BN_IDLE, BN_OPENING, BN_OPEN, BN_JOINING, BN_ACTIVE, BN_CLOSING, BN_FAILED };
enum BrowserNetError { BNE_NONE=0, BNE_BOOT=1, BNE_OPEN=2, BNE_CLOSED=3,
 BNE_TYPE=4, BNE_SIZE=5, BNE_BACKLOG=6, BNE_DEADLINE=7, BNE_TARGET=8,
 BNE_STALE=9, BNE_AUTH=10, BNE_MAP=11, BNE_MILESTONE=12,
 BNE_CAP_CONSUMED=13, BNE_ENET=14, BNE_VISIBILITY=15 };
void browsernet_begin();
void browsernet_frame(unsigned frameId);
BrowserNetState browsernet_state();
int browsernet_error();
void browsernet_close(int reason);
void browsernet_game_observed(unsigned milestone,int cn,int lifeSequence);
```

Declarations only in T058, no new game implementation. Milestones1=SERVINFO,2=SERVINFO_CONTD,3=WELCOME,4=SPAWNSTATE, genuine post-parse observations only. Future client.cpp owns actual host/connpeer creation/JOINING and milestone validation/ACTIVE. Host allocation happens before WS OPEN; actual ENet peer connect/flush begins only after OPEN. Do not add extra setters or implement lifecycle consumers here. C bridge negative statuses use the matching numeric error reasons (private C enum names allowed); status0=opening,1=open,negative=first latched error; status(0) returns latest failed-open reason or BNE_STALE if none. Open returns positive logical handle or-1, never fake OPEN. One boot/open/live socket per page; failed/consumed boot cannot silently reopen, explicit fresh page/Module/boot required.

## Immutable boot and endpoint

Read window.OUTBREAK_NETWORK_BOOT once, plain own-data schema1 object with ONLY schema_version:1, runId:32lowerhex, endpoint:'ws://127.0.0.1:29865/enet', capability:canonical22base64url representing16 bytes. Snapshot validated scalar copies, never retain mutable boot references or use a command parser. Validate unknown/missing/accessor/bad values before WebSocket constructor. Connect URL endpoint+'?cap='+canonical capability, protocol outbreak-enet-dgram.v1, binaryType='arraybuffer'. Require window.location.origin exactlyhttp://127.0.0.1:29866. No DNS/alternate endpoint/automatic retry/refresh/service account/private key. No URL/token/payload logging or exported packet injector. Component mocks may supply a clearly labeled same-origin boot; actual browser harness must really use that loopback origin.

## Real ENet platform behavior

Initialize has no network side effect. socket_create(DATAGRAM) calls ob_ws_open once, returns positive OPENING handle; second live creation fails. Host options/arrays do not send datagrams; C++ future code polls before peer connect. Destroy invalidates generation then closes its real socket once; deinitialize closes backend too. Socket bind/listen/connect/shutdown return-1, accept ENET_SOCKET_NULL; client enet_host_connect is a core operation distinct from socket_connect. Select always-1 without touching fd_set; caller audit proves excluded discovery/select unreachable in single-peer path. Never index fd_set using logical handle.

NONBLOCK1 succeeds; RCVBUF/SNDBUF positive settings acknowledge fixed actual caps, not requested kernel capacity. BROADCAST/other unsupported options fail visibly; current host ignores BROADCAST failure, document it without enabling broadcasts. Numeric address_set_host accepts only127.0.0.1; get_host/ip produces that exact address into sufficient buffer, no DNS. Preserve network-order host and host-order port29863, validate complete target for every send. enet_time_get/time_set use monotonic emscripten_get_now/performance.now uint32 wrapping base, unaffected by prediction pauses, no wall-clock server-time claim.

Send accepts1..65 vectors, validates null/length arithmetic/current memory ranges/overflow and aggregate2..4096; gathers one complete datagram immediately to JS-owned independent bytes. No retained Wasm pointer or cached HEAP view. Actual WS must be OPEN; opening/closed/invalid/backlog/size errors latch first terminal reason and return-1, never0 to imply reliable retry after core removes commands. Positive return is full admitted byte count, not delivery. One WS message per gathered datagram; no envelope/ENet parser/filter/reliability emulation.

Receive dequeues exactly one complete owned ArrayBuffer into current heap/caller vectors with capacity validation and fixed upstream address. Empty or exhausted frame budget returns0 with no message consumed. Short capacity/nonbinary/oversize/stale target latches reason and returns-1; never return truncated prefix. Each async event captures handle+monotonic generation+actual WS object and cannot deliver after invalidation. A stale callback is ignored/counted privately, never damages a current valid generation. Explicit operations on stale handles fail.

socket_wait timeout0 only; ob_ws_readiness accepts ENET_SOCKET_WAIT_SEND1/RECEIVE2 bits and returns requested readiness intersection or negative reason. Receive ready only complete queued message AND remaining frame budget; send ready only OPEN/not terminal/backlog under cap. Unknown condition bits/nonzero timeout fail visibly; clear unavailable bits. Do not consume a datagram merely to test readiness. Error state polls negative, not spin success.

## Frozen bounded component policy

Incoming queue<=64 datagrams AND128KiB, oldest queued item<=500ms. Outbound actual WebSocket.bufferedAmount plus any own pending copies+new bytes<=128KiB; no second unbounded queue. Oldest continuous nonzero outbound backlog<=500ms; this conservative observation is not per-packet delivery acknowledgement. Per direction token buckets256 datagrams/s burst64 and512KiB/s burst128KiB. First violation closes/latches failure, no silent drops to pass. WS OPEN2s deadline, absolute session150s; main ob_ws_frame resets receive quota only for a genuinely new unsigned frame ID: <=32 datagrams AND64KiB across ALL host service/keepalive calls that frame. First callback/message before initial frame cannot bypass budget.

Visibility hidden or frame gap>1000ms latches BNE_VISIBILITY/close with no catch-up; time continues monotonically. Bounded interval/deadline monitoring may close while frame paused, but never calls C/game or mutates player state. Close invalidates generation and clears application admission/queued bytes/application timers and listeners within2s, immediately requests native WebSocket.close once; it cannot force peer/browser readyState CLOSED within2s. Track actual close observation separately, never manufacture CLOSED. At most one bounded retired socket/close observer may remain (no same-page reopen), reporting unobserved closure/timeout at2s; release it on actual close or owned page/context destruction. Cooperative actual CLOSED<=2s is measured; an unresponsive-peer case must report timeout and have the authorized component/runtime supervisor close its OWNED browser context/profile to enforce final network cleanup. Backend logical cleanup is not physical socket release. This close-only observer is exempt from the application-listener cleanup deadline, never forwards data/calls C/game and cannot accumulate multiple sockets. Cleanup idempotent. No more than512 bounded records and8MiB output; overflow fails. No public game/action API or LLM provider integration.

## Verification and permitted execution

Use inspected existing Emscripten7.0.0/Node24.19 exact pins/frozen cache; C gnu11/-fsigned-char, release-O2 and debug-O0/-g as appropriate. Component-only link real ENet core +new C backend/JS library, omit unix.c; standard accepted64MiB initial/2MiB stack/growth, --js-library approved new platform binding flag. Explicit exported test wrappers are permitted only in labeled component outputs, never export-all production. No new ports/deps/downloads or full game/source/build modifications.

First source/signature/caller audit, actual Wasm compile/link release/debug, JS syntax; meaningful extracted JS/mock-WebSocket tests may exercise async events/backlog/close/memory growth/stale generations and queue policy, all labeled simulations. Test real C functions through linked Wasm wrappers where possible; no mirrored ENet parser. Do not feed malformed bytes to real ENet receive parser. Component tests are not multiplayer proof.

After own driver inspection, bounded real browser platform harness is authorized within T058: owned127.0.0.1 static29866 serving only component outputs and synthetic WS29865 (exact T050 ws source/Node env) accepting fixed contract origin/subprotocol. Real native browser WebSocket/real linked backend wrappers exchange2/1400/4096-byte known payloads, scatter/receive bounds and current-heap growth. Those arbitrary component payloads go only through socket wrappers, NOT game/ENet parser. Maxone browser/context/WS, normal Chrome security/no unsafe flags, temporary profile, no external request, native UDP/game/gateway source import/launch. Harness may use a distinct fresh page/boot per independent case; <=20s child/<=30s supervisor per suite, <=5s cleanup. No fixed-port owner => stop, do not kill others/changeports. Record exact Node/vendor/compiler/source/output/browser/driver identities, actual vs simulated outcomes and all owned handle/timer/listener/port cleanup. Additional invocations need new evidence and changed-code rationale. Runtime tools inspected before execution; no unfamiliar execution as discovery.

Acceptance is complete source and honest component evidence, not main app/native multiplayer/P0/authority/production or hard total-memory containment. Unexecuted cases stay NOT RUN; MAIN reviews before accepting/consumer release. Questions stop affected scope only, never tune a frozen bound or add a private API.
