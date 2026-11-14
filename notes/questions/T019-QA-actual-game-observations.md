# T019 actual-game artifacts and observation expectations

- Author / worker: QA/Performance, chat `01a1b92d-28be-7110-9ac6-7ae01476c117`
- Ticket and revision: T019 revision 0.3 RELEASED
- Phase and contract revision: P0 revision 0.3 prerequisite subset; BROWSER_FOUNDATION revision 0.3
- Exact clause or interface affected: T019 Dependencies and Smoke runner contract: actual-game mode waits for lead-identified T014 artifacts and separately frozen actual-game observation expectations.
- Status: OPEN (lead resolution is recorded separately)

## Question

For the later actual-game run, what exact artifact root/build identity/document
URL and observable rendering/input/audio/network expectations does the lead
authorize? No such observation contract is supplied by T019, and
`web/build/out` was absent at the recorded preflight. No new game API has been
invented by this worker.

## Evidence and impact

`web/qa/results/preflight-authorized.json` records root state and the successful
existing Chrome launch. `web/qa/results/fixture-verification.json` verifies only
explicitly labeled fixtures. All fixture results carry `game_verified: false`
and NOT RUN game gates. Browser launch/page load cannot verify AssaultCube.
Independent preflight/server/fixture implementation and verification are complete
and can be reviewed without this future dependency.

## Options for owner and lead

1. Identify accepted T014 artifacts and freeze the exact actual-game observation
   expectations in a separately released assignment before integrated testing.
2. Review T019 as fixture-verified infrastructure while retaining actual-game
   behavioral checks as NOT RUN until the integrated prerequisite gate is ready.

Neither option accepts T014/T015/P0 or gameplay/performance gates.

## Work paused

Only actual-game browser behavioral checks and their observation integration.
No artifact root outside the QA fixture root has been served. No source,
contract, ticket or decision change is requested or performed by this note.
