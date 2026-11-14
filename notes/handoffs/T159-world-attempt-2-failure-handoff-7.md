# T1591.11 actual attempt-2 failure handoff

- Worker: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Lease: T1591.11/D266/WORLD_QUERY_FOUNDATION0.8, ONE exact fixed caller2 invocation; unchanged QUERY_PUBLICATION0.2 and original G1 API/numeric/row/resource requirements.
- Base: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work; no Git invocation/mutation/commit.
- Writes: fixed caller created NEW tests/outbreak/geometry/G1/attempt-2/** only, including owned SDK copy/compiled partials/logs/failure; this own NEW post-terminal handoff. All source/preparation/history/dependencies/original tools/cache/SDK and both MAIN callers stayed read-only.
- Disposition: **ACTUAL FAILURE, consumed and preserved. Outer exit1 at command21 Wasm link: wrapper.o undefined memcmp. No repair/retry, G1 acceptance, final inventory or freeze.**

## Exact authorization, caller and observed outer exit

Read D266/current ticket1.11/foundation0.8 and all1547 bytes of caller2 before execution. Revalidated exact caller/source/preparation3 artifact/installed rules/fixed tool identities, ordinary source/caller sizes/modes/single links, absent attempt2 and absent preparation3 refusal marker. D266 SHA256be98c6e4900496573ea96a97c8486585785530d69267e3eab47ec10cfb28b2e1; caller2ea79dbf4923e1802e2a4158e81458293935cdeb9ba3f64b620b46fb5bec10256. Caller review notes/reviews/MAIN-T159-fixed-caller-review-2.json hashes87b16da69d152e865a6427acd87b849f28a7478c618be1042417adc619758866. MAIN's4605-record preflight receipt43f862bccf4e4c67f0b276820d77791f382669a08cd09a6e3837cd17952f442e and independent review4aa659f31cf2b9d2b50ee9c106cd0235e761d0a328b1f4c75795f66cec687e00 remain the pre-run review inputs.

Exactly once, no arguments, from /Users/jd1/code/apps/outbreak:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -B /private/tmp/outbreak-T159-approved-caller-2.py
```

Initial tool chunk2586bc returned running session93771 with empty output. The SAME session was polled; final chunk67b36f observed **exit_code1**, traceback ending `RuntimeError: actual child refused: 21` at verify.py2767. No observation timeout/restart, second caller invocation, alternate entry/tool/flags, probe, repair/retry/source edit or case reduction. All subsequent actions were standard read-only inspection/hashing and this NEW note. Old caller1 was never invoked.

Failure ledger elapsed_seconds5.24358491692692 is sampled before failure.json durability, not a precise independently measured full outer elapsed. The original300-second whole and60-second operation cutoffs were not reset; no timeout/output overflow caused this failure. The same-handle outer exit1 is the final terminal observation. No candidate success manifest exists.

## Concrete link failure, not an output-oracle result

Commands0..19 (all20 native/Wasm object and same-option assembly/stack-usage compilations for geometry/hash/fixed/rules/wrapper) exited0. Command20 native link exited0, producing an unexecuted native executable. Command21 Wasm link exited1 with exactly124 stderr bytes,0 stdout:

```
wasm-ld: error: /Users/jd1/code/apps/outbreak/tests/outbreak/geometry/G1/attempt-2/wasm/wrapper.o: undefined symbol: memcmp
```

Its exact argv, also retained in the final process receipt:

```
/private/tmp/outbreak-web-sdk/upstream/bin/wasm-ld --no-entry --export=setup_address --export=load_setup --export=request_address --export=response_address --export=run /Users/jd1/code/apps/outbreak/tests/outbreak/geometry/G1/attempt-2/wasm/geometry.o /Users/jd1/code/apps/outbreak/tests/outbreak/geometry/G1/attempt-2/wasm/hash.o /Users/jd1/code/apps/outbreak/tests/outbreak/geometry/G1/attempt-2/wasm/fixed.o /Users/jd1/code/apps/outbreak/tests/outbreak/geometry/G1/attempt-2/wasm/rules.o /Users/jd1/code/apps/outbreak/tests/outbreak/geometry/G1/attempt-2/wasm/wrapper.o -o /Users/jd1/code/apps/outbreak/tests/outbreak/geometry/G1/attempt-2/geometry.wasm
```

Read-only emitted assembly identifies a normal direct call in the harness comparison helper, not a conjectured source production counterexample: diagnostics/wasm/wrapper.s12442–12453 defines `_ZN12_GLOBAL__N_111same_motionERKN2ob21RationalCapsuleMotionES3_` with two pointers, `i32.const72`, `call memcmp`, `i32.eqz`. A memcmp function declaration is at line37; source wrapper.cpp193 defines same_motion and its existing callers observe rational inputs. These are retained compiler/linker facts. No helper definition/library/flag/source was added, no binary was patched and no alternate link or target was attempted.

The four prepared version commands22..25 and both complete16384-row targets26..27 did NOT RUN. No geometry.wasm, native.responses.bin or wasm.responses.bin exists. No actual oracle/native-Wasm equality, Fault/guard/output/immutable-input behavior or full query/ABI/export/call-chain correctness is established by successful compilation or the native link.

## Complete retained process and ownership facts

All22 final process receipts are in failure.json; logs00..21 retain each stdout/stderr and provisional receipt. Twenty-one receipts have ok=true; the final Wasm link has ok=false. Independent read-only counts:22 reaped=true,22 owned_group_observed_quiescent=true,22 retention_complete=true,22 group_mutation_attempted_before_reap=false,21 POST_REAP_ABSENT observations. Every receipt lists stdin/stdout/stderr/selector closed and no skipped release. Combined child stdout/stderr is124 bytes (all earlier logs empty), under the unchanged8388608 pre-growth cap. No unresolved child/process ownership is reported in these receipts.

The21 successful operations actually exercised D260's strict terminal0 route: fresh original waitable terminal0, pre-reap errno1 recorded as UNKNOWN, zero mutating signal, strict original reap0, distinct first timely post-reap ESRCH, resolution POST_REAP_ABSENT. This is observed evidence for those21 operations, not all possible platform/error paths or proof of the unproven host cause.

Final failed command21 retained facts:

| Fact | Value |
| --- | --- |
| Original PID /PGID | 65848 /65848 |
| Bound and confirmed nonreaping anchor | true /true |
| Native waitid result /errno | 0 /0 |
| Terminal event | SIGCHLD20,CLD_EXITED1,status1,returncode1 |
| Primary supervisor fault | nonzero original exit observation |
| Additional group-probe fault | PermissionError `[Errno 1] Operation not permitted` |
| group_permission_observation | null, as required for nonzero terminal |
| Mutating group signal attempted | false |
| Reaped /wait attempts /returncode | true /1 /1 |
| Later group observed absent | true |
| Completed closes /release skipped | all four /none |
| Retention complete /final state | true /FINAL_REFUSAL |
| Child complete elapsed | 0.024372875108383596 seconds |

The nonzero link correctly did not receive the terminal0 exemption. Its raw EPERM and nonzero primary remain fatal despite later absence. No broad PermissionError waiver or post-reap mutation occurred. D235's fixed library/ABI boundary was authorized for these original children; no separate real capability probe, PID discovery/attachment, positive-PID proxy, privilege/sandbox change or global signal was used. No approval-review rejection is inferred from a runtime errno.

Provisional receipts intentionally remain BEFORE_FINAL_RETENTION_CHECK. Final elapsed/retention/ok fields are in failure.json; do not infer success from provisional records or from files alone. Outer secondary_retention is null. Failure marker remains `T159 incomplete/failed actual attempt; do not consume`.

## Stable retained failure and selected compiler evidence

Prefix tests/outbreak/geometry/G1/attempt-2/, read-only wc/shasum/stat:

| Member | Bytes | SHA256 |
| --- | ---: | --- |
| FAILURE | 54 | 02ff810742b776a8f03757fc4db1a7ac8702984f60602a10e97aaa6213f56933 |
| failure.json, all22 final receipts | 51225 | 9b299169fb9fc079f8cd4d49fec6ff924cab32707106151f40cc475860034461 |
| logs/21.stderr | 124 | f808a9404a2ae577bd0458c85540682b3f2370d8a5d665a7073d7715e74a6fbf |
| logs/21.stdout | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| logs/21.provisional-receipt.json | 2165 | d73ee30f791b32371e7e83a5a41bad58d52bc3f2b47c51ec6ef6046ecc42b916 |
| geometry-native, NOT EXECUTED | 223664 | 971f23f0908c290004abe24e282145c4e5a76e20737b2447eeda59fa543a4ed4 |
| wasm/wrapper.o | 9446939 | b673fa4750d527420b72e4b50f1065525ec61751d67fe1b5ecd3647c51a3e890 |
| diagnostics/wasm/wrapper.s | 280614 | 2f522c0e3b49623f81729df16c75c729fee9ea560a013327ac32851024ebfb03 |
| diagnostics/wasm/wrapper.su | 2164 | 2fb00ddd40ac0ee4b4a1cea7d6cbce9c2f0d496dccbbc1bc00badf704d4e7976 |
| inspected-plan.json | 32825 | 5dfe08512420ce2696c39b898288f3bf82115f75893ac1f02c0928aae782077b |
| setup.bin | 915564 | b96adfac57cc4a3b51768d86a9a92206d92199ea9359ca08c9b4e1f2bb2064a9 |
| corpus.bin | 2709120 | d6f1a202961c82cccde81a003aca448aa54942c5f077055907482d46b0d6a642 |
| expected.bin | 2686976 | 580ead76672dce81f30b50cee37b70f59a87c62008e2d9b61a16803aa55d3ad5 |

All native/wasm object/.su/.d files and diagnostics/native plus diagnostics/wasm .s/.su/.d files for the five units are retained, along with the owned SDK copy, own caches/tmp and xcrun_db. The partial non-cache inventory used `rg --files --hidden --no-ignore`, so ignored objects were included. Native executable is0755/single-link; observed other selected compiler artifacts are0644/single-link. These selected pins are not a final frozen inventory. The9.4MiB object is an artifact, not captured stdout/stderr or an enlargement of the8MiB output cap.

No processes.json, actual-dependencies.json, frame-analysis.json, review-ready-owned-graph.json, terminal manifest.json, linked Wasm module or target response file was produced. The final complete receipts reside in failure.json. Dependency closure and complete native/linked-Wasm frame joins were scheduled after all26 commands; they were NOT REACHED. Raw emitted assembly/.su/.d are preserved evidence, not a largest-frame substitute or unmeasured normal-helper zero charge. No analyzers or extra tools were executed after failure.

## Protected inputs and truthful failure limits

Before attempt creation, fixed actual preflight checked reviewed clearance/preparation/source/dependency records, full accepted G0 binding, fixed tool/argv/environment/D235 input identities, original SDK/header candidates/aliases, full schema and semantic coverage. It copied the exact original recorded SDK into owned attempt2/cache/sysroot, verified copied membership/kind/mode/bytes/hash/exact symlink targets, and retained exact prepared raw inputs before spawning commands. This does not replace the final post-run protection verification, which was NOT REACHED after the failed link.

Independent standard post-terminal hashes match all5 harness/docs,3 production geometry/store files, installed333b... rules, all12 preparation3 artifacts, old A1 failure/marker and both fixed callers. Verifier staysd3436c1a7a2dc7800937fffa578babc3894624fb46f0ff2c9e455d8ae4d01395; wrapperdf4dfcc355cb5d7bcba81ff3a5e9c8377b15d3894fc7e06cba51ae3e0e2b7129; runner010ac5e0e19fd5f96c808d7b3d3ac8c762a798a6bc751c6c28722a59631232cc; schema15e0582628ef70b2848c7142b40b3b78e910d58bbb70fc8c496453add86f0598; READMEe23e97fe09d9b873d29587baa986fa2727f8e78a4d998fb01df96af204ff7c4d. Production pins remain geometry.h8bfa5558.../geometry.cppbf30f77b.../store.h7a7b185d.... Preparation3 manifest65ac8e8c65cb2eab9b8394b548a445fed991c50630f90494d44697cdc3cc8653 and plan2eae6a6f76dd1b06358cd8abb34c2032a9f724aae8a0fe37b5470ffa5e83604f remain unchanged. Old A1 failure160218d7.../marker02ff8107..., caller176d18838... and caller2ea79dbf4... stayed immutable. No source, dependency, SDK/original-cache or historical artifact was repaired or rewritten.

The complete original/history protected after-graph and all-source/header/tool/SDK frame/output terminal gates were not completed by the failed workflow; no blanket after-protection PASS is claimed. No post-failure project helper, generic graph verifier, compiler/link/version/symbol/ABI/runtime probe or alternate entry was invoked. Read-only assembly/source inspection identifies the specific emitted dependency only.

## Acceptance evidence and next gate

| Obligation | Outcome |
| --- | --- |
| Exact fixed caller2 once | observed outer exit1; failure preserved |
|20 object/diagnostic commands | exit0 |
| Native link command20 | exit0; executable not run |
| Wasm link command21 | FAILED undefined memcmp from wrapper.o |
| Four version commands | NOT RUN |
| Both16384-row production targets /oracle equality /guard observations | NOT RUN |
| Complete emitted normal frames/dependency/ABI/export qualification | NOT REACHED /INCOMPLETE |
|22 original handles /groups /retention | final receipts reaped/absent/retained; zero mutating signals |
| D260 terminal0 unknown observation |21 real resolved observations; nonzero link correctly refuses |
| Final protected graph /REVIEW_READY /inventory /freeze /acceptance | NOT REACHED /NOT AUTHORIZED |
| Retry/repair/source change/extra effects | NONE |

MAIN must review this consumed failure before naming any future source/entry/effect lease. This handoff authorizes no memcmp shim/libc/flag change, follow-up compile or target run. Worker stops with attempt2 and all inputs/partials stable. Full G1/G2/caller/gameplay/runtime/P0/MVP/RSS/performance/human/Player/QA/T149 holds remain unchanged.
