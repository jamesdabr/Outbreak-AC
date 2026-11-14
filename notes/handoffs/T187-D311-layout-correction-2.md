# T1871.2 D311: exact private layout source correction

- World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Authority read: T1871.2, D311, G2_FOUNDATION0.3/D309, D307 exact-head amendment; T193 final rejection handoff read as historical evidence only.
- **SOURCE CORRECTION ONLY / NO WORLD COMPILER, PARSER, TEST, GENERATION, ORACLE, SDK, FFI, QUERY OR RUNTIME EXECUTION / NOT ACCEPTED.** Full Q/R package remains in construction.

## Stable production bytes and exact changes

`source/outbreak/p1_geometry.cpp`: **74884 bytes / SHA2565163a100e558022cc26e3e9693a470677e5a3b79570d68a12c0961ae457b0cb8**.

Only D311's named private production blocks changed:

1. QSlotRefs now has `query_wide::Int<N> (*const lower)[32]` and matching upper. Its indexing returns `index<32?(*lower)[index]:(*upper)[index-32]`.
2. Existing QueryWork control aggregate binds `&lower,&upper`, taking pointers to the actual two typed32-element arrays.
3. Added standard-layout assertions for QueryWork8/16 before offsetof and retained all original offsets/768 assertions, now explicitly including staged0 and all phase offsets for BOTH modes.

No production query behavior/body, G1 line, owner array, attribute/flag, packing, suppression, header, dependency, work/width/status/cap or public record changed. The diff against the failed source contains only those three exact changes. No other production correction is inferred as authorized.

Before editing, current production was verified equal to T193's failed74169-byte /0d999988280531d74ded6bfa27ae35e032233886267ddb1deb5def276cc4bf3b input. A NEW own raw-text source snapshot at `notes/proposals/T187-T193-failed-source-snapshot-1.md` preserves exactly those bytes/hash; it is data for a standard diff, never a compiler/project input or an edit to T193 evidence.

- Exact failed-source diff: `notes/proposals/T187-D311-layout-correction-diff-1.md`,2962 bytes/SHA256e9a35e71d54bf988f0cb2a2749fc6bd7ffa7188d2e5132112ae4cd87d8bc9c6b.
- Exact accepted-prefix diff: `notes/proposals/T187-production-source-diff-2.md`,44815 bytes/SHA2569e1caa85500c68c4f1c9d941af1ed77c6718aff090f85f01f58f1a1768cd8bc1.
- Read-only `head -c 31382 source/outbreak/p1_geometry.cpp | shasum -a 256` still gives accepted c232100352425092561f6fc9701c77db17f643893510fde780839db21be17d21. Old source/diff/progress notes are preserved, not rewritten to claim corrected success.

## Storage/lifetime/source-role ledger

The actual owners remain lower32 in q_lower and upper32 in q_upper, synchronously alive across q_body and descendants. Binding pointers are const, point to complete actual arrays, and do not escape the stack lifetime. Dereferencing selects that array before indexing; there is no cross-array pointer arithmetic, copied/third bank, nested public query/bank, heap or store scratch. Work copying/moving stays deleted. G1 Work70 and reference bindings remain untouched.

Logical G2 still has64 accepted Int8/16 slots: each real owner1152/2176 bytes, combined slots2304/4352. QueryWork remains declared/asserted768, giving totals3072/5120. Nonwide offsets are staged0, candidate160, walker240, conversion368, tags464, pose_indices528, counters536, Fault600, feasibility608, control/slack640, end768. Both standard-layout traits and every numeric offset now have explicit source assertions for both modes. Const typed pointers do not establish native/Wasm representation or emitted fit by assumption; future separately released checks must evaluate these assertions and later full emitted proofs must charge both actual owner frames and all control/scalar/helper costs.

The R and in-progress Q verifiers' **new** current-production source pins, exact binding-literal checks and source-frame operator anchors were updated to this current source. Their source maps still require the same three private prototype/definition joins, real32-element arrays, direct matching upper/body calls, standard layout, deleted Work copying and every old/new public-root/normal-callee proof. This is current-source rederivation in new harnesses, not rebasing an old accepted or failed proof. No R/Q verifier or fake control has been imported/run. Their current construction hashes are not frozen by this layout-only handoff.

## Historical failure and boundary

MAIN's D311 records both original T193 frontend calls rejected exit1 with nine invalid offsetof diagnostics each,10218 bytes total, all334 bound inputs unchanged. This handoff does not replace that failure, claim a passing syntax result or authorize a retry. No compilation was performed by World. MAIN must separately name/release any corrected-source frontend operation after reading this stable source/hash/diff/lifetime correction.

Q construction continues in its disjoint allowed five files. D307 is read and the intended literal equality ID is12544 (existing root/head allocation), with h4080 literal seed and independently certified permitted variants; h3738 nearby/rounded-disagreement rows and both default heights remain. Exact IDs/certificates and complete Q/R sources will be reported in a later full source handoff. No full source-package, generated-catalog, native/Wasm semantic/frame/caller/browser/performance/human/Player/QA/T149/MVP acceptance is claimed here.
