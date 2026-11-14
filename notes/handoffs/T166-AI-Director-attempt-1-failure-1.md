# T166 actual attempt-1 failed native frame classification

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket / revision: T1661.2 / D239; sole invocation consumed; worker did not change authoritative status.
- Phase / contract revisions: RULES_INITIALIZER_FOUNDATION0.3 / D231,D237,D239; D196 qualifications retained.
- Base and pre-existing edits: ticket base bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work; no Git commands or mutations.
- Changed files: NEW tests/outbreak/rules_initializer/candidate-1/attempt-1/** and supervisor-fixtures-1/** from the sole verifier; own NEW question and this handoff only. Source, preparation/history and live dependencies remain immutable.
- Commit / patch reference: none.

## Acceptance evidence

PASS — release/preflight binding: reviewed driver8438bf98f05981f7e47dfd1a13631df761d0094dc0b8c793ca3cf72577cb763f, supervisor6acaf1f7b98b93ef21b592630131d6b61f6270ca55ab71f424c3ebf78da9c4ae, candidate333b6d0717fbb9b75b74aa96426f8180ad443b49c1acf5711f2a73a7c218da5e and preparation-2 pins c1744e41ab610fafaa8a9746092d846400a97daf9b34c7d440344ebea75c08d0 were used without retargeting historical controls. actual-release.json binds current authority separately. Exact sole command from project root:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B tests/outbreak/rules_initializer/candidate-1/verify.py --actual c1744e41ab610fafaa8a9746092d846400a97daf9b34c7d440344ebea75c08d0
```

PASS — guarded simulations: all54 actual-method mocked supervisor/terminal cases passed in the one fixture child. Its result explicitly records zero actual children/signals/waits inside those fake cases. This is simulated boundary coverage, distinct from the ordinary real build children.

PASS — builds and process supervision:18 exact planned native/Wasm object/assembly/link children returned0; executables were linked but not run. Native Darwin arm64 Apple clang and prepared MacOSX15.5 SDK, plus the pinned isolated Web SDK clang/wasm-ld, used unchanged -O2 diagnostics and object plans. All19 original handles including the fixture child were reaped; group absence observed; no primary, secondary or unresolved cleanup error. Every recorded end preceded its original child deadline; maximum child elapsed0.14682366698980331s. Aggregate observed child output60 bytes, from the fixture summary; all build stdout/stderr0. processes.json is an OUTER_FAILURE_LEDGER, not a fresh child allowance. Signal guard restored prior SIG_DFL and timer[0,0], errors[]. CLI observed exit1/REFUSE and pending_original_handles0 through the SAME session12783. No performance claim or tool-version observation is made.

PASS — actual zero-init/old-copy checks on both targets: native descriptor is in __TEXT,__const, no runtime initializer observed and old automatic initializer-copy mechanism absent. Wasm descriptor has compiler .rodata designation and linking init_functions0, with no old-copy mechanism. Wasm linear memory is not hardware immutable. These emitted-object/assembly observations require independent review and do not establish runtime behavior.

FAIL — complete native frame gate: frames.json native errors contain `Indirect call:_Z11rule_scalarjbx`. Both partial graphs were retained. The diagnostic shows a range-checked70-entry local switch jump table and `br x10` in the wrapper, supporting a local-dispatch interpretation for MAIN review; the current refusal remains binding. Native reported sums factory1424, validator1872, basis160 and run2656 are NOT accepted complete native proof while this error remains. Wasm frame gate passed with respective qualified sums1776,2216,168,3144, including declared local/parameter charges. No physical OS/VM/JIT stack attestation is claimed; D196 qualifications remain.

NOT RUN — four version children, native/Wasm262-row targets, both7864-byte response comparisons and target timing. native.bin, wasm.bin and result.json are absent. The4192-byte request corpus and7864-byte independent expected stream remain prepared evidence only. No candidate behavioral acceptance, REVIEW-READY success, final freeze, live installation or consumer pin change.

PASS — preservation: protected-before.json and protected-after-failure.json are byte-identical across42597 records. Prepared non-authority input pins remain unchanged; live p1_rules.cpp remains913ce462a5c3896d766adc66751f278d188462ee6b3b97973269d976b3cf00b2. No source/history/preparation repair, retry, alternate entrypoint, SDK acquisition, old-suite execution, game/browser/server/network or Git effect.

Core retained SHA256 identities (relative to tests/outbreak/rules_initializer/candidate-1):

| Artifact | SHA256 |
| --- | --- |
| attempt-1/FAILURE | 32081029060e7ac8a65788cdbfa23d33b55f88c3f11fcbe2b73b94536ecc6d27 |
| attempt-1/frames.json | 91c1c0ff9f6bf3c091a7d4f6c77285c2b0dc50d125a45476c6d26c62c90058d1 |
| attempt-1/zero-init.json | 9c29bbc074143689778e5e761c8bd7f9d6f40845ccd2440ae2b2d081ea91c5fd |
| attempt-1/processes.json | 25da01b793358fc86018caf09c350db06f8bb2910ef1d33c53b5c8aaa7a32d41 |
| attempt-1/dependencies.json | de2c15776120405e7e30d2c026a100117bb8e5ab315a87b14f8fa7f3c5ba6893 |
| attempt-1/guard.json | 70445148e5bdac579e06311db7402d235d5450bef0aa48f9125113fbcb52e9a0 |
| attempt-1/actual-release.json | e3ca5c0f28b4ce2fbd5cf730fc767f9c2dc81d01ae3f193828e910e33cb7978a |
| attempt-1/protected-before.json AND protected-after-failure.json | e017039a991d99d85a9881e275bdd1719a5ad47ba95966f100fa311cff663733 |
| supervisor-fixtures-1/result.json | 48af02db4af89dbb597dc38955ffd2acddfdf6e6be40801cac23a8d369e13e76 |

## Implementation status

The isolated initializer candidate and harness were prepared earlier and now compiled/linked on both targets. Fake boundary coverage passed; actual corpus behavior is incomplete because the mandatory pre-target native frame gate refused. No source change was made during this lease. The actual failure and all raw diagnostics/process/copy artifacts remain preserved, without a final-inventory/freeze package.

## Integration and questions

New notes/questions/T166-AI-Director-native-local-jump-table-1.md identifies the exact classification issue and possible separately scoped review/correction paths. Ticket1.2, contract0.3 and D239 were reread before submission. Failure stops/preserves under their explicit no-retry clause. No further execution or repair is authorized; MAIN disposition is required before new work. Candidate acceptance/live installation and full unchanged T161 proof remain separate. QA/T149 and all gameplay/P0/human holds remain.
