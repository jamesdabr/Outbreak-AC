# T082 fixed impairment preparation handoff

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T0825.5 RELEASED under D077; re-read before submission.
  APPROVED EXPERIMENTAL_IMPAIRMENT0.1, GOVERNANCE/BROWSER_FOUNDATION/P0 0.5,
  client0.3/main0.1/backend0.2/transport0.2 unchanged. PREPARATION ONLY, submitted
  for MAIN review; no self-acceptance/status change or actual impaired run.
- Base:13f0d8eea4822dee5c976661218d022be74342e3, extensive existing dirty work
  preserved. No commits/push/reset/dispatch/new package/install/compiler.
- Existing modifications ONLY T067/{supervise.py,policy.py,observe.cjs,README.md}
  for fixed case/pins/shim/receipt support; test_preparation.py, ownership.py and
  diagnostic-schema.json byte-identical. NEW tests/impaired/T082/{run.py,
  shaper.cjs,preset.json,test_shaper.cjs,test_impaired.py,README.md}; NEW
  results/two-client-T067/source-T079-1/**; results/impaired-T082/
  preparation-20261108-1/**; this own handoff.

## Submitted behavior

Preserved complete7-file T079 driver BEFORE edits, byte-exact against D074 pins
and T077 accepted receipt, with original→snapshot path/hash mapping. All T079
PASS/T075 FAIL source/receipts/evidence immutable. No game/backend/gateway/vendor /
asset/build/native/SDK/old-pins changes. No production transport policy changed.

The baseline remains the default, using the same fields/token/roles/dependency
set/topology/genuine proof/limits/cleanup and25 tests; it never installs the shim.
One new19-line entrypoint delegates to the same supervisor with only internally
fixed case impaired40_drop50. There is no arbitrary case/observer/program/env /
flags hook or copied divergent supervisor. Runtime verifies case/ticket match.

Impaired pins retain all strict original closure/authority gates and add exact
T082 ticket/token/role/baseline_only false, exact preset, MAIN-accepted T079/T082,
complete impairment_driver tree+file hashes/roles, and isolated impaired runtime /
native outputs. No accepted execution pins were created. README gives exact
future command/schema and explains pending MAIN acceptance/pins/release.

After a future complete gate, ONLY that dedicated observer child temporarily
wraps node:dgram.createSocket before importing frozen gateway. Each gateway UDP
socket remains a real original native socket, with all address/connect/bind /
error/close behavior delegated. Only raw send/message scheduling is instrumented;
no ENet parser, game/app message injection, new socket endpoint, global OS/network
configuration, fake state or visibility/timing spoof. Future report label is
ACTUAL_IMPAIRED_TWO_GAME_CLIENT; actual game profile stays network-client.

Preset delay40_drop50_v1:40ms each direction, exactly every50th aggregate raw
datagram per direction across the2 sockets dropped. Buffers/rinfo copied before
asynchronous scheduling; length2..4096, queues64/131072 each direction, pending
deadline500ms. Early timer wake reschedules to the floor. Overflow/late/signature /
socket/native errors fail visibly, not unannounced extra profile loss. Drops
complete upstream send admission callback once without OS delivery. Planned close
cancels queued/inflight ownership explicitly; late canceled native callbacks never
call user twice; duplicate normally completed callbacks fail. Buffers/timers and
factory/method restoration have explicit receipts. No raw packet/token persisted.

Stats independently validate both direction/global and per-socket identities,
observed/dropped/scheduled/delivered/canceled/error accounting, bytes/queue peaks,
callback ownership, delay min/max/histogram and exact drop event ordinals/socket
mapping. Parent requires>=1 actual profile drop AND delivered timer EACH direction,
no faults, restored factory/2 closed sockets/zero timer-buffer-pending resources.
No loss observed means no successful impairment claim. Finite loss denominator
is explicit; nominal added80ms is not measured RTT or a latency distribution.

All genuine full native join/map/spawn/ACK/alive identity, ordinary W250ms own>=2 /
new receiver matching parsed receipt<=1unit/2s in both directions, frame/error /
join/cleanup gates remain unchanged.180s whole,8MiB child,15s join, later-frame
1000ms, gateway2s/native3s, no threshold/flag/input workaround or reconnect waiver.

## Preparation verification

| Criterion | Result |
| --- | --- |
| Original baseline regression suite |25 guarded Python tests PASS. Default baseline positive/negative schemas, readiness/clock/movement/ownership/cleanup/routing/history criteria preserved. |
| New case/receipt gate suite |8 guarded Python tests PASS, including negative subcases: wrong case/token/role/scope/type/preset/dependencies/membership/output, no effect/runtime creation, tampered receipt counts/loss/latency/queue/callback/events/cleanup, plus old7 snapshot and45 old actual evidence fingerprints. |
| Actual source parsing | Node24.19.0 SHA27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1 verified;3 syntax checks exit0: shared observer, shim and fake fixture script. Python AST parses. |
| Isolated Node shaper fixtures |14 checks PASS using own fake EventEmitter sockets/factory/monotonic clock/timers; actual sockets0, no external package/browser/native/server/network.100 invented raw datagrams EACH direction produce exact drops50/100,98 deliveries, copied bytes/boundaries and40ms floor; additionally delayed75/120ms histogram, early timer, late deadline, both queue caps, close/up/down/inflight cancellation, native/duplicate/late callback/error forwarding, unknown signatures and restoration fault. |
| Independent receipt validator | Python validates Node fixture packet accounting, then rejects altered variants. This is labeled fixture metadata, not an actual game/impairment success report. |
| No real effect from Python tests | subprocess.Popen/run, os.system/posix_spawn and socket.socket forbidden throughout. Fake accepted-looking authority/pins exist only in temporary FIXTURE_ONLY filesystem/effect doubles, never RealView actual execution. |
| Protected current inputs | Read-only check of all26610 D074 pinned files: only4 explicitly allowed shared-driver files changed,26606 others byte-identical;48 aliases and10 memberships unchanged. Snapshot exact7 matched separately. T07923/T07522 actual fingerprints unchanged. |
| Actual impaired experiment | NOT RUN. No accepted pins/output runtime/native sandbox, real socket, browser/native/game/package execution, compile/install or additional actual baseline created by this preparation. |

Node fixture sources inspected before invocation, minimal env without preloads.
Initial11 checks were extended to13 and then14 as boundary/cancellation/histogram
cases were added; all intermediate fixture receipts retained in this new prep
directory, final source validation uses shaper-fixture-3.json. No failing actual
run was masked, tuned or retried. Shared game sources/artifact/SDK stay immutable.

Reproduction from /Users/jd1/code/apps/outbreak (use a NEW preparation output):

```sh
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node --check web/transport/tests/impaired/T082/shaper.cjs
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node --check web/transport/tests/two-client/T067/observe.cjs
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node web/transport/tests/impaired/T082/test_shaper.cjs PREPARATION-DIR/shaper-fixture.json
PYTHONDONTWRITEBYTECODE=1 python3 web/transport/tests/impaired/T082/test_impaired.py --receipt PREPARATION-DIR/shaper-fixture.json
PYTHONDONTWRITEBYTECODE=1 python3 web/transport/tests/two-client/T067/test_preparation.py
```

The frozen result.json records33 Python tests (25+8),14 fake Node cases,3 syntax
checks and13 current source fingerprints. python-fixtures.log retains full33-test
run; shaper-fixture-3.json has complete fixture metadata; preservation.json and
plan.json separate immutable old/current identities and future NOT_RUN scope.

## Remaining gates / freeze

Prepared source frozen with results/impaired-T082/preparation-20261108-1/result.json;
later finding requires a question before editing. MAIN alone reviews/accepts T082
and supplies fresh complete current pins+out-of-band expected SHA and explicit
actual release. Preset/hash or helper success is not execution authority.

No unresolved scope incompatibility blocks preparation submission. Actual real-UDP
delay/loss/game outcome/callback/resource behavior remains NOT RUN; a future run
could still fail unchanged game/time/error thresholds or insufficient actual
drops. Preserve any such result with no automatic retry/tuning. Comparison with
T079 will be across different run samples. No authority/cache/rejoin/performance /
eight-player/human media/P0/MVP acceptance follows from these fixtures.
