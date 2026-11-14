# T145 RSS feasibility — notes handoff

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket/revision: T1451.0 RELEASED notes-only /D172; unchanged PLATFORM_DECISION0.1 RSS budgets. No selfacceptance/status change.
- Changed: NEW notes/proposals/T145-engine-RSS-method.md and this own NEW handoff only. All source/SDK/tools/old evidence/authoritative files/Git preserved.
- Proposal:8869bytes,1045 whitespace-delimited words, SHA25678d612410669ab2243800c976b55048190e751ea8c466412d1a4889216ccd6f6.

## Acceptance evidence

PASS bounded assessment, two paths only: owned Mach task high-waters with complete lifetime history; native direct-child sole wait4 reaper. Exact installed SDK15.5 header paths/line locations, byte fields/revision counts, wait ABI and kqueue limitations documented. Primary Apple OS source/documentation links distinguish published implementation from installed behavior. Existing T099 unresolved RSS section and accepted v4 supervisor’s competing poll/wait reapers read as DATA only.

PASS strict semantics: genuine per-task kernel high-water differs from sampled RSS. A complete sum of final per-process lifetime peaks is a conservative simultaneous-tree upper bound; incomplete census/terminal values invalidate that bound. Exceeding it is not proof simultaneous usage exceeded budget. Footprint/heap/normalized values cannot substitute. No invented child-count limit or pre-handle zero.

PASS access/coverage limits: task-name-compatible access is considered separately from debugger control/inspect policies; same UID is not installed hardened-Chrome permission proof. No privilege/entitlement/flag change proposed. Complete Chrome birth/pre-handle/transient/exit/reparent/PID/exec/cleanup coverage remains unproved; NOTE_TRACK/NOTE_CHILD unsupported since10.5 and NOTE_FORK does not deliver child PID through kevent. Current snapshot-based cleanup ownership is not a lossless RSS census. Permission-only or sampling stress success could not prove completeness.

PASS native path and qualification: one designated wait4 exact-child terminal reaper must replace every competing poll/wait consumer, preserve ownership/deadlines and retain raw ru_maxrss/exit/units. Published source implies bytes; archived Apple manual says kilobytes, so the explicit discrepancy requires installed confirmation before PASS. Child aggregation uses max rather than a summed tree peak. Early-exit usage can be retained by the direct-child reaper without assuming launch-handle interval zero; missing usage fails measurement.

Recommended smallest follow-up: MAIN may separately scope native reaper preparation then an approved bounded owned synthetic-child unit/early-exit/spike test. Chrome budget stays NOT_OBSERVED pending an actual reviewable lossless lifecycle/terminal-RSS method, not a threshold waiver or privileged instrumentation plan. This is a precise method gap, not a declaration that all independent P0 work is blocked.

## Work performed and remaining boundaries

Only named source/header/contract/proposal reads, primary Apple documentation/source browsing and builtin file hash/word-count metadata. No project imports/scripts/helper execution/tests/builds, live Mach/kqueue/rusage calls, process inspection/ps/lsof, browser/probe/native/network experiment, installed-package execution, system/privilege change or Git. No actual RSS/access/capability result generated or simulated; published main-branch source is not the running kernel’s identity.

No new execution permission is requested or inferred here. MAIN retains method/release decisions; future tests need their own exact scope/approval. T143 independent, QA paused, owner braking preference pending. Notes submitted for MAIN review; Engine returns to standby.
