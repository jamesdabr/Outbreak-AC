# MVP parameters and frozen decisions

Revision: 0.2. Status: DRAFT. Values below are proposed owner/lead decisions. Workers may not tune or amend them. FREEZE REQUIRED rows prohibit release of dependent implementation until the lead records an approved value.

| Parameter | Proposed contract value |
| --- | --- |
| Final player capacity | 8; approved by owner in D001 |
| Squad size | 1-4 |
| Match duration | 900 seconds; dedicated smoke profile 120 seconds |
| Active extraction window | Last 180 seconds; smoke profile last 30 seconds |
| Extraction departure | Exactly at match deadline |
| Seat capacity | 4 in eight-player MVP; 2 in four-player integration profile |
| Boarding hold | 2 seconds uninterrupted; movement outside zone or damage interrupts the hold |
| Base health | 100 |
| Bleed-out | 30 seconds on first down, 20 on second, 10 on third; fourth lethal event while alive after three prior downs eliminates directly |
| Downed health | 100 independent of living health; received damage reduces it |
| Revive hold | 5 seconds uninterrupted; either actor taking damage, helper firing/moving out of range, losing line of sight or releasing input cancels progress |
| Revived health | 40; no armour or combat immunity granted |
| Recovery lock | 1 second without firing after revive |
| Simultaneous revive helpers | One accepted helper per target; server receipt order wins; no progress stacking |
| Revive item cost | None |
| Friendly damage | 100% of ordinary player damage; no automatic kick/ban/score punishment for betrayal |
| Materials | Wood only; carry cap 12 |
| Wooden barricade | Cost 3 wood; placement hold 2 seconds; intact salvage 2 wood; damaged salvage 1 wood; destroyed salvage 0 |
| Structure cap | 4 per creating player and 12 per original squad; creation identity persists through disconnect; removed objects release cap |
| Predator count | At most 1 active; no automatic respawn in a round |
| Walker cap | 12 living at once including Predator-directed walkers; Predator is additional |
| First playable encounter | 4-8 walkers; final controlled test 12 walkers plus 1 Predator |
| Primary client platform | Web browser; no native client installation required; approved in D002 |
| Browser and OS support matrix | FREEZE REQUIRED in P0; desktop keyboard/mouse is the proposed initial scope, mobile/touch support is not assumed |
| Browser client foundation and transport | FREEZE REQUIRED in P0 after rendering/networking spike evidence; workers cannot switch engines or select a transport unilaterally |
| Dedicated server development target | macOS arm64 retained for local development; production hosting target deferred |
| Initial load/download/memory and browser input/audio behavior | FREEZE REQUIRED in P0 alongside browser performance profiles |
| Initial server fixed tick | FREEZE REQUIRED in P0 with shared simulation contract |
| Snapshot cadence and interpolation | FREEZE REQUIRED in P0 |
| Player movement validation/prediction and shot timestamp policy | FREEZE REQUIRED in P0; claimed client hits cannot authorize damage |
| Weapon damage/rate/magazines/reload/spread/headshot rules | FREEZE REQUIRED before P1; only pistol and one automatic rifle |
| Starter ammunition, loot amounts and medical item behavior | FREEZE REQUIRED before P2/P3 |
| Move/sprint/crawl speeds and collision dimensions | FREEZE REQUIRED before P1/P2 |
| Revive/boarding ranges and hit interruption semantics | FREEZE REQUIRED before P2/P3 |
| Walker HP, damage, cadence, perception/noise ranges | FREEZE REQUIRED before P2 |
| Barricade HP, repair cost/rate, damage interruption and anchor bounds | FREEZE REQUIRED before P3 |
| Spawn separation, reachable loot and traversal bounds | FREEZE REQUIRED before P2/P3 after greybox measurement |
| Predator HP, perception/memory, command cooldowns and cue assets | FREEZE REQUIRED before P4 |
| Director spawn distance/visibility checks, regional budgets, cooldowns/recovery | FREEZE REQUIRED before P4 |
| LLM tester state/action interface and validation | DEFERRED for later owner/lead discussion; game-state observations, no screenshot requirement; T013 cannot be released until its separate contract is approved |
| Performance reference hardware, resolution, FPS/tick/bandwidth thresholds | FREEZE REQUIRED in P0; gates cannot be weakened after measurements without an amendment |

Once approved, production values may change only through a recorded amendment. The smoke profile may shorten time and reduce participant/seat counts exactly as specified; it may not bypass authority, collision, revive, loot or boarding logic. Debug overrides must be explicit, logged, excluded from acceptance runs and authorized in the ticket.

D084 freezes the platform/reference/initial measurement subset in APPROVED PLATFORM_DECISION.md0.1. D086 freezes matching P0/P1 numeric/behavior rows in APPROVED P1_RULES.md0.1. Those addenda supersede corresponding FREEZE REQUIRED rows above; later-phase values and full implementation interface records remain pending. No gameplay ticket is released merely by this freeze.
