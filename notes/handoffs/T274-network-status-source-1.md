# T274 — Browser connection status source ready

- Worker: World /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket / revision: T2741.0, RELEASED D468; source stable, writes CLOSED for MAIN review.
- Phase / contract revisions: VISIBLE_SLICE0.6. Ticket and contract reread before submission; unchanged.
- Base commit and pre-existing edits: no Git operation authorized or performed. Existing accepted T261 page used as read; preserved layout, controls, bundle path, engine hooks and other existing behavior.
- Changed files: `web/visible/play.html`; this new handoff only.
- Commit or patch reference: working source; no commit authorized.

## Acceptance evidence

- PASS (source): existing public immutable `window.outbreakNetworkSnapshot()` read at most twice per second while initialized and visible. Inspected `client.cpp` bn_publish_json/bnpublish and `browsernet.h` state/error definitions. BN_OPENING → Connecting; BN_OPEN/BN_JOINING → Joining; BN_ACTIVE → Playing; BN_CLOSING → Closed; BN_FAILED or nonzero error → Connection failed. BN_IDLE waits for a connection; absent snapshot awaits client initialization. No readiness inferred from engine initialization.
- PASS (source): all existing error values 0–15 have fixed concise diagnostic descriptions. Only state/error transitions enter the bounded existing Client messages area; no snapshot serialization, counters, raw capability, boot data or exception reflection. Unknown/malformed observations fail visibly without echoing their contents.
- PASS (source): loading/abort/exit precedence retained; polling stops on failure, engine exit, pagehide and hidden visibility, and resumes only for an initialized visible page. No network lifecycle calls, engine/entity/Module state mutation, synthetic input/join/spawn, policy change or new dependencies.
- PASS (syntax only): canonical Python stdlib extracted the sole inline script to `/private/tmp/outbreak-T274-3g8eaunu.js`; `/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node --check /private/tmp/outbreak-T274-3g8eaunu.js` exited 0 with no output. The page script was parsed, never executed.
- NOT RUN: browser/runtime/network/render/input checks. No service, probe, install, Git or new test infrastructure. MAIN separately owns the next actual session; QA remains paused.

## Implementation status

Implemented read-only page status and lifecycle timer handling. No simulations/test doubles or gameplay fixes. Playing is a presentation of the engine's published BN_ACTIVE observation, not new render/input or phase acceptance evidence.

## Integration and questions

Only the existing public snapshot function is consumed; no shared interface changes or unresolved question. Reproduce syntax checking by extracting the sole inline script from play.html and passing that text to the fixed Node executable with `--check`. Actual network failure diagnosis and subsequent runtime remain separately owned.
