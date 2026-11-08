# T076 compact Blackwood world recommendation

World/Match-Systems; T0764.9/D069. **PROPOSAL ONLY. Every new geometry, number, ID/schema, allocation and ownership suggestion here requires MAIN freeze and individually released data/source work.** CONTRACT/PARAMETERS/INTERFACES0.2 and P2/P3 drafts are constraints, not implementation authority. No current map, source, asset, build, T067/T075 input or runtime was changed.

Recommend a single128×128-unit greybox encounter with one roofed central structure, two broad exterior approaches, eight outdoor deployment recesses, finite32-slot loot and one north-yard extraction. This supports the complete eight-player/squads1–4 requirement without a full town, additional encounter, weapon, recipe, extraction route or safe zone. It is a candidate to measure/playtest, not a declaration of balanced geography.

## What exists versus what is proposed

**Actual current DATA observation:** accepted network manifest c9ecfa62…359d7/map85617396…98134 is a561-byte native-v10 CGZ,64×64 cells, revision2,2224 open cells,8 FFA technical starts and5 LIGHT records. The bounded read-only helper reconfirmed its exact hash before/after. Original courtyard[8,56)², structure[26,38)×[24,40), original door/RLE layout and scoped original media are reusable references. These starts are not final squads, native PLAYERSTART is not authoritative Outbreak deployment, and this inspection adds no native/game/runtime evidence. Existing T075 baseline remains exact.

**Hypothetical measurement:** [final report, iteration2](../../web/world/reviews/T076/measurements-2.json) and [inspected stdlib helper](../../web/world/reviews/T076/measure.py) use a separate in-memory rectangle grid. They do not generate a CGZ, import project modules, run native collision/navigation or invoke a subprocess. Initial `measurements.json` is retained exploratory iteration1 (24 loot locations/older offsets), not the final candidate. Exact final rectangle/point tables are in iteration2; the tables below name them.

**Future work:** a NEW original map/MatchDefinition (candidate name `blackwood_greybox_v1`, not a rename/overlay of dev_outbreak_browser), bounded shared importer/queries, authoritative deployment/AI/transactions, real capsule/nav/runtime and human evidence. Proposed factor7 geometry requires later original data generation and new manifests. Reuse authored textures/fonts/models/notices where licensed and suitable; new wood/loot/region/cue art must be original or explicitly approved, never assumed stock assets. No final mesh, navmesh, locator/API or packaged configuration is created here.

## Coordinate convention and geometry — PROPOSED

Engine units, not metres: +X east, +Y north, +Z up; canonical actor foot z0. Standing eye4.5/height5.2/radius1.1 refer to T071/T002 candidates. **Do not copy legacy CGZ start z5 into a portable foot-origin anchor.** All rectangle bounds are half-open; collider contact/quantization policy belongs to T002. Offsets below are multiples of1/8 and exactly representable under its proposed Q10. No private coordinate/wire API is adopted.

```text
                    +Y / north
   D06 NW             D05 N              D04 NE
            north-yard reserved band / E01
   D07 W     west approach | building | east approach    D03 E
                south connecting apron
   D00 SW             D01 S              D02 SE
                    +X / east ->
```

| Geometry / logical region | Candidate specification |
| --- | --- |
| World / walkable perimeter |128² cells; playable courtyard[8,120)², outer solid perimeter; flat floor0, exterior ceiling16. No heightfields/stairs/ladders/crawl tunnels in first greybox. |
| One main combat space |Central yard envelope[34,94)×[32,96), connected to the same peripheral apron. Four metadata quadrants, not four independent encounters: BW-R00 SW x<64,y<64; R01 SE x≥64,y<64; R02 NW x<64,y≥64; R03 NE x≥64,y≥64, clipped to courtyard. |
| Enterable structure |Outer[50,78)², walls2 thick, interior[52,76)², floor0/ceiling12, inaccessible roof. West doorway x[50,52),y[60,68); east x[76,78),y[60,68), each8 wide/full12 high. |
| Interior cover |Two full-height screen strips[62,64)×[56,62) and[64,66)×[66,72); keep the central y[62,66) passage. No extra room/encounter. |
| Exterior approaches |West x[36,44), east x[84,92), both y[32,96); south connector[36,92)×[32,40). Routes go around opposite sides of the building and reconnect at extraction. |
| Deployment sight screens |20 axis-aligned full-height opaque strips, exact rectangles in report. Corner recesses use L screens; side recesses use U screens with outward openings and at least6-unit outer apron. They are unroofed entry cover, not eight additional buildings or immunity zones. |
| Cover/query intent |Static screens/walls block Move/Bullet/Camera/Sight/Navigate. Building ceiling/floor are real3D surfaces. Wood4-high boxes use their actual height, not infinite opaque2D walls; standing eye/camera may see over them. No invisible bullet-blocking cover invented for aesthetics. |

