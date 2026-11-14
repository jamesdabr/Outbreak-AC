# T164 Engine focused correction review-ready handoff 2

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket: T164 revision1.1 / D236, RELEASED FOCUSED SOURCE/PREPARATION CORRECTION.
- Governing: BLACKWOOD_BUILD_PREPARATION0.1 / D224, T163/D223 and T148, with D235 adapter route unchanged.
- Submission: **REVIEW-READY; NOT ACCEPTED, NOT FROZEN, NO ACTUAL EXECUTION RELEASE.**
- Base: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work; no Git command/mutation or clean-tree claim.
- Changed source: only recipe.py, test_recipe.py, SCHEMA.md, README.md under web/build/blackwood. Added only fresh pass-8, review-ready-2.json and this own new handoff. build.py, verify.py, config.json, shell.html and all prior passes/baselines/index1/handoff1 are unchanged.
- Commit/patch: none authorized or created. Exact current identities below.

## Focused D236 disposition

MAIN review `notes/reviews/T164-final-source-evidence-review-1.md` SHA2568c818a22a598e3efad332dbb1ad96f1187b200c2746b8dca1b392f10a6b6b394 returned one receipt-slot gap. D236 and T1641.1 were read before this correction. Original group-cleanup and final marker/history findings were already cleared by MAIN; no additional generic scope was undertaken.

**Implemented / guarded evidence PASS:** the final verifier now checks the fixed excluded receipt slot through strict Gate.read/record. Whenever present it must be exact canonical receipt bytes and ordinary single-link mode0644 {bytes,sha256,mode}; once observed it participates in subsequent consumed-identity rechecks. An observed receipt disappearing refuses even in default read-only mode. After an explicit receipt request, final presence is required.

The long final observation/control/owned-inventory checks are followed by receipt validation, consumed rechecks and another receipt validation to detect previously absent-slot creation during those rechecks. Explicit refusal-marker absence remains the final required observation. Pre-publication checks allow an absent optional slot; post-publication checks require its presence. Default verification still writes nothing; explicit publication remains exclusive, without overwrite, cleanup or repair. No record fields, CLI/API/tool commands, gameplay values or limits changed. This is not a filesystem-atomicity claim after return.

**Actual-method fixture evidence:** a new pinned receipt-race matrix has14 leaves. It calls the actual new verifier and injects late mutations during final config reads inside observe, consumed rechecks and publication. Thirteen cases refuse: default/requested late wrong creation/replacement, default/requested observed deletion, requested deletion during the post-publication final observation, immediate publication replacement/deletion, default symlink/hardlink/wrong-mode creation, and absent-slot creation during consumed recheck. One positive accepts a correctly created canonical receipt; default-mode cases assert zero verifier writes. Injection reachability and publication/observation facts are retained for every leaf.

## Current guarded pass

