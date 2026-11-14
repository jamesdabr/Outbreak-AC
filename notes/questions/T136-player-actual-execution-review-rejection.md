# T136 — Actual diagnostic rejected before process creation

- Author / worker: Player / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e.
- Ticket and revision: T1361.1, RELEASED by MAIN D154; worker does not change status.
- Phase and contract revision: BROWSER_CAPABILITY_PROBE0.3/D108/D154; browser prerequisite only.
- Exact clause or interface affected: ONE actual fixed caller invocation, separately released from the earlier human preparation-only resume; platform escalation approval.
- Status: OPEN (lead resolution is recorded separately).

## Question

MAIN supplied explicit D154/T136 actual execution authorization and the exact caller digest. Automatic approval review rejected the requested escalated supervisor before creating any process, stating that trusted human authorization covered only preparation and excluded the actual probe. Direct human approval of this specific actual diagnostic is needed before another execution request. No bypass, alternate permissions attempt or indirect launch was made.

## Evidence and impact

Read D154, T1361.1, capability0.3, the full fixed caller and confirm-cross-system-execution skill. Read-only identity checks matched caller SHA8dec5cb9c2933bacd032d6da63d1ddd28cf8b45fd58c403c4c259587791ab1e6, fixed Node SHA27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1 and accepted freeze SHAc9022e2af4875c3affa44977940653149fbfa1a83f248a416ddeb3e2b0390640. Actual run-1 was absent.

Requested exact child argv: `/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node /private/tmp/outbreak-T136-caller.cjs`, cwd `/Users/jd1/code/apps/outbreak`; NODE_OPTIONS empty, NODE_COMPILE_CACHE unset. The inspected inline Python stdlib supervisor would invoke that child once, bound combined output8MiB, begin owned-group timeout handling at135s and reap the exact child within150s. Escalation justification: "Run one approved isolated local Chrome capability diagnostic and close its owned resources."

Tool outcome: `CreateProcess ... Rejected`, not an executed child exit. Exact review reason:

> The command launches the actual browser capability diagnostic, creates run-1 artifacts, listeners, and child processes, while the trusted user authorization only resumed T103 preparation and explicitly excluded a real probe run.

The review also explicitly prohibited a workaround or indirect execution. No supervisor/caller/Chrome/listener started from this rejected request. Actual invocation count0; no actual command exit/time/report/capability or cleanup measurement exists. Post-rejection read-only verification found all18 frozen members unchanged and run-1 still absent. No fixture rerun, source/cache/reference edit, permission retry or actual fallback.

The concrete effects requiring confirmation are one isolated headed Chrome, public Playwright/CDP, the three owned loopback fixture listeners29876/29877/29878 plus its loopback control endpoint, approved ps/lsof observations and owned cleanup, with new output confined to run-1. No game/native/gateway/remote/install or QA resumption.

## Options for owner and lead

Obtain direct human approval for precisely this actual fixed diagnostic, then resolve execution approval before any new invocation. Alternatively retain the accepted preparation without actual capability evidence. Neither this note nor elapsed time authorizes execution or changes the released method.

## Work paused

All T136 actual execution and run-1 creation. Accepted T103 preparation stays frozen. No independent T136 runtime work remains safe to execute under the rejection; read-only reporting is complete.
