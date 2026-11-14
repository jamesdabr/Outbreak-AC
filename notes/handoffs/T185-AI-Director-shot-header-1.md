# Ticket handoff — T185 exact shot declaration header

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T1851.0, RELEASED EXACT NEW HEADER ONLY D294; submitted for MAIN review, no authoritative status change.
- Contracts: GOVERNANCE0.5/D294; SHOT_FOUNDATION0.1; accepted camera header T181/D281. Full typed MotionState/G1/G2/camera/shot implementation remains separately gated.
- Base/pre-existing edits: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved overlay; no Git. Header absent before creation; existing files read-only.
- Changed files: NEW `source/outbreak/p1_shot.h` and this NEW handoff only.
- Commit/patch: none authorized/performed.

## Acceptance evidence

| Criterion | Result / evidence |
| --- | --- |
| Absent path/ordinary ancestors/no overlapping definition | PASS. Before creation, both existence/symlink checks found no header; ls of every ancestor through source/outbreak showed ordinary directories. Word-boundary searches across actual source C/C++ headers/sources found no shot symbols or MotionState. rg exit1 meant no matches, not a failed source operation. |
| Exact literal header, sole include and symbol homes | PASS. Read every line and compared bytes with SHOT_FOUNDATION0.1's sole cpp block via sed extraction piped to cmp; dedicated comparison exit0/no differences. Only include p1_camera.h; namespace ob; exact ShotKind/AcceptedShot/SpreadDraw/ShotResolution/resolve_shot and borrowed const AngleTables. Subsequent actual-source search finds these symbols ONLY in p1_shot.h. MotionState is a forward declaration ONLY. No duplicate HitZone/CameraPose/InputFrame or extra helper/API/definition. |
| Ordinary0644/single-link identity | PASS. stat reports mode644,nlink1,Regular File,652 bytes. No chmod/repair was needed. |
| Preserved input identities/revision checks | PASS. Ticket/foundation/current inherited headers match before/after SHA256 below; re-read ticket1.0/foundation0.1 before submission. One read-only hash request used an incorrect D294 filename and returned ENOENT; rg identified the exact existing decision path below, then its hash was read successfully. No write/effect followed that lookup error. |
| Compiler/tests/ABI/runtime | NOT RUN, explicitly outside the exact-header lease. No syntax probe, fake MotionState/mirror harness, project import, fixture/oracle/data generation, SDK/FFI/probe/runtime/network/Git/worker effect. Literal inspection is not compilation or implementation evidence. |

New header: **652 bytes**, SHA256 **61c3c1dd5f0cf3d7898fd7e626cbb1eb0ca4d7dece194b45cf9971f36d8d25ea**.

## Read-only input pins

| Input | SHA256 |
| --- | --- |
| tickets/T185.md1.0 | 77f6bbc767a0a4133ca0acdbf339c43843307732b1d88b5ccda59160ebdea82d |
| MVP/SHOT_FOUNDATION.md0.1 | d56f9d2b5707864b65d9087257b0e6d3479ed26fdd2ff4b51289c810a2d8a91a |
| notes/decisions/D294-shot-packet-and-header-materialization.md | b0682b3207c28d8b7aa66dfefbecec8d05fd6d3b31c451fb61ea79fae6e92d0f |
| source/outbreak/p1_camera.h | f3ab259fed5172a7763b6c85ebf873e0f1f0d501b4aaf204b2dd6f6639732174 |
| source/outbreak/p1_geometry.h | 8bfa5558899bcbaa172ce8a4ab38df3f48cae8468e9b43c976ad0e047e096a90 |
| source/outbreak/p1_rules.h | 6871e774d92b38e638856545ec898567394ee617f88c9fb9cdcafd4d1b7af3e9 |
| source/outbreak/p1_types.h | 8f9222262be5cfbc5e16f10b040b6bef95385af0db58669cfc3d0cfcc6f8b621 |

Pins identify direct inspected inputs, not a whole-repository inventory or compiled ABI claim.

## Implementation status and integration

Materialized declarations ONLY; no function implementation, consumer, MotionState definition, simulation/test double or generated evidence. SpreadDraw still contains both FULL supplied uint32 words, unchanged names/mapping; no bin conversion/RNG or eligibility behavior. Header existence does not adopt the remaining T184 local Fault/validation/alias/storage/evidence-composition proposals or Engine M4.

No existing include/build/dependency/asset/source change. No ambiguity in the literal assignment remains. MAIN reviews the exact artifact; worker stops. Full typed/G1/G2/current regression/camera/shot/caller/transaction/two-browser/renderer/human/performance gates and Player/nativeT167/QA/T149 holds remain mandatory. Compilation, ABI and runtime must be established only by separately released actual consumers; none is claimed here.
