# T155 — Complete World-query release packet

**PROPOSAL ONLY / T1551.0 / D195. NOT READY FOR COMPLETE CONTRACT ADOPTION:** three precise trace-record/selection clauses await MAIN in notes/questions/T155-world-hit-record-and-tie-semantics.md. This packet specifies the unaffected implementation graph, not another foundation/engine feasibility investigation. No source, interface, movement value or geometry policy is adopted here. No project code/import/test/compiler/runtime was executed. All native/Wasm/oracle/frame/performance items below are planned evidence, not PASS.

## 1. Scope, immutable dependencies and staged ownership

Use intended H3, T108 pair exchange, T110 common timeline and D150/T132 local progress direction. Preserve full ray, sphere, vertical capsule, actor-pair, rational span, stationary classifier, witness/normal, tie and static-initialization obligations. Engine owns timing/step/slide/projection/holds/debt and atomic commit; World owns the single feature kernel. No relative-motion sweep against static world, chord replacing a piecewise path, or private gameplay approximation.

T153's accepted private arithmetic is a **read-only dependency only after MAIN acceptance**; its current release/clearance is not inferred acceptance. Do not edit p1_query_wide.h or append another bigint. Int<8>/Int<16> and thirteen checked operations remain exact; an overflowing intermediate cannot be rescued by later cancellation. T154's exact AngleTables/rules validation is consumed only after its separate MAIN acceptance. Do not freeze the currently edited rules/angle source as an accepted dependency. T147 hash, accepted fixed and map_import APIs remain unchanged. Query-header adoption and every implementation stage need new explicit MAIN leases.

Proposed serial leases, all final features retained:

