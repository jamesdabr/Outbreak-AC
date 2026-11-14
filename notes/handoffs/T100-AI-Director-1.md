# T100 source provenance audit handoff

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T1001.0; RELEASED at final read. Submitted for MAIN review; no authoritative status or acceptance changed.
- Governing subset: D100 assignment, D099/T096 path audit, T070/D064 frozen accepted build input, later D087/T089 and D090/T091 exact source acceptance; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5 audit only. Required governance and ticket re-read before submission.
- Base/pre-existing overlay: HEAD freshly read as13f0d8eea4822dee5c976661218d022be74342e3;32 modified tracked source files,109 unchanged tracked scoped files,13 untracked accepted/prototype/prerequisite files. Existing source, active tooling, SDK/libraries/assets/pins/history and T098 freeze/evidence preserved.
- Changed: only NEW notes/reviews/T100-source-provenance.json, NEW notes/reviews/T100-source-provenance.md and this own handoff. No commit, branch, dispatch, source/package staging or Git mutation.

## Acceptance evidence

| Ticket requirement | Mechanical result / evidence |
| --- | --- |
| Fixed-root current ordinary inventory | PASS154 files: source/src97, source/enet48, source/outbreak6, direct web/transport .h/.c/.js3. Exact byte/size/mode/path/Git identity per row; zero scoped links/special files or linked ancestors. No transport results/history/vendor recursion. |
| Accepted T070 input provenance | PASS actual network-out/build-metadata.json SHA2565447bdcc68e3f732ba37bdaf2c03b8ec0f2258e45d4dc6f336acfa39b1eef037 matches D064 accepted artifact record. Of116 relevant inputs,114 exact current, two exact later accepted changes, zero missing/unexplained. Historical PASS strings and stored command arrays were not executed or treated as current proof. |
| Exact later main/MD3 changes | PASS main5f51c53b5a6f2be1180252c7aee972ab754bf0abc91d8a3d0f276153a38834f1 equals D090/T091; MD3f60cdc019579cba4876ff741438934c56b6d626ac55c36c28e8b8ab8abe644be equals D087/T089. Both result before-fields equal T070 originals; actual result digests match frozen result entries. Decisions/results/freezes individually hashed in JSON. No blanket difference waiver. |
| Every Git-modified tracked source | PASS all32 separately listed/full-hashed in JSON and grouped exhaustively in Markdown.30 equal T070; two equal exact later acceptance. Git status agrees; cached diff empty, index Git blob/mode identities independently computed from file bytes. |
| Prototype versus compatibility provenance | PASS ENGINE_AUDIT/BROWSER_PORT_AUDIT/D003 exact baseline used. Six original tracked prototype files plus untracked outbreakstate.h unchanged; clientgame.cpp is mixed prototype/accepted compatibility and matches T070 whole-file hash. Other25 modified tracked files are later prerequisite/compatibility overlay, including exact main/MD3 follow-ons. No gameplay/authority inference. |
| Nonbrowser inputs / portable / native provenance | PASS six portable files match D076/T078 or D092/T093 data identities; native Makefile.am matches accepted native inventory. ge25519_base.data matches actual native dependency despite old broad inventories omitting it.30 remaining package/build/doc/license files unchanged against Git identity; no historical build SHA256 claimed where absent. unix.c already in browser input inventory but absent browser compile list; genuine native compile unit. |
| Relevant native source comparison | PASS comparison, historical mismatches retained. All112 broad native source-input members present; nine older whole-file hashes differ, each explained by T070/later acceptance. Actual45-project-dependency native union:44 equal, only sound.h differs; current equals T070/D047. D052 remains historical scoped equivalence, not a raw-hash waiver for future build. |
| Modes / required framework link provenance | PASS136 files raw0644,18 raw0755; directory modes separately recorded. Seven named original framework links checked individually: exact raw text/mode0755/Git120000 blob identity and confined resolution. No recursive framework/SDK/media/cache hashing. All other framework bytes remain outside this audit. |
| Bounded read-only reporting / final verification | PASS source JSON DATA and Python stdlib only; no project imports/tests/compiler/Node/signing/probe/native/browser/network/service execution. Final second check verifies exact154-member scope, all byte/size/mode/ancestor identities,52 reference digests and seven named links. Only two new reports/own handoff written. |
| Clean source revision/checkout/build/runtime/full P0 | NOT RUN / not authorized. No source content accepted by this worker, manifest/pins manufactured, runtime capability/config/entropy read, artifact publication or source edit. Final active authoring freeze remains a separate MAIN prerequisite. |

## Findings and report identities

No missing or unexplained current production inputs were found within the exact T100 scope. This is a mechanical provenance result, not approval of all package files, transient tool hashes or game behavior.

- notes/reviews/T100-source-provenance.json:176495 bytes, SHA256 ae1f791fd6287b2c1c5ac93e55add4ef59e18412097bb439785dfd25f10c8f85.
- notes/reviews/T100-source-provenance.md:12027 bytes, SHA256 b4720091f477c30a07eca07155d790aab156aa3605380e5ec50c5c69c9e1a5b0.

The JSON records all current identities, accepted/current comparison rows, exact reference hashes and limitations. Markdown explains the evidence chain, complete modified-source groups, nonbrowser/portable distinctions, historical native discrepancy and remaining MAIN gates. No source bytes are copied into the reports. Reports are frozen on submission; follow-up requires a new owned note/release rather than rewriting historical evidence.

## Reproduction and implementation status

Read-only Git inspections used: git status --short --untracked-files=no; git diff --stat/--numstat; git diff --cached --name-only; git ls-files --stage for the fixed roots and seven explicit framework links; git rev-parse HEAD. No command from any project module or JSON command array ran.

Own Python standard-library inventory used os.walk(followlinks=False) only under source/src, source/enet, source/outbreak and direct-child extension filtering under web/transport. It lstat-checks ordinary files/ancestors, hashes actual bytes, compares fixed evidence JSON maps, computes Git blob identities and reads only the seven named framework link texts/resolutions. It rechecks all current source records before JSON creation; final verification separately recomputed exact membership, every recorded source identity, all52 reference digests and seven links after both reports existed. Markdown supplies the comparison procedure. No persistent audit code or new test/build artifact was authored.

Delivered actual read/hash/data reconciliation only; no simulation or test double. OS/compiler/hardware performance is not measured or claimed. Historical native/browser/portable execution evidence remains historical and separately scoped.

## Integration and questions

No unresolved question for this audit. Retain ge25519_base.data, native build metadata, six portable sources and declared original framework links in MAIN's final source/prerequisite reconciliation. Do not reintroduce the two unconsumed historical transport headers recorded by old T070 inventory. No dependency/interface/asset changed.

MAIN owns final source/portable/package content review, final candidate/package/measurement source freeze, reviewed Git revision/fresh checkout, common source manifest and exact declared link/tool/SDK inputs, complete actual compiler-discovered closure and separate build/runtime execution releases. This handoff accepts none of those future gates and leaves frozen T098 unchanged.
