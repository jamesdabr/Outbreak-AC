# T146 native reaper/calibration — review-ready

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket/contracts: T1461.0 RELEASED guarded preparation / D173; NATIVE_RSS_CALIBRATION0.1, platform0.1, governance/foundation/P0 prerequisite0.5. Re-read exact ticket/contract before submission.
- State: REVIEW-READY, NOT FROZEN; MAIN independent review/clearance pending. No selfacceptance/status or contract edits.
- Base/pre-existing edits: no prior T146 root. Six new allowed files and owned preparation-1 evidence only, plus this own new handoff. No accepted controller integration, copied old package or unrelated edits/Git. T147 exclusive portable files untouched.

## Implemented preparation

PASS sole reaper: reaper.py NativeWait4Reaper claims one trusted OwnedChild association and exclusively calls exact-PID wait4/WNOHANG. Cache terminal status/rusage once; normal/signaled status and raw maxrss retained, even if usage is invalid. Defensive cached results, EINTR/deadline bounds, ECHILD/error poisoning, duplicate handle-claim/reflected competing returncode/PID-change refusal. Terminal/lost association never causes a later signal. No Popen destructor/poll/wait/private subprocess internals or wait-any-child.

PASS fixed future parent: zero-argument runFixedNativeRSSCalibration(), effect-free import/no CLI. Exact root/Python3.11.9/macOS arm64/helper-module locations/SIGCHLD disposition gates, six source/five SDK header/executable identities. Direct posix_spawn uses fixed argv/minimal env/fresh session, fixed child signal defaults, pipes and /dev/null; returned ownership stored before later fallible setup. Bounded drains and finally cleanup preserve partial acquisition/output/terminal facts. Contracted python3 path is the actual literal symlink python3→python3.11; future identity binds only that exact raw target plus strict canonical ordinary target, before/after. No tool/command selector, fallback or modification.

PASS fixed child/self ABI: baseline,32MiB touch_release,32MiB spike_early_exit only, sequential/no descendants. Every byte in private anonymous mapping touched using4096-byte blocks, released in finally. Self Mach reader loads only fixed libSystem at future entry; checked48-byte/count12 layout/offsets before calls through uint32 self port/task flavor and int32 record storage/return. Raw status/count/size/range/phase/monotonic peak checks, available failed raw observations retained. No Mach/ctypes-library/mmap effect at import or during preparation.

PASS explicit spike demonstration: drain both pipes to EOF, delay250ms with no competing reaping, then require first non-EINTR wait4 collection already terminal; still-live case fails. Fake test confirms terminal high-water survives the simulated released/early-exit interval. This is not actual spike/unit evidence.

PASS scope/bounds/privacy: whole20s/work15s/cleanup5s, child4s, no retry,8KiB each stdout/stderr,256KiB aggregate report/stream totals,128events; overflow/deadline/schema/usage/abnormal exit/cleanup failures cannot yield budget PASS. Exact owned unreaped child TERM/<=1s/KILL within remaining deadline; fallback fails. No unrelated signal/process discovery. Raw exceptions/environment/private config not reflected. Future exact caller must also enforce whole20s through syscall/acquisition/publication intervals; no invented pre-handle zero.

SCHEMA.md documents exact exports, records, literal paths/limits, ABI header locations, supported fixed alias, lifecycle/partial failure and proposed interpretation. Raw wait4/self-Mach ratios remain REVIEW_REQUIRED/NOT_EVALUATED; published-source bytes versus archived-manual KiB discrepancy explicit. No automatic unit conversion, native512MiB/Chrome2GiB PASS, footprint substitution, Chrome-root sum or complete tree claim.

## Guarded fixture evidence

PASS — inspected authored harness/helpers, then invoked only:

```text
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/qa/memory/T146/test_reaper.py
```

Final33tests/0failures/0errors, actual_effect_attempts[]. Audit/patch/import guards precede project imports; real subprocess/fork/spawn/exec/wait/wait4/waitpid/kill/pipe/ctypes-library/Mach/mmap/socket/host queries and helper clocks/sleeps denied. Helpers run through explicit mocked boundaries. Production ABI-binding code runs once through an in-memory fake ctypes/library object, never real ctypes or libSystem. No synthetic child execution, compilation or installed dependency import occurred. Unittest duration is runner metadata, not benchmark evidence.

Coverage: cached once-only public status/rusage, WNOHANG/EINTR/abnormal exit/ECHILD/invalid/missing usage/wrong PID/status, deadline interrupt storm, competing claims/changed association/no post-terminal signal, unit ambiguity, Mach status/count/range/layout/availability, child schema/phases/PID/ABI/duplicate/nonfinite errors, stream/event bounds, real production collector delay/overflow/deadline, cleanup TERM/KILL/fallback/lost ownership, partial pipes/returned child, fixed argv/env/session, parent zero-argument/exclusive output/unsupported host and fixed Python alias. Earlier passing29/31/32/33-case intermediate results/logs remain unchanged; final33 includes refined spike assertions.

run-1 remains absent. Mocked future report documents exist only in memory; all retained preparation is FIXTURE_ONLY/actual_process:false/actual_wait4:false/actual_mach:false/units_confirmed:false/P0:false. No actual access, ABI/units, RSS, child cleanup or OS compatibility acceptance.

## Exact checkpoint

All paths below under web/qa/memory/T146/preparation-1:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| review-ready-1.json | 6990 | 8a7f51afd61444e85aef09f354115951a878102b47b730936276a091596e8a1f |
| fixture-result-5.json | 848 | 616f89055257b5bed44666fc82dcee702ab5bce30770c5df0439ca34e83fe477 |
| source-diff-1.patch | 59653 | 286acbd258848fbf7424916d711ca5da99b37c7ccb761bb4eaa8143790034f39 |

Checkpoint binds all six exact sources, governing refs, five declared SDK identities, latest result and all current17 owned source/preparation members; checkpoint itself is the18th owned file. No links/specials consumed. Builtin-only metadata/hash/diff checkpoint authoring allowed writes to only two exact new paths and denied effects/mutations elsewhere; no project import/rerun during checkpoint authoring.

| Source | SHA256 |
| --- | --- |
| reaper.py | 9d089e2a8f70e28ee35d084f10d1a4bd6c57dd93e641fa92b15f33078bfa8836 |
| calibrate.py | 2446f04d12fcebb4ec17f972eb7cc8b80b1f40d4e71417171eff062a01ec781c |
| child.py | 74c826213dcfb13d65a94741808f3447192591961f7c2a888e6d394863c615cb |
| test_reaper.py | fc10361a1889a269aca1a6f18ae78a2cb017dd6a87608751b9193413760c3e30 |
| SCHEMA.md | c7298b9a14397b893dd8f92880f2aaa3e43996c250d9dd7761a7a908e9fcaec4 |
| README.md | 960c66c6783a04f122d5ac7c5b55bd23813b4e9d569400b2c3cc989e09b72db5 |

## Pending MAIN gates

Review source/schema/fixtures before explicit final freeze clearance; no freeze here. Future actual calibration requires separate exact caller/tool/source review and owner approval, with actual unit provenance accepted before any budget evaluation. No actual native/browser/game/network/process audit, Mach/wait4/mmap experiment, integration, system/privilege change, dependency install, runtime retry or broad forest audit. No question requires guessing an ABI: source layout is specified, installed behavior deliberately remains untested. QA stays paused; T143 and owner braking preference remain independent. Engine returns to standby after this review-ready delivery.
