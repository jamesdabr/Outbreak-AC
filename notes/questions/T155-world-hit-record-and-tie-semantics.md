# T155 exact hit-record and winner clauses requiring MAIN adoption

- Author: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket: T1551.0, notes-only D195.
- Governing: P1_RULES0.2; intended H3/T108/T110/D150 query behavior, not adopted gameplay headers.
- Exact clauses: H3 TraceHit.point:Pos3, earliest physical root/Q32 certificate, physical-stance-capsule head point and100*(point.z-foot.z)>=85*height; world-wins distance ties<=11; ray from==to Invalid.
- Status: OPEN. This note does not amend a record, tie rule or damage value.

## Q1 — Integer hit point cannot preserve an exact physical head-zone predicate

Use a valid target capsule foot(8192,8192,0), r1126,h3738. Its top cap centre is(8192,8192,2612). Ray from(6000,8192,3177) to(10000,8192,3178), with target identity valid and not ignored, has upper-cap entry governed by:

`p(t)=16000001*t^2-17534870*t+3856213`.

At t=3/10, p=35752.09>0; at t=1/2, p=-911221.75<0; derivative is negative throughout[0,1/2]. Thus its first physical entry has3177.3<z<3177.5. This lies on the actual upper cap (z>2612), inside the global numeric domain, not a rendered/inflated target. Exact head threshold is85*3738/100=3177.3, so the physical hit is head. Nearest/ties-away Q10 z is3177, for which317700<317730 gives body. Truncation also gives body. More fundamentally a generic algebraic surface point is not representable by integer Pos3.

The packet supplies exact private linear-at-root classification, so arithmetic is not missing. The public delivery/consumer clause is missing: H3 has only a rounded Pos3 plus floored Q32 time, and the literal physical-point predicate cannot be reconstructed universally from those fields.

Proposed MAIN resolution: adopt an explicit exact head-zone result (e.g. a field or separately specified World-owned trace result/API), computed at the physical root before coordinate quantization; document TraceHit.point as a rounded diagnostic surface witness. A different choice to define damage on the rounded point must be an explicit behavior decision, not silently substituted. World has not selected either or changed H records. Source leases for exact root predicates/static initialization can be reviewed independently; final damage-ray record publication/consumer integration waits.

## Q2 — Near-distance priority and earliest-root return need one exact winner clause

H3 simultaneously asks for earliest physical contact and world priority for distance ties<=11, then IDs. T110 defines the exact11-Q10 predicate on the two reported Q32 times of the SAME linear interval, not on twice-rounded distance fields. Neither defines here whether a later world candidate within11 replaces an earlier actor candidate's TOI/witness, whether only scheduler priority changes, or how a multi-candidate tie set is anchored.

Threshold closeness is not transitive: roots at travel distances100,108,116 have adjacent differences8 but endpoint difference16. A scan that repeatedly replaces the current winner by a lower-ID candidate within11 can drift from100 to116 and depend on enumeration order. Returning the earliest time with the later feature's normal/point would mix two physical events.

The packet gives an exact total physical-root ordering and the already specified rational Q32-distance predicate. MAIN must adopt where the priority group is anchored (proposed true-earliest candidate, never a chained winner), which clock/distance representation it uses, and whether returned time/witness belongs to the priority winner or retains a separate earliest blocker. An additional result field or explicit separation between trace selection and Engine scheduling may be needed. No epsilon, new11 value or new response policy is proposed privately. End-to-end winner publication is blocked on this clause; feature/root arithmetic is not.

## Q3 — Ray starting inside/touching a solid/actor needs explicit output semantics

T108/T110 specify strict penetration Invalid and nonclosing touch Clear for moving bodies, while H3 only explicitly makes a zero-length ray Invalid. A nonzero ray originating strictly inside an actor or static solid has no nonnegative entry surface but is obstructed at its origin. Hit0, first exit, and Invalid have different muzzle/LOS/head-zone meanings; an interior origin is not a physical surface point under Q1. Copying the capsule rule into rays would choose policy not currently stated.

Please specify inside/on-surface ray classification and witness/normal/head behavior, including tangent/separating origin touch and ignore-filter order. Recommendation for review is to distinguish an origin obstruction from a physical surface hit; no new binding record or return behavior is adopted here.

## Independent work and paused portions

The named T155 packet still supplies full feature construction, sign-safe rational/root ordering (including a bounded resultant comparator), pair/stationary/witness arithmetic, finite per-query work, storage/header/lease and independent native/Wasm plans. No512-bit insufficiency is inferred from the old340-bit claim; no wider core, fallback, repeated unguarded squaring or project execution is introduced.

Only final trace hit/head/winner/initial-ray publication semantics and their dependent source acceptance are paused. Full query implementation is not marked READY until MAIN resolves/adopts these exact clauses. All required ray/sphere/capsule/pair/rational behavior remains in the staged plan. Owner movement preference, QA/T149/runtime holds and other workers' exclusive source leases are unchanged.
