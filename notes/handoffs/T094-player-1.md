# T094 — Foundation measurement component preparation

- Worker: Player / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e.
- Ticket/revision: T0945.17, RELEASED at final read; D090, FOUNDATION_MEASUREMENT0.1, FOUNDATION_OBSERVATION0.1, PLATFORM_DECISION0.1; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5 preparation only. MAIN owns review/status.
- Base:13f0d8eea4822dee5c976661218d022be74342e3 plus accepted frozen T089/T091 overlay and other preserved dirty/untracked work.
- Changed: NEW web/qa/foundation/T094/** and this NEW own handoff only. No production/old QA/controller/test/source/tool/artifact/ledger/pin/contract/status edits, commits/reset/dispatch. QA chat remains on human hold.
- Outcome: **COMPONENT_PREPARATION_DELIVERED;36 PURE FAKE-PAGE CASES PASS; ACTUAL_BROWSER/RUNTIME/BENCHMARK/RSS/INTEGRATION NOT RUN.** Private result schema, component, fixtures and15-member evidence frozen; no self-acceptance.

## Acceptance evidence

| Criterion | Result / evidence |
| --- | --- |
| Exact component boundary | PASS measure.cjs exports only async measureFoundation(page), imports nothing, rejects additional options/hooks before actions. No launch/bootstrap/join/respawn/private function/console/Module/state setters/HTTP/socket/process/package import or arbitrary profile/URL/flags. Existing source-defined public snapshot getter is observation only. No integration into old controllers. |
| Fixed entry/readiness/load/canvas observations | PASS preparation. Validates origin, exact immutable foundation snapshot/descriptor, source diagnostics/timing, native joined/alive map2 identity/milestones, reference viewport/DPR/aspect/clip. Reads navigation/resource raw/encoded/transfer bytes with explicit unavailable/null/cache ambiguity. Running/control timestamps are observed upper bounds, not invented original readiness times. Complete requested artifact/notices transfer inventory remains external. |
| Ordinary input sequence | PASS fake Page sequence. Ordinary focus/canvas capture if needed, mouse +32/+16 with source default yaw+/pitch− and wrapped yaw difference, W250/release>=2units, fresh stationary state, W/Space/LMB100ms then Escape and published neutral/loss of capture within2s, cleanup then neutral ordinary recapture. Requires new game frames for relevant action observations; no alternate-axis/teleport/retry/state mutation. |
| Steady observer and limits | PASS fixtures.3s warmup then fixed60s rAF observer, bounded32768 tuples/8MiB report/512 events. Source timing.frame_id+1==game frame validated; retain observer and raw-game clocks separately, no unexplained skipped/regressed frames, label duplicate observations separately, all new game intervals enter nearest-rank p95 without trimming. FPS>=55/p95<=33.4/Wasm<=512MiB checks confined to frame section; JS heap availability separate, no RSS inference. Owned observer timer/rAF cancelled on completion/fault. |
| Last focus/visibility experiment | PASS fixtures. Only after steady stage, ordinary held inputs and ONE newly owned about:blank Page. Terminal PASS requires actual read hidden transition, neutral public held/capture loss, BN_FAILED/error15 plus source kind2/error15 event. Missing transition/incomplete proof NOT_OBSERVED; unrelated errors fail. Original page/context/browser not closed or reconnected, no cap reuse/visibility forcing. Only owned probe closed in finally. |
| Audio/model/errors | PASS preparation. Before/after existing gesture audio snapshots retained; actual reported context-running/cue-playing facts distinguished from physical hearing. Model snapshot retained as preload evidence only. Global/audio/lifecycle errors preserved and fail applicable sequence. No private audio play API or oscillator. |
| Private bounded report | PASS RESULT_SCHEMA.md documents/fixes version1 layout for MAIN review. FOUNDATION_COMPONENT_OBSERVATIONS, exact initial/last/final public envelopes, individual statuses, error and cleanup facts, pending external gates. No aggregate PASS/P0/MVP/authority acceptance. Sample/report bounds use UTF8 bytes; overflow explicitly fails, preserves bounded first/last frame records and never passes truncated benchmark data. |
| Pure tests/source provenance | PASS36 cases, Node exit0/stderr empty. All fixture scenarios and receipt FIXTURE_ONLY/actual_browser:false, fake_60s_is_not_benchmark:true. Actual current foundation/diagnostics/timing/model/network/audio EM_JS publishers extracted and executed with explicit fake inputs/AL/document/clock/heap. Component loaded in isolated VM without require/process/browser bindings. No Playwright/network/socket/package/process imports or real physical actions. |
| Preservation | PASS before.json==after.json and freeze recheck. Protected all source/src/ENet, old QA excluding own new T094, old T067/T082 controllers, original SDK/cache, signed/native artifacts/ledger, published browser artifacts and T074/T081/T089/T091 evidence; only NEW allowed files written. |

## Fixture coverage and interpretation

Positive fixed sequence proves behavior against fake inputs, including yaw359→2 wrap, actual extracted publisher schemas, recording all fake game intervals, expected hidden15 and owned cleanup. Negative cases cover missing/extra/wrong/nonfinite/mutable foundation data, absent actor/model, wrong map/dead client/origin/viewport, global/audio errors, event/resource overflow, stale observations, no mouse/movement, held release/recapture failure, skipped/regressed game frames, Wasm budget, long-tail percentile failure,32768-tuple overflow, mid-steady schema corruption, unrelated terminal and refusing original page as a probe. Additional cases cover missing transfer and optional JS heap APIs, explicit duplicate-observer accounting, hidden NOT_OBSERVED, cleanup key/owned-probe failures, and extra option/hook rejection. Expected failure cases themselves PASS only when the component retains its failure/cleanup report. None is actual browser or60s performance evidence.

## Frozen identities and commands

Evidence root web/qa/foundation/T094. Frozen15 members;16 files including evidence-freeze.json. No frozen member edits after freeze.

- measure.cjs `db4906dc9532ed81562b52b97e7466f40d30a2c7f78237085c3728e129a74ddc`.
- RESULT_SCHEMA.md `e3a0a1ef93ee7d1ecc511b7d98f7ecb364f89c2007c06b38b016b62fcdfd3d7f`.
- prep-1/receipt.json `4c0f521a9c153ee94592aa7ee85d8159441817ace72dc4cc7353a06bde0b1e67`.
- run-result.json `e9803aa0642601e25dcf734f931f9637a69bcb0c95eaa60a8476d305defad75d`.
- evidence-freeze.json `5d2729fd40f73e4f37c019465c79c985bf7002f699d8f64de9026aa36f999287`.
- Frozen production main remains `5f51c53b5a6f2be1180252c7aee972ab754bf0abc91d8a3d0f276153a38834f1`; MD3 remains `f60cdc019579cba4876ff741438934c56b6d626ac55c36c28e8b8ab8abe644be`.

Historical commands executed once after inspecting own source/fixtures/entrypoints; not permission to rerun or overwrite frozen outputs:

```text
python3 -B web/qa/foundation/T094/run_prep.py
python3 -B web/qa/foundation/T094/freeze.py
```

Runner invokes only installed `/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node web/qa/foundation/T094/test.cjs`, Node SHA256 `27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1`, with minimal PATH/own TMPDIR and NODE_COMPILE_CACHE. Exact command/environment/source hashes and exit0 retained. One prep-1 output, no retry. Freeze imports only own standard-library snapshot helpers and rehashes evidence, never reruns Node/tests. No compiler/SDK setup/game/native/browser/service/install/sanitizer execution. Preparation uses local macOS host; no hardware performance claim.

## Integration and remaining work

Private nested schema is proposed for MAIN review before another worker consumes it. No coupled supervisor/runtime schema, new pins, artifact acceptance or integration has been invented. Future actual use requires accepted full current-source browser/native candidates, exact MAIN pins/expected digest, separately released supervisor integration and execution. External startup console/GPU/process/RSS/cold-warm load/complete transfer and physical human evidence remain pending. A historical or fake Page sequence cannot pass PLATFORM/P0/MVP gates.

No blocking question remains for this preparation deliverable. MAIN reviews source/schema/fixtures and decides any successor integration release; current QA hold and frozen production sources are unchanged.
