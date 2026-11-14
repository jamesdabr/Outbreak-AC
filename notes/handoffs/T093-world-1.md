# T093 actual matched-sanitizer decoder corpus handoff

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket/revision: T0935.16 / D089; PORTABLE_FORMAT_FOUNDATION0.1 / D079; GOV/BROWSER/P0 0.5. Ticket/decision/pins rechecked before submission. MAIN alone accepts T083/T084/T093; no self status/phase changes.
- Base:13f0d8eea4822dee5c976661218d022be74342e3 plus preserved shared overlay.
- Changed: NEW tests/outbreak/sanitized/T093/** and this own handoff only. New inspected runner/dependency discovery, owned tight-wrapper copies, two deliberate negative controls, new binaries/objects/debug/dependency records, raw bounded results, provenance/freeze. Production/original wrappers/corpora/oracles/references/toolchain/SDK read-only. No source fix, old driver rerun, commit/reset/revert/dispatch or unrelated T091/T088/T092 inputs.

## Acceptance evidence

PASS — Trusted MAIN pin-file SHA256
674d712553b7e702d1f90e1ba56f51d4fe48243302e8a447e06d08b0d8930006
verified before compiler/native execution and after completion. All19leaf sizes/
hashes unchanged; exact SDK alias target/resolution and clang++->clang->clang-22
links validated. Full envelope Wasm reference is attempt-1/wasm.txt; partial
attempt2 Wasm was never used. Map complete references are attempt2.

PASS — Actual SAME production .cpp/.h compiled with original frozen wrappers
using accepted project-local LLVM22.1.8/matched runtime, C++11,
-fsanitize=address,undefined -fno-sanitize-recover=all, original module-specific
flags, frame pointers/debug/dependency evidence. T083_NATIVE exact-size heap
checks remain active. Both source modules unchanged from original native/Wasm
proofs. No fake codec or object/startup-only promotion.

PASS — Pre-build -###/-M header discovery passed with permitted existing
-isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk (MacOSX15.5.sdk).
T083 iostream/string resolves bundled LLVM22 libc++v1 headers; no additional
include override/header/runtime workaround needed.828source/header/tool/SDK
pre-discovery identities; actual .d and Darwin linker dependency_info records
complete874consumed dependencies, unchanged before/after execution. Supplement
records its own new wrapper dependencies separately. Exact commands/environment/
compiler/source/header/wrapper/runtime/object/link inputs and results retained.
No unconsumed main.cpp/candidate-tool/controller source snapshot.

Actual complete original corpus results (each original vector once):

| Target | Vectors / batches | Result | Complete output SHA256 |
| --- | --- | --- | --- |
| T083 frozen envelope wrapper |13482 /53|PASS|741c8cb36d9b002cd72ecf955b527de4913d5333ac6c5ef9aa94e7f7e62163e3|
| T084 frozen map wrapper |9639 /76|PASS|7580f9b1ed9565f8a9145cf1062a04fc148e01f4b044fc8c2eecf89c45787062|

Every actual byte/field/error/canary outcome directly compared with the original
golden AND retained full native AND retained full Wasm stream before accepting
each batch. Hashes summarize those full byte comparisons; no golden regeneration,
corpus trimming or oracle modification. Original independent geometry/golden
semantics remain those frozen in T083/T084; T093 adds actual sanitizer execution.

PASS — Additional owned native map tight allocation replay9636vectors:
9635selected vectors/76batches, plus one previously unallocated valid65537-cell
case at original index23 in one supplemental probe. Exact input[declared] and
FlatCell[capacity] new[] buffers with true ASan ends; input immutability, every
allocated output byte, metadata guards/fields and full failure preservation
compared to the guarded original reference. Oracle-visible bytes unchanged;
any mismatch clears the existing canary flag. Production decoder unchanged.

Initial owned fixture cap65536 excluded four scalar cases. A second separately
owned copy changes ONLY fixture ceiling to65537 to cover the feasible case;
actual65537cells allocated/65536decoded, output exact original oracle/native/Wasm.
It reuses unchanged instrumented production object. No original full corpus or
original tight pass retried. Distinct source/plan/dependencies/result retained.

Three UINT32_MAX-capacity cases (indices9,17,25) remain outside bounded heap
allocation. They ran in the COMPLETE original scalar/reference corpus. No claim
that those static-buffer probes provide a valid UINT32_MAX-cell caller allocation;
no such allocation was attempted. Tight replay scope explicitly9636, not9639.

PASS — Instrumentation controls each compiled/run ONCE <=10s:

- ASan intentional one-byte write past8-byte heap allocation: actual
  heap-buffer-overflow/right-redzone/source-line report, SIGABRT(-6), reaped,
 0.4713s. Raw diagnostic2155bytes retained.
- UBSan intentional volatile INT32_MAX+1: actual signed-integer-overflow/source-
  line report, SIGABRT(-6), reaped,0.3916s. Raw diagnostic445bytes retained.

These intentional failures validate reporting; no production sanitizer finding
occurred. They are owned standalone control faults, not game memory corruption.

PASS — Bounded selector-based stdin/stdout/stderr capture, exact expected-size
stdout ceiling,1MiB stderr ceiling, explicit overflow/timeout kill/reap path.
Batch bounds256envelope/128map,<=60s; complete module<=900s. All206actual corpus
child invocations succeeded/reaped, empty stderr, no overflow/timeout/cleanup
issue. Max actual corpus child0.331271s. Original module elapsed4.1417s envelope,
6.5527s map; tight stream10.1511s plus supplement0.3313s. Timings are test evidence,
not game/performance acceptance.

PASS — ASAN_OPTIONS=detect_leaks=0:halt_on_error=1 and
UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 exactly retained. Clean environment,
task-owned TMPDIR/CLANG_MODULE_CACHE_PATH. Scoped escalation only as released.
No custom suppression/altered memory checks, runtime mixing, new dependency,
download, SDK/global/toolchain mutation, services/network/browser/server/game,
source repair or automatic retry. Original Apple17 timeouts and prior evidence
remain historical/immutable. All19MAIN pins/all874consumed dependencies and own
recorded inputs unchanged.

NOT RUN — Leak detection (explicit existing option disables it), whole-game or
native-engine import/render/capsule/navigation, app-message body semantics,
gameplay/balance/human/eight-player and complete P0/P1/MVP gates. Sanitizer corpus
success covers the exact approved portable subsets/cases, not general formats
or an unbounded safety proof. No phase gate waiver.

## Evidence / reproduction / frozen identity

Review [README](../../tests/outbreak/sanitized/T093/README.md), inspection-plan/
result, execution-plan, dependency-before/execution-before/after, actual .d/
.link-deps records, negative-controls.json with raw reports, all raw batch
commands/stdout/stderr/results, complete original output files, map-tight result,
tight-extra result and final-verification.json. Original/native/Wasm/golden files
stay read-only at their MAIN-pinned locations. Do not rerun exhausted one-shot
entrypoints or old drivers; repeat/correction requires a new MAIN release.

terminal-freeze.json pins1030new source/harness/plan/dependency/object/binary/
debug/result/output/provenance records, excluding itself/this handoff and named
ephemeral task tmp/clang-cache. SHA256:
d00c184bb9a8bdcbc51c5260e577c659676130709abf35a1b716da55579401a9.

- Original execution result:e6f81aca4382cb72658f3bf0aa1187d1b5a195bef3fd380b6e8870e51f07f953
- Final aggregate verification:8894b61e947b7661a464f1bdfcfcaffc5501c763fed72a41fca3d42a3631f407
- Provenance:c838c372fa0e76416c0e04b727729108dc30ea501d0e60d62aef1a1d7551b2ce
- Tight supplementary result:ad1e777755f71add85b215911a202996af1a42fcf630171c8e3f9ace7fa72bd5
- Tight9635 output:ef36e9e42f8e95267104314c5db3bbf006341a27c09606ae96adb37c1a56dfd0
- Capacity65537 output:ae66c24392622f4140acd87a0f52c8450e81ff6cda9eb98cb6735cbdccdb5255

## Implementation status / integration and questions

Actual isolated ASan+UBSan execution and controls complete; no simulated codec
substitute or production change. No unresolved source/corpus/sanitizer/cleanup
fault; no new question or repair request. Submitted frozen for MAIN review and
acceptance of T083/T084/T093 scope only. No integration or phase acceptance made.
