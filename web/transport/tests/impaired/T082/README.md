# T0825.5 fixed UDP impairment — preparation only

One preset: delay40_drop50_v1,40ms each direction and raw aggregate direction
ordinals50,100,… intentionally dropped, across the2 owned UDP sockets. No game
or network experiment has been run here. Node fake-factory/clock/timer fixtures
and syntax checks are preparation evidence only. MAIN acceptance and fresh
complete pins/expected SHA/explicit actual release are still required.

Historical accepted T079 driver preserved before edits in
web/transport/results/two-client-T067/source-T079-1,7 files matching D074 and
the T077 receipt. Original T079 PASS and T075 FAIL evidence stays immutable.

## Private case and pins

Default T067 entrypoint remains baseline, with the same fields/token/roles /
topology/dependencies/25 criteria. It neither imports nor installs the shim.
run.py selects the sole additional internal case impaired40_drop50; there are
no observer/program/environment/profile/flags hooks. Both use the same parent /
observer and game proof. Runtime rejects case/ticket mismatch before effects.

Future command, **NOT AUTHORIZED / NOT RUN**:

```sh
python3 -B web/transport/tests/impaired/T082/run.py --execute \
  --pins /Users/jd1/code/apps/outbreak/notes/decisions/MAIN-SUPPLIED.json \
  --pins-sha MAIN-SUPPLIED-SHA256 --attempt MAIN-SUPPLIED-ID
```

No execution pins are generated here. The exact shared schema retains every
current source/SDK/Node/browser/Playwright/vendor/gateway/native/library/map /
bundle/metadata/D064 authority/alias/membership gate. Impaired pins additionally:

- ticket T082, execution_release EXPLICIT_IMPAIRED_TWO_CLIENT_NATIVE_GAME_EXECUTION;
  scope role full-cpp-two-browser-native-game-impaired, baseline_only false;
  game profile remains network-client, clients/capacity2, map_revision2, trusted_only true.
- accepted_dependencies original exact set PLUS T079 and T082 ACCEPTED by MAIN.
- impairment exactly preset.json (no extra fields or numeric/type changes),
  also hashed and compared to data; all run.py/shaper.cjs/preset.json roles driver.
- complete impairment_driver tree rooted web/transport/tests/impaired/T082,
  every current file hashed with exact membership; no partial/stub substitution.
- outputs only web/transport/results/impaired-T082/runtime-ID and
  web/server/run/T082-ID, fresh nonexistent owned attempt paths.

Missing/wrong authority/SHA/case/token/role/preset/dependency/source/membership /
output refuses before process/listener/staging. Test authority files/effects are
clearly FIXTURE_ONLY doubles. Accepted T082 is a future requirement, not a
worker assertion. Shared report label is ACTUAL_IMPAIRED_TWO_GAME_CLIENT.

## Shaper semantics

Only the future dedicated observer child wraps node:dgram.createSocket before
importing the frozen gateway, after complete pins. Each accepted factory call
is exactly udp4, max2, with an actual original native socket underneath. All
address/bind/connect/error/close behavior delegates to the real socket; only
connected send(Buffer,callback) and message(Buffer,rinfo) are scheduled. Unknown
signature/socket/length/source fails visibly; no parsing of ENet/game bytes.
Inbound rinfo must be actual IPv4 loopback source29863 with matching byte size.

An owned Buffer copy and rinfo copy occur before scheduling; boundaries/bytes unchanged.
Independent aggregate up/down ordinals start1 across both sockets. Multiples50
are dropped immediately as intentional raw network loss, with the upstream send
admission callback completing once, without an OS send. Other packets enter
direction queues capped64 pending datagrams/131072 bytes, length2..4096; pending
includes upstream sends awaiting native callback. Each monotonic due timer has
a40ms floor (rescheduled if fired early), a500ms pending deadline, and a finite
queue; overflow/late work are explicit error outcomes/faults, never profile drops.

