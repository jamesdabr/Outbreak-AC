# Ordinary grounding certificate and charged query schedule

- Author / worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket and revision: T180 revision1.0 / D277, notes-only plan
- Phase and contract revision: GOVERNANCE0.5; P1_RULES0.2; QUERY_CALLER_BRIDGE0.1; QUERY_PUBLICATION0.2; proposed H/T110/T139/draft2 movement materialization
- Exact clause or interface affected: H section4 ground/no-jump gravity reset, grounded sprint/jump/step eligibility and world-only support; T110 sections4–5 ordinary static tails and actual-floor landing; packet2 section9 query frequency envelope; actual p1_geometry.h public query results and opaque StaticStore
- Status: OPEN (lead resolution is recorded separately)

## Question

What exact existing-query certificate and update order establish/clear grounded for ordinary non-step movement, particularly a grounded actor walking off a ledge with no accepted jump, and how is a valid horizontal floor landing recovered from the coherent first record without reading private StaticStore cells?

Please bind the support test, when committed grounded is trusted versus revalidated, the ordering relative to gravity/sprint/jump integration and finalization, and the exact bounded query charge. A stationary classifier's Touching relation alone cannot distinguish support below the foot from a wall/ceiling contact. A moving-body stationary/tangent query is Clear, not a support normal. The proposed ordinary ground/no-jump gravity reset also means that a fresh downward displacement cannot be assumed without defining it. The dry-flat rule fixes what counts as walkable ground but does not itself supply that lifecycle/certificate or an opaque-cell accessor.

## Evidence and impact

Read-only inspection found `MotionState.grounded` and ground/no-jump remainder reset in `notes/proposals/T002-P1-headers.md` section4, and world-only grounding plus the explicit step Down actual-floor clause in `notes/proposals/T002-P1-common-timeline-addendum.md` sections4–5. `notes/proposals/MAIN-P1-definition-closure-draft-2.md` does not add an ordinary support recurrence. `source/outbreak/p1_geometry.h` exposes sweep/classify/headroom and metadata inspection, not raw static-cell access or a support result. No source/runtime test was run.

This is separate from the already pending owner braking-selector question and T176 M4 stance/flags materialization. It does not reopen radius, gravity, jump, step height, slope, tick duration or query semantics. The implementation plan can specify spans/rollback/storage and full evidence obligations now, but cannot freeze truthful ledge/landing goldens or implement a new support probe on inference. An additional support query must map into the original89508813 schedule rather than being free work.

## Options for owner and lead

1. Cite a previously frozen exact support/grounding recurrence and its existing public-data certificate, with its precise query slots and ordinary/step update ordering. Engine will consume it unchanged.
2. Freeze the missing private caller recurrence using existing query APIs and dry-flat geometry. Specify any support-probe shape/displacement/contact interpretation, coherent landing foot rule, and ordering, and reconcile every call with an existing bundle/tail slot. No new API, private World read, radius/epsilon/dt/cap increase is implied by this option.

A recommendation is not authorization: prefer a short explicit existing-query caller clause before source release. If neither option fits current records/caps, MAIN must resolve that exact seam rather than Engine supplying a new hook or guessing ground.

## Work paused

Future `prepare_once` grounded/gravity eligibility, `build_world_tail` ordinary support finalization, `try_step` exact landing-foot extraction and their expected support/ledge cases remain gated before implementation/golden generation. T180 source/evidence planning, resource arithmetic, full timeline/debt/rollback specification and the new handoff continued within the current notes-only lease. No source, tests, fixtures or authorities changed.
