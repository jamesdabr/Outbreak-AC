# T178 final source and guarded-job submission — inventory refused

- Worker: MAIN delegate /root/review_native_candidate.
- Ticket/revision: T1781.2, RELEASED D272.
- Contracts: DEFAULT_DEV_BUILD_PREPARATION0.2, BUILDER_TERMINAL_GROUP_CLOSURE0.3, D269/D271/D272; D263/D235/D236/D238 retained. Current pinned authority hashes rechecked before submission.
- Base: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved overlay. No Git invocation. All six pre-existing source files matched MAIN baseline manifest da4be7392462c33bfd8bc4bc6e1b59c1616f602792dd96de52671b46a7210e99 before edits; copies retained under tests/outbreak/builder_reap/T178/preparation-1/pre-edit.
- Changed sources: web/build/dev_regression/{recipe.py,test_recipe.py,SCHEMA.md,README.md}; NEW tests/outbreak/builder_reap/T178/test_reap.py. build.py/verify.py unchanged. New preparation: focused home/preparation-1/**, module tests/preparation-1/pass-11/**. Own new preinspection/data-plan/final handoff notes only. No commit.

## Acceptance evidence

PASS (guarded simulation): direct original-child os.waitpid/WNOHANG correction, no Popen.wait/poll fallback; exact nonbool originalPID/status/uncached handle gates, ECHILD lost ownership refusal, terminal status conversion and immediate verified returncode/parent_reaped publication before the caller post-call clock. The unchanged hard=min(commandStart+120,wholeStart+3600),work=hard-5 feeds the helper;6000 observations and<=0.01 pauses add finite bounds without a new wait-entry budget. D263 terminal EPERM record/action/FIRST ESRCH and unrelated errors remain, private schema unchanged. Production source diff is confined to the helper and Effects.run consuming call.

PASS: all seven sources frozen before the first invocation, recorded in notes/handoffs/T178-source-freeze-preinspection-1.md SHA256bf99ba0d1b6f0bb05e07e66bf95bb65cb84e9cbb93c9f16f9bd5c7906862185e. No code/test/schema/doc edits between or after either job. Both actual-source harnesses deny real process/tool/FFI/network/old-driver effects before loading the current recipe. Fake Popen.wait/poll throw if called. No old project helper import. Existing228 groups/247 leaves retained with consuming fake boundaries adapted. Both source and current authority hashes rechecked at submission.

Exactly one focused invocation:

`python3 -B tests/outbreak/builder_reap/T178/test_reap.py`

Observed exit0, PASS_FIXTURE_ONLY16 cases,0.016435166937299073s,244058 retained bytes,6 guard denials. Fixed meaningful cases cover terminal0/nonzero/signal, noevent/EINTR continuation, consuming ECHILD, cutoff, wrong/bool PID/status, nonterminal status, cached returncode/changed identity, late valid consume and unrelated primary. Actual Effects.run/helper tested with fake boundaries and retained raw wait results/state/action traces. Source/clock/no-expired-following-effect assertions passed. Result tests/outbreak/builder_reap/T178/preparation-1/focused-1/result.json SHA25694a620c6d5884b4a564dcdbf8be51f81a70f52831493ac89ad2ed774ef44e7f6 (47098B). Invocation-plan SHA2565c42304f619804da2e424c18723139d8d8247e8368046ead542d2f7ddaa71fbe.

Only after focused terminal PASS, exactly one full invocation:

`python3 -B web/build/dev_regression/test_recipe.py --pass-id pass-11`

Observed exit0, PASS_FIXTURE_ONLY228 groups/247 leaves,123.06437454209663s,4203574 retained bytes,7 guard denials. Complete prior whole-client simulated graph and all prior scope/alias/role/receipt/deadline/IO/terminal-policy cases retained. Result web/build/dev_regression/tests/preparation-1/pass-11/result.json SHA256591d9c40e0f7b069aeb7a020ed883415aaf8edd5a0b3db80891181b2a9dc4e3a (983032B). Invocation-plan SHA2564505bc9e05ff95fa8c6b40977458f210058f644a23fb8bf481fad76b2cdaf975, with source baseline diffs. Each job separately within300s/8MiB output/128MiB retained. No retry/repair.

FAIL / NOT PUBLISHED: the sole inspected final3 DATA-ONLY operation refused during external-role validation, before mkdir, slot reservation, or any final3 write. It returned exit1 in0.210965458s: `ValueError: read-only external identity unchanged web/build/.cache/ports/libpng.6.59.tar.gz`. The authoring helper constructed a generic record containing SHA256 but omitted the archive-specific historical SHA512, then compared complete dictionaries. This is my metadata authoring error, not evidence that the archive changed. Read-only diagnosis confirms all shared physical metadata,1589315 bytes and SHA25686a3e4b501f7f50e392c4e456ea158893e9a595b1c63eb88c7bb9f6cf8772dad match the historical record; the extra expected SHA512 was not computed by that operation. Historical expected SHA512e14302d87864432d747896e3944a6416d4b5f3059f538cfe615ddbe1d0084d4a02d4df3ef2761b02c839858625bed57d873198792c3583029c619e1cf8c4561b remains unchanged. No external-change inference. No retry, field removal, incomplete comparison, corrected metadata continuation or source repair performed. MAIN explicitly directed preservation and a terminal handoff, with any future role-specific SHA512+SHA256 script separately reviewed/released.

final2 and final3 remain ABSENT. The final3 inventory/receipt/freeze criterion is incomplete, so this is a source/two-job evidence submission, not a complete candidate freeze or acceptance. Data plan notes/handoffs/T178-final3-data-operation-plan-1.md is preserved as a pre-operation plan, not a result. Prior T168 graphs/control blobs/history and T175 candidate remain historical and unchanged; historical owned file identities checked against T168 freeze except the four leased live sources before the metadata refusal.

## Implementation status and limits

Implemented: strict consuming source/caller and necessary private test/schema/document bindings. Simulated: all process, native ABI, selector, group, clock/storage/tool/build actors in both jobs; actual current methods executed with fake boundaries. NOT RUN: actual tools/version calls, native wait/FFI/load/signals/process/compiler/build/SDK-copy/browser/runtime, full client link or multiplayer. Fakes do not prove installed Darwin support, syscall preemption or hardware performance. No ticket/contract/status/freeze acceptance authority exercised.

## Integration and questions

No public API/recipe/flags/profile/asset/dependency changes. Wrappers, old sources/evidence/tools/SDK/cache remain read-only. NativeT167/Player/QA/T149 and all human holds unchanged. No real project attempt/candidate/common manifest created. Stop after this stable packet; MAIN alone disposes review and any separately authorized metadata-only continuation.

Frozen source SHA256:

- tests/outbreak/builder_reap/T178/test_reap.py 45555e8a764d1902c38a7dcd95b2b739d28a68b73f5b63fc1d8b59678a506167
- web/build/dev_regression/README.md f440d57f954d5323c5c636e9aceddd44d8c0e07d7b22e3ebdcbaab017d3f0d2c
- web/build/dev_regression/SCHEMA.md 19026aced80b5cf8591bcad06f75b25fd84c7e3a71ad183ca7e3d57c2b5614c4
- web/build/dev_regression/build.py 1e47f5fed2ea414405f1ad816e0aae7007bb41d4165cb553225fee2788209a7b
- web/build/dev_regression/recipe.py 7a4dd4f5555a23a96623d4d5c09d431e51220bdd6a1180467416e531d184dd4c
- web/build/dev_regression/test_recipe.py 705edf60dd7d80428f80e86a0950ca82ee577021daca82921d5a1d498fa3a140
- web/build/dev_regression/verify.py 3ec91f59208df47eded9d931d8a39ffd0f476a156312bd2312afdad94506c549

Retained job totals:

```json
{
  "tests/outbreak/builder_reap/T178/preparation-1/focused-1": {
    "bytes": 244058,
    "files": 10
  },
  "web/build/dev_regression/tests/preparation-1/pass-11": {
    "bytes": 4203574,
    "files": 372
  }
}
```
