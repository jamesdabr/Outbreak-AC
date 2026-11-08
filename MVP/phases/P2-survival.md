# P2 Four-player survival encounter

Revision: 0.1. Contract status: DRAFT. Phase state: PLANNED. Authority: owner and coordinating lead only.

## Entry conditions

P1 ACCEPTED; P2 parameters and map/anchor interfaces frozen.

## Required deliverable

Four clients join a compact greybox with server-run walkers, gunfire/noise perception and universal down/revive/elimination. Squad identities are independent of combat hostility. Include downed crawl and squad-only spectating.

## Acceptance gate

1. Four client connections observe the same 4-8 walkers pursuing, attacking, taking damage and dying under server authority.
2. Walkers follow valid indoor/outdoor routes, respect static geometry and log failed paths without teleporting.
3. A downs B; unrelated C revives B after the frozen uninterrupted hold; B can immediately damage C after the recovery lock.
4. Damage and bleed-out finish downed survivors; subsequent downs use the approved schedule; elimination cannot be reversed.
5. All-squad knockdown does not instantly eliminate anyone; spectator views cannot expose unrelated players or a free camera.
6. Revive interruption, simultaneous helpers, disconnect and late-observer state tests pass.

## Exclusions

No Predator, Director spawning, construction, economy persistence or extraction implementation.

## Tickets and handoff

Mandatory tickets: T006, T007, T008. Each requires an individual RELEASED assignment and write allowlist. Evidence goes in `notes/handoffs/`. Questions go in `notes/questions/`. Only the lead may accept this phase, revise its criteria or release the next phase.
