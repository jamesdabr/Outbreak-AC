# T127 single dispatched controller refused without retained attempt

- Author / worker: World/Match-Systems
- Ticket / revision: T1271.1 / D147 explicit finalized-pins dispatch
- Contract: smoke0.7/admission0.4/GOVERNANCE/BROWSER_FOUNDATION/P0 0.5
- Status: OPEN (MAIN resolution recorded separately)

## Exact observation

The ONE fixed accepted controller invocation for D147-pair-1 terminated exit2 after19.25273037503939seconds. Stdout exactly `{"status":"REFUSED_OR_FAILED","authority":false,"P0":false}` plus newline (60bytes); stderr empty. Supervisor fault null, no timeout/overflow/signals; controller reaped. No second invocation, gate/admission call, probe or workaround.

Finalized pins55981916bytes/SHA256c10b343d5175c27591e340a8793fcc6c2b61de1eae99a77124692ae0155ffb4e matched before and after. Nine accepted checkpoint2 source hashes and accepted freeze942fffc368ffc0afb8c72a06c6bedd7ae8d467e0da865e6bb6c555c932a8f605 matched before invocation; source hashes still match after termination.

Both exact output roots remain absent, as does web/transport/results/candidate-pair parent. All three serialized absent_roots remain absent. No receipt/report/ledger/partial-attempt files exist. The CLI catch intentionally emits generic redacted failure and no specific exception. No exact failing gate or runtime-started flag is available; no failure cause inferred from this summary alone. No native/browser/Node/inspector/runtime evidence exists.

## Question / next boundary

MAIN should identify the precise pre-reservation refusal using independently reviewed DATA/source analysis or separately authorize a narrowly scoped no-effect diagnostic/source correction. This worker will not call internal gates/import controller/admission to bypass the one-call boundary, patch source/pins, manufacture failure artifacts or retry. Missing detailed diagnostics may merit a separately reviewed future failure-reporting change, not a repair under this terminal ticket.

## Preservation

Own question/handoff are the only new writes, authored AFTER authoritative terminal completion as dispatch permits. No other workspace write while CLI live. Pins/source/old artifacts unchanged; no token/output rewrite. Other-worker write quiescence remains MAIN-controlled. No runtime/P0/gameplay/performance/human acceptance. Complete command/env/exit/output/hash/cleanup limits in notes/handoffs/T127-world-1.md.
