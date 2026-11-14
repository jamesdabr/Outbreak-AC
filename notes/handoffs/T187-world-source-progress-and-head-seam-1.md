# T187 source progress and exact-head catalog question

- Worker: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket / revision: T1871.0 / D301, source construction only
- Phase / contracts: G2_FOUNDATION0.1, WORLD_QUERY_FOUNDATION1.6/D300, QUERY_PUBLICATION0.2/D203/D259, QUERY_CALLER_BRIDGE0.2/D284, adopted T173 plan/review
- Base: ticket's bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved overlay; no Git command and no clean-checkout claim
- Status: **INCOMPLETE T187 SOURCE PACKAGE; NOT COMPILED / NOT EXECUTED / NOT ACCEPTED.** This is a progress/question handoff, not submission of the required complete production+ten-file package.
- Existing file changed: source/outbreak/p1_geometry.cpp only
- New source files: the five tests/outbreak/geometry/G2/regression-G1 files below
- New own notes: this handoff, two standard-diff proposal notes, and the precise question below
- No commit/branch, authority/header/dependency/asset/old-evidence edit or effect lease consumed.

## Required resolution

Read `notes/questions/T187-head-equality-lattice-seam-1.md` (4510 bytes, SHA256554840e10b8bcc8fe3d5a8316af8ba5d5e780d44d8b717083e50ab52d954ea75). The literal T173 head-example sentence can be read as requiring a physical exact head equality at h3738. That is impossible for the frozen integer public ray/target records: its contact circle requires a sum of rational squares with odd7-adic valuation. The note gives the complete elementary proof and a concrete valid proposed equality at h4080, endpoint(33764,32876,3468), offset(996,108,514), without changing the head rule or any row/cap.

MAIN needs to clarify whether h3738 governs only the nearby rounded3177 examples, allowing a different valid stance for exact equality. No alternative equality seed has been silently substituted. The public exact-head predicate remains implemented, with equality Head. Only the disputed mandatory catalog entry/coverage assertion is substantively blocked by this question; other Q source is not claimed impossible. The Q five-file package has **not been constructed or completed** in this progress delivery. Its independent source work remains outstanding, as well as the disputed entry. No empty/fake Q files or fake corpus were made to claim ten-file completion.

AGENTS.md says: “Do not amend a contract because it seems inefficient, infeasible or inconsistent with existing code. Record a question and stop only the affected work. Continue independent authorized work where possible.” Production and fresh R source construction continued after the question. The catalog interpretation remains pending; there is no source, preparation or acceptance waiver.

## Source identities

| File | Bytes | SHA256 |
| --- | ---: | --- |
| source/outbreak/p1_geometry.cpp |74169|0d999988280531d74ded6bfa27ae35e032233886267ddb1deb5def276cc4bf3b|
| tests/outbreak/geometry/G2/regression-G1/verify.py |241515|56ad4c7674ef6de946c1a2945d454a31c7350d58223296e3e31a7273eafbb5cc|
| tests/outbreak/geometry/G2/regression-G1/wrapper.cpp |39984|a36b3840f6bb8b98958d0f4ec7625d8254e2cb1a8d8371d72e264544955a465d|
| tests/outbreak/geometry/G2/regression-G1/wasm_runner.mjs |3616|010ac5e0e19fd5f96c808d7b3d3ac8c762a798a6bc751c6c28722a59631232cc|
| tests/outbreak/geometry/G2/regression-G1/SCHEMA.md |10895|5181d3740535868e7f19eec424f4f2491f92e09c94a98121e92561c6efcc6e1d|
| tests/outbreak/geometry/G2/regression-G1/README.md |13436|cce6c2a681eb8a2fb3d8d79e79abb67ef4a28d713a34a2c654e10f9ecd302fca|

Exact standard diffs against the accepted immutable archive:

- `notes/proposals/T187-production-source-diff-1.md`:44094 bytes, SHA256aa310735a3dad6ec0e73afb3a69ee702b9d4db2305f009c96103d6af23ce55f6. Ordinary `diff -u` output; status1 means differences, not test failure.
- `notes/proposals/T187-R-source-diff-1.md`:58999 bytes, SHA256a89aefe5bbc39b4e6f8796398c576bd316389192df3529146be9bc47f64438f2. Ordinary `diff -ru` over the five-file archived G1 source directory and the new R directory. The runner is byte-identical, so has no diff hunk.

The production diff is an append after the entire accepted G1 source. Read-only `head -c 31382 source/outbreak/p1_geometry.cpp | shasum -a 256` returned c232100352425092561f6fc9701c77db17f643893510fde780839db21be17d21, equal to the31382-byte archived file. G1 private/public bodies, Work70, owner annotations, static layout and lifetime expressions remain the complete exact prefix. Accepted final freeze still hashes3d3491058f07e37edf240e21d227a6bffaf3d14ad0b9d8c544a670fe938934da.

