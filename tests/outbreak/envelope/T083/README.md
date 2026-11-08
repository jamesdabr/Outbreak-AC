# T083 header-only codec — partial execution evidence

Scope: APPROVED PORTABLE_FORMAT_FOUNDATION0.1 section A / T0835.6 / D079.
Only envelope.h/.cpp are production files. No body decoder, application message
acceptance, authentication, match/sequence validation or integration is implied.
All nonzero type bytes, zero epoch/sequence/ID and opaque ID bytes are header-valid
only. The accepted numeric kernel remains unchanged and is not a dependency.

## Current result

Wasm:13,482 independent Python golden cases,53 batches<=256, zero mismatches;
zero imports, memory plus three named test ABI exports only, no libc/runtime
archive needed. The same production source was compiled, linked and executed.
Native: first compile FAILED because directly invoking the installed Command
Line Tools clang++ cannot locate iostream in the recorded clean environment.
Native execution and ASan/UBSan are NOT RUN. No alternate flags/include paths,
runtime installation, sanitizer suppression or substitute codec was used.

MAIN question: notes/questions/T083-engine-native-launcher.md recommends the
/usr/bin/clang++ launcher already accepted/executed in T078, with identical test
flags and a new once-only task-owned attempt. That change has not been executed.

## Corpus and checks

Python struct golden bytes/fields are independent of the C++ codec and contain
all offsets, little-endian scalars,16-byte opaque IDs, type0/255/all byte values,
zero/max epoch/sequence, body0/1064/1065/65535, every input truncation0..35,
every provided length36..1101 and encoder capacity0..1137, header field corruption,
all flags, single-bit mutations, every combination of malformed validation
categories, contradictory/null precedence and8192 seeded randomized cases.
Outputs compare full canonical fields or the entire guarded destination, not
only a digest. Rejection checks entire output-object bytes including padding,
all destination bytes, guards and unchanged encode control/input. Success
checks all36 encoded bytes and untouched trailing capacity. All cases vary
offsets0..7. Header success never validates an unknown application body.

The native wrapper is prepared to repeat calls with exact-size heap allocations
alongside guarded buffers so ASan can detect access beyond declared lengths;
this memory-safety coverage remains unexecuted pending native tool resolution.

## Evidence and reproducibility

Initial authorized invocation from repository root:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/envelope/T083/verify.py
```

This failed at native build-0; attempt-1 preserves plan.json (pre-build exact
input/tool/runtime/ABI/corpus hashes, clean environment, flags/commands),
corpus.txt,expected.txt,labels.txt and logs/build-0.stderr. No evidence overwritten.
Independent unaffected Wasm continuation:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/envelope/T083/wasm_only.py
```

Exit0; wasm-continuation-plan.json records helper hash/commands before execution;
wasm-result.json and logs/wasm-only-* record actual compile/link/execution and
full comparisons.32,575 original frozen file identities remain identical:
source/src,source/enet,fixed.h/.cpp,T078 evidence,current/offline/native outputs,
T070 bundle,original cache and installed SDK. Unconsumed other-owner controller
and candidate-test directories are not compile inputs or snapshotted dependencies.
The continuation rechecks every originally recorded identity; it does not claim
an independent new directory-membership inventory. No code writes there occurred.

Only task-owned sysroot copy/temp/cache/log/object/Wasm/corpus/output paths are
written. Installed SDK7.0.0/compiler777e6e5..., SDKClang/LLD24, Node24.19.0 and
Python3.11.9; native intended AppleClang17. macOS26.5.1 arm64. Native sanitizer
dylibs are present/hashed but coverage is not claimed. wasm-ld uses --no-entry
and explicit case_buffer/result_buffer/execute exports; Node asserts no imports
and exact exports. No new library/flag fallback or game/service/network execution.

The driver allows a fresh --attempt attempt-N but refuses existing evidence.
Current files/attempt are frozen on this partial handoff; future native launcher
changes and execution require MAIN resolution. Tests do not establish P0/P1,
physics/authority, full protocol support or performance.
