# T105 actual native candidate stopped by SDK alias guard

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T1051.0 RELEASED / immutable D110 actual native build prerequisite. No self-acceptance/status change.
- Contracts: CANDIDATE_NATIVE_FOUNDATION0.3/D107, accepted private report/freeze/verification schemas; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5. Ticket/native contract/governance and clean-root source/README reviewed before execution; T105 re-read after terminal failure.
- Execution root/source: /private/tmp/outbreak-clean-D109-1, reviewed31d433b993d393b1902f7f57285a1d5ea6d2042d. Original repository and D106 clone remained read-only except these own new original-repo notes.
- Writes: only new clean-root web/server/candidate-attempts/ parent and D110-native-1/**, plus own new T105 question/handoff notes. No source/pin/manifest/contract/SDK/original framework/cache/library/old-evidence/Git edit, extra root log, branch, commit or dispatch.
- Outcome: **ONE ACTUAL BUILDER INVOCATION, exit1 / FAILED. Independent verifier NOT RUN; no native binary, full build or runtime acceptance.**

## Exact execution and identities

Used fixed existing Python3.11.9 with -B, disabled ambient PYTHONPATH/PYTHONHOME/user-site and preserved the builder's fixed child Runner environment. From /private/tmp/outbreak-clean-D109-1, exactly once:

```text
env -u PYTHONPATH -u PYTHONHOME PYTHONNOUSERSITE=1 /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/server/candidate/build.py --execute --candidate-id D110-native-1 --pins /private/tmp/outbreak-clean-D109-1/notes/decisions/D110-candidate-native-pins.json --pins-sha256 65a6d2f8f3e93d6efc5d2d6f28be2595675e2c4039043fafa03db04dd745a463
```

Initial local read-only checks matched exact pins digest, common manifestdf64341ac627b84625909beb65f293c434573453b50ecc7452fba6916c469fda, reviewed stage/build/verify hashes and absent attempt/container. MAIN pin review supplied1809 inputs,817 SDK files,96 framework members and893 source entries. No authorization/plan/observation/pins regeneration was performed. The live exec session36346 was polled to authoritative exit1; no observation yield caused a restart.

## Actual evidence versus uncompleted work

| Criterion | Result |
| --- | --- |
| Actual admitted fresh attempt and fixed installed compiler identities | PASS partial: source/pin/current gates admitted and reserved only D110-native-1. Both actual /usr/bin/clang/clang++ --version outputs report Apple clang17.0.0 clang-1700.0.13.5, arm64-apple-darwin25.5.0, InstalledDir CLT/usr/bin. |
| Fresh physical copied framework and ordered signing/inspection | PASS recorded partial: nested then parent copy signing; four copy-signature checks; two frameworks' file/dependency/load/signature/ad-hoc inspections completed. No original framework/library signing. |
| Fresh release/dependency/object work | PARTIAL: crypto.cpp pre-discovery/compile/post-dependency/file checks passed; one actual release object2e351b3cd1aaaa4ee63797e308f5d5792d765cdb76b938a4088df4dc894b3e36. Next release log.cpp discovery completed exit0 but its raw dependency alias failed the subsequent gate. No object reuse. |
|32 objects / two native links | FAIL/incomplete: one release object recorded, no log.cpp compilation, no link, no ac_server binary, no debug mode. |
| Current dependency alias gate | FAILED as designed for unsupported alias: SDK/usr/include/sched.h -> raw pthread/sched.h, mode0755, canonical SDK/usr/include/pthread/sched.h. Canonical target already pinned07d65b8d135be978a33579b5a333bd4576a8c6b36351ef510e0cca2aa0987020 in both ordinary maps. Native0.3 only permits pthread.h, so no generic alias waiver was applied. |
| Child-command status/bounds/cleanup | All22 recorded child commands exit0/group_reaped=true; timeout/overflow/kill_fallback allfalse. Failed overall status is the post-command dependency guard, not a compiler error. Step21 discovery elapsed51.586ms. Runner-recorded attempt elapsed3857.252ms; not a hardware/performance or total outer preflight timing claim. |
| Preserve failed terminal evidence | PASS retained FAILED report/freeze,22 stdout/stderr log pairs, both raw .d files for crypto, log.pre.d, object, signed copy and inspection outputs. Builder final preservation checks added no separate error. Read-only independent stdlib check matched exact153 owned terminal file/directory/link members, modes/bytes/hashes/raw link text. Pins/manifest still match. |
| Independent verify.py / NEW receipt | NOT RUN, correctly conditional on builder success. No verification/receipt.json exists; no manual receipt or accepted-artifact manifest created. |
| Runtime/full P0/MVP | NOT RUN: no resulting native binary launch, server/game/browser/gateway/socket/network, download/install or further tool/compiler/signing invocation. |

The build is actual execution, not fixture evidence. The preserved FAILED status is not promoted by successful partial command exits or prior52-test preparation. All runtime/authority/gameplay/multiplayer/P0 claims remain false.

## Frozen failure identities

All below under /private/tmp/outbreak-clean-D109-1/web/server/candidate-attempts/D110-native-1/:

- report.json SHA2562cbb59b820f290343ae4daa011a8b4e82de94e58c09ff1233a66188d0ba66c92.
- freeze.json SHA25626027a52829c5c8630e4c293b4bea8b3432f3da7a97fa67b67990146662340e2;153 terminal members excluding freeze/optional receipt.
- release/log.pre.d SHA256c4fd1b45db65f65e251d9b6633a1923197787c8e98d4cb097b115cfafd5786c3.
- logs/021.stdout and .stderr both empty SHA256e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.

Report steps retain exact argv/environment/exits/log digests; last step21 is -M discovery for log.cpp using canonical MacOSX15.5.sdk, not historical MacOSX.sdk. Read-only inspection of that retained .pre.d found the allowed pthread.h alias plus the rejected sched.h alias. No failure source/pin/log/SDK rewrite or retry occurred.

## Integration and question

OPEN notes/questions/T105-AI-Director-sdk-sched-alias.md records the exact contract boundary, raw/canonical path, target pin, failed step and options for MAIN. Actual build allowance is exhausted. New recipe/contract/source/pins/fresh attempt authority is required for any correction/retry; this handoff grants none. MAIN may review retained actual dependency aliases before a separately released correction, but no additional audit/implementation is assumed here.

No independent verification, native acceptance or later browser build is admitted by this failed attempt. All preserved source/prerequisite/partial evidence stays unchanged pending MAIN decision.
