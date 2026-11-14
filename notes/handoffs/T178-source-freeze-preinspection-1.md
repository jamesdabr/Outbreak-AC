# T178 source freeze and two-job preinspection

- Worker: MAIN delegate /root/review_native_candidate
- Ticket/revision: T1781.2 RELEASED D272; closure0.3/D269/D271; default-dev preparation0.2.
- Base: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved overlay. No Git used. All six baseline source hashes verified against MAIN manifest da4be7392462c33bfd8bc4bc6e1b59c1616f602792dd96de52671b46a7210e99; immutable pre-edit copies retained under focused preparation. Wrappers unchanged.

Only production differences are strict consuming helper and its Effects.run call. Source AST/diff inspected, no project execution yet. The helper checks original handle/PID/uncached state each observation, exact nonbool raw wait tuple, terminal status, consumes no other PID and marks ECHILD lost. Returncode and parent_reaped publish before post-call clock. Unchanged hard=min(commandStart+120,wholeStart+3600),work=hard-5;6000 observations and clipped0.01 pauses are extra bounds. D263 producer/reader, D235 FFI, D236 receipt and D238 persistence code remain unchanged.

Focused harness inspected: sixteen fixed cases exercise actual Effects.run and helper with fake boundaries, assert raw facts/truthful state/no late follow-on effect; Popen.wait/poll refuse. Guards are installed before recipe loading; six denial selfchecks cannot perform real effects. Full harness retains exact228/247 names and prior assertions, adapting only consuming fake boundary and new immutable invocation bindings. No old driver import or real OS/tool/native/SDK/build/runtime effects. Each job independently300s/8MiB output/128MiB retained.

ALL seven sources now frozen before the first invocation. Exactly one focused job, only its PASS permits exactly one full pass11. No source changes/repair/retry/overwrite after invocation. Both PASS permit only inspected pending final3 data; failures preserve and stop. This note records preinspection, not observed test success or acceptance.

Frozen source SHA256:

- web/build/dev_regression/recipe.py 7a4dd4f5555a23a96623d4d5c09d431e51220bdd6a1180467416e531d184dd4c
- web/build/dev_regression/build.py 1e47f5fed2ea414405f1ad816e0aae7007bb41d4165cb553225fee2788209a7b
- web/build/dev_regression/verify.py 3ec91f59208df47eded9d931d8a39ffd0f476a156312bd2312afdad94506c549
- web/build/dev_regression/SCHEMA.md 19026aced80b5cf8591bcad06f75b25fd84c7e3a71ad183ca7e3d57c2b5614c4
- web/build/dev_regression/README.md f440d57f954d5323c5c636e9aceddd44d8c0e07d7b22e3ebdcbaab017d3f0d2c
- web/build/dev_regression/test_recipe.py 705edf60dd7d80428f80e86a0950ca82ee577021daca82921d5a1d498fa3a140
- tests/outbreak/builder_reap/T178/test_reap.py 45555e8a764d1902c38a7dcd95b2b739d28a68b73f5b63fc1d8b59678a506167

Authority SHA256:

- tickets/T178.md 88342bce3681d3067c12f4f3a17393b342a5cb2027baa855309b267ca1b3462a
- MVP/DEFAULT_DEV_BUILD_PREPARATION.md c6b2ddd4b4dd87050066b93fbe114504c27b75a162f93bebf24f52c306b28ec9
- MVP/BUILDER_TERMINAL_GROUP_CLOSURE.md d4b08c04953bd57986966318ce74b4dc1fcdbcd0fa2a5a842927f278a07d5515
- notes/decisions/D263-builder-terminal-group-corrections.md 945643e12d63ecd39e45cd2b25ae348eec57612ffe0b102546f07a8d62c50e55
- notes/decisions/D269-strict-original-reap-builder-correction.md 567944dc27da881e589cdeea8b6116995447b1547d55a48f231f10feeb594b19
- notes/decisions/D271-builder-original-cutoff-clarification.md fdc5dbb3c74be47fd163d7c4bfad5b59499623c5fd2db40e5f3dbb0bf44e1420
- notes/decisions/D272-default-dev-strict-reap-release.md 5e93cfc44e6f503e5ad6cc37951bf9fa0962573e3093a91ede4e5b742549e72c