The one-unit conservative AABB-inflated grid has10420 connected free nodes without wood and10284 with every proposed panel occupied. All named spawn/loot/enemy/door/extraction proxy nodes connect in both cases. Cardinal edges avoid diagonal corner cuts; grid representatives are `(floor(x)+0.5,floor(y)+0.5)`, not exact continuous anchor positions. This does **not** prove shared capsule sweeps, nav portals, actor crowding, camera safety, jump/headroom or deterministic native/Wasm agreement.

## Deployment that covers every squad partition — PROPOSED

| Cluster ID | Centre(x,y) | Suggested inward initial aim, degrees from +X toward +Y |
| --- | --- | ---: |
| BW-D00 SW |20,20|45|
| BW-D01 S |64,20|90|
| BW-D02 SE |108,20|135|
| BW-D03 E |108,64|180|
| BW-D04 NE |108,108|225|
| BW-D05 N |64,108|270|
| BW-D06 NW |20,108|315|
| BW-D07 W |20,64|0|

Each cluster offers FOUR alternative slots `-S0..S3`, offsets(-1.375,-1.375),(+1.375,-1.375),(-1.375,+1.375),(+1.375,+1.375), foot z0. Only the configured eight participants are instantiated, never32 survivors. A cluster is exclusively assigned to one squad; unused slots stay empty.

Analytic candidate distances: minimum member separation2.75>diameter2.2; maximum pair distance3.8891<4; maximum member-to-centre1.9446; minimum cross-cluster slot distance41.25>the T002-recommended24. All32 candidate slots are clear in both measured obstacle states. No direct standing-eye segment exists between any pair of different clusters in this exact rectangle model, including every slot combination. This is NOT camera/FOV/peek/privacy proof; the shared sphere rig, dynamic poses and human visibility must be tested.

Any partition of8 with parts≤4 has at most8 groups. Eight exclusive four-slot clusters therefore suffice independently of partition/permutation. Helper enumerates15 unordered shapes and108 ordered compositions. Shapes:4+4;4+3+1;4+2+2;4+2+1+1;4+1⁴;3+3+2;3+3+1+1;3+2+2+1;3+2+1³;3+1⁵;2⁴;2³+1²;2²+1⁴;2+1⁶;1⁸. Mixed squads and eight solos require no shared centre or relaxed separation.

Recommend server-private seed-domain shuffle of eligible cluster IDs, then stable squad/participant ordering for allocation; no skill/outcome-based placement or client chosen coordinates. Before DeploymentCreate, validate every actual pose/capsule/headroom/pair/route and initial-encounter capacity against the exact map/rules hash. Allocate the whole roster atomically. Invalid geometry, insufficient groups/slots or required initial enemy eligibility returns Lobby with a reason; no half-deployment, spectator-to-survivor fallback, hidden relocation, loosened distance or safe-zone grace. Squad identity is fixed for the round and never damage immunity. Start locations are not disclosed to opponents by HUD/diagnostics.

## Finite loot and interaction anchors — PROPOSED

There are32 slots, eight per quadrant. In EACH ordered row below, item kinds are **pistol12, rifle30, medical1, wood3, pistol12, wood3, medical1, wood3**. Total map stock:96 pistol rounds,120 rifle rounds,8 medical items,36 wood. These are proposed extra world stocks, not a change to T071 starter loadouts or an adopted medical effect/cap. No replenishment or persistent inventory; depletion/reset belongs to authoritative round state.

