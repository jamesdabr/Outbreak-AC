# T150 pre-run advisory identity mismatch

- Author: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket/revision: T1501.0, RELEASED D183.
- Contract: ANGLE_TABLE_FOUNDATION0.1, opening adopted Package A reference and certified fixed-input requirements.
- Status: OPEN; MAIN resolution must be recorded separately.

## Question

The approved contract pins notes/proposals/MAIN-next-rules-prerequisite-advisory-1.md to SHA256 a6ba6af1f2faf065b7fac6cc269223b20cbbdfdd107b0a09d5a194c9597b3fc8. The current ordinary file is15688bytes and hashes to4c0cb7a77c38b1b24fdb5cd67132f5f8539a336113932bcc91dad32281f74790. Which exact advisory bytes are the approved input for T150? Please restore the pinned version or record the newly intended binding in authoritative contract/release documents before the once-only attempt.

## Evidence and impact

Read-only stdlib hash inspection found the mismatch twice during preparation; no T150 module/entrypoint was imported or invoked to discover it. The main driver's existing expected hash remains the contracted a6ba...fc8 value; no current-hash fallback or tolerance was introduced. tests/outbreak/angles/T150/attempt-1 is still absent. No attempt or certificate output exists and no generation failure/one-use attempt was consumed.

Independent authorized preparation is complete enough for source review: new generate.py/verify.py/test_angles.py/SCHEMA.md/README.md/LICENSE.txt only. AST syntax checks passed without executing project code. Actual generation, rational certificate verification, reproduction, negatives and guarded import execution are NOT RUN; no table or digest claim. New source remains unfrozen and actual artifact review-ready delivery is pending.

The D183 filename typo identified by MAIN was already corrected to notes/decisions/D183-certified-angle-artifact-release.md before any attempt. Fixed interpreter alias python3→python3.11 was inspected and recorded explicitly in source; no toolchain change. Existing accepted T147 numeric/core/hash source hashes and T147/T148 freeze digests matched their known accepted identities in read-only preflight.

## Options for MAIN

1. Restore the advisory file to the exact contracted a6ba...fc8 bytes, preserving any newer revision separately under MAIN ownership, then explicitly confirm the unchanged assignment may proceed.
2. Review the current4c0c...790 advisory and record an authoritative corrected binding/revision, if it is the intended input. Then World can update only the local source gate to that approved identity and perform the still-unconsumed attempt.

No option is adopted by this note; World does not amend the contract or advisory.

## Work paused

Only actual once-only T150 generation and dependent certification/reproduction/test/publication are paused on this input identity. No attempt1 reservation, production change, process/network/compiler/browser/server call, occupied retry or freeze. All accepted packages/tools and source evidence remain unchanged; QA remains paused.
