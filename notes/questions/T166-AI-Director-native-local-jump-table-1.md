# T166 native frame gate refused a wrapper switch branch

- Author / worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket and revision: T1661.2; sole D239 actual invocation consumed.
- Phase and contract revision: RULES_INITIALIZER_FOUNDATION0.3 / D231,D237,D239.
- Exact clause affected: complete same-O2 normal-call frame closure, indirect/unknown refusal, unchanged64KiB limit; failure preserves/stops without repair, retry or alternate entrypoint.
- Status: OPEN (lead resolution recorded separately).

## Question

Please dispose of the retained native frame refusal and authorize any further work separately. The analyzer reports `Indirect call:_Z11rule_scalarjbx`; retained assembly appears to show a bounded local switch jump table in the test wrapper. This observation does not override the failed gate or grant permission to change its classification.

## Evidence and impact

The one approved D239 command returned session12783, retained and polled to terminal exit1/REFUSE. No replacement invocation occurred. Under tests/outbreak/rules_initializer/candidate-1/attempt-1, FAILURE records `Refused('Actual compiled frame/zero-init gate refused (both partial graphs retained)')`. frames.json retains both graphs: native errors contain only the indirect-call report above, while Wasm errors are empty and its frame gate passed. Both actual zero-initializer/old-copy gates passed. All54 guarded fake cases and18 native/Wasm build/diagnostic/link children passed; all19 original child handles were reaped and owned-group absence observed. Four version children and both262-row corpus targets were NOT RUN.

In native-wrapper-diagnostic.s, function _Z11rule_scalarjbx begins at line976 and executes `br x10` at line992. It first compares w0 with69 and branches out of range to local LBB6_142. For admitted indices, it loads a halfword from lJTI6_0 indexed by w0, adds that scaled offset to local LBB6_2, and branches to the computed address. The table at line1840 has70 entries, each `(LBB6_x-LBB6_2)>>2`; read-only inspection found all70 target labels defined within the same function. The branch does not use the link-register call instruction. This supports the inference of local switch dispatch rather than a function call, but the current analyzer has refused it and the actual package remains failed.

Native diagnostic SHA256fd15561de23c80a0f39f0fd695562062a78f35b137ffea8a2a641c34c5661586; frames.json SHA25691c1c0ff9f6bf3c091a7d4f6c77285c2b0dc50d125a45476c6d26c62c90058d1. The reported native run sum2656 is partial failed evidence, not an accepted complete bound. No mathematical mismatch was observed because neither corpus target executed. The zero-init observations do not establish candidate behavioral acceptance or live installation.

## Options for owner and lead

1. Independently review the retained emitted control flow and determine whether an explicit bounded local-branch qualification can be accepted under a separately recorded proof scope.
2. Release a focused analyzer correction that distinguishes demonstrably closed local jump tables from unknown indirect calls, preserving unknown-call refusal and the64KiB ceiling, then review/pin a fresh proof scope before any execution.

These are options only. No flags, wrapper, candidate, harness or proof-policy edits were made to ease the gate. No blanket indirect exclusion or guessed callee cost is proposed.

## Work paused

All actual execution, repairs, retries, regeneration, alternate target/version invocation, source installation, consumer changes and freeze. Only the authorized new post-terminal notes were written after failure. No independent implementation remains authorized under the consumed D239 lease. QA/T149, T161 full proof, gameplay and human gates remain unchanged.
