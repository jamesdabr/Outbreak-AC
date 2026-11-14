# T040 attempt 2 — accepted map ownership fix integrated

- Worker: Engine & Multiplayer
- Ticket: T040 1.3 RELEASED integration under D021; no status/contract amendment
- Baseline: AGENTS, browser foundation/GOVERNANCE/P0 0.5, exact D006/D009 profile, accepted original pack; D017 diagnostic/history preserved
- Base commit: `13f0d8eea4822dee5c976661218d022be74342e3` plus accepted working tree
- Engine source/header/tooling/config changes in this attempt: NONE
- Only tracked input change versus D016: MAIN-accepted T042 source/src/worldio.cpp, SHA-256 `8b6d1e7aa7197be1d5030954f48662bcaab85412b222cea027762fbdb1c488c1`
- New writes: web/build/generated/t040/d016-snapshot, attempt-2 evidence/artifact snapshot/logs, current web/build/out and authorized target caches only; this new handoff
- No commits/push/reset/revert, source/asset/QA/server edits, dispatch/messages to workers, browser/server/game launch or global installation

## New frozen artifact

Artifact ID:
`T040-24f41b7c5e1c9eafa5b72e31cb5bddb2a40a405a7d1f1f772bc437cbfbb1d2e0`

Root `/Users/jd1/code/apps/outbreak/web/build/out`, entry `index.html`.
Current output is **frozen for MAIN/QA**. Exact copy retained under
`web/build/generated/t040/attempt-2/artifact/`.

| File | Bytes | SHA-256 |
| --- | --- | --- |
| index.html | 1330 | `22b4e8d79b6032639783f075a2d7bed69dde780476b2889ae80cff19f34a1725` |
| index.js | 340204 | `0bfb0bc1c50c18ac5558a04c9dd2364b1465f6fb01630078b5e07f469d7a505f` |
| index.wasm | 1845020 | `2718f7c49ddd7fa056f304222ce916021bface86c46c32c93adcb05e9e18cddd` |
| index.data | 87897 | `66574ce6af122f6c10fdfa51c7030c6f25511bd0936f09d292e07f316cd30877` |
| build-metadata.json | 146965 | `e47c49c26e1715846cfc22cd0208cdb9a36ae395cdd775810c4d44ce2ef36e45` |

HTML/JS/data remain byte-identical to D016; Wasm and metadata reflect the
accepted map ownership source fix. No diagnostic --emit-symbol-map flag is
present in the acceptance command.

## Acceptance evidence

| T040 criterion / D021 requirement | Result | Evidence |
| --- | --- | --- |
| 1. Preserve prior runtime/metadata; consume accepted stable source | PASS | Before replacing out, verified all five attempt-1/D016 file pins, copied the full prior out/notices/metadata and result to generated/t040/d016-snapshot, hashed snapshot.json. D011 and D017 snapshots/history remain unchanged. worldio stable hash checked before build; all other tracked inputs match D016. |
| 2. Real compile/link, identical SDK/six ports/profile/pack; no source/new flags | PASS | All 53 actual CLIENT_OBJS C++ + 8 ENet C units compiled, each exit 0 and valid Wasm object; actual full link exit 0. Conservative separate attempt output avoids stale reuse. Config equality versus attempt-1 is exact, including ticket label; accepted pack inputs identical. No extra ports/flags, symbol-map flag, error suppression or source edit. |
| 3. Exact output/preload/notices/source/port identity and native preservation | PASS | Verifier checks every final input/output hash, real canvas id, Wasm signature, all 41 actual JS-described data slices against accepted manifest, total 87897 bytes, metadata and notices. Node --check actual index.js exits 0. All six port recipe/archive hashes pass; native outputs unchanged, stale_inputs empty. |
| 4. Concrete ID/pins/source delta; honest link/runtime distinction | PASS | artifact-pins.json and table above; integration-verification.json proves only worldio.cpp changed. Exact actual commands/diagnostics/source/object hashes in attempt-2/result.json/logs/source/** and link.log. No browser/engine run performed by Engine. Recovery remains NOT RUN pending new actual QA. |
| 5. Same-ticket accepted-fix iteration, immutable attempts and freeze | PASS for attempt 2 | D021 explicit accepted hash consumed within existing T040 scope. Prior attempts/diagnostic preserved; new output snapshotted and frozen. Ticket remains RELEASED for MAIN review/later explicit accepted source fixes; no new scope assumed. |

Evidence root: `web/build/generated/t040/attempt-2/`. Key files are
result.json, link.log, artifact-pins.json, integration-verification.json,
preload-output-verification.json, qa-launch-command.json and artifact/.
Top-level stdout/verification logs are under generated/t040.

Environment unchanged: macOS 26.5.1 arm64, Python 3.11, inspected Emscripten
7.0.0/compiler `777e6e5db7b4990bcaeb1b9998ed642cc84e6629`, local Node24.19.0.
Exact safe legacy GL profile, GL_UNSAFE_OPTS=0, 64MiB initial memory, 2MiB
stack, memory growth, six approved ports and original manifest
`1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3`
are preserved. Source/library notices and original media notices remain.

## Commands already executed

From `/Users/jd1/code/apps/outbreak`:

```sh
python3 -B web/build/build_client.py --jobs 4 --evidence-dir web/build/generated/t040/attempt-2 --pack-sha256 1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3 --pack-authorization notes/decisions/D006-pack-acceptance.md
python3 -B web/build/verify_client_bundle.py --evidence-dir web/build/generated/t040/attempt-2
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node --check web/build/out/index.js
git diff --check
```

All exit 0. No driver source change was required for this iteration.
qa-launch-command.json contains the new exact ID/five file pins and bounded
real-mode observer command; supplied but NOT RUN by Engine. Do not rebuild
while MAIN/QA consumes this bundle.

## Remaining verification

Successful integration proves neither recovery from the D016 allocator trap
nor rendered/moving frames. MAIN must independently pin this artifact and
dispatch the actual browser observer. T042's accepted source/helper/object
scope is not promoted to runtime or sanitizer success here. The optional
ASan timeout and malformed-RLE observation retain D021's stated limits;
no ASan build flag, arbitrary-map acceptance or decoder rewrite was added.
Actual input/collision/audio/models/network/eight-player gates remain separate.

No new compile/link/integrity blocker remains. Historical handoffs/questions,
tickets/contracts/decisions and other workers' files were not edited. Only
MAIN may accept this attempt or authorize a later accepted-fix rebuild.
