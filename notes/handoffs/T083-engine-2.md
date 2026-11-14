# T083 D080 continuation handoff — native passed, sanitizer incomplete

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket/revision: T0835.6 RELEASED; D079/D080. No self-acceptance or ticket change.
- Phase/contracts: PORTABLE_FORMAT_FOUNDATION0.1 section A; existing governance/browser/P0 subset0.5; numeric0.1 unchanged.
- Base/pre-existing edits: shared checkout preserved. Original attempt-1, failed direct compiler command, partial handoff and Wasm evidence untouched. No clean-checkout assertion.
- Changes: approved one-line verify.py native launcher correction; NEW verify-before-D080.py backup,native_only.py,README-D080.md,attempt-2/** in tests/outbreak/envelope/T083; NEW notes/questions/T083-engine-sanitizer-timeout.md and this handoff. Production envelope.h/.cpp and all accepted fixed source/evidence unchanged.
- Commits/dispatch/source integration: none. No contract/status/other source/tool/SDK/artifact/pin edits.

## Acceptance evidence

| Criterion | Result / evidence |
| --- | --- |
| D080 exact native launcher correction | PASS: /usr/bin/clang++ inspected/hashed/versioned before invocation. Unchanged C++11/O2/Wall/Wextra/Werror and sanitizer flags/env. Original driver backed up; attempt-1 evidence preserved. |
| Actual native full corpus | PASS: native_only.py executes actual attempt-2/native on13,482 unchanged vectors in53 batches<=256; zero per-case mismatches, complete output retained. native-result.json/native-complete-plan.json/logs/native-complete-* substantiate actual source, binary, env and every batch. |
| Native versus SAME production-source Wasm / independent oracle | PASS: native-complete.txt byte-identical to attempt-1/wasm.txt and expected.txt. Rebuilt attempt-2/envelope.wasm byte-identical to original binary. Full Wasm runtime evidence retained in attempt-1; attempt-2 additionally executed first256 Wasm vectors before sanitizer timeout. No fresh full Wasm runtime claim for attempt-2. |
| All section-A boundary/malformed/canary cases | PASS native+retained Wasm: unchanged13,482-vector independent Python struct corpus, all declared lengths/truncations/capacities/types/flags/IDs/endianness/error priorities and8192 seeded random cases; full fields/destination/guard/object-failure checks. Ordinary native also repeats exact-size allocations; no fake codec. |
| ASan/UBSan compile | PASS: actual installed combined sanitizer build exit0, no new flags/runtime/header changes or suppression. Exact planned command/log/runtime hashes retained. |
| ASan/UBSan execution | INCOMPLETE: first256-vector batch timed out at60s; driver exit1/TimeoutExpired. No retry. Empty sanitized.txt is not passing coverage; startup cause unproven. See sanitizer-timeout.json and OPEN question below. |
| Source/game/fixed/artifact/cache/SDK preservation | PASS:32,575 original protected identities unchanged in native continuation. Original corpus/oracle/Wasm binary unchanged; production source hashes unchanged. Membership inventory is not independently repeated by continuation. No unrelated controller/candidate tests consumed or snapshotted. |
| Formatting / scope | PASS: git diff --check exit0; only allowed task-local/note writes. No game/browser/native server/network/service/install or current build integration. |
| Full body/app/protocol/map/authority/P0/P1/performance | NOT RUN/outside release. Header validity grants no application meaning or admission. |

Executed from /Users/jd1/code/apps/outbreak:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/envelope/T083/verify.py --attempt attempt-2
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/envelope/T083/native_only.py
```

First command: build/link succeed, sanitizer runtime timeout/exit1. Second:
exit0,native_cases=13482,batches=53,failures=0,changed_protected=0.
macOS26.5.1 arm64; AppleClang17.0.0 via approved launcher; SDK7.0.0/compiler
777e6e5.../Clang+LLD24 and Node24.19.0; Python3.11.9. Exact identities/flags/
clean env in plan.json and execution logs. No performance/hardware claim.

SHA256 unchanged production:

- envelope.h:5a9ed4462b5c3fdcb61fced19293b335c4ea12994d8b8bb9f89584d3598b6168
- envelope.cpp:2c0bff1bbc6d1a03eea3e5bba59b6bb0ae8684b41f86f22c7ebe3523df2337dc
- corpus:11a86a820b5ebed0b362a1178c87921bceb72acff4d0d0f0990675cf5f1b0e0b
- independent expected/full native/full retained Wasm outputs:741c8cb36d9b002cd72ecf955b527de4913d5333ac6c5ef9aa94e7f7e62163e3
- actual native:6f428e43365c5824f6473d2476812f16b80c9c41984302a64babcfbc2cf87777
- pending sanitizer executable:0031b161c71c66ba8340fc4312dc16f98fec83b72e5fbf3272ab092a9fff8968

## Implementation status

Envelope implementation unchanged and verified native+Wasm for the full frozen
corpus. Numeric source unchanged. This handoff supplements the preserved first
handoff; it does not rewrite its compile failure or imply sanitizer acceptance.
No production/body/wire API change, dependency or game behavior added.

## Integration and questions

D080 resolves original native header-discovery question. New OPEN question:
notes/questions/T083-engine-sanitizer-timeout.md requests one60s identical-command/
input/env/executable sanitizer retry outside default process sandbox using
platform scoped escalation. If successful, finish unchanged bounded corpus;
otherwise stop. T084's separate permission is not generalized to T083.

Python3.11.9 subprocess.run POSIX timeout handler was inspected: kill then wait
before reraising. No actual child exit code persisted. Independent pgrep check
failed (sysmond service unavailable), so no extra process-list cleanup proof is
claimed. No sanitizer retry or boundary change has executed.

New evidence and source remain frozen pending MAIN's narrow resolution. T083
gate remains incomplete until genuine sanitizer coverage; MAIN alone accepts,
resolves questions or releases further work. No phase gate waived.
