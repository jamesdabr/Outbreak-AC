# T077 corrected observer preparation handoff

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T0775.0 RELEASED, **PREPARATION ONLY**, re-read before freeze.
  Submitted for MAIN review; no authoritative status change/self-acceptance.
- Contracts: browser foundation/GOVERNANCE/P0 0.5; client0.3/main0.1;
  backend0.2/transport0.2; D070 reviewed failed T075, historical T067/D067
  preparation and D064 actual build/verifier retained separately.
- Base:13f0d8eea4822dee5c976661218d022be74342e3, master, pre-existing extensive
  dirty engine/web/docs preserved. No commits/push/reset/dispatch or new dependency.
- Changed existing files ONLY under web/transport/tests/two-client/T067:
  observe.cjs timing/evidence, supervise.py final tuple cleanup, policy.py matching
  helpers/observation/dependency rules, test_preparation.py regressions, README.md
  current-version documentation. ownership.py and diagnostic-schema.json unchanged.
- NEW: web/transport/results/two-client-T067/source-T075-1/** (seven original
  files plus mapping manifest); preparation-T077-20261108-freeze-1/** (fixtures.log,
  preservation.json, plan.json, result.json); this own handoff.

## Implementation and evidence

| Criterion | Submitted result |
| --- | --- |
| Preserve complete old driver BEFORE edits | PASS. All7 byte-exact files match both D068 runtime pins and original preparation receipt; source-T075-1/manifest.json maps original→snapshot paths/SHA. Historical source/receipt/runtime evidence never overwritten or represented as current. |
| Positive first-frame classification | Implemented in prepared JS plus pure Python reference. Timing frame0, engine loading frame_count1/rendered0, exact first lifecycle/WS advance counters, opening/joining lifecycle and initial kind0 events/prejoin map/identity, frozen visible public observations, no error. Preserve raw startup value and resample; it cannot enter readiness or ACTIVE/movement acceptance. Missing/ambiguous identity fails. |
| Later-frame/errors/deadlines unchanged | FIXTURE checks PASS. Every later frame raw>1000 still fails with a main-frame interval label, without inferring backend cause. Actual backend error/BNE15, hidden/global error, open/join deadlines and all prior gates remain. Settled Python observation requires frame_id>=1/raw<=1000; no startup success exception. No game/backend/clock/prediction/visibility or threshold edits. |
| Bounded full failure / first ACTIVE evidence | Prepared source retains A/B only, fixed last/first_active/startup slots. Full public network/main/timing/model/audio/browser sample is retained BEFORE timing/eligibility/global failure checks. First ACTIVE per client is retained before paired readiness, never equated with paired proof. Null explicitly means unavailable. Events/global errors512, remotes256, preloads3, per-sample and retained-byte bounds1MiB, final output8MiB; overflow explicitly fails with bounded sample fault. Cap redaction precedes retention/disk. |
| Final gateway UDP tuples on failure | Implemented parent bookkeeping only: union valid observed baseline and final/retired tuples even when observer fails before paired validation. Validate fixed loopback gateway schema,<=2 known session IDs/facts, exact address/port/IPv4 UDP tuple shape, integer1..65535; merge uniquely into existing lsof/rebind checks. Missing/invalid final or connected tuple facts fail ports_released, while valid other tuples still get checked. No ownership inference or unrelated kill. |
| Strict future pins | Matching pure dependency rule now requires MAIN-accepted T077 plus all prior dependencies and fresh current file pins. Missing/unaccepted T077 fixtures refuse before effects/runtime creation. Old D068 pins are historical and cannot authorize modified source. Recipe ticket T067/token/output rules unchanged; new runtime release remains required. |
| Guarded preparation suite | **25 tests PASS**,0 errors/failures. Original17 test methods remain plus8 new T077 methods with negative subcases. subprocess.Popen/run, os.system/posix_spawn and socket.socket forbidden during all tests. Python helper/reference/source/data checks only. |
| Protected preservation | PASS read-only check: out of26592 old pinned files only5 explicitly allowed files changed;26587 others byte-identical. All48 alias identities and10 file-membership trees unchanged. All22 frozen actual T075 evidence fingerprints unchanged. No game/source/pack/build/bundle/SDK/native/pins edits. |
| Actual follow-up | **NOT RUN**: Node/JS syntax/package/compiler/browser/native/server/network or second baseline. T075 historical result remains FAIL; whether B's1047ms was first startup elapsed or a backend gap remains unproven. |

## Source reasoning and test limits

Read main.cpp1540–1660/1714–1757: frame.frames initially0, timing published at
frame0, engine count incremented to1 before final publication, no ordinary draw
until frame_count>3. Read client.cpp204–234: first published frame call/advance/WS
count1; begin calls1, opening or joining map/own identity still prejoin. Backend
enet_websocket.js62 checks inter-frame elapsed only when lastFrame is non-null.
This supplies a strict positive startup identity without a new API or guessed
inference from raw duration/BN_OPENING alone. Snapshot producers remain immutable.

The JS FIRST_FRAME_IDENTITY JSON table matches the pure Python reference table
under a SOURCE test. Tests cover genuine long frame0 startup and resampling,
already-open initial joining case, invalid/ambiguous/missing/bool/stale fields,
later1000 boundary/1001 failure, real terminal error/hidden/global errors,
bounded full last/first ACTIVE samples and raw fields/redaction, overflow/missing
slots/required components, and missing/unaccepted future T077 pins. These are
fixtures/reference/source inspection, **not execution of the JS classifier**.
Current JS syntax/runtime remains for MAIN's separately authorized verification.

The actual historical failed T075 report is consumed only as immutable DATA:
it has no gateway_receipt, and the new pure helper still extracts both final
UDP61734/62986. Additional fixtures cover duplicate union, malformed address/
family/extra protocol/boolean/out-of-range ports, missing final/connected tuple
facts, and retain valid other tuples while failing completeness. No socket was
opened to run these cases. Original successful additive cleanup supplement stays
historical and unchanged.

Reproduction from /Users/jd1/code/apps/outbreak:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/transport/tests/two-client/T067/test_preparation.py
```

Captured test output and current seven source hashes are in
web/transport/results/two-client-T067/preparation-T077-20261108-freeze-1/result.json
and fixtures.log. Current plan explicitly requires MAIN acceptance of T077,
fresh current complete pins+out-of-band expected SHA and separate execution
release/output scope. No accepted execution manifest was authored here.

## Freeze and remaining gates

Corrected source frozen with the new preparation receipt; later findings require
a question before any edit. Old source snapshot and historical evidence are
separate, immutable records. No unresolved source-interface question blocks this
preparation submission. MAIN decides acceptance and any new runtime release.

All actual corrected browser timing/evidence/cleanup behavior, full paired
identity/map/spawn/ACK and bidirectional movement remain NOT RUN. No authority/
native cache/clientsequence, physical audibility/pixels/animation/headed input,
reconnect/impairment/performance, human playtest or P0/P1/MVP acceptance is claimed.
