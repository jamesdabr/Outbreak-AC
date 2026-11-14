# T108 Engine handoff — additive capsule-pair exchange

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T1081.0 RELEASED notes-only; delivery for MAIN review, no self acceptance/status edit
- Phase / contract revisions: GOVERNANCE/BROWSER_FOUNDATION/P0 0.5; approved P1_RULES0.2/D112; frozen T0021.1 proposal graph, not approved source interfaces
- Base and pre-existing edits: shared workspace preserved; no checkout/source mutation. Last observed source HEAD in prior T002 handoff31d433b993d393b1902f7f57285a1d5ea6d2042d, not a new clean-checkout/source-build assertion. Frozen T002 input hashes below unchanged.
- Changed files: NEW notes/proposals/T002-P1-pair-query-addendum.md; own NEW notes/questions/T108-engine-common-trajectory.md; this NEW handoff and NEW notes/handoffs/T108-engine-freeze-1.md receipt.
- Commit/patch reference: no commit/Git mutation, source/header/MVP/ticket/decision/artifact edit or worker dispatch.

## Acceptance evidence

PASS means static proposal coverage, never approved implementation or measured
correctness. Re-read tickets/T108.md and P1_RULES0.2 for final submission.

| Required item | Result / evidence |
| --- | --- |
| Separate complete pure pair primitive, both starts/deltas, World/Engine ownership | PASS proposal: addendum section1 declares PairContact and QueryStatus sweep_capsule_pair, existing typed arguments only. No StaticStore/CollisionView or relative delta against world. World B owns exact geometry; Engine C owns trajectories/bilateral clamp/transaction. |
| Fields/ranges/lifetime/error/output invariants and malformed/map bounds | PASS proposal: sections1–2, borrowed nonoverlapping values, exact P1 living shape/global and actual-map responsibilities, ordered failure checks, unchanged PairContact on Invalid/IterationLimit, explicit Clear sentinel. No opaque store/new allocator. |
| Certified TOI, world witnesses/normal, symmetry/ties and special cases | PASS proposal: section3, inclusive Q32 endpoint, fixed denominator for byte-identical Q30 normal, two rounded rational witnesses, argument swap, same-bin conservative ordering/revalidation, zero/equal deltas, initial overlap/touch/separation and head-on. No push/radius inflation/damage semantics. |
| Exact bounded work and caller bilateral-clamp ownership | PASS proposal: section4, <=3 quadratic pieces/6 roots, checked8-limb arithmetic, bounded root/certificate/8192-byte temporary requirement, same fraction for both actors, no extra dt, frozen4-pass limit/fault behavior. Actual arithmetic/stack/resource proof NOT RUN. |
| Step/world trajectory integration without invented gameplay policy | OPEN scoped convention, explicitly allowed by ticket: addendum section4 and new T108-engine-common-trajectory.md explain why actual step/slide legs cannot be replaced by endpoint chords and ask MAIN to define shared interval/stance/step timing. Pure linear exchange is complete; complete piecewise caller integration is not claimed. |
| Worked example and independent/metamorphic validation plan | PASS proposal: section5 hand-worked t=1/2 example, q2147483648, mirrored normals/witnesses; independent rational/interval oracle, swap/common-motion/transforms/splitting, malformed/budget/canonical rollback cases. Tests/oracles were NOT EXECUTED. |
| Additive mapping, frozen APIs/body/numbers preserved | PASS static: section6 names exact header sections3/4/include graph and seams B/C affected after approval; no new wire/body/ID/build unit, immutable accepted fixed/envelope/map APIs and approved P1_RULES0.2 values. Original three hashes below match MAIN review. |
| Notes-only scope/freeze | PASS static: only new allowed Markdown; read-only cat/sed/rg, shasum and git diff --no-index --check inspection. No project imports/entrypoints/tests/compiler/Node/native/browser/network/service/install/source/Git mutation/dispatch. |

Actually performed commands: read ticket/governance/P1_RULES/frozen proposal and
review notes; `shasum -a 256` on the frozen original/new notes; and
`git diff --no-index --check /dev/null <new-note>` on addendum/question. Both
checks returned empty whitespace diagnostics with exit1 (new-file differences),
not executable test results. Handoff/freeze receive the same static check.
No toolchain/OS/hardware/performance or actual correctness result is claimed.

## Frozen input/output identity

Unchanged original input hashes, SHA256:

| File | SHA256 |
| --- | --- |
| notes/proposals/T002-P1-headers.md | 79fa17d45f11d480a66a57435a258811722c075e1dddc1926428958f2cb01709 |
| notes/proposals/T002-P1-wire.md | b625e2e9d8161c3fff5c2afc0f0976fc1f6d03e62d0fdb4a2ba52c15c4aeac16 |
| notes/proposals/T002-P1-seams.md | b50cd481a3cf4d4acf5822fa17f87e254f12dfaf441c9b718ccbf2b87ceb1855 |
| notes/handoffs/T002-engine-2.md | 27ec5850e938fbf07726176e3f1a79e3b2eea13383f834fd33dcde3677bb4a95 |

New addendum SHA256467fe123a20d36ffaf18382d9d7e9818798fcd5eba592844b94acba9d3231b90.
New scoped question SHA256cb044593df9b5b221b1730bc0014a7f288ba3434bc65eb4c63fa815ea88d907e.
T108-engine-freeze-1.md records these plus this handoff's terminal hash, without
editing any frozen input or requiring a self-referential hash.

## Implementation status

Implemented: new Markdown only. Simulated/test doubles: none. Unimplemented:
all proposed declarations/World narrow phase/Engine caller/test suite; no actual
native/Wasm compile, pair oracle, resource/performance or browser evidence.
Typed interface approval/full P0/individual source leases remain prerequisites.

## Integration and questions

MAIN reviews the pure linear query separately from the scoped common-trajectory
question. That question pauses only caller timeline adoption/implementation;
it does not authorize a new policy, helper source or edit to frozen MoveResult/
move_one. No dependency, asset, gameplay number, wire body, ID or terminal policy
is added/changed. D112's resolved P1-only terminal semantics remain closed.

Reproduce static review by reading addendum sections1–6, comparing its exact
extension to frozen header sections3/4 and seams stages B/C, checking the manual
example and the scoped question, then rerunning only read-only hash/whitespace
commands. Any successor edits need an explicit lease/review and successor hashes.