| IDs in listed order | Candidate(x,y), foot0 |
| --- | --- |
| BW-L01..08 SW |(32,36);(48,42);(56,46);(56,56);(46,48);(56,60);(34,48);(52,46)|
| BW-L09..16 SE |(96,36);(80,42);(72,46);(72,56);(82,48);(72,60);(94,48);(76,46)|
| BW-L17..24 NW |(32,92);(48,82);(56,72);(56,68);(46,78);(52,82);(34,80);(56,82)|
| BW-L25..32 NE |(96,92);(80,82);(72,72);(72,68);(82,78);(76,82);(94,80);(72,82)|

Candidate interaction aim point z1, nonblocking loot marker/trigger radius0.5; T002 use range3/shared eye LOS/pickup400ms are recommendations requiring freeze. Actors do not gain resources by client proximity or rendered icons. Commit `min(stock,capacity)` once with request/result identity and stock/inventory before/after; competing pickup/repair/revive actions use the frozen server receipt ordering. No trading UI or infinite drops. MAIN must choose terminal-inventory handling; do not quietly adopt T002's proposed destruction policy.

**Universal revive has no static anchor.** Its target is any eligible downed survivor, irrespective of squad, with actual range/LOS/headroom/held-state checks; do not restrict revival to these loot sites. Preserve the draft universal5s interruption/recovery/down schedule and server-only resolver. Medical/use/wood/headroom rules need MAIN/T002 reconciliation before implementation.

## One barricade recipe and extraction reservation — PROPOSED

Use T002's candidate panel4 wide×4 high×0.5 thick, fixed axis per anchor; no client free placement/rotation. Width axis x means x±2,y±0.25; y means x±0.25,y±2; foot0/top4. IDs BW-B01..12:

| IDs | Centre / width axis |
| --- | --- |
| B01,B02 |(51,62)/y west doorway lower half; (77,66)/y east doorway upper half|
| B03,B04,B05 |(48,44)/x; (64,44)/x; (80,44)/x|
| B06,B07 |(48,56)/y; (80,56)/y|
| B08,B09 |(48,74)/y; (80,74)/y|
| B10,B11,B12 |(48,80)/x; (64,80)/x; (80,80)/x|

One doorway panel leaves the other4 units of an8-wide doorway open; candidate portal centres BW-V01(51,66) and BW-V02(77,62). These constrained anchors deliberately cannot seal the entire building or extraction. Remaining necks need real capsule/AI/crowding tests, not a claim that every wood wall is breach-only.12 simultaneous panels is a geometric stress state;36 proposed wood could fund12 builds before salvage/loss, but creator/squad/occupancy transactions still apply. Physical slots are not a new grant to exceed draft caps4 per creator/12 per original squad. Preserve cost3/carry12/placement2s/salvage2 intact,1 damaged,0 destroyed, and anyone may damage/repair/dismantle; HP/repair/dismantle values remain MAIN's freeze.

One extraction BW-E01 is centred(64,90), candidate boarding prism x[58,70),y[86,94),z[0,6) in foot coordinates. Its trigger is not collision, a seat reservation or immunity. North reservation x[34,94),y[84,96), BOTH exterior approach strips and south connector above form one reserved-access union. Reject any new obstacle whose XY footprint inflated by1.2 (radius1.1 + proposed0.1 margin) overlaps it; validate3D/actor overlaps and required routes at commit too. All12 proposed panels satisfy this stronger rectangle margin. Loot/enemy anchor footprints are outside the reservation. Actors/enemies can still move/fight there: reserved means no construction/static blockage, not a safe zone or an empty combat corridor guarantee.

All12 panel occupancy leaves every named grid anchor/portal connected; deleting obstacles cannot remove grid connectivity, so the binary-occupancy model also covers every subset. This monotonic argument does not prove runtime nav response, capsule portals or moving-body clearance. No dynamic gate, crisis, second extraction or cancellation rule is added.

