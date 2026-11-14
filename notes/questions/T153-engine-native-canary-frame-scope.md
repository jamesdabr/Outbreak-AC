# T153 native compiler canary edge and helper-stack proof scope

- Author/worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket/revision: T1531.0, RELEASED isolated arithmetic D190.
- Contract: QUERY_ARITHMETIC_FOUNDATION0.1, compiled complete helper-chain<=2048bytes; unknown diagnostics require a question, no flag/cap change or retry.
- Status: OPEN; MAIN resolution recorded separately.

## Question

May the helper-chain certificate explicitly exclude the compiler's canary-failure abort edge under the existing valid-storage/no-concurrent-mutation C++ call preconditions, while retaining it as an unmeasured fault path? Or does MAIN require a stack bound for that external system abort routine too? No exclusion/zero charge is adopted by this question.

## Evidence and impact

The ONE T153 attempt passed all5912 rows against independent Python integers/isqrt on actual native and Wasm, with exact outputs and unchanged protected inputs/tools. No compile/test failure/retry. Source/driver remain unchanged after the attempt.

Object and same-O2 diagnostic .su files match exactly; all emitted helper calls are statically resolved, no recursion/indirect calls. Normal known native chain, conservatively INCLUDING the test dispatcher: run384 + round_div<16>432 + divrem<16>304 =1120bytes; helper-only max736. Wasm linear ABI chain is288+208+224=720; helper-only432. Additional conservative charge of all declared Wasm locals gives1044bytes along the same path; it is not Node/JIT physical stack attestation.

Native mul<8> and mul<16> each contain a compiler-generated call to ___stack_chk_fail. Its frame is not emitted in our .su; it is a system-library abort path, not another source helper. Retained native-diagnostic.s:1671 and corresponding second occurrence are both recorded in attempt-1/frame-analysis-1.json. No external callee was silently charged0. The analysis status remains NATIVE_TRAP_EDGE_DISPOSITION_REQUIRED rather than full stack PASS.

The source multiply's product[2*N] writes are at i+j<=2N−2 and i+N<=2N−1 for i,j<N; output/source Int objects are valid by contract, all loop bounds literal and inputs immutable during a call. No source operation writes outside these arrays or publishes before validation. This supports a valid-storage normal-path qualification, not a claim that arbitrary memory corruption/host failure cannot happen. No stack-protection flag, inlining/optimization or source/cap change is proposed.

## Options for MAIN

1. Recommended: explicitly accept the normal valid-call C++ ABI chain certificate, preserving both canary abort edges as out-of-model/unmeasured fault paths rather than0byte routines. Bind source array bounds/call preconditions, raw .su/.s and complete known graph. No new build/test needed for that scope clarification.
2. If the2048 ceiling includes the external corruption-abort routine, keep native full-chain proof unresolved and name the separately reviewable evidence method. Current installed compiler outputs do not contain its frame. Do not disable protections, install tools or widen a cap merely to pass.

## Work paused

Only unconditional native complete-frame acceptance and REVIEW-READY completion/freeze are paused. Arithmetic verification, retained evidence and Wasm linear-stack analysis are complete; a bounded evidence handoff can be delivered now. No further compile/run/source edits/retry or actual integration occurs pending MAIN disposition. QA/T149/actual RSS holds unchanged.
