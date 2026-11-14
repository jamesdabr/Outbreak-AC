# T058 browser platform component handoff

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket/revision: T0583.2 RELEASED; approved MVP/EXPERIMENTAL_BROWSER_BACKEND.md0.2, D039 prerequisite2.8 + D043 prerequisite3.2; governing browser foundation/GOVERNANCE/P0 0.5. Re-read ticket/contract before submission; no authoritative status edited.
- Base: 13f0d8eea4822dee5c976661218d022be74342e3, shared tree already dirty. Existing consumer/main/client/core/source/build/vendor/gateway/QA/assets and other workers' files untouched. No commit/push/reset/dispatch.
- New production files only: `web/transport/enet_websocket.c`, `enet_websocket.js`, `enet_ws_bridge.h`, `source/src/browsernet.h`.
- New component code/evidence: `web/transport/tests/backend/T058/**`, `web/transport/results/backend-T058/**`; own close-bound question and this note. Source/header bytes now stable; headers remain T058-owned until MAIN records transfer.

## Acceptance evidence

| Criterion | Result and scope |
|---|---|
| Genuine platform/C ABI and guards | **PASS.** New C unit implements unchanged initialization/time/address and all12 socket/select signatures, compiling against real enet.h/unix.h. Select always returns-1 without dereferencing fd_set. Core host creation uses logical socket/options only; BROADCAST fails deliberately, documented because core ignores its return. Core single-peer create/connect/service/flush calls do not use socketset_select (only excluded serverms path does); protocol.c1862 returns before blocking wait for timeout0. This is a source audit, not whole-game reachability proof. No core parser/host/peer/packet implementation was duplicated. |
| Frozen API surface | **PASS.** Seven exact C/JS bridge exports including ob_ws_readiness; each declares $OutbreakWS dependency. browsernet.h contains exactly approved enums/six lifecycle declarations under the three required guards, no consumer implementation/setter. C/C++ bridge linkage and representative types/error ABI compile; native/offline/standalone exclusions preprocess empty for the new files. Existing headers unchanged. |
| Boot, ownership, limits and lifecycle | **PASS implementation + focused simulated evidence.** Own-data descriptor validation before constructor, fixed origin/endpoint/protocol, canonical capability, one consumed boot, sticky errors, separate generation/WS checks, immediate copied datagrams, heap-range/scatter validation, no async C/game calls or retained Wasm views. Fixed count/byte/rate/deadline/visibility/frame limits and idempotent logical close implemented. Readiness does not consume data. Detailed ownership/counters below. |
| Actual Wasm release/debug component | **PASS final attempt4.** Nine C units each mode (seven real ENet core units + new backend + labeled wrappers), both real links. Frozen Emscripten7.0.0 revision777e6e5db7b4990bcaeb1b9998ed642cc84e6629; gnu11/signed-char, O2 release and O0/g debug;64MiB initial/2MiB stack/growth; --js-library new binding, no unix.c. Explicit test wrappers only; no export-all/Asyncify/embind/proxy/socket shim. Outputs are component-only, not the game. |
| Labeled simulation suite | **PASS11 groups.** `mock-20261108T064242-b141ef97/result.json`: unchanged JS library evaluated with mock WebSocket/clock/heap, not a network or ENet parser. Includes boot/accessors/origin/canonical errors, opening/consumption/sticky errors, readiness/non-consumption/initial quota,32-datagram/64KiB budgets and repeated/stale/wrap frame IDs, independent send copy/current heap replacement, short capacity no-prefix, text/oversize/queue/rate, opening/queue/backlog/frame/hidden/absolute deadlines, stale callbacks/idempotence, and0.2 passive unresponsive close. Report labels simulations explicitly. |
| Actual browser socket-wrapper suite | **PASS6 final checks.** `browser-20261108T064616-da76ed0f/result.json`; actual Chrome156.0.8078.80, Playwright1.62.1, exact Node24.19/ws8.21.0. Both modes exchange known2/1400/4096-byte payloads through genuine scatter-send/scatter-receive C wrappers with real native browser WebSocket and synthetic WS peer; current Wasm heap grows and4096 exchange repeats. Both short-capacity cases return-1/size error with no prefix written. Options/address/time and readiness checked through actual C. Only host allocation/socket wrappers invoked; arbitrary payloads NEVER reach enet_host_service/receive parser/game. |
| Actual close/handshake/cleanup | **PASS narrow0.2 scope.** Four cooperative actual CLOSED measurements6.7–6.9ms. Deliberately paused synthetic peer yields logical cleanup + timeout + one passive observer, actualClosed=false; then supervisor destroys its OWNED context. All five real browser handshakes offer exactly `permessage-deflate; client_max_window_bits`, version13/exact origin/host/protocol; all responses have no extension, Node ws.extensions empty. No request-header rewriting. Final browser/context/profile stopped/removed, zero owned network handles/WS clients, both fixed ports have no LISTEN and SO_REUSEADDR bind/close succeeds with errno recorded. |
| Current identities/preservation | **PASS.** final.json stale=[], real component input/object/output hashes match current files, all19 vendor files and both accepted native binaries unchanged; JS syntax/header/guards/git diff --check pass. No active browser/game artifact overwritten. Concurrent other-owner work is not claimed frozen by this ticket. |

