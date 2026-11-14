# T017 revision 0.4 actual Wasm verification remains unavailable

- Author / worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket and revision: T017 revision 0.4 RELEASED
- Phase and contract revision: P0 / BROWSER_FOUNDATION / GOVERNANCE revision 0.4; D004
- Exact clause or interface affected: Acceptance criterion 5; D004 remaining-work paragraph permits no SDK/installer/port execution without a reviewed command.
- Status: OPEN (lead resolution is recorded separately)

## Question

The source clock follow-up is complete. Actual `main.cpp` Wasm compilation still needs the ready pinned SDK and reviewed lead-provided invocation. This follows the routing in D004 and the historical T017-player-wasm-prerequisite question; it is not a request to install or execute an installer here.

## Evidence and impact

Read current `web/build/preflight.py` before running `PYTHONDONTWRITEBYTECODE=1 python3 web/build/preflight.py --json`. Exit 1; report `/private/tmp/outbreak-t017-r04/wasm-preflight.json` says `missing_prerequisites`: Emscripten 7.0.0 tool executables/version and local `.emscripten` config absent under `/private/tmp/outbreak-web-sdk`. No compiler/installer/port fetch was executed. Native release/debug syntax, wired-frame fixture, lifecycle fixture and protected-source checks pass independently.

## Options for owner and lead

Continue D004's T022 inspect-first SDK route, then supply the reviewed compiler command when available. Review the new T017-player-2 handoff as source/native/helper evidence in the meantime; actual Wasm remains NOT RUN and cannot be waived by this worker.

## Work paused

Actual Wasm TU compilation only. T014 integrated browser/game checks remain unperformed under their separate unreleased integration scope.
