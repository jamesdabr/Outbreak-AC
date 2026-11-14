# Ticket handoff — T181 exact camera interface header

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket / revision: T181 1.0, RELEASED EXACT INTERFACE HEADER ONLY D280; delivery for MAIN review, no authoritative status change.
- Phase / contracts: CAMERA_FOUNDATION 0.1/D280; accepted conditional T179/D279; actual geometry/rules/type homes. Full G1/G2/P0/consumer implementation remains unaccepted.
- Base and pre-existing edits: ticket base bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved overlay. No Git command was used. The assigned header was absent before creation; unrelated existing files were read-only.
- Changed files: NEW `source/outbreak/p1_camera.h` and this NEW handoff only.
- Commit/patch: none; direct allowlisted new-file materialization.

## Acceptance evidence

| Criterion | Result | Evidence |
| --- | --- | --- |
| New header absent, ordinary directory ancestors | PASS | `ls -ld` of /Users, /Users/jd1, code, apps, outbreak, source and source/outbreak showed ordinary directory entries; `test -e` and `test -L` both found no header before creation. Created file is an ordinary 427-byte file. |
| No existing actual CameraPose/CameraSolution/solve_camera home | PASS | Before creation, a word-boundary rg search for all three symbol names across actual source C/C++ headers/sources returned no match. After creation, the only matches are p1_camera.h lines5,8,11,12. Historical Markdown proposals are not actual declarations. |
| Literal contract content, sole include, namespace and immutable table borrow | PASS | Read the complete new header; compared bytes against CAMERA_FOUNDATION's sole cpp block using `sed -n '/^```cpp$/,/^```$/p' MVP/CAMERA_FOUNDATION.md` followed by `sed '1d;$d'` piped to `cmp - source/outbreak/p1_camera.h`. No differences. Only include is p1_geometry.h; namespace ob; exact two records and sole function declaration with `const AngleTables &`. No implementation/helper/extra API or constant added. |
| Byte identity and preserved direct inputs | PASS | SHA256/byte reads below; authority and existing direct header input hashes match before/after. Re-read current ticket/contract before submission. |
| Compiler/syntax probe/test/mirror harness/consumer/runtime | NOT RUN, explicitly excluded | No compiler, project import, SDK/FFI, fixture/oracle/dataset, runtime/browser/network, dependency or Git operation. Text comparison is literal inspection, not a test harness or compilation claim. |

New header: **427 bytes**, SHA256 **f3ab259fed5172a7763b6c85ebf873e0f1f0d501b4aaf204b2dd6f6639732174**.

## Read-only preserved identities

| Input | SHA256 before/after |
| --- | --- |
| tickets/T181.md 1.0 | 05ec1a7b3e35aa69eff5604c4f467998fca2488489e1256660d1475b508f80b0 |
| MVP/CAMERA_FOUNDATION.md 0.1 | 69f18ae49dd237856e28ba74344e4ecd229d982a968a0b0792a9eb56c308b533 |
| notes/decisions/D280-camera-interface-and-placement-adoption.md | 0603fd1df7ed9fb0c6a3f671e3bcdd570f733bfec0645d19ab80e6b43909115a |
| source/outbreak/p1_geometry.h | 8bfa5558899bcbaa172ce8a4ab38df3f48cae8468e9b43c976ad0e047e096a90 |
| source/outbreak/p1_rules.h | 6871e774d92b38e638856545ec898567394ee617f88c9fb9cdcafd4d1b7af3e9 |
| source/outbreak/p1_types.h | 8f9222262be5cfbc5e16f10b040b6bef95385af0db58669cfc3d0cfcc6f8b621 |

Hashes identify inspected direct inputs; they do not claim a fresh whole-repository preservation inventory or broader source/runtime acceptance. Reads used ordinary shell text/filesystem/hash tools only. No build, ABI, target, performance or hardware measurement is claimed.

## Implementation status

Materialized only the exact CameraPose/CameraSolution and solve_camera declaration header. No function definition, caller, consumer, simulation or test double exists as part of this delivery. Header content freezes no additional semantics beyond CAMERA_FOUNDATION0.1. None-camera-only, physical358/computational360, paired-domain/provenance, one-sweep and atomic-failure requirements are future implementation obligations.

## Integration and questions

Sole new interface home is p1_camera.h; it borrows existing CollisionView/RulesP1/AngleTables/types/TraceHit through geometry, with no extra dependency or asset. No ambiguity found in the literal header assignment. MAIN reviews and accepts or returns this delivery before any successor work.

Future real consumers must compile and validate the header and full behavior after accepted G2 and a separate named release. Full actual geometry/provenance/feasible paired-state/observer/shot/transaction/browser/human gates, Player/nativeT167/QA/T149 holds remain mandatory and unchanged. No current caller/ABI/wire/runtime guarantee follows from declaration materialization. Stop for MAIN acceptance.
