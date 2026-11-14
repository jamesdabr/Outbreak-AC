# T057 fixed loopback WS/datagram gateway

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket/revision: T057 2.7 RELEASED; submitted for MAIN review, no self-acceptance
- Governing: MVP/EXPERIMENTAL_TRANSPORT.md 0.1, D037 prerequisite2.7, browser foundation/GOVERNANCE/P0 0.5; accepted T050/D033 dependency
- Base commit: 13f0d8eea4822dee5c976661218d022be74342e3. Pre-existing shared-tree edits preserved. No commit/push/reset/dispatch.
- Changed files: NEW web/transport/{gateway.cjs,gateway-limits.cjs}, tests/{run_gateway.py,gateway-component.cjs,gateway-policy.cjs,gateway-mocks.cjs}, results/gateway-T057/** and this handoff only.
- Final gateway SHA-256: `04d4cdf1578c44d535dac40208bffb85c26788cc91e447a6cc0debe05d3f94bc`.
- Final policy SHA-256: `bbc53104cf2b9b87abfcb5711ef830cb2e1180bfda4800d6021ed42363a9a831`.

## Acceptance evidence

Final result: web/transport/results/gateway-T057/attempt-4/result.json, PASS,
exit0, child reaped,2.240674917s,16171 combined output bytes, no watchdog/output
violation. All16 component checks,8 deterministic policy cases and15 actual-
component/mock-socket/fake-clock cases pass. Functional results only; no
performance or game claim. Host Darwin arm64; exact existing Node24.19.0 at
`/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node`, SHA-256
27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1.

| Contract criterion | Result / evidence |
| --- | --- |
| Exact dependency, clean import/config | PASS: supervisor rehashes all19 accepted vendor files and exact Node before child; no dependency changes/npm/addons. Import adds no handles/requests, loads14 ws CJS modules, no .node or fs.close/closeSync patch. Bad/unknown/duplicate-cap config rejected before listen. |
| Fixed API/topology/bytes | PASS: startGateway only; exact TCP127.0.0.1:29865, each session udp4 binds127.0.0.1:0, connects127.0.0.1:29863. Real2/1400/4096 bytes in both directions for A/B, distinct source tuples, exact payload assertions and recorded length/hash/tuple. No ENet parsing/envelope. |
| Admission and token burn | PASS: real wrong/missing/null Origin, wrong Host/version/protocol/extensions/method, duplicate header/query, encoded route, third active session and replay rejected; bad admission allocates no UDP. Correct canonical UTF8-string SHA256 plus both timingSafeEqual comparisons. Invalid RFC key handled by ws, burns reservation, no UDP; later replay rejected. |
| Sessions/retirement/resources | PASS implementation, real active/retired peak2; deterministic/mock limits separately | At most2 active,4 pending TCP,4 reserved retirement positions,6 UDP enforced. Tokens are never refreshed, so only2 lifetime reservations can succeed per configured instance. Retired tuple held60s/discarding in actual component with fake clock; no delayed retired forward. Real abrupt loss retires both tuples. Whole close releases them immediately. |
| HTTP bounds | PASS for four pending TCP/2s deadline/eight-attempt budget in real suite. Fifth TCP refused, four headerless peers expire, ninth upgrade rejected. maxHeaderSize8192 set; oversized-header rejection path source-inspected, not separately exercised. Constant empty403 response then destroy, no content/redirect. |
| WS parser bounds | PASS real text1003,4097client1009,16 nonempty fragments delivered and17client1008 rejected before UDP. Exact frozen maxPayload4096/maxFragments16/maxBufferedChunks32/deflate=false/UTF8validation enabled/autoPong=false/closeTimeout1000 set. maxBufferedChunks rejection/invalid UTF8/masking/empty-frame paths NOT RUN. |
| Direction rate/queue bounds | PASS policy + actual-component mocks:256 packets/s burst64,512KiB/s burst128KiB;65th packet stops before UDP send; UDP64/128KiB pending; WS bufferedAmount+own pending+new bytes<=128KiB. Own copy after checks, no second application queue. Failure/clear/late callbacks release once. Callback failure counts no successful send. |
|500ms backlog and wire accounting | PASS fake clock at499/500ms and callback at500ms before timer dispatch. Raw bucket1MiB/s burst128KiB; full-component mock stops later forward. Real coalesced upgrade+frame measured273 bytes exactly, including8-byte encoded head once. |
| Control/heartbeat/application/session/run | PASS actual-component fake clocks: manual pong8 burst/9th denied; every5s8-byte nonce ping; newer matching pong cannot forgive missing older10s pong;30s application idle;150s absolute session despite application/pongs;180s whole-run close. No wall-clock150/180s run, by bounded-suite design. |
| Diagnostics/redaction | PASS:512 records/component/session bounds; mock513th diagnostic sets failure/stops with original512 retained. Snapshots contain no tokens/URLs/payloads/handles. Driver scans output for owned caps; supervisor8MiB cap. This module emits no logs itself. |
| Lifecycle/cleanup | PASS: idempotent close promise, cloned snapshot counters, close-during-bind race, callback failure and late-generation cases; all six real groups end with0 tracked TCP/UDP handles and0 component timers. Child has0 clients/raw clients/network handles. Parent no-LISTEN lsof exit1/empty plus SO_REUSEADDR TCP bind/close and UDP bind/close succeed. No plain-bind-only conclusion. |
| Frozen inputs/other workers | PASS: all17 runtime files unchanged; vendor, engine/game/audio/build/QA/native server untouched. No external endpoints, credentials, browser, native server or game child launched. |

## Implementation status

Implemented complete component API/resource policy, with no CLI. Public
module import performs no listen/timer/CLI action. Native socket library
callbacks remain asynchronous; a generation/closed guard stops stale data.
Session generation increments on first finish. First terminal reason wins;
later close/error events can attach safe close code/parser enum without
reviving a session. Reserving retirement capacity includes active sessions,
so teardown never needs an unavailable quarantine slot. UDP sockets remain
owned and connected while retired, discarding replies until60s or whole close.

No hand-written frame parser. Raw data accounting is prepended before HTTP/ws
consumption. ws re-emits its upgrade head via unshift; the already-counted
prefix length is excluded from accounting across copied/coalesced chunks,
without removing, inspecting or transforming any data. Initial raw bytes,
including head, are charged once.

One per-session maintenance timer selects the next heartbeat, missing-pong,
idle, absolute-session or oldest-backlog deadline. At most two unanswered
8-byte heartbeat nonces exist before the oldest10s deadline. Each callback
also checks send age and generation, covering delayed timer dispatch. Whole
close stops admission, clears maintenance/retirement/run timers, closes active
and retired UDP, requests WS close, forces remaining owned peers/TCP after1s,
and resolves after all owned HTTP/WS/UDP/TCP completion. No unrelated process
killing. No CLI was added; therefore CLI signal/config-file behavior is NOT
IMPLEMENTED/NOT RUN (optional in0.1); an eventual consumer owns signal wiring
to the exposed normal close path under its separate release.

## API and counter schema

`require('web/transport/gateway.cjs').startGateway(config)` returns a Promise
of `{address, snapshot, close}`. Config must be a plain data object with
exactly schema_version=1,32-lowercase-hex run_id and capability_sha256 array of
two distinct64-lowercase-hex digests. Each digest hashes the canonical22-char
base64url string in UTF8, not its decoded16 bytes. No route/destination/limit
override or implicit file/profile/credential configuration exists.

`address` is `{address:'127.0.0.1',port:29865,family:'IPv4'}`.
`close(reason)` returns the same Promise on repeated calls; arbitrary caller
reason strings are normalized to owner_close, never reflected as credentials.
Known internal run/error reasons are retained in cleanup.reason.

Snapshot schema_version1 includes run_id/address, cloned counters, active,
pending_tcp,retired,udp_total,sessions,diagnostics,failure,cleanup. Each session
has session_id,generation,state,reason,upstream_connected,udp_tuple (or null),
close_code,parser_error (safe whitelist or generic),counters,to_udp/to_ws
pending_sends/pending_bytes,control_pending_bytes and bounded records.
Diagnostics are `{reason,session_id}` only. Cleanup has state,HTTP/WS closed
flags,normalized reason,timers,TCP/UDP handle counts. No mutable internal
references, capabilities or socket handles are returned.

Component counters:

- tcp_accepted/tcp_rejected: tracked accepts versus immediate pending-cap refusal.
- upgrade_attempts: all upgrade events, including denied attempts beyond8.
- admitted: atomic capability/session reservations, including later RFC failure; not proof of completed handshake or usable game session.
- rejected: bounded HTTP rejection decisions; udp_allocated: sockets created after successful library upgrade.
- to_udp_datagrams/bytes and to_ws_datagrams/bytes: successful send callbacks only, also present per session; OS/library completion does not itself prove peer/application delivery.
- retired_discarded: messages ignored after retirement; send_errors: failed send callbacks; late_callbacks: callbacks ignored after generation/close change.
- wire_bytes: unique incoming raw bytes, including headers/head; control_received: public ping+pong events, including a policy-violating event.
- diagnostic_overflow: explicit failure attempts at diagnostic capacity.
- peak_active/peak_pending_tcp/peak_retired/peak_udp: maxima of owned tracked state.

## Reproduction and immutable attempt history

Already executed reviewed supervisor commands from repository root:

```sh
python3 -B web/transport/tests/run_gateway.py --attempt attempt-1 --rationale 'Initial reviewed T057 implementation: real loopback component cases plus explicitly labeled policy and mock-clock regressions.'
python3 -B web/transport/tests/run_gateway.py --attempt attempt-2 --rationale 'Changed reviewed drivers add exact coalesced-upgrade-head wire accounting, remaining admission-header matrix/RFC-key burn and raw-wire stop-before-forward mock; preserve attempt-1.'
python3 -B web/transport/tests/run_gateway.py --attempt attempt-3 --rationale 'Fix attempt-2 demonstrated duplicate upgrade-head wire charging by exact re-emitted prefix length, add numeric observation and immutable input snapshots; rerun changed source/driver only, preserve prior evidence.'
python3 -B web/transport/tests/run_gateway.py --attempt attempt-4 --rationale 'Final changed-source review: enforce every-5s nonce pings with oldest matching-pong deadline, and send-callback age checks before timer dispatch; add full-component fake 150s session test. Preserve attempts 1-3.'
```

Attempt1 PASS on its smaller initial suite. Attempt2 FAIL exposed duplicate
head accounting with the identity-based guard; original result/stdout/stderr
remain unchanged. Attempt3 PASS after exact-prefix correction. Final source
review then corrected ping cadence and callback-age checks; attempt4 PASS on
those exact current hashes. No blind identical retries. Attempts3/4 additionally
retain byte-identical source snapshots; all attempts retain source/tool/vendor
hashes, actual argv/environment, results/stdout/stderr and cleanup evidence.

Each child uses only PATH=/usr/bin:/bin,WS_NO_BUFFER_UTIL=1,
WS_NO_UTF_8_VALIDATE=1,TMPDIR pointing to an owned temporary cwd. Exact paths
are in each report. Supervisor has20s child deadline, owned process-group
termination only on violation, bounded output, child reap, and cleanup within
the30s parent budget. No deadline/output violation occurred. All invocations
were inspected and explicitly within the released fixed-loopback scope.

Final static verification and all evidence hashes are under
results/gateway-T057/final-verification.json and SHA256.json. Current sources
match the actual attempt4 source snapshots. Ticket/contract revisions were
re-read before submission. No unresolved scope question.

## Limitations and next owner

Real byte forwarding uses a clearly labeled synthetic UDP endpoint, not
native ENet or a game. Resource/timer/race assertions are explicitly separate
policy/fake-clock/mock-socket evidence; they are never described as real
network timing or game PASS. No public/hostile service approval, aggregate
RSS/CPU bound, zero-copy/backpressure guarantee, browser backend, reconnect,
authority, real multiplayer or P0/P1/MVP acceptance follows.

maxFragments counts nonempty retained payload buffers, not every wire/control
frame; maxBufferedChunks counts TCP chunks, not bytes. Parser allocation before
message callbacks and empty/control framing semantics remain the accepted
dependency caveats. No floods or system-resource stress performed. Native
ENet1GiB reassembly/untrusted-map debt remains outside this component. MAIN
must review/accept this source and release any consumer/native/browser/game
integration separately. T040 output remains frozen.
