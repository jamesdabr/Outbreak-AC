# P3 Four-player extraction core loop

Revision: 0.1. Contract status: DRAFT. Phase state: PLANNED. Authority: owner and coordinating lead only.

## Entry conditions

P2 ACCEPTED; P3 loot, construction and extraction parameters frozen.

## Required deliverable

Complete a four-player round with finite supplies, wood, one wooden barricade recipe and the server-controlled extraction lifecycle. Support standard fifteen-minute and two-minute smoke profiles using the same gameplay logic.

## Acceptance gate

1. Players spawn with the frozen loadout, find finite loot and cannot duplicate pickups or overspend wood.
2. Barricades obey anchor/cap/corridor checks, affect player movement and shots, and cause valid walker rerouting or barrier attack.
3. Any survivor can damage, repair or dismantle a structure; salvage and material changes agree across clients.
4. Two seats in the four-player profile are awarded by the contracted request ordering; downing, leaving, cancellation and disconnect release seats.
5. Only living boarded players succeed at departure; deadline combat ordering and terminal states match CONTRACT.md.
6. Late connections cannot spawn survivors; disconnect/reconnect and successive round resets do not preserve combat resources or objects.

## Exclusions

No additional recipes, item trading UI, multiple extracts, crises, Predator or Director implementation.

## Tickets and handoff

Mandatory tickets: T009, T010. Each requires an individual RELEASED assignment and write allowlist. Evidence goes in `notes/handoffs/`. Questions go in `notes/questions/`. Only the lead may accept this phase, revise its criteria or release the next phase.
