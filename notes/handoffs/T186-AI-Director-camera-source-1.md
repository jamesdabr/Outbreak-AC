# Ticket handoff — T186 camera source construction

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T1861.0/D297, SOURCE CONSTRUCTION ONLY; submitted for MAIN code review, not authoritative acceptance.
- Governing: CAMERA_FOUNDATION0.2/D297; accepted427-byte camera header T181/D281; conditional T179 proof; corrected T182 section2 frozen by D297; accepted rules/basis/fixed interfaces.
- Base/overlay: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved overlay. New source was absent (including symlink check), source ancestors ordinary directories; no existing source/header/tool/evidence file edited, no Git.
- Changed files: NEW `source/outbreak/p1_camera.cpp` and this NEW handoff only.
- Patch: complete new326-line source, no existing-file hunk/build/include/consumer integration.

## Stable source and status

`source/outbreak/p1_camera.cpp`: **12659 bytes**, SHA256 **9cdb0bf7cae943812f3ff84616adbf18caf67445165ff8998918004be664748a**.

**IMPLEMENTED AS SOURCE; NOT_COMPILED; NOT_TESTED; NOT_ACCEPTED.** Complete solve_camera definition and finite private helpers are present, with no placeholder/stub/fake query. Exact source/contract/manual logical review and fixed paper arithmetic are the evidence delivered. No actual C++/Wasm ABI, stack/frame, dependency lowering, geometry behavior or runtime performance result is claimed.

## Requirement/source map

Line numbers below bind the pinned source; ranges describe source sections, not measured machine frames.

| Requirement | Source map / source-review result |
| --- | --- |
| Sole accepted signature and public-interface use | Lines1–10,205–206: p1_camera.h/fixed.h only; one ob::solve_camera definition; all20 private functions and two immutable constants in anonymous namespace. No new public type/API/constant/header/dependency. Static assertions enforce the three planned owner-object size ceilings when a future compiler runs; their success is NOT observed here. |
| Null-before-dereference; canonical context and exact hash order |208–221: map null ->Null/3/1; validate_rules_p1 false unchanged; inspect_static false unchanged; rules then angles all64-byte comparisons ->Rules/3/2,3. StaticInfo scope ends before basis/query. Only public inspected side is retained as a bounded primitive limit; no StaticStore layout/accessor/copy. |
| Exact local pose/weapon/revision precedence |222–237: positive world revision4, WeaponType5, pitch6,height7,eye8,gap9,footx10,y11,z12,bodytop13. Signed64 before gap/top arithmetic. No equality of world revision to static revision, no body/actor/observer authentication assertion. |
| Accepted basis, world-Z, full-sum FRU, None |239–258 and64–83: accepted aim_basis false tuple unchanged; E Overflow14; checked full signed FRU sum then ONE nearest/ties-away displacement division and checked eye add, ideal Overflow15/muzzle16. None muzzle explicitly0 and unused; selected Pistol/Rifle offsets from fully canonical rules. |
| Pre-query D/A/halo/length order |260–276: checked x/y/z D ->Overflow17, checked square accumulation18, endpoints/travel haloRange21, floor_isqrt and frozen D/A/L0 premises ->Invariant22. Zero span cannot divide or become successful no-query shortcut. |
| One complete real query; false preservation |278–288: exactly one sweep_sphere(view,{E,360},D,CameraMask,trace,error); false returns immediately with exact query Fault. No other geometry query/source hook. Actor/box arrays are NEVER dereferenced locally; real G2 retains complete validation before mask filtering. A partial failed result is not inspected/published. True badFault ->Invariant23, unexpected/inconsistent statuses24. |
| Both coherent successful witnesses checked |121–151,289–301: Clear both fully canonical and therefore fieldwise identical; Hit both World/NullA/nonrayNone/legal stable ID/q/distance/nonzero bounded normal, priority.q>=first.q. Malformed successful structure ->Invariant25. Primitive0 remains legal. Normal component bounds precede squaring. No physical/root/tie authentication is inferred from these structural checks. |
| Clear/Hit/ceil/clamp/displacement rounding |289–316: Clear copies ideal; Hit uses ceil33Q/L0 without overflow-prone numerator addition, guards increment Overflow19, compares first.q with backoff BEFORE unsigned subtraction. Rounded signed displacements are added to E x/y/z in order ->Overflow20; final endpoint/travel haloRange21. Clamp q0 yields E through same exact arithmetic. First witness unchanged on clamp; priority never places camera. |
| Complete staged logical-field publication |163–202,317–324: explicitly copy every TraceHit/ActorRef/point/normal/status/zone/origin field from query.first to staged obstruction, then every CameraSolution field to out. Caller output is never written before publish_solution at320. No failure follows that first write; success Fault fields becomeNone/0/0. No native padding read/memcpy-as-field-observation. |

