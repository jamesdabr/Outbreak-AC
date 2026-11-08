# Outbreak application audit

Audit date: 7 November 2026, America/New_York.

Outbreak can reuse AssaultCube's shooter client, networking transport, dedicated server infrastructure, editing tools and several gameplay primitives. Its extraction mode and server-simulated PvPvE world require substantial new implementation. The most consequential work is server authority, infected simulation, dynamic object replication and collision, and separating squads from AssaultCube's two teams.

Recommendation: continue building the first playable on this codebase. Keep the initial map within the native geometry model and establish an authoritative multiplayer encounter early. This is a source-level recommendation, not a successful runtime or performance certification.

## Scope and evidence

- Repository: `https://github.com/jamesdabr/Outbreak-AC.git`.
- Committed baseline inspected: `13f0d8eea4822dee5c976661218d022be74342e3`, dated 17 June 2023, subject `Revert "editor camera bugfix"`.
- The working tree contains concurrent, uncommitted Outbreak prototype edits. These were inspected and preserved. Prototype observations below describe the working-tree snapshot, not the committed baseline or a completed feature.
- Source inspection covered build configuration, camera and rendering, physics, weapons, server packet handling and events, bots and navigation, map storage, pickups, audio and representative license notices.
- Twelve selected C++ translation units passed syntax checks on this machine. No linked executable, running dedicated server, multiplayer session, playtest or load test was demonstrated by this audit.
- The engineering brief supplies the intended game direction. Proposed tickets below refine implementation sequencing without changing product rules.

## Reuse assessment

Here, reuse means an implementation foundation exists. It does not mean an Outbreak acceptance test has passed.

| System | Assessment | Evidence and required work |
| --- | --- | --- |
| Arcade movement | Reuse and extend | `source/src/physics.cpp`: movement, gravity, jumping, crouching and collision. `clientgame.cpp`: local and remote player movement. Tune run/sprint and add downed movement; vault/slide remain separate work. |
| Weapon mechanics | Reuse and extend | `weapon.cpp`, `weapon.h`, `entity.h`: weapon classes, hitscan, recoil, magazines, reloads, grenades and effects. Retune for Outbreak; replace trust in client hit lists. |
| Dedicated server | Reuse and extend | `server.cpp`, `server.h`: connections, player state, events, pickups, match time and damage. Add fixed simulation steps and authoritative world actors. |
| Network transport | Reuse | Bundled ENet; client connections and protocol serialization in `client.cpp`, `clients2c.cpp`, `protocol.*`. Transport need not be replaced to implement Outbreak. |
| Gameplay replication | Substantial extension | `server.cpp::buildworldstate()` aggregates client position/message buffers. Add server-created infected, structures, inventory and extraction snapshots, join synchronization and stable entity IDs. |
| Third-person camera | Extend existing foundations | `rendergl.cpp::recomputecamera()` already has third-person spectator follow cameras. Add a controllable shoulder camera, obstruction handling and coordinated aiming. |
| Character rendering | Reuse pipeline with new assets/states | `rendermodel.cpp::renderclient*()` renders full characters and weapon attachments. Render the living local player in shoulder view; add downed, revive and infected animations. |
| Renderer | Reuse for the first playable | Existing OpenGL world/model/particle/shadow rendering. Legacy matrix/immediate-mode calls are present. Modern rendering and a new content pipeline are larger independent projects. |
| Map editor and storage | Reuse within limits | `editing.cpp`, `worldio.cpp`, `world.h`: in-game editing, entity placement, compressed map storage and metadata. Add authored Outbreak anchors and validation. |
| Native world geometry | Restricts design | `world.h::sqr` stores one floor and ceiling per horizontal cell. Ordinary stacked rooms cannot be authored as native cube geometry. Model/clip workarounds need separate collision, AI and server verification. |
| Bot navigation | Selective reuse | `bot/bot_waypoint.cpp` contains authored/flooded waypoints and incremental A*. Useful algorithms and tools; not a ready dedicated-server navigation system. |
| Zombie AI | New server system | Existing bots are armed player-like client entities. Add walker perception, pursuit, attacks, health, spawning and replication on the server. |
| Predator and Director | New systems | No implementation of the specified leader coordination, regional encounter budgets, extraction crises or logged policy decisions was identified in the inspected paths. |
| Pickups | Reuse arbitration, extend data model | `server.cpp::serverpickup()` validates and awards finite map pickups. Add materials, capacities, item instances and transactional transfers/salvage. |
| Construction | New gameplay system | Existing mapmodel/clip collision and `physics.cpp::objcollide()` are useful primitives. They do not provide networked, destructible, player-built structures. |
| Squads | New identity layer | `entity.h` hardcodes CLA/RVSF teams and team predicates. Add squad IDs, membership and private squad communications separately from combat hostility. |
| Revive and elimination | New server state machine | Baseline states in `entity.h` omit downed/extracted states. The current local experiment is described below. |
| Extraction and scoring | New mode | Existing server match timer/intermission can be extended. Seats, boarding, departure, extracted status and survival outcomes need implementation. |
| Audio and cues | Reuse playback, add gameplay semantics | Existing positional sound and scripted voice commands. Add a server noise-event system for infected and readable Predator cues. |
| Live voice | New integration | `SV_VOICECOM*` carries predefined sound IDs. No live microphone/codec/voice streaming implementation was identified in the inspected audio and protocol paths. |
| HUD and menus | Reuse UI primitives | Existing health/ammo, time, scoreboard, console and scripted menus. Add squad, materials, revive and extraction UI; remove enemy-location information for the Outbreak mode. |
| Cosmetics and account progression | Later system | Existing match statistics are not Outbreak account progression. Account identity, storage and unlocks need separate design and implementation. |

