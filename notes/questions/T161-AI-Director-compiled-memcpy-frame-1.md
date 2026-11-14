# T161 attempt-2 compiled normal memcpy frame is unmeasured

- Author / worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket and revision: T1611.2, one actual attempt-2 consumed; worker did not change status.
- Phase and contract revision: SPREAD_CONE_FOUNDATION0.3 / D214,D220,D225.
- Exact clause affected: complete same-optimization native/Wasm normal-callee frame proof<=64KiB; unmeasured normal callees refuse; accepted dependencies/source/argv/flags immutable; no repair/retry/extra invocation.
- Status: OPEN (lead resolution recorded separately).

## Question

Please dispose of the preserved actual failure and select a separately scoped proof/source path for the compiler-emitted normal memcpy callee. No source/flags/proof-policy repair or extra execution was attempted. This is a missing normal-callee resource proof, not a mathematical mismatch or corruption-abort edge.

## Evidence and impact

D225 actual release binding preparation-2/actual-release-1.json SHA2569bb03431b1d94f77384c94497122c9f7897434234723a3b5642c621f97836da2 was exclusively appended before the ONE exact approved invocation. Current driver SHA256681d035a0ec61f7a623c683a44a4911d886de6d06eefa57df01a0889f880675b was unchanged. The same returned process session17197 was polled to terminal exit1; no replacement run.

Actual verifier elapsed12.19965520792175s, combined child stdout/stderr0 bytes. All22 planned native/Wasm object/assembly/link children returned0; each original handle was reaped, owned-group absence observed, no primary/secondary/unresolved cleanup or guard expiry. Actual argv/environment/counts exactly equal the prepared22-command/48-batch plan. All97755 requests and3128160 independent expected response bytes were generated and match MAIN's pinned corpus SHA4e6fbf0e4a8ded92f2f1fcdc99804bc7c253477bd04dd4413ef7da25eb32c82a / expectedSHA017f5cfc3c6634fd1e7bf6a8fbc4fdccdae334029ab34f13c7d909f7d9c0f987. Actual copied owned sysroot, dependency closure, native/Wasm binaries and raw same-O2 diagnostics are retained in attempt-2.

The required pre-target frames() gate raised `RuntimeError('Unmeasured normal callee: memcpy')`. Native source evidence: attempt-2/native-rules-diagnostic.s line35, within accepted ob::rules_p1, emits `bl _memcpy`; line34 loads length268 into w2 for its staged canonical rules initializer. Caller .su frame is560 bytes, but this is NOT a bound for the external callee. No measured emitted .su/body for system memcpy exists in this compiled proof. It is reachable on normal valid sampler/half-angle calls and cannot inherit D196's corruption-abort exclusion or be silently counted0. Accepted p1_rules.cpp remains SHA913ce462a5c3896d766adc66751f278d188462ee6b3b97973269d976b3cf00b2; no accepted-source change caused this finding.

No native/Wasm corpus target, tool-version command or additional runtime executed: frames gate precedes them. native.bin,wasm.bin,frames.json,result.json are absent. Neither target's complete compiled-frame proof nor actual mathematical output/timing acceptance is established. The failed package remains failed, not REVIEW-READY success.

All protected-before/protected-after-failure records match exactly, including original attempt-1, complete prior preparation plus actual-release binding, accepted source/evidence/SDK/original cache. All release-bound authority/source/harness/docs inputs rechecked unchanged after terminal observation. No browser/game/server/network/install/Git, RNG/shot/state integration or extra fixture/driver invocation.

## Options for owner and lead

1. Release an exact normal-callee proof for the actual toolchain/runtime memcpy implementation, with full reachable ABI/live-frame evidence and unchanged64KiB ceiling. No guessed constant or blanket host-library exclusion.
2. Have the accepted rules-source owner prepare a separately authorized behavior-preserving initializer amendment with unchanged canonical fields/hash/API, then review/freeze dependencies and release a fresh bounded proof. Current worker cannot edit that immutable dependency or change compiler flags to manufacture a fit.

These are options only, not implementation authority. The remaining frame closure may expose additional issues after this first reported missing callee; no claim of sole blocker or complete Wasm proof.

## Work paused

No further actual execution, repair, source/harness/doc edit, retry, new attempt or freeze. All22 build/diagnostic effects and failure/partial proof remain preserved. Await MAIN disposition under current no-retry contract. QA/T149/runtime/RSS/full-phase/human holds unchanged.
