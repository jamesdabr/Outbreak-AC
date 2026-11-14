# T156 Engine review-ready handoff

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket: T156 revision1.0; REVIEW-READY submission, no authoritative status change.
- Contract: ACTIVE_INPUT_CODEC_FOUNDATION0.1 / D200; advisory and H/W references pinned in plan.json.
- Base: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved existing work; no Git commands or mutations. Seven new owned sources/harness/docs and fresh attempt-1 evidence only.
- Platform: Darwin arm64. Installed pinned Python3.11.9, native clang17, Emscripten7.0.0 clang24/wasm-ld, Node24.19.0. Exact binary identities, argv and minimal environment: attempt-1/plan.json. No performance/hardware qualification claimed.

## Acceptance evidence

PASS: Exact adopted Held/InputFrame records live in p1_input.h, which includes only accepted p1_types.h. Double inclusion, member type/enum assertions and exact function pointer signatures compile as C++11 with warnings as errors on both targets. Actual production codec is compiled separately from test wrapper.

PASS: Explicit28-byte LE encoding; Size before Null before Identity/Range/Flags; widened signed decoding; staged decode publication and28-byte append. Both APIs set full Fault with stage/detail0. All yaw/tick values structurally accepted.

PASS: Sole actual attempt completed in 2.25s. 67,421 independent oracle cases per target: 66,432 decode and989 encode. Decode exhausts65,536 pitch patterns plus512 axis cases; encode includes512 axis cases. Family totals are retained in result.json. Meaningful bit/identity/tick/yaw/held/pitch/length/buffer/arithmetic/priority cases are included.

PASS: Native and Wasm each returned3,236,208 actual binary bytes, exactly equal to expected.bin. Every response is exactly48 bytes with all observation flags31. Full actual bool/Fault/defined output fields or initialized backing window and used are compared. Guards, input preservation, failure output preservation and successful prefix/suffix checks all passed.

PASS: Aggregate all-child output6,472,416 bytes <8,388,608; all8 compiler/link/test operations exited0 and were reaped, each <60s; whole driver <300s. No child stderr. No retry. All nonnull declared extents describe accessible storage; large arithmetic controls use null only. No alias/invalid-reference/UB probes.

PASS: Own copied frozen sysroot verified before build; own cache/tmp/Node/module paths. Direct dependency hashes recorded before execution and 61 rechecked at review checkpoint. Accepted core/numeric/envelope/hash and original sysroot protected snapshots are byte-identical before/after the closed actual interval; fixed tool binaries rechecked unchanged. This is a named-input preservation claim, not whole-workspace or live protection of unrelated worker files.

PASS: Wasm runner rejects all imports. Link pins only five test exports plus memory; capacities64/48 fixed before link. Production has no test hooks, allocation, clock, I/O, mutable globals or extra dependencies.

Evidence root: tests/outbreak/input/T156/attempt-1/. plan.json precedes compiler/runtime effects and pins corpus, oracle and exact layout. Native/Wasm raw outputs, expected.bin, cases.json, process receipts, dependency/protection snapshots and result.json are retained. review-ready-1.json binds sources, evidence and current authority; SHA256 71f9492a70aabbc0201f3427339aa23ecbbde9daaaae652dee0ff507e04e0bfe.

## Changed source and harness identities

- source/outbreak/p1_input.cpp SHA256 ee6bfe1c507f07802284661a54ca71b18cc4a4d7c6773393a87404160d576310
- source/outbreak/p1_input.h SHA256 e8ad0291d5cb33d68b4ed8050daf1684fbbb03d40eb0b735305940278095bddd
- tests/outbreak/input/T156/README.md SHA256 906fc5b8522646c061d54156934dd5d9c3d37f6c9ffb7398b44f2f091eb54632
- tests/outbreak/input/T156/SCHEMA.md SHA256 bcb4696fe00e17a4411946791046c19fbff71a33077eb29037751793ca4c5e52
- tests/outbreak/input/T156/verify.py SHA256 7e64176bd41fce557296cdd2f9c58af8626b8ba9b69b74be4e77cb2d4ec13174
- tests/outbreak/input/T156/wasm_runner.mjs SHA256 9f50869bdf0e275fb4195e79377b94cddeeff2f8402476bc9d6b8f3eb822c3a2
- tests/outbreak/input/T156/wrapper.cpp SHA256 208849b2bbaa6003c1697ec1bffe1cad6dd4d6bf0f60fa38610a5c9b328a7adf

## Implementation status

Implemented and actually tested: pure active Input28 encoder/decoder and exact adopted records. The independent oracle and wrappers are isolated test infrastructure; no simulated multiplayer is presented as runtime evidence.

NOT RUN / unreleased: full packet/batch/envelope integration, protocol eligibility/admission, input age/order/life matching, client/server networking, authority/replication/gameplay, browser/app/dedicated-server execution, P0/performance/human acceptance. Existing QA/T149/RSS/runtime holds remain unchanged. No installs, network, old drivers or Git operations occurred.

## Integration and questions

No unresolved codec question. Consumers must include adopted p1_input.h only under their own future release. No accepted p1_types/rules/query-wide source or old evidence changed. MAIN review and explicit final-freeze clearance remain pending; no freeze created.

Historical reproduction command (already occupied; DO NOT RERUN): /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/input/T156/verify.py. Inspect retained evidence instead.
