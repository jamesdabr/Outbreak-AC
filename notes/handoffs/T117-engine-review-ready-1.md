# T117 Engine & Multiplayer review-ready checkpoint

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket: T117 revision1.4, RELEASED preparation only.
- Contracts: CANDIDATE_PAIR_SMOKE0.5 and CANDIDATE_RUNTIME_ADMISSION0.4; D123/D126/D129/D132/D134.
- State: REVIEW-READY, NOT FROZEN. Await explicit MAIN checkpoint clearance under D134. This handoff makes no acceptance or ticket-status change.
- Base: original repository; compiled artifact source remains its separately reviewed bdaa8df7 identity. New external controller source is not claimed compiled into that artifact. Historical source/evidence/SDK/cache/artifacts/admission versions and pre-existing edits were preserved. No Git mutation or commit.
- Changed source: exactly the nine new files under web/runtime/pair-smoke listed below. New evidence only in preparation-T117-1; own T117 question notes record D126/D129 issues now resolved by MAIN.

## Acceptance evidence

PASS — inspected guarded FIXTURE_ONLY builtin suites, run from /Users/jd1/code/apps/outbreak:

```sh
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node web/runtime/pair-smoke/test_observe.cjs
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B web/runtime/pair-smoke/test_policy.py --review-ready
```

Node:17 tests,0 failures. Python:35 tests,0 failures,0 errors. Both record actual_effect_attempts:[] and actual_runtime/authority/P0:false. Python audit/patch guards precede project imports; Node blocks effectful imports/process/network/random/timer APIs. Only owned fixture files were written. The public admission API is an explicitly injected FIXTURE_ONLY boundary double; no actual admission implementation was imported/called, no real controller CLI/child entrypoint/runtime was invoked.

Current evidence:

- web/runtime/pair-smoke/preparation-T117-1/review-ready-3.json — SHA256 `11ea93351f5a3cec7e8b8ab8f12f243925f9257abb117e9bd1e32af689d3691c`.
- python-result-3.json — `e8590f5adf5b1627489bc0e1d6ccee3228a9bfcffd7523aea5cadf15fd600e9b`; python-test-3.log retains full35-test output.
- node-result-3.json — `1cb5cca6d396a48ab721315f05f5cccabb41b408090e8a3af1e753702f22b3a8`; node-test-3.log retains full17-test output.

The review record binds all nine current hashes, complete retained preparation file inventory and governing ticket/contract/review/decision hashes. Python result independently binds all nine; Node result binds its observer and harness. Earlier numbered logs/results remain unchanged. Transient owned filesystem link negatives were removed; retained fixture files are ordinary single-link files. No freeze record was generated.

## Candidate source and private-schema hashes

All paths below are within web/runtime/pair-smoke; SHA256:

| File | SHA256 |
| --- | --- |
| policy.py | 6dad190866f3dc7c9f116faa2f28008081ea04b19d45c72df82012154e711db7 |
| supervise.py | 3dae4be7bf6d4458c6b2e76bf4e4467f0a99957d03e1eef762bf43cde0ee6900 |
| ownership.py | 7a5f414a404240d73fc8896d0357813c313851fb7dfd7dcd5d25b22e1873e963 |
| observe.cjs | dd58e3d24c0257dd22132975de4a433c4cfa8c4e869dd9e2232fd213986bc19d |
| run.py | b2d251c2bf071cab4cb93588c0df0ce2143bc89fbf338fe2d2d1fe2a794211bc |
| test_policy.py | 035361e4c796e2e590d08606c010458b319ea614b40997cd1b2bc80d5e12fdad |
| test_observe.cjs | d4ceee0c9e4479122b9a39459a2b2bcc9727b83cd95211fb250a3f255af07978 |
| SCHEMA.md | 6c8ab6e23e7c9ffde973e890ffe5a3b33bbf85e7191823bac09713a5f2b3e4dd |
| README.md | 81bee22a53b59216aa0a7c180e4d35b5f9f5754c606edff987778a0bd5d3a24f |

## Implementation status

Implemented future controller source: strict independent digest/schema/root/role/tree/alias gates before effects, D129 derived ordinary0644 authorization self-row preserved through closure, literal web.runtime.admission_v4.admission seam plus separately pinned original stage.py, fixed source-derived native setup and browser options, admitted publication-only routes, two ordinary-input client movements with independently checked identity/parsed receipts, finite evidence/privacy/deadlines, owned process/profile/tuple cleanup and original-UNION-owned preservation. SCHEMA.md defines private plan/child/report/ledger/receipt layouts and terminal slots. No selectors/fallbacks or public API/data changes.

T118 five returned findings addressed in the same working package:

1. Both movement directions bind every own tuple to independently validated A/B active identities; duplicate/relabelled first-direction proof refuses (test26).
2. Popen handles are provisionally retained before ps registration; recovery requires exact live owned handle, parent/group/executable/birth identity (test27).
3. Report remains pending; final ledger/admission/deadline gates precede the final atomic receipt seal. Late failure cannot leave a PASS receipt (test28).
4. Inspector output streams into the shared bounded evidence budget before append; overflow fails and the retained own handle is stopped/reaped. No unbounded subprocess.run capture (tests29/32).
5. Authorization ordinary0644/nlink1 checks precede parsing and remain checked after admission/through preservation (test30 and D129 cases).

Additional fixture coverage includes partial cleanup tuple retention, loaded private library paths/hashes/signatures, narrow D132 otool tool-role exception, exact child/private cleanup schema, raw first-ACTIVE getter lag, original startup/frame0 distinction, visibility/warnings/counters, join/receipt deadlines, phase ledger, source mapping and import-no-effects. Native evidence follows D126: startup/two connections+logins/maprev2 plus gateway sessions/UDP and real published receiving-parser receipts; no fabricated native per-position/internal ordinal diagnostics.

Simulated only: files/admission/Page/process/ports/native log inputs in fixtures. Future effectful Runtime/observer/inspector implementations are authored but uninvoked. Fixture success does not establish that OS/process/browser integration meets the runtime bounds.

NOT RUN: actual v4 import/current accepted-graph integration; any actual CLI, subprocess inspector, native/browser/gateway/static service, socket/network, compilation/install; real two-way smoke, loaded-image observation, actual cleanup/timing; hardware/performance/audio/pixels/human evidence; authority/P0/MVP acceptance. No performance claim is made, so hardware benchmarking does not apply to these fixture results.

## Integration and questions

No dependencies/assets/wire/gameplay/shared API changed. D126 and D129 resolved the two own questions. v4 acceptance, actual current admission proof, controller/private-schema approval, exact MAIN runtime pins and separately explicit one-use execution release remain later gates. T103/Player/QA holds and all historical failures remain intact.

Requested MAIN action: review this exact source/test/schema candidate and evidence before freeze. Return in-scope findings within the current lease or issue explicit D134 checkpoint clearance. No final freeze or actual integration/execution is claimed or performed by this submission.
