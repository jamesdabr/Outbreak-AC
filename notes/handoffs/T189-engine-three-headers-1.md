# Ticket handoff

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T1891.0 / D303, EXACT THREE NEW HEADERS ONLY
- Phase / contract revisions: approved MOTION_INTERFACE_FOUNDATION0.1/D303; accepted T183 notes/D299; separate D284/D295 construction clauses. Full G2/typed behavior/M4/owner/movement implementation remains pending. Existing World T187 source and AI camera checks are disjoint; no permission inferred for their code or evidence.
- Base commit and pre-existing edits: ticket-provided bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved overlay; no Git. lstat/lexists confirmed all three header paths and this handoff absent before creation, including no dangling-link conflict. Existing source scan found only p1_shot.h's MotionState forward declaration, no full MotionState/MoveResult/private records or move_one/move_joint declarations. No unrelated edit was reverted or modified.
- Changed files: NEW source/outbreak/p1_motion_state.h, NEW source/outbreak/p1_motion.h, NEW source/outbreak/p1_motion_private.h; NEW this handoff notes/handoffs/T189-engine-three-headers-1.md.
- Commit or patch reference, if explicitly authorized: none.

## Acceptance evidence

| Ticket criterion | Observed result |
| --- | --- |
| Exact authority/read boundary | PASS read-only: full T189/D303/foundation, actual types/input/geometry/camera/shot headers, AGENTS and required README/GOVERNANCE/CONTRACT/PARAMETERS/INTERFACES/P1 phase read. Draft phase scope was not treated as implementation authority beyond D303. Ticket/foundation reread during literal verification; revision1.0 unchanged. |
| Paths/symbols absent | PASS before mutation: all three paths absent by lexists (including dangling links); only existing MotionState forward declaration in p1_shot.h. No conflicting full definitions or movement declarations/owners found. |
| Literal headers | PASS text inspection ONLY: each entire new file equals its corresponding foundation cpp code block byte-for-byte, including whitespace and final newline. No extra enum, helper/body/validator/constructor/assertion/export/comment/fallback overload. |
| Metadata | PASS each new header is an ordinary regular file, mode0644,nlink1. No symlink/hardlink or replacement of an existing file. |
| Sole full MotionState home | PASS actual source scan: p1_motion_state.h ONLY full definition, both retained stance origins explicit; includes only p1_types.h. Existing p1_types.h unchanged. Existing p1_shot.h MotionState; is a forward declaration and unchanged, not another definition/home. |
| Public/private include/type homes | PASS p1_motion.h includes geometry,input,state actual homes and contains sole MoveResult/move_one declaration with explicit self/table/scratch. Private header includes only p1_motion.h, motion_private namespace owns sole InputUse/TickActorIn/TickIn/TickOut/move_joint declarations. Existing InputFrame/CameraPose/HitZone definitions remain their accepted homes; no SimStore/World/advance_tick, codec or callable adapter added. |
| Preserved-input boundary | PASS size/hash/mode/nlink comparison: all25 snapshotted existing inputs unchanged (10 authority/instruction/contract files +15 existing Outbreak headers). Header membership changed exactly15->18, the three authorized additions only. Existing source bodies/builds/consumers/tools/evidence/assets were not written by this task; active disjoint workers' bodies are not claimed frozen or owned here. |
| No forbidden evidence/effects | PASS observed tool history: cat/wc/rg/ls, read-only standard-library lstat/byte/hash/literal comparisons and apply_patch only3 new headers/this note. No project import/compiler/mirror test/ABI probe/fixture/oracle/data generation/SDK/FFI/runtime/query/network/Git/build/consumer/dependency or worker-dispatch operation. |
| Compilation/ABI/runtime | NOT_COMPILED; ABI/layout assertions NOT RUN; native/Wasm/query/runtime/performance NOT RUN. Literal equality/sole-home inspection is the assigned evidence, not source-consumer or platform proof. |

Exact new file identities:

