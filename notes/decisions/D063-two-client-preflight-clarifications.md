# D063 Two-client preparation clarifications

MAIN source review of pending T067 found two prelaunch requirements: parent must retain proven browser ownership when Node fails before final JSON, and actual artifact dependencies must name T070/T072 acceptance rather than treating T066 tooling as a full build. Both preserve existing acceptance obligations.

The static server may return exactly GET /favicon.ico204 with no body, matching accepted T063 browser.cjs32. Current network shell has no icon; the browser's incidental request must not create a needless404 console error. No new file is served or game error hidden. Exact runtime/notices routing and all other unknown-route rejection remain. T067 revision4.2 records these clarifications; worker must re-read before final freeze. No game execution or pending artifact acceptance granted.
