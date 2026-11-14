# T050 standalone WS dependency evidence

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T050 2.3 RELEASED; submitted for MAIN review, no self-acceptance
- Phase / contracts: browser prerequisite foundation/GOVERNANCE/P0 0.5; D029 bounded execution addendum 2.3; accepted T048 inspection
- Base commit: 13f0d8eea4822dee5c976661218d022be74342e3. Shared tree already contains other workers' modified/untracked files; none were reset, committed or changed by T050.
- Changed files: new exact 19-file web/transport/vendor/ws-8.21.0/**; web/transport/tests/T050-{run.py,import.cjs,loopback.cjs}; web/transport/results/T050-*; own T050 question and this handoff.
- Commit/patch: no commit authorized or created. SHA inventory: web/transport/results/T050-SHA256.json.

## Acceptance evidence

Actual runtime host: Darwin arm64. Exact existing Node v24.19.0 executable
`/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node`, SHA-256
`27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1`.
These are functional dependency observations, not performance benchmarks.

| Criterion | Result | Actual evidence |
| --- | --- | --- |
| Exact reviewed portable copy and MIT notice | PASS | All 19 members/151087 bytes match the accepted T048 source inventory, including LICENSE/package.json. No source patches, symlinks, npm/install/lifecycle scripts or optional addons. T050-vendor.json pins every file; manifest SHA c70bc9a3f7cb6c0d5d2b3135ded5cf513c305ae81f6f6a245e3cba8bca5a1cc2. |
| Import-only child, then conditional loopback | PASS | Drivers reviewed before execution. T050-import.json: exit0, 0.039168s, 3076 output bytes, all 11 recorded checks true. Exactly 14 reviewed CJS modules loaded, no .node addon/unrelated module; expected exports; fs.close/closeSync, environment, global own keys, process listeners and active handles/requests unchanged. No package constructors/listeners in import child. |
| Bounded real WS dependency exercise | PASS for all eight child cases | T050-loopback.json child PASS, exit0 naturally, 0.085963s parent elapsed / 47ms child; 2669 output bytes; no timeout/kill; child reaped. One loopback child only; peak two WS endpoints. Owned address 127.0.0.1:51793, version13, exact dependency-test protocol. |
| Required options | PASS for configuration; buffered-chunk rejection NOT RUN | maxPayload4096, maxFragments16, maxBufferedChunks32, perMessageDeflatefalse. Exact options emitted in child result. |
| Close/error/listener cleanup | PASS for child teardown; original parent report FAIL | Normal close1000, parser errors/close codes and terminate1006 recorded below. HTTP/WS closed; zero clients, peers, tracked clients and active network handles. Parent's immediate plain-bind probe returned false; original report remains FAIL. |
| Independent owned-port cleanup check | PASS; MAIN disposition pending | T050-port-cleanup.json: lsof LISTEN query returned exit1/empty output; SO_REUSEADDR socket bind to exact owned address/port succeeded and closed. No new listener, connection or package execution. Original errno/TCP state was not captured; no definite TIME_WAIT diagnosis. See question note below. |
| Browser build frozen | PASS | Complete file membership and hashes match T050-browser-freeze.json, including notices. T040 attempt4 remains unchanged. |
| Gateway/UDP/ENet/browser/native server/game/multiplayer | NOT RUN | Outside this dependency-only release; no corresponding implementation or claim. |

Eight actual child cases:

| Case | Result / observed semantics |
| --- | --- |
| Small binary | PASS, exact 15 bytes and SHA recorded |
| 4096-byte binary | PASS, exact bytes/SHA recorded |
| 16 nonempty fragments | PASS, reconstructed 16-byte binary/SHA recorded |
| Normal close | PASS, client/server1000 |
| 4097-byte rejection | PASS, client1009; server WS_ERR_UNSUPPORTED_MESSAGE_LENGTH, local close1006 |
| 17 nonempty fragments | PASS, client1008; server WS_ERR_TOO_MANY_BUFFERED_PARTS, local close1006 |
| Explicit caller text rejection | PASS, close1003, caller policy; not a binary-only parser guarantee |
| Owned peer terminate | PASS, client/server1006 |

Three binary deliveries, one caller text rejection, zero unexpected errors
and zero dropped entries in the bounded 64-entry event ring. Expected parser
errors remain visible; they were not silently classified as normal closes.

## Implementation status

Implemented exact dependency vendoring plus a supervisor, import audit and
real WS loopback driver. No mocks or simulated WS deliveries. Supervisor
verifies Node/vendor identities, uses task-local temporary cwd, stdin closed,
separate owned process group, 4.5s/9.5s deadlines and combined output cap65536
bytes, and reaps children. Environment contains only PATH=/usr/bin:/bin,
WS_NO_BUFFER_UTIL=1, WS_NO_UTF_8_VALIDATE=1 and the recorded task TMPDIR.

The original supervisor's plain-bind cleanup measurement omitted
SO_REUSEADDR and did not record errno. It cannot distinguish all socket-reuse
conditions from a leaked listener. Its FAIL and the executed driver are
preserved unchanged. Separate no-listener/reuse-bind evidence supplements
the record; it does not overwrite the original FAIL. No package child was
rerun after this failure.

maxFragments counts nonempty retained payload buffers, not every wire/control
frame or rate. maxBufferedChunks counts TCP chunks, not bytes; its rejection
threshold was not stress-tested. maxPayload is not a total connection memory,
CPU or rate bound. This exercise proves no universal zero-copy/backpressure,
UDP/ENet reassembly, admission/session bound, production transport selection
or multiplayer behavior. The browser entry of this Node package remains
unsuitable for browser-native WebSocket use as documented in T048.

## Integration and questions

No engine/shared interfaces or browser build inputs touched. Dependency is
only the exact separately authorized ws8.21.0 source copy with MIT notice.
Original T048 inspection and all prior handoffs/results remain immutable.

Already executed once per phase, in this order:

```sh
python3 -B web/transport/tests/T050-run.py import
python3 -B web/transport/tests/T050-run.py loopback
```

First command exit0; second supervisor exit1 with child exit0 and all eight
cases PASS, due solely to the recorded parent plain-bind result. Commands
are historical reproduction references, not an invitation to rerun the
one-shot authorization. Actual child argv/environment/module hashes are in
the two JSON reports; stdout/stderr are retained separately. Follow-up used
`/usr/sbin/lsof -nP -a -iTCP:51793 -sTCP:LISTEN` and one stdlib SO_REUSEADDR
bind/close, without listen/connect. Final static verification is recorded in
T050-final-verification.json; full evidence hashes in T050-SHA256.json.

Open evidence disposition: notes/questions/T050-engine-parent-port-check.md.
MAIN should review original FAIL together with child and separate cleanup
evidence and accept or return the criterion. No further package runtime is
authorized by this handoff. T040 graphics artifact remains frozen for MAIN's
actual browser observation; this ticket adds no graphics recovery evidence.