| File | Bytes | SHA256 | Mode | nlink |
| --- | ---: | --- | --- | ---: |
| `source/outbreak/p1_motion_state.h` | 445 | `4ac3aa394a62d6a459e89c8fe78c63737a4b7d76a8e96a90174cb841dbc250fc` | 0644 | 1 |
| `source/outbreak/p1_motion.h` | 492 | `40ce3fbacc71b76f19b889b7f0642878ee67b78ca0953ba2315f7f9b196b26ae` | 0644 | 1 |
| `source/outbreak/p1_motion_private.h` | 827 | `a36e48041741ca304cacad0645f2eca4f06e59654c62bcec4d96a46ddc154bfc` | 0644 | 1 |

Reproducible inspection: read the foundation with pathlib, extract its THREE cpp fenced blocks with a bounded text regex, compare each file's raw bytes, inspect lstat regular/mode/nlink, SHA256 the new files and existing protected inputs. This is literal/metadata inspection, not a generated fixture, mirror test or compiler. Source-only rg over source/**/*.h and source/**/*.cpp found exactly one full definition of each new record and one declaration for each new function; the shot forward declaration was separately distinguished. New direct includes match the foundation blocks. No implementation/function body or source consumer includes were added.

Proposed/reviewed envelopes remain UNMEASURED: MotionState64/align4 required<=64/align<=8; MoveResult68/align4 required<=80/align<=8; private TickActorIn<=48/TickIn<=48/TickOut<=640. No actual sizeof/offsetof/compiler-frame result is asserted. Native memory is not wire; Motion60/Own204/baseline1144 remains a future reviewed encoding proposal requiring separate freeze/real bytes. Original T180786432 arena/768 bridge/query8192/fullcaller65536 limits are not increased or discharged by a header.

Protected read-only input snapshot (all compared unchanged before handoff; final recheck follows creation):

