# T157 — REVIEW-READY private synthetic spread stream

**REVIEW-READY, NOT FINAL FROZEN OR SELF-ACCEPTED.** Await MAIN source/evidence review and explicit final freeze clearance. No owned process remains live; no additional execution planned.

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/contract: T1571.0 / D206 / APPROVED SPREAD_STREAM_FOUNDATION0.1 adopting stable advisory. Mandatory governance/MVP/AGENTS/foundation scope read; exact contract/advisory/ticket and accepted T156 tool plan inspected, ticket/contract identities rechecked before submission.
- Base/pre-existing work: ticket bdaa8df7ec39d9408f97feda4560832d7ef26c3c with preserved shared checkout; no Git/status/cleanliness claim. All pre-existing production/accepted artifacts remain read-only.
- Writes: NEW source/outbreak/{p1_spread_rng.h,p1_spread_rng.cpp}; NEW tests/outbreak/spread/T157/{verify.py,wrapper.cpp,wasm_runner.mjs,SCHEMA.md,README.md}, fresh attempt-1/**; this own new handoff. No existing source/header/recipe/tool/SDK/original cache/authoritative file, other lease or asset changed. No integration/publication/source transfer.

## Implemented subset

Exact private-integration ob::spread_rng::State and seed_stream/draw_pair only, guarded C++11 header including only accepted p1_types. No public Seed4/MatchInit, cone/aim/shot/ordinal/eligibility/commit/room/network/OS entropy. All test data and seed material are deterministic SYNTHETIC fixtures, not real secrets.

Seed checks exact32 size BEFORE null, constructs65 bytes (master32,rawMatch16,PID LE8,nine literal ASCII spread-v1 bytes/no NUL), calls unchanged accepted SHA512, decodes first16 bytes as four LE words, repairs only all-zero derived words, then publishes. Internal hash failure maps to Invariant before output publication. Every raw Match/PID bit pattern is mathematical input, not admission authority.

Draw rejects only all-zero input State with Invariant, retaining State/scalars. Otherwise stages exactly two sequential xoshiro128** steps in prescribed order and publishes after both. Unsigned widened multiply/shift plus uint32 narrowing provide required modulo behavior; no wrap fault, discarded draw, reseed or extra validation transition. Fixed locals only; no I/O, allocation, clock, engine, mutable global, float/compiler128/host crypto or new production dependency. Guards/exports/retained test State are wrapper-only.

## Actual verification and limits

One inspected invocation from /Users/jd1/code/apps/outbreak:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/spread/T157/verify.py
```

Exit0,9343 cases PER TARGET across10 bounded stream-preserving batches:690 seed calls and8653 draw-pair calls,9320 successful/23 refused. Eight fixed compile/link operations and20 native/Wasm batch executions all exit0 with zero stderr; same actual new helper plus accepted hash, no substitute implementation. Wasm has zero imports and precisely memory/request_address/response_address/run exports. Every exact40-byte output equals independent oracle, not only a checksum.

| Criterion | Evidence |
| --- | --- |
| API/include/signature/State | PASS: exact advisory interface block/sole core include, double-include/signature/16-byte State assertions compile both targets. |
| Seed concatenation/endian/domain | PASS: each256 master,128 match,64 PID bit; zero/ones/ascending/asymmetric grids, PID0/max/high-bit, explicit byte-order variants and all eight offsets. Independent hashlib over65-byte material, first16 LE decode;668 successful synthetic preimages retained as ordinary oracle INPUTS, not a preimage search/forced output. |
| Size/null/failure semantics | PASS:20 Size refusals including size0/1/31/33 and large null declarations, two exact32-null refusals, one zero-State Invariant refusal. Exact Fault code/stage0/detail0, actual unchanged State/draw sentinels and guard/input observations all match. Nonnull views have accessible declared backing; no pointer/alias/UB probes. |
| State bits/wrap/two-step sequence | PASS: every128 State bit, individual zero words, ones/alternating/asymmetric/high-bit/rotation/multiplication/shift wrap and deterministic states. Independent arbitrary-integer oracle uses algebraically expanded simultaneous old-word transition versus production ordered XOR assignments. All four state words and both outputs compare every call. |
| Continued REAL State | PASS:256 streams×32 calls=8192 draw-pair calls,128 from raw synthetic State and128 from actual seed_stream outputs. No stream split across processes; op3 has zero replacement-state payload and operates solely on retained actual State. Every intermediate State and all64 draws/stream match. Seed-init calls are included in690, continued calls in8653. |
| Exact40-byte compact observation | PASS: all bool/Fault/State/actual draw slots/flags7/six reserved-zero bytes match. Seed draw slots are independently initialized actual sentinels, not fabricated API outputs; zero refusal returns actual zero State. Accessible guards surround every relevant object/backing. |
| Tools/plans/dependencies/effects | PASS: inspected new source/harness/driver, exact source/tool/argv/environment/layout/corpus/stream plan before compilers; actual generated dependencies before target execution. Fixed tool roles/path/hash equal accepted T156 plan; observed aliases recorded without general substitution. Own verified sysroot/cache/tmp/module/Node paths only; no old driver import/invocation/install/fallback/app/browser/server/network/Git. |
| Bounds | PASS:raw373720 bytes/target,747440 both; all child output747954 including514 version bytes, below shared8MiB and1600000 raw envelope. Driver10.8266s, largest child0.3924s, under300s/60s. No timeout/overflow/failure/retry. These are operation receipts, not performance acceptance. |
| Preservation | PASS:40228 protected identities unchanged across accepted core/hash/fixed/envelope/map, frozen T147/T151/T154 test/evidence, SDK/original cache; before/after protection JSON identical. Own source/harness/reference inputs unchanged during execution. No whole-workspace claim on concurrent workers. |
| Zero-derived repair/internal hash failure | SOURCE-REVIEW ONLY, as permitted; no SHA preimage search/fake hash/injection/hook. |
| Statistical/cryptographic-strength/entropy/P0/gameplay/performance/human | NOT RUN / no such claim. |

Observed macOS26.5.1 arm64, Python3.11.9 canonical binary; accepted Apple clang17, SDK Emscripten7.0.0/revision777e6e5db7b4990bcaeb1b9998ed642cc84e6629 clang24/wasm-ld and Node24.19.0. Full executable hashes, exact argv, clean child environment, aliases/versions and native/Wasm header dependencies are retained. No old accepted driver/suite was rerun and no accepted source/data was edited; accepted hash was compiled and executed as a dependency in this new test.

## REVIEW-READY identities

SHA256; attempt shorthand means tests/outbreak/spread/T157/attempt-1. All seven source/harness/doc hashes still match pre-execution plan.

| File | SHA256 |
| --- | --- |
| source/outbreak/p1_spread_rng.h | 54eacd6a645ed9daeae9246d3957933fecd9b5c50434e3639fa07e49cc754acd |
| source/outbreak/p1_spread_rng.cpp | ada3b2373ccf20bc37af7658e242d9cb77de788fed8c60e045c9bf6a5a21a29b |
| tests/outbreak/spread/T157/verify.py | 874642fbb9195667adda234eb3496c87cd507975e4aa715f15a201d51c3d18a7 |
| tests/outbreak/spread/T157/wrapper.cpp | 025f3d00a58fb4962c7173f37b9c878345001db46df0f535f4d302ccf572a5c5 |
| tests/outbreak/spread/T157/wasm_runner.mjs | 990c5e8875847e9352da01d4b77ae056b95be80b6780ca031a29fafce01fcf33 |
| tests/outbreak/spread/T157/SCHEMA.md | ce371659ac3d92fd13aa9ca05a82c3ca2a2cc279a16603390260994876146d76 |
| tests/outbreak/spread/T157/README.md | 6c0b6b34651edf9ad0c885114142199ef77930e47d927999dcbac3ae684cfae2 |
| attempt/result.json | 53e4748540628753fa0ac0d57d553ee44fcc9f0a2889b772705a27a35ef476b0 |
| attempt/plan.json | bb622f8b6c6919e214a98d82cebcb8798c56bed2163b23f3f5996ec7208c9c43 |
| attempt/corpus-plan.json | 093318399d9928f63248a3500cf778c6161da31a4b5bec77758e00c533cc9a4d |
| attempt/processes.json | d0c206b77cf0ba2df055c4148bb2493ce3d1ee5fdc26e81174882b4b3269a84d |
| attempt/dependencies.json | a297f7c29490e5ca9f3fb3bfc3b2495cad33a118e252f8a0149cd9c267cf8226 |
| attempt/corpus.bin,896928 bytes | 1053ac9eaf2d5b3e8354e9b79c89851b616d6bdf616dfcbfd8a63ad051ca5f7b |
| attempt/expected.bin,native.bin,wasm.bin,each373720 bytes | 79d8cd3111acd29d2649b7aec1983e9283792d1b9ef73c4d8ff59defb455c980 |
| attempt/cases.json | 51999a62c4df4bd577ff3e4660c6f0d1b69a2d5ee705ec98336bffbbb1fd3a98 |
| attempt/streams.json | 0b4f549c340983be2a9cee7f731c340dbab9167704fceaea18b4d44636fb98f1 |
| attempt/seed-preimages.bin,43420 bytes,synthetic only | 9dc9f1788ae94d98adc1eca82a864486b973bd185d510ca5bdfcc3849f4dd390 |
| attempt/spread.wasm | 9e7dd6806b6f78fa676db63930e010396063e2ff4dc887c698b55eec22006734 |
| attempt/protected-before.json,protected-after.json | 352b4e218e8a495900587edd36ec930927b916e5c3a30e7e3cc41277269cf976 |
| MVP/SPREAD_STREAM_FOUNDATION.md0.1 | 498381a7ed25c8bf25b6f8bb6a7e3e3352a1137a89589d6f1aa6ff84c6e44c0e |
| tickets/T157.md1.0 | 62b5e48ead2644ec2c2b30210df72bdaa08215e5dec6c58160a1f6c68cc0eb78 |

## Next boundary

No scope expansion/source correction needed by this delivery. Preserve REVIEW-READY package and wait explicit MAIN freeze clearance; no occupied attempt retry/cap adjustment or consumer integration. Future server-private owner alone determines shot acceptance/stream advance; neither helper success nor raw mathematical Match/PID grants admission. Real OS entropy/master secret lifecycle, public Seed4/MatchInit storage, cone/shot/ordinal/commit, fulltyped/P0/platform/human/QA/runtime/RSS gates remain pending. Own handoff hash is reported separately. Stop/standby for review.
