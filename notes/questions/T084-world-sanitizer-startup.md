# Installed sanitizer executable stalls before input

- Author / worker: World/Match-Systems
- Ticket and revision: T084 5.7
- Contract: PORTABLE_FORMAT_FOUNDATION 0.1 / D079
- Exact clause: actual installed native ASan/UBSan byte/memory coverage; missing runtime/flag requirements question first, no invented substitutes.
- Status: OPEN (lead resolution recorded separately)

## Question

May the identical inspected task-owned sanitizer executable be retried outside
the default filesystem/process sandbox, with its already recorded environment
and no new compiler/runtime flags? If that is inappropriate, please specify an
approved installed sanitizer/runtime diagnostic or classify this environment's
sanitizer gate as blocked pending a separate release. No waiver is inferred.

## Evidence and impact

All five attempt-1 build commands succeeded: installed Apple clang17 native and
ASan+UBSan native, SDKclang24 actual same production Wasm objects, direct LLD
link with explicit exports/no suppression/library fallback. Native batch0 output
matches the independent oracle. Sanitized batch0 timed out after60seconds with
no captured output. A second exact-command run with empty stdin also timed out
after10seconds with no stdout/stderr: this is before any corpus decoding.

Exact executable/environment/flags/tool hashes are recorded in
tests/outbreak/map-import/T084/attempt-1/plan.json; empty-input result in
sanitizer-empty-input.json. No services/install/SDK/global cache modification.
Timeout killed and reaped each task-owned child. Native/Wasm verification and
parser boundary tests can continue independently; sanitizer success cannot be
claimed from compilation or a timeout.

## Options for owner and lead

1. Authorize an identical unsandboxed local sanitizer retry (recommended if the
   sandbox is the cause), task-owned input/output/cache only, no network.
2. Supply an approved installed runtime/diagnostic command and exact flags.
3. Keep sanitizer coverage blocked while reviewing native/Wasm evidence; this
   does not satisfy or waive the required sanitizer acceptance gate.

## Work paused

Further sanitizer execution/runtime-flag changes and final PASS submission wait
for resolution. Production decoder/native/Wasm/corpus work may continue within
the existing release. No contract or status changed.