## Exact execution and historical failures

Already executed, not an invitation for an unreviewed repeat:

```text
python3 web/transport/tests/backend/T058/build.py
python3 web/transport/tests/backend/T058/run.py mock
python3 web/transport/tests/backend/T058/run.py browser
python3 web/transport/tests/backend/T058/final.py
```

Drivers inspected before execution; runtime permission escalations approved the exact owned local component actions, no automatic rejection. Node env is PATH=/usr/bin:/bin, WS_NO_BUFFER_UTIL=1, WS_NO_UTF_8_VALIDATE=1 and ticket-local TMPDIR. Parent verifies exact accepted Node SHA27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1,19-file vendor hashes and current compile inputs/outputs. Runtime suite one browser/context/application WS at a time, fresh pages per case; synthetic fixed WS29865 and static29866 only, no UDP/native/game/gateway import or launch. Playwright is the inspected installed automation tool; synthetic WS uses the exact vendored package, not Playwright's internal ws export. Browser chromiumSandbox=true and unsafe default arguments removed; actual argv is retained.

Final child4.033s / parent4.2033s, under20/30s bounds; no watchdog/kill. Browser PID91279 stopped; temp profile removed. Exact scripts/environment/cwd/PIDs/argv/source and served hashes/stdout/stderr/port checks are in reports. Host arm64 macOS26.5.1/Darwin25.5; Python3.11.9; native clang17; compiler/SDK/library hashes in final.json.

Preserved failures, no overwritten evidence:

1. `build-attempt-1.json`: all C compiles passed, default link failed on absent frozen-cache libGL-getprocaddr.a. No dependency installed/cache built. Attempt2 used the project's existing legacy GL cached variant; release linked, debug failed on missing libstubs-debug.a. Attempt3 reused nonasserting runtime libraries (ASSERTIONS=0) and both linked. Debug C remains O0/g; Emscripten runtime assertion instrumentation is not claimed. Attempt4 adds existing safe GL_UNSAFE_OPTS=0 and is current. All old objects/reports preserved.
2. `browser-20261108T064430-62445938/result.json` remains **FAIL**: all six actual wrapper/close/handshake checks passed, but generic console recorder recorded eight errors without text. SDK source suggested two GL initializer warnings; that was an inference, not recovered original text. Changed safe-GL link + recorder produced a fresh final run. Final records five **exact** inherited libglemu.js153 warnings separately, zero unexpected console/page errors. No GL/render call is made by wrappers. The old FAIL is not relabeled PASS; changed-code rationale retained.
3. Close question `notes/questions/T058-AI-Director-browser-close-bound.md` remains verbatim; D043 resolves it via platform0.2. No fabricated socket CLOSED state or hidden force-terminate policy.

## API, counters and ownership for future consumers

`enet_ws_bridge.h`: open/status/send/recv/frame/close/readiness exactly as0.2; private OB_WS_* values0..15 match lifecycle errors. open returns positive opening handle or-1. status0-handle gives failed-open reason, positive current handle reports opening/open/first terminal error. Arbitrary stale handles return stale/error, stale close cannot affect valid state. No new public packet injector/snapshot/lifecycle setter.

Private JS state has one consumed flag, monotonic generation, lastOpenError, one session and scalar staleCallbacks. Session fields: live/error/opened/started/frameId/lastFrame, leftCount/leftBytes, queue/queuedBytes, two token buckets, backlogAt, one application interval, closeTimer/closeHandler, closeObserved/closeDeadlineMissed, scalar sent/received counts. No growing event log/output (zero production output); no token/URL/payload logging. These fields are private implementation diagnostics, not a public snapshot schema for consumers.

