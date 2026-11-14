# T031 real browser client link and frozen QA artifact

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T031 0.6 RELEASED, additive D008 0.8 and D009 0.9; submitted for MAIN review, no authoritative status change
- Governing baseline: AGENTS; BROWSER_FOUNDATION/GOVERNANCE/P0 0.5; D006, accepted T027 pack decision, accepted T034 stable-source decision
- Base: `13f0d8eea4822dee5c976661218d022be74342e3` plus preserved dirty tree and D006 source baseline. Initial source hashes matched D006. Player's separately accepted T034 updates were consumed; Engine never edited Player/AI/World/QA source.
- Changed Engine source: only source/src/tools.h exact D008 native-arm64 ASSERT guard. Stable SHA-256 `e53d32d55e5b81ac5e5be3e8a2411a8363dae858631f06cfd3ed11b16eef6fcf`; platform.h unchanged this ticket.
- Authored build files: web/build/build_client.py, client-config.json, shell.html, verify_client_bundle.py; updated README.md; verbatim notices under web/build/notices with provenance.json. Generated objects/logs/fixtures/results under web/build/generated/t031; target dependency/cache writes under web/build/.cache; linked output under web/build/out.
- Commits/branches/push/reset/revert: none authorized or performed. No service, browser, game client or dedicated server was launched by Engine.

## Acceptance evidence

