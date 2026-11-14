# T103 child-target pause ownership before guard installation

- Author: Player / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e.
- Ticket/revision: T1031.0.
- Contract: BROWSER_CAPABILITY_PROBE0.1, all created child targets remain paused until the same guard is installed; no automatic alternate method.
- Status: OPEN; MAIN records any resolution separately.

## Question and evidence

Installed Playwright coreBundle.js:37587–37593 adds worker sessions and sends Runtime.runIfWaitingForDebugger automatically, then enables worker auto-attachment. Its browser connection also enables auto-attachment at38109. A separate public CDP session installing its own paused-target handler must not assume it is the only debugger/resume owner. Protocol declarations alone do not establish whether another session's resume can release execution before our guard.

May the fixed probe use one same-origin iframe child check, keeping that frame under the already guarded primary target, and fail/leave NOT_OBSERVED if it becomes a separate target without a proved paused guard? This is within the contract's worker/iframe choice and avoids claiming an unproved independent worker-resume ordering. Alternatively MAIN could require a separately reviewed worker pause-ownership method before a child target is created. No actual browser or protocol call was made to resolve this.

## Independent work and affected boundary

Continue import-no-effects source/pure guards/cache/GPU/report/ownership fixtures and primary-target preparation. Do not add private Playwright connection access, alter installed auto-attach code, disable browser isolation or silently claim worker coverage. Actual child-target creation/resume method remains pending MAIN resolution; it is not permission to skip child/target coverage in acceptance.
