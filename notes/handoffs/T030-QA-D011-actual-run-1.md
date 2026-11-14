# T030 first actual-engine D011 run — startup failure

- Worker: QA/Performance / `01a1b92d-28be-7110-9ac6-7ae01476c117`
- Ticket: T030 revision 0.5 continuation; exact real-run authorization D011
- Governing evidence: `D011-real-browser-run.md` and `D011-first-real-browser-artifact.json` read after MAIN lifted the hold
- Artifact ID: `8792410f512392c628063109856fc3e65d97a037590ff0f9d376f4e70a8e637c`
- Source baseline: `13f0d8eea4822dee5c976661218d022be74342e3` plus lead-verified current build inputs; no source/observer/build/asset change by QA
- Changed files: new `web/qa/results/T030-real-D011-1.json`, matching stdout/stderr logs, this handoff and new own question note
- Execution: 8 November 2026, 00:14 America/New_York; evidence UTC timestamp `2026-11-08T05:14:17.454Z`
- Commit/push/branch/reset/revert: none

## First actual result

**FAIL — real startup:** `RuntimeError: function signature mismatch`.

The first actual D005 sample recorded:

```json
{"schema_version":1,"profile":"offline-map","phase":"error","frame_count":0,"rendered_frame_count":0,"map_name":"","player_position":[0,0,0],"input_locked":false,"runtime_errors":["RuntimeError: function signature mismatch"]}
```

Observer exited 1 with `real_observation` code `runtime_error`; the browser page
exception message is `function signature mismatch`. The unchanged observer
captured the message, not a stack/callsite. The causal source function is unknown
from this run and is not guessed. No repeat run or bypass was used.

All four real files loaded over local HTTP with exact approved response hashes:

| File | SHA-256 |
| --- | --- |
| index.html | `22b4e8d79b6032639783f075a2d7bed69dde780476b2889ae80cff19f34a1725` |
| index.js | `0bfb0bc1c50c18ac5558a04c9dd2364b1465f6fb01630078b5e07f469d7a505f` |
| index.wasm | `3b3a7aa8674f8bdb6e827238c8d7c47b31e9861c4e86b7988a7187f7b906628b` |
| index.data | `66574ce6af122f6c10fdfa51c7030c6f25511bd0936f09d292e07f316cd30877` |

HTTP status was 200 for all four. No other page resource request, external/blocked
request, failed request or HTTP failure was observed. This is real linked-engine
runtime evidence, not a fixture, echo, compile-only or successful gameplay result.

Console errors captured verbatim:

- `WARNING: using emscripten GL emulation. This is a collection of limited workarounds, do not expect it to work.`
- `WARNING: using emscripten GL immediate mode emulation. This is very limited in what it supports`
- `TODO: glShadeModel`

Console warnings also include two
`WebGL: INVALID_ENUM: hint: invalid target` entries. These are separately recorded;
this run does not establish whether they caused the signature mismatch. They were
not filtered or reclassified to make a passing result.

## T030 criterion evidence for this continuation

| Criterion | Status | Actual evidence |
| --- | --- | --- |
| 1. Explicit accepted artifact/root/URL/pins, fail closed, confinement/cleanup | PASS | D011 identity and all four pins supplied explicitly; root `web/build/out`; owned ephemeral loopback; actual response hashes match; real runtime error failed closed; all owned cleanup verified. |
| 2. Real diagnostics/map/yielding rendered frames | FAIL | Actual diagnostics available, but phase error before frame 1; no map or rendered-frame progress. No rendering PASS recorded. |
| 3. Normal input/Escape/blur/resume/positions | NOT RUN | Observer stopped on startup error before attempting lifecycle input. No gesture/motion/collision conclusion. |
| 4. No fixture substitute / no synthetic actual-game PASS | PASS | Actual lead-verified bundle used; no fixtures. `game_verified: false`, all actual-game gates remain NOT RUN. |
| 5. Existing tools/bounds/identity/trajectory/errors/cleanup | PASS | Actual Chrome 156.0.8078.80, Node v24.13.0, Playwright 1.62.1, Python 3.11.9; Darwin 25.5.0 arm64. Source hashes, exact command/argv, served files, first diagnostics and errors, browser/context/profile/server/port closure captured. |
| 6. Honest runtime handoff / follow-up needs | PASS | This immutable failed-run handoff and exact-error question preserve the failure without changing source or weakening checks. |

No runtime, T014/P0/MVP or eight-player acceptance is implied. Audio and
weapon/player models remain omitted in the approved map-only artifact. Multiplayer,
dedicated authority and performance are NOT RUN.

## Exact reproduction command and tools

Working directory: `/Users/jd1/code/apps/outbreak`.

```sh
node web/qa/game_probe.mjs --mode real --root web/build/out --url http://127.0.0.1:0/index.html --artifact-id 8792410f512392c628063109856fc3e65d97a037590ff0f9d376f4e70a8e637c --expect-file index.html=22b4e8d79b6032639783f075a2d7bed69dde780476b2889ae80cff19f34a1725 --expect-file index.js=0bfb0bc1c50c18ac5558a04c9dd2364b1465f6fb01630078b5e07f469d7a505f --expect-file index.wasm=3b3a7aa8674f8bdb6e827238c8d7c47b31e9861c4e86b7988a7187f7b906628b --expect-file index.data=66574ce6af122f6c10fdfa51c7030c6f25511bd0936f09d292e07f316cd30877 --output web/qa/results/T030-real-D011-1.json > web/qa/results/T030-real-D011-1.stdout.txt 2> web/qa/results/T030-real-D011-1.stderr.txt
```

Exit **1**. A future authorized repeat must choose a new output filename; these
historical results cannot be overwritten. Use new lead pins if the artifact changes.

Node path `/Users/jd1/.nvm/versions/node/v24.13.0/bin/node`; Playwright path
`/Users/jd1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.js`;
Chrome path `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.
The observer/server were inspected before execution, and remain unchanged
(`game_probe.mjs` SHA-256 `ef0c755c37b1293e493e1f653b411215d19d5407065a7e92249977cd7641f459`).
Chromium sandbox remained enabled; no unsafe GL/autoplay/pointer-lock/web-security
bypass flag was added. Automatic approval review permitted the exact D011 local run.

## Cleanup and remaining work

Actual root `/Users/jd1/code/apps/outbreak/web/build/out` was served by owned server
PID 61296 at `http://127.0.0.1:60887/` with a 60-second maximum lifetime. This
historical URL is now closed. Server exited 0; port closure was checked. Browser
PID 61271 stopped, its fresh temporary profile was removed and the isolated context
closed. No process-name/port-based kill or existing user profile was used.

New question: `notes/questions/T030-QA-D011-startup-signature-mismatch.md` asks MAIN
to assign the exact real startup error for diagnosis/fix and provide a newly
verified artifact if needed. Additional stack/symbol diagnostics require the
corresponding scoped direction. QA made no patch, source change, dependency
installation, artifact mutation or observer relaxation. D006 route implementation
and input work remain behind first successful startup and a later lead release.
