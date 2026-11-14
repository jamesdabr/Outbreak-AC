# T067 two-client observer preparation handoff

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket: T067 revision4.2 RELEASED, **PREPARATION ONLY**; submitted for MAIN review,
  no authoritative status change/self-acceptance.
- Contracts: BROWSER_FOUNDATION/GOVERNANCE/P0 0.5; client0.3/main0.1;
  backend0.2/transport0.2; D010/D020/D052/D054/D055/D057/D058/D060/D063/D064.
  Re-read ticket4.2 before submission. T068 integration/diagnostics and frozen
  T069 checklist read; D064 build acceptance is separate from runtime release.
- Base: 13f0d8eea4822dee5c976661218d022be74342e3, master. Extensive pre-existing
  modified/untracked engine/web/MVP/ticket/notes work preserved. No commits,
  branches, resets, worker dispatch, source/asset/SDK/bundle edits or native
  runtime directories created.
- Changed files: NEW only `web/transport/tests/two-client/T067/{README.md,
  diagnostic-schema.json,policy.py,ownership.py,supervise.py,observe.cjs,
  test_preparation.py}`, this own handoff, and
  `web/transport/results/two-client-T067/preparation-20261108-freeze-1/{fixtures.log,
  plan.json,result.json}`. Prepared source is frozen with the receipt; later
  findings require a question before any changes.

## Acceptance evidence

| Criterion | Submitted evidence / result |
| --- | --- |
| Exact future command, pins/schema and interfaces | README and plan.json, prepared for review. Missing/wrong digest/authority/release/profile/role/dependencies/source/membership/pack/bundle/tools/output cannot call fake runtime effects or create fixture runtime paths. Exact accepted T061 schema and D064 current artifact/receipt/verifier gates. |
| Inspected future supervisor/static/observer source | Prepared only; no runtime claim. Native exact c2 D010 sandbox; map staged under packages/maps/servermaps. Exact runtime/notices routes plus D063 GET favicon204/empty; other routes/methods rejected. |
| Genuine spawn/diagnostics semantics | FIXTURE checks pass. D057 zero-request native spawn accepted only with actual ordered milestone4+ACK proof; already ACTIVE not sent artificial request. Still-JOINING click after SERVINFO+2s,>=1100ms between ordinary requests. Cross-getter transition settle allowed; actual spawn timestamp remains strictly<15s after real OPEN, no late-join waiver. |
| Bidirectional movement semantics | FIXTURE checks pass: own>=2 horizontal; newer matching cn/life receiver parsed position/count/time within1 unit and2s, frame/render progress, distinct identities. Reject own-only, duplicate/reused identity, frozen frames, old parsed receipts, wrong position, late deadline, missing input focus/capture. Passive receiver focus recorded honestly, not required. |
| Failure/cleanup and Node partial startup | FIXTURE checks pass. Pure owned-process selector/signal helper tested with isolated-profile Chrome plus descendants, unrelated Chrome, reparenting, vanished child and PID/birth reuse. Parent independently scans profile provenance before final JSON; early atomic capability-free ownership receipt persists browser PID/control-port/profile facts. Fallback signals only matching owned identities and always fails/freeze-reruns. Missing cleanup fields never PASS. Actual resource behavior NOT RUN. |
| Pack | Actual read-only stdlib test:79 files/388791 bytes, each entry size/SHA matches accepted network manifest. No pack generator/validator imported or run. |
| Redaction, bounds and error classification | FIXTURE checks pass; two exact T047 notices once/page only. Other errors preserved, caps/token text redacted before persistence.512 events/component,8MiB/child,180s whole attempt,15s genuine join,2s movement/gateway close,3s native SIGINT. Parent reserves cleanup by160s. |
| stdlib preparation suite | **17 tests,0 failures,0 errors**, Python3.11.9, macOS26.5.1 arm64. `PYTHONDONTWRITEBYTECODE=1 python3 web/transport/tests/two-client/T067/test_preparation.py`. Full captured run in fixtures.log; source fingerprints in result.json. All process/socket entry points used by project runtime are mocked/forbidden in tests. |
| Earlier fixture failure | Initial16-test run failed one membership fixture because fake filesystem and pin inventory shared a mutable list. Corrected fixture uses separate lists; production comparison unchanged. Subsequent17-test suite passes. Historical issue explicitly retained in result.json. |
| Actual tools/game | **NOT RUN**: compiler/Node/version commands/package imports/JS syntax/server/listener/browser/native game/network. No actual MAIN runtime pins manufactured, no game success report. |

## Implementation status

Pure authorization/routing/diagnostic/ownership helpers and labeled fixture tests
are implemented and exercised. Future effects are **unexecuted source**. The
prepared Node script cannot substitute its OBSERVATIONS_COMPLETE status for
Python parent proof validation and independently complete cleanup. No private
Wasm/Module/ENet action calls or socket-only fixture can satisfy the baseline.

Future pin schema requires MAIN acceptance of T070/T072 in addition to prior
source/tooling components. D064 has now supplied BUILD acceptance: exact bundle
35bad2ff04cdc17df5193ca026969380e7c9dc4176596601972b4af163b90e0a.
Observer gates the exact D064 JSON, complete published bytes/membership, original
build pins, separate additive verifier and immutable receipt without invoking
that verifier or erasing the historical verification exit2. This is no runtime
acceptance. Complete future MAIN runtime pins+expected SHA and explicit execution
release/output allowlist remain required before every child/listener/staging.

The README documents failure/cleanup ordering, proved-ownership fallback,
per-attempt immutable evidence, preflight/cleanup ownership+bind/errno checks for
fixed and recorded ephemeral ports, and explicit limitations. Missing final JSON
cannot yield successful cleanup; owned surviving Chrome can be discovered from
its unique isolated profile even before launchServer's receipt. Parent tracks
birth/command against PID reuse, retains only owned metadata, and never kills an
unrelated owner. Cleanup failures/crash freeze reruns rather than automatic retry.

## Integration and remaining gates

No shared interfaces changed; no new dependency/assets added. Exact published
APIs are consumed read-only. Actual scheduling/focus, CSP and package behavior,
JS syntax, full C++ instantiation/native handshake/map/spawn/ACK, both movement
directions and OS cleanup all remain **NOT RUN** until separate release.

T068/D057 limits preserved: render phase running is scene readiness; ACTIVE can
coexist with death, so movement requires alive0. Own prediction is distinct from
receiver parsed x/y; distinct gateway tuples do not prove internal cn/cache
binding. owned_local_attempts carries its qualified path coverage, while timing's
embedded-server false is a compile-profile fact, never global runtime-zero proof.

D060/T069 separate gates remain NOT RUN: ordinary weapon selection/engine quit,
held-fire/jump release and internal AudioContext-close acknowledgment. Context
destruction is abrupt peer loss. Optional model preload/audio states do not prove
pixels, animations, human hearing or complete input/media acceptance. Native
internal cache/clientsequence, authority, reconnect/impairment, performance,
human playtest and P0/P1/MVP are unobserved/unaccepted by this handoff.

MAIN may review the frozen source and receipt; no unresolved question currently
blocks this preparation submission. Actual execution remains unreleased.