All local faults use camera_fail at12–18, writing code/stage3/detail individually. Helper/query false tuples are not rewritten. Canonical rules/table/inspection/basis success contracts remain normal callee obligations; the frozen explicit successful-query guards apply after the one query. No invalid/lifetime-alias probe, occupied-origin rescue, radius358 resweep, normal-distance shortcut, cache/history/smoothing, MotionState or shot behavior.

## Finite private helpers and call graph

| Private helpers / lines | Finite work and callees |
| --- | --- |
| camera_fail12; equal_hash6420 | Scalar Fault writes; only new-source loop is exactly64 hash bytes, invoked at most twice. |
| add_i6428; multiply_i6435 | Scalar signed64 prechecks before add/multiply; short-circuit sign branches divide only by nonzero values with safe signed divisions. No recursion/heap/wide arithmetic. |
| nearest_i3249 | Positive denominator check before division; remainder magnitude cannot be INT64_MIN; ceil-half comparison avoids doubled remainder overflow. Checked quotient step via add_i64 then checked int32 narrow. Negative half ties round away from zero. |
| offset_component64; offset_point77 | Exactly x,y,z sequence, up(0,0,S); three checked products/two checked adds before one nearest_i32/component; checked_add_i32. Max six components for ideal+weapon muzzle, no per-product rounding. |
| add_square85 | One checked multiply_i64 square plus checked unsigned accumulation; called three times. |
| position_halo95; displacement_halo102 | Fixed three-coordinate comparisons; widened int32 differences fit signed64. No point/array traversal. |
| canonical_null111; same_position116; clear_witness121 | Fixed complete logical comparisons only; length narrow follows validated1278..7731. Both Clear records match the same complete canonical record. |
| nonzero_normal131; hit_witness142 | Fixed bounds/identity/normal checks, at most two witnesses; squares bounded before computation, sum<=3*2^60<2^62. No feature/root computation. |
| rounded_travel153 | q<=Q before signed cast/multiply, nearest_i32 with positive Q, checked_add_i32. Max three components on Hit; displacement rounded BEFORE addition. |
| copy_position163;copy_direction170;copy_hit177;publish_solution193 | Explicit finite member writes, no loops/padding reads/whole large state by value. Infallible final publication after all checks. |

External normal API callees are exactly validate_rules_p1,inspect_static,aim_basis,checked_add_i32,checked_sub_i32,isqrt_u64,sweep_sphere. Their full compiled closures are NOT bounded by declaring them leaves: canonical validator ->rules factory/encoding/hash and table comparisons; basis ->certified lookup/table comparison/normalization/root; fixed adds/subtracts ->accepted narrowing; sqrt ->existing <=32 root steps; query ->complete THEN-ACCEPTED G2/G1/wide/validation graph. No G2/private implementation is cloned here.

The new source has no indirect call, recursion, dynamic loop, heap/VLA, mutable static/cache, clock/I/O/entropy, float/libm/compiler128, World internals or actor/box dereference. Fixed source maxima, not observations: nearest rounding<=9 components, checked FRU products<=18 plus3 square/3 final products, two64-byte hash scans, one floor-root, one public sweep. Earlier failures shorten these paths; no hidden query/search or reset of query visit/work caps.

## Source liveness and resource qualification

Retain the T182 **768-byte paper envelope**, NOT an emitted-frame pass:

| Owner / scope | Paper slots and lifetime |
| --- | --- |
| StaticInfo info213–221 | <=272, bounded by future static_assert. Lexical lifetime ends before staged solution/basis/query; retain only uint64 primitive limit. This does not prove compiler stack-slot reuse. |
| CameraSolution staged240–324 | <=128, includes F/R/E/I/M/camera/obstruction, no duplicate whole solution. Future static_assert, not observed ABI. |
| TraceResult trace281–317 | <=112, ONE initialized reusable result containing both witnesses. Future static_assert. No public query work bank allocated by camera. |
| Scalars/temporary chains | <=192 source paper allocation. Main nonowner live scalar/shape slots at Hit are72 bytes (cell limit8,delta12,squared8,length4,Sphere16,numerator8,backoff8,q8). Explicit rounded_travel/nearest/add parameter-value/reference-slot+temporary accounting at64-bit pointer assumptions gives116 more,188 total. Earlier FRU chain is172 plus only8 retained scalar=180. These are logical source-slot bounds, not native calling conventions/spill/stack-alignment observations. |
| Control/alignment allowance |64 paper reserve; root borrowed-parameter/value slot allowance56 at64-bit pointers, remaining reserve plus unused scalar space are provisional. Actual compiler lowering/ABI, simultaneous inlining/spills/call alignment must be derived, not inferred to fit. |

