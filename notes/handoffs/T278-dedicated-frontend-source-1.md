# T278 — Dedicated frontend hostname

Engine /01a1b92b-53f9-7132-aeb9-72b637ac3a90; T2781.0 / D476; EXPERIMENTAL_TRANSPORT0.4, EXPERIMENTAL_BROWSER_BACKEND0.3, VISIBLE_SLICE0.9.

## Implemented

Only two project sources changed:

- `web/transport/gateway.cjs`: added fixed `FRONTEND_HOST='outbreak.localhost'`, changed the accepted Origin to `http://outbreak.localhost:29866`, and used the frontend constant in the actual Host predicate and first-failed-header helper. Socket bind/source/backend constant `HOST='127.0.0.1'` and UDP port29863 remain unchanged.
- `web/transport/enet_websocket.js`: exact immutable boot endpoint is now `ws://outbreak.localhost:29865/enet`; required page origin is `http://outbreak.localhost:29866`. No numeric-host or other alias fallback.

The diff is one constant declaration, two Host comparisons and two bridge string literals. Cookie/Authorization/Proxy-Authorization rejection, original diagnostic labels/order, cap/replay validation, protocol/extensions, queues, timers, error semantics, exports and cleanup were preserved. Logical ENet destination remains127.0.0.1:29863. No cookies read/cleared, DNS API, settings, selector, dependency, visible-source or old-candidate changes. MAIN's source backups were not touched; no Git actions.

## Verification performed

Inspected `/private/tmp/outbreak-T278-check.cjs` before its one finite execution. Fixed executable `/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node`, clean environment `env -i PATH=/usr/bin:/bin NODE_OPTIONS= WS_NO_BUFFER_UTIL=1 WS_NO_UTF_8_VALIDATE=1`:

```sh
NODE --check web/transport/gateway.cjs
NODE --check web/transport/enet_websocket.js
NODE /private/tmp/outbreak-T278-check.cjs
```

`NODE` abbreviates the exact executable above. All exited0; actual pure result:

```json
{"status":"PASS","gatewayCases":33,"bootCases":18,"loopbackBackend":"unchanged","browserBoundary":"SIMULATED","realSockets":0,"projectModulesStarted":0}
```

The check extracts the actual gateway condition/helper and evaluates them without loading gateway imports or calling startGateway. It accepts exact new Host/Origin with absent or standard extension offer, rejects numeric/other/case/port/origin variants, every other header failure and present-but-empty/falsy cookie/credential headers. It checks unchanged listener/UDP bind/connect/source expressions and C-bridge numeric destination guards.

The actual JS-library source is loaded only into a bounded VM with inert WebSocket/document/timer boundaries. Its real boot validator accepts the new endpoint/origin and constructs the expected synthetic URL/subprotocol, rejects old/other endpoints/origins and bad/missing/extra/accessor/nonplain boot data before the fake constructor, retains error1 for invalid boot, error2 for a simulated constructor failure and error13 for repeated open. This is labeled simulation, not browser/connection evidence. One short output line, within5s/1MiB; no real socket/process/FFI/browser/Wasm/compiler/component-suite effects.

## Pending

New browser candidate/rebuild and a fresh actual session remain MAIN's separate work. Actual reserved-host resolution, cookie isolation, no-cookie admission, genuine native join/spawn, pointer capture and visible character/movement are **NOT RUN here**. No claim the hostname has already fixed runtime. QA remains paused. Stable source submitted; stopping.
