# T030 D016 corrected actual-engine run — memory trap

- Worker: QA/Performance / `01a1b92d-28be-7110-9ac6-7ae01476c117`
- Ticket: T030 revision 0.5 actual-run continuation under D016
- Artifact: `T040-3800e5ef78bcb84033e30c72e276ebebc342b6f97185fbfcb434de021d87a7ab`
- Authorization/pins read: `D016-corrected-browser-run.md`, `D016-corrected-browser-artifact.json`
- Source/observer/build/assets changed: none
- New files: `web/qa/results/T030-real-D016-1.json`, `.stdout.txt`, `.stderr.txt`; this handoff and `notes/questions/T030-QA-D016-memory-out-of-bounds.md`
- Execution: 8 November 2026, 00:23 America/New_York; UTC start `2026-11-08T05:23:56.866Z`
- Exit: **1 / FAIL**; `game_verified: false`; all actual-game gates NOT RUN

## Actual result

The corrected engine reached its original map-read log, then trapped before the
first frame with **`RuntimeError: memory access out of bounds`**. The unchanged
accepted observer stopped at `real_observation`, code `runtime_error`.

```json
{"schema_version":1,"profile":"offline-map","phase":"error","frame_count":0,"rendered_frame_count":0,"map_name":"","player_position":[0,0,0],"input_locked":false,"runtime_errors":["RuntimeError: memory access out of bounds"]}
```

Full captured exception stack:

```text
RuntimeError: memory access out of bounds
    at http://127.0.0.1:49445/index.wasm:wasm-function[3179]:0x1714c9
    at http://127.0.0.1:49445/index.wasm:wasm-function[3202]:0x174f63
    at http://127.0.0.1:49445/index.wasm:wasm-function[1694]:0xaf316
    at http://127.0.0.1:49445/index.wasm:wasm-function[775]:0x31048
    at http://127.0.0.1:49445/index.wasm:wasm-function[2001]:0xcc072
    at http://127.0.0.1:49445/index.wasm:wasm-function[1064]:0x4dbd4
    at callMain (http://127.0.0.1:49445/index.js:1:339160)
    at run (http://127.0.0.1:49445/index.js:1:339618)
```

No symbolic source-callsite attribution is claimed. The earlier signature
mismatch is not the first captured failure here; this does not establish complete
recovery from the earlier startup defect or any running-game acceptance.

Captured informational startup messages, in order:

```text
private/entropy.dat not found.
..restart AssaultCube for this setting to take effect
OFFLINE_MAP omissions: no bots, HUD weapon/local character model preload, or audio backend. Not P1/MVP acceptance.
Master/LAN services unavailable in offline browser profile
Renderer: WebKit WebGL (WebKit)
Driver: OpenGL ES 2.0 (WebGL 1.0 (OpenGL ES 2.0 Chromium))
read map packages/maps/dev_outbreak_browser.cgz rev 1 (32 milliseconds)
Outbreak original browser courtyard proof
```

The observer's `console_info` retains `[log]` prefixes in raw evidence. The map
loader log is not proof of successful map startup: diagnostics never reported a
running map or rendered frame.

## Delivery and secondary evidence

All four on-disk runtime files matched the exact D016 pins before launch. The
server recorded GET 200 for only index.html/index.js/index.data/index.wasm, with
no blocked/external request. Browser response hashes for HTML, JS and Wasm match
the lead pins. `index.data` response-body hash was **not captured**: the saved
evidence contains `ERR_ABORTED` and Playwright's `Network.getResponseBody` error
`No data found for resource with given identifier` / response body not available
after navigation. This might involve the failed-run lifecycle, but cause/timing
is not established by these untimestamped callback records. No four-response
integrity PASS or clean-network claim is made for this run.

Console errors remain unfiltered: two Emscripten GL emulation warnings and
`TODO: glShadeModel`. Console warnings contain two WebGL INVALID_ENUM hint-target
entries. They are preserved separately from the actual memory trap; causation is
not inferred. No exception swallowing, warning allowlist, source fix or observer
relaxation was performed.

## Per-criterion continuation evidence

| T030 criterion | Status | Evidence |
| --- | --- | --- |
| 1. Exact artifact/root/URL/pins, fail closed, local confinement/cleanup | PASS for execution guards; response delivery incomplete | Exact D016 identity/four local pins passed preflight; actual runtime trap failed closed; owned loopback and cleanup passed. Three response hashes match, data response-body verification NOT RUN/failed capture as documented. |
| 2. Real phase/frame/render/map/player/input observations | FAIL | Actual phase error/memory trap; zero frames/rendered frames, empty diagnostic map. Loader log does not replace running/render evidence. |
| 3. Input/focus/Escape/resume/motion/collision | NOT RUN | Startup failure preceded all lifecycle interactions. |
| 4. Real provenance, no fixture/synthetic game PASS | PASS | Actual lead-verified engine artifact, no fixtures; all game gates NOT RUN, game_verified false. |
| 5. Bounded tools/identity/trajectory/full errors/cleanup | PASS | Accepted T037 observer captured full stack, startup info, console and secondary request/body errors. All created resources closed. |
| 6. Honest evidence/follow-up | PASS | New immutable failed-run result and exact-error question; no unapproved rebuild, patch or repeat. |

Audio/player/weapon models remain omitted by the current profile. Multiplayer,
authority, performance and T014/P0/MVP acceptance remain unverified.

## Exact command and identities

Working directory `/Users/jd1/code/apps/outbreak`:

```sh
node web/qa/game_probe.mjs --mode real --root web/build/out --url http://127.0.0.1:0/index.html --artifact-id T040-3800e5ef78bcb84033e30c72e276ebebc342b6f97185fbfcb434de021d87a7ab --expect-file index.html=22b4e8d79b6032639783f075a2d7bed69dde780476b2889ae80cff19f34a1725 --expect-file index.js=0bfb0bc1c50c18ac5558a04c9dd2364b1465f6fb01630078b5e07f469d7a505f --expect-file index.wasm=6165af498f65cc7a51a877801679978a5672fea7c78f27c1ae143cd09c1ab229 --expect-file index.data=66574ce6af122f6c10fdfa51c7030c6f25511bd0936f09d292e07f316cd30877 --output web/qa/results/T030-real-D016-1.json > web/qa/results/T030-real-D016-1.stdout.txt 2> web/qa/results/T030-real-D016-1.stderr.txt
```

Actual tools: installed Chrome 156.0.8078.80, bundled Playwright 1.62.1, Node
v24.13.0, Python 3.11.9; Darwin 25.5.0 arm64. Executable/module paths and actual
browser argv are in JSON. Accepted observer SHA-256:
`bce6370ccb9c98f1ee505019dddf217b7b2071f8f07739e0842930e90ccf953c`.
Normal accepted launch profile and Chromium sandbox retained; no security/input/
autoplay/unsafe GPU bypass added. Automatic review permitted the exact released
local run; no tool install or public service was used.

Owned server PID 65392 served explicit root
`/Users/jd1/code/apps/outbreak/web/build/out` at
`http://127.0.0.1:49445/`, with 60-second maximum lifetime. It exited 0 and its port
checked closed. Browser PID 65366 stopped; its isolated temporary profile was
removed and context closed. Historical URL is no longer live. No broad kill or
user-profile access occurred.

## Next integration need

MAIN should assign the captured memory-trap stack for diagnosis, with explicit
symbol/debug scope if needed, and supply new verified pins for any rebuilt output.
The question note records the concrete error without guessing a source cause.
D011, T037 and all earlier evidence remain unchanged. No new code or route
implementation is authorized or performed by this actual-run continuation.