| Stage | Exclusive proposed paths and delivery | Prerequisites / acceptance |
| --- | --- | --- |
| G0 immutable authority data | NEW web/world/authority-p1/{map-manifest.json,anchors.json} and a separately named data-only fixture root | MAIN releases exact fixed-input data assembler; accepted T148/T080/T084 source bytes only; pin actual raw-map/cell/geometry/anchor SHA512 before consumption. No map boot/default selection or accepted-profile edit. |
| G1 static and complete pair core | NEW source/outbreak/p1_geometry.h/.cpp, NEW narrow p1_store.h; NEW tests/outbreak/geometry/G1/{verify.py,wrapper.cpp,wasm_runner.mjs,SCHEMA.md,README.md}, literal fresh attempt | T153/T154 accepted and G0 adopted. Static initialization/inspection, integer+rational pair, pose classifier and rational distance predicate complete; no geometry duplicate or fake World. Public TraceHit can remain forward-declared until Q1–Q3 are adopted. |
| G2 full static/view queries | World-only explicit successor lease to the same geometry files and NEW tests/outbreak/geometry/G2/** | MAIN first resolves Q1–Q3 and adopts exact resulting TraceHit/initial-ray/winner semantics. Full ray/sphere/capsule/headroom/masks/actors/boundaries, not a faces-only demonstration. Per-query width/work/stack and full oracle evidence mandatory. |
| G3 actual common-timeline consumer | Separate Engine-owned motion/store lease, World query files read-only | T110/D150 exact 65-span/aux/prefix/hold/debt implementation; prove caller call/stack/shared-scratch ledger, no new query semantics or arithmetic ownership transfer. |
| G4 camera/shot/scope integration | Separately owned Player/Engine source leases, geometry read-only | Exact head result and trace tie contract adopted; bind actual call frequencies, transactions and full native/browser/performance evidence. No gameplay/P0 release inferred from G0–G2. |

NEXT stages are names for MAIN to turn into literal tickets/roots, never runtime selectors. No worker is dispatched or asked to negotiate an interface by this proposal. G1 is independently implementable after adoption/dependencies; that does not omit G2's required behavior or mark the complete packet ready while Q1–Q3 remain open.

## 2. Exact proposed header and storage subset

`p1_geometry.h` includes only p1_types.h, accepted p1_rules.h and map_import.h. Reuse the H3 declarations verbatim:

```cpp
enum QueryBits:uint16_t { MoveMask=1,BulletMask=2,CameraMask=4,SightMask=8,NavMask=16 };
struct Aabb { Pos3 min,max; };
struct Capsule { Pos3 foot; int32_t radius_q10,height_q10; };
struct Sphere { Pos3 centre; int32_t radius_q10; };
struct ActorShape { ActorRef actor; Capsule capsule; };
struct BoxShape { uint32_t id; Aabb bounds; uint16_t mask; };
struct StaticStore;
struct CollisionView {
 const StaticStore *map; const ActorShape *actors; uint8_t actor_count;
 const BoxShape *boxes; uint8_t box_count; uint32_t world_revision;
};
struct TraceQuery { Pos3 from,to; uint16_t mask; ActorRef ignore; };
struct TraceHit; // G2 definition requires MAIN's Q1–Q3 resolution
struct HeadroomResult; // H3 status+TraceHit obstruction after that resolution
struct SpawnAnchor { uint16_t id; Pos3 foot; Aim aim; uint8_t squad_group; };
struct StaticInit {
 const FlatCell *cells; uint32_t count; FlatMapInfo info;
 const AngleTables *angles; MapHashes hashes;
 const SpawnAnchor *anchors; uint8_t anchor_count;
};
struct StaticInfo { FlatMapInfo map; MapHashes hashes; uint8_t anchor_count; };
struct PairContact {
 ActorRef actor_a,actor_b; uint64_t toi_q32;
 Pos3 point_a,point_b; Dir3 normal_b_to_a;
};
struct RationalCapsuleMotion {
 ActorRef actor; int32_t radius_q10,height_q10; uint64_t denominator;
 int64_t from_num[3],to_num[3];
};
enum class PoseRelation:uint8_t { Clear=0,Touching=1,Overlapping=2 };
struct PoseFeasibility {
 PoseRelation relation; HitKind kind;
 ActorRef actor_a,actor_b; uint32_t primitive_id;
};
bool inspect_static(const StaticStore &,StaticInfo &,Fault &);
bool inspect_anchor(const StaticStore &,uint16_t,SpawnAnchor &,Fault &);
bool inspect_anchor_at(const StaticStore &,uint8_t,SpawnAnchor &,Fault &);
QueryStatus sweep_capsule_pair(const ActorShape &,const Pos3 &,
                              const ActorShape &,const Pos3 &,PairContact &,Fault &);
QueryStatus sweep_capsule_pair_rational(const RationalCapsuleMotion &,
                                       const RationalCapsuleMotion &,PairContact &,Fault &);
bool classify_pose_set(const StaticStore &,const RationalCapsuleMotion *,
                       uint8_t,PoseFeasibility &,Fault &);
bool movement_contact_tie(const RationalCapsuleMotion &,uint64_t,uint64_t,bool &,Fault &);
// Required G2 signatures, not removed from final scope:
bool trace_ray(const CollisionView &,const TraceQuery &,TraceHit &,Fault &);
bool sweep_capsule(const CollisionView &,const Capsule &,const Pos3 &,
                   uint16_t,ActorRef,TraceHit &,Fault &);
bool sweep_sphere(const CollisionView &,const Sphere &,const Pos3 &,
                  uint16_t,TraceHit &,Fault &);
bool headroom(const CollisionView &,const Capsule &,ActorRef,HeadroomResult &,Fault &);
QueryStatus sweep_capsule_world_rational(const StaticStore &,
                                        const RationalCapsuleMotion &,TraceHit &,Fault &);
```

H3's current proposed TraceHit is {status,kind,primitive_id,actor,toi_q32,distance_q10,point,normal}; it has no exact head-zone field. Do not pretend the forward declaration solves Q1 or privately add a field. G2 must publish MAIN's exact adopted successor record.

Proposed NEW `p1_store.h` initially includes p1_geometry.h and contains only the existing H6 names: enum class StorageKind:uint8_t {Static=1,Simulation=2,Ingress=3,Outbox=4,Client=5}; struct StorageSpec {uint32_t bytes,alignment;}; StorageSpec storage_spec(StorageKind); bool init_static(void *,uint32_t,const StaticInit &,StaticStore *&,Fault &); void destroy_static(StaticStore &). MAIN explicitly gives World this initial narrow file lease, then serializes later Engine additions. No unimplemented simulation factory or duplicate storage function is smuggled into G1. storage_spec returns the fixed H6 five pairs (2097152/64,2097152/64,262144/64,1048576/64,2097152/64); an invalid enum returns {0,0}. Only Static is implemented as a lifetime-bearing store in G1.

Proposed static arena layout, offsets from caller's 64-aligned 2097152-byte buffer:

| Region | Offset | Capacity | Lifetime |
| --- | ---: | ---: | --- |
| Validated header/info/hashes/anchor index | 0 | 256 | Immutable after successful init |
| 65536 explicit four-byte FlatCells | 256 | 262144 | Immutable |
| One copied AngleTables (101544 array bytes+64 digest bytes) | 262400 | 101608 | Immutable; no 100KiB automatic temporary |
| 32 SpawnAnchor records, proposed sizeof<=24 | 364032 | 768 | Immutable, ID sorted |
| Canonical geometry encoding scratch | 364800 | 262784 | Init only; no query cache or retained borrowed pointer |
| Remaining reserved bytes | 627584 | 1469568 | Unused; not permission to enlarge other stores |

Offsets include alignment gaps. Require native/Wasm static_assert of fixed-width byte sizes and proposed SpawnAnchor size/alignment; a mismatch is a review failure, not a silent reinterpretation. Canonical bytes never use struct padding. The full static reservation stays2MiB; only placement into caller-owned memory, no allocator/free/moving/live reinit. Failure preserves out handle/Fault policy and publishes no usable store; destination bytes may be unspecified as H6 allows. Destroy invalidates lifetime/views, does not free caller memory. Store lifetime encloses every borrowed CollisionView. Invalid/dangling/overlapping C++ allocations and concurrent mutation are caller precondition violations, not magically safe enum cases.

Proposed exact init precedence: null storage/cells/angles/nonempty anchor pointer -> {Null,1,0}; capacity/alignment -> {Storage,1,0}; count/info/cell format -> {Map,1,first_bad_cell_or0}; anchor ID/group/domain -> {Identity or Range,1,first_bad_anchor}; accepted rules/angles/hash mismatch -> {Rules or Map,1,0}; internal arithmetic failure -> {Overflow or Invariant,1,0}. A missing anchor inspection ID is Identity, bad index Range, stage2/detail requested ID/index. Success Fault={None,0,0}. These are proposed adoption clauses, not edits to existing factories.

## 3. Immutable map, anchors, hashes and validation

Cells must be accepted decoder outputs: side64/128/256, count=side²<=65536, positive revision<=INT32_MAX, entity_count<=1024; kind0 canonical floor/ceiling/tag0, or kind4/tag0/floor<ceiling. Heights multiply signed cell values by1024 explicitly. No corners/heightfields/vdelta/clips/models/water or config execution. This does not repeat or replace map_import's raw-byte validation. The bounded outer installer verifies raw ACMP SHA512 and its approved source manifest; StaticInit has no raw bytes and cannot independently attest that outer step.

Copy cells, all supplied anchors and every table element/hash; retain no mutable input aliases. Verify AngleTables through the accepted T154 validator against the accepted rules factory and pinned full array material, not a caller-selected self-consistent digest. Compare hashes.rules/angles to that exact context. Map SHA512 binds bounded decompressed ACMP bytes at the outer boundary. Geometry SHA512 input is explicit LE u16 side, u32 revision, row-major four cell bytes, u8 anchor_count, then ID-sorted anchors encoded u16 id,3i32 foot,u16 yaw,i16 pitch,u8 group: at most262759 bytes, fitting the init-only arena scratch and accepted bounded sha512_bytes. No streaming-hash API change or giant stack encoding.

Anchors:0..32, unique nonzero u16 IDs; group0..7/max4 per group; valid foot-domain and Aim pitch/yaw. Inspect by index enumerates ID order, lookup unknown ID fails without output change. Group is asset grouping, not a squad/grant. Planner later picks complete groups and validates chosen living standing capsules/all pairs; init does not assert every alternative is simultaneously deployed/safe. NoAnchor remains an ordinary atomic Lobby denial, never rounded/synthetic spawn.

G0 maps accepted `BW-Dgg-Ss` deployment slots to numeric id1+4*gg+s and group=gg; copies exact Q10 foot coordinates. Canonical from-east aim maps to Outbreak yaw by nearest/ties-away((theta_cdeg−9000 mod36000)*65536/36000), pitch0. This follows F=(-sinYaw,cosYaw,0); it is not native CGZ yaw=(theta+90deg). Current Blackwood angles are multiples45deg, hence exactly representable. Preserve strings as provenance and validate reverse association. Never substitute8 integer technical starts for32 canonical alternatives or convert loot/walker/predator points into grants. G0 must publish actual new numeric/canonical hashes for MAIN; none is invented in this notes-only task.

Sources are the accepted84-file Blackwood assembly and accepted T080 sidecar, not stock content or a regenerated map. Both dev map and Blackwood remain; asset mounting/default startup/geometry/config/anchor edits are outside this packet. Candidate-not-balance-accepted, no capsule/nav/gameplay proof, technical-start distinction and no-resource/actor-grants limitations remain. A future room chooses one explicitly approved immutable map, not automatic Blackwood startup.

Static IDs: cellIndex*3+part0(solid)/1(below floor)/2(above ceiling), maximum196607; outer faces196608..196613. World-solid outside x/y actual[0,side*1024], z[−131072,131072]. Each space supplies closed below-floor and above-ceiling blocks; a solid cell spans the full Z range. Touch at a closed boundary is distinct from strict penetration. Hit with primitive_id0 is legal; status distinguishes it from Clear's zero sentinel. Boxes preserve H capacity32/unique id>=0x10000000, but P1 box_count must0; nonzero in P1 is explicit unsupported/Range, not skipped. Later wood transactions need separate adoption.

View actors0..8, unique valid slots/generation/life, P1 r1126/h3738..5325, current fixed stance per call. Only masks including Move/Bullet consider actors; Camera/Sight/Nav alone do not. Exact matching ignore ref only; null is all-zero, malformed nonnull refs fail. Known nonzero mask subset of31 required. Caller authenticates match/alive/current revision; static map revision is not silently equated to CollisionView.world_revision. No world/private canonical pointer is added.

Proposed general static-query numeric shape domain (for MAIN adoption): positive radius<=131072, vertical height2r..262144; current living/camera callers retain their exact frozen1126/358 shapes. End numeric halo and per-component travel follow T110; large legal broad-phase footprints may return QueryLimit. Stationary pose-set rational capsules retain the narrower T108 P1 shape/domain. This specifies numeric validation, not a new gameplay collider/tuning value. Zero-radius point queries use trace_ray, not an invalid sphere. Q3 still blocks the ray's initial-inside/touch output rule.

## 4. Feature graph and denominator discipline

Use local parameter t∈[0,1] of the caller's **original** interval throughout a query. Integer world has d1. Rational world has its input d<=Q=2^32. Paired rational has unreduced D=d_a*d_b<=2^64. No rebasing a feature/axis piece, denominator accumulation, whole-set LCM, or multiplying all8 pose denominators. Classify each body/world with its own d and each pair with its two-body D.

World sphere/AABB: for each coordinate, closest point is clamp(center,lo,hi). Its27 clamp states are inside plus6 faces/12 edges/8 vertices. For one selected active-axis set, v(t)=(U+V*t)/d is centre minus closest box point, constrained by that feature's signed exterior and remaining-axis slab inequalities. Squared contact is f=A*t²+B*t+C with A=sum(V²), B=2sum(UV), C=sum(U²)−(r*d)². Six faces may use the equivalent signed linear plane equation;12 edges/8 vertices use quadratic roots. Retain feature inequalities and test them at the algebraic candidate, never on a rounded position. Closed inequalities deduplicate shared-boundary roots by exact root equality, primitive ID and fixed face/edge/vertex rank.

Vertical capsule/AABB reduces exactly to a sphere at the FOOT against an extended-Z box [lo.z−(h−r),hi.z−r], same XY/r. This follows minimum distance between [foot.z+r,foot.z+h−r] and box Z interval; it is not a rendered capsule or point-height approximation. Reconstruct original capsule-axis/world witnesses afterward. Outer halfspaces have direct linear contact equations for sphere/capsule extents and six fixed IDs. All per-cell primitive geometry is derived on demand; no2*65536 AABB array.

Ray/static uses closed rational slab entry/exit, exact signed plane fractions and validity of all slabs. Ray/actor uses the actual stance capsule: point-to-axis distance, lower-cap/barrel/upper-cap pieces and R=actor radius. Sphere/actor uses the same point/axis graph with R=r_sphere+r_actor; capsule/actor uses the closest-two-axis graph with the target stationary. No inflated damage target, root of an expanded render box or one-actor relative sweep against the world. Unsupported initial-ray cases are Q3, not guessed by treating them as capsule overlap.

Pair graph: form relative horizontal affine components and the two vertical interval-gap affine boundaries. Split only validity intervals at their zero crossings; at most3 chronological pieces. On a piece D_z is upper gap, lower gap, or0; horizontal components unchanged. Coefficients stay in the original t/D, not a new piece fraction. Test endpoints/constant/stationary cases, discriminant and up to2 roots/piece; choose first physically valid piece/root. Algebraically identical boundary events are one contact. This avoids any unrelated pair-quadratic-to-pair-quadratic comparison: later pieces are later by rational boundary order.

Initial pair penetration is Invalid/Invariant, including moving-apart/coincident cases. Initial touch blocks iff exact D(0)·relative_delta<0; stationary/tangent/separating touch Clear as T108. A later grazing double root and t1 touch are Hit. World sweep applies that rule per primitive, skips nonclosing initially touched features and continues searching other primitives. Ordinary stationary classification is separate: exact distance²<R² Overlapping, =R² Touching, >R² Clear. It never calls an Invalid sweep to infer overlap.

Integral delegation is an explicit early branch after rational validation: if ALL sampled from/to coordinates are integral, exactly delegate to the integer semantics. Otherwise use the prescribed unreduced d/D, including normal denominator. Do not claim denominator-rescaling invariance of quantized normals: ceil-isqrt normalization is representation-dependent, and this delegation is part of T110's definition. Physical root/status can be invariant while a prescribed quantized witness differs.

Engine's local/global time composition retains its two explicit endpoint cases: lower u=Q returns b; upper u+1=Q returns b, including u=Q−1. In particular (b−a)=Q times Q is2^64, never a wrapping uint64 product. Other products are<=Q*(Q−1); adding Q−1 for ceiling division then fits uint64. Conservative floor composition does not certify an adjacent GLOBAL bin or exact simultaneity. No kernel piece substitutes a newly scaled time denominator into its coefficients.

## 5. Sign-safe root, feature and winner graph

Private root certificate is a tagged linear fraction or (A,B,C,Delta,branch sigma) with A>0 and Delta>=0; sigma−1/+1 denotes (-B+sigma*sqrt(Delta))/(2A). A0 is dispatched first; B0/C signs classify constant/degenerate equations. Negative discriminant is no root, never passed to sqrtrem. Exact0 discriminant has one candidate. Linear denominator is made positive with simultaneous numerator sign change. No unchecked division, lost sign or narrowing before domain checks.

**Linear expression at a quadratic root.** For ell(t)=l*t+m, form X=2A*m−B*l and Y=sigma*l. Sign ell(root) is sign(X+Y*sqrt(Delta)), denominator2A positive. If Delta0 or Y0 use X; X0 uses Y when Delta>0. If X,Y have the same nonzero sign use that sign. Only opposite signs permit magnitude squaring: E=X²−Y²*Delta; equality gives0, otherwise sign is sign(X)*sign(E). All operands are independently bounded below. This handles feature halfspaces, piece endpoints, t0/t1, exact head predicate privately, rational bounds and Q32 bin decisions. Never square without those branch conditions.

**Q32 certification.** Validate exact root in[0,1], handle exact0/1 explicitly, then32 binary comparisons of root to k/Q isolate the adjacent bin. Equality returns that k, not k−1. Report q=floor(Q*t); Hit1 and Clear both use q=Q but distinct status. sqrtrem(Delta) may supply an initial bracket, with128/256 digit cap, but floor/ceil sqrt is not an approximate physical root or a replacement for the32 exact sign comparisons.

**Competing world roots: bounded resultant comparator.** This is the missing global winner operation, not a universal pair-width claim. Let f=A*t²+B*t+C and g=a*t²+b*t+c, A,a>0. At f's selected root r define

`L=A*b−B*a; M=A*c−C*a; N=B*c−C*b; R=M²−L*N`.

Then sign g(r)=sign(L*r+M). With X=2A*M−B*L, Y=sigma*L, the exact identity is

`X²−Y²*Delta = 4*A²*R`.

Use the preceding sign branches, but in the opposite-sign case use sign R, since4A²>0. **Do not construct X² or Y²Delta here:** those naïve intermediates can exceed the released width. This symbolic resultant identity eliminates them BEFORE operations, not by overflowing then cancelling. Zero R is handled exactly, including common roots; it is not an uncertainty tolerance.

To compare r with a chosen root of g, first evaluate sign g'(r)=sign(2a*r+b) by the bounded ordinary linear-at-root operation. For g's lower root: derivative>0 implies r is later; derivative0 implies later unless Delta_g0 (equal); derivative<0 gives comparison −sign g(r). For g's upper root: derivative<0 implies earlier; derivative0 implies earlier unless Delta_g0; derivative>0 gives sign g(r). Thus equal roots, tangent roots and shared Q32 bins are distinguished without repeated radical squaring. Rational-vs-root uses linear-at-root; fraction-vs-fraction uses checked cross products. This defines a total exact physical-root order, independent of feature enumeration.

Maintain two certificates (current exact earliest, new candidate); stream primitives, never store all roots. The exact11-Q10 **reported-time** distance predicate is the existing T110 formula sum((to−from)²)*(q1−q2)²<=121*d²*Q², with absolute time difference formed safely. Diagnostic distance_q10 is not substituted. A second streaming pass can choose a priority candidate anchored to the true earliest, never a chained current winner. **How that group changes returned TOI/normal/head result is Q2 and not adopted.** Exact same-root world primitive ties can already use fixed IDs/feature rank. No shared Q32 bin is asserted to mean equal physical roots.

## 6. Explicit finite width ledger

Bounds are strict absolute magnitudes, sign separate. Each product/sum is checked before publication; arithmetic Overflow faults rather than Clear/blocked. Use I256 for the integral graph and I512 for rational calls/comparators; no new width, generic radical comparator or arithmetic API. The following graph keeps every constructed integer within the selected width.

| Construction | Premise and constructed bound |
| --- | --- |
| Rational pair U,V,D | D<=2^64, abs(U_i)<=2^18D, abs(V_i)<=2^19D; no piece reparameterization |
| Pair A,B,C,Delta | A<2^168, abs(B)<2^168, abs(C)<2^166, abs(Delta)<2^337; retain every term before subtraction |
| Pair Q32 lin-root certificate | (2Ak+BQ)²<2^404; Delta Q² and separately formed difference<2^405 |
| Pair boundary n/m | abs(n)<=2^82,m<=2^83; boundary sorting products<2^166; lin-root squares<2^504, difference<2^505 |
| Pair polynomial at rational boundary | A n²+Bnm+C m²<2^335; all three terms separately fit |
| World affine U,V,r | d<=2^32, abs(U)<2^20d, abs(V)<=2^18d, r<=2^17; extension/halo included |
| World A,B,C,Delta | A<2^102, abs(B)<2^105, abs(C)<2^106, abs(Delta)<2^211 |
| World feature-boundary fractions | abs(n)<2^52,m<=2^50; squared lin-root expressions<2^312, difference<2^313 |
| World Q32 certificate | squared expressions<2^276, difference<2^277 |
| World competing-root resultant | conservatively all six coefficients<2^106: abs(L),abs(M),abs(N)<2^213; M²,LN<2^426; abs(R)<2^427; abs(X)<2^321 (NOT squared) |
| World derivative-at-root branch | slope2a<2^107; X<2^214; X²<2^428; Y²Delta<2^425; subtraction<2^429 |
| Integral feature/winner graph | generous coefficient bound2^46/Delta<2^95; resultant<2^187, derivative-square difference<2^190; integral root/bin/domain comparisons fit256 |
| Pair normal | fixed denominator DQ<=2^96; evaluated UQ+Vq<2^116; actual closest-axis numerator<=2^114; three squares<2^230; ceil root<2^115; component*2^30<=2^144 |
| Pair quantized witnesses | midpoint may use2DQ; final common denominator<=2^127, numerator<2^146; signed nearest/ties-away only at end |
| World normal/witness | denominator dQ<=2^64, offset numerator<2^85; squares sum<2^172; scaled normal<2^115; witness denom<=2^95/numerator<2^116 (generous halo/axis midpoint allowance) |
| Travel distance at reported q | S=sum((to_num−from_num)²)<2^102; S*q²<2^166; divisor dQ<=2^64. floor(sqrt(T)/v)=floor(isqrt(T)/v), v>0 |
| Movement distance tie | left<2^166, right<2^135; no sqrt or root-difference radical |
| Exact private head-zone sign | ell(t)=100*(from.z−actor.foot.z)+100*delta.z*t−85*h at physical ray root; abs(l)<2^25,abs(m)<2^28, integral coefficient bound2^46 gives X<2^76, squared-difference<2^153; fits256. Delivery of this bool remains Q1 |
| Stationary set | each world test as above; each pair uses only its own two denominators. No eight-body denominator product |

The explicit T126 regression Delta*Q²=81144064*2^320 remains>2^346; no universal340-bit assurance is made. The new resultant graph is specifically for world/actor feature coefficients under the listed bounds. Do NOT apply it unqualified to two arbitrary rational-pair polynomials (coefficients168bits); their analogous generic resultant bound would be675bits. The query avoids that operation by ordered pair pieces; Engine orders separate pair events by conservative global time/stable key as already specified. If a later caller actually requires exact unrelated-pair radical order, that is a new overwidth question, not a silent16-limb extension.

Feature-validity signs use original affine offsets and exact root tags; squared-difference signs use the branches in section5. Root denominators are never repeatedly multiplied by piece boundaries. No exported gcd/reduction/radical routine is needed. Normalization and witness fractions retain the required unreduced representations even when root comparisons use algebraic identities.

## 7. Witnesses, stationary classification and error/output behavior

Pair q witness: evaluate both axis segments at q/Q; disjoint intervals choose facing ends, overlap chooses common intersection midpoint. Their difference has denominator exactly DQ (midpoint factor2 cancels); N=ceil_isqrt(sum(Di²)), nonzero, n_i=trunc(Di*2^30/N). Points are nearest/ties-away of axis_A−r_A*n/2^30 and axis_B+r_B*n/2^30. Preserve swap symmetry exactly, including negation/canonical zero; no unquantized Di/N witness substitution. Rounded surface witnesses are not committed actor positions or head-zone oracles.

World sphere/capsule witness reconstructs closest original box/axis points at reported q with the same midpoint convention; face normals are exact unit axes, edge/vertex normals use dQ and ceil-root normalization. Nearest integer witness rounding occurs last; actual capsule body/stance is used. Moving-body strict initial overlap is an Invariant fault; no arbitrary depenetration normal. For rays, a private physical-root point/head predicate is computable using linear-at-root, but the public rounded-point/exact-head delivery and origin case remain Q1/Q3. Do not silently reinterpret that unresolved field.

Clear uses T110 sentinel: qQ/kindNone/id0/null actor/zero normal, nearest endpoint foot or sphere centre, floor full interval travel. World Hit uses World/null actor/stable primitive ID, actor Hit uses Actor/valid target and primitive_id0. All normal nonzero successful moving-body hits meet |n_i|<=2^30 and sum(n_i²)<=2^60. Ray-specific exceptional origin output waits for Q3.

Pose set validates count0..8, null only for0, distinct valid actor slots, stationary numerator equality and exact halo/shape bounds. Count0 returns Clear/None/null/null/id0. Otherwise stream per-body static overlaps and each unordered pair; strongest relation Overlapping>Touching>Clear, then actor_a ascending, World before Actor, primitive/pair IDs. Permutation does not change geometric witness. No normal is invented. Outside actual map is Overlapping within valid numeric halo; beyond halo is Range. Any error leaves output unchanged.

Proposed view-query validation order: valid StaticStore lifetime (pointer/allocation precondition), explicit null map, counts/nonempty pointers/mask/P1-zero boxes, ignore ref, actor refs/unique slots/shapes in input order, query shape/start/end/time domain, then geometry. Stage2 aggregate detail8; individual malformed actor detail0..7. Pair APIs keep their stricter frozen refsA/B/distinct/shapeA/B/endA/B/relative order and detail0/1/2; QueryLimit remains {QueryLimit,2,3} for pair, aggregate8 for the other queries. Validate d in1..Q before signed64 bound products; reject numerator-domain violations before negation/addition. Pos3+delta is widened before endpoint validation. No int32 overflow is relied on to reject malformed inputs.

Proposed zero-displacement headroom uses stationary classification, Touching is feasible/Clear; strict overlap is ordinary Hit obstruction, with zero normal and no push, point a diagnostic foot, q0/distance0. This stationary obstruction is explicitly not a physical damage-ray surface result. False means fault and preserves the whole HeadroomResult. Bool query APIs succeed only Clear/Hit and set Fault None; failures return false with output unchanged, not a half-written Invalid status field. Direct QueryStatus APIs return Invalid/IterationLimit with untouched outputs as T108/T110. Arithmetic Overflow maps stage2 Overflow; violated internal arithmetic premise maps Invariant; domain Null/Identity/Range/Map and QueryLimit remain distinct. Nonclosing touch is never an arithmetic error. All filters/argument checks precede geometry.

## 8. Complete broad-phase and per-query work ledger

Do not equate centre-line DDA to swept-volume coverage. Ray uses exact closed supercover grid traversal after clipping to the actual XY grid; tied corner crossings visit both side cells and diagonal. At side256, at most769 unique cells (513 ordinary crossings plus at most256 corner extras), within1024. A vertical XY-stationary ray visits its closed footprint cells, not a divide-by-zero path. Six outside halfspaces are always considered independently.

Sphere/capsule use a duplicate-free row-strip rational grid walk: for row j, clip the centre segment to y in[row_min−r,row_max+r]; evaluate its x extrema at that exact clipped parameter interval; enumerate every cell in that x range expanded by r. This conservative swept-square corridor contains the swept disk, including endpoint/corner touches, and visits each candidate cell once without a65536-bit visited array. Row/column indices have fixed0..255 bounds. Charge EVERY enumerated candidate, even culled/space cells, to1024; if unfinished after1024 return QueryLimit and preserve output. No first1024-only Clear. Legal long-diagonal T126 input may exhaust the cap; it is not misreported coverage or normal-play success. P1 small-motion/stationary footprints remain small, but actual reachable-path/resource evidence is separate. The literal row-strip algorithm must be adopted as the specified swept-volume traversal, not passed off as old centre-line coverage.

Stationary classifier P1 footprints conservatively<=25 cells/body, <=200 for8 plus28 pairs, including all close-boundary cells and outside checks. Larger generic headroom shapes use the same bounded traversal and can fault QueryLimit. Rational row-strip interpolation uses one parameter fraction n/m with |n|<2^52,m<=2^50; x numerator products/sums<2^105, denominator<=2^82, fitting512; no rational root is introduced in broad phase.

| Maximum one full World sweep enumeration | Count |
| --- | ---: |
| Unique charged grid cells | 1024 |
| On-demand below/above/solid boxes (max2 per cell) | 2048 |
| Static features plus6 outer faces | 53254 |
| Quadratic discriminants | 40960 |
| Linear+quadratic candidate roots including outer faces | 94214 |
| Integer-root digit iterations at256/Delta | 10485760, plus one witness root<=256 |
| Q32 binary certificate comparisons,32/root | 3014848 |
| At most8 feature/domain sign tests per root | 753712 |
| Streaming physical winner comparisons | 94213 |

View actor tests add at most8*3 quadratic pieces/48 candidate roots/24 discriminants for ray/sphere versus stationary capsules; capsule/actor uses the pair kernel at most8 calls. Account these explicitly, never hide them in the static count. P1 dynamic boxes0; any future32-box implementation adds their own26 features/candidate counts under a separate release. Early rejects/culls reduce actual work, not the published maximum.

Per constructed coefficient/discriminant reserve<=48 wide multiplies/64 add-sub/32 compares. One ordinary linear-at-root decision uses<=12 multiplies/12 add-sub/8 compares; resultant+derivative winner decision<=96 multiplies/64 add-sub/32 compares. Final normal/witness/distance reserve one sqrt and<=64 multiplies/16 divide-or-round operations. These are explicit planned ceilings to be derived line-by-line from the real source; a source loop with a hidden additional decision cannot inherit the table for free. Multiply/root/division loop costs are the accepted T153 ledger, including its callees. Finite millions of certificates are NOT a20ms proof.

## 9. Automatic storage and caller work boundaries

One query entry allocates a private5120-byte workspace:64 I512 slots=4352 plus768 bytes scalar/cell traversal/indices/tags/results. Integral queries can use the same reservation. No all-feature/root/cell arrays, all-window array, AngleTables/cell copy or recursion. Root-builder, comparator, stationary and witness phases reuse the bank; no whole public query is recursively called by another public query.

| Simultaneous private bank use | I512 slots / reuse |
| --- | --- |
| Two root certificates A/B/C/Delta | 8, retained during streamed candidate comparison |
| U/V three components and coordinate/radius denominators | 8, builder slots8..15 |
| Resultant L/M/N/X/Y/two products/R | <=10, slots16..25; no X² in this branch |
| Derivative/linear-root squares and difference | <=6, slots26..31 |
| Witness normal/root/remainder/points/rounding/distance | <=32 after scan, reusing builder/comparator slots; winner certificate remains4 |
| Sorted pose indices8, cell walker, stable winner tags | In768-byte scalar allowance; borrow input poses, no automatic pose[8] clone |

Reserve<=1024 additional bytes across geometry wrappers/scalar callee frames and<=2048 for the accepted wide-helper chain:5120+1024+2048=8192 query chain. This is a source allocation/liveness requirement, not measured fit. Actual source must pass slots by reference, avoid by-value Int/large record temporaries and prove compiler spills/alignment/normal callees fit on native and Wasm. A largest function frame alone is insufficient. Apply D196's defined-call/native canary exclusion and honest Wasm linear-ABI/declared-local interpretation; do not claim physical JIT/control-stack attestation. Full caller chain still<=65536 including query, codecs and motion; query8KiB is not added on top of64KiB.

Static init's large encoding/table/cell storage is in its already reserved caller arena, not this query frame or a new shared allocation. Engine's plan/trial/event buffers remain in its existing786432-byte shared scratch; no query arena is retained there by stealth. Query operations borrow immutable inputs only, publish staged small results and have no wall clock/cache/global state.

To remove T126's undefined c/U from the eventual caller proof, propose the following explicit **future Engine source schedule**, not a claim its current unimplemented caller already follows it. Define one verification bundle as at most536 World legs and4060 pair windows/aux checks. Each leg/window has one initial stationary classifier plus its sweep (skip sweep on ordinary overlap); one final full pose classification. Thus<=9193 public query calls/bundle. Third-party overlap/contact becomes explicit debt, not a fabricated Clear or a query-error-as-rejection.

Assign every bundle a literal cause:1 initial-plan check; <=116 event scans (4*(28+1));4 pass verifications;<=4896 dyadic prefix trials (144*34);8 optional-branch validations;1 final commit check;<=144 post-response verifications. Total<=5170 bundles. There is no free nested SafeStart/rescan: charge to the current scan/trial or fault if no category remains. Static-tail invocations are separately bounded by8 initial+224 pair-affected+32 world-tail+16 step-stage+8 fork-restoration=288; <=16 up/down probes,32 world guards and112 pair guards,<=144 guard classifications,3 initial/stance classifications and8 growth headroom checks. This is a concrete proposed counted schedule with unchanged response/pass/step limits, not a tunable higher-response budget. Source review must show each branch maps to one category and rejected branches retain spent counts.

The bundle envelope alone is47527810 calls; with the603 separately listed planning/guard/stance calls it is47528413 before Player camera/shot/recipient-scope work. It is deliberately loose and not evidence all are simultaneously attainable or affordable. Player/scope invocation frequencies and their shared reuse are NOT frozen by a World packet; a later caller lease must bind them before claiming complete-tick work/64KiB/performance closure. No measured normal-play bound is inferred from these paper counts. A caller needing additional verification cannot silently increment c/U, grant another resolving pass or commit partial debt.

## 10. Independent native/Wasm evidence plan

Use later inspected fixed drivers and accepted installed compiler/SDK/Node/Python roles as DATA, never run T084/T147/T150/T153/T154 occupied drivers. Proposed each stage whole<=300s, each compile/link/target<=60s, combined child/tool logs<=8MiB; exact tool/dependency/source/corpus/argv/environment identities before effects, fresh owned cache/sysroot/tmp/logs. No new install/runtime library/flags or original-cache writes without MAIN. Actual production geometry functions run on native and Wasm; no JS fake solver or compiler-only PASS. Test-only wrappers own minimal fixed exports/request/response buffers, no production ABI export attributes/app inclusion.

Proposed final corpus<=16384 rows, each request<=1024 bytes/response96 explicit bytes; total request data<=8MiB (generator checks aggregate), both actual response streams<=3145728 bytes, leaving5242880 under8MiB for tool logs. Map setup/data not printed as logs; include its explicit bounded request/cell identities in the retained corpus. Full expected/raw native/raw Wasm responses and untouched-output/input guards retained. No platform struct serialization.

| Family | Case cap / required independent checks |
| --- | --- |
| Static init/storage/hash/assets | 3072: all3 sides, full decoded cell equality, unknown modifiers/IDs/groups/angles/hash/alias/lifetime/capacity/alignment; no100KiB stack table; fixed numeric sidecar mapping, canonical byte hashes, failures publish no handle |
| Ray/sphere/capsule/static features | 4096: every6/12/8 feature and sign, all masks, floors/ceilings/solid/outer faces, extended-Z reduction, exact endpoints/corner and face ties, candidate valid only in its Voronoi domain, long-footprint QueryLimit not Clear |
| Integer/rational pairs | 3072: all3 vertical pieces, zero/equal relative motion, initial touch closing/nonclosing, strict overlap, later tangent/t1, arbitrary d near1/Q and nonintegral endpoints, original-parameter boundary ordering |
| Stationary/normal/witness | 1536:0..8 poses, permutations/strongest stable witness, outside numeric halo vs actual-map solid, exact Q30 bound/sign/swap, overlap midpoint/negative ties-away, integral-delegation representation branch |
| Root ordering/bin/ties | 2048: lower/upper/double/shared roots, X/Y sign table, resultant0/opposite-sign branches, close roots in one Q32 bin, exact dyadic equality, T126>340-bit regression, Q1 head example, adopted Q2 tie-set policy |
| Fault/limit/atomic output | 1024: every malformed field, width refusal/negative-discriminant premise, work caps, poisoned complete outputs unchanged, bool/direct status mapping, no Clear for unsupported/overflow/QueryLimit |
| Metamorphic/caller regressions | 1536: swap/translation/reflection/common velocity/status-time invariants, unchanged301 travel and exact sampling, split intervals without witness-invariance assumptions across representation changes, T126/D150 hold/debt/whole-step rollback examples |

Oracle is separate Python exact rational geometry: closest-point/segment distance and piecewise convex minima, not the production26-feature walker or limb implementation. Root order uses rational interval isolation and polynomial gcd/Sturm logic for equal/near roots, not a copy of the production resultant shortcut. Proposed offline cap2048 dyadic refinement steps, degree<=4, intermediates<=16384bits, plus actual300s driver bound; failure preserves evidence and asks MAIN, no approximation/tolerance or silent extra run. Witness/normal oracle uses exact fractions and independent integer isqrt at the specified reported q/denominator. Certificates compare every explicit field, not only digests or native-to-Wasm self-agreement. Oracle/source proof and compiled correctness are distinct.

Require compile-time record/arena bounds, actual compiler-produced native/Wasm call-chain frames, normal-callee accounting and live-bank source audit. Injected work/overflow fixtures are labeled; do not corrupt host memory. Full motion transaction tests additionally prove canonical tick/IDs/RNG/ACK/outbox unchanged on failures. Actual platform tick p95/p99 and full population/human/browser requirements remain later unchanged PLATFORM_DECISION gates, not this unit-corpus result.

## 11. Decisions still blocking complete adoption

Q1 is an exact counterexample, not a tolerance preference: for the specified cap/ray, physical z is in(3177.3,3177.5), so exact head is true while nearest Pos3.z3177 classifies body. MAIN must choose exact result delivery and distinguish a diagnostic rounded surface point; World has not added a public field.

Q2 must locate the existing11-Q10 priority predicate relative to true-earliest root selection and returned feature/time, with an anchored nonchaining tie set. The arithmetic for both exact root order and existing rational reported-time predicate is supplied; their combined publication policy is not inferred.

Q3 must specify nonzero ray origins inside/on surfaces and any head/normal exception. Swept-body overlap behavior cannot silently become ray behavior. These clauses block final G2 record/return-oracle acceptance, not an excuse to discard those required rays or relabel an arithmetic fault geometry.

Therefore **NOT READY FOR COMPLETE WORLD CONTRACT ADOPTION** until Q1–Q3 are resolved and incorporated into an authoritative exact header/behavior amendment. G0/G1 clauses and the explicit feature/sign/width/storage/work/test plan are submitted for MAIN review now. Complete executable/compiled stack/shared-scratch/caller-frequency/performance proofs remain required acceptance evidence in their named source stages, not missing mathematical guesses to be replaced by a paper PASS. Movement preference is irrelevant. QA/T149/runtime/full phase/human holds unchanged.

## 12. Read-only reference identities (SHA256)

| Reference | SHA256 |
| --- | --- |
| H headers / section3 | 79fa17d45f11d480a66a57435a258811722c075e1dddc1926428958f2cb01709 |
| T108 pair addendum | 467fe123a20d36ffaf18382d9d7e9818798fcd5eba592844b94acba9d3231b90 |
| T110 common timeline | bb10cc027171ed4b7a34b0d25e6035beb7ce54ae56dfe2749aa10f1354dce58f |
| T132 progress proposal | a5fb7a4ae119868647edb014f9c8342b42580e78071206a8768228220ec77b9f |
| T126 resource/width findings | 32970ac803fdecab342c64421631b268ee77a60be3c57a50cade3e6c27c6ff9c |
| T152 arithmetic packet | 241f543b71e6663d55342ccd3f398ea52f575e9fe9d5cfa25e97af89a3b5ef7d |
| D150 | 7488af4515839a3290af395806c3d8e907c719a538761ce2085363a138d16467 |
| QUERY_ARITHMETIC_FOUNDATION0.2 | 126f2b0afe57a7f9a9f7e43b90d69dcd45fdd4e726bc4d764b591d50d62cf2c6 |
| P1_RULES0.2 | 63a2a843f69e2495a97383ac17d559793f43611867c36a9bb84159f2b3f86fd3 |
| PLATFORM_DECISION0.1 | ff1dfd40bc402110e546e08d8d8d6523501be2edd5128c9a8b160ccdd65c4624 |
| PORTABLE_FORMAT_FOUNDATION0.1 | d50bac8d4c768f6b1e843ca6688473baf948ce1e98393c3bfaa9c1cf519a5a90 |
| map_import.h | a8ee019deec650add0cc885dba337ef70517106dc9719fceb0535ce6e664c90f |
| map_import.cpp | 1da8d4c5c10f51463f5f4c9bc88ca5b3ea13effba22ab614bef56c0212b82604 |
| T148 assembly manifest | 8c4f7eef5f0deafb06bec60d62be529a684a30d56bbdc6dc3e5f38dd21c69e60 |
| T080 canonical sidecar | 159d3afe87123616e8346f6db00c2fd3a99325abbfa74a67b825bebfd89af05e |
| ANGLE_BASIS_FOUNDATION0.1 | 4461ac0e4b31bd62fa2ceaa3da504b0c05f24fa3051ed4bb15f1eb6d786e90b4 |
| T1551.0 | a5579d4c65e632fe6d747eda4b6c78234682ebc3567c2e179d5135d87732e8ce |
| D195 | efe2d30a03b5693e06ff81e7d714b82a0e8d44e1c468914eb544203c706ce3fa |

Paths for shorthand references are the exact existing files cited in sections1–3 and the own handoff; no old proposal or accepted evidence is edited. Only this new packet, own question and handoff are written.
