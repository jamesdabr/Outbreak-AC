# Outbreak MVP product contract

Revision: 0.2. Status: DRAFT FOR OWNER AND LEAD DISCUSSION. Target: private playable MVP. Eight-player scope approved in D001; detailed contract remains under owner/lead discussion. No worker may implement this draft without a released ticket.

## Player experience

A player opens a web URL, loads the game without installing a native client, joins a match, and enters a compact Blackwood encounter map as a survivor. The survivor scavenges, fights other survivors and infected, can revive a stranger or betray a squadmate, and attempts to leave through a limited-capacity extraction before a fifteen-minute deadline. Equipment and resources reset every match. Surviving means actually extracting alive, not achieving the highest score.

## Included scope

- Browser delivery is the primary MVP platform. The client runs on the player's device in a supported browser, with a separate authoritative dedicated server. A downloadable native client is not a completion requirement. Browser/OS support and performance targets must be approved before implementation release.
- Eight simultaneous player client slots in the final MVP. LLM-controlled clients occupy ordinary player slots and must be reported separately from human participants. Earlier integration gates use two and four clients. A client connection is not a zombie slot.
- Private direct-connect/lobby setup, squads of one to four and no power progression. Squad membership is fixed at match start. A squad is not a damage immunity team.
- One compact greybox Blackwood map: one main combat area, at least one enterable structure and two viable approaches. Single-level native geometry is sufficient. Full-town dimensions and building counts are excluded.
- Third-person shoulder camera, obstruction handling, aligned aiming, run, sprint without stamina, crouch and jump. No slide, vault or shoulder switching requirement.
- Pistol and one automatic rifle, server-owned health, ammunition, reload and damage. Exact balance and loadout are frozen in PARAMETERS.md before the relevant ticket is released.
- Always-on PvP and full friendly damage, without inherited friendly-fire punishment, Rogue flags, enemy markers or safe zones.
- Alive, downed, eliminated and extracted states. Any living survivor can revive any downed survivor regardless of squad. Downed survivors crawl, cannot fire and can be finished. Elimination is final for the round. Own-squad-only spectating; when no eligible squad survivor remains, show the results/wait view without a free camera.
- Walkers with server perception, gunfire/noise response, valid navigation, melee attacks, hit/death replication and obstacle response.
- Finite loot consisting of ammunition, medical supplies and wood. No item trading interface is required; betrayal/rescue must work without one.
- One anchored wooden barricade recipe. Anyone can damage, repair or dismantle it. Material transactions are authoritative. Salvage returns less than the cost. No placement may block reserved extraction access.
- One extraction location and one announced departure per round. Limited capacity is visible to players. No crisis or route cancellation in the MVP.
- One identifiable Predator with front/flank command choices, local perception, audio plus visual command cues, and loss of coordination on death. It directs existing walkers rather than creating actors without budget.
- Director-lite: seeded, logged regional allocation and pacing within a fixed population budget, valid offscreen spawns and recovery intervals. It may not target a squad because of skill, change announced extraction rules or choose winners.
- HUD for health, ammo, timer, squad condition, wood, revive progress and extraction status; final results show extracted/eliminated/left-behind outcomes separately from optional match statistics.
- Developer diagnostics, a repeatable smoke scenario, multiplayer acceptance evidence and a manifest of assets permitted in the candidate build.
- A developer interface through which an external LLM tester can receive game state and issue ordinary player actions. Screenshot observations are not required. Detailed state visibility, actions, transport, adapter/provider and acceptance cases are deliberately deferred to a separate owner/lead contract. The interface must not let tester actions bypass normal server validation or make live game simulation wait for an LLM. This requirement is not permission to implement a particular interface yet.

## Match lifecycle

Lobby -> Deployment -> Active -> Results -> Lobby. The server starts active play only after configured participants are ready. Late connections after deployment are spectators until the next round; no mid-round survivor spawning. Spawn anchors are distinct across squads, keep squadmates together and are not revealed to opponents. Failure to allocate valid starts returns to lobby with a reason rather than silently relaxing spawn rules.

All deadlines use server simulation time. The first accepted boarding request obtains a seat; equal-tick requests are ordered by server receipt sequence, then actor ID. Clients cannot reserve seats by claiming earlier timestamps. Boarding requires a living, nondowned survivor in the valid zone. Boarding uses an uninterrupted hold; completion occupies a seat but is not extraction success. Boarded survivors remain vulnerable. Leaving the zone, cancelling, being downed, eliminated or disconnecting releases the seat. At departure the server first resolves due combat/down/bleed-out events, then extracts living boarded survivors, then marks remaining nonterminal players left behind. No client can be both extracted and eliminated.

Disconnect removes the actor from play, releases interactions/seats and records LEFT. No same-round survivor reconnect or replacement; the player may observe permitted squad members. Squadmates do not instantly die when their whole squad is downed. A fully downed squad remains rescue-eligible until each individual timer expires.

Match reset clears health state, equipment, materials, loot depletion, structures, actors, seats and timers. Only round results/logs survive; there is no persistent account database in this MVP.

## Explicit exclusions

Twenty-four-player scale, full Blackwood town, runners/brutes, multiple Predator variants, extraction crises, multiple extract routes, cover/spike traps and other recipes, vehicles, arbitrary terrain edits, freeform construction, live voice integration, accounts, cosmetics/unlocks, monetization, public matchmaking, a public master-server listing, advanced anti-cheat services, unapproved engine migration and broad renderer replacement. Browser compatibility work within a released ticket is in scope; changing the engine requires an owner/lead decision.

These exclusions apply to the MVP only. Workers may not implement them speculatively. Any change requires an owner/lead amendment.

## Definition of MVP complete

All phase gates through P5 and the later approved LLM tester interface contract are accepted; the required loop runs on the approved browser client and dedicated server build; every mandatory acceptance case has evidence; and the owner and lead approve the candidate. Simulated players can verify protocol/load behavior but do not replace the required human playtest. Syntax checks alone do not satisfy a build or gameplay gate.
