# P0 Foundation

Revision: 0.5. Contract status: released prerequisite subsets APPROVED in BROWSER_FOUNDATION.md; complete phase gate remains DRAFT. Phase state: RELEASED FOR PREREQUISITES ONLY. Authority: owner and coordinating lead only.

## Entry conditions

T017/T022-T025 may execute only under the approved browser-foundation subset and individual released assignments. Integrated T014/T015 and other P0 tickets need their own release after relevant prerequisites and decisions. No complete P0 acceptance is implied.

## Required deliverable

Produce isolated browser rendering and multiplayer transport proofs. Submit evidence to the owner/lead for the client foundation and transport decision. Then establish reproducible browser client and native dedicated server developer builds with exact dependency versions, isolated configuration and browser join/smoke steps. Submit the shared simulation/interface proposal. The lead freezes P1 interfaces, relevant parameters and performance reference/thresholds. Reconcile existing prototype edits before assigning overlapping files.

## Acceptance gate

1. A browser renders and controls a small test map using the proposed client foundation, with measured compatibility/performance and documented missing features.
2. Two browser clients exchange state through a separately running server using the proposed browser-compatible transport, with recorded latency/loss behavior and limitations.
3. Owner/lead records the selected client foundation, transport and supported browser/OS matrix before dependent production implementation.
4. A clean checkout plus documented prerequisites builds browser client artifacts and the native dedicated server; record commit, commands, toolchain and dependency versions.
5. Run the approved smoke procedure with two browser clients connecting to the dedicated server; no public registration or stock user settings writes.
6. Lead approves the concrete shared-interface addendum and fills every P0/P1 FREEZE REQUIRED parameter.
7. Lead records base revisions, source ownership and approved assets/configuration for the next phase.

## Exclusions

No new gameplay, unilateral engine switch, broad renderer rewrite, public deployment or speculative future-phase implementation. Minimal compatibility/transport changes are permitted only inside the released spike scope. A blocked AssaultCube browser path requires evidence and owner/lead decision; it does not authorize workers to substitute another engine.

## Tickets and handoff

Mandatory integrated tickets: T014, T015, T001, T002, T003. Prerequisite work/status is tracked under T016-T025 in tickets/INDEX.md; acceptance of a prerequisite does not accept the integrated gate. Each requires an individual RELEASED assignment and write allowlist. Evidence goes in `notes/handoffs/`. Questions go in `notes/questions/`. Only the lead may accept this phase, revise its criteria or release the next phase.

D005 releases the exact integrated browser-foundation subset T026-T030 under BROWSER_FOUNDATION.md 0.5; no full phase/MVP acceptance is implied.
