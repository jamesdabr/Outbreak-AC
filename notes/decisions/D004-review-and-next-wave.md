# D004 First-wave review and ready follow-up assignments

Authority: human owner instructed MAIN to check worker chats, review completed work/questions, and hand out ready tickets. The lead inspected all five completed handoffs, all six question notes, authored source/tool changes and saved QA evidence.

## Review outcomes

- T018 ACCEPTED as metadata inventory/generator only: 11 fixture tests independently rerun; fresh inventory matches saved deterministic output, 22 entries/513359 bytes, 27 unresolved records, readiness false. Incomplete game closure and permissions remain truthful downstream blockers, not failures of this inventory ticket.
- T019 ACCEPTED as QA infrastructure only: 12 static-server tests independently rerun successfully; reviewed smoke/preflight code and saved healthy/error/missing/external/timeout Chrome fixture evidence. Actual game observations remain unverified.
- T020 ACCEPTED as documentation-only separation plan: verified common initserver/serverms initialization, deferred worker creation before nondedicated return, local handshake and source ownership proposals. This accepts no runtime adapters or measured budget.
- T016 BLOCKED after partial submission: useful preflight/probe and narrow headers, but no pinned SDK and no actual Wasm objects. Do not waive release/debug Wasm criteria.
- T017 re-released at revision 0.4 for the source fix below; it remains partial until actual Wasm TU evidence. Native main.cpp release/debug syntax checks independently pass. Existing protected combat files match D003 hashes.

Lead evidence and current source fingerprints are in D004-review-baseline.json. Existing worker handoffs and question notes are retained without editing.

## Question resolutions and routing

1. T016 SDK prerequisites and T017 Wasm prerequisites: release T022 to Engine for inspect-first official SDK source acquisition and exact setup proposal. This authorizes source download/inspection only, not execution of unfamiliar installer code or compiler port fetches. The lead can freeze a concrete setup command after reading that evidence. T016 remains blocked; T017 may complete independent source/native checks.
2. T017 shared embedded clock: approve bounded OFFLINE_MAP simulation for the browser experiment. Client-local gameplay delta is 0 on reset and capped at 250 ms thereafter; the retained offline embedded simulation follows that same bounded clock by design. It is not a real-time standalone-server benchmark. Native branches and separately running dedicated-server clock code remain unchanged. Any future NETWORK_CLIENT must have a separately frozen clock/transport contract. This resolves the contradictory experimental clause without changing the production match timer.
3. T018 dynamic/map closure: select existing packages/maps/official/ac_complex.cgz for READ-ONLY dependency inventory only, together with common startup roots. T023 expands metadata parsing, inspects embedded configuration as data and records replacement/permission blockers. No stock media pack, distribution or permission clearance is approved.
4. T019 actual-game observations: actual-game root remains absent, so observations remain deferred to T014. Release independent T024 to measure browser WebGL capabilities through an explicitly labeled diagnostic fixture; it is not an engine rendering or gameplay pass.
5. T020 service boundary: approve the first OFFLINE_MAP experiment retaining the existing bounded local protocol/simulation. Release only the small T025 server-side deferred no-auth adapter: one queued local/no-auth request per poll, same-thread completion, preserved stale-client validation, explicit rejection of remote/auth requests. Other service changes and the future NETWORK_CLIENT interface remain deferred. No blanket successful stubs or global semaphore/thread shims.

## Revalidation and ownership

BROWSER_FOUNDATION revision 0.4 governs the next isolated wave. T017 owns main.cpp; T022 Engine-owned SDK inspection files; T023 World-owned asset inventory; T024 QA-owned WebGL diagnostic; T025 AI-owned server.cpp deferred-processing adapter and its exact isolated tests. No overlap or public protocol change is authorized. T014/T015/T021 remain unreleased pending real prerequisites.

Only the coordinating lead updates contract/ticket status. Do not interpret these technical experiments as full gameplay approval, final engine/transport selection or acceptance of browser multiplayer. No source implementation was performed by MAIN during this review; worker source edits are reviewed and retained.
