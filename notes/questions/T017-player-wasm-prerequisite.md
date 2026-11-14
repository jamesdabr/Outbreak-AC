# T017 actual Wasm translation-unit check lacks the pinned SDK

- Author / worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket and revision: T017 revision 0.3 RELEASED
- Phase and contract revision: P0 revision 0.3 prerequisite subset; BROWSER_FOUNDATION revision 0.3
- Exact clause or interface affected: Acceptance criterion 5 and authorized execution scope (consume lead-accepted T016 compiler configuration; no SDK install authorized here).
- Status: OPEN (lead resolution is recorded separately)

## Question

When T016 has an accepted configuration and authorized ready SDK/cache, please identify the approved actual `main.cpp` Wasm compile invocation with task outputs under `/private/tmp/outbreak-t017-*`.

## Evidence and impact

After reading `web/build/preflight.py`, `compile_probe.py` and `probe-config.json`, ran the read-only `PYTHONDONTWRITEBYTECODE=1 python3 web/build/preflight.py --json`, saving output to `/private/tmp/outbreak-t017-checks/wasm-preflight.json`. It returned exit 1, `missing_prerequisites`: pinned Emscripten 7.0.0 tool executables, version file and local `.emscripten` configuration are absent at `/private/tmp/outbreak-web-sdk`. No compiler, downloader, installer or SDK activation was run. The current T016 configuration probes `clientgame.cpp`, not `main.cpp`, and was still worker-owned work in progress at inspection. This is not accepted Wasm evidence for T017.

Native syntax checks and task-local helper/source checks continue independently. The full actual Wasm TU check is NOT RUN/BLOCKED. Browser linkage and integrated runtime are separate T014 work regardless.

## Options for owner and lead

1. Provide/accept T016's exact compiler configuration and scoped ready SDK/cache, then re-release/assign the remaining T017 compile step as appropriate.
2. Review the source/native/helper handoff as partial while the SDK remains unavailable. This does not waive criterion 5 or accept browser readiness.

## Work paused

Actual Wasm compilation only; no SDK installation or acquisition is attempted by this worker.
