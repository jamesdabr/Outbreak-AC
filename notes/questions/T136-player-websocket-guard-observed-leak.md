# T136 — Fixed guard did not prevent owned disallowed WebSocket upgrades

- Author / worker: Player / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e.
- Ticket and revision: T1361.2, single actual D162 owner-approved diagnostic; worker status unchanged.
- Phase and contract revision: BROWSER_CAPABILITY_PROBE0.3/D108/D154/D162, prerequisite only.
- Exact clause or interface affected: Network.setBlockedURLs ordered allow-first fixture patterns plus wildcard deny must prevent disallowed HTTP/WS attempts, with zero sink requests/upgrades; unsupported/incomplete enforcement is failure without alternate method/retry.
- Status: OPEN (lead resolution is recorded separately).

## Question

How should MAIN resolve WS-guard feasibility after the ONE released actual run accepted the guard command but disallowed WebSocket handshakes reached both owned sinks? The run is terminal FAIL; no adjustment or further actual call is authorized.

## Evidence and impact

Human explicitly approved one local capability test in D162; platform review allowed the newly approved request. Exact approved caller SHA2a227ef4960bce08fd640152fd39ecbb959a4fbca8322a8e6b5dd05df02a7a06 ran once, zero-argument probe invocation, fixed Node24.19.0 with NODE_OPTIONS empty/NODE_COMPILE_CACHE unset. Previous D155 rejection remains historical before process creation, not an earlier actual run.

Report web/qa/capabilities/T103/run-1/report.json:29744bytes, SHA2e0fdca3546415b4d03efe98fc6853a653ffcad402337f29d428d554425d061a. status FAIL, error `denied HTTP/WS leaked or incomplete`, overall_scope PARTIAL. One cold navigation; warm/new-page/iframe checks not reached. All five saved capability check fields remain NOT_OBSERVED because the early denial assertion stopped before classification; do not rewrite them as PASS/FAIL.

Raw facts establish the stopping condition: Network.enable and exact ordered Network.setBlockedURLs completed before navigation. Allowed data/WS echo succeeded with outbreak-capability.v1. The HTTP denied URL produced CDP loadingFailed blockedReason inspector and sink HTTP count0. However ws://127.0.0.1:29877/denied reached denied-sink upgrade count1, and ws://127.0.0.1:29878/denied reached wrong-path upgrade count1. Both failed only with `Connection closed before receiving a handshake response`, not ERR_BLOCKED_BY_CLIENT. Fixture promise `blocked:true` alone was correctly insufficient, so the run refused the complete guard claim. This observes this fixed method/run; it is not a universal assertion about every Chrome configuration or alternative enforcement.

Raw independent own-canvas/SystemInfo facts were collected: Apple M3 Max/ANGLE Metal, own128x72 WebGL context, error0, no recorded context loss, viewport1280x720/DPR1. GPU check remains NOT_OBSERVED due early termination; no game GPU/performance claim. No warm cache/revalidation or iframe evidence exists.

Caller child8918 exit1, reaped under tool session44147; supervisor2.151626625098288s, stdout511bytes/stderr0, no signals/deadline/overflow. Probe elapsed1991.6609999999998ms. Cleanup PASS with no fallback/errors: Chrome8919 exited0, owned PGID8919 gone, profile removed, all fixture ports29876/29877/29878 plus control62476 rebound, lsof exit1/empty, listeners closed, acquisition cleanup complete, CDP sessions explicitly detached. All18 frozen preparation members remain byte/mode-identical. No retry, source/flags/private-API change, repair, or extra host test.

D108 remains explicit: early raw output NOT_OBSERVED/PUBLIC_HANDLE_NOT_AVAILABLE_EARLY/complete_byte_bound_proven:false. Actual post-handle778bytes plus report29744=30522bytes, no overflow; this does not bound early output. Pending game/physical media/frame/RSS/P0 gates unchanged; QA remains paused.

## Options for owner and lead

Retain this failure as installed-method feasibility evidence and keep dependent complete-guard measurement blocked. MAIN may separately authorize a reviewed investigation/proposal for a method preserving cache semantics; any alternate mechanism/policy/source and any new actual attempt require a new scoped release. Do not silently route/cache-disable, tune patterns/flags or rerun the immutable attempt.

## Work paused

All further T136 actual execution, source adjustments and run-1 writes. The released single call is consumed; only post-terminal own handoff/question reporting was performed. MAIN review/decision is required before any new work.
