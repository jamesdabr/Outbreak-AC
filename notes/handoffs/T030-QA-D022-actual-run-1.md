# T030 D022 real running-map/input evidence — strict run still FAIL

- Worker: QA/Performance / `01a1b92d-28be-7110-9ac6-7ae01476c117`
- Ticket: T030 0.5 continuation under D022; existing accepted T037 observer unchanged
- Artifact: `T040-24f41b7c5e1c9eafa5b72e31cb5bddb2a40a405a7d1f1f772bc437cbfbb1d2e0`
- Exact release/pins read: `D022-world-ownership-browser-run.md`, `D022-world-ownership-browser-artifact.json`
- Execution: 8 November 2026, 00:37 America/New_York; UTC start `2026-11-08T05:37:21.484Z`
- New files: `web/qa/results/T030-real-D022-1.json`, `.stdout.txt`, `.stderr.txt`; this handoff and own exact-issue question
- Source/observer/build/assets/contract changes: none; no commit/push/reset/revert

## Actual outcome

**FAIL, exit 1**, observer code `browser_errors`: Console/page/network errors
present. The actual runtime nevertheless reached a running original map and input
observations for the first time. Preserve these distinct findings; do not promote
partial recovery to correct rendering or full game acceptance.

- All **23** trajectory samples are phase `running`, profile `offline-map`, map
  `dev_outbreak_browser`, finite positions and empty runtime_errors.
- First frame/render sample **5/2**, then **9/6**, **12/9** across separate browser
  turns; final **138/135** after input. These are real engine diagnostic counters
  after draw returns, not a pixel-correctness/performance result.
- No page exception or exception stack was captured. D016's memory trap did not
  recur during this run; no broader memory-safety conclusion is inferred.
- All four response hashes match exact D022 pins. Only those four local files
  were requested; no blocked/failed request or HTTP/body-capture failure occurred.
- Raw result remains `game_verified: false` and every actual-game gate NOT RUN,
  because the final strict error check failed. No gate or warning was altered.

### Concrete browser diagnostics

| Raw diagnostic | Count | Recorded category |
| --- | --- | --- |
| WARNING: using emscripten GL emulation. This is a collection of limited workarounds, do not expect it to work. | 1 | console_errors |
| WARNING: using emscripten GL immediate mode emulation. This is very limited in what it supports | 1 | console_errors |
| TODO: glShadeModel | 1 | console_errors |
| WebGL: INVALID_ENUM: hint: invalid target | 2 | console_warnings |
| WebGL: INVALID_ENUM: readPixels: invalid format | 135 | console_warnings |
| GL_INVALID_OPERATION: glDrawElements: Vertex buffer is not big enough for the draw call. | 23 | console_warnings, with browser WebGL object prefix |

The existing strict failure check counts console_errors; it does not silently
allow the SDK warnings. Repeated concrete GL warnings are separately material
renderer evidence even though they arrive at warning level. No image correctness,
geometry/model/HUD completeness or visual regression PASS is claimed from counters.
No source-cause attribution or screenshot/visual inspection was performed.

Startup info includes original map reads, loaded-textures/mapmodels/mapsounds
messages and DM mode; it also logs `map dev_outbreak_browser does not support game
mode deathmatch` before another map read. The raw ordered 19-entry console_info
array is preserved; no omission/mode message was suppressed or treated as a
successful missing feature.

### Normal input observations

| Step | Actual evidence |
| --- | --- |
| Spawn | Position `[48,32,4.5]`, matching the right-side original approach. No teleport/state injection. |
| Canvas click | Diagnostic lock true and browser pointerLockElement is canvas, frame/render 23/20. |
| Fresh W | x 48 → 45.67733 at y 32, frame/render 38/35. |
| Fresh S | x 45.67733 → 46.52384 at y 32. |
| Fresh A / D | Horizontal/strafe positions change; A ends `[47.82430,34.35085,4.5]`, D ends `[47.98215,33.43816,4.5]`. Existing momentum means these are observations, not calibrated displacement bounds. |
| Escape | Browser lock false and diagnostic lock false, frame/render 91/88. |
| Attempted blur while W held | Tab-switch test sampled browser focus true/visibility visible. It did not establish an observable blur. Diagnostic/browser lock were false, but this cannot certify held-key release on blur. |
| Resume click | Browser pointer capture reacquired; diagnostics briefly lagged then lock true by frame/render 113/110. |
| Fresh W after resume | Position `[47.99973,31.95400,4.5]` → `[45.64915,31.92394,4.5]`, frame/render 131/128. |
| Post-input frames | Continued to frame/render 138/135 with finite position `[44.61441,31.92140,4.5]`. No collision assertion inferred from motion. |

