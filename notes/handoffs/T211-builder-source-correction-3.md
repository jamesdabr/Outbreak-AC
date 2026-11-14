# T2111.2 D364 callback-root source correction — review ready

- Worker: MAIN delegate `/root/review_native_candidate`.
- Ticket: T211 revision1.2, RELEASED source only at final readback.
- Governing: D364/D361/D352, BLACKWOOD_BUILD_PREPARATION0.6,
  DEFAULT_DEV_BUILD_PREPARATION0.7, closure0.3. No execution permission.
- Base/pre-existing work: T2111.1 submitted bytes and independent returned
  review2 SHA256 bbeb0fb49180551b45483733098ec12609054daf870f589d70a74b53a2166c38.
  Original accepted T177/T178 and every earlier T211 note/plan/diff/handoff
  remain immutable; no Git operation/base-state cleanup or unrelated edit.
- Changed files: both modules' test_recipe.py, SCHEMA.md and README.md; both
  tests/T211 focused source files. Both recipe.py files remain byte-identical;
  they are included in the ten-source before/diff packet with empty deltas.
  Six build/verify/config/shell roles are unchanged and remain in all16 pins.
- New own notes: question T211-dev-foundation-revision-binding-3.md,
  T211-r2-before-* (ten), T211-r2-diff-* (ten), guarded-source-plan-3.md,
  source-correction-pins-3.md and this handoff. No authority/status edits.

## Acceptance evidence

SOURCE TEXT INSPECTION ONLY. No parser/AST/import/helper/test/generator/control/
preparation/job/probe/compiler/tool/version/Node/SDK-copy/FFI/native/browser/
runtime/network/Git/process effect occurred. No result/control/manifest/scaffold
or build output was created. All proposed guarded checks remain NOT RUN.

The sole H1 correction is exactly:

    self.fs.put(self.m.HISTORICAL_ROOT+'/web/late-original',b'late')

Actual argument/module/model flow, inspected directly in the existing source:

1. SimulatedEffects.__init__(m,fs) stores `self.m=m` and `self.fs=fs`.
2. model(m,data) sets `r=m.Recipe(); r.root=m.HISTORICAL_ROOT`, installs that
   same virtual fs and `r.effects=SimulatedEffects(m,fs)` (test_recipe.py154).
3. Recipe.execute constructs `r=dict(...)` at recipe.py541. It passes that
   RESULT DICT to `self.effects.report(r)` at recipe.py564; production report
   indexes the same result shape at recipe.py760.
4. The corrected fixture callback therefore obtains the fixed root from
   `self.m`, not from its result-dict parameter. Its virtual history mutation
   is inside the SAME canonical root used by model and preservation. No new
   selector, retained Recipe parameter, callback API or fallback is introduced.
5. The existing late-report-history case and expected refusal remain; the
   mutation reaches the original final current-history check. No AttributeError
   catch, accepted-refusal broadening, deleted case or extra case is added.

The previous T2111.1 r.repo expression and accompanying plan2/handoff claim
were incorrect because report's argument is a dict. Those records remain
historical returned source, not current evidence or invocation inputs. This
packet corrects that object-flow claim explicitly; no execution is asserted.

All four test startup plan references now read NEW plan3. Schema/readme current
plan references and the dev callback description agree with that correction.
The production recipe deltas are EMPTY: H2 actual safe53 device/inode bounds,
canonical ns strings and same focused boundary discriminators are unchanged.
H3 remains focused result.source_hashes16, full Blackwood source_sha2568, full
dev source_hashes6, with full startup/external pre/post/THROUGH protection16.
No original full-result schema or outcome changed.

## Stable pins, complete deltas and future finite plan

NEW `notes/proposals/T211-guarded-source-plan-3.md`:
SHA256 e5c5f5d266530153754ddfa010d89305a9154522bdd2445175280c0338340d8a.
It contains the complete updated16-source lengths/hashes, unchanged closed job
allocations, full case maps/guards/effect denials and exact future invocation
paths. It supersedes plans1/2 without editing either. Proposed jobs remain
BWdeadline32, BWhistory64, devhistory64, fullBW148groups256leaves and
fullDev228groups247leaves. Each future job separately retains300s/8MiB output/
128MiB fixtures/<=256 leaves and requires a separately pinned MAIN release.

NEW `notes/proposals/T211-source-correction-pins-3.md`:
SHA256 df2b655bb3f04284d7ed45ae1e035c8137ad8723569ad1fe861cdfa9387720ad.
This records all16 final source lengths/hashes, current ticket/foundations/
D364/review2/question identities, all10 pre-edit snapshot hashes and all10
complete final delta hashes. T211-r2-before-* raw source copies were made BEFORE
any source edit and match the submitted T2111.1 bytes. Full source deltas are
T211-r2-diff-{blackwood,dev_regression}-{recipe.py,test_recipe.py,SCHEMA.md,
README.md}.md and T211-r2-diff-{blackwood,dev}-focused.md. Empty recipe diffs
are intentional evidence of unchanged production, not omitted comparison.

Historical plan1 SHA20e4823fb161bcaf18afa7add758beaa82cd2e8077285cbd2041bdad32f9b6d5
and plan2 SHAeb38e8c9f39553488a9dfd50a0796f0b24eabc6c0df35dfd59e4c15b4ce7f399
remain unchanged. No previous diff/handoff has been rewritten.

## Implementation status, integration and questions

Implemented as unparsed source: exact H1 fixture correction, four plan3 startup
references, matching current source documentation and new complete pin/plan
packet. Simulations are definitions only, not run. Syntax/guarded preparation/
actual builds/native ABI/runtime/compiled or full-game acceptance are NOT RUN.
All61units125commands/profiles/assets/notices/aliases/flags, original deadline/
eligible-close/unresolved/receipt/final-marker/strict-reap/EPERM rules and
exact14 nofollow lstat-only five-key original-history restrictions remain.
Original special CONTENT was never read, hashed, followed or mutated. No T216
protected role/graph or other worker source/authority was changed.

Question T211-dev-foundation-revision-binding-3 is RESOLVED by MAIN's explicit
reply and header correction: the dev header now says Revision:0.7, matching
ticket/D364. Worker did not edit it. Final authority readback matches BW0.6/
dev0.7/T2111.2. No remaining source-scope question identified.

Submission grants no follow-on effect. MAIN independently reviews and alone
releases any future guarded invocation. Stop here; all actual browser/native/
admission/gameplay/human holds remain.