Queue holds independent Uint8Array-owned ArrayBuffers, count<=64/bytes<=128KiB; queue bytes removed once on dequeue or logical close. Async handler never reads HEAP or parses game packets. Send gathers on C stack, then JS-owned copy before browser send; no second application outbound queue. Browser bufferedAmount+new size cap128KiB, continuous nonzero backlog observation500ms, not delivery ACK. Per-direction token buckets256/s burst64 and512KiB/s burst128KiB. Receive allowance starts0 and replenishes only for new serial unsigned frame IDs (32/64KiB); duplicate/older IDs cannot refill and wrap works. Current HEAP view reacquired per bridge call. Timeout/hidden/frame gaps close with first sticky reason; network monotonic time is independent.

Logical close invalidates first, clears data/application interval/listeners, requests browser close once, and retains at most one passive close observer/retired socket. At2s it records missed actual close and clears the timer, retaining only passive observer until actual event or page destruction; cooperative event releases it/WS reference. No same-page retry. Actual closure is separate from status/logical teardown; fixture-only t_observe_close exposes bits for testing, never added to production headers.

## Limits and integration boundary

**NOT RUN:** real ENet peer negotiation/receive parsing, native UDP gateway, native server, game/browser main/client consumers, genuine multiplayer, authority, P0/P1/MVP, whole-process/hostile memory safety or packet capture. Existing1GiB fragment exposure/untrusted-map debt remains. No malformed ENet injected. Browser platform peer connection must only start after status OPEN in the separately released consumer; declarations alone do not implement JOINING/ACTIVE or guarantee future discovery/UI paths are disabled. Not every invalid C pointer/vector combination was dynamically exercised; range/error checks also have source/compile evidence. Most adversarial deadlines/rate/queue/visibility cases are explicitly simulations, not browser stress measurements.

No new production dependencies; frozen cache/compiler only. Existing GL library initializer warning is artifact-link noise, not renderer evidence. Actual context destruction + browser/synthetic-peer cleanup bounds this component; no universal browser socket force-close guarantee is claimed. MAIN reviews before accepting/consumer release; no further browser invocation needed absent a concrete new issue/release.

## Stable identities

| File | SHA256 |
|---|---|
| web/transport/enet_websocket.c | 5d386d859e7178e9777de130ac399da26a015f51b78f78d4bcaee86ecfbac053 |
| web/transport/enet_websocket.js | ce706fd7b8e2ce583d15483ef122b35f91bc48d14f58af6495994c69c6180d34 |
| web/transport/enet_ws_bridge.h | c1905aef1a57b0f599d2e176d90c1e8786fbfea5caf9ec12a8c36f3f7840b832 |
| source/src/browsernet.h | 0a7f522f26d6a29c1956e15a69d601e481790d69091071622f9db73c759e6b44 |

Current component artifacts in `web/transport/results/backend-T058/build-4/`:

- release/component.mjs `1c17213a8340a9bc8a914ce4a40250bc3c8bd05bb008cf5dedd47772f2f15c6b`
- release/component.wasm `822c9697bd3aef0f8cdf5dac5592597c28eb07f26020b86938227c30bffe55d8`
- debug/component.mjs `ce99d35e19c9c668c6f61b648187bf3b2152f052bf57b21f8cec2f0f2ff6a9eb`
- debug/component.wasm `554e186678fa3de49f7094ba1f49c26f02975b6303b92a38b29e3c25ccdf8b1b`

Evidence SHA256, under `web/transport/results/backend-T058/`:

- build.json / build-attempt-4.json: `58bc4f437f8624e0611a9c5ef8b09608ad1a0fcf643b48242422b34dd91538ff`
- mock-20261108T064242-b141ef97/result.json: `24b41367fe3d3e860bb0eaa47a5893f7f6d07b44e8c92866baeb45ced9898685`
- final browser result: `86df4e40cbfe530c2fe30612db562615f6435736eb2815e08a1fb821f88c3079`
- preserved first browser FAIL: `7153880fefe65a2300aa1918385c25e204ea3f7eb143d8f0d3c3500453540eac`
- final.json: `000bc5b982d0624a8834ab60d267fb4d121b101839185d6f41c897de3add8626`
