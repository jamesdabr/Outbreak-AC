# Local authentication failure has no disconnect implementation

- Author / worker: AI-Director
- Ticket and revision: T025 / 0.4 RELEASED
- Phase and contract revision: P0/BROWSER_FOUNDATION/GOVERNANCE 0.4
- Exact clause or interface affected: T025 criterion 2, explicit existing auth failure semantics for ineligible current local requests
- Status: OPEN (lead resolution is recorded separately)

## Question

`server.cpp::disconnect_client` immediately returns unless the slot is ST_TCPIP. Should a rejected current ST_LOCAL request remain without a continued handshake after an explicit DISC_AUTH diagnostic and the existing disconnect_client call, or should a future specifically authorized local failure path also tear down/reset that local connection?

## Evidence and impact

The native completion failure path calls disconnect_client(cn, DISC_AUTH). That function's guard excludes ST_LOCAL; it cannot clean up a local peer. T025 requires ST_LOCAL/no-auth only and explicit auth failure for ineligible current requests, but does not define a new local-disconnect/reset policy. Calling the existing failure path cannot be described as a completed local disconnect. Wrong-type, wantauth and needsauth local fixtures can verify rejection/no continuation/ownership without claiming a real local failure handshake.

## Options for owner and lead

1. Accept explicit diagnostic plus existing DISC_AUTH rejection call with no success/continuation as this micro-adapter's bounded failure behavior; local teardown remains later work.
2. Freeze and release a local teardown/reset/error-state policy with exact ownership and validation. Avoid silently granting success or invoking remote peer operations on ST_LOCAL.

## Work paused

No new local teardown or client reset is implemented without a decision. Independent eligibility, stale-slot discards, bounded queue processing, existing completion path, fixtures and native syntax checks continue. The handoff will identify local failure teardown as unresolved, not accepted runtime behavior.
