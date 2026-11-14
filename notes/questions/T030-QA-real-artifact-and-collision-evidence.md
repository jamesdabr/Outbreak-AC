# T030 concrete artifact identity and collision observations

- Author / worker: QA/Performance, `01a1b92d-28be-7110-9ac6-7ae01476c117`
- Ticket and revision: T030 revision 0.5 RELEASED
- Phase and contract revision: P0 prerequisite subset / BROWSER_FOUNDATION 0.5
- Exact clause or interface affected: T030 criteria 1/4 require the lead-supplied real artifact identity; D005 read-only diagnostics contract requests fresh-input motion/collision observations.
- Status: OPEN (lead resolution is recorded separately)

## Question

When the linked artifact is ready, supply its accepted build identity, entry HTML,
and exact bundle file SHA-256 values under `web/build/out`. A build ID or synthetic
diagnostics alone cannot prove that a page contains the accepted engine. The
observer can bind its private CLI inputs to these file hashes without defining a
new shared build-manifest format or modifying build output.

Also identify the actual original-map collision scenario (obstacle/bounds, approach
and expected player clearance/stop) for a later collision assertion. D005 supplies
positions but no collider geometry or acceptance route. A stationary player can
mean collision, no input, or a bug; the observer must not infer collision success
from a plateau alone.

## Evidence and impact

`web/build/out` was absent at T030 start. The D005 diagnostics contract is sufficient
to implement strict schema/phase/map/frame/position validation, bounded fresh-input
and focus/pointer lifecycle observations, and negative synthetic tests. These
independent steps continue. Real checks stay NOT RUN until accepted artifacts are
identified. The observer never promotes a labeled fixture or a canvas/metadata
page to game evidence.

## Options for owner and lead

1. Supply accepted bundle identity/hashes and freeze the first actual-map collision
   route when reviewing linked T014 output; run the observer under that release.
2. Review the observer implementation and negative fixtures first, retaining actual
   game and collision checks as NOT RUN until integration evidence exists.

## Work paused

Only actual-game execution/PASS evidence and a definitive collision assertion.
No instrumentation/API, geometry, contract, build file or ticket change is made.
