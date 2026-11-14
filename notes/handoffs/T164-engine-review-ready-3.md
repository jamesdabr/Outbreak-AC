# T164 Engine command-persistence correction review-ready handoff 3

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket: T164 revision1.2, focused source/preparation correction D236/D238; foundation BLACKWOOD_BUILD_PREPARATION0.1/D224, T163/D223, T148 and D235 unchanged.
- Status: **REVIEW-READY, NOT ACCEPTED OR FROZEN; NO ACTUAL EXECUTION AUTHORITY.**
- Base: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work; no Git command/mutation or clean-tree claim.
- Source writes: only web/build/blackwood/{recipe.py,test_recipe.py,SCHEMA.md,README.md}. Other four source files, all earlier passes/baselines/indices/handoffs remain unchanged. New evidence is pass-9, review-ready-3.json and this new handoff only.
- Commit/patch: none authorized or created; stable byte identities below.

## Focused correction disposition

Read T1641.2, D238 and `notes/reviews/T164-operation-persistence-deadline-review-1.md` SHA2562473b4628c37258fa7b80665626df36f1596ebd1c90cb00a7d2a0072da505ff9. The confirmed defect was normal child-log persistence starting after known command expiry and continuing write/flush/fsync without the original cutoff. MAIN additionally clarified that raw release must itself begin before that same cutoff; expired releases must remain unresolved, not gain a cleanup grace.

**Implemented; guarded actual-method evidence PASS:** Effects.run passes hard=min(original command start+120, original attempt start+3600) to the exclusive persistence helper. It starts no log persistence when already expired, including a late supervisor-receipt preparation return. The actual helper checks cutoff before open/chmod/fdopen/every short write/flush/fsync and after each return before any next effect. It uses unbuffered raw I/O with closefd=False, preventing buffered close from starting hidden pending writes.

Raw-object and descriptor releases are independently eligible only while the original cutoff remains. A late release return blocks any next release. Expired/skipped releases are SKIPPED_EXPIRED_UNRESOLVED; strong raw/FD and process/selector references are retained in a private in-memory ownership registry until process exit. No ambiguous close is retried. Existing supervisor selector/pipe release paths obey the same eligibility check, preserving their independent error/skipped facts. Accepted normal operations require actual completed releases before cutoff. Interpreter/OS exit cleanup is not claimed as command-budget proof, and no universal kernel-call preemption is claimed.

PersistenceRefusal retains cutoff, initiated actions, eligible/skipped releases, returned partial-write counts, known-prefix hash, unresolved write return, flush/fsync/release/error/late facts. Failed log identities are qualified; unknown retained identity is not presented as a complete log hash. Child raw-prefix byte/hash facts survive even when no log is created. Successful COMMAND.elapsed_ms is sampled after persistence and eligible release returns rather than before them; late returns refuse and do not start another child-phase mutation. Supervisor log frames remain pre-persistence snapshots, while the outer COMMAND receipt reports retention-inclusive outcome/timing.

A separate actual producer preserve_failure path may write only the exclusive FAIL result ledger under the remaining ORIGINAL attempt start+3600 cutoff while failure.json dominates. That cutoff reaches every ledger persistence substep. Whole expiry skips the ledger; late ledger I/O prevents subsequent flush/fsync/close. It never resumes child-log work, emits usable success or grants a fresh budget. Outer ledger facts are retained separately in memory on the failure exception, without adding RESULT/COMMAND fields or files.

**D236 remains covered:** final receipt canonical bytes, ordinary single-link0644 identity, observed-identity rechecks, requested presence and final marker checks remain implemented. All14 late receipt-race leaves pass unchanged. No other API/schema keys, flags, tool commands, gameplay/interface values or caps changed.

## Guarded current pass and meaningful new scenarios