272+128+112+192+64=768 conservatively charges all three owners even though static metadata is lexically dead before query. Concrete source scopes exclude large RulesP1/AngleTables/store copies: only public StaticInfo metadata is copied by its inspector. Aggregate value-initialization of info/staged/trace may lower to ordinary memset/bzero/copies; fieldwise publication may also be lowered by the compiler. These normal emitted callees, parameter spills/inlining/CFI/tail/runtime helpers are UNMEASURED, never zero-priced. The source slot arithmetic and size assertions do not certify emitted768, full query8192, portable caller65536, Wasm linear ABI+locals or physical VM/JIT/OS stack/RSS. All remain later mandatory proof.

## Verification actually performed

Read-only full source review with numbered lines; matched each frozen table branch and every published field; inspected accepted header/fixed/rules helper contracts; rg confirmed one sweep call, the one finite hash-loop site and no local actor/box dereference/other query/unsafe memory primitive/shot/MotionState symbol. Initial source absent and no existing-file patch. These are source inspections, not executable tests or static compiler diagnostics.

One inline `python3 -B` builtins-only fixed-paper arithmetic check completed exit0,<256 bytes:768 partition,188/180 logical scalar-chain arithmetic, normal sum<2^62, canonical FRU<2^43/final products<2^45,33Q<2^38,7732²=59783824 and arbitrary uint16-side primitive multiplication<2^34. It did not read/import/execute the new code, exercise helper algorithms, generate cases/data/oracles or call a query. No project driver/import, compiler/syntax build, test/fixture/golden/corpus generation, SDK/FFI/probe/runtime/network/Git/worker action.

## Preserved read-only input identities

| Input | SHA256 before/after |
| --- | --- |
| tickets/T186.md1.0 | 12916e3cdba40d83ff56833e5f75656d3e75bcfe831e5e80f79fb9a998f3b898 |
| notes/decisions/D297-camera-source-construction-parallel-release.md | fd4218e138f0ccd42a3b00ef944888dabc8fc0bf466ea553096eaa7623dd433e |
| MVP/CAMERA_FOUNDATION.md0.2 | f6fba5bbef5d21487f30b45b062f6b89e72f4e557b1dd51e7d91cc03f729333d |
| corrected T182 packet | ac64e4bb4a591bf7f53c4ea5a1fb832f29216c8e6dae033020c0bd65899c2c6e |
| source/outbreak/p1_camera.h | f3ab259fed5172a7763b6c85ebf873e0f1f0d501b4aaf204b2dd6f6639732174 |
| source/outbreak/p1_geometry.h | 8bfa5558899bcbaa172ce8a4ab38df3f48cae8468e9b43c976ad0e047e096a90 |
| source/outbreak/p1_rules.h | 6871e774d92b38e638856545ec898567394ee617f88c9fb9cdcafd4d1b7af3e9 |
| source/outbreak/p1_types.h | 8f9222262be5cfbc5e16f10b040b6bef95385af0db58669cfc3d0cfcc6f8b621 |
| source/outbreak/fixed.h | f2b7c303eab8ad4e4ad33593f55759196a8f711bbd791e8ad50715824aa792c3 |
| source/outbreak/fixed.cpp | d7a40cfc8e47b17965e6f31c5f9d7ad1f9650e0c3fb4b306c459cc89a4a7e49a |
| source/outbreak/p1_rules.cpp | 333b6d0717fbb9b75b74aa96426f8180ad443b49c1acf5711f2a73a7c218da5e |

These pin direct read inputs, not a fresh whole-tree inventory or in-flight geometry acceptance. Current ticket/foundation/decision were re-read at submission; no source specification conflict was identified by manual review. MAIN's independent code review may return concrete corrections under a new lease.

## Incomplete work and stop boundary

No stub, simulation, guessed World implementation or test replacement accompanies the full source. Real accepted G1/G2/current changed-source regression must precede camera compiler/query/test/composition/acceptance. Exact source/corpus/tool/role/argv/normal-frame/output/ownership preflight and separately named verification/actual leases remain mandatory; no downstream job starts automatically. Caller logical body/eye/transition/observer/revision provenance, full tick/shot/transaction/browser/reticle/comfort/performance/human and Player/nativeT167/QA/T149/fullphase holds remain unchanged. Worker stops for MAIN code review with source explicitly UNVERIFIED.
