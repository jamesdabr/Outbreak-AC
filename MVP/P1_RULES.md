# Authoritative P1 rules

Revision:0.2. Status: APPROVED MAIN D086/D112 for numerical/behavior freeze and explicitly tagged P1 evidence-only completion. P0 acceptance, complete shared record/wire/body definitions and individually released P1 tickets remain mandatory before gameplay implementation. This addendum supersedes only matching draft P0/P1 rows in PARAMETERS0.2 and resolves the named T002 policy questions. Later-phase numerical recommendations remain drafts unless explicitly stated here.

## P1 evidence-only terminal boundary

D112 approves the proposed trusted EndP1Scenario control only for a separately released P1 combat evidence scenario, before full extraction exists. It may produce Results reason P1ScenarioComplete when that explicit scenario's evidence criteria have been met; it is not an MVP win, extraction, client action, public console/admin command or grant to an LLM player. The trusted coordinator/harness owns it; normal clients cannot submit it. No test hook may silently force gameplay state or bypass authority/atomic commit. In a P1-only build reaching active_start_tick+45000 without the mandatory later extraction lifecycle, emit an explicit Results-Aborted/P1ScopeBoundary with the last committed tick, not normal success. Existing debt/fault/lease abort behavior remains unchanged. Later P3/MVP profile must implement the full900s round/last180s extraction and cannot use this P1-only boundary as normal product behavior. Typed enum/wire/private-control layouts still require MAIN interface approval; this paragraph approves the limited semantic policy only.

## Time and authority

Server50Hz, fixed20ms ticks, uint64 tick. At most4 catch-up ticks per scheduler turn, retaining residual debt and yielding I/O. Debt>200ms makes the attempt unhealthy and enters Results-Aborted with the last committed tick; never discard simulation time or report normal extraction success. Adapter heartbeat/leases use monotonic wall time; gameplay deadlines use simulation ticks. Tick cost/memory limits are in PLATFORM_DECISION0.1.

Client50Hz intents, last3 recent records redundant per batch, <=8 queued input records/peer. Select newest eligible state once/actor/tick; retire older eligible records explicitly as superseded, not extra integration. Input age<=160ms/8ticks, future<=20ms/1tick against acknowledged server clock estimate; reject invalid age rather than clamp timestamps. Reliable control edge may wait<=1tick for referenced input, otherwise MissingInput. Silence100ms without fresh valid input neutralizes movement/fire/aim/sprint/use. No delayed rifle catch-up burst. No client dt/position/hit/origin/resource grants.

Snapshots25Hz/every2ticks; remote interpolation80ms, extrapolate<=80ms then freeze/fade stale presentation. Own prediction stores<=128inputs/2.56s and replays from authoritative own state through the same movement/world revision. Input ACK is a retirement high-water mark, with last-applied and rejection/supersession counts separate. Logical prediction is corrected immediately; presentation-only correction<=100ms for error<=0.25units. Missing/stale collision revision stops prediction and requests bounded resync. No target rewind: shots use current post-movement authoritative poses.

New authority target must neutralize on local blur/hidden/lock loss and keep the actor vulnerable. Heartbeat1s/transport timeout10s; no guarantee hidden tabs remain alive. No immediate hidden/frame-gap disconnect in that future target. Frozen experimental backend0.2 remains unchanged; its successor needs its own approved lease/profile. Escape pauses local input/overlay only, not multiplayer simulation. Explicit resume gesture consumes its click and cannot fire.

## Deterministic representation

Foot-origin positions signed Q10, velocities signed Q16. Numeric helpers follow accepted SHARED_NUMERIC_FOUNDATION0.1. Quantize decimal spatial constants once to nearest integer/ties away; publish effective values, never use platform float rounding inside authority. Speeds/accelerations are exact integer units represented in Q16. Durations below are exact integer ticks. Geometry contact/tie epsilon is conservatively ceil(0.01*1024)=11 Q10 units; world wins a hit-distance tie, then stable primitive/entity ID. Checked64-bit intermediate arithmetic and explicit failure states; no silent saturation/overflow.

Yaw is a uint16 full turn; pitch is signed centidegrees clamped[-8000,8000]. Runtime angle/query/normalization/TOI algorithms and exact public state records are still subject to the complete shared-interface release; workers cannot invent divergent angle tables or hidden movement remainder state under this rules freeze.

## Movement and camera

