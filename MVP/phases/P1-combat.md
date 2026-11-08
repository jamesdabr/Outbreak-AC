# P1 Multiplayer third-person combat

Revision: 0.2. Contract status: DRAFT. Phase state: PLANNED. Authority: owner and coordinating lead only.

## Entry conditions

P0 ACCEPTED.

## Required deliverable

Two connected browser clients render living full characters in shoulder view, move/aim/fire and exchange server-validated pistol/rifle damage. Share map queries, actor IDs and bounded simulation. Squad-friendly damage remains possible; inherited betrayal punishment is disabled for Outbreak.

## Acceptance gate

1. Camera retracts at walls/corners and recovers; living local model is visible without the first-person weapon overlay.
2. Reticle aiming and muzzle obstruction are tested at approved distances and near cover.
3. Server determines valid hits from approved queries rather than client hit lists; rejects invalid weapon, cadence, ammo, timestamp and duplicate requests.
4. Both browser clients agree on health/ammo/death after exchanges under the approved normal and impaired-network profiles.
5. Modified Outbreak clients/servers use the approved isolated protocol/connection configuration.

## Exclusions

No zombies, revive, construction, progression or extraction implementation in this phase.

## Tickets and handoff

Mandatory tickets: T004, T005. Each requires an individual RELEASED assignment and write allowlist. Evidence goes in `notes/handoffs/`. Questions go in `notes/questions/`. Only the lead may accept this phase, revise its criteria or release the next phase.