Preserve draft900s round/last180s active window/4 seats (120s/last30s/2 seats only approved four-player smoke), uninterrupted boarding, vulnerability/release conditions and combat/down/bleed-before-departure ordering. T002 raises first-accepted-request versus hold-completion arbitration; this geometry proposal does not resolve that conflict or grant early reservations. MAIN must freeze it before transaction tests.

## Walkers, Predator and Director — PROPOSED anchor plan

| Kind / IDs | Ordered candidate(x,y), foot0 |
| --- | --- |
| Initial/available walker BW-I01..12 |(46,50);(58,46);(82,50);(70,46);(46,76);(58,72);(82,76);(70,72);(58,56);(70,56);(58,66);(70,62)|
| Reinforcement BW-RI01..08 |(32,44);(44,30);(84,30);(96,44);(96,84);(96,96);(32,96);(32,84)|
| Alternative Predator BW-P01..04 |(34,44);(94,44);(96,82);(32,82)|

These are alternative spawn candidates, not20 walkers/four Predators. T002's initial4 at four players /8 at eight players is a recommendation; select balanced quadrants before admitting actors, not always the firstN list entries. Hard ceiling remains12 living walkers plus one additional Predator; at most one Predator ever/round, death removes coordination and does not refund an automatic replacement. Four-player P2 has walkers only; Predator/Director implementation remains P4.

Mirror T002 pacing for discussion only:24 total walker admissions including initial population, at most2 new per20s, no more than12 living; every admission debits the server budget once. Candidate min survivor distance24 and outside every relevant survivor eye/canonical camera LOS/FOV, valid capsule/headroom/route, no actor/wood overlap or reserved spawn footprint. Actual initial4/8 eligible capacity must be validated before starting. Later no valid offscreen anchor logs SkipNoCandidate and retains unspent budget; never relax distance, hide on-screen pop-in, teleport or add budget-free enemies. Current helper checks anchor geometry/connectivity, **not full admission/offscreen eligibility**. Eight dispersed solos may deny every reinforcement; that is permitted pacing failure, not a reason to spawn beside them.

Predator front/flank goals come only from local perceived/remembered targets through T002 SenseView and shared paths/portals, directing existing walkers; no hidden-player lookup or omniscient rally placement. Audible and visible command cues and coordination-loss evidence need separate original cue/data work and AI freeze; T002's32-unit cue/3s assignment are unapproved suggestions. Director uses preweighted geographic region budgets/seeded logs, not squad skill or extraction winner targeting. Preserve all-side friendly damage/PvP and no enemy HUD positions.

## Traversal estimates and explicit balance concern

Hypothetical cardinal grid: nearest loot41–54 units from a deployment slot; extraction52–134 units without wood (same extrema with all12, some individual south-cluster routes lengthen). Using T071 proposed speeds:

| Motion | Speed units/s, PROPOSED | Extract route-time estimate |
| --- | ---: | ---: |
| Run |16|3.25–8.38s|
| Sprint |24|2.17–5.58s|
| Crouch/aim |8|6.50–16.75s|
| Downed crawl |3|17.33–44.67s|

Nearest loot is about2.56–3.38s at constant16/s. These are distance/speed calculations on a one-unit proxy, not observed times or bounds on real diagonal/capsule motion; they omit acceleration/braking/turning/input/collision/holds/combat. Coordinate-to-grid offsets also exist. North versus southwest extraction access is asymmetric (52 versus134): random pre-round allocation spreads expected advantage across rounds but does NOT prove fairness within one round. Extraction is inactive until the late window, yet holding terrain can still matter. Require human opening/loot/control/boarding review; do not freeze this as balanced or silently relocate E01 without remeasurement. Draft5s revive/2s board and T071 short TTK can dominate these travel scales.

## Shared schema, ownership and MAIN decisions