Inspected command: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/build/blackwood/test_recipe.py`.

`tests/preparation-1/pass-9` reports **PASS_GUARDED_PREPARATION_ONLY** in64.110117 seconds: **124 top-level groups /214 executed leaves**. The count is120 individual groups plus four matrix groups containing26 adapter,32 supervisor,14 receipt-race and22 persistence leaves. The128 cap applies to top-level groups; each exact matrix list is pinned before new imports. No negatives were dropped and no cap was increased. This single fresh pass followed the D238 source correction; no unchanged retry occurred.

The22 persistence leaves invoke actual Effects.run and actual FileSystem.write_new with fake process/file/clock primitives. They cover already-expired creation (zero I/O), late receipt preparation (zero I/O), late open/chmod/fdopen/write/flush/fsync/raw-close/fd-close, write/flush/fsync/release errors, a seven-byte partial write returning late, short-write success, and retention-inclusive success timing. Every recorded I/O/release starts before its applicable cutoff. Late write has no subsequent flush/fsync/close, late flush has no fsync/close, late fsync has no close, and late raw close has no descriptor close. Skipped ownership remains unresolved and success is refused.

Three leaves exercise the actual complete producer exception/outer-ledger path: (1) child operation expired at its original220 fake-clock hard end, then a separate FAIL ledger succeeds under original whole3700; (2) a late child return exceeds whole3700 and no ledger I/O begins; (3) outer ledger write itself returns late and performs no following flush/fsync/close. The refusal marker remains in every case. Fake late-return clock jumps are deliberately out-of-budget FAIL observations, not actual waits or changed thresholds. Successful retention timing includes80ms of fake persistence steps, proving the earlier pre-retention stamp is gone.

The original positive graph still exercises61 genuine ordered unit names,125 simulated commands,84 actual copied public-data slices/411990 bytes and exact17-file bundles/notices with actual orchestration and independent verification. All runtime/audio/model/multiplayer/authority/P0 claims remain false, and fixture receipt status remains FIXTURE_ONLY. No actual source compiler/object/tool behavior is inferred.

Pass9 retained3873269 bytes and187 captured stdout/stderr bytes, within the unchanged300s/128-group/4096-virtual-node/8 MiB captured-output/128 MiB fixture caps. Future build3600s, command120s and per-command log8 MiB maxima are unchanged. Guards before new imports deny real child/process/control/signal/wait/uname/compiler/Node/version/signing/network/SDK-copy/ctypes/old-project-import effects. Actual-method process and raw-file primitives are fictional; only the preparation driver writes its own bounded evidence files. Real children/tools/SDK copies/network/FFI: zero.

## Exact current source identities

All eight current files are ordinary single-link mode0644 and match pass9 snapshots/result pins. Only the four leased files changed from pass8.

| Repository path | Bytes | SHA256 |
| --- | ---: | --- |
| web/build/blackwood/README.md | 6926 | `89bf8ba9b463f6aac630616dd7e17c4a4e4264b1c8e37fb489135d22eafdb4a0` |
| web/build/blackwood/SCHEMA.md | 21265 | `40f2b969ef6e03ba4ef30e2d6f7e8c54de0d749781c766ba853d44f84e678a32` |
| web/build/blackwood/build.py | 342 | `4c195f205d2947d821834de19e852b0b5d3911e9d26c9a782bbc5fb4e883bb99` |
| web/build/blackwood/config.json | 1558 | `10aa1033b0830efff51b1b4bdbb3fab9479efef453e380f7e2bf5532d4f464fb` |
| web/build/blackwood/recipe.py | 86557 | `914e6ab78db81b344accbdab7d2c815a66f0143197c8aaa9533e237bcf20baec` |
| web/build/blackwood/shell.html | 2012 | `6fccbeb1094a4f09998db25b123d2b9287b75da013f80d6e72a0444efa751399` |
| web/build/blackwood/test_recipe.py | 74079 | `ca11112cf67d5b91afadec43fdf68d061487fdba39b8e7eef8ac0b45108d54f6` |
| web/build/blackwood/verify.py | 339 | `506f52fcd76548ae8aef46043de9256e83d5d621343f074da843818933ada3eb` |

## New index and immutable history

`web/build/blackwood/tests/preparation-1/review-ready-3.json`:57411 bytes, SHA256 **3b07ca937f69e88b29f470efe6f250d73096a0cd7b51b0192823ad7da2bb9b5c**. It indexes254 pre-index fixture files/23648954 bytes, all eight source identities, current T1641.2/D224/D235/D236/D238/review controls and both historical handoffs/indices. It is a review index, not a freeze; only its own recursive hash is excluded.

| Pass9 evidence | SHA256 |
| --- | --- |
| plan.json | 6f130a9d8ce537633c03002b163d3e60460b1bc027681a883972aa1e9d4b5b9c |
| result.json | 08e7a4b7e70617629ad8aa4ddd2b9a4a86522585ed5f8bc7bf9220de3ebd51e9 |
| cases.json | f9d158127f2145e8b27ba12bb2a79e0994e9c42447796168f8347761953e6e02 |
| guard.json | 2a92d0ead07d3ac6481cafa479972f4d1f72de20d16bb2bf7f5a2c8f6513acc2 |
| protected-before.json AND protected-after.json | edb429d12dff40f706678a089953ca40f341b85a9996a44014ade340c4377b8a |
| positive-graph.json | 569fb34ca38616385a376b8421d6dd2618865e271f061087c01d2ac50fed514a |

All222 prior pre-index2 fixture files plus index2 (223-file union), both old indices, both old handoffs and four read-only current sources were rehashed unchanged. Index1 remainsfc3e82116bf8d0671c61c7c4ae44b78d7cad3179bd27e47278a535b2c371a3c1; index2 remainsf456288f7522629e9a687a3fbe72ea1cc70435902a0d26d8b883842953f4d0d4. Handoff1 remainsab8f9ec076e0e8a3da5d17f272d0bc81680b586e7aa0ae78f020333c85cd79ff; handoff2 remainsf45c60c13896d990120045a3a61f205549a280fdd1308eb4649f85ee40b34108. Earlier control pins are historical; none was rewritten after ticket revisions. All failed passes/source snapshots and earlier positive evidence remain preserved with their limitations.

Retained per-pass measurements:

| Pass | Recorded elapsed seconds | Retained fixture bytes | Retained captured-stream bytes |
| --- | ---: | ---: | ---: |
| pass-1 | not recorded | 284636 | 0 |
| pass-2 | not recorded (~342.4 file-time interval) | 2038213 | 187 |
| pass-3 | 302.632712 | 2067095 | 187 |
| pass-4 | 298.002146 | 2072247 | 187 |
| pass-5 | 59.441476 | 2084640 | 187 |
| pass-6 | 59.888614 | 3592451 | 187 |
| pass-7 | 61.181691 | 3622051 | 187 |
| pass-8 | 63.884902 | 3634144 | 187 |
| pass-9 | 64.110117 | 3873269 | 187 |

Historical unrecorded timers remain unrecorded. The pass2 file-time interval is approximate, not a repaired timing result; pass2/3 over300s remain disclosed failed evidence. Failed captured bytes refer to failure.json stdout_stderr; successful capture refers to stdout-stderr.bin, excluding external runner tracebacks. Original handoffs retain full historical failure explanations. No actual-engine performance inference follows from pure test timing.

## Incomplete work and review stop

No actual current-project plan/build/verification, compiler/Node/SDK-copy/library resolution/native wait/native build/staging/signing/default-dev regression/admission/controller/server/transport/browser/pair/runtime was run. Underlying Darwin WNOWAIT behavior and real persistence/cleanup timing remain UNPROVEN. Actual attempts/, candidates/ and the MAIN-owned blackwood-source-manifest.json remain absent/unwritten. No shared source/interface/authority/control/asset/tool/cache was edited; no new dependency, public selector or process command was added.

Ticket1.2/D238 and the unchanged approved foundation were checked for submission. D236 and D238 are addressed in stable source and guarded evidence; MAIN alone reviews, clears acceptance/freeze and releases any actual successor. QA/T149/runtime/RSS/full-phase/performance/human holds remain. This handoff stops work for MAIN review, without a freeze or further test retry.
