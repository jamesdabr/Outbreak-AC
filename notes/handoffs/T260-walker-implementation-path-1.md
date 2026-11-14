# T260 — Smallest real server-run walker encounter

AI & Director · T2601.0 · D434/VISIBLE_SLICE0.1. Read-only source inspection; no implementation, build, helper, runtime, Git or network execution. Only this handoff written. MAIN owns the next contract/release.

**Recommendation:** after the visible survivor baseline, add a separate server-owned infected actor on a short collision-checked Blackwood route, then aggro, melee, survivor weapon damage and death replicated to observers. MAIN can designate a smaller demonstration before the contracted 4–8-walker encounter. Keep Predator/Director out of this increment.

## Reusable paths and actual boundaries

| Path | Reuse / missing work |
|---|---|
| `source/src/server.cpp:4627` `serverslice()` | Dedicated-server update/time hook (`sg->gamemillis`); add bounded infected update here, respecting pause/map reset. Existing `processevents()` supplies the combat-event integration point. |
| `source/src/bot/bot.cpp:90` `CBot::Think()`; `bot_ai.cpp` `FindEnemy()`/`HearSound()`; `bot_waypoint.cpp:2322` `CBot::AStar()` | Useful perception, pursuit and route-following references, **not a server module**. `clientgame.cpp:785` calls `BotManager.Think()`; bots use `player1`, `lastmillis`, `playerent`, weapons and client `moveplayer()`. Makefile `SERVER_OBJS` excludes bot objects. Do not port the whole bot manager. |
| `clientgame.cpp:550` `newbotent()`; `botmanager.cpp:872` `CreateBot()` | These allocate ordinary player/client numbers and put entities in `players`. They cannot be the infected actor architecture. `CBot::SendBotInfo()` merely rate-limits a timestamp; it does not implement infected replication. |
| `server.cpp:472` `buildworldstate()` / `:4495` `sendworldstate()`; `clients2c.cpp:143` position parsing | Reuse transport/send scheduling and interpolation patterns. Current positions are client-numbered player streams. Add distinct server-originated infected lifecycle/state messages with stable actor identity/version, initial observer state, death/removal and reset handling; never consume human slots or accept client infected movement. |
| `server.cpp:1912` `serverdamage()`; `serverevents.h:36` shot processing | Reuse survivor damage/publication machinery through an explicit infected attack-source adapter. Current attacker/target are `client*` and shot hits resolve client identities. Add server-validated survivor-to-infected hits and infected health/death; do not fabricate a client attacker or trust client hit claims. |
| `serverchecks.h` `checkclientpos()`; `serverfiles.h` `servermap` | Existing server floorplan/border checks are coarse player checks, not a complete navigation/LOS/collision solver. The client bot's visibility/`moveplayer` dependencies are missing server adapters. First provide authoritative static collision/LOS and a validated short route; path failure stops/reports instead of teleporting or walking through walls. No new general navigation framework is needed for that first route. |
| `rendermodel.cpp:953` `renderclient()` / `:1101` `renderclients()` | Reuse lower-level `rendermodel()`/MD3 animation loading. `renderclient()` dereferences player weapons/team/spectator state; use a separate infected render loop and snapshot presentation object, without client AI or invented player IDs. |

## Asset and minimal ownership split

The approved Blackwood pack at `web/assets/blackwood-profile/pack-root/packages/models/outbreak/` contains survivor/pistol/rifle MD3s and notices; survivor has idle/run/attack/pain/death animations. I found **no packaged walker model/skin** there. `packages/audio/outbreak/walker_attack.wav` exists in that pack. MAIN must approve an infected visual/animation mapping, or an explicitly temporary distinguishable use of the existing humanoid; audio alone is not an enemy visual.

- **AI & Director:** new isolated infected state/update module: separate bounded actor pool, idle/notice/pursue/melee/dead behavior, target/noise memory and route failure. No edits to legacy bot/player allocation.
- **Server/World integration owner:** server tick/reset, actual collision/LOS/route adapter, server combat adapter and infected lifecycle/snapshot serialization; freeze shared identity/messages before source release.
- **Client/asset owner:** decode separate actor snapshots, interpolation/render/death/removal and approved model packaging. Coordinate `clients2c.cpp`/`rendermodel.cpp` with MAIN’s current visible-client ownership.

## Decisions MAIN still needs

`MVP/PARAMETERS.md` leaves walker HP, damage, attack cadence, perception/noise ranges and movement/collision dimensions unresolved for P2. Also freeze speed, melee reach/LOS/windup/cooldown, memory/retarget/repath limits, collision-checked spawn/route and snapshot/update cadence. Existing scope is 4–8 walkers initially, maximum12 living walkers; eight human slots remain separate, Predator additional later. `MVP/phases/P2-survival.md` requires shared server authority, indoor/outdoor routes, obstacle respect and replicated damage/death. MAIN should select the exact visible increment and numbers, without importing armed-bot skill defaults or the local `outbreakstate.h` revive prototype as balance authority.

STOP after delivery. No proof corpus/framework, additional proposal packet, source permission, runtime result or P2 acceptance is claimed.
