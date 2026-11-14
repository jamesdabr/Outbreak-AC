# T187: later entry to a constant-zero face changes the selected normal

- Author / worker: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket/revision: T1871.2 / D301/D307/D311; source construction only
- Governing: G2_FOUNDATION0.4; T173 sections4–5 and T155 packet2 feature/root/witness rules
- Exact clauses: closed feature inequalities/shared-root deduplication by fixed face/edge/vertex rank; A0/B0/constant dispatch before division; faces use exact unit axes, edges/vertices use original-axis ceil-isqrt normals at reported q.
- Status: OPEN; MAIN disposition is separate. No production change proposed here is assumed authorized.

## Concrete case and question

Use the EXISTING F4 step/block64 fixture, Sphere centre(32410,12800,8192), radius358, delta(0,0,-10001), MoveMask, no actors/boxes. This is a valid generic public sweep with no strict initial overlap. The relevant raised-floor cell is x32,y12, physical box[32768,33792]x[12288,13312]x[-131072,1024], primitive_id2401. Its lower-X face rank0 has a constant-zero surface equation because centre.x=32768-358, delta.x=0. Its other slabs first become valid when centre.z reaches1024. The X-min/Z-max edge rank11 has a genuine double root at that same physical time.

Does the adopted closed-feature minimum-rank rule require this contact to retain face rank0 (with exact -X unit normal), even though its face equation is constant and needs the earliest entry to its validity interval? Or is the intended candidate set restricted to isolated roots, allowing the edge rank11/quantized edge normal here? The frozen prose appears to require the former; current production realizes the latter.

## Paper evidence, not execution

Relevant contact time is t=7168/10001. No static contact precedes it:

- The outside room at x31 has floor0, so its floor contact is later at centre.z358.
- The raised ceiling at x32 starts at6144. The sphere initially touches its lower-X face; that primitive is skipped by the frozen moving-body nonclosing-touch rule (the sphere moves parallel to that face).
- Other raised-floor cells are farther than radius358 in X or Y. The chosen Y12800 is a cell centre,512 from either Y boundary. Outer halfspaces and other F4 features are away from this sweep.

For Q=4294967296, `q=floor(7168*Q/10001)=3078324725`, and `7168*Q-10001*q=3003`. Thus at reported q the original closest edge differences have numerator(-358*Q,0,3003) with denominator Q. Since `3003² < 2*358*Q+1`, their ceil norm is358*Q+1. The current edge materialization therefore produces

`normal=(-1073741823,0,2)`.

A selected face rank0 instead prescribes the exact face normal

`normal=(-1073741824,0,0)`.

Both surface points round to(32768,12800,1024), and both contacts have their own q/distance/identity, so comparing only point/time/identity would miss the normal difference. The floor0 contact is666 Q10 later, beyond the11 anchored group; first and priority both select this raised-floor primitive.

Current production74884/SHA2565163a100e558022cc26e3e9693a470677e5a3b79570d68a12c0961ae457b0cb8: q_box skips a face when its plane velocity is zero; the edge's quadratic emits the double root. q_box_validity has the special closed-face rank canonicalization for rays only. Neither the constant face's validity-entry root nor nonray minimum face rank is retained. q_materialize accordingly uses the edge-normal branch. G1 is unaffected and remains the accepted byte prefix.

The independent Q closest-distance oracle currently classifies the exact contact's minimum physical feature as face0 and expects the unit face normal. It has not been run, and no target result has been observed. This is a source/paper disagreement to resolve before corpus preparation, not a reason to normalize expected output to production.

## Options and affected work

1. Confirm minimum closed physical feature rank, including later entry to a constant-zero face's validity interval. Release a precise private G2 correction: represent that earliest validity entry (or canonically retain its face rank after the equivalent edge/vertex root) within the same two certificates/64 slots/768 bytes/original caps. No public/API/G1/header/flag change is needed in principle, but an exact source schedule/work/lifetime proof must accompany any authorized implementation.
2. Clarify that constant-zero features emit no validity-entry candidates and minimum rank applies only to isolated eligible certificates. Then explicitly clarify the corresponding materialization rule for this case and let Q independently model that adopted convention. This is a specification interpretation, not permission for the worker to silently change an oracle.

Recommendation: option1 follows the existing closed-feature minimum-rank/unit-face wording. Do not change the production source or old frontend evidence without MAIN's exact disposition; D311 authorized only the already completed layout correction. No new source correction, compiler, test, oracle, generator or query has been executed here.

Only finalizing this constant-face expected normal/canonical-feature entry and any production correction is paused. Independent full Q/R source/schema/protection work continues. The same case fits an existing root/degenerate stratum, with no extra row, fixture, operation, work cap, width or runtime allowance.