| Input | Bytes | SHA256 |
| --- | ---: | --- |
| `AGENTS.md` | 4097 | `ce448e974df50fd14c91e15570c234c284053492eaf94e292828d201cd5c5f7b` |
| `tickets/T189.md` | 1848 | `cbbbb081036c0dc968d45fa3522262b2ae9158a43e5c39f82f7f0182ec456057` |
| `MVP/MOTION_INTERFACE_FOUNDATION.md` | 4986 | `de795a0f3a412b6aaf72ebfbde88009efc193457214bd28e55df803f31a68470` |
| `notes/decisions/D303-movement-declaration-materialization.md` | 1708 | `394b7419150acfc3dfe1aaa2bde11c1751c55d394b869ef3a61cd96f9425cfde` |
| `MVP/README.md` | 3701 | `a78e1ac9ab9fb47ce39c6a6bbf3986d1785a67d81b672914877895a65994f097` |
| `MVP/GOVERNANCE.md` | 13305 | `e5363e7f8b63588c184d4e64f6b8086d4e17a3876ee67f654e8170e1023c0016` |
| `MVP/CONTRACT.md` | 7402 | `339fa42db7a6e4a9bc777e2906970c69c4bb0b205a333fddd836cbcf2977d59b` |
| `MVP/PARAMETERS.md` | 5092 | `d996f740e144b797ab8841003dd85eabed6da364cbdf2e67ffb7ffeb4eec7396` |
| `MVP/INTERFACES.md` | 3996 | `1c8274267e938905d8d7a65e27d3b27a4d6a1d823d3d97e51d282eb0f9d16b3c` |
| `MVP/phases/P1-combat.md` | 1495 | `43c27cd1a0ba812840f456a5c7063b4eb4688a1d54b5f4f8a62845894a709484` |
| `source/outbreak/envelope.h` | 975 | `5a9ed4462b5c3fdcb61fced19293b335c4ea12994d8b8bb9f89584d3598b6168` |
| `source/outbreak/fixed.h` | 615 | `f2b7c303eab8ad4e4ad33593f55759196a8f711bbd791e8ad50715824aa792c3` |
| `source/outbreak/map_import.h` | 682 | `a8ee019deec650add0cc885dba337ef70517106dc9719fceb0535ce6e664c90f` |
| `source/outbreak/p1_camera.h` | 427 | `f3ab259fed5172a7763b6c85ebf873e0f1f0d501b4aaf204b2dd6f6639732174` |
| `source/outbreak/p1_geometry.h` | 3367 | `8bfa5558899bcbaa172ce8a4ab38df3f48cae8468e9b43c976ad0e047e096a90` |
| `source/outbreak/p1_hash.h` | 152 | `4492332dcad22c68ac983491e89bf81fbbccad1b82f2abc825e4c24140e8c3f3` |
| `source/outbreak/p1_input.h` | 443 | `e8ad0291d5cb33d68b4ed8050daf1684fbbb03d40eb0b735305940278095bddd` |
| `source/outbreak/p1_input_batch.h` | 328 | `683674269a669c77be4a6f5fe51f65e8dcc9f23810c4cc9bdf398e19368d7452` |
| `source/outbreak/p1_query_wide.h` | 9202 | `715521a8f35e959f2e338dbc48db412c2dff81b2de2fa773707169dad28f3e83` |
| `source/outbreak/p1_rules.h` | 1442 | `6871e774d92b38e638856545ec898567394ee617f88c9fb9cdcafd4d1b7af3e9` |
| `source/outbreak/p1_shot.h` | 652 | `61c3c1dd5f0cf3d7898fd7e626cbb1eb0ca4d7dece194b45cf9971f36d8d25ea` |
| `source/outbreak/p1_spread_cone.h` | 425 | `5a3d7be39ff47205f8a172ec22ba4645451bb7d484f8a42791296f9b08475be9` |
| `source/outbreak/p1_spread_rng.h` | 325 | `54eacd6a645ed9daeae9246d3957933fecd9b5c50434e3639fa07e49cc754acd` |
| `source/outbreak/p1_store.h` | 393 | `7a7b185ddba685cfdf313398c24558e54abb1ca674d2e305793e27420d4c0bc3` |
| `source/outbreak/p1_types.h` | 2378 | `8f9222262be5cfbc5e16f10b040b6bef95385af0db58669cfc3d0cfcc6f8b621` |

## Implementation status

Created ONLY the three literal declaration headers. Implemented movement/validation/stance/Q1/solver/store/codec/camera/shot/runtime behavior: NONE. Simulated behavior/generated corpus/oracle/fixtures/goldens: NONE. Compilation, native/Wasm ABI/field offsets, frame/work/caller/resource proof, query execution, gameplay/transport/browser/performance/human acceptance: NOT RUN. Declaration materialization cannot create a valid living actor or commit a tick.

D303 supersedes the unadopted H/T183 p1_types home ONLY for the full MotionState record. The existing accepted core header is untouched; no historical T183 note/decision was amended. D303 does not adopt the rest of full validation/Fault/alias/stance/proxy/encoding/transaction semantics beyond separately adopted D284/D295 clauses. Owner horizontal selector is not chosen, exposed as an argument or asked again.

## Integration and questions

No conflict/question required. No shared existing file/dependency/asset/codec/build/include consumer changed. Future specifically leased consumers must include the new state/public/private homes as appropriate and establish proper typed backing/lifetime/alias/Fault/source coherence; namespace privacy is no adapter call grant. The existing shot forward declaration remains compatible without adding an include or fabricating a smaller type.

Full accepted G2/current G1 changed-source regression, complete M4/owner/type-behavior/private/public caller/proxy/codec/source/evidence freeze and separately named implementation/actual/tick/browser/normal-impaired/performance/human/native/Player/QA/T149 gates remain. Submit exact headers/new handoff after final identity check and STOP for MAIN review; no automatic body/compile/test/runtime continuation. Ticket/phase acceptance remains lead-owned.
