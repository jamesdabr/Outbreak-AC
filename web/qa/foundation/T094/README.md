# T094 measurement component preparation

Requires review of MVP/FOUNDATION_MEASUREMENT.md0.1, T0945.17 and private RESULT_SCHEMA.md. New source only; no old controller/QA/production integration. QA chat's human hold remains unchanged.

`measure.cjs` imports nothing and exports only async measureFoundation(page). The future supervisor supplies a genuinely joined network Page with approved source/artifacts/pins and handles external errors, GPU, process/RSS and global cleanup. This component reads only public snapshots/DOM/performance and issues the fixed ordinary Page sequence. It cannot launch/bootstrap/install/join/spawn or write game/Module state.

Fixed actions: validate map2/alive/running/reference viewport; bring page forward and canvas gesture if needed; relative mouse; W250/release; stationary state; W/Space/LMB100ms then Escape/release; ordinary neutral recapture;3s warmup;60s bounded rAF observation; LAST held inputs plus one owned blank tab. Only owned probe closes; original page remains untouched. Focus loss may legitimately fail to produce a real hidden transition and is then NOT_OBSERVED. No retry/connection reset or forcing visibility.

`test.cjs` uses only installed Node builtins and local source reads. No Playwright/package/process/socket imports or launch; all Pages/documents/clocks/rAF/heap/actions are fake. It extracts actual production foundation/diagnostics/timing/model/network/audio publishers with source hash verification and executes them in an isolated VM with explicit fake inputs. The measurement module is loaded in a VM without require/process/browser bindings. Every receipt/scenario is FIXTURE_ONLY/actual_browser:false; fake60s is not actual benchmarking. No physical capture/focus/visibility occurs.

The test creates one NEW prep-1 directory, refusing overwrite. Source inspection precedes its one invocation using the existing pinned Node24.19.0 executable. Preserve failure outputs; any authorized follow-up attempt uses a fresh owned directory. Final freeze checks source/tool/history preservation and records member hashes without another test run. No current browser/native artifact is built or run here.