## High priority engineering gaps

### Combat is partially authoritative

`server.cpp`, in the `SV_SHOOT` handler, accepts shot destination and a list of claimed hits. `serverevents.h::processevent(client *, shotevent &)` checks life state, weapon validity, cadence, magazine availability, target life sequence and ray limits, then calls `serverdamage()`. For ordinary hits, this path does not independently reconstruct the ray against world geometry and target collision to establish the claimed hit. Grenade events similarly accept client-provided targets and distances subject to checks.

Keep server-owned health, ammunition, reload/cadence enforcement and damage broadcasts. Implement server hit tests against world, characters, infected and structures; bound timestamps and define latency compensation. Do not describe the current hit pipeline as fully authoritative merely because the server subtracts health.

### Movement and simulation need a shared server world

The `SV_POS` and compressed position handlers accept client positions. `physics.cpp` is in `CLIENT_OBJS`, not `SERVER_OBJS`, in `source/src/Makefile`. The dedicated server has map information (`serverfiles.h::servermap`, compressed floorplan data and map entities), but not the client's complete movement/collision simulation assembled as a shared server physics module.

`server.cpp::serverslice()` advances match time by elapsed wall-clock differences. `sendworldstate()` gates broadcasts at 40 ms, approximately 25 Hz. Broadcast cadence is not a fixed physics tick.

Extract shared world queries and collision interfaces, establish server-owned actor simulation, and decide the first playable's player movement validation/prediction scope explicitly. AI, placements and hit tests must use the same obstacle definitions.

### Bots are not multiplayer infected

`clientgame.cpp` invokes `BotManager.Think()` in bot modes. `botmanager.cpp::Think()` depends on `player1`, client frame time and local bot entities. Bot object files are part of the client target and absent from the standalone server target.

Reuse waypoint authoring and selected pathfinding/perception ideas. Implement an independent server actor model rather than disguising infected as extra player connections. Add navigation invalidation or blocked-edge updates for barricades, reachable attack positions and explicit failed-path handling.

`BotManager.LetBotsHear()` exists, but the source search found its declaration and definition without a call site. Its presence is not evidence of a working gunfire-to-infected hearing loop. Wire authoritative combat noise events explicitly.

### Team rules conflict with Outbreak

`entity.h` encodes two combat teams throughout helper predicates and arrays. `serverdamage()` subtracts frags for team kills and contains automatic kick/ban paths. `serverchecks.h::check_ffire()` can disconnect a player for excessive nonlethal friendly damage in open servers.

Outbreak needs independent squad membership, universal damage and a mode-specific policy disabling inherited friendly-fire/team-kill punishment. Otherwise intended betrayal can trigger removal from the match. Spectator access must also be restricted by squad rather than ordinary team/free-camera rules.

### Dynamic objects need more than map editing

`physics.cpp::mmcollide()` handles authored clip/mapmodel collision; `objcollide()` provides simple object overlap. Neither constitutes a construction lifecycle or server-owned structure registry.

Add validated anchors, material debits, authoritative placement IDs, collision insertion/removal, structure damage, repair, dismantle and salvage. The same object must obstruct movement, shots and infected routing on every peer. Reserved extraction corridors need server checks, not just client placement previews.

### Geometry and content impose practical limits

The native horizontal cell has a single floor/ceiling span. Start Blackwood with streets, yards, single-level interiors and two route choices. Stacked interiors, traversable bridges over rooms and simultaneous roof/interior access need explicit experiments; a rendered prop alone does not solve navigation and collision.

`world.h` allows client map factors up to 11, while `serverfiles.h` sets `SERVERMAXMAPFACTOR` to 10. Do not assume a map accepted by the editor is valid on the dedicated server. Nominal meters need calibration against engine units, movement speed and measured travel times.