Recommend a versioned map/rules-bound MatchDefinition sidecar, **not** a new private file/wire contract: stable typed anchor ID, kind, region, canonical foot pose/aim, volume/shape, allowed stance/mask, capacity/occupancy constraints, route/reservation memberships and source geometry hash. All point positions across deployment slots/loot/wood/initial/reinforcement/Predator/extraction are unique in iteration2; typed IDs are unique and stable independent of array reordering. Runtime identity is MatchID+anchor ID+generation/state_version, using T002's server-owned entity/request semantics. Material stock and remaining admissions are runtime state, not respawnable data defaults. Full hidden spawn/seed/allocation diagnostics stay server-only, not a client enemy/loot exploit API.

Reconcile with T002 `import_map`/`validate_anchors`, CollisionView/world_revision and QueryMask Move/Bullet/Camera/Sight/Navigate. The authoritative/camera/shot/nav views share approved static primitives and dynamic wood geometry. Unsupported native cell/clip types fail import; renderer mips/meshes are not authority. A proposed2-unit nav grid needs deliberate origin/portal nodes and swept-edge validation: a4-unit residual doorway has only1.8-unit centre clearance after radius inflation and can be missed by poorly aligned coarse samples. The one-unit review graph is NOT adoption of that nav representation. Sound/occlusion semantics remain a MAIN mask decision, not an invented extra enum. Renderer/native axis/yaw adapters and quantization must be frozen with Engine/Player.

Proposed ownership: World authors new original greybox/anchor metadata and data validation only after MAIN release; Engine owns portable importer/query/collision/nav interfaces and canonical IDs; AI owns perception/path consumption/budgets; Player owns camera/input/presentation integration; World/Engine own authoritative inventory/wood/extraction transactions only through agreed module leases; MAIN owns ordering/schema/parameter freeze and runtime test release. T002's referenced delivery companion was not present at inspection; its architecture/interfaces and T071 remain nonbinding context, not transferred file ownership.

MAIN must decide exact geometry/cover/reservations, deployment privacy/proximity/seed policy, sidecar format/coordinate mapping, collision/nav masks/capsules/portal semantics, initial/pacing/offscreen/cue budgets, loot/medical/wood quantities/effects and all interaction/cap/seat ordering before implementation. No P2/P3 system is implemented by this note, and no P4 work is released early.

## Concrete future acceptance work

1. **Data/import:** bound real new CGZ/sidecar membership/decompression/cells/IDs/notice provenance; golden native-render versus shared StaticWorld shapes; reject bad offsets/cells/overlaps/unsupported clips. Match hashes before Ready, no current dev-map override.
2. **Deployment:** every15 partition shape/108 ordering plus arbitrary roster IDs/seeds, all8 solos/4+4, actual capsule/headroom and cross-group clearance/visibility; invalid anchor/capacity returns Lobby atomically. No hidden start leak or mid-round replacement/respawn.
3. **Navigation/world queries:** native/Wasm replay, standing/crouch/crawl/resize/door/camera/shot alignment; both approaches and partial-door portals with every allowed wood state; dynamic revision replan stops blocked motion immediately, no teleport. Include downed actors/crowds and reachable revive headroom.
4. **Transactions:** competing pickups/placement/repair/dismantle, duplicate/changed/old-epoch requests, creator/squad caps after leave, salvage loss and finite-stock/carry arithmetic; shared obstacle registration and reservation/route rejection are atomic. No resources from failed commits.
5. **Encounter:** actual four clients4–8 walkers/P2 universal revive/down/finishing/squad spectate; actual8+12walkers+1Predator maximum, valid offscreen admission/skip logs, local front/flank cues and death loss, budget/accounting under retries. No squad skill targeting or free actors.
6. **Extraction/round:** ordinary2s holds, full/contended seats, cancel/leave/down/disconnect release and frozen tie rules; due combat/bleed at departure, no extracted+eliminated double result; smoke/normal same logic; two successive resets clear all stock/wood/AI/actors/seats/timers. Reserved access is actually traversable under combat/crowds.
7. **Human/performance:** measure first-loot/encounter/extraction asymmetry, shoulder visibility/corner comfort, downed rescue feasibility and legible original cues; genuine eight-player human loop plus frozen server/browser performance thresholds. Pure grids/simulated clients do not replace runtime or required human acceptance. Deferred tester interface stays separately owned.
