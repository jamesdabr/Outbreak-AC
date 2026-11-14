# T057 3.2 / D043 standard browser offer correction — frozen submission

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket: T0573.2 RELEASED; contract MVP/EXPERIMENTAL_TRANSPORT.md0.2; D043 plus D037/browser foundation/GOVERNANCE/P0 prerequisite subset. Submitted for MAIN review, no self-acceptance.
- Base commit:13f0d8eea4822dee5c976661218d022be74342e3; shared edits preserved, no commit/push/reset/dispatch.
- Current source frozen after final review/test/static hash verification; no further implementation/build/runtime work without release.
- Writes this revision: scoped gateway.cjs and tests/gateway-component.cjs; NEW results/gateway-T057/attempt-{5,6}/**, results/gateway-T057/revision-3.2/** and this handoff. Other T057 source/policy/driver unchanged. No vendor/build/output/game/audio/backend/native/QA edits.

## Accepted contract change implemented

Extension request header is allowed only when absent or exactly
`permessage-deflate; client_max_window_bits`. Duplicate raw headers, duplicate
comma-separated offers, unknown extensions and modified parameters reject
before capability reservation/UDP allocation. ws remains perMessageDeflate=false;
the response never negotiates an extension. Receiver RSV checks remain active.
Safe parser diagnostics now also retain WS_ERR_UNEXPECTED_RSV_1.

No other topology/admission/capability/resource/time/retirement/API changes.
The complete API/counter schema and implementation description in
notes/handoffs/T057-engine-1.md remain applicable **except** its historical
0.1/revision2.7 source hash, blanket extension rejection and old final-result
references, superseded here. That note and all attempts1–4 remain immutable.

## Final identities and acceptance evidence

| File | SHA-256 |
| --- | --- |
| web/transport/gateway.cjs | f70dacb108df16d2f228b866a392927fda61b4e2895fa041ced9f8ab3bb3613e |
| web/transport/gateway-limits.cjs | bbc53104cf2b9b87abfcb5711ef830cb2e1180bfda4800d6021ed42363a9a831 |
| web/transport/tests/gateway-component.cjs | 9da60719b5059bc46199b60f17e851181f0fc077f0f443829c58cf26f46e37a5 |
| web/transport/tests/run_gateway.py | 312ac1ca1527d830c79b5a1a927a72dcfdc8bcaf7c685a5b84d10166e3652055 |

Final executed report: web/transport/results/gateway-T057/attempt-6/result.json.
PASS, child exit0/reaped,2.246705583s,18492 combined output bytes, no deadline
or output violation. Darwin arm64, exact Node24.19.0/hash and all19 accepted
ws8.21.0 files checked by unchanged supervisor. Clean environment is exactly
PATH=/usr/bin:/bin,WS_NO_BUFFER_UTIL=1,WS_NO_UTF_8_VALIDATE=1 and ticket-owned
TMPDIR/cwd; report records actual paths/argv. No npm/addons/dependencies added.

| Criterion | Result | Actual evidence |
| --- | --- | --- |
| Exact standard offer accepted, no negotiation | PASS, Node component client | Actual ClientRequest header recorded as permessage-deflate; client_max_window_bits; response_extensions=null and negotiated_extensions="". Byte-identical2-byte and4096-byte round trips against labeled synthetic UDP endpoint. |
| Unknown/duplicate/modified offers | PASS, real loopback rejection | Four requests: unknown name, repeated comma-list offer, duplicate header lines and client_max_window_bits=12. All rejected; admitted=0/udp_allocated=0 before subsequent valid request. |
| No compressed/RSV framing | PASS, real library parser | One vendor-public-encoder RSV1 frame on the uncompressed session: client close1002; server parser_error WS_ERR_UNEXPECTED_RSV_1, local close1006; no additional UDP datagram. No custom frame parser or malformed ENet. |
| Other component0.2 policy/API | PASS at prior evidence level | Entire final suite reruns19 component checks,8 deterministic policy checks,15 actual-component/mock-socket/fake-clock checks. Real2/1400/4096 A/B bytes/tuples, strict other headers/routes/caps, parser text/size/fragment cases, pending4/header2s/attempt8, exact head accounting273/273, callback/queue/time/retirement mocks all pass. |
| Normal close and final cleanup | PASS in attempt6 | All seven real groups finish closed with0 component timers/TCP/UDP handles. Child0 WS/raw clients and no network handles. Parent no TCP LISTEN (lsof exit1/empty) plus SO_REUSEADDR TCP bind/close and UDP bind/close pass on fixed29865/29863. |
| Exact inputs frozen | PASS | Current source matches retained attempt6 source snapshot/hash; policy/mock/supervisor unchanged. Accepted vendor and all17 frozen runtime files unchanged. All original attempts1–5/results/handoff/root historical manifest retained. |
| Genuine browser opening/response | NOT RUN | This suite uses Node ws configured to generate the exact standard offer; no browser launched. D043 requires genuine browser component evidence before real game proof; MAIN must release/own that later step. |
| Game/native/ENet/authority/multiplayer/performance | NOT RUN | No game/native/browser child, build, external endpoint or production traffic. No gameplay/transport acceptance inferred from synthetic echo. |

## Driver failure and preserved history

Attempt5 FAIL is preserved. Its newly added upgrade observer incorrectly
assumed response.req existed; Node emitted an uncaught TypeError before the
standard-offer case, child exited1 in0.063665917s, report correctly records
missing_valid_json. Original stderr contains the actual source/stack. Normal
gateway close was not observed in that failed child; parent independently
verified no LISTEN and successful fixed-port bind/close after process exit.
No failure was promoted to PASS.

Inspected vendored websocket.js: it emits upgrade before clearing websocket._req
(lines938–947). Driver now reads that inspected ClientRequest via its normal
getHeader method during the event and records only safe extension metadata.
Optional chaining prevents the metadata callback throwing if absent; exact
offer assertions still fail if request evidence is missing. Actual component
source did not change between attempts5/6, only this reviewed driver correction.

Executed from repository root after inspection/syntax checks:

```sh
python3 -B web/transport/tests/run_gateway.py --attempt attempt-5 --rationale 'D043 / T057 3.2 / contract0.2 changed source: accept only absent or exact standard browser extension offer without negotiation; add real component standard-offer/response, unknown/duplicate/modified offer and unnegotiated RSV1 regressions; preserve attempts1-4.'
python3 -B web/transport/tests/run_gateway.py --attempt attempt-6 --rationale 'Correct attempt-5 driver-only upgrade metadata error after inspecting vendored event order: capture ws ClientRequest header during upgrade, not absent response.req. Same D043 source, exact standard-offer/no-negotiation/RSV1 checks; preserve attempts1-5.'
```

Each invocation has distinct changed-code/review rationale, new path, exact
source snapshots/Node/vendor hashes/argv/environment/stdout/stderr/results;
no blind identical retry. Historical attempt2 accounting failure also remains
as described in first handoff. No existing result or handoff overwritten.
Historical root SHA256.json still hashes58fe3a72ecc43d5f28aa7e24014ef512be75e3a7759fff9aa85e12ef627fd4ae;
its old current-source entries describe that historical revision. Current
pins/evidence inventory live under revision-3.2 instead.

## Interface, limitations and next owner

API unchanged: startGateway(config) -> Promise<{address,snapshot,close}>;
schema_version1 plain exact config with run_id and two capability_sha256
digests of canonical UTF8 tokens. Fixed address127.0.0.1:29865, distinct connected
udp4 tuples to127.0.0.1:29863. Snapshot schema_version1/run_id with cloned bounded
counters/sessions/tuple/reason/cleanup; no capabilities, URL, payload or handles.
admitted counts reservations, including later RFC failure; send counters count
successful callbacks, not remote application delivery. close is idempotent,
normalizes untrusted reasons, resolves after owned handles complete. No CLI;
optional CLI/signal wiring remains unimplemented for a future consumer.

Resource/timer/race coverage remains explicitly fake-clock/mock evidence,
including60s tuple hold,500ms backlog,5/10s heartbeat,30s idle,150s session and180s
run. No actual long network run or total RSS/CPU bound asserted. maxFragments
counts nonempty retained buffers; maxBufferedChunks counts TCP chunks, not
bytes. Buffered-chunk rejection/invalid UTF8/masking/empty-frame stress paths
remain unrun; one controlled RSV1 path is now exercised. Native ENet1GiB
reassembly/untrusted-map debt remains outside this component.

Re-read T0573.2/contract0.2 before submission. No unresolved component scope
question. MAIN owns source acceptance and any genuine browser/native/game
integration release; no such launch authorized here. Current T057 source/tests
are frozen for review, and T040 runtime output remains frozen.
