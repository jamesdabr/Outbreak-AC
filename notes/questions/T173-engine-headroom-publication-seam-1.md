# T173 headroom participation and stationary publication seam

- Author / worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket and revision: T1731.0, READ-ONLY PLAN + NEW NOTES ONLY.
- Phase and contract revision: WORLD_QUERY_FOUNDATION0.5; QUERY_PUBLICATION0.1/D203; T155 packet2 adopted as the mandatory G2 boundary under D211/D256.
- Exact clause or interface affected: packet2 sections3,7–9; QUERY_PUBLICATION's stationary single obstruction; `headroom(const CollisionView &,const Capsule &,ActorRef,HeadroomResult &,Fault &)` in source/outbreak/p1_geometry.h.
- Status: OPEN (lead resolution is recorded separately).

## Question

Please freeze the implicit participation and complete stationary headroom result convention before its source lease. The signature has no mask argument; actor participation is defined for Move/Bullet, and packet2 defines Touching as feasible/Clear and strict overlap as Hit, but does not explicitly name headroom's implicit mask or the obstruction ordering among multiple strict overlaps. Its single obstruction also needs an explicit Clear record convention, rather than inferring it from a moving query.

## Evidence and impact

Packet2 SHA256 cd41ac77fc201fa1137aeaea3bcf5a4cccfb4e5c5186651bb108885768118325 section7 says headroom is stationary, Touching Clear, strict overlap ordinary Hit with q0/distance0/normal0/diagnostic foot; false preserves the whole HeadroomResult. Section3 restricts view actors to masks including Move/Bullet. The frozen header SHA2568bfa5558899bcbaa172ce8a4ab38df3f48cae8468e9b43c976ad0e047e096a90 supplies ignore but no mask. QUERY_PUBLICATION0.1 says all headroom obstruction times0 and retains the selected existing witness. Existing G1's stationary PoseFeasibility selection is not itself a HeadroomResult definition and validates only P1 living shapes/owner identities.

This is a small G2 adapter/publication seam, not an invitation to change geometry, capsule dimensions, tolerances, storage, or movement rules. The rest of T173's source/work/traversal/oracle/frame/evidence plan proceeds independently. There is no current source implementation lease to pause.

## Options for owner and lead

Recommended explicit closure, if it matches the intended frozen semantics: headroom has implicit MoveMask; validates the complete view/ignore first and filters exact ignore; World and nonignored actors participate. Only strict overlaps obstruct. All obstruction times0; choose World before Actor, World primitive ID ascending, ActorRef(slot,generation,life) ascending, fixed feature order on identity equality. Hit record has own identity, q0,distance0,point=queried foot,normal0,zoneNone,originNone. Clear uses the same canonical stationary-endpoint Clear TraceHit as zero-travel body queries (q=Q,kindNone,id0,NullA,foot,zero distance/normal,zoneNone,originNone); outer HeadroomResult.status=Clear. On success FaultNone; all faults preserve the complete output.

Alternatively MAIN can point to an already accepted clause specifying different implicit participation/order/Clear tuple, with its exact reference and expected records. Do not implement a worker-selected alternative or a static-only shortcut. T173's proposed case allocation can bind either exact resolution without deleting any family or increasing caps.

## Work paused

Future headroom-specific implementation and its exact expected output tuples await this narrow recorded resolution plus the independently required accepted G1 proof and named G2 lease. All source/fixtures/tests/effects remain unreleased by T173. No worker negotiation or amendment occurred.

Authority observation before submission: foundation0.6/T1591.9/D258 separately permits World's exact G1 actual proof; no G1 acceptance or G2/headroom semantic resolution follows. T1731.0 and this notes-only question remain unchanged in scope.