Read-only SHA256 checks of geometry/store headers and all eleven dependency files matched the accepted literals in the new R verifier: geometry.h8bfa5558…96a90; store.h7a7b185d…0bc3; p1_rules.cpp333b6d07…18da5e; wide715521a8…3e83; all remaining dependency identities also matched. Historical identities were not retargeted to new source.

## Production implementation and maps

All five frozen declarations now have definitions, rather than Clear/Hit stubs:

| Public function / line | Source behavior |
| --- | --- |
| trace_ray1452 | Full view/mask/ignore/actor/domain validation, private point adapter, closed origin tags, exact algebraic head sign, two-pass TraceResult |
| sweep_sphere1465 | Generic positive sphere, world26-feature and true actor capsules, no fabricated owner/ignore |
| sweep_capsule1474 | Generic vertical capsule, original extended-Z box reduction and physical-axis surface reconstruction, exact full-ref ignore |
| headroom1482 | Implicit MoveMask, strict-overlap only, stable World/Actor identity, coherent outer status and complete obstruction, touching Clear |
| sweep_capsule_world_rational1491 | P1 owner/shape/original numerator-domain validation; all-six-integral N8 selection before bank construction, otherwise original-d N16 |

Private map (current source): validation602–665; tags670, walker679, conversion687, counters696, QueryWork703; ordinary algebraic sign777; exact World root order796; Q32 certification830; first/anchored-priority reduction860; feature ranks905–926; affine/coefficient builders927/938; exact box/actor validity947/972; root streaming988/992; initial occupancy1011; full box1044; actor1073; outside halfspaces1098; row fraction/clip1131 and x conversion1153; cell1168, row walker1185, closed ray supercover1222; stream1275; physical bounds/axes1280/1300/1324; serial materialization1336; private owner prototype/definition pairs1405–1443; public adapters1452 onward.

Separate G2 lower/upper actual arrays are32 slots each. q_lower1441 owns lower; q_upper1438 owns upper; q_body1408 borrows both, with synchronous lifetimes and no pointer arithmetic crossing arrays. Exactly these three new private boundaries have Clang noinline prototype/definition pairs; no old annotation or compiler flag changed. Actual compiled fit is NOT established.

Logical64 slots:0..3 retained certificate,4..7 candidate;8..15 affine;16..25 resultant;26..31 ordinary sign;32..35 suspended row endpoint fractions,36..37 x extrema;38..59 scratch;60 original motion norm,61 fixed near RHS,63 traversal zero. Witnesses run serially in8..39 (39 zero), preserving norm60/RHS61 for pass2. No third certificate or simultaneous G1 bank. All operations use unchanged accepted query_wide Int8/16, no float/128/new bigint. Resultant opposite-sign evaluation constructs R rather than forbidden X²/Y²Delta; derivative selection uses the separately bounded ordinary graph.

Nonwide offsets/assertions: staged TraceResult0..159; candidate160..239; walker240..367; conversion368..463; two tags464..527; pose indices528..535; counters536..599; Fault600..607; PoseFeasibility608..639; control/slack640..767. Declared totals64*36+768=3072 or64*68+768=5120. These source assertions have NOT been compiled. Every actual owner frame/local, control/body, scalar/helper/callee chain still needs emitted proof.

Source walkers enumerate each closed ray supercover event (initial up to4 neighbours, later at most3 sorted by cellIndex), gridline/XY-stationary/endpoints, or ascending row-strip x intervals with exact positive-denominator fractions. ONE1024 counter precedes every cell access across both passes; space cells and repeated pass2 visits count. Initial tests are within the same streamed primitive visits. Solid/floor/ceiling primitives and six true outside halfspaces use frozen IDs. Full box26 features and actor three regimes remain; P1 boxes>0 reject Range.

Pass1 retains the physically earliest algebraic candidate and materializes its complete first. Pass2 retains spent counters and immutable first.q, filters with original anchored11 metric, and selects explicit World/Box/Actor priority. Each own witness/zone stays with its own identity/root. Full output publishes only after all traversal/materialization succeeds. Clear is canonical; every Invalid/IterationLimit path preserves complete non-Fault output. Source review is not proof that all paths execute correctly.

Physical witness uses original closest axes (facing endpoints or overlapping-Z midpoint), quantized own normal, then the moving body's facing SURFACE with final signed ties-away rounding, denominator E*2^31<=2^95. Rays use their prescribed own diagnostic base point. On integer vertical Down<=819, +Z floor contact's own surface point equals its foot at reported q; precontact error<819/Q<1/2 rounds to the exact integer floor, including negative/degenerate/lower-outer/endpoint cases. This is a source/paper construction claim awaiting independent Q evidence.

## R source and finite proof plan