Same-delay scheduling walks ordered jobs; no intentional reorder, duplication,
corruption or payload-dependent policy. Raw UDP may still have native network
behavior; this does not create reliability or server authority. Nominal added
round trip80ms is a scheduled profile, **not measured ping/internet RTT**.

Counts per direction and per socket include observed bytes/datagrams, scheduled,
dropped, delivered, canceled, errors, pending bytes/datagrams, peaks, callbacks /
errors/late callbacks, delivered-delay count/min/max and40–49/50–99/100–499ms
histogram. Actual delay is monotonic shaper waiting until real OS-send dispatch /
downstream message release, not end-to-end latency. Metadata drop events retain
only kind/direction/ordinal/socket; never tokens or raw packet bytes. Events and
faults bounded512; overflow is a visible experiment fault. Child output8MiB.

Close cancels queued/inflight ownership once, releases buffers/timers, gives
upstream callbacks explicit close errors, ignores and counts legitimate native
callbacks arriving after cancellation without calling users twice, and restores
the factory/methods after gateway cleanup. Duplicate native callbacks on normally
completed sends are faults. Native socket/send errors and throwing callbacks are
visible faults. Only expected close cancellations may account for callback errors;
they are recorded separately from intentional loss, not hidden as profile drops.
Changed factory identity is not overwritten; restoration fails explicitly.

Parent independently validates exact preset,2 closed sockets, zero resources /
restored factory, all global/socket accounting equations and latency histograms,
raw byte/queue bounds and callback ownership, precise drop ordinals and socket
mapping, no faults, and>=1 profile drop AND timer delivery EACH direction. No
observed drop means no successful impairment claim, even if game movement passes.
Observed finite loss is reported dropped/observed; it need not be exactly2%.

## Unchanged genuine proof and cleanup

Real native-c2/map2/accepted full client, distinct cn/current alive life, actual
SERVINFO/CONTD/WELCOME/SPAWNSTATE/ACK, ordered milestones and real join<15s.
Ordinary inputs only, W250ms own>=2/newer matching receiver parsed position within
1unit/2s in each direction, advancing frames/no genuine errors. T077 first-frame
classification/full last+first-ACTIVE evidence unchanged. Backend frame1000ms,
prediction50ms, whole180s, gateway2s/native SIGINT3s, no limits/flag/state spoof.
Owned processes/groups/profiles, static/gateway/native handles and every observed
UDP/control/fixed port cleanup remain mandatory. No actual rerun or recovery
shortcut follows a failure; preserve/freeze and question MAIN.

## Preparation reproduction

Use pinned Node24.19.0 (SHA27db838b…b5b1), built-ins and own code only; no packages
or real sockets. Example fixture output belongs under a NEW preparation directory:

```sh
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node --check web/transport/tests/impaired/T082/shaper.cjs
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node --check web/transport/tests/two-client/T067/observe.cjs
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node web/transport/tests/impaired/T082/test_shaper.cjs PREPARATION-DIR/shaper-fixture.json
PYTHONDONTWRITEBYTECODE=1 python3 web/transport/tests/impaired/T082/test_impaired.py --receipt PREPARATION-DIR/shaper-fixture.json
PYTHONDONTWRITEBYTECODE=1 python3 web/transport/tests/two-client/T067/test_preparation.py
```

Fixture sources were inspected before execution; runs used a minimal environment
without NODE_OPTIONS/preloads. Fake sockets are EventEmitters with injected clock /
timers.14 Node cases cover copied2/4096-byte boundaries/rinfo, independent ordinals,
floor/early reschedule, late timeout, both queue caps, close/up/down cancellation,
native errors/duplicate/late callback ownership, unknown signature and restoration.
Python guards forbid subprocess/socket effects; strict-case tests reject wrong
pins and independently validate/tamper the Node fixture receipt. Original25
baseline tests still pass. These are **not** fabricated game/impairment results.

Actual delayed/lost native datagrams, actual game proof under impairment and
resource behavior remain NOT RUN. Comparison with accepted T079 will compare
different samples, not establish a latency distribution. No authority/rejoin /
performance/eight-player/human-media/P0/MVP conclusion is authorized here.
