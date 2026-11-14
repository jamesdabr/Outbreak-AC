# T083 envelope codec partial handoff — native launcher question

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T0835.6 RELEASED / D079; incomplete gate, no acceptance claim or status change.
- Phase / contract revisions: APPROVED PORTABLE_FORMAT_FOUNDATION0.1 section A; GOV/BROWSER_FOUNDATION/P0 subset0.5; numeric0.1 unchanged.
- Base and pre-existing edits: shared checkout and accepted browser/native/numeric prerequisites preserved; no clean-checkout claim. World independently owns map_import; other-owner controller/candidate tests excluded from compile inputs/preservation dependencies.
- Changed files: NEW source/outbreak/envelope.h,.cpp; NEW tests/outbreak/envelope/T083/{wrapper.cpp,wasm_runner.mjs,verify.py,wasm_only.py,README.md,attempt-1/**}; NEW notes/questions/T083-engine-native-launcher.md and this handoff only.
- Commit/patch reference: none; no commits, dispatch, game/current source/SDK/assets/build/pin/contract/ticket/decision/numeric edit.

## Acceptance evidence

| Criterion | Result / evidence |
| --- | --- |
| Exact section-A public API/constants/error values | PASS implementation/static review: only EnvelopeHeader,EnvelopeError,three constants and two codec functions. stdint-only C++11 production files; no allocation/I/O/game globals, struct wire memcpy or padding/endian/unaligned-read assumptions. |
| Validation order / no partial output | PASS Wasm: exact Null/Short/Length-before-read then Magic/Version/Flags/HeaderSize/Length/Type decoder order; encoder Null/Short/Length/Type. All failure output/destination bytes unchanged; error reports exact category. |
| Independent golden bytes/fields/canaries | PASS Wasm only:13,482 cases in53 bounded batches<=256; zero per-vector mismatches. Full36-byte goldens, canonical fields, entire destination+guards/trailing bytes and failure-object preservation checked. |
| Required malformed/boundary/random corpus | PASS Wasm only: all truncations0..35/provided lengths36..1101/capacities0..1137/type bytes/flags, body0/1064/1065/65535, extrema/opaque IDs/endian, late type failure, combined error priority, single-bit mutations and8192 deterministic randomized cases. corpus/expected/output hashes below. |
| Actual SAME production source on native and Wasm | PARTIAL: genuine SDKClang compile/LLD link/Node Wasm runtime passed, no libc or imports. Native build-0 FAILED: iostream not found. Native source path/hash is the same proposed build input, but native execution is NOT RUN and cross-target gate is not met. |
| Installed native ASan/UBSan | NOT RUN: installed runtime dylibs inspected/hashed; clean flags recorded, but execution remains behind native header-discovery question. No object/syntax/mock result is promoted to sanitizer coverage. |
| Frozen source/game/artifact/cache/SDK preservation | PASS recorded identity comparison:32,575 before/after file identities unchanged, including fixed.h/.cpp and accepted T078 evidence; no source/build integration. Wasm continuation checks original identity set, not a new directory-membership inventory. |
| Scope / formatting | PASS: writes only within new allowlist; git diff --check exit0. No old helper, browser, game/native server, network, port acquisition, installation or service launch. |
| Full app/body/auth/authority/map/P0/P1/performance | NOT RUN / outside release. Nonzero header type accepts no application meaning; epoch/sequence/ID semantics remain unapproved. |

Executed from /Users/jd1/code/apps/outbreak:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/envelope/T083/verify.py
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/envelope/T083/wasm_only.py
```

First command exit1 at native compile; second exit0,wasm_cases=13482,batches=53,
failures=0,changed_protected=0. Full commands/environment/input/tool hashes were
written before invocation to attempt-1/plan.json and wasm-continuation-plan.json.
Actual logs are retained. macOS26.5.1 arm64, Python3.11.9, SDK7.0.0/compiler
777e6e5db7b4990bcaeb1b9998ed642cc84e6629, SDKClang/LLD24.0.0git84ba7b37...,
accepted Node24.19.0; directly invoked native AppleClang17.0.0 failed to locate
the test wrapper's C++ standard-library header. No performance claim.

SHA256:

- envelope.h:5a9ed4462b5c3fdcb61fced19293b335c4ea12994d8b8bb9f89584d3598b6168
- envelope.cpp:2c0bff1bbc6d1a03eea3e5bba59b6bb0ae8684b41f86f22c7ebe3523df2337dc
- corpus:11a86a820b5ebed0b362a1178c87921bceb72acff4d0d0f0990675cf5f1b0e0b
- expected/Wasm output each:741c8cb36d9b002cd72ecf955b527de4913d5333ac6c5ef9aa94e7f7e62163e3
- Wasm:277923c29caa016c3ecbff6876f48412a473d9cc28e6560a330ea016621d527f

## Implementation status

Header codec and bounded harness implemented, no fake codec or game integration.
Wasm complete for this corpus; native/sanitizer gate remains incomplete. Small
candidate/scalar records and bytewise LE reads/writes preserve failure atomicity.
Encoder writes exactly36 bytes; payload is never serialized/validated here.
Accepted numeric and separate World code remain read-only and unused.

## Integration and questions

OPEN notes/questions/T083-engine-native-launcher.md: approve installed
/usr/bin/clang++ (the launcher actually used successfully in T078) for both
native variants, same flags/environment and new task-owned once-only attempt,
or specify exact native tool/environment. T083 explicitly requires questioning
missing runtime/flag requirements; no alternative launch or flag was tried.

No new dependency was installed. The copied frozen sysroot/libc archive was
inspected; no memory library was needed or linked. Unimplemented imports are
not suppressed. Current source/tests/evidence are frozen with this partial
handoff pending MAIN's narrow resolution; do not overwrite attempt-1 or old
evidence. MAIN alone resolves, reviews/re-releases and accepts the full gate.
