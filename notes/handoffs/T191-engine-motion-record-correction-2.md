# Ticket handoff

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T1911.1 / D306/D312, OWN PROPOSAL CORRECTION ONLY
- Phase / contract revisions: GOVERNANCE0.5; MOTION_INTERFACE_FOUNDATION0.1/D303/D304 declarations; MOVEMENT_PREPARATION0.1/D295; accepted closed T183 notes/D299. No validator/codec/API/record semantic adoption or source/evidence operation.
- Base commit and pre-existing edits: no Git. Original proposal27982/850003a666a557c3d37bc86b9be190b96f1c54cc401ccbd7527f41af25f74420 existed and was reviewed. Independent review/original handoff and all source/authority/proof files preserved. No overlapping owner or unrelated edit touched.
- Changed files: ONLY own `notes/proposals/T191-motion-record-codec-contract-1.md`; NEW this handoff `notes/handoffs/T191-engine-motion-record-correction-2.md`.
- Commit or patch reference, if explicitly authorized: none.

## Acceptance evidence

PASS denotes requested text correction/identity comparison, not a compiled or executed codec/alias fixture.

| D312 criterion | Result |
| --- | --- |
| Read updated assignment/review | PASS: full T1911.1, D312 and independent review e69bdbb37b8c8f2935c3c6de033a60dd36c1e6fe7ea4c672b1c1d7622393c72e read. Review R1 is one genuine original preservation contradiction, not an implementation failure. |
| Descriptor versus source distinction | PASS corrected section4: full DECLARED payload span disjoint from live ByteBuffer descriptor; SOURCE MotionState tested ONLY against append60, preserving read-only source-prefix/suffix success. No descriptor-byte preservation exception or whole-capacity source ban. |
| Checked bounds and first error | PASS: order4 adds full payload address/end representability at unchanged {Overflow,9,259}; order5a full-payload/descriptor then5b append/source, both unchanged {Invariant,9,260}. Used/capacity/null/record order and every decoder tuple unchanged. |
| Publication/preservation consistency | PASS: .used+60 publication occurs in descriptor proved outside the payload, so unchanged outside-append payload promise now holds. All false payload/descriptor bytes remain preserved through independent Fault. No native-padding promise, impossible typed overlap or fictitious allocation added. |
| Defined required alias case | PASS planned EFP01: live enclosing aggregate with ByteBuffer member then128 live bytes, character view of actual whole owner, capacity actual sizeof, used actual tail offset, sufficient/disjoint append. Full-payload descriptor overlap REFUSES order5a unchanged despite append disjoint. Future actual<=256 backing assertion, not measured layout. No fixture created/executed. |
| Required successes/finite union | PASS EFP02 ordinary descriptor-disjoint success and EFP03 source-in-unmodified-prefix success retained. Three named slots are WITHIN original64 encoder framing/alias rows. Total512/V176/E144/D192, two jobs/12 actual children/all byte/work/caller/time caps unchanged; no new rows/allocations or hidden multiple SUT calls. |
| No unrelated contract change | PASS read-only text equality checks: record/API/wire sections1–3, entire decoder contract and byte/job/work/frame plan unchanged verbatim from original reviewed proposal (block hashes below). Only encoder alias-consistency prose/case mapping, correction status and current input qualification changed. |
| History/input protection | PASS snapshot: old21 comparison changed ONLY ticket1.1, remaining20 matched. Added D312/review/original handoff =>24 pins. Original handoff/review bytes preserved; the named proposal is edited IN PLACE, old SHA explicitly HISTORICAL_REVIEWED_IDENTITY, NOT a preserved immutable proposal snapshot. Current qualification is T1911.1/D312. Accepted headers/input codecs/T183/source/proof files read-only. Fresh final24 check follows this handoff. |
| No effects/adoption | PASS observed: read-only text/hash inspection and apply_patch ONLY own proposal/new note. No source/header/authority/test/old note mutation, project/own import, generator/catalog/oracle/fixture/control, compiler/link/SDK/FFI/probe/runtime/network/Git or worker negotiation/dispatch. PROPOSAL_ONLY/NOT_IMPLEMENTED/NOT_EXECUTED retained. |

### Exact clause diff