The model loader in `rendermodel.cpp` tries MD2 and MD3; `model.h` exposes these formats and a fixed animation vocabulary. There is no native glTF/FBX import path in this loader. Plan asset conversion and animation state additions before commissioning final character assets.

## Current uncommitted prototype

At inspection, modified files included `bot/bot.cpp`, `clientgame.cpp`, `entities.cpp`, `entity.h`, `physics.cpp`, `protos.h` and `weapon.cpp`, plus untracked `outbreakstate.h`.

- `outbreakactive()` explicitly excludes multiplayer, remote connections and demo playback. This is an opt-in local experiment, not networked gameplay.
- `outbreakstate.h` implements local down/revive timing with 20 s bleed-out, 3 s revive and a once-per-reset downing guard. The brief's prototype values are 30 s and 5 s. These should become agreed configuration values.
- `clientgame.cpp::canrevive()` requires `isteam()`. It does not implement universal stranger/enemy revival.
- `updateoutbreakplayer()` zeros movement, and bot thinking stops movement for downed bots. Downed crawling remains work.
- Local downing applies only to selected team-mode, nongib, nonsuicide lethal damage cases. The production death/downing policy needs explicit server rules.
- A third-person eligibility helper exists, but its use in the camera/renderer was not present in the inspected snapshot. The helper alone does not establish a playable shoulder camera.
- `weapon.cpp` adds a local geometry intersection for the experiment. This does not alter the server's hit authority.

Preserve the experiment as exploratory work and reconcile its behavior with the multiplayer tickets. Shared-directory changes may continue after this audit snapshot.

## Build and verification

Host: Darwin arm64, Apple clang 17.0.0. `xcode-select -p` points at `/Library/Developer/CommandLineTools`. Homebrew `sdl2-config` reports 2.32.10, but the checks below used repository framework headers.

### Observed build configuration gaps

- `source/src/Makefile` supplies MinGW and non-MinGW branches. The latter uses Unix/Linux libraries such as `-lX11`, `-lGL` and `-lrt` without a dedicated Darwin linker branch. It is not a ready native macOS build recipe.
- `platform.h` enables SDL threads on macOS even for standalone builds. The Makefile's standalone include/link settings do not supply the corresponding SDL setup.
- `source/xcode` contains a native Xcode project and bundled frameworks. `file` reports SDL2 as universal x86_64/arm64, while SDL2_image is x86_64-only. An arm64 client cannot link that SDL2_image slice unchanged; replace/rebuild it or deliberately build an Intel configuration.
- Xcode build notes reference very old deployment/launcher assumptions. The project contains a packaging script that copies all packages and creates a DMG; use a focused developer build before any packaging work.
- The Makefile assigns debug flags, then later assigns `CXXFLAGS` again in compiler branches. Review effective debug flags rather than assuming `DEBUGBUILD=1` preserves the intended settings.
- `.github/workflows/build-linux64.yml` is manually dispatched and builds Linux binaries. Its production `sed` command writes to stdout without modifying the file. It does not establish automatic PR checks or gameplay validation.
- `source/tests` was empty at inspection. There is no Outbreak regression or load harness there yet.

### Checks performed

All commands ran from the repository root. No repository binaries, configure scripts, launchers or servers were executed. Compiler syntax checks parse source without linking or running the application.

Standalone server check, exit 0:

```sh
clang++ -fsyntax-only -DSTANDALONE \
  -Isource/src -Isource/enet/include \
  -Isource/xcode/Frameworks/SDL2.framework/Headers \
  source/src/server.cpp
```

Client check, exit 0 with a deprecated `sprintf` warning:

```sh
clang++ -fsyntax-only \
  -Isource/src -Isource/enet/include \
  -Isource/xcode/Frameworks/SDL2.framework/Headers \
  -Isource/xcode/Frameworks/SDL2_image.framework/Headers \
  -Fsource/xcode/Frameworks -idirafter source/include \
  source/src/clientgame.cpp
```

The same client flags passed for `rendergl.cpp`, `rendermodel.cpp`, `physics.cpp`, `weapon.cpp`, `client.cpp`, `clients2c.cpp`, `entities.cpp`, `worldio.cpp`, `bot/botmanager.cpp` and `bot/bot_waypoint.cpp`. Several produced deprecated `sprintf` warnings. These twelve passing translation units are a useful compilation signal, not a full build.

Next build evidence needed: clean linked client/server, launch with isolated Outbreak settings, two clients connecting, then four clients with one authoritative infected encounter. Record exact dependency versions, hardware, FPS, simulation tick timing and bandwidth. `MAXPLAYERS=32` and `MAXCLIENTS=256` in `protocol.h` are constants, not evidence for 24-player plus horde performance.

## Source and asset boundaries

This is a sampled notice inventory, not a complete file-by-file clearance or legal opinion.

