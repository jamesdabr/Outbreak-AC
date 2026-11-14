# T092 native candidate preparation handoff

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket / revision: T092 / 5.19; submitted for MAIN review, no authoritative status changed.
- Phase / contracts: CANDIDATE_NATIVE_FOUNDATION0.2, CANDIDATE_BUILD_FOUNDATION0.2, D087/D088/D090/D091; PLATFORM_DECISION0.1; browser prerequisite governance0.5 only. Re-read ticket/contracts before submission.
- Base: 13f0d8eea4822dee5c976661218d022be74342e3 plus existing accepted source overlay. Existing tracked changes in .gitignore and source/src were preserved; no source, old artifact/helper, SDK, contract, ticket, decision, branch or commit changed by this work.
- Changed files: only NEW web/server/candidate/{stage.py,build.py,verify.py,test_preparation.py,README.md}, preparation-20261108-1/**, preparation-T092-readonly-20261108/plan.json and this own handoff.
- Commit/patch: none authorized or created. Private source/schema/evidence frozen for review; no other adapter should consume these until approved.

## Acceptance evidence

| Criterion | Result | Evidence |
| --- | --- | --- |
| Fixed native recipe, authority/source/SDK/tool/dependency gates, copied-framework staging, bounded capture, terminal records | PASS as implemented preparation; real effects NOT RUN | Five new source/docs files and private schemas in README.md. Fixed 16 units per mode, 32 compile commands, two links; nested-copy signing precedes parent-copy signing. |
| Pure strict positive/negative preparation tests, full simulated builder and independent verifier/receipt | PASS, FIXTURE_ONLY | `python3 -B web/server/candidate/test_preparation.py > web/server/candidate/preparation-20261108-1/fixtures-5.log 2>&1`: 25 tests, exit0, 5.900s. Real subprocess/socket functions forbidden; actual capture logic exercised using fake child/fd/selector/read/signal/clock effects. Temporary objects/logs/signatures/pins are not real build proof. |
| Shared package, opaque historical links, forbidden consumed aliases, changed current headers without historical exceptions | PASS in fixtures | Tests cover common manifest additional portable/doc members, source hashes/modes, SDK/Python/authority failures, protected absent roots/raw links, undeclared included historical header, confined staging links and output alias refusal. |
| Reservation, no reuse/overwrite, failed command/timeout/overflow, object/log/command/runtime/closure corruption | PASS in fixtures | Full pipeline and resealed-invalid record tests; independent live read-only signature/dylib double failures; combined command log bound; failed attempts/receipts retained and not promoted. |
| D090-authorized current source/framework/SDK/tool-file observation | PASS, partial read-only observation; NOT_EXECUTION_READY | `python3 -B web/server/candidate/preparation-20261108-1/read_only_observation.py`: exit0, no errors; 25 source/build file records, 96 framework members, 66 imported Python authoring files. Subsequent pure checks validated framework schema and unchanged observed source bytes. No broad unrelated-worker preservation snapshot made. |
| Plan-only CLI without actual attempt reservation/probes | PASS | `python3 -B web/server/candidate/build.py --plan-only --candidate-id T092-readonly-20261108`: exit0; preparation-only plan.json and plan-command.log. Actual web/server/candidate-attempts absent. |
| Actual compiler identity/dependency discovery, signing, compile/link, native/browser/network/runtime/clean-checkout proof | NOT RUN | Explicitly unreleased by T092. No accepted source/execution/native artifact manifests produced. Full P0/gameplay remains unaccepted. |

`preparation-20261108-1/preparation-result.json` is the consolidated evidence index, SHA256 `387db65c56e8a3076d2ab12d3e60232f82050dcc2481aec59723d2d53d8603ad`. `freeze.json` freezes 16 source/doc/preparation members, SHA256 `1e47a7cbc5edd604277dda42c7f40b88790eedbfca51a27f5fb791cdb2b6e321`; it excludes only itself and this separately submitted handoff.

Intermediate evidence is retained: fixtures-1 FAIL (four fixture path aliases and one fixture signature-payload mistake), fixtures-2 PASS14, fixtures-3 FAIL (fake Child missing returncode), fixtures-4 PASS23, fixtures-5 PASS25. Production canonical-path and malformed-signature checks were preserved. Final verifier review added independent current dylib/RPATH checks and aggregate command/attempt log bounds, covered by final fixtures.

## Implementation status

Implemented: generated fixed recipe, strict duplicate/type/path/current-byte/source-manifest/authority gates, structured preservation, separate authoring closure, atomic fresh reservation, physical confined copy, ordered copied-framework signing, pre/post actual dependency comparison, link input inventory, Mach-O/signature/RPATH checks, bounded owned-group capture, failed terminal evidence and independent read-only verifier/exclusive optional receipt. Full private record fields and authority boundaries are documented in README.md. Independent verification shares only pure recipe/data helpers and bounded capture, not historical native build helpers.

Simulated: all process responses, signature text, compiler objects and linked binaries exercised by tests. Even successful fixture statuses NATIVE_LINKED_NOT_RUN / VERIFIED_BUILD_ONLY_NOT_RUN belong only to temporary FIXTURE_ONLY directories, deleted at test cleanup. `fixture_only` in the prep result describes build evidence; the separately named read-only source/file observations are actual hashes, not simulated files.

Observed on the current macOS arm64 workspace, using existing Python3.11.9 authoring only: HEAD as above; canonical SDKSettings.json reports Version15.5 at the fixed MacOSX15.5.sdk path; five /usr/bin tool launchers are ordinary files and hashed, without invoking them. Production main.cpp SHA256 `5f51c53b5a6f2be1180252c7aee972ab754bf0abc91d8a3d0f276153a38834f1` and md3.h `f60cdc019579cba4876ff741438934c56b6d626ac55c36c28e8b8ab8abe644be` match D090. These two anchors do not prove native compiler consumption. No performance/toolchain execution claim is made.

Incomplete by design: MAIN source-manifest absent; complete actual compiler/linker closure and Apple17 identity probe unperformed; accepted execution pins/out-of-band digest and explicit execution release not supplied. Read-only observation is partial preparation provenance, not an authorization observation or a full historical protection freeze. No flag/alias workaround adopted.

## Integration and questions

No shared gameplay interfaces, external services, dependencies or assets changed. No unresolved contract question is required for this prep submission. MAIN review must approve private schemas/source before any consumer integration, create the common reviewed source package/revision and accepted pins, and separately release actual execution. The present worker cannot self-accept or run that next phase. Frozen files should remain unchanged pending review; later findings require a new question/re-release.

For read-only freeze verification, load freeze.json and hash each listed repository-relative ordinary file against its bytes/mode/SHA256; compare exact membership of the two preparation directories plus the five source/doc files, excluding freeze.json. Do not rerun the exclusive observation/plan writers into these retained paths; their no-overwrite behavior intentionally refuses reuse. The fixture suite can be rerun only under a newly authorized evidence path after any review change.