| Location | Original reviewed clause | Corrected proposed clause |
| --- | --- | --- |
| Encoder order4 | checked append start/end or known object end representability | checked FULL `[data,data+capacity)` span AND append start/end AND known source/descriptor object ends; SAME Overflow9/259 position |
| Encoder order5 | append60 overlaps source OR descriptor | 5a FULL payload overlaps descriptor;5b append60 overlaps source; SAME Invariant9/260 position for either |
| Success publication | outside-append payload unchanged while .used advances, without excluding a prefix/suffix descriptor | SAME preservation guarantee, now justified by full-payload descriptor disjointness before publication; no descriptor exception/padding promise |
| Alias explanation | written range only; descriptor reject only if append overwrites it | written-range SOURCE check preserved; DESCRIPTOR rejected anywhere inside FULL payload, even when append disjoint |
| Existing64 encoder rows | generic valid-span/disjoint-prefix checks | explicitly EFP01 descriptor-in-prefix refusal, EFP02 ordinary success,EFP03 source-prefix success, within SAME64 and all other original obligations |
| Status/pins | T1911.0/old21 inspection | T1911.1/D312 correction, current24 inspection and explicit historical reviewed identity; original handoff/review unchanged |
| Historical identity wording | prior correction inaccurately said old proposal/handoff/review keep historical bytes | proposal edited IN PLACE; old proposal SHA is HISTORICAL_REVIEWED_IDENTITY only, no immutable snapshot created; old handoff/review files unchanged and CURRENT T1911.1/D312 proposal SHA reported below |

The original contradiction is acknowledged, not reclassified as a success: a valid descriptor-in-prefix aggregate previously passed the append-only check, then publishing used changed bytes promised unchanged. The selected correction rejects that well-defined case. No execution was needed or permitted to establish this text-level inconsistency.

Protected unchanged text blocks, compared directly to the original27982-byte proposal text read into MEMORY before editing. This records an in-memory before/after comparison, NOT a claim that a durable immutable original-proposal byte snapshot was created:

| Block | SHA256 before AND after |
| --- | --- |
| `record_api_wire` | `260244e721e504276eb18f76fe1dfe99d8c471dcb1214345afb41346fdbe72e2` |
| `decoder` | `b7a42311db45e4090a9336f9750ade9da1f47a77060f385a0c1b95e7ad541bc6` |
| `byte_job_work` | `fe2c2b77eff19483d6498ebd78d0a14738d4165a8262fc666ddd7eab4dc919ef` |

CURRENT T1911.1/D312 corrected proposal identity:31961 bytes/SHA256 `642822790eb368a9726b322900a2ef9f8d24dfbe662f0692611c01e484268c99`. Original27982/850003a666a557c3d37bc86b9be190b96f1c54cc401ccbd7527f41af25f74420 is HISTORICAL_REVIEWED_IDENTITY only; that SHA is not current and no immutable original-proposal byte snapshot exists in this delivery. Original handoff/review files below ARE unchanged.

Preserved prior records:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| `notes/reviews/T191-motion-record-contract-review-1.md` | 6979 | `e69bdbb37b8c8f2935c3c6de033a60dd36c1e6fe7ea4c672b1c1d7622393c72e` |
| `notes/handoffs/T191-engine-motion-record-contract-1.md` | 8483 | `e1ec2148901f06072845c9c1078fd4b9fea838cbb57fbe6aa6e5d0de945f4d7a` |

Reproducible checks used standard-library pathlib/hashlib/json/re for literal size/hash inspection, current input comparison and exact old/new text-block equality. No runtime object/alias test, case enumeration, generated bytes or arithmetic oracle was performed. Original512-row/byte/work sums remain the previously proposed paper accounting, not executed source results. Native/Wasm/ABI/frame/toolchain/performance NOT RUN.

## Implementation status

PROPOSAL_ONLY / NOT_IMPLEMENTED / NOT_EXECUTED. No validator/codec/header/source/data/control created or executed. Future full declared-span checks are proposed source obligations, not a newly adopted API or an actual passing alias test. Exact record-domain/wire/native/parent separation and D295 Fault disjoint API precondition remain. No owner horizontal selector or new grounded/air/weapon/rate constraint was chosen.

## Integration and questions

No new question required: D312 selects this exact correction for re-review. No accepted header, parent codec/Input28/envelope or query/camera/shot proof archive changed. MAIN must re-review corrected text and separately adopt/release before any source/preparation/actual operation. Existing full query/source/caller/tick/browser/human/nativeT167/Player/QA/T149 gates unchanged.

Submit stable corrected text/exact diff/current input qualification and this NEW handoff after fresh final identity verification, then STOP for MAIN review. Any new unannounced relevant authority/input change must be reported rather than silently repinned. Ticket status remains lead-owned; no automatic implementation follows.
