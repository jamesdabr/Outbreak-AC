# T110 Engine handoff — common timeline and feasible rounding proposal

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T1101.0 RELEASED notes-only; delivery for MAIN review, no status/self acceptance
- Phase / contract revisions: GOVERNANCE/BROWSER_FOUNDATION/P0 0.5; P1_RULES0.2/D112 unchanged; D115 selected trajectory direction; frozen T002/T108 proposals are inputs, not adopted source interfaces
- Base and pre-existing edits: frozen note hashes below; no source revision built/changed, checkout or clean-source claim. Shared workspace/source changes preserved.
- Changed files: NEW notes/proposals/T002-P1-common-timeline-addendum.md; this own NEW handoff; own NEW notes/handoffs/T110-engine-freeze-1.md terminal receipt. No old T002/T108 note/handoff/question edit.
- Commit/patch: none; no Git/source/MVP/ticket/decision/artifact edit, project code execution or worker dispatch.

## Acceptance evidence

PASS means proposed/static coverage only. No native/Wasm/compiler/test/browser/
resource/performance or implemented-correctness result is claimed.

| T110 item | Result and evidence |
| --- | --- |
| One bounded Engine-private actual common timeline, not chords/sequential actor dt | PASS proposal: addendum sections1/3/4, master spans and exact rational sampling, original20ms integration/timers once, complete coverage/remaining tails, phase-aware auxiliary sampling. |
| Record capacities/time composition/no unrelated rounding loss | PASS proposal: private Span/Aux/StepFork/ActorPlan/EventWindow/PairVisit/CandidateEvent/SafeStart;65 spans/actor,2 auxiliaries,514 calendar times,129 pair common intervals; global floor/upper certificate composition, immutable unaffected span endpoints/denominators. Actual size/bounds/performance proofs NOT RUN. |
| Complete World-owned exchange, without Engine geometry duplication | PASS proposal: section2, RationalCapsuleMotion, PoseRelation/PoseFeasibility and four pure functions (rational pair/world sweep, pose classifier, exact distance tie). Complete fields/domain/ownership/status/lifetime/error/unchanged-output contracts; old integer T108 delegates unchanged where applicable. |
| Ordinary overlap versus malformed/query failure | PASS proposal: classifier successful Clear/Touching/Overlapping; malformed/overflow/limit failure is Fault. Sweep Invalid never becomes a false overlap or Clear. World end/trial outside-solid halo distinct from malformed domain. |
| Discrete pre-movement stance; zero-time step groups; full slides/tails | PASS proposal: sections3–5, joint headroom/crouch fallback and fixed per-tick shape; Down-before-Up group sweeps with both moving legs; remaining horizontal-time forward; real world-only landing; cached original blocker, no stale wall projection before a successful step, branch rejection without budget reset. |
| Conservative rounding/caller bilateral ownership and valid-start argument | PASS proposal: section6, <=34 shared dyadic prefix trials including T=2^32 and r0; actual changed prefix swept again, no chord across bends, paired clamp/projection/remainder clearing, no radius inflation/push/epsilon/extra dt. Third-actor debt remains explicit until full verification; local valid-start fallback does not claim all crowds solve within4passes. |
| Global earliest scheduling / review feedback | PASS successor proposal: section7 scans all unresponded pair candidates, chooses earliest conservative global time/tie/group key, revalidates after plan change; once/pair/pass and4passes retained, auxiliary groups and earlier newly exposed events explicit. Obsolete stable-pair-outer-loop finding is not carried forward. |
| Replan/pass/step limits and transaction fault | PASS proposal: original4world/4pair/one-step bounds; at most112 pair responses/32 world responses,8 monotone step disables; no free resolving verification pass. Any unresolved debt/fault/capacity failure discards candidate and all canonical outputs. |
| Worked examples and real validation plan | PASS specified/manual: timing-plan step versus moving peer (remaining300 from full400 at Q/4), two-leg slide and unaffected301 travel; independent exact oracle/metamorphic/adversarial/fault/native+Wasm/prediction checks, all NOT RUN. Fixture is not an actual approved-map/gameplay pass. |
| Public/canonical/prediction/source effects and scope preservation | PASS proposal: section9, same move_one/MoveResult, private joint kernel helper pipeline, provisional prediction with unavailable remote receipt/path uncertainty; no wire/ID/accepted fixed/envelope/map/numeric/terminal/full-MVP scope change or source lease. |

## Actual static verification

Read full T110/D115/T108 question/pair addendum/base movement+query records and
P1_RULES0.2; reread ticket/D115/rules before submission. Used only read-only
cat/sed/rg/shasum and `git diff --no-index --check /dev/null <new-note>` plus
new allowed Markdown patches. Addendum check returned empty whitespace diagnostics,
exit1 for a new-file diff; handoff/receipt get the same check. No executable test,
script/import/entrypoint, compiler/Node/native/browser/network/service/install or
Git mutation. No OS/toolchain/hardware claim is needed for a notes-only result.

The new rational core's16-limb/512-bit bound and<=8192-byte call stack are explicit
additional implementation obligations, not claimed existing8-limb support or a
measured fit. Private scratch/work/time targets must pass actual future production
measurements against unchanged PLATFORM_DECISION thresholds. The proposed dyadic
choice is conservative, not nearest-feasible or a monotonic feasibility claim.

## Frozen input/output identity

Unchanged input SHA256 values reconfirmed read-only:

| Path | SHA256 |
| --- | --- |
| notes/proposals/T002-P1-headers.md | 79fa17d45f11d480a66a57435a258811722c075e1dddc1926428958f2cb01709 |
| notes/proposals/T002-P1-wire.md | b625e2e9d8161c3fff5c2afc0f0976fc1f6d03e62d0fdb4a2ba52c15c4aeac16 |
| notes/proposals/T002-P1-seams.md | b50cd481a3cf4d4acf5822fa17f87e254f12dfaf441c9b718ccbf2b87ceb1855 |
| notes/proposals/T002-P1-pair-query-addendum.md | 467fe123a20d36ffaf18382d9d7e9818798fcd5eba592844b94acba9d3231b90 |
| notes/handoffs/T108-engine-1.md | c2f65ebc80d90f85f035bcfbf112597bd6067f636def3c80e83ef1fa93c94250 |
| notes/handoffs/T108-engine-freeze-1.md | 891c1da32401e8eddbf0f2af7a026a4bc504afe5281e8007313704c78bf00b89 |

New addendum SHA256bb10cc027171ed4b7a34b0d25e6035beb7ce54ae56dfe2749aa10f1354dce58f.
T110-engine-freeze-1.md pins the addendum plus this handoff after final read-only
hashes, avoiding a self-referential handoff hash. MAIN's interim draft hashes are
superseded by this final submitted identity, not retroactively accepted.

## Implementation status and integration

Implemented: new Markdown only. Simulated/test doubles: none. Incomplete:
all proposed source/header/core/caller/tests and actual native/Wasm/browser/
resource/performance evidence. This note is not an adopted collision policy or
gameplay release. MAIN must review/adopt exact helper formats, arithmetic and
backoff/scheduling choices before full P0 plus individually released source work.

D115 provides enough direction to submit this concrete proposal without another
worker policy question. Frozen T108 question remains an unchanged historical
record; only MAIN can close/adopt the complete caller convention. No new
dependency, asset, source unit or worker instruction is issued here.

Reproduce static review by reading addendum sections1–9 against D115/T110, checking
global-earliest pseudocode, phase samples, integer/rational delegation, feasibility
and34-trial endpoint bound, then read-only shasum/whitespace commands. Future tests
listed there require separate explicit execution release and real production code.
