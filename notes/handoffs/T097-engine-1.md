# T097 production-discovery correction handoff

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket/revision: T0975.23 RELEASED; D097/D099, CANDIDATE_BUILD_FOUNDATION0.2, D088/D091, GOV/BROWSER_FOUNDATION/P0 subset0.5. Preparation correction only, no self-acceptance.
- Base/overlay: existing13f0d8eea4822dee5c976661218d022be74342e3 plus preserved accepted/mixed overlay. No clean-source/build claim.
- Changed: ONLY repository_inputs() body in web/build/candidate_recipe.py; NEW web/build/tests/candidate/T097/{candidate_recipe.T088.py,run_t097.py,attempt-1/**}; this NEW handoff.
- No commits/reset/dispatch/source-manifest/accepted pins, source/game/SDK/cache/native/old wrapper/config/helper/schema/test/receipt edits. T088 remains historical, its old source archived exactly before correction.

## Acceptance evidence

| Criterion | Result / evidence |
| --- | --- |
| Exact authorized source diff | PASS: archive of accepted T088 code SHA256e6d464a4aff7897b001fb360251857c1bb00abeaf2f1b60c52ec0c2ee8e65c15; AST method boundaries plus byte-identical prefix/suffix prove every other function/global unchanged. discovery-only.diff captures the complete narrow change. |
| Genuine required .data / root bridge | PASS actual read-only discovery: source/src/ge25519_base.data explicitly added; actual crypto_tools.h include confirmed; production enet_ws_bridge.h retained. Source/src+ENet header selection and61 units unchanged. No undeclared-header exception. |
| Exclude unconsumed history | PASS actual read-only old-method/current-method comparison on the SAME current tree: only added path is ge25519_base.data; only removed paths are web/transport/results/native-enet-T063/sound-pin-audit/{current,historical}.h. Transport headers now root-only, no tests/results recursion. |
| Focused source-discovery regression | PASS6 tests: .data/root bridge/genuine source headers, changing/new/malformed unconsumed nested header irrelevant, source/bridge/.data symlink rejection, source-included but undeclared header refused by unchanged dependency gate. Unrelated IO doubled in labeled fixtures; .d fixture is simulated, no compiler claim. |
| Accepted immutable suite | PASS38 original tests imported from unchanged test_candidate.py into NEW T097-owned legacy-38 RUN. Same global audit denies subprocess/fork/exec/socket effects; attempted_real_effects=[]. Old once-only writer/main not invoked and original outputs untouched. |
| Full test result | PASS44 tests,0 failures/errors. attempt-1/tests.log/result.json and source snapshots retained. No actual subprocess/compiler/tool/version probe/build/runtime. |
| Read-only corrected observation | PASS actual plan:61 units/6 ports/5 aliases/79-file388791-byte pack,tool_errors=[]. Source manifest remains PENDING_MAIN_SOURCE_MANIFEST, execution readiness false; no accepted pins or real attempt/publication reserved. actual-plan.json written only under T097 new allowance. |
| Preserve originals | PASS: full original protection unchanged after excluding only new owned T097 attempt; production-discovery byte identities unchanged across tests. T08835 direct frozen files remain exact; authorized changed live source maps to its exact archived36th member. Old freeze/receipts/snapshots not rewritten or padded with witnesses. |
| Scope/format | PASS: all source diff outside repository_inputs byte-identical; git diff --check exit0. No schema/flags/commands/actual .d gates, accepted APIs, source/native/artifacts or T083 changes. |
| Real build/clean compiler closure/runtime/P0 | NOT RUN; requires later MAIN source review/manifest/execution release. Static includes/read-only observation/fake objects are not compiler dependency or build proof. |

Executed local inspected entrypoint from /Users/jd1/code/apps/outbreak:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/build/tests/candidate/T097/run_t097.py
```

Exit0,44 tests,0 failures/errors/attempted real effects. Existing Python3.11.9;
no environment/SDK/tool modification. Archive imported only as an inspected
immutable declaration module; its discovery method is compared on the current
tree, not by rerunning old CLI/build/evidence writers. Production input path
count is476; proposed source entries add alias provenance separately. Pure
fixture vs actual read-only results are labeled independently.

## Implementation status

Corrected source SHA256:
68ebfd201c2ee38afd370268a40f64b8b29ea91a7f027722091faf37b4e43dcb.
Immutable38-test module remains
43978d0646496919f4c46a0e4ca756d88e6e40c43fe56c93f8a23cfde042a70a.
New terminal freeze under tests/candidate/T097/attempt-1/freeze.json includes
corrected/archived source, new harness/evidence and this handoff; excludes itself.

No historical source witness becomes a compile input. All actual transitive
dependencies must still be pinned and compared before/after a future compiler
run; unknown .data/header types are not generally auto-trusted. Explicitly
shared MAIN source-package members retain unchanged0.2 validation/stability.

## Integration and follow-through

No new semantic conflict/question. MAIN must review this corrected identity and
new prep receipt before source revision/manifest/real build release; T096 list
remains a path proposal, not final source authority. No old T088 source or
receipt is retroactively rehashed. Candidate source/test/evidence are frozen on
submission; no more implementation absent another exclusive lease.

Priority T097 reporting is complete; resume already-released T0021.1 NOTES ONLY.
Its incomplete P1 proposal grants no source/API/gameplay/build implementation.
