# Outbreak MVP contracts

This directory defines the playable MVP and the phased delivery contracts. The human owner and coordinating lead are the only contract editors. Workers execute released tickets and raise questions in `notes/questions/`.

Baseline revision: 0.5. Status: gameplay contracts remain DRAFT FOR OWNER AND LEAD DISCUSSION. Decisions D003/D004 separately approve the browser prerequisite subset in `BROWSER_FOUNDATION.md`; individually released tickets are tracked in `../tickets/INDEX.md`.

The owner selected an eight-player private playable MVP, reached through a four-player core-loop milestone, and requested a future game-state interface for LLM testers. These scope decisions are recorded in `../notes/decisions/D001-mvp-scope.md`. Browser delivery is now central, as recorded in `../notes/decisions/D002-browser-first.md`: the MVP must be playable from a web URL without installing a native client. Detailed gameplay values and technical contracts remain drafts for owner/lead discussion. Workers must not treat scope approval as ticket release.

## Read order

1. `GOVERNANCE.md`: authority, release, amendment and acceptance rules.
2. `CONTRACT.md`: MVP experience, included systems and exclusions.
3. `PARAMETERS.md`: exact behavior values and remaining lead decisions.
4. `INTERFACES.md`: shared technical decisions and approval requirements.
5. `phases/`: entry conditions, deliverables, exclusions and acceptance gates.
6. `../tickets/INDEX.md`: assignments and execution status.

For browser prerequisite work, read `BROWSER_FOUNDATION.md` before execution. `../BROWSER_PORT_AUDIT.md` supplies the completed source audit, while the approved subset and assigned ticket define exact implementation authority.

## Delivery phases

| Phase | Outcome | Gate |
| --- | --- | --- |
| P0 Foundation | Browser rendering/networking proofs, approved client foundation, browser build and dedicated server | Lead accepts build evidence and freezes the contracts required by P1 |
| P1 Multiplayer combat | Two browser clients move, aim and exchange server-validated damage in third person | Authoritative combat and camera tests pass |
| P2 Survival encounter | Four clients encounter server-run walkers and universally revive downed survivors | PvPvE and revive state remain consistent across clients |
| P3 Core extraction loop | Four-player match includes loot, barricade and extraction | Complete four-player round passes lifecycle and transaction tests |
| P4 Signature MVP | Eight-player round adds one Predator and Director-lite; tester interface is specified separately before implementation | Tactical cues, fairness and population budget tests pass |
| P5 MVP acceptance | Reproducible browser candidate and completed gameplay/performance evidence | Owner and lead accept the MVP |

Only the lead marks a phase accepted or releases dependent work. Phase order does not authorize a worker to start the next phase. Small fixes after submission need a re-released or new ticket.

First-wave review: T018/T019/T020 accepted within their inventory/tooling/documentation scopes; T016 remains SDK-blocked; T017 source follow-up and T022-T025 are released under the approved browser prerequisite subset. No integrated browser game has been accepted.

D004 next assignments: T022 SDK source/setup inspection, T017 clock follow-up, T023 selected-map dependency inventory, T024 browser WebGL diagnostics and T025 bounded offline local-auth completion. Current authoritative status is in tickets/INDEX.md; T014/T015/P0 remain unaccepted.

D005 releases the exact integrated browser-foundation subset T026-T030 under BROWSER_FOUNDATION.md 0.5; no full phase/MVP acceptance is implied.
