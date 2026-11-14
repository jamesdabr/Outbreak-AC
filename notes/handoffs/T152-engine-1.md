# T152 private collision arithmetic packet — notes handoff

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket/revision: T1521.0 RELEASED notes-only /D186; approved P1_RULES0.2/D150 qualifications and accepted numeric/core/hash context. No status change/adoption/selfacceptance.
- Changed: NEW notes/proposals/T152-private-query-arithmetic.md and this own new handoff only. All source, other proposals, contracts/tickets/decisions, SDK/tools/drivers/attempts and Git unchanged. T150/T151 exclusive ownership untouched.
- Packet SHA256:241f543b71e6663d55342ccd3f398ea52f575e9fe9d5cfa25e97af89a3b5ef7d;2743 whitespace-delimited words. Final ticket/P1 revision re-read unchanged before submission.

## Delivery and criterion coverage

PASS proposal coverage — specifies private C++11 header-only ob::query_wide Int<8>/Int<16>, exact little-word signed magnitude/canonical zero,13 necessary operation signatures, exact return statuses/refusal precedence, whole-input alias support, dual-output alias refusal, scalar/partial-overlap preconditions and unchanged outputs. No gameplay/public API/types/hash/fixed change, generic bigint/rational/radical library or new production translation unit.

PASS operation justification/bounds — maps operations to pinned pair/timeline coefficients, discriminants, certificates, normalization, witness rounding and distance ties. Checked u64 carry/borrow and product bounds,2N product overflow detection, bounded W+1 guard division, nearest/ties-away division without overflowing2r, two-bit restoring sqrt/rem, sign-safe import/narrow/zero rules and exact literal loop caps documented. D150’s qualified pair512-bit scope preserved; no universal340-bit or full World certificate. Domain/certificate failure remains query-owned, arithmetic refusal never becomes Clear.

PASS ownership/resource plan — proposes ONE explicit initial Engine lease for new private p1_query_wide.h and a new isolated harness; World later consumes accepted header read-only, transfers/corrections require MAIN lease, no concurrent header edits. Planned live-array ledger and conservative1480-byte payload reserve plus proposed2048-byte compiled helper-chain ceiling are NOT measurements; existing whole-query8192/whole-chain64KiB/full-tick limits remain. Complete feature/winner/width/query-work/liveness/performance proofs remain separately required.

PASS independent test plan — same real production header on native/Wasm, independent Python integers/isqrt, signed truncation/rounding oracle, finite<=8192 vectors in five bounded families,<=304byte rows/4MiB corpus, raw per-target output<=2490368bytes and8MiB combined log cap. Includes every needed operation’s signs/zero/limit/carry/borrow/shift/quotient/root boundaries, overflow and full-output preservation, valid whole-object alias modes, invalid encoding/multifault precedence and the concrete T126 >340-bit certificate regression. No invalid C++ reference/UB tests, mirrored limb oracle or fixture-for-executable substitute.

Uses accepted T147 driver/tool/copy-cache model and T151 approved factory approach AS DATA, never invokes old drivers. Proposed300s whole/60s operation bounds, inspected exact tools/argv/dependencies/copied cache, minimal named test exports/no app/public-header dependency, preserved failures and review-before-freeze are explicit. Compiler frame evidence remains a later actual obligation; no diagnostics/tool availability is fabricated.

Packet concludes READY FOR MAIN CONTRACT ADOPTION because helper semantics are specified, while remaining PROPOSAL_ONLY. No owner movement preference selected, contact/response policy reopened or full World/P1 proof claimed. MAIN alone adopts a private contract and releases source/harness ownership/commands.

## Exact source-reference identities

SHA256 captured by direct read-only shasum, no project imports or driver execution:

| Reference | SHA256 |
| --- | --- |
| tickets/T152.md | 09ed02a63a4dbdae93dd0780e354bc78ab924eb0634b13fe7a915e4296017ad2 |
| notes/decisions/D186-private-collision-arithmetic-packet.md | 734f41c693c7fe3d7e8c1b320c9b08b04b483349cf70ed091b3af63e22c956ab |
| notes/decisions/D150-quantized-contact-progress-direction.md | 7488af4515839a3290af395806c3d8e907c719a538761ce2085363a138d16467 |
| notes/proposals/T002-P1-pair-query-addendum.md | 467fe123a20d36ffaf18382d9d7e9818798fcd5eba592844b94acba9d3231b90 |
| notes/proposals/T002-P1-common-timeline-addendum.md | bb10cc027171ed4b7a34b0d25e6035beb7ce54ae56dfe2749aa10f1354dce58f |
| notes/reviews/T126-AI-Director-resource-proof-review.md | 32970ac803fdecab342c64421631b268ee77a60be3c57a50cade3e6c27c6ff9c |
| notes/proposals/T132-P1-quantized-contact-progress.md | a5fb7a4ae119868647edb014f9c8342b42580e78071206a8768228220ec77b9f |
| MVP/P1_RULES.md | 63a2a843f69e2495a97383ac17d559793f43611867c36a9bb84159f2b3f86fd3 |
| MVP/SHARED_NUMERIC_FOUNDATION.md | b5cb841a224d3f354e6f2af0f22ba39951c4cb9acf5f1f1bf26440f18b2e483e |
| MVP/SHARED_HASH_FOUNDATION.md | 62fbe105ac3d1d6fbd98777e98a5b859ce3414974c8ac6b7f66171fa95a8a4a4 |
| MVP/SHARED_RULES_FOUNDATION.md | a1a69fadef059991a7065d89c75ccae32165a7e4e716b4d3a1ec23f2e6b5fac8 |
| source/outbreak/fixed.h | f2b7c303eab8ad4e4ad33593f55759196a8f711bbd791e8ad50715824aa792c3 |
| source/outbreak/p1_types.h | 8f9222262be5cfbc5e16f10b040b6bef95385af0db58669cfc3d0cfcc6f8b621 |
| tests/outbreak/hash/T147/verify.py | 7596e7d0b4f29ad810364606c05df910fd23ab9b8ca95f003b83fcb6492cee7a |

## Actual work and limits

Only direct named document/source reads/searches, SHA/word-count metadata and authoring two new notes. Arithmetic/bounds are paper derivations, NOT executable verification. No source changes, project imports/scripts/test/compile/link/native/Wasm/Node/old driver execution, process/system/SDK/Git/network calls or worker dispatch. No corpus, runtime, benchmark, query or stack evidence was generated. No new question is needed to choose helper semantics; compiled stack/work/consumer adequacy are explicit later proof obligations, not accepted exceptions.

T149/actual RSS/QA holds remain unchanged. Packet and handoff submitted; Engine returns to standby for MAIN disposition and any separately released source lease.
