# T078 isolated numeric verification

Frozen submission under T0785.1 / D072 / SHARED_NUMERIC_FOUNDATION0.1.
Only `source/outbreak/fixed.h` and `fixed.cpp` are production code. The wrapper,
Python oracle and Node runner belong exclusively to this test directory.

## Executed result

94,976 vectors,24 batches (maximum4096 records), zero mismatches. Native and
Wasm output match the Python exact-integer oracle byte-for-byte. The65,536
signed-byte pairs include65,025 valid and511 invalid pairs containing-128.
Additional int16 boundary pairs,121 output-alias rejection cases, scalar
input/output aliases, int32 boundaries/signs/ties/negative and zero denominators,
rounded overflow, uint64 square boundaries/max and deterministic random cases
are included. Every rejected operation checks sentinel preservation; scalar
alias cases preserve their original input on failure. The oracle independently
checks the normalized squared-magnitude bound for valid axes.

Examples:3/2→2;-3/2→-2;1431655765*3/2→failure/unchanged;
isqrt(UINT64_MAX)→4294967295;axes(127,0)→(65536,0),
axes(127,127)→(46340,46340),axes(1,1)→(516,516).

| Evidence in attempt-1 | Contents |
| --- | --- |
| plan.json | Input/API/harness/tool hashes recorded before compilation, exact compiler/link/execution commands and clean environment, OS/architecture/Python identity. |
| protected-before.json / protected-after.json |37,735 identical file identities across frozen source/src,source/enet,web/runtime, current/offline/native game outputs, current T070 bundle, original cache and entire installed SDK. No changed membership/content. |
| corpus.txt | Identical streamed vectors for native and Wasm; uint64 text enters Node as BigInt without Number conversion. |
| expected.txt / native.txt / wasm.txt | Exact per-vector status/output including unchanged failure values. All three SHA256 ef6be0cd47985dd9428730c8781b8faa51dc09032b32b938008013c4d674d6bb. |
| result.json | Counts per operation, zero failures, preservation result and full corpus/object/executable/output hashes. |
| logs | Four successful actual compile/link commands, tool versions. native-clang.version supplements the basename-shared clang++.version, which records SDK Clang. |
| cache/sysroot | Task-owned verified copy of frozen46MiB sysroot; no Emscripten/port builder or global cache write. |

Corpus SHA256:bd8cc8807f6a60e8f70573b4211c6e086a5eb4e8ae7d96b06c8950d4052739f4.
Wasm SHA256:e8b75362236ed57d00bd5a1d5c501a0249a1b565e3173ae5c29c74feaa5e8d93.
Full production-source hashes are in plan.json and the handoff.

## Execution boundary and reproduction

Executed from the repository root:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/numeric/T078/verify.py
```

The driver refuses an existing attempt-1 directory and never overwrites evidence.
Reproduction needs a newly authorized fresh task-owned attempt location; preserve
this frozen submission. Exact four build commands are in plan.json. No existing
helper, game inventory, game entrypoint, service, browser, network, package manager
or installer is invoked. Native Apple Clang17 C++11 compiles the same fixed.cpp
as the installed SDK Clang24 (Emscripten7.0.0/revision777e6e5...) Wasm target.
Accepted wasm-ld links only fixed.o+wrapper.o with --no-entry and four named
test exports. Node24.19.0 asserts zero Wasm imports and exactly memory plus those
four exports; no runtime library or JavaScript game glue is needed. No additional
link flags or library acquisition fallback occurred. Python3.11.9 supplies
arbitrary-precision arithmetic/math.isqrt; macOS26.5.1 arm64. No performance claim.

## Production arithmetic reasoning

Int32 sums/differences/products fit signed64. The product magnitude is<=2^62,
so signed division/negation cannot hit INT64_MIN/-1. Remainder magnitude is less
than the divisor magnitude<=2^31; doubled remainder and one-unit rounding stay
within signed64. Range-check before writing preserves failed outputs.

The sqrt search has an exclusive2^32 upper bound, so every tested midpoint is
at most UINT32_MAX and its uint64 square cannot overflow. For normalization,
distinct-reference and axis-range checks occur before any write. They establish
S<=32258, S*2^32<2^47 and abs(axis*2^32)<2^40; the outer branch's denominator is
positive and its exact floor-root square is safe. Explicit division truncates
toward zero; the ceil root is conservative. No float/128-bit arithmetic, heap
allocation, mutable production global, I/O or game behavior is involved.

This verifies the isolated numeric API only. It does not verify movement,
collision, camera, weapons, networking, engine choice, P0/P1 or the full MVP.
