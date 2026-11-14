# T019 fixture-verified QA infrastructure handoff

- Worker: QA/Performance / `01a1b92d-28be-7110-9ac6-7ae01476c117`
- Ticket / revision: T019 revision 0.3 RELEASED; submitted for lead review without changing authoritative status
- Phase / contract revisions: P0 0.3 prerequisite subset; BROWSER_FOUNDATION 0.3; GOVERNANCE 0.3; MVP README 0.3; product/parameters/interfaces 0.2 remain draft context
- Base commit and pre-existing edits: `13f0d8eea4822dee5c976661218d022be74342e3`, D003 source baseline preserved. `web/qa` did not exist at assignment. Eight protected prototype files still match D003 SHA-256 values; see `web/qa/results/submission-state.json`. Other workers' allowed `main.cpp`, `platform.h`, `tools.h` changes were observed and left untouched.
- Changed files: only the exact T019 allowlist and this worker's own notes, listed below
- Commit or patch reference: none; no branch/worktree/commit/push/reset/revert performed
- Evidence execution: 7 November 2026, approximately 23:11–23:15 America/New_York; raw JSON timestamps use UTC on 8 November

## Acceptance evidence

| T019 criterion | Status | Evidence |
| --- | --- | --- |
| 1. Discover Python/Node/Playwright/browser candidates and source/output state without repo binaries or environment installation | PASS | `web/qa/results/preflight-authorized.json`: Python 3.11.9, Node v24.13.0, bundled Playwright 1.62.1, candidate existence, selected Chrome executable, actual browser version/launch/cleanup, source present and `web/build/out` absent. No game binary or installer ran. Deliberately absent browser/module paths produce NOT RUN/exit 2 in `negative-missing-browser.json` and `negative-missing-module.json`; verification summary confirms no browser launched for those checks. |
| 2. Static-server confinement/MIME/error/method regressions | PASS | `web/qa/results/server-tests-authorized.txt`: 12 tests, OK, exit 0. GET/HEAD, query strings, Wasm/JS/MJS/JSON/data MIME, no-cache/no wildcard CORS, missing paths/no success HTML fallback, no listings/writes, nonloopback rejection, traversal/percent/double encoding, outside file/directory symlinks, internal symlink and optional named isolation profile covered. Only new temporary and QA fixtures used. |
| 3. Explicit-root loopback startup, bounded ports and owned cleanup | PASS | Lifecycle test: PID 38625, `http://127.0.0.1:51818/`, explicit QA fixture root, exit 0, port closed. Fixture suite: PID 39151, `http://127.0.0.1:52268/`, same root, exit 0, port closed. Logs in `server-tests-authorized.txt`, `fixture-server.txt`, `fixture-verification.json`. Explicit root/port required; invalid bounds and occupied port fail without stopping the existing owner. CLI duration is bounded. |
| 4. Existing-browser healthy and intentional failure fixtures | PASS | `ok.json`: PASS/exit 0. `error.json`: FAIL/exit 1 with intentional page exception. `missing.json`: FAIL/exit 1 with HTTP 404 captured. Every fixture has visible/metadata FIXTURE ONLY labels, `game_verified: false`, six NOT RUN game gates and owned browser cleanup. These are fixture verification results only. |
| 5. Reject external requests/navigation and bound timeouts | PASS | `external.json`: Fetch, iframe document navigation and WebSocket attempts to `t019-external.invalid` intercepted; request failures report `ERR_BLOCKED_BY_CLIENT`; run fails/exit 1. HTTP routing aborts before external dispatch and WebSocket routing never connects to a server. `timeout.json`: intentional completion timeout at 1500 ms, exit 1, total observed run 2.211 s, owned browser stopped. `fixture-verification.json` confirms expected exits and server cleanup. Remote initial URL is rejected before browser launch in `negative-remote-url.json`. |
| 6. Partial handoff if no usable browser is available | NOT RUN | Conditional fallback does not apply: installed Chrome launched successfully in the authorized execution context. No browser install is needed. Missing-dependency NOT RUN behavior was separately verified using intentionally nonexistent paths. |
| 7. Exact commands and separation of fixture/game evidence | PASS | `web/qa/README.md` documents preflight, server tests, explicit-root serving, each fixture command/expected exit, dependency selection, sandbox behavior, cleanup, output schema and future actual-game prerequisite boundary. No real-game or performance gate is claimed. |

Initial sandbox attempts failed to bind (`Operation not permitted`) and Chrome
aborted. They are retained in `results/server-tests.txt`, `preflight.json` and
`preflight.txt`, rather than described as passing evidence. The inspected,
ticket-authorized loopback/browser commands were then allowed through automatic
approval review and rerun successfully. No automatic approval rejection remains.

### Exact tools and principal commands

Working directory: `/Users/jd1/code/apps/outbreak`.