Inspected command: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/build/blackwood/test_recipe.py`.

`tests/preparation-1/pass-8` **PASS_GUARDED_PREPARATION_ONLY** in63.884902 seconds: **123 top-level result groups /192 executed leaf scenarios** =120 individual groups +26 observer leaves +32 supervisor leaves +14 receipt-race leaves in three matrix groups. The plan's128 cap applies to top-level groups, not leaves; all three exact subcase lists were pinned before import. No cap increased, negative dropped or unchanged retry performed. Source correction prompted this sole fresh pass after pass7.

The full positive fake graph still exercises61 genuine ordered source names,125 simulated commands,84 actual copied public-data slices/411990 bytes and exact17-file bundles/notices through actual orchestration and independent verification. Fake receipt status is FIXTURE_ONLY. Source/header/reference provenance, strict roles/closures, payload/metadata checks and all-false runtime/audio/model/multiplayer/authority/P0 claims remain checked.

Pass8 retained3634144 fixture bytes and187 captured stdout/stderr bytes. Existing limits remain300 seconds with two-second failure-retention reserve,128 top-level groups,4096 virtual nodes,8 MiB captured output and128 MiB retained fixture bytes; future real build3600s/command120s/log8 MiB caps remain unchanged. No real build-timing or engine-performance inference follows.

Guard evidence reports zero actual children, process/tool/version/compiler/Node/signing probes, SDK/cache copies, network and FFI calls. Real process/control/signal/wait/uname/ctypes/old-project-import effects are denied before new imports; only explicit fictional boundaries replace them when actual methods are called. All test writes stay in the fresh pass, and before/after selected accepted real input hashes match. Actual attempts/, candidates/ and web/repro/blackwood-source-manifest.json remain absent/unwritten. No actual production plan/build/verify or runtime was invoked.

## Exact stable source identities

All eight current source files are ordinary single-link mode0644, and equal pass8 snapshots/result source pins. Only the four leased files changed relative to pass7; the other four pins remain exact.

| Repository path | Bytes | SHA256 |
| --- | ---: | --- |
| web/build/blackwood/README.md | 6264 | `d5c592abd3ad769b6add92430093859003f8d90f4a26ddbcb772fafcf58a21df` |
| web/build/blackwood/SCHEMA.md | 18622 | `0411d27e976dbe423d7639e8a77d1e82232b7169898060d80e79aba6d8fc5c5b` |
| web/build/blackwood/build.py | 342 | `4c195f205d2947d821834de19e852b0b5d3911e9d26c9a782bbc5fb4e883bb99` |
| web/build/blackwood/config.json | 1558 | `10aa1033b0830efff51b1b4bdbb3fab9479efef453e380f7e2bf5532d4f464fb` |
| web/build/blackwood/recipe.py | 81300 | `535ec8ebcef63387ea5f081058dcc27b49eed69468d99c09359f60eabc9acab9` |
| web/build/blackwood/shell.html | 2012 | `6fccbeb1094a4f09998db25b123d2b9287b75da013f80d6e72a0444efa751399` |
| web/build/blackwood/test_recipe.py | 62669 | `7f7f2a79234831e879b81e85da93c2a2c6aada5634a9e75a909bac9b1c7f65b5` |
| web/build/blackwood/verify.py | 339 | `506f52fcd76548ae8aef46043de9256e83d5d621343f074da843818933ada3eb` |

## New evidence index and preservation

`web/build/blackwood/tests/preparation-1/review-ready-2.json`:50135 bytes, SHA256 **f456288f7522629e9a687a3fbe72ea1cc70435902a0d26d8b883842953f4d0d4**. It indexes222 pre-index fixture files/19725550 bytes, all eight current source identities, current T1641.1/D224/D235/D236/review controls, and historical index/handoff identity. It is a review index, not a freeze, and excludes only its own recursive hash.

| Pass8 evidence | SHA256 |
| --- | --- |
| plan.json | f0155c9c245e91d0fdd2f98c80092cd22ed92dd95c4d69b5d93c3647d980242a |
| result.json | 57206a80981079cfc5bd307a690508b9754aab7fd7afcc30d8a693ae6726bb2d |
| cases.json | 2f97a6a7e498d9eedfa201a8fd40a1f40c767b78a6d379a5e6ab9d9ef51b434c |
| guard.json | 2a92d0ead07d3ac6481cafa479972f4d1f72de20d16bb2bf7f5a2c8f6513acc2 |
| protected-before.json AND protected-after.json | edb429d12dff40f706678a089953ca40f341b85a9996a44014ade340c4377b8a |
| positive-graph.json | d8e769134daa2dd957a9a22b62a6ba6c1604322675c8ca6fd03b7f064d8faa15 |

The prior190 indexed fixture files plus index1 itself (191-file union) were rehashed unchanged. Index1 remainsfc3e82116bf8d0671c61c7c4ae44b78d7cad3179bd27e47278a535b2c371a3c1; original handoff1 remainsab8f9ec076e0e8a3da5d17f272d0bc81680b586e7aa0ae78f020333c85cd79ff. Their old ticket/control pins are historical and were not rewritten after revision1.1. All five historical failures and both prior successful passes remain intact. Handoff1 retains full historical failure explanations and original scope evidence; pass7 remains valid simulated evidence with the subsequently identified receipt correction handled here.

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

Unrecorded historical timers remain unrecorded; pass2 file timing is approximate and not a qualified repaired result. Pass2/3 exceeded300 seconds and remain disclosed failed evidence. Failed capture figures refer to the retained failure.json stdout_stderr field; successful capture figures refer to stdout-stderr.bin, excluding external runner tracebacks. No old measurement was edited.

## Incomplete work and stop boundary

No actual compiler/Node/library resolution/native wait, SDK/cache copy, native build/staging/signing, default-dev regression, admission/controller, server/transport/browser/two-browser or gameplay/runtime proof was run. Underlying Darwin WNOWAIT behavior remains UNPROVEN. Mandatory real builds/native/admission/pair/runtime/RSS/performance/full-phase/human requirements and QA/T149 holds remain. No source manifest or shared interface was edited, and no new dependency/selector/profile was introduced.

Ticket1.1/D236 lease and BLACKWOOD_BUILD_PREPARATION0.1 were checked for submission. This stable source/evidence handoff addresses the one returned private-verifier correction and stops for MAIN review. MAIN alone clears freeze/acceptance and any later actual execution release.
