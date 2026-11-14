# T083 sanitizer first-batch timeout after D080 launcher correction

- Author / worker: Engine & Multiplayer
- Ticket/revision: T0835.6 / D079/D080
- Contract: PORTABLE_FORMAT_FOUNDATION0.1 section A and tools/evidence gate
- Exact affected clause: actual installed ASan/UBSan execution; question any further missing runtime/flag requirement
- Status: OPEN; only sanitizer execution blocked, native independent comparisons continue

## Question

D080's T083 launcher correction compiled the actual native and ASan/UBSan
executables successfully in new attempt-2. The first sanitizer batch timed out
at60s under the default process sandbox. No retry, alternate flag/runtime,
suppression or boundary change ran. D080 explicitly grants an outside-sandbox
retry to T084; this note does not infer that grant for T083.

Request one bounded identical-command sanitizer retry outside the default
process sandbox, with the platform's scoped escalation mechanism: same
attempt-2/sanitized executable, first256 records of attempt-2/corpus.txt,
exact attempt-2/logs/sanitized-000.command.json environment/flags and60s timeout,
new task-owned output/log files only. If successful, finish the unchanged
remaining bounded corpus under those same controls. If it stalls again, stop
and retain the outcome; no repeated retries or gate waiver.

## Evidence and impact

Recorded command/executable/build/runtime/input identities:
tests/outbreak/envelope/T083/attempt-2/plan.json and logs/build-1.*;
logs/sanitized-000.command.json. Actual driver exited1 with subprocess.TimeoutExpired
for the exact sanitized executable after60 seconds. No ordinary stdout/stderr
log was emitted by invoke after the exception; the empty sanitized.txt is not
passed coverage. Python subprocess.run kills and waits on a timed-out child;
that handler was inspected. Independent process enumeration was unavailable
(pgrep exit3: sysmond service not found), so no separate process-list cleanup
claim is made.

Source, wrapper, corpus/oracle and original Wasm results are unchanged.
attempt-1 and partial handoff remain intact. Native full-corpus comparison is
independent and continues; sanitizer startup cause is unproven. No external
API, network/service, dependency acquisition or game execution is proposed.

## Options for owner and lead

Recommend the bounded same-input escalation above, analogous to D080's T084
resolution but explicitly scoped to T083. Otherwise specify a local execution
boundary; sanitizer coverage remains incomplete, never waived.

## Work paused

No further sanitizer invocation or execution-boundary change until MAIN
resolves this note. Production codec and unaffected native/Wasm checks do not
depend on a runtime/API change.