- Python: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3`, 3.11.9
- Node: `/Users/jd1/.nvm/versions/node/v24.13.0/bin/node`, v24.13.0
- Playwright module: `/Users/jd1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.js`, 1.62.1
- Browser: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`, actual launched version 156.0.8078.80
- Host: macOS 26.5.1 arm64, Darwin 25.5.0. No hardware/performance acceptance claim is made.
- Playwright-managed Chromium and standalone Chromium app candidates were absent; installed Chrome was usable. This observed setup does not freeze a support matrix or prove WebGL.

```sh
python3 -B web/qa/tests/test_serve.py > web/qa/results/server-tests-authorized.txt 2>&1
python3 -B web/qa/preflight.py --source-root . --output-root web/build/out --output web/qa/results/preflight-authorized.json > web/qa/results/preflight-authorized.txt 2>&1
git diff --check
```

These commands exited 0 on the authorized retries; `git diff --check` emitted no
errors. The exact absolute server and five Node smoke command arrays, including
the ephemeral URL and every parameter, are retained in
`web/qa/results/fixture-verification.json`. Its server command was:

```sh
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B /Users/jd1/code/apps/outbreak/web/qa/serve.py --root /Users/jd1/code/apps/outbreak/web/qa/tests/fixtures --port 0 --duration 120
```

For example, the healthy fixture command was:

```sh
node /Users/jd1/code/apps/outbreak/web/qa/smoke.mjs --mode fixture --url http://127.0.0.1:52268/ok.html --root /Users/jd1/code/apps/outbreak/web/qa/tests/fixtures --artifact-id T019-FIXTURE-ONLY-ok --output /Users/jd1/code/apps/outbreak/web/qa/results/ok.json --timeout-ms 1500 --observe-ms 500
```

The other suite commands substitute `error`, `missing`, `external` and `timeout`
for `ok` in the URL, artifact identity and output path; each must exit 1. These
historical ports are now closed. README commands use a newly started explicit
fixture server on port 8765 or its newly emitted ephemeral URL.

### Cleanup and evidence ownership

Browser probe PID 39056 and fixture browser PIDs 39153, 39186, 39219, 39253 and
39294 report `browser_stopped: true`. Each run owns its temporary browser profile
and BrowserServer; close/kill is scoped to that returned object/process only.
The loopback browser-control listener is also owned and closed by BrowserServer.
Fixture-server PID 39151 was terminated through its own subprocess handle, exited
0 and its port was checked closed. Temporary server regression roots were cleaned.
No kill-by-name or kill-by-port command was used.

## Implementation status

Implemented:

- stdlib tool/root preflight and bounded isolated browser launch probe;
- read-only, no-cache, numeric-loopback-only explicit-root development server;
- path decoding/confinement and no-follow file opening, MIME/error handling,
  optional named COOP/COEP profile and bounded service lifetime;
- isolated Playwright smoke runner with explicit mode/root/identity/URL,
  document-byte identity check, fixture label inspection, request blocking,
  diagnostics, bounded observation and deterministic exits;
- positive/negative fixtures, server regressions and reproducible local commands.

Simulated/test-only behavior:

- HTML fixtures and their private button/completion marker;
- synthetic intentional JS error, missing file, external attempts and timeout;
- `.wasm`/`.data` MIME payloads are labeled text probes, not compiled code/assets;
- fake absent executable/module paths verify fallback reporting only.

Incomplete / NOT RUN:

- actual-game rendering, controls/focus/pointer lock, audio, multiplayer,
  dedicated-server authority, load/profiling/performance, and browser matrix gates;
- WebGL usability and human keyboard/mouse/audio behavior;
- actual-game behavioral observations, pending lead-frozen expectations and T014
  artifact identification. The harness currently leaves these NOT RUN even if a
  later game static page loads; it does not invent a game observation API.

Fixture elapsed timings are harness durations, not measured game frame times or
performance acceptance. This handoff does not accept T014, T015, P0 or the MVP.

### Changed files

- `web/qa/preflight.py`, `serve.py`, `smoke.mjs`, `README.md`
- `web/qa/tests/test_serve.py`
- `web/qa/tests/fixtures/ok.html`, `error.html`, `missing.html`, `external.html`,
  `timeout.html`, `fixture.js`, `fixture.json`, `fixture.wasm`, `fixture.data`
- `web/qa/results/**`: preflight/test/fixture stdout/stderr/JSON evidence,
  negative-case evidence and submission-state hashes
- `notes/questions/T019-QA-actual-game-observations.md`
- this handoff

No shared game interface, source, build output, runtime, asset manifest,
AGENTS/MVP/ticket/decision file was modified by QA. The source/output state and
final QA file hashes are recorded in `results/submission-state.json`. Governing
ticket/contracts were reread before submission and remain at assigned revision
0.3. No overlapping edit was observed under QA's allowlist.

## Integration and questions

`notes/questions/T019-QA-actual-game-observations.md` requests the exact future
T014 artifact identity/root/document and approved behavioral expectations. It
blocks only actual-game observation work, not review of this infrastructure.

No dependency or browser installation, external service, public binding, account
access, user browser profile or native game profile was used. Bundled runtime
metadata and authored scripts were inspected before execution. The server was
served only from the explicit QA fixture root and newly created temporary test
roots. Only the lead may accept this infrastructure submission or release later
game tests.
