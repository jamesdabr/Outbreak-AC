# Outbreak agent instructions

## Authority and mandatory reading

The human project owner and the lead agent in the coordinating chat are the only authorities allowed to define, approve or amend Outbreak scope, phase contracts, ticket contracts, balance values and shared interfaces. Workers must not assume the lead role. A worker assignment must explicitly identify the worker and ticket.

Before implementation, read `MVP/README.md`, `MVP/GOVERNANCE.md`, `MVP/CONTRACT.md`, `MVP/PARAMETERS.md`, `MVP/INTERFACES.md`, the assigned phase contract and the assigned ticket. Follow higher-priority platform and user instructions where applicable.

For the browser prerequisite wave, also read `MVP/BROWSER_FOUNDATION.md`. Its approved revision 0.5 and an individually RELEASED prerequisite ticket authorize only the isolated work defined there under decisions D003/D004/D005; unresolved draft gameplay contracts do not grant additional scope.

For T147 portable core/hash prerequisite work, also read approved `MVP/SHARED_HASH_FOUNDATION.md`0.1/D174. It authorizes only that individually released isolated subset before full P0, with no gameplay or production integration release. Existing numeric/envelope/map APIs and all other phase gates remain.

Only a ticket with status RELEASED, a named assignee, accepted dependencies, an explicit write allowlist and pinned contract revisions authorizes implementation. DRAFT, READY, BLOCKED, SUBMITTED and ACCEPTED tickets do not authorize new implementation. Do not implement future phases speculatively.

## Worker restrictions

- Do not edit `AGENTS.md`, anything in `MVP/`, anything in `tickets/`, or lead-owned decisions in `notes/decisions/`. Do not change your own ticket status, acceptance criteria, scope, ownership, dependency list or allowed files.
- Work only inside your released ticket's write allowlist. Read-only inspection of other project files is allowed. A broad folder allowance does not override an explicit exclusion.
- Do not change another worker's code, reset/clean the working tree, revert unrelated edits, create/delete branches or merge/cherry-pick work without an explicit assignment authorizing it.
- Internal implementation choices are allowed only when they preserve every contract, interface, parameter and acceptance criterion. Do not change observable behavior to make a test pass or quietly substitute local simulation for multiplayer implementation.
- Do not amend a contract because it seems inefficient, infeasible or inconsistent with existing code. Record a question and stop only the affected work. Continue independent authorized work where possible.
- Do not add dependencies, change engine, wire formats, shared interfaces or asset permissions without the lead's recorded authorization.
- Do not launch services, publish builds, push to GitHub or contact external systems unless the ticket or direct user instruction explicitly authorizes that action.

## Questions and delivery

Write questions as new Markdown files in `notes/questions/` using `notes/QUESTION_TEMPLATE.md`. Identify the ticket, contract clause, ambiguity, impact and proposed options. Do not edit another author's note. A note is not authorization.

Creating your own question note is permitted even when implementation is unreleased or blocked. Creating your own assigned-ticket handoff is also permitted outside the source write allowlist. These note permissions do not authorize source, contract or ticket edits.

Write completion evidence in a new file under `notes/handoffs/` using `notes/HANDOFF_TEMPLATE.md`. Report implemented, simulated and incomplete behavior separately, with reproducible verification and changed files. The lead reviews the handoff and changes authoritative status.

Re-read ticket and contract revisions before starting and before submission. If an assigned revision changes or an overlapping edit appears, stop affected work and notify the lead through a question note. Preserve pre-existing uncommitted edits. Do not dispatch or instruct other workers unless the lead explicitly assigns that responsibility.
