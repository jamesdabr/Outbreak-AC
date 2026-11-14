# T031 D008 stable arm64 debug assertion header

- Worker: Engine & Multiplayer
- Ticket/revision: T031 0.6 with approved D008 additive revision 0.8
- Scope: exact architecture-correct ASSERT selection only
- Changed source: source/src/tools.h:16
- Stable tools.h SHA-256: `e53d32d55e5b81ac5e5be3e8a2411a8363dae858631f06cfd3ed11b16eef6fcf`
- Status: header edit complete; MAIN may relay this exact stable identity to AI T033. No further tools.h edits are planned under this amendment.

The `_DEBUG` builtin-trap branch now selects `__EMSCRIPTEN__ || __aarch64__ || __arm64__`. Other architecture branches and release behavior are unchanged. No server/game was executed and no other source was edited by Engine.

## Verification

Evidence: web/build/generated/t031/assert-regression.json, assert_fixture.cpp, assert-arm64.s and assert-x86_64.s. Exact commands/exit codes are recorded there.

- PASS: actual native arm64 debug fixture compiles/links and its true assertion exits 0.
- PASS: false debug assertion exits by SIGTRAP (Python return code -5); core dumps disabled for the isolated child. Actual server was not crashed.
- PASS: emitted arm64 assembly contains `brk`.
- PASS: emitted x86_64 debug assembly retains `int3`.
- PASS: release fixture exits 0 for both argument conditions, preserving release behavior.
- PASS: git diff --check.

This is an isolated assertion test, not server runtime or browser/game verification. T031 final Wasm rebuild/link waits for Player T034 stable source, then conservatively recompiles all 61 target units because tools.h changed. Earlier 61-object/link evidence is now stale with respect to the new header and will not be claimed as final. AI remains owner of its native build output and reruns affected objects separately.
