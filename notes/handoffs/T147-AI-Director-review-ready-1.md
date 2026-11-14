# T147 — REVIEW-READY portable core/hash

**REVIEW-READY, NOT FINAL FROZEN OR SELF-ACCEPTED.** MAIN source/evidence review and explicit freeze clearance are required next. No more test invocation is planned or needed by this delivery. No owned process remains live.

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T1471.0 / D174; SHARED_HASH_FOUNDATION0.1 approved isolated P0 prerequisite; governance/browser-foundation/P0 reporting0.5. Updated AGENTS and mandatory MVP documents read; ticket/contract re-read before submission.
- Base: ticket names bdaa8df7ec39d9408f97feda4560832d7ef26c3c with preserved shared work. Git/status was not invoked; no clean-checkout claim. source/outbreak contained only accepted fixed/envelope/map pairs before the three new files.
- Changed files: NEW source/outbreak/{p1_types.h,p1_hash.h,p1_hash.cpp}; NEW tests/outbreak/hash/T147/{verify.py,wrapper.cpp,wasm_runner.mjs,SCHEMA.md,README.md}; fresh attempt-1/**; this NEW own handoff only. Existing sources/contracts/SDK/cache/recipes/Git remain untouched by this work.
- Commit/integration/publication: none. MAIN retains exclusive source-lease transfer authority; no target includes these files.

## Implemented behavior and provenance

Exact section1 core declaration block, with include guard/stdint-only C++11/ob namespace; no other proposed p1_types records or behavior. Hash header declares only bool sha512_bytes(ByteView,Hash512 &,Fault &). Production hashes0..2097152 bytes, rejects Size before Null, sets exact stage/detail0 Fault on both outcomes and leaves all digest bytes unchanged on refusal. Empty null succeeds without null arithmetic/memory access. Digest is staged before publication and explicitly emitted big-endian.

Inspected/adapted local crypto.cpp lines216–283, SHA2560c3e194dfc60e93066d5a0e30644158d46df373a3b6df63c27ecd18126fcf1b0. Retained public-domain/LibTomCrypt comment; same SHA round constants/schedule/logic, replacing engine macros and unaligned/endian casts with explicit bytes. No production dependency, host crypto, allocation, mutable global, I/O, exception, signed overflow or compiler128. This is repository code reuse with independent digest verification, not a formal cryptographic audit claim.

No simulation/test-double substitutes for production hash: both compiled targets invoke the actual p1_hash.cpp. Mutable buffers/exports/native I/O are test-wrapper-only.

## Acceptance evidence

| Ticket criterion | Observed result |
| --- | --- |
| Exact core definitions/include graph/signature | PASS: verifier exact-text compares the entire adopted declaration block to pinned H; core includes only stdint, hash includes only core. Both target compilations exercise guards/signature/static assertions. |
| Bounded standard SHA-512 / refusal/output semantics | PASS:334 successes and6 denials, exact per-case Fault/status/digest equality with independent hashlib and failure sentinels. Size-before-Null includes both null/nonnull oversize and UINT32_MAX. |
| Required binary/boundary/standard corpus | PASS:340 cases; lengths0..260; eight offsets at111/112/127/128/239/240/255/256; standard empty/abc/112-byte multiblock/million-a; NUL/high-bit/all-bytes;2MiB offset7; null0/nonempty/oversize. Four literal standard digests match hashlib and both production targets. |
| Actual native AND Wasm same source | PASS: six compile/link operations exit0; native and import-free Wasm run exit0, zero stderr. All340 raw lines on each exactly equal expected.txt. Wasm exports precisely memory plus six named test helpers. |
| Inspected fixed tools/plan/isolated effects | PASS: prior T078 approach read as data, never rerun. New source/harness inspected, plan/tool/source identities recorded before compilation; corpus identities before first compiler; copied sysroot verified. No fallback flags/library acquisition/install/app/network/browser/server. |
| Bounds and evidence retention | PASS: total driver10.0143s, largest child0.3596s, combined child output93674 bytes; ceilings300s/60s/8MiB. Full argv/status/logs, inputs/tools, generated dependencies, corpus and raw outputs retained. Attempt1 exclusive/occupied refusal, no failure/retry. These timings are gate-operation accounting, not performance acceptance. |
| Accepted primitives and original SDK/cache | PASS:33875 protected file/directory/symlink identities unchanged; fixed/envelope/map, original crypto.cpp, original SDK and original build cache. protected-before.json equals protected-after.json byte-for-byte. Driver inputs unchanged throughout execution. This is the enumerated protection set, not a whole-workspace snapshot of concurrent workers. |
| Full interface/rules/tables/gameplay/P0/performance/human | NOT RUN / outside this module; pending gates remain mandatory. |

Executed once from /Users/jd1/code/apps/outbreak after inspection:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/hash/T147/verify.py
```

Exit0: `passed=true,cases=340,exact_native_wasm_hashlib=true,changed_protected=0`.
OS recorded macOS26.5.1 arm64. Native Apple clang17.0.0/clang-1700.0.13.5; installed SDK Emscripten7.0.0/revision777e6e5db7b4990bcaeb1b9998ed642cc84e6629, upstream clang/LLD24.0.0git84ba7b37f02df5a5567e31a1bcfa0f607e578f12; Node24.19.0; Python3.11.9. Exact executable SHA256s/environment/compiler argv are in attempt-1/plan.json. Native/Wasm compile dependency files and dependencies.json hash actual consumed headers; no SDK manager executed.

## Exact REVIEW-READY identities (SHA256)

| File (repository-relative; attempt means tests/outbreak/hash/T147/attempt-1) | SHA256 |
| --- | --- |
| source/outbreak/p1_types.h | 8f9222262be5cfbc5e16f10b040b6bef95385af0db58669cfc3d0cfcc6f8b621 |
| source/outbreak/p1_hash.h | 4492332dcad22c68ac983491e89bf81fbbccad1b82f2abc825e4c24140e8c3f3 |
| source/outbreak/p1_hash.cpp | 5669fd85c115b12212a1aba0b0aa352503f61ec319e4eab9d1be9b6dd6aecceb |
| tests/outbreak/hash/T147/verify.py | 7596e7d0b4f29ad810364606c05df910fd23ab9b8ca95f003b83fcb6492cee7a |
| tests/outbreak/hash/T147/wrapper.cpp | 0f2e6f6d5425f1162a3407da77eaeeb3d4cf0ab788d5c8cca58ce9e6506a7e58 |
| tests/outbreak/hash/T147/wasm_runner.mjs | 2671d76365f923d87803ec4f7187774e4e49400d8e369a30d447fbfdcdae1e51 |
| tests/outbreak/hash/T147/SCHEMA.md | 6c356c67075a29ec980adfbd2f9ab6138076ce987318a3f94d5f241f96e0bcf1 |
| tests/outbreak/hash/T147/README.md (pre-execution preparation record) | 78f15fd505be609cd5d46aec87646301bb6a2b50f3caca3b0bf80d2604cfd76a |
| attempt/result.json | f8a0381e10bbc4cb489824c006567b387dcf1fe1968aca035d1d8cb36f60fdff |
| attempt/plan.json | cf3998fcf19894093bdf0a61cd85614779fd10058b3ae3d9874c3558a4bd5d41 |
| attempt/corpus-plan.json | 00815f6345ba7a3204d2257d584cad792819c7cc58f6975ff34284cbe9c0ac3b |
| attempt/processes.json | 686fa35ce671908840f05de9b87442bda56883566c8b731e67dfa09c55802b22 |
| attempt/dependencies.json | 0108f9a096143007e8d70133cfacad9034c5f981a7c62506b31be90302b52eee |
| attempt/corpus.bin (3149023 bytes) | 34ebd4fc4c0b1891fcd198334f99a64da6a46603d9939dc6e00a1b4c34b44b0d |
| attempt/cases.json | 63882666afb55e3560346ba7cb583e4090d68643ac99e05f8f27b8ae9577da51 |
| attempt/expected.txt, native.txt, wasm.txt (each340 lines) | ff93158aa3e387c5e78eac291576e7d01b9b458d36c901adaf0a85d9c08194b3 |
| attempt/native | d5f72bb2079c7f4c8db6be7cf3689cc0c580f12c558ccb2742b4ee4415cac2de |
| attempt/hash.wasm | 3d49350b487fe5e365d367ae0634f129638305780215e29272503528461df066 |
| attempt/protected-before.json, protected-after.json | bc87bd768f17f4c4c8a4f9d7ccdd27db13cb7be39bb4c7e44de07b9816c47903 |
| governing MVP/SHARED_HASH_FOUNDATION.md0.1 | 62fbe105ac3d1d6fbd98777e98a5b859ce3414974c8ac6b7f66171fa95a8a4a4 |
| tickets/T147.md1.0 | 7846409eab464e112a9b24b6264bff5e5b6c8283f0af0d31646487f9024ac4df |

Handoff identity is reported separately to avoid self-reference. Input source/schema/docs/harness bytes above still match the pre-execution plan; no post-test source or README changes were needed.

## Integration, limitations and next boundary

No open scope question: explicit D174/T147 authorization plus inspected fixed local driver sufficed; cross-system skill inspection found no additional external action. Review-ready evidence is preserved, not final frozen. MAIN must review the source and independent results and explicitly clear freeze. No code/table/target/recipe extension, source-owner transfer or rerun is implied; occupied attempt1 must not be overwritten. Final freeze may record all accepted package identities only after clearance.

This verifies the isolated real portable hash/core declarations, not full P1 behavior/API adoption, canonical digest schemas, rule/angle artifacts, security audit, game/server/browser integration, clean-build/performance/platform or human acceptance. Unsupported aliases are outside the API. QA remains paused; Engine T146 and Player T143 remain independent. Standby for MAIN review with no more execution.