| Rule | Frozen value |
| --- | --- |
| Run/sprint/crouch/aim walk |16/24/8/8units/s; normalized diagonals |
| Ground acceleration/braking |64/96units/s² |
| Air horizontal cap/acceleration/gravity |16units/s /16units/s² /32units/s² |
| Jump |12units/s vertical; fresh edge only, grounded standing; no held repeat/double jump |
| Living capsule radius |1.10units; Q10=1126 |
| Standing height/eye |5.20/4.50; Q10=5325/4608 |
| Crouching height/eye |3.65/3.10; Q10=3738/3174 |
| Stance transition |200ms/10ticks; foot preserved, enlarge only with headroom; blocked stand stays crouched |
| Step/slope |<=0.80units/<=45°; approved map/query implementation must actually support used geometry |
| Sprint eligibility |grounded forward/forward-diagonal, no aim/crouch/reload/fire; no stamina |
| Shoulder rig |eye−6.00*aim_forward+1.25*horizontal_right+0.30*up, fixed right shoulder |
| Camera collision |continuous eye→ideal sphere sweep radius0.35 (Q10=358), safety margin0.03 (Q10=31); include opaque world/wood, exclude actor bodies |
| Camera recovery |immediate stateless retraction/extension; no minimum boom through cover, no temporal origin smoothing |
| Lens |horizontal FOV90° hip/75° aim, near0.15;100ms visual-only lens transition |
| Pitch/sensitivity |±80°, hip existing scale3, aim multiplier0.70, no acceleration/filter |
| Tight own-body fade |camera-eye<1.00 alpha0.20; restore≥1.20, visual only; genuine local living actor visible normally |
| Logical muzzle (forward/right/up from eye) |pistol(0.65,0.35,−0.50), rifle(1.10,0.35,−0.50) |

Living actor collision uses same start-of-tick trajectories and deterministic swept-pair resolution, not one client pushing another. Continuous capsule/sphere/ray queries must distinguish Clear/Hit/Invalid/IterationLimit; <=4contact/slide iterations and <=4stable residual actor-pair passes. Any exhausted solver faults the candidate tick, not a through-wall success. Exact query records/TOI numerical algorithms require the shared-interface release before implementation. Downed collider/crawl details belong to P2; do not use an impossible capsule shorter than twice its radius.

Server derives the same stateless camera from authoritative pose/aim. Trace unspread centre ray to weapon range for convergence T. Guard eye→muzzle and eye→T against world; reject nominal convergence behind eye or within0.25units. Otherwise spread muzzle→T and take its nearest physical world/actor intersection. World wins epsilon ties. Legal cover-blocked shots spend one round/cadence and emit Blocked with no damage; invalid/stale/duplicate/no-ammo requests never spend. No render tag/GPU depth/old worldpos/client hit list is an authority source.

## Weapons and health

| Rule | Pistol | Rifle |
| --- | --- | --- |
| Trigger |fresh press, no held repeat |held while fresh input lease valid |
| Body damage |34 |20 |
| Interval |240ms/12ticks |100ms/5ticks |
| Magazine/start reserve/reserve cap |12/48/96 |30/90/180 |
| Reload |1600ms/80ticks |2200ms/110ticks |
| Range |100units |150units |
| Cone half-angle hip/aim |1.20°/0.20° |1.80°/0.35° |

Health100, no armour. Friendly/squad damage100%, no betrayal penalty/kick/ban. Head multiplier2 when first contact lies in upper15% of the actual stance capsule, not rendered mesh/head tag. Moving at accepted horizontal speed>0.10 adds0.60°; airborne adds1.00°; crouch multiplies final cone by3/4. Quantize final half-angle to nearest centidegree/ties away. Server-private deterministic spread stream advances only on accepted shot ordinals; uniform solid-angle cone algorithm and seed/state layout must be frozen in shared implementation interfaces. Client cannot select/retry seeds. No view recoil/velocity kick/distance falloff/penetration/ricochet/third weapon in P1; visual shot poses are allowed.

Deploy with both weapons, rifle selected. Select1=pistol/2=rifle,200ms/10tick switch, cancel trigger/reload, fresh trigger required. Reload transfers min(magazine deficit,reserve) atomically at completion; no extra chamber. Selection/sprint/life loss/leave cancels without transfer; damage alone does not. Fire cannot cancel reload; no autoreload. Dry feedback once per press. Reload finishing on a tick may supply a valid shot that tick. Weapon/life fields remain server-owned.