Host: macOS 26.5.1 arm64; existing Python 3.11; target Emscripten 7.0.0/compiler `777e6e5db7b4990bcaeb1b9998ed642cc84e6629`, local Node 24.19.0. Native syntax/fixture compiler: Apple clang 17.0.0.

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1. Real CLIENT_OBJS + ENet source compilation, no host input/substituted units | PASS | Final 61 commands exit 0: 53 real C++ TUs parsed from Makefile, 8 repository ENet C TUs. Every object has Wasm magic/hash; no reused objects in the final conservative rebuild. Exact commands, diagnostics and source hashes in generated/t031/result.json and logs/source/**. No native PCH/framework/library or fake engine source in target inputs. |
| 2. Pinned target libraries, exact PNG/libpng, safe compatibility flags | PASS | Six retained port archives and all recipe SHA-256 values verified in final result.port_integrity. PNG 1.6.59 SHA-512 matches D006. SDK OpenAL only. Final link explicitly contains LEGACY_GL_EMULATION=1 and GL_UNSAFE_OPTS=0 per D009; no unsafe/undefined-ignore/thread/SIMD/JPEG flags. |
| 3. Actual HTML/JS/Wasm/data, bounded memory/stack/growth, real status shell | PASS — link/static verification only | Full link exits 0. INITIAL_MEMORY=67108864, STACK_SIZE=2097152, ALLOW_MEMORY_GROWTH=1; default WebGL1. HTML parser verifies canvas id canvas; loading/error callbacks are real runtime callbacks and do not fabricate diagnostics. Wasm magic and Node --check of actual index.js pass. No runtime/render claim. |
| 4. Only accepted original pack; exact contents and notices | PASS | Manifest SHA 1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3; exact 41 files/87897 bytes validated before preload at /outbreak. Independent inspection of emitted JS filename/offset metadata and all actual index.data slices reproduces every accepted per-file hash. Original pack notices remain embedded; 11 verbatim source/target-library notices plus provenance are beside the bundle. No stock asset tree or private config was copied. |
| 5. Identity/flags/input/output hashes and concurrent-change detection | PASS, with metadata-only D011 note below | Final result and out/build-metadata.json identify commit, every source/header/config/pack input, actual commands, compiler/ports, outputs and omission profile. No stale inputs or source changes during final build; native outputs unchanged. All four runtime files match D011 exactly. Final metadata-only integrity refinement changed build metadata/driver fingerprint before freeze; both metadata identities are preserved and disclosed below. |
| 6. Current native/Wasm regressions, exact QA launch, honest runtime limits | PASS — build/regression scope | current-regression.json: 10 current native release/debug syntax passes and five actual _DEBUG Wasm objects (clientgame/main/server/editing/rendermodel), stable input hashes. D008 assert-regression proves native ARM brk, isolated false assertion SIGTRAP(-5), x86 int3, unchanged release behavior. QA command below is supplied, NOT RUN by Engine. |

Canonical evidence directory: `web/build/generated/t031/`. Final successful
attempt-5 contains result.json/link.log/current-regression.json, exact current
build-metadata.json, preload verification and artifact pins. Earlier real
attempts 1/2 failed at seven legacy GL imports and are preserved separately;
accepted T034 removes those imports via existing real draw paths, not stubs.
Attempt 3 conservatively rebuilt all units without link. Attempts 4 and 5
both linked successfully with D009 flags and identical runtime output bytes.

## Frozen runtime output identity

MAIN's D011 QA identity remains
`8792410f512392c628063109856fc3e65d97a037590ff0f9d376f4e70a8e637c`.
Its four runtime files remain byte-identical and are frozen for QA:

| File under web/build/out | Bytes | SHA-256 |
| --- | --- | --- |
| index.html | 1330 | `22b4e8d79b6032639783f075a2d7bed69dde780476b2889ae80cff19f34a1725` |
| index.js | 340204 | `0bfb0bc1c50c18ac5558a04c9dd2364b1465f6fb01630078b5e07f469d7a505f` |
| index.wasm | 1845486 | `3b3a7aa8674f8bdb6e827238c8d7c47b31e9861c4e86b7988a7187f7b906628b` |
| index.data | 87897 | `66574ce6af122f6c10fdfa51c7030c6f25511bd0936f09d292e07f316cd30877` |

**Metadata-only coordination note:** D011 captured build-metadata SHA
`9890ade7a064111fc5c40ec40b36b77089fc275aa7c242df50db7977cfb65bf9`.
Immediately before MAIN's freeze message, a final build-driver integrity
correction completed: the pinned SDK actually retains the PNG archive as
libpng.6.59.tar.gz, not libpng.tar.gz. SDK had already checked the correct
SHA-512 before building; the driver now independently records/validates all
six retained archives instead of skipping its wrongly named PNG path. This
changed only build-driver fingerprint and metadata; final HTML/JS/Wasm/data
hashes above are identical across both successful links.

Current out/build-metadata.json is 144515 bytes, SHA
`b26443f20a8e929f97bc3df72e1c11333afe0f0d10bdf3ae560eccbf5ff7cec4`;
its internal build fingerprint is
`b89a85d2ceb6ef61f962b4a84dadea92773ca8386c6681244483bf0fed566217`.
This metadata identity is submitted for MAIN reconciliation; Engine does not
amend D011 or redefine its accepted QA identity. D011-freeze-check.json records
the exact comparison. No bundle/source/profile change occurred after the
freeze message; no more builds are planned without a new concrete assignment.

## Commands and implementation

Exact successful build from repository root (already executed):

```sh
python3 -B web/build/build_client.py --jobs 4 --pack-sha256 1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3 --pack-authorization notes/decisions/D006-pack-acceptance.md
python3 -B web/build/generated/t031/regression_current.py
python3 -B web/build/verify_client_bundle.py
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node --check web/build/out/index.js
git diff --check
```

These were inspected before execution. Do not rerun the build during QA's
frozen-artifact session. Verification reads output as data and never runs
the game. Diagnostic commands and first-use target compilation logs remain
under t031; source/media notices have explicit source hashes/provenance.

Actual link source fixes are Player's accepted main/editing/vertmodel bytes
in D008-gl-fixes-acceptance.json; no extra Engine source workaround was added.
The Engine-only arm64 header fix is documented separately in
notes/handoffs/T031-engine-assert-1.md. All shared header consumers were
conservatively rebuilt afterward. Existing native Makefile/build artifacts,
pre-existing combat source and other owners' files were preserved.

## Exact QA serve/launch handoff — not executed by Engine

The existing QA real-mode harness owns a bounded loopback server and an
isolated browser profile. This command uses the **D011 accepted runtime ID
and four runtime pins**; current metadata-only re-pin is a separate MAIN
decision. Run only when MAIN dispatches QA:

```sh
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node web/qa/game_probe.mjs --mode real --root web/build/out --url http://127.0.0.1:0/index.html --artifact-id 8792410f512392c628063109856fc3e65d97a037590ff0f9d376f4e70a8e637c --expect-file index.html=22b4e8d79b6032639783f075a2d7bed69dde780476b2889ae80cff19f34a1725 --expect-file index.js=0bfb0bc1c50c18ac5558a04c9dd2364b1465f6fb01630078b5e07f469d7a505f --expect-file index.wasm=3b3a7aa8674f8bdb6e827238c8d7c47b31e9861c4e86b7988a7187f7b906628b --expect-file index.data=66574ce6af122f6c10fdfa51c7030c6f25511bd0936f09d292e07f316cd30877 --output web/qa/results/T031-real-first.json
```

QA may choose its own fresh result path; Engine wrote nothing under web/qa.
Do not pin the old D011 metadata SHA against the regenerated current metadata.

## Remaining scope and limits

No successful game/browser session has been observed by Engine. Actual map
load/render, PNG alias decoding, controls/collision, focus/pointer lifecycle
and diagnostics require QA/T014. Audio and local character/HUD weapon models
remain intentionally omitted by the approved offline profile. Browser
mapshot/minimap texture readback is explicitly unsupported under D008;
normal framebuffer screenshot remains. Model code retains real direct
vertex/index drawing, but actual model rendering lacks runtime evidence.

Dedicated-server client joins, browser networking, authority/replication,
two-client proof and the eight-player MVP remain separate unaccepted gates.
The historical GL/default questions are technically resolved by D008/T034
and D009; their old notes were preserved. No unresolved build/compiler/link
error remains in this submission. Only MAIN may accept T031 or amend D011's
metadata identity. Ticket/contract/addendum revisions were reread before
submission; no contract, ticket, decision or earlier handoff was edited.
