# Shared numeric foundation prerequisite

Revision:0.1. Status: APPROVED ISOLATED P0 PREREQUISITE under D072. This freezes ONLY the following portable numeric API and verification, not the full T002 protocol/gameplay/interface proposals or production platform/P0/P1 acceptance. Relevant existing browser/GOVERNANCE/P0 subset remains0.5.

## Exact source/API ownership

Engine exclusively owns NEW source/outbreak/fixed.h and fixed.cpp for T078. C++11, namespace ob, include stdint.h only as needed; no SDL/GL/OpenAL/ENet/JS/game globals, allocation, I/O, exceptions, filesystem, wall clock or mutable global state in these production files. No existing source/build inventory is changed. Tests live NEW tests/outbreak/numeric/T078, outside frozen source/src/source/enet/web/runtime/driver trees.

Public declarations:

```cpp
namespace ob {
constexpr int POSITION_FRAC_BITS = 10;
constexpr int VELOCITY_FRAC_BITS = 16;
constexpr int32_t UNIT_Q16 = 65536;
bool checked_add_i32(int32_t a, int32_t b, int32_t &out);
bool checked_sub_i32(int32_t a, int32_t b, int32_t &out);
bool rounded_mul_div_i32(int32_t a, int32_t b, int32_t denominator, int32_t &out);
uint32_t isqrt_u64(uint64_t value);
bool normalize_axes_q16(int16_t x, int16_t y, int32_t &out_x, int32_t &out_y);
}
```

Private helpers are free if all semantics preserved. No unapproved public types/symbols. No signed overflow, platform floating rounding, floating math, undefined conversion or compiler-only128-bit arithmetic. Use checked64-bit intermediates and explicit integer behavior.

## Semantics

checked add/sub return false for any mathematical result outside int32 range; out is unchanged on failure. rounded_mul_div computes exact mathematical a*b/denominator, rounded to nearest integer with exact halves AWAY FROM ZERO; accepts negative denominator, rejects0 and rounded result outside int32; out unchanged on failure. Compute multiplication in signed64 (all int32 products fit), never overflow during remainder/rounding or negation.

isqrt returns the greatest uint32 r with r*r<=value, including0 and UINT64_MAX (answer UINT32_MAX). No overflow in comparisons, no floating sqrt or sentinel collision.

normalize accepts axes each in[-127,127], rejects others with BOTH outputs unchanged. Let S=x*x+y*y. If S<=127*127, each result is truncation toward zero of axis*65536/127. If S>127*127, let D=ceil(sqrt(S*2^32)); each result is truncation toward zero of axis*2^32/D. This deliberate conservative integer normalization guarantees squared output magnitude<=65536^2, preserves sub-unit input scale, avoids diagonal speed bonus and platform differences. Zero maps0,0. Integer denominator/ceil root must be exact; all intermediate bounds checked. Aliasing the two output references is unsupported and must be rejected with unchanged referenced value (document/test explicitly); ordinary distinct outputs are required. No movement speed, timestep, collider/camera/weapon behavior is implemented or approved by this module.

## Verification gate

Actual native AND Wasm execute the SAME production source against an independent exact-integer oracle and identical bounded vector corpus. Cover all int32 extrema/sign/zero/negative denominator/tie/round-overflow cases, uint64 square boundaries/max, every256^2 signed-byte axis pair (valid and invalid), unchanged outputs on failure and alias rejection. Test vectors may be streamed in bounded batches; no giant stack object or unbounded report. Independent Python integer arithmetic/math.isqrt is suitable oracle; mirrored C++ implementation is not. Compare actual returned values/status per vector across targets; labels/object compile alone cannot satisfy execution.

Use installed inspected native clang++ and accepted Emscripten SDK/Node identities; task-owned frozen-cache copy/temp/cache/log paths only, no acquisition/SDK/cache/global edits. Minimal Wasm test build may directly link the actual two objects with accepted wasm-ld, --no-entry and ONLY named test C-ABI exports; no full client/port build, error suppression/export-all/unsafe flags or browser/server/network. Inspect/pin exact test flags/tool/runtime/environment before execution; if new runtime libraries/missing cache needed, question rather than install/change flags silently. No production entrypoints/export attributes added for tests; test-only wrapper owns exports.

Record source/API/tool/commands/hash corpus/native+Wasm outputs and exact numeric results, bounded failure evidence, fixed native/offline/current game artifact unchanged. This is pure arithmetic evidence, not authoritative movement/combat/network/physics/P0/MVP proof. MAIN alone accepts and releases dependent work.