## Commit and lifecycle ordering

Only advance_tick may commit canonical state. Adapter ingress may update bounded receipt/rate/pending-body metadata; it cannot allocate actors, retire gameplay ACKs, advance gameplay RNG or cache a success outside a committed tick. Stage into persistent heap-owned candidate World and output; validate/reserve everything before one commit. Precommit faults discard state, tick, IDs, RNG, results, retirement ACKs and outputs unchanged. Postcommit transport failure records delivery failure and schedules loss for next tick; never roll back/regrant. No large World/Replica/StaticWorld by-value temporaries; portable stack<=64KiB. Initial working targets: World<=1MiB each/2buffers, static<=2MiB, scratch/inbox/outbox<=2MiB, client replica/prediction<=2MiB, total shared<=8MiB excluding renderer/transport. Measure actual size/stack/copy cost before acceptance.

Per tick: (1) cutoff leave/disconnect/lifecycle; (2) select input, eligible reload/switch, movement/aim; (3) gather valid shots/melee from the same postmovement/start-combat life set, resolve damage batches and permit valid simultaneous trades; (4) lethal/down and due bleed; (5) revalidate/complete interactions; (6) complete boarding/seat arbitration; (7) departure combat/bleed already resolved, extract living boarded then mark remaining outcomes; (8) staged AI plans, invariant/encoding/outbox checks and atomic commit. Later-phase stages are specified ordering constraints, not permission to implement them in P1.

An actor Alive at combat-phase start takes that batch against living health; overkill does not spill into a newly created down pool. Actors already Down take finishing damage. P1's lethal scenario has no automatic mid-round respawn; later P2 sole life resolver must implement required30/20/10s down schedule/free universal5s revive/recovery, not a second combat death writer.

Boarding seats are awarded only at successful2s hold completion; no reservation during an unfinished hold. Equal-tick completions order by original server receipt sequence, then actor ID. Damage cancels unfinished boarding; nonlethal damage after completed boarding retains the seat. Cancel/zone exit/down/elimination/disconnect releases it. This clarifies the draft's 'first accepted request' as acceptance of completed boarding, preserving uninterrupted hold and no client timestamp priority.

Revive completion must fit a crouched living capsule at the same foot; otherwise explicit NoHeadroom, target stays Down, no health/resource award/push/teleport. Keep final map free of crawl-only traps. Firing/sprint/selection cancels ongoing use; completed boarding permits ordinary combat and remains vulnerable. These resolve policy ambiguity, not P2 release.

## Identity and transport direction

Eight ordinary player slots, fixed squads1–4 at deployment. Private anonymous participant identity, fresh one-use admission/connection epoch; no account system. Active late join is spectator. Same-round disconnected survivor is LEFT; readmission can only grant permitted own-squad observer, never replacement/alive restoration. All terminal states stay terminal for that MatchID.

Future authority transport profile:8live/16retired/24total UDP sockets,60s retirement;16pending TCP/32upgrade attempts per admission epoch;3600s session/7200s gateway run leases. Before deployment require>=1050s lease remaining; otherwise explicit re-admission in Lobby/Results with fresh connection generation and consumed cap, never hidden in-round renewal. Existing fixed experimental profiles stay unchanged. Exact coordinator/control channel, public wire bodies, room secrets, decoder bounds and ENet receive-allocation policy still need explicit interface freeze; these values authorize no service/connection changes by themselves.

## Presentation and acceptance

WASD/mouse, LMB/RMB, R,1/2,C,Shift,fresh Space; E reserved for later interactions. Escape releases all holds and opens overlay; resume requires gesture; ordinary Leave uses server loss/leave without same-round survivor restart. Wheel/other native weapon selection disabled in new target. Local body renders once in shoulder pass, HUDgun off, original supported model/skin/attachments; no spectator-state shortcut or enemy radar.

P1 evidence must cover cover/near-wall/corner/headroom, aim targets2/8/32/96units and rifle144, static shared endpoint discrepancy<=0.02units, actual visual barrel/logical muzzle discrepancy<=0.20units and direction<=2° in idle/run/crouch/aim/extreme pitch. Server health/ammo and rejection/dup/cadence/reload/full friendly damage require real two-browser normal+fixed-impaired evidence. Camera comfort/pose/pixels/audibility and full MVP human playtest remain human evidence. Source-derived helpers, renderer preloads and native relay cannot satisfy these tests.
