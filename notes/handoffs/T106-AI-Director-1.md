# T106 exact two-header SDK alias preparation

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T1061.0 RELEASED at final read; submitted for MAIN review, no authoritative status/self-acceptance.
- Governing: native0.4/D111 exact two-alias correction; D107/D091; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5 preparation only. Full ticket/native0.4/D111 and frozen T105 failure reviewed before work; ticket/native markers re-read before freeze.
- Base: original source31d433b993d393b1902f7f57285a1d5ea6d2042d. Work began after completed frozen T105 handoff/question. All D106/D109 clones, D110 attempt/pins/manifest, SDK/source/libraries/old records remain read-only.
- Changed: only web/server/candidate/stage.py, test_preparation.py, README.md; NEW preparation-T106-20261108-1/** and this own handoff. build.py/verify.py unchanged. No Git/branch/commit/dispatch/contract/status change.

## Acceptance evidence

| Requirement | Result / evidence |
| --- | --- |
| Archive before editing | PASS prior-source/ holds exact prior three editable files plus unchanged read-only build/verify for baseline suite; prior-source-archive.json maps paths/hashes. Two immutable fixture DATA references copied into that new archive so original52 can run without editing it. All archived source bytes matched T104 freeze. |
| Exact two fixed aliases | PASS SDK_PTHREAD_ALIAS value unchanged; added SDK_SCHED_ALIAS for SDK/usr/include/sched.h -> raw pthread/sched.h, mode0755, ordinary canonical SDK/usr/include/pthread/sched.h. SDK_HEADER_ALIASES is a fixed source tuple containing exactly these two; no manifest-supplied alias map. |
| Shared validation before effects and when consumed | PASS shared sdk_header_alias rejects unknown names before filesystem access, then checks ordinary ancestors, exact raw type/text/mode, confined canonical ordinary target, canonical-only declaration in both existing maps and current target hash. authorize checks BOTH before reservation/effects; dependency_paths checks whichever exact raw alias is consumed before normalization. Existing raw .d/logs and subsequent canonical dependency/hash checks unchanged. |
| Proper physical fake SDK / original behavior | PASS common setup adds only sched.h physical temporary link/target, canonical-only pins and both raw names in FakeRunner dependencies. All52 original test bodies AST-identical, including pthread negatives, framework/owned-path/authority and no-real-external-read full pipeline guard. |
| Retained actual failure-format regression | PASS byte-identical copy of actual failed log.pre.d, SHA256c4fd1b45db65f65e251d9b6633a1923197787c8e98d4cb097b115cfafd5786c3. Provenance pins original path/report/freeze. Positive test uses its two exact raw alias lines/continuations in a fixture-target dependency record; no new compiler discovery is claimed. |
| Both-alias simulated build and independent verifier | PASS both normalized canonical targets appear in every fake unit's dependency map, both raw names remain in .d text,32 fake compiles/two links and independent verifier retain original success shape. Fake objects/signatures are not actual build evidence. |
| sched negative/pre-effect coverage | PASS wrong raw spelling/mode/type/target, missing/ordinary alias, nested target, linked ancestor, missing/undeclared/changed target pins/bytes all refuse before any fake Runner call/reservation. Consumed-time mode/hash/declaration changes refuse after gate. Unknown same-byte alias and unknown helper selector refuse; pthread behavior retained. |
| Guarded prior52 + corrected62 suites | PASS archived52 exit0/22.158s; corrected62 exit0/25.475s. Ten new regression cases. No failing run/retry. All real process/socket/compiler/signing guards retained; original no-real-CLT/Python/usr-bin file-read test now covers both aliases. |
| Narrow source / preservation checks | PASS static-review.json: only old sdk_pthread_alias validator replaced by sdk_header_alias, authorize loop and dependency normalization changed; all other old stage definitions/View/constants AST-identical. build/verify bytes unchanged. Old T104 frozen members preserved via explicit archive mapping; T105 failed report/freeze/raw .d and own failure notes retain hashes. |
| Actual new build/tool/SDK/runtime | NOT RUN. No actual compiler/version/native-tool/signing/build/discovery, SDK file access in tests, D110 retry/verifier, clone/cache staging, source-manifest/pin or link-stub-map mutation. |

## Implementation and evidence distinctions

Production change is only the exact two-header alias correction approved by native0.4. The shared validator retains the previous strict target/ancestor/current-pin checks and has no generic alias permission. Public schemas, flags, SDK selector, target/tool roles, limits, recipe identity, existing staged-framework handling and readonly consumer code are unchanged.

MAIN D111 supplies the complete selected alias-set conclusion from all32 retained .d files. This worker read/copies only the already retained failed T105 log.pre.d as DATA and preserves its path/hash provenance. The regression selects only the two raw header lines and their continuation format; it does not claim to replay all historical SDK dependencies or run a current compiler. No source/library/SDK bytes were patched to make the fixture pass.

Executed in original repository, guarded fixture commands only:

```text
python3 -B web/server/candidate/preparation-T106-20261108-1/prior-source/test_preparation.py > web/server/candidate/preparation-T106-20261108-1/prior-52.log 2>&1
python3 -B web/server/candidate/test_preparation.py > web/server/candidate/preparation-T106-20261108-1/corrected-1.log 2>&1
```

README documentation was updated after the passing source/tests run. Do not overwrite frozen logs on rerun. Tests use existing Python/macOS authoring and temporary fake SDK symlinks only, no actual native/hardware performance claim.

## Frozen identities

- preparation-T106-20261108-1/preparation-result.json SHA256c3183eadad8ab42da4d8897785cb3bf75ca0f2bef1a662874411e34d704685ca.
- preparation-T106-20261108-1/freeze.json SHA25665bd9bdd432b49849963b98cc70fa4de3e85348fcee31cfb9ad571d86cc78ef5;20 frozen files.
- stage.py SHA256b13b516fb82fb80dc13a70b5ac4264d5948117f1cb637d72620ec91a33a6a313.
- test_preparation.py SHA25674320e4832f9b8a32c608b97c4d16456bacff8f822273fb352012925f2e03bf1.
- README.md SHA256dce0d99d32691b51b576eb9c5deda34a2e01a917501659a57dd5454c2307d20e.
- Unchanged build.pyc81fd4d53a0e27c3f98a471b44c0479d20f16eca305f6775d2d7ce74a91609b6; verify.py686ca766fab080dbafd69bf4720f11296a0035a17abd5c2b30ab113255f9cd09.

Freeze contains five live source/docs plus all new preparation files, including original source copies, two fixture-data references, failed raw-data copy/provenance, both suite logs, targeted diff, static review and result. It excludes only itself and this handoff. Original source references map explicitly to archived bytes; old T104/D110 freezes/receipts remain untouched and are not misrepresented as current successor source.

## Integration and questions

No unresolved question for this correction. System link-stub predeclaration remains MAIN/T107 authorization data and was not changed. Actual T105 failure remains immutable/exhausted; no new native acceptance or retry follows from62 fixture passes.

MAIN reviews successor source/private documentation/evidence, then owns any new source revision/clean root, complete linker/SDK/source/Python declaration, exact pins/digest and separate actual execution release. No implementation or execution beyond that review handoff is inferred.
