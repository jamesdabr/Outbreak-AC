# T142 — Replay integration and scope-origin wording

- Author / worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T1421.0 / D168, notes-only review.
- Phase/contracts: P1_RULES0.2; H/T frozen proposals; final typed adoption/P0 pending.
- Exact affected clauses: MAIN closure draft1:7 (Q1), :23 (Q3); SHA25651e6a4ca60c4676154068d0bc7d94c3718d48acf7bad3f92f22c2af8e574fc42.
- Status: OPEN; MAIN resolution recorded separately.

## Question

Can MAIN clarify Q1's once-per-tick wording as once per traversal, allowing required authoritative reconciliation recomputation, and explicitly alias Q3's origin to H's CameraSolution.camera? Exact minimal proposed text and evidence are F1/F2 in `notes/reviews/T142-AI-Director-closure-review-1.md`.

## Evidence and impact

H section7 replays retained future ticks from authoritative state; literal prohibition on replaying a previously predicted tick would omit required integration. H has eye/ideal/camera/muzzle but no origin field; different choices alter scope around cover. These are narrow draft wording questions, not findings that the intended candidate algorithms fail.

## Options for owner and lead

1. Approve the minimal clarifications/corrected successor draft, retaining H's existing replay and solved-camera sources.
2. Cite an already governing exact interpretation resolving these words, or return different explicit text for review under the same approved rules.

Recommendation: record F1/F2 disposition with the successor's identity. Ground braking selector A/B remains independently pending owner preference; this question selects neither and adds no fields/values/gates.

## Work paused

No implementation is released. Only candidate clause adoption awaits MAIN; scoped review/handoff can complete independently. No existing file or held work is changed.
