# D002 Browser delivery is central

Authority: direct human owner statement in the coordinating chat on 7 November 2026, following discussion of browser delivery: "I think it is central". Recorded by coordinating lead.

## Approved direction

The MVP is browser-first. Players must load the game through a web URL without installing a native client. A separate authoritative dedicated server remains the architecture direction. Native client delivery is no longer a required MVP platform.

## Effect on draft contracts

Affected documents advance from revision 0.1 to 0.2: MVP overview, product contract, parameters, interfaces, P0/P1/P5 phase contracts, tickets T001/T002/T003/T004/T006/T012 and the ticket register. Add draft spike tickets T014 and T015 for browser rendering and multiplayer transport evidence. Unaffected contracts retain revision 0.1.

P0 must establish browser rendering, browser-compatible multiplayer transport, an owner/lead client foundation decision and reproducible browser/server builds. All later player-facing acceptance evidence uses browser clients. Downloadable native clients cannot substitute for that evidence. ENGINE_AUDIT.md remains a historical source audit; its native-build recommendation is superseded for delivery planning by this decision.

## Decisions still reserved

This does not select a browser support matrix, mobile/touch scope, toolchain, transport or replacement engine. Desktop keyboard/mouse is a proposal for the initial scope, not an implicit mobile commitment. AssaultCube remains a candidate; workers report findings and the owner/lead chooses whether to retain it. LLM tester interface detail remains deferred with game-state observations and no screenshot requirement.

## Release state

The updated contracts and tickets remain DRAFT. No worker is dispatched and no implementation is authorized by this amendment alone. Before release, the lead freezes the exact spike scope, dependencies, write allowlists and relevant technical decisions. No game source was changed for this decision.
