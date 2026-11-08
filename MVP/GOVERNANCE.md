# Contract governance

Revision: 0.5. Status: APPROVED FOR BROWSER PREREQUISITE WORK; gameplay phase contracts remain drafts. Contract authority: human owner and coordinating lead only.

## Source of truth

Higher-priority platform instructions and direct human instructions take precedence. Within project documents, an approved amendment recorded by the lead updates the referenced baseline; otherwise the MVP contract, parameters and interfaces govern phase contracts, which govern tickets. Tickets may narrow scope but cannot override a governing contract. The engineering brief and ENGINE_AUDIT.md provide context; they do not independently authorize worker scope or override these contracts.

On a conflict or missing behavior, workers write a question instead of selecting the most convenient interpretation. Existing prototype behavior is not approval of a different rule.

## Release and acceptance

The lead maintains all authoritative statuses. Contract states are DRAFT or APPROVED. Phase states are PLANNED, RELEASED, IN_REVIEW or ACCEPTED. Ticket states are DRAFT, READY, RELEASED, BLOCKED, SUBMITTED or ACCEPTED. A worker reports progress through notes without modifying these states.

A ticket can be RELEASED only when its governing contracts are APPROVED; required predecessor tickets/phases are ACCEPTED; all relevant parameters and interfaces are frozen; a named assignee, explicit file allowlist, base revision, contract revisions and verification plan are recorded; and existing overlapping edits are reconciled. The lead must record an exclusive write owner for shared files during execution. Two workers may not concurrently edit the same file without an explicit integration plan in both tickets.

Decision D003 approves `MVP/BROWSER_FOUNDATION.md` revision 0.3 as the governing subset for individually released T016-T020 experiments. These prerequisite tickets may start before P0 is accepted, and do not depend on unresolved gameplay values that they do not implement. They do not accept the complete P0 gate, choose the production engine/transport, approve draft gameplay contracts or release later tickets. All relevant experimental values and source ownership must still be frozen in their released tickets.

A worker submits a handoff with results for every acceptance criterion. The lead reviews the changes and evidence, performs integration checks appropriate to the change and accepts or returns the ticket. A phase is accepted only after all mandatory tickets and phase criteria pass. A successful compile is not runtime or multiplayer evidence. Missing evidence cannot be waived by a worker.

## Amendments

Only the owner and lead discuss and approve contract amendments. Workers may raise an issue and suggest options in a question note but must not negotiate scope with other workers or implement a proposed amendment.

The lead records each approved amendment in `notes/decisions/` with the human instruction or coordinating-chat decision, rationale, affected clauses/tickets, old and new revisions, and required revalidation. The lead updates every affected contract and ticket before re-release. Historical handoffs remain unchanged. Closed question notes remain unchanged; a separate resolution note links the decision and supersedes them.

The lead may resolve routine technical choices that preserve the approved product behavior. Player-facing scope changes, changed exclusions and changed acceptance thresholds must be discussed with the owner. No worker may resolve such choices by inference.

## Questions and blockers

Workers create `notes/questions/<ticket-id>-<worker>-<short-subject>.md`. Files are append-only by ownership: create a follow-up note rather than overwriting another note. State exactly which work is blocked. Independent released work may continue. No reply, elapsed time or proposed option constitutes approval. A resolution must identify the applicable decision and re-released ticket/contract revision before affected implementation resumes.

## Workspace and integration

All paths beginning `/MVP`, `/tickets` or `/notes` in project discussion mean directories relative to this repository root, not filesystem-root directories. The lead owns integration. Worktree/branch setup and commits are authorized only through explicit assignments or human instructions. Workers preserve unrelated edits and identify all pre-existing changes touching their allowlist before starting.

These documents establish agent workflow rules. They are not filesystem access controls; the lead must review changes for compliance.

Decision D004 extends the approved experimental subset to BROWSER_FOUNDATION.md revision 0.4 and individually released T022-T025/T017 revision 0.4. First-wave acceptance is limited to each ticket's actual scope; partial T016/T017 evidence does not accept T014 or P0.

D005 releases the exact integrated browser-foundation subset T026-T030 under BROWSER_FOUNDATION.md 0.5; no full phase/MVP acceptance is implied.
