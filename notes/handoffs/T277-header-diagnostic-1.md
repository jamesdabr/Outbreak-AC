# T277 — Fixed first-failed-header diagnostics

- Engine /01a1b92b-53f9-7132-aeb9-72b637ac3a90; T2771.0, EXPERIMENTAL_TRANSPORT0.3 / VISIBLE_SLICE0.8 / D474.
- Changed: `web/transport/gateway.cjs`, `web/visible/gateway_local.cjs`, this new handoff; pure-check entry `/private/tmp/outbreak-T277-check.cjs`. Existing source/history preserved outside these localized changes. No Git action.

## Implemented

Added private pure `firstFailedAdmissionHeader(req,h,seen)` returning only the twelve approved fixed field labels or null, in the original predicate's order and with identical expressions. The actual admission condition remains textually unchanged. Its failure body now records `admission_header_<literal>` immediately before the original `reject(t,'admission_headers')`. Duplicate-header handling still occurs before this gate. No header values, URLs, keys, credentials, capabilities or exceptions are logged.

The isolated wrapper retains its prior summary keys/counts and adds twelve zero-initialized fixed reason slots: method, host, origin, version, protocol, upgrade, connection, key, extensions, cookie, authorization and proxy_authorization, each prefixed `admission_header_`. Existing counting logic populates them from bounded diagnostics. No new exports/imports, dependencies, snapshot schema, admission allowance, socket handling or cleanup changes. Existing diagnostic overflow behavior and summary/run bounds remain.

## Actual verification

Inspected the temporary check before its one execution. All three commands used the fixed Node executable `/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node` under `env -i PATH=/usr/bin:/bin NODE_OPTIONS= WS_NO_BUFFER_UTIL=1 WS_NO_UTF_8_VALIDATE=1`:

```sh
NODE --check web/transport/gateway.cjs
NODE --check web/visible/gateway_local.cjs
NODE /private/tmp/outbreak-T277-check.cjs
```

`NODE` above abbreviates that exact executable, not a shell variable or PATH lookup. Both syntax checks exited0. The pure check exited0:

```json
{"status":"PASS","cases":175,"retained_predicate":"exact","decision_order_and_exceptions":"equal","fixed_summary_slots":26,"project_modules_invoked":0,"sockets":0}
```

The check reads source, extracts only constants/helper into a bounded VM, verifies the retained old condition verbatim, and compares helper decisions/property-read order/exception classes against that condition. Cases cover valid absent-extension and exact-standard-offer requests, allowed header casing/connection token combinations, every individual failure, all failure pairs and a combined failure, plus missing/falsy/truthy/non-string values. It also checks all prior and added wrapper slots and their small serialized size. No gateway/module startup, real project require, socket, timer, native/browser/component suite, FFI or probe was invoked. Check completed within the5s/1MiB allowance; tool output was one short result line.

## Pending

This is diagnostic source, not identification of local5's actual failed field: that value was never retained. MAIN's separately released fresh session should produce one `admission_header_*` count alongside the unchanged `admission_headers` count. No security/pointer-lock or other engine fix is inferred. QA remains paused. Stable source submitted; stopping for review.