Real blur/held-key release and D006 wall/door-route collision checks remain
**NOT RUN**. The unchanged observer reports those limitations. Audio and player/
weapon models remain omitted; multiplayer, authority, performance and headed/
human support matrix are unverified. No fake input policy/security flags were used.

## Per-criterion continuation evidence

| T030 criterion | Status | Meaning |
| --- | --- | --- |
| 1. Exact artifact/root/URL/pins, fail closed, confinement/cleanup | PASS | All four actual response hashes match; error check remained strict; owned numeric-loopback resources cleaned. |
| 2. D005 real map/frame/position progression | PASS for narrow diagnostic observations; rendering gate NOT RUN | Actual original map and yielding counters observed, no exception, but GL diagnostics prevent rendering acceptance. |
| 3. Normal input/focus lifecycle | NOT RUN as a complete criterion | Click/movement/Escape/reacquisition/fresh-resume observations above succeeded; blur/held-key proof and collision remain incomplete. |
| 4. No synthetic substitute/gate promotion | PASS | Actual accepted artifact only, no fixture; raw gates remain NOT RUN. |
| 5. Bounded tools, full errors/info/trajectory/cleanup | PASS | Raw 23-sample trajectory and unfiltered diagnostics retained; all owned cleanup passed. |
| 6. Honest follow-up | PASS | Exact renderer/focus issues recorded in new question; no code change/filter/repeat to manufacture pass. |

## Exact command / source / cleanup

Working directory `/Users/jd1/code/apps/outbreak`:

```sh
node web/qa/game_probe.mjs --mode real --root web/build/out --url http://127.0.0.1:0/index.html --artifact-id T040-24f41b7c5e1c9eafa5b72e31cb5bddb2a40a405a7d1f1f772bc437cbfbb1d2e0 --expect-file index.html=22b4e8d79b6032639783f075a2d7bed69dde780476b2889ae80cff19f34a1725 --expect-file index.js=0bfb0bc1c50c18ac5558a04c9dd2364b1465f6fb01630078b5e07f469d7a505f --expect-file index.wasm=2718f7c49ddd7fa056f304222ce916021bface86c46c32c93adcb05e9e18cddd --expect-file index.data=66574ce6af122f6c10fdfa51c7030c6f25511bd0936f09d292e07f316cd30877 --output web/qa/results/T030-real-D022-1.json > web/qa/results/T030-real-D022-1.stdout.txt 2> web/qa/results/T030-real-D022-1.stderr.txt
```

Exit 1. Actual tools Chrome 156.0.8078.80, bundled Playwright 1.62.1, Node
v24.13.0, Python 3.11.9; Darwin 25.5.0 arm64. Executable paths/argv are in JSON.
Observer hash unchanged:
`bce6370ccb9c98f1ee505019dddf217b7b2071f8f07739e0842930e90ccf953c`.
No new dependency/browser, unsafe GL/autoplay/pointer-lock/security bypass or source
mutation. Exact released run passed automatic execution review.

Owned browser PID **69206** stopped, isolated temporary profile removed and context
closed. Owned server PID **69228** exited 0, explicit real artifact root
`/Users/jd1/code/apps/outbreak/web/build/out`; bound
`http://127.0.0.1:56463/`, port verified closed. No unrelated process touched.
This historical URL is no longer live. Run observation lasted 2612 ms; it is not
a frame-rate/latency benchmark.

## Integration

New question: `notes/questions/T030-QA-D022-renderer-errors-and-blur.md`. MAIN should
assign exact renderer diagnosis and any later focus/route observation scope; QA
did not patch or weaken the observer. D011/D016 failures remain immutable. T044
static dependency report work was retained during this priority run. No T014,
P0, multiplayer or full MVP acceptance follows from this partial real progress.