| Component | Notice observed | Engineering consequence |
| --- | --- | --- |
| Core Cube-derived source | `source/README_CUBEENGINE.txt`: zlib-style terms, altered-source marking, notice preservation and additional no-relicense clause | Preserve notices and clearly identify the Outbreak fork. Do not apply a conflicting blanket repository license. |
| AssaultCube source origins | `source/README.txt`: Cube, pCube, Sauerbraten and other sources | Extend the inventory to individual headers and bundled components before distribution. |
| ENet | `source/enet/LICENSE`: permissive MIT-style terms | Preserve its actual bundled notice; the historical Cube README's description of ENet is not the current bundled notice. |
| Player models | `packages/models/playermodels/license.txt`: permission requested for use beyond personal use | Obtain permission or replace with suitably licensed Outbreak characters before shared release. |
| Weapons and pickups | Their respective `license.txt` files specify attribution, noncommercial and share-alike terms | Do not assume these are commercially reusable because the engine source is modifiable. Track or replace them. |
| Textures | Mixed notices; e.g. Golgotha directory describes public-domain material; Noctua permits private/commercial projects with attribution and restrictions | Some assets may be retainable. Make decisions per asset and source notice rather than discarding or approving all stock textures. |
| Sounds | `docs/package_copyrights.txt` notes incomplete source provenance and identifies GPL ricochet sounds | Track each included sound and its obligations; replace uncertain material in distributable builds. |
| Whole distribution | `README.html` points to the official package licensing page | The source license is not permission to redistribute a modified stock bundle. Keep packaging separate from development builds. |

Official supporting reference: https://assault.cubers.net/docs/license.html . The previously reviewed package documentation distinguishes whole-package restrictions from individual component permissions. The local notices above establish the concrete asset concerns in this checkout.

## Initial worker tickets

These are proposed assignments for the planned worker chats. This audit did not create chats or dispatch work.

| Ticket | Owner | Deliverable and acceptance | Dependency |
| --- | --- | --- | --- |
| OB-ENG-001 Native developer builds | Engine and Multiplayer | Reproducible linked client and dedicated server on this Mac; explicit dependency setup; isolated Outbreak launch settings; no stock packaging step | None |
| OB-QA-001 Baseline verification | QA and Performance | Repeatable build/connection checks and recorded hardware/build identity; clearly separate local bots from network clients | OB-ENG-001 for execution |
| OB-ENG-002 Shared simulation contract | Engine and Multiplayer | Define actor IDs, world queries, fixed step, lifecycle events, join snapshots and versioned Outbreak protocol; implement minimal server actor path | Begin alongside OB-ENG-001 |
| OB-PLY-001 Shoulder camera | Player and Combat | Living local model visible, shoulder offset, obstruction recovery, reticle/muzzle alignment and no shooting through near cover | OB-ENG-001 for playable validation |
| OB-ENG-003 Authoritative combat | Engine and Multiplayer with Player and Combat | Server validates a shot against world and target collision; health/ammo/death replicate to two clients; unsupported hit claims do not award damage | OB-ENG-002 |
| OB-WLD-001 Encounter greybox | World and Match Systems | One small structure, two practical approaches, spawn/loot/extract anchors and measured travel times; compatible with server map limits | Agree anchor schema with OB-ENG-002 |
| OB-AI-001 Networked walker | AI and Director | One server actor perceives, paths, attacks and dies; two clients observe the same result; scale to 4-8 with measurements | OB-ENG-002, OB-WLD-001 |
| OB-MAT-001 Squad and match rules | World and Match Systems with Engine and Multiplayer | Separate squad IDs; open PvP without inherited team-kill kicks; configurable 2-minute test match and extraction terminal states | OB-ENG-002 |
| OB-PLY-002 Authoritative down and revive | Player and Combat | Server-owned down/bleed-out/revive/elimination; any living survivor can revive; interruption and final-death rules verified | OB-ENG-003, OB-MAT-001 |
| OB-WLD-002 Barricade | World and Match Systems with AI and Director | Validated placement/material debit, shared collision, infected route response, destruction and stranger salvage | OB-ENG-002, OB-AI-001 |
| OB-QA-002 Four-player loop | QA and Performance | Four clients fight players/infected, revive and extract; disconnect/race checks; report FPS, tick cost, traffic and failed paths | First playable systems integrated |
| OB-ASSET-001 Asset allowlist | Project lead, then art/audio owner | File-level source/permission inventory for assets actually shipped; replacement queue for player/weapon/sound restrictions | Before any shared packaged build |

Predator tactics and Director pressure follow the authoritative walker and extraction loop. Broader Blackwood production follows the greybox. No renderer replacement, engine switch or design change is required merely to begin these tickets; concrete implementation evidence should drive those decisions.
