# T002 Engine & Multiplayer proposal handoff

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T0021.0 RELEASED, D056/D061; submission for MAIN review, not self-acceptance.
- Phase / contract revisions: P0 proposal only; GOV/BROWSER_FOUNDATION/P0 0.5; CONTRACT/PARAMETERS/INTERFACES0.2 draft requirements used as proposal constraints. Existing experimental transport/backend0.2, network-client0.3/main0.1 remain unchanged.
- Base commit and pre-existing edits: ticket base13f0d8eea4822dee5c976661218d022be74342e3 plus preserved accepted browser/native prerequisite work. No clean-checkout claim; independent T070/T075/T077 work is not owned by this handoff.
- Changed files: NEW notes/proposals/T002-engine-architecture.md, notes/proposals/T002-engine-interfaces.md, notes/proposals/T002-engine-delivery.md, notes/questions/T002-engine-authority-freeze.md and this NEW handoff only.
- Commit or patch reference: none; no commit/push/branch/source/contract/ticket/decision edit.

## Acceptance evidence

PASS here means the requested proposal material is supplied, not that the
recommendation has been approved or implemented. All execution-dependent claims
are NOT RUN. No OS/toolchain/hardware performance result is claimed.

| Ticket requirement | Submission evidence / status |
| --- | --- |
| Full eight-player authority and unsafe existing seams | PASS proposal: architecture contrasts legacy server SV_POS/POSC and client GE_HIT with server-owned movement/combat/life/resources; isolates old app serializers, DM spawn, team penalties and local prototype. Retains renderer/native transport conditionally on MAIN foundation selection. |
| Concrete portable modules, signatures and world integration | PASS proposal: interfaces gives exact candidate signatures, fixed-point values, bounded queries/map import/wood/nav, typed IDs and adapter boundaries. Delivery gives exact future file ownership and exclusive overlap sequence. These are not adopted headers or leases. |
| Clocks, prediction, input and shot policy | PASS proposal:50Hz/20ms,25Hz snapshots,4 catch-up,200ms unhealthy-debt policy,160ms age/20ms future,100ms silence,80ms interpolation/extrapolation, bounded reconciliation and no target rewind; all await numeric freeze. Operational transport wall time is distinguished from gameplay ticks. |
| Exactly-once effects, bounded protocol and lifecycle | PASS proposal: OBP1 envelope/channels/limits, match/participant/connection/entity/life/request identity, terminal cache/input retirement, baseline/readiness, LEFT/no replacement, own-squad spectator, Results/Lobby reset and eight-slot successor transport recommendation. No change to current two-cap profiles. |
| P1–P4 complete gameplay seams | PASS proposal: two weapons/current-world camera/muzzle traces/full friendly damage; down/crawl/free universal revive; finite loot/medical/wood/placement/salvage; boarding/extraction; bounded Walkers/one Predator/seeded Director/eight-player squads. T071 values aligned as recommendations only. |
| MAIN admission ownership clarification | PASS proposal: admit_input/admit_action accept PeerInbox/PeerAdmission, never mutable canonical World. Single adapter thread owns operational rate/receipt/pending-body metadata between ticks; frozen cutoff prohibits reentry. Final request results, RNG/IDs and input ACK retirement are staged canonical state owned by advance_tick. |
| MAIN failure atomicity and memory clarification | PASS proposal: persistent heap World A/B, bounded staged events/encoded reserved outbox, one final commit. Solver/resource/event256/encoding/invariant faults discard candidate with no canonical/RNG/ID/ACK change. Post-commit delivery failure cannot roll back. Explicit initialization allocation failure, no large by-value stack objects, proposed64KiB kernel stack inside unchanged2MiB browser stack;8MiB shared-memory target and clone bandwidth require future measurement. |
| Dependency sequence and meaningful verification | PASS proposal: delivery stages0–7 with file owners, actual shared native/Wasm replay, failure-injection invariants, two then four/eight real browsers, privacy/load/impairment tests and separate human perception/LLM contract gates. No fake server or bare socket count substitutes for gameplay evidence. |
| Runtime/build/gameplay/performance acceptance | NOT RUN: notes-only release forbids compiler, project code, browser, native service and network execution. No authoritative gameplay, P0/platform acceptance, production engine selection or performance proof is claimed. |

Verification used read-only cat/sed/rg inspection and notes-only apply_patch.
Final formatting check: git diff --check (covers tracked workspace changes only;
new proposal notes also inspected directly). Reproduce content inspection with
`rg -n 'PeerInbox|Failure atomicity|StepFault|64KiB|HeadroomResult' notes/proposals/T002-engine-interfaces.md`
and read the companion architecture/delivery sections. Future tests are specified
in the delivery note and are not authorized or claimed executed here.

## Implementation status

Delivered five Markdown notes only. No implementation, simulation, test double,
build artifact, source API or runtime behavior was added. Existing accepted
transport/backend/data/source evidence remains historical prerequisite evidence.
MAIN reports T075 observer failure (raw1047 while B OPENING); startup versus
interframe cause remains unproven. T077 correction proceeds independently. This
handoff neither fixes nor accepts that run, nor treats legacy game proof as new
Outbreak authority.

## Integration and questions

No existing interface was changed and no dependency or asset was added. Future
source ownership is a proposed plan only; frozen headers and new exact file
leases must precede implementation. MAIN must separately resolve P0/foundation,
adopt interface/parameter addenda and approve implementation releases.

Open owner decisions are in notes/questions/T002-engine-authority-freeze.md:
boarding fairness versus completion, revive headroom/use conflicts, private
eight-slot identity/lease continuity, overload/no-rewind/batching and all numeric
freezes. Player's T071 proposal and tag-output question remain independently
owned. No worker dispatch or provider/API contract is inferred.

These new T002 notes are frozen on submission. MAIN reviews and records approval
or a narrowly released revision; this handoff does not amend authoritative status.
