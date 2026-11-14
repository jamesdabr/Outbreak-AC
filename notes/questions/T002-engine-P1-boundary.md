# P1 combat-only scenario completion at the full-round boundary

- Author / worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket and revision: T002 revision1.1, D096 notes-only proposal
- Phase and contract revision: P1-combat0.2 draft; P1_RULES0.1 and PLATFORM_DECISION0.1 approved
- Exact clause or interface affected: P1 excludes extraction; CONTRACT0.2 requires900s round/extraction lifecycle; proposed TrustedKind::EndP1Scenario, ResultsReason and AbortReason::P1ScopeBoundary
- Status: OPEN (lead resolution is recorded separately)

## Question

What explicit evidence-only terminal policy should the P1 combat build use before
P3 departure/boarding/extraction exists? The new three-note proposal supplies
complete fields and proposes a private EndP1Scenario control for early P1 results,
with a tagged scope-abort at active_start_tick+45000 if reached without P3.
Neither is an MVP extraction success or a changed900s/last180s product rule.

## Evidence and impact

MVP/phases/P1-combat.md excludes extraction; MVP/CONTRACT.md requires the full
extraction lifecycle and MVP/P1_RULES.md forbids reporting an unhealthy attempt
as normal success. P1_RULES does not explicitly define a healthy combat-only
scenario's terminal result before P3. The proposed enum/control/status behavior
needs MAIN resolution before its implementation, not a worker-chosen exception.
See notes/proposals/T002-P1-{headers,wire,seams}.md, lifecycle/result sections.

## Options for owner and lead

1. Approve the proposed evidence-only control and explicit P1 scope-boundary
   abort, retaining full final lifecycle as a later mandatory implementation.
2. Define a different explicit P1-only scenario completion result at the boundary,
   still distinct from full-MVP extraction; revise the proposal enums/semantics
   through the normal interface review before dependent release.

Recommendation: option1 makes unimplemented scope visible without inventing an
extraction result. This is a proposal, not authorization or an approved exception.

## Work paused

No implementation is released; all P1 implementation already waits on P0 and
MAIN interface approval. Only adoption/implementation of this scenario terminal
policy specifically awaits resolution. The complete notes/handoff can be reviewed
independently. No source, contract, ticket or prior proposal is changed.
