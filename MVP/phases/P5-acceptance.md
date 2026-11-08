# P5 MVP acceptance and candidate delivery

Revision: 0.2. Contract status: DRAFT. Phase state: PLANNED. Authority: owner and coordinating lead only.

## Entry conditions

P4 ACCEPTED for eight-player scope; all required assets and performance thresholds frozen. The separately deferred tester interface contract must be approved before T013 execution and final MVP acceptance.

## Required deliverable

Integrate the required systems, execute the acceptance matrix, produce a permitted private candidate and obtain owner/lead acceptance. Defects return through scoped tickets; QA cannot weaken contracts.

## Acceptance gate

1. Reproduce browser client and dedicated server builds from the documented baseline and run standard and smoke round profiles through the approved browser/OS matrix. Players load and join from a URL without native client installation.
2. Verify browser loading, keyboard/mouse control, pointer capture, audio activation, focus loss and disconnect behavior against the P0-approved platform contract. Complete the full MVP loop with recorded results for all earlier phase criteria and reconnect/reset/race cases.
3. Run the frozen eight-client, 12-walker, one-Predator performance/network profile; provide hardware, frame/tick distributions, traffic and failed-path counts.
4. Run a human playtest with at least four people; record actual participants, squad assignments, rounds, observed problems and replay interest without inventing results.
5. The separately approved tester interface acceptance cases pass and demonstrate an actual LLM driving a normal client through state/actions; scripted doubles are identified as such and do not substitute for the LLM evidence. Provider, cost and run limits require owner/lead agreement before this test.
6. Candidate uses only assets in the approved manifest, retains required notices and excludes private configuration.
7. No open contract violations remain. Owner and lead explicitly accept the candidate and MVP completion.

## Exclusions

No unapproved feature additions, dependency upgrades, public publication or claims of 24-player/horde readiness.

## Tickets and handoff

Mandatory tickets: T012, T013. Each requires an individual RELEASED assignment and write allowlist. Evidence goes in `notes/handoffs/`. Questions go in `notes/questions/`. Only the lead may accept this phase, revise its criteria or release the next phase.
