# D003 Browser audit ticket drafting and first-wave dispatch

Authority: the owner explicitly instructed this coordinating chat to audit the browser port, compile the report, use subagents to write tickets, then hand jobs to the proper worker threads to work on them. The report was completed before subagents were started.

## Decision

Approve revision 0.3 of MVP/BROWSER_FOUNDATION.md for isolated prerequisite work only. Use subagents to write proposed tickets under notes/ticket-proposals; the lead reviews and adopts authoritative tickets. This delegation is drafting assistance, not transfer of contract authority.

Release ready T016-T020 assignments to the five existing worker chats after review, with explicit file ownership and execution scope. Retain T014/T015 as integrated proof gates and T021 as an unreleased transport follow-up. The full MVP gameplay parameters, final engine/transport choice and later phases are not approved by this decision.

## Experimental baseline

Current source commit: 13f0d8eea4822dee5c976661218d022be74342e3 plus preserved uncommitted prototype edits. Initial candidate: AssaultCube/WebAssembly; experimental SDK 7.0.0; first evidence target desktop Chromium on macOS arm64. Official SDK metadata was read at https://raw.githubusercontent.com/emscripten-core/emsdk/main/emscripten-releases-tags.json and identifies 7.0.0 as release 6afbd83493d647051772d491124187d4e9a0cda9. No SDK was installed by the audit.

## Existing worker mapping

- Engine & Multiplayer: 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- player combat: 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- World/Match-Systems: 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- QA/Performance: 01a1b92d-28be-7110-9ac6-7ae01476c117
- AI-Director: 01a1b92c-689a-71c1-820b-f1062dd0a82b

All are local and share the repository directory. Do not create duplicate chats or assume branches/worktrees have been requested. No model overrides were requested.

## Revision effect

Add the approved browser-foundation subset and clarify its release exception in governance/root instructions. Existing draft gameplay contracts remain drafts. Final ticket state and evidence are maintained in tickets/INDEX.md and notes/handoffs after actual dispatch; this record does not assert that a job has completed.
