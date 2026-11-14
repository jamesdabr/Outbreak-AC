# T151 — REVIEW-READY fixed rules factory

**REVIEW-READY, not final frozen or self-accepted.** Await MAIN source/evidence review and explicit final freeze clearance. No owned process remains live; no more execution is planned.

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T1511.0 / D185, APPROVED SHARED_RULES_FOUNDATION0.1. Updated mandatory AGENTS/governance/MVP/browser-foundation/P0 documents read; exact ticket/contract re-read before submission. P1_RULES0.2 constants unchanged.
- Base/pre-existing work: ticket source revision bdaa8df7ec39d9408f97feda4560832d7ef26c3c, preserved shared work. No Git/status/cleanliness claim. p1_rules files were absent before creation; existing accepted source/core/hash/fixed/envelope/map and T147 package preserved.
- Changed: NEW source/outbreak/{p1_rules.h,p1_rules.cpp}; NEW tests/outbreak/rules/T151/{verify.py,wrapper.cpp,wasm_runner.mjs,SCHEMA.md,README.md}, fresh attempt-1/**; this new own handoff. No source-owner transfer, integration, existing recipe/cache/SDK/authoritative edit, commit or publication.

## Implementation

Exact adopted WeaponRules/RulesP1 declarations, guarded stdint-only-via-core C++11 header with only p1_types include; rules_p1 is the sole new public function. No tuning input, AngleTables/validator/aim, movement selector, simulation or app binding. Local staged fixed record, checked200-byte explicit LE encoder, unchanged accepted SHA512, then infallible field publication and Fault None/0/0. Signed i32 encoding uses mathematical modulo2^32; no struct padding is encoded/hashed or used as a canonical representation. Any internal encoder/hash failure maps to Invariant/0/0 before out publication.

Production has no allocation, I/O, clock, mutable global, engine/host-crypto/new dependency or large buffer. Small fixed records/arrays and accepted hash locals are comfortably below64KiB by construction; no whole-game stack/performance claim. Unsupported alias/invalid allocation remains caller precondition. No legal caller-input rejection exists; no invalid-reference UB or artificial hundreds-case corpus was made. Internal invariant-failure handling is source-reviewed, not injected/executed here.

## Acceptance evidence

| Criterion | Observed result |
| --- | --- |
| Exact declarations/include/signature/types | PASS: exact-text comparison to the two adopted H record blocks and sole core include; native/Wasm guard/signature/array/type assertions compile. No excluded symbols introduced. |
| Real factory + accepted hash on both targets | PASS: eight fixed compile/link commands exit0, zero stderr; real native executable and import-free Wasm both run exit0 with actual p1_rules.cpp/p1_hash.cpp. Wasm has exactly memory plus six named test-only exports. |
| Independent all-field/canonical hash oracle | PASS:70 scalar fields serialize to200 explicit bytes; all200 returned bytes plus64 returned digest bytes match independent Python struct/constants/hashlib on both targets. No C++ values/layout or mirrored encoder is read into the oracle. |
| Deterministic output after different state/poison | PASS: three calls after0x00/0x5a/0xff poison overwrite complete defined fields/hash and Fault Invariant/123/456→None/0/0; before/after guards on distinct record/Fault allocations remain intact. Three raw native/Wasm/oracle lines equal exactly. |
| Signed offsets and order | PASS: camera[-6144,1280,307], pistol[666,358,-512], rifle[1126,358,-512] and all array/weapon order encoded in fields.json/canonical.bin and observed returned bytes. Native padding is outside the format. |
| Inspected bounded isolated tooling | PASS: new verifier adapted from T147 as text only, no import/old execution. Source/harness inspected, exact tool/source/argv/environment plan before compilers, independent canonical/corpus hashes before compilation, six generated dependency files hashed before target execution. Own verified sysroot/cache/temp/module cache only; no fallback/import acquisition/app/network/browser/server/Git. |
| Preservation | PASS:35951 protected entries unchanged across accepted primitive/core/hash source, entire frozen T147 test/evidence tree, original installed SDK and original cache. Before/after protection JSON identical; direct driver inputs unchanged. No assertion about unrelated concurrent workers' whole workspace. |
| Operation bounds | PASS:9.7222s driver, largest child0.3875s,3766 combined child-output bytes; limits300s/60s/8MiB. No failure, retry or occupied evidence overwrite. These are operation receipts, not platform performance acceptance. |
| Full rules enforcement/typed API/P0/game/performance/human | NOT RUN / outside this isolated factory. |

One inspected invocation from /Users/jd1/code/apps/outbreak:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/rules/T151/verify.py
```

Exit0: passed=true,cases=3,canonical_bytes=200,exact_native_wasm_oracle=true,changed_protected=0. macOS26.5.1 arm64; accepted Apple clang17, Emscripten7.0.0 clang24/wasm-ld, Node24.19.0 and Python3.11.9 roles/pins. Exact tool identities, argv/environment/OS and source inputs in plan.json; separate version logs and actual native/Wasm dependency identities retained. No T147 entrypoint or existing build driver invoked.

## Canonical material and exact REVIEW-READY identities

Actual200-byte material is `tests/outbreak/rules/T151/attempt-1/canonical.bin`; independent SHA512 and both returned digests:

`c11570130bba5d4031c3e4782c88798b10161cc06d9c67ad06522d9c0aaecde49b823935fc9bed35d92ce2913a3dfe1399fc7818d852c572d33005162cec8433`

SHA256 identities below. Attempt shorthand means tests/outbreak/rules/T151/attempt-1; source/harness bytes still match pre-execution inputs.

| File | SHA256 |
| --- | --- |
| source/outbreak/p1_rules.h | a347d16b3a48e0234d471cdfcfc431e2877085c4f14dc9c801f3d2cfe4f9a896 |
| source/outbreak/p1_rules.cpp | 7ab5a9b474ecf269f3f1e898ef39985728dd329d7cf5c3dc98005ed7f02b1bc1 |
| tests/outbreak/rules/T151/verify.py | dabbac5d79ec14f8b6a77a9753f71f7c153616de6b76bf776c58955695dfed5f |
| tests/outbreak/rules/T151/wrapper.cpp | c49bf7ef322d34f9b82f894dc569ee8a95256d88e495784f11ca1520ea53be62 |
| tests/outbreak/rules/T151/wasm_runner.mjs | 23217dfb25b31eda0e2805fec1e1b6caeb05052abc62362a424bc74355ef3f86 |
| tests/outbreak/rules/T151/SCHEMA.md | afd2e700941322c7b8219d60897ecaa6e4c66b52048ad3d20fbbca2a27360a0e |
| tests/outbreak/rules/T151/README.md (pre-execution plan) | d78d20d59c42178b53300c4dcf11d9c3c25bd0707b4772cada982685abe5f403 |
| attempt/result.json | 313dc9e259084492a217de7e5f634b1c6439b99ee6c6b87c0d15fee6d19dfef7 |
| attempt/plan.json | e970815275bc2621c94409b82fac78e6976a36764ea4c90ed6b73f92456d737e |
| attempt/processes.json | d3c87832fe364c2a534e758bbf840d6d5013f91571f0121b838bda5b5e2fa355 |
| attempt/dependencies.json | 7a40c4e4a4cfff40ea33b9938e7e6e1b89d857c3f672aff900b388e62820018d |
| attempt/corpus-plan.json | e3f602198ecd24196f303bf0c7fcb53931f16c509663035c75112b8e45440020 |
| attempt/canonical.bin | ef9fe11b25e7d15ff585cd9175a1e479a55cc5e93efaf56c34cec891e7ed7a66 |
| attempt/fields.json | 0f9fc93343cae00b0dff2da22d53198fb3cfd373675cb41f81dd0224ad88b992 |
| attempt/expected.txt, native.txt, wasm.txt | 6d12f58ab05b183406983b5b87d32049487bcc3609335a88961ba7adfe5cc2e8 |
| attempt/protected-before.json, protected-after.json | 3beb826cbac92cf237ce4a62c11f3d1943ea73ab2e8ef3f3153bd27182c6eb91 |
| attempt/rules.wasm | 79a332898683e3c7cfe18c3bc21353ec005cb4c5fa468514196feb52bd90aeca |
| governing MVP/SHARED_RULES_FOUNDATION.md0.1 | a1a69fadef059991a7065d89c75ccae32165a7e4e716b4d3a1ec23f2e6b5fac8 |
| tickets/T151.md1.0 | 1d3f1e3fa62b7c18b39ef42b62cb9ff0f0c3bf2feca881ad29b86512b7a92cb2 |

## Integration and next boundary

No scope expansion or question is needed. REVIEW-READY package remains unchanged for MAIN review, not final frozen. Wait explicit freeze clearance; no test rerun/occupied attempt retry or source/header extension. Only a new lease may add validator/AngleTables/aim/table consumption or integrate targets. T150 and owner ground selector are independent; QA pause/T149/actual memory/human/fullP0/performance gates preserved. Handoff own SHA256 is reported separately to avoid self-reference. Stop/standby for MAIN.
