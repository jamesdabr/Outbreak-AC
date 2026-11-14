# T159 preparation-1 coverage correction and fresh preparation scope

- Author / worker: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket and revision: T1591.4/D221.
- Phase and contract revision: WORLD_QUERY_FOUNDATION0.4; adopted execution plan c7b2844ea06f00e74a0511d44b0fac69b20a142bbdf6eae244d048c77b9afb63.
- Exact clause affected: complete finite family/predicate/transform catalog before actual effects; no repeated automatic generator retry, fresh preparation-1 only; actual attempt-1 remains unreleased.
- Status: OPEN; MAIN resolution is separate.

## Question

The first guarded preparation completed and its occupied output/source snapshot is preserved. Post-generation static inspection found coverage-construction gaps. It is **not ready for actual compiler/native/Wasm clearance**. Please review this source/preparation snapshot and assign the controlled correction/fresh-preparation scope, rather than approving an actual attempt from its successful generation status.

## Evidence and impact

Preparation manifest `tests/outbreak/geometry/G1/preparation-1/manifest.json` SHA256 `f7173ba02e86ab086c625401bc71b539e5d50c8ba7cda4a55050e876b8f518d8` records16384 rows and successful pure generation in15.825 seconds, NOT target correctness. All8 source/harness identities remain exactly the recorded snapshot. No compiler, target, SDK copy or actual attempt ran; attempt-1 remains absent.

Concrete post-generation findings:

1. Static controls use opcode1 only on odd local indices, while StorageKind is selected with `local%8`. Actual storage_spec cases therefore omit kinds0/2/4/6. Use a separately stepped control selector, e.g. `(local//2)%8`, and assert every required kind has actual opcode1 coverage.
2. Table mutation choice uses `local%9` while first/middle/last selection uses `local%3`. For a fixed choice these are correlated: yaw mutations only select8192, centidegree mutations only9000. Select positions with an independent quotient, e.g. `(local//9)%3`, and assert every required position/array is present.
3. The current catalog retains independent polynomial/normal certificates and exact row outcomes, but does not yet retain explicit transform-parent mappings or enforce every named semantic coverage predicate. A label is not a proof that a first root exercises a particular chronological piece or that a time-splitting relation was checked. Extend the finite coverage validator rather than inferring completeness from16384 rows or label totals. In particular, add literal first-contact seeds for the overlap and later upper-gap pieces and record the selected piece. A candidate upper-gap example within existing bounds is A foot(32768,32768,8192),delta(20000,0,6000), B foot(47768,32768,10278),delta0, bothh3738/r1126: its two gap boundaries are1/10 and3572/6000, and the potential horizontal approach is later. This is a proposed fixture to certify independently, not an executed target result.
4. The source snapshot contains the real native/Wasm adapters, pure generator/oracle and dormant original-handle supervisor primitive. Full future actual-driver orchestration, compiler-diagnostic call-chain analysis and controlled supervisor fault-regression execution are not yet complete. `verify.py` deliberately refuses direct actual entry. Complete these as inspected source before requesting an actual-run lease; do not treat the dormant primitive as a completed actual verifier.

These are harness/preflight gaps, not evidence that production geometry is accepted or incorrect. No cap, API, numerical behavior or resource requirement should change. The generated expected stream remains a useful independently computed snapshot, but it cannot discharge the full adopted coverage requirement.

## Options for owner and lead

Recommended: return the current source/preparation snapshot for focused correction, preserve preparation-1 unchanged, explicitly authorize a separately named fresh preparation output and one new guarded generation after source/static review. Keep the exact16384 rows and all family/subfamily/byte/time caps; replace redundant rows within the existing reviewed allocation, add required predicate/transform assertions, and complete the actual-verifier source before the new stable source pin.

Alternatively review production source first and serialize the harness/corpus correction as a separate follow-up ticket. Either option must keep actual attempt-1 absent until the corrected full source/harness/generated manifest has MAIN static clearance. Neither generation success nor elapsed15.8s is a basis to waive missing cases or compiler frame evidence.

## Work paused

No preparation-1 overwrite/rerun, source mutation that would silently stale its identities, SDK copy, compiler, target, actual attempt, freeze or integration. Current snapshot and all accepted dependencies are preserved for MAIN review. This note and the new source/preparation handoff are the only post-generation writes.
