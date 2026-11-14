# T078 portable numeric foundation handoff

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T0785.1 RELEASED, D072; frozen submission for MAIN review, no self-acceptance.
- Phase / contract revisions: APPROVED SHARED_NUMERIC_FOUNDATION0.1; GOV/BROWSER_FOUNDATION/P0 subset0.5. Full gameplay/interface proposals and P0/P1 remain independently gated.
- Base commit and pre-existing edits: existing shared checkout and previously accepted browser/native prerequisite work preserved; no clean-checkout assertion or unrelated edit ownership. No existing allowlisted production files were present before creation.
- Changed files: NEW source/outbreak/fixed.h,fixed.cpp; NEW tests/outbreak/numeric/T078/{wrapper.cpp,wasm_runner.mjs,verify.py,README.md,attempt-1/**}; this NEW handoff. attempt-1 contains task-owned cache/temp/logs/native/object/Wasm/corpus/output/evidence files only.
- Commit or patch reference: none; no commit, branch, dispatch, contract/ticket/decision or existing source/build/artifact/pin edit.

## Acceptance evidence

| Criterion | Result / evidence |
| --- | --- |
| Exact approved five functions/constants | PASS: fixed.h/.cpp match approved declarations and semantics; no other public production API or game integration. Checked add/sub, signed ties-away rounded mul/div, floor uint64 sqrt, conservative Q16 axis normalization. |
| Unchanged failures / alias rejection | PASS: per-case sentinel comparisons, int32 overflow/zero-divisor/rounded-overflow, invalid int16 axes,121 output-alias cases; scalar input/output aliases also tested. Production writes only after successful checks. |
| Actual native AND Wasm, same production source | PASS: four actual compile/link commands exit0; native binary and import-free Wasm executed. Actual fixed.cpp source is identical in both builds, recorded before compilation. Minimal test-only C ABI, only fixed.o/wrapper.o, no runtime library/import or game glue. |
| Independent exact oracle / exhaustive axis corpus | PASS:94,976 cases in24 batches<=4096, zero per-case native/Wasm/oracle mismatches. All65,536 signed-byte pairs plus int16 extrema/alias, arithmetic signs/extrema/ties/overflow, square boundaries/max/randoms. Python arbitrary integers/math.isqrt, no mirrored C++ oracle. |
| Before/after preservation | PASS:37,735 frozen file identities identical, no added/removed/changed identity across source/src,source/enet,web/runtime,current/offline/native outputs,T070 bundle, original cache and installed SDK. All tool-created files are under the task directory; no existing helper/build inventory/pins touched. |
| Pinned tools/environment/flags and bounded evidence | PASS: attempt-1/plan.json records exact commands, clean env, input/tool/API/harness hashes before build. No fallback flags, missing library, download, port acquisition, global cache/SDK or environment modification. result.json and full corpus/output hashes retained. |
| Scope / formatting | PASS: notes and isolated arithmetic/test additions only; git diff --check exit0. No gameplay, mock game, browser, native server, service or network execution. |
| Movement/combat/gameplay/P0/P1/performance | NOT RUN / not part of this release. Numeric results make no platform, timing, physics or gameplay acceptance claim. |

Executed command from /Users/jd1/code/apps/outbreak:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/numeric/T078/verify.py
```

Exit0: passed=true,cases=94976,batches=24,failures=0,changed_protected=0.
macOS26.5.1 arm64; Apple Clang17.0.0 (clang-1700.0.13.5), SDK7.0.0/compiler
777e6e5db7b4990bcaeb1b9998ed642cc84e6629, SDK Clang/LLD24.0.0git84ba7b37...,
accepted Node24.19.0 (SHA25627db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1),
Python3.11.9. Exact executable identities and compiler/link/runtime environment
are in plan.json/logs. Native version was additionally captured to
logs/native-clang.version because the native and SDK tool basenames share the
driver's clang++.version log name. No benchmark/hardware-performance assertion.

Production SHA256:

- fixed.h:f2b7c303eab8ad4e4ad33593f55759196a8f711bbd791e8ad50715824aa792c3
- fixed.cpp:d7a40cfc8e47b17965e6f31c5f9d7ad1f9650e0c3fb4b306c459cc89a4a7e49a
- corpus:bd8cc8807f6a60e8f70573b4211c6e086a5eb4e8ae7d96b06c8950d4052739f4
- expected/native/Wasm outputs each:ef6be0cd47985dd9428730c8781b8faa51dc09032b32b938008013c4d674d6bb

## Implementation status

Five production arithmetic functions and constants implemented, executed on
both targets and frozen. No simulation/test-double substitution. All writes
remain in the released new-file allowlist. The test-only wrapper's mutable
sentinels and exports are not production APIs. Integer bound arguments and
exact numeric examples are in tests/outbreak/numeric/T078/README.md.

## Integration and questions

No new dependency/asset, build integration or game source/API change. No missing
runtime/cache/flag was encountered, so no execution-scope expansion or open
question is needed. The original46MiB sysroot was copied/verified task-locally;
direct installed LLVM compile/link avoided invoking Emscripten port acquisition.
No existing offline/native/current game artifact was rebuilt or rerun.

Exact reproduction inputs/commands/environment: attempt-1/plan.json; exact oracle,
input/output and preservation evidence: attempt-1/result.json and adjacent files.
The driver refuses reuse of attempt-1. A reproduction needs an explicitly
released fresh task-owned attempt location; do not delete this frozen evidence.
Source/tests/evidence/handoff are frozen for MAIN's review. MAIN alone accepts
T078 or releases dependent work; T002 and P1 remain separate.
