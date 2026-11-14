# T040 attempt 1 — accepted font command fix integrated

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket/revision: T040 1.3 RELEASED; submitted attempt evidence, no self-acceptance/status edit
- Governing baseline: AGENTS; browser foundation/GOVERNANCE/P0 0.5; D006/D009 exact build profile; D011/D012/D013 history; D015 execution addendum 1.3
- Source base: `13f0d8eea4822dee5c976661218d022be74342e3` plus preserved accepted working tree. Only engine-source delta versus linked D011 is MAIN-accepted T038 rendertext.cpp `b8d6481f8681b3b7223d5d75f1a46b67417252dd10e39b22598b0f43e4d36e68`.
- Engine source/header changes by this ticket: NONE. All engine/asset/QA/server/contracts/decisions read-only.
- Changed build tooling: build_client.py and verify_client_bundle.py gain an explicit generated attempt evidence directory; client-config.json ticket label becomes T040 1.3, with every compile/link/port flag unchanged. New evidence/output under web/build/generated/t040 and web/build/out only. Historical T031 evidence/handoffs remain untouched.
- No commits/push/reset/revert, worker dispatch, service/browser/game launch, global installation or profile access.

## Artifact for MAIN's new QA pinning

Artifact ID:
`T040-3800e5ef78bcb84033e30c72e276ebebc342b6f97185fbfcb434de021d87a7ab`

Root: `/Users/jd1/code/apps/outbreak/web/build/out`; entry `index.html`.
**Current output is frozen for QA.** It has also been copied byte-for-byte
to `web/build/generated/t040/attempt-1/artifact/` for immutable attempt history.

| File | Bytes | SHA-256 |
| --- | --- | --- |
| index.html | 1330 | `22b4e8d79b6032639783f075a2d7bed69dde780476b2889ae80cff19f34a1725` |
| index.js | 340204 | `0bfb0bc1c50c18ac5558a04c9dd2364b1465f6fb01630078b5e07f469d7a505f` |
| index.wasm | 1845609 | `6165af498f65cc7a51a877801679978a5672fea7c78f27c1ae143cd09c1ab229` |
| index.data | 87897 | `66574ce6af122f6c10fdfa51c7030c6f25511bd0936f09d292e07f316cd30877` |
| build-metadata.json | 146965 | `b6d7652b06fa078f930aeaabe47e5bc43bae3636edf8295800c2301d9f90901d` |

Only Wasm and build metadata differ from the preceding runtime bundle; HTML,
JS and original data remain byte-identical. The changed Wasm reflects the
accepted source fix, not a new compatibility flag.

## Per-criterion acceptance evidence

| T040 criterion | Result | Evidence |
| --- | --- | --- |
| 1. Preserve D011 and consume accepted stable source | PASS | Before any mutation, verified all four D011 runtime pins and copied complete prior out tree/notices/final metadata plus T031 result to generated/t040/d011-snapshot. snapshot.json records hashes; metadata is the D013-reconciled b26443f… version. Accepted rendertext hash checked before build. Other accepted engine/header bytes unchanged. |
| 2. Real changed/stale compilation and link, same profile/ports/pack | PASS | New attempt directory, driver/label fingerprint and conservative dependency policy caused an actual full rebuild: 53 C++ + 8 ENet C units, all exit 0 and genuine Wasm objects. Actual full link exit 0. Six approved recipe/archive identities pass. SDK/flags/ports/memory/pack compare exactly to T031 except ticket label. No cast emulation, undefined suppression, extra dependency/flag or source edit. |
| 3. Verify actual output/preload/notices/input identity/native preservation | PASS | verify_client_bundle.py passes input/output hash stability, Wasm signature, real canvas id, every actual data-package slice and all 41 original per-file hashes. Node --check index.js exits 0. Native outputs unchanged and no stale inputs. All output/notices hashes in result.json and build metadata; integration-verification.json and preload-output-verification.json provide separate results. |
| 4. New ID/pins/current metadata/source change list, no game claim | PASS | artifact-pins.json, table above and integration-verification.json identify only rendertext.cpp as changed engine source. Full argv/logs/source/header hashes are retained. No Engine browser/server execution. Actual corrected font-command startup/rendering remains NOT RUN pending MAIN's dispatch using accepted T037 observer. |
| 5. Repeat only MAIN-accepted fixes with retained attempts; freeze | PASS for current integration attempt | Tooling supports separate attempt directories; prior D011 and T031 preserved. Current outputs frozen after all checks. No later source fix is assumed accepted. Future iterations require MAIN's explicit accepted stable identity while keeping the same ticket/flags/pack scope; no authoritative status changed. |

Environment unchanged: macOS 26.5.1 arm64, existing Python 3.11, inspected
Emscripten 7.0.0/compiler `777e6e5db7b4990bcaeb1b9998ed642cc84e6629`, local
Node 24.19.0. Target flags remain gnu++11/fsigned-char/O2, ENet HAS_SOCKLEN_T=1,
SDL2/SDL2_image PNG/zlib/Vorbis/Ogg/libpng, SDK OpenAL, legacy GL with
GL_UNSAFE_OPTS=0, INITIAL_MEMORY=67108864, STACK_SIZE=2097152 and memory growth.

Accepted manifest:
`1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3`;
41 original files/87897 bytes mounted only at `/outbreak`. Source/media notices
are preserved unchanged. No assets or inherited host configs were added.

## Commands and evidence paths

From `/Users/jd1/code/apps/outbreak` (already executed):

```sh
python3 -B web/build/build_client.py --jobs 4 --evidence-dir web/build/generated/t040/attempt-1 --pack-sha256 1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3 --pack-authorization notes/decisions/D006-pack-acceptance.md
python3 -B web/build/verify_client_bundle.py --evidence-dir web/build/generated/t040/attempt-1
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node --check web/build/out/index.js
git diff --check
```

Each exits 0. Authored driver changes were inspected before execution.
`generated/t040/attempt-1.stdout.log` and `attempt-1.verify.log` retain the
top-level output. `attempt-1/result.json`, `link.log`, `logs/source/**`,
`artifact-pins.json`, `integration-verification.json`,
`preload-output-verification.json` and artifact snapshot retain actual evidence.
No prior T031 result/log was overwritten by the new attempt directory.

`attempt-1/qa-launch-command.json` supplies the exact new-ID, five-file-pinned
real-mode QA command with an ephemeral loopback URL. It is **not executed by
Engine** and requires MAIN's actual QA dispatch; its output filename is a
candidate and QA may choose a fresh owned result path. Engine made no write
under web/qa. T037's accepted stack-capable observer stays unchanged.

## Remaining verification and integration

No compile/link/output-integrity blocker remains. The D012 setfont callback
diagnosis remains an inference about the first actual startup fault until QA
runs this new Wasm and observes its result/full stack. Link success does not
establish frames, rendering, input, collision, audio/models or multiplayer.
No simulated test or fixture substitutes for those actual engine gates.

T040 remains a released integration ticket pending MAIN review and subsequent
explicit accepted-fix iterations. Keep current bundle frozen during QA.
New source, flags, dependencies or pack scope require the existing question
process. T014/T015/full P0/eight-player MVP are not claimed complete. Ticket
and governing revisions were reread before submission; no old handoff,
question, ticket or decision was edited.
