# T177 Engine strict original-child reap handoff 1

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket / revision: T1771.1/D269/D271, SOURCE + TWO DISTINCT GUARDED JOBS + CANDIDATE INVENTORY.
- Contracts: BLACKWOOD_BUILD_PREPARATION0.2, BUILDER_TERMINAL_GROUP_CLOSURE0.3, GOVERNANCE0.5. Accepted T164 baseline remains historical; preserved T174/R1 packet is not accepted current source.
- Base/pre-existing overlay: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work; no Git command or clean-tree claim.
- Changed files: only existing web/build/blackwood/{recipe.py,test_recipe.py,SCHEMA.md,README.md}, NEW tests/outbreak/builder_reap/T177/test_reap.py and preparation-1/**, NEW module tests/preparation-1/pass-11/** and final-3/{inventory.json,receipt.json,freeze.json}, own NEW question/plans/this handoff. Other four module sources/assets/SDK/tools/authority/history unchanged.
- Commit/patch: none authorized or made.
- Submission: **PENDING_MAIN_REVIEW; no correction acceptance, actual build or held-work release.**

## Acceptance evidence

PASS — preserved MAIN8-source baseline manifest ba722457ad9f005bd67de94ad3b56d9d5be3a7cb03875c60179e151dce8ec1b6 matched all eight starting sources/archive bytes. Current-vs-MAIN exact four-file diffs are pass-11/diffs/{recipe.py,test_recipe.py,SCHEMA.md,README.md}.T177.diff, alongside preserved historical baseline diffs. build.py/verify.py/config.json/shell.html remained identical. All old pass10/final2 files and source archives remain immutable.

PASS — R1 correction: actual reap_original_child uses only os.waitpid(originalPID,WNOHANG), exact nonbool original handle/PID/returncode/terminal-status validation, at most6000 observations including EINTR and pauses<=0.01s under the SAME original hard deadline. ECHILD/mismatched PID/bool/nonterminal/malformed status/cached or changed identity refuses, without Popen.wait/poll/proxy/fallback. Cached returncode no longer sets verified reaped facts. Valid consuming exit/signal facts immediately set process.returncode and existing code/reaped state before post-call time validation. Late valid consumption remains truthfully reaped but fails, with no expired following OS effect. Nonzero/signal cannot grant builder success.

PASS — D271 exact cutoff binding: historical NEW question notes/questions/T177-engine-original-reap-cutoff-1.md remains immutable, resolved separately by MAIN D271. Existing hard=min(commandStart+120,wholeStart+3600),work=hard-5 passed unchanged; no60s command cutoff, fresh wait-entry clock, grace/reset. The6000/.01 bounds are additional ceilings only. All D263 nullable permission observations, strict independent reader/action sequence/first distinct timely post-reap ESRCH, unrelated primary/cleanup/persistence failures and D235/D236/D238 boundaries remain. No new private wire field/public game/API/recipe/profile/61-unit125-command/84-member411990-byte/17-file/notice/source-acceptance/alias/dependency behavior changed.

PASS — **ALL9 sources frozen before first invocation** in the inspected plan,154292bytes/SHA2569f13bdc3c1428c15492a1381e528ca3339d66b7ac0ab46562461a4d071af66e7. Both jobs independently validated those pins; no source edits between or after. Static AST comparison established identical148 group names/all256 leaves and fixed16 focused case names; no case deletion/cap enlargement. Fixed commands from repository cwd:

1. `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -B tests/outbreak/builder_reap/T177/test_reap.py`
2. ONLY after observed focused PASS/exit0: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -B web/build/blackwood/test_recipe.py`

**Focused:** observed0af756 exit0;16 fixed case groups/16 meaningful scenarios,32 explicitly planned actual-source exercises (each actual helper direct plus actual Effects.run), recorded0.09649787505622953s. Raw cases cover terminal0/nonzero/signal/noevent/EINTR/consuming ECHILD/noevent ceiling+cutoff/wrong or bool PID/bool or nonterminal status/already cached/changed original PID/prewait cutoff/late valid consume/unrelated primary. Fake Popen.wait/poll traps assert never called, including negatives. Direct noevent case records6000 observations/5999 bounded fake pauses; integrated counterpart proves original hard expiry. ECHILD leaves original_handle_reaped false/exit_code null; late valid consume retains true/0 and failed receipt; primary errors are not rescued. Each case uses actual new source, not a mirrored policy or old test import.

**Full:** launch ee984a, session44853, same-session09239a then63f32a terminal **exit0**; complete148groups/256leaves, recorded63.61321791599039s. All prior124groups/214leaves and T17424groups/42leaves retained; only fake consuming boundary/control/guard/doc bindings adapted. Raw status getters reflect actual fake waitpid consumption, Popen methods refuse; before-closure cutoff remains after a timely helper return. No combined/reset job budget, retry, repair or occupied overwrite. These result clocks are recorded job observations, not separately measured precise outer-wall or native timing.

Both DISTINCT jobs independently retained original300s/8MiB combined output/128MiB fixtures. Focused retained16 files/1536956 bytes; full retained39 files/4112553 bytes. Captured+terminal output bytes focused0+2628, full187+996, each<8388608. Guard-before-private-load, all real process/wait/signal/FFI/tool/network/SDK-copy and old-driver imports denied; real effects reported zero. Protected-before/after pairs match byte-for-byte and all9 source byte/metadata pins match the pre-first-invocation plan. No failure markers.

| Evidence | Focused SHA256 | Full SHA256 |
| --- | --- | --- |
| result.json | `520bbfbe6117fa838cea9452bebf987425935287aad1e9ca866787ff9d9640d9` | `daa18285839763cd56d73b0950e61fc98f79bca468a165d087b7d3bdd942f11e` |
| cases.json | `285727d45ce4bcaf220d622eaa0987b1db522283a4f66eae398550f7d63ed62a` | `13c15379fa6a1bff4c71df8073d7dc5809c36f68f0d6ea2d568844d155679a68` |
| guard.json | `b7f3c091447ffd727974cf7d7d12cc0205ec04d41dfda33d8b03aa256b8bf5a0` | `2a92d0ead07d3ac6481cafa479972f4d1f72de20d16bb2bf7f5a2c8f6513acc2` |

PASS — after BOTH observed PASS, one inspected standard-library DATA-ONLY final3 operation: launch c68061/session17318,97db8a exit0, recorded1.105113708996214s. Only the three candidate records were created; all slots exclusively reserved0644/nlink1 before owned directory metadata, same inodes filled. Inventory explicitly historical reserved-slot prefill; receipt binds completed inventory; freeze binds completed inventory+receipt and complete module AND focused-home graphs. Sole direct freeze bytes/hash/derived timestamps excluded, with stable path/type/mode/nlink/device/inode retained. No unowned/shared-parent metadata or broad cache/history exclusion.

Complete candidate roots: web/build/blackwood AND tests/outbreak/builder_reap/T177. **363 ordinary files including direct freeze** (362 hash-bound members),74 owned directories,0 links; current9sources, every historical pass/final1/final2, pass11 and focused source/evidence included. **427 current external ordinary references +5 exact approved aliases0755/raw target/resolved identities**; current authorities/R1 review/primary installed subprocess source/MAIN baselines/accepted T163/T148/tool/ABI/port roles/own plans. Prior controls/freezes remain historical, not retargeted.

Owned graph SHA256 `81e5858fdd9d6ff6e7fa0fdec57508b2165e2d61cfc9c790bee03d409777be85`; external-role SHA256 `2948da5f57c8c8bb69fd1e1b286da195e54983b1eb0bac1d2004736b59c6eef1`. Operator recaptured both complete graphs/external roles/preexisting304module files/focused source/all9frozen sources. Subsequent read-only note QA rechecked362 member bytes+metadata/74directories/exact membership/cross-links/digests/old final1+final2 freeze hashes/source pins. All three records **PENDING_MAIN_REVIEW**, not accepted; combined new record bytes757948<134217728.

| Candidate final3 record | Bytes | SHA256 |
| --- | ---: | --- |
| inventory.json | 376013 | `f676b9a73d545277a53bdb501f59627f1d16e4dc7407d51a561cf15586e738ca` |
| freeze.json | 376507 | `ddb2b8599d05998fe8cf643593deaec064acecb0e047a40e32c3e8187e72278c` |
| receipt.json | 5428 | `6a9c22c0aaeebe488d1b9e8623c8bbd1e468489c0be241ae748ad21b020c2e86` |

## Current frozen source pins

| Path | Bytes | SHA256 |
| --- | ---: | --- |
| tests/outbreak/builder_reap/T177/test_reap.py | 16070 | `193600eabb0f88eb0830eb3f3d536cf0fa11d86aa9568c14d94b226b66bd4d6a` |
| web/build/blackwood/README.md | 10153 | `7c83198889179b9a1e122742d6a12fa14f628d70a378c8716862031d634b7b91` |
| web/build/blackwood/SCHEMA.md | 25194 | `75edd5ccd7669143b05dd5f79d87f8a16acffaa55f8e9fcbe50be5b1380d968f` |
| web/build/blackwood/build.py | 342 | `4c195f205d2947d821834de19e852b0b5d3911e9d26c9a782bbc5fb4e883bb99` |
| web/build/blackwood/config.json | 1558 | `10aa1033b0830efff51b1b4bdbb3fab9479efef453e380f7e2bf5532d4f464fb` |
| web/build/blackwood/recipe.py | 91917 | `ca7068ea74e3a0cd47654b700e892ee64ead2d32026e9b5cdaa7dba11a869fb9` |
| web/build/blackwood/shell.html | 2012 | `6fccbeb1094a4f09998db25b123d2b9287b75da013f80d6e72a0444efa751399` |
| web/build/blackwood/test_recipe.py | 88244 | `b8624fb634b31e2d56b553717adc5afaa2846dce130948294c7224c87160c8e1` |
| web/build/blackwood/verify.py | 339 | `506f52fcd76548ae8aef46043de9256e83d5d621343f074da843818933ada3eb` |

## Implementation status

Implemented: narrow strict consuming-reap source correction/necessary private fake-boundary guard/doc/control bindings and focused test source. Simulated:16 focused cases and separate148/256 full regression only. Actual data checks: source/diff/byte/metadata/graph integrity. NOT RUN: actual compiler/Node/version/tool/native/FFI/signal/wait/process/SDK-copy/build/verify/server/browser/network/Git. The authorized Python test interpreters/data-only inventory are ordinary task filesystem work, not a claimed zero-filesystem-effect operation.

No source edit after first invocation. Pre-invocation patch-context mistakes applied no changes and were corrected before freeze; neither was a failed fixture/job or an automatic retry. All old failures/source snapshots/pass10/final2 remain. No consuming ECHILD status is converted into success and no actual platform support/EPERM cause/process/persistence/performance proof is claimed from fake cases.

## Integration and questions

No open semantic question after D271. The preserved question's resolution and exact original deadline are bound in the frozen plan/source/docs. Own inspected inventory operation note: notes/proposals/T177-engine-final3-inventory-operation-1.md,11834bytes/SHA2568b9b3c58839ff03db2911e5c6f884b79727166c92c4da530a038efd61bdb1f34, embedded code SHA2563fc3d63173d916d4395695a105b2a22941ef6ce08478e3f75c34c8ddc78d02c6. The final graph binds that operation and pre-first-invocation plan as current external references; this outside handoff is not recursively inserted into it.

MAIN reviews the stable source/diffs/16rawcases/full148-256/candidate final3 packet before acceptance or any actual build. Future admission/controller materialization binds the accepted corrected producer semantics/source, never a relabeled old Popen.wait proof. Full Blackwood/default-dev/native builds, source manifest, actual native+two-browser map/load/render/mapident/spawn/current-life ACK/reciprocal movement/cleanup and all P0/full-game/authority/third-person/combat/survival/extraction/eight-player/performance/RSS/human gates remain mandatory and separate. NativeT167/Player/QA/T149 remain held, untouched/unreassigned; no worker negotiation/dispatch. Submitted and stopped for MAIN review.