R is a new five-file source copy/rederivation of the accepted source archive, not an import or execution of an occupied driver. Original16384 G1 data construction/oracles/serialization are retained. Future preparation must regenerate and match all five P5 artifacts by literal hash: setup915564, corpus2709120, expected2686976, catalog12928990, coverage8650. No data was generated/copied as an expectation.

The new R wrapper's dormant typed op11..15 path retains every new public function in the linked graph; actual R parent/native/runner stream gates still admit only op0..10, so no extra actual query/case is added. New backing uses256 initialized live actor/box records for malformed counts. Fieldwise saved inputs/volatile observations cover view, actor/box fields, queried records, deltas and rational motion. All G2 outputs/Fault have immediate seven-byte before/after arrays with a leading alignment byte, distinct complete hit/head poisons, explicit full serialization, guard/input failure refusal. This dormant source is not G2 geometry evidence.

R source maps: `require_source_clearance`67; `g2_source_ledger`1131; `prepare`1293; `source_owner_declarations`2337; closed source/frame inventory2410; source-lifetime map2536; `actual`3081; sixteen new G2 source-role controls3391.

The source ledger binds exact current source and existing G1 prefix; actual owner-source declarations, template widths, normal/diagnostic .su/assembly, dependency closure and linked Wasm body/index/call/local bindings are freshly required. It now inventories all15 public computational roots plus run, all G2 private functions/QueryWork methods and typed wrapper helpers. Unknown normal callees remain refusals, never zero cost; D196 canary-only exclusion is unchanged. Exact q_upper→same-width q_body direct joins are checked; both complete actual owner frames/locals charge to mode, body/scalar control to geometry, helper sum separately and wide as its subset. Limits remain mode3072/5120, geometry1024, accepted helpers2048, full query8192, full portable caller65536. Wasm linear ABI+locals is not VM/OS/RSS measurement.

Proposed future controls: retain original128 meaningful fakes (40 supervisor,16 durable terminal,6 arena guards,14 analyzers,24 focused,12 D260,16 prior source-role) plus exactly16 G2 source/frame models=144 per independent job. New names in g2_source_role_regressions: native-two32-all-costs; Wasm body locals; owner5121; body1025; helper2049; complete8193; nested bank; mixed width; orphan body; duplicate upper; body mischarged as owner; unknown normal callee; wrong source line; wrong definition symbol; wrong whole-source pin; run65537. These are proposed source controls, NOT RUN, not physical geometry evidence, not an enlarged real-case allowance.

Finite source work retains1024 cells,2048 boxes,53308 features,41008 discriminants,94316 roots,10499072 root digits,3018112 bins,848844 other signs,94314 winner comparisons,94316 ties,2048 initial boxes,16 initial actors and4 final roots. The ledger separately bounds coefficient/discriminant/sign/resultant/tie/witness/row/import/copy/preamble operations and substitutes accepted nested helper scalar prices at N8/16, including validation/copy/compare/subtract loops. Row scalar tests<=512, ray events<=1026, pending-sort<=6 comparisons/event, actor validation8/28 duplicate comparisons. Widths preserve World resultant427/derivative429, G1 pair505/405 and T126. These are source/paper envelopes, not measured execution or affordability.

## Acceptance evidence and remaining steps

- PASS READ-ONLY: accepted G1 complete byte prefix; current unchanged header/dependency SHA identities; accepted final-freeze SHA; standard append/R diffs; ticket/foundation reread still1.0/0.1.
- IMPLEMENTED SOURCE / UNVERIFIED: all five production definitions and separate G2 storage/root/feature/traversal/publication graph; fresh five-file R source, current graph/proof/control plan.
- INCOMPLETE: Q five-file source, all16384 literal Q rows/independent exact World oracle/root certificates/canonical schemas/catalog assertions/controller adaptations; clarification of the exact-head entry. No complete ten-file T187 submission or acceptance is asserted.
- NOT RUN: source parser/import/compile/syntaxbuild, controller fakes, fixture/corpus/oracle/prepare, native/Wasm/FFI/SDK copy/tool probe/runtime/browser/network/Git. No preparation-1, attempt-1 or final root was created for either job.
- Simulated behavior consists only of future fake definitions; no simulation was executed and no evidence file was produced.

After MAIN's catalog interpretation, complete and review Q source and re-review all source/frame/work maps. Any resulting code change requires fresh source hashes/diffs and a new handoff; the current source/diff notes are this progress snapshot, not effect clearance. Only after a COMPLETE source review may MAIN separately freeze/release guarded R and Q preparations, each16384 rows/original300s/60s/8MiB, then separately actual28-child jobs after their concrete frozen source/data/process/tool/SDK/dependency/terminal plans pass review. Neither current helper models nor eventual R/Q output substitutes for G3/G4/caller transaction/browser/performance/human/native/Player/QA/T149/full-MVP gates.

No old G1 source/evidence or authority is to be rebased. No automatic preparation, actual, correction/retry or integration follows this progress handoff.
