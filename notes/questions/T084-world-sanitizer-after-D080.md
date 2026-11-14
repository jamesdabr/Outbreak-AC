# Sanitizer startup still stalls after approved escalation

- Author / worker: World/Match-Systems
- Ticket / revision: T084 5.7
- Contract: PORTABLE_FORMAT_FOUNDATION 0.1; D079 and D080
- Clause: actual installed ASan/UBSan coverage; D080 requires stop/question if the one identical escalated startup retry still stalls.
- Status: OPEN; MAIN resolution separate.

## Question

What installed sanitizer/runtime diagnostic or separate environment should be
approved next? The single D080 retry is exhausted. No additional execution,
runtime flags, sanitizer suppression, dependency acquisition or waiver is
authorized by this note.

## Evidence and impact

D080 startup retry used the exact original attempt1 executable, empty stdin,
same recorded environment/cwd/flags, with platform require_escalated execution.
Original executable SHA256:
5c2d900240142f83a8adf212d9affc68873ad93b58805a1d06adedf48c376f8c.
Startup again timed out10seconds with empty stdout/stderr. subprocess.run killed
and reaped the child; zero corpus cases/batches ran. Before/after38251 protected
files unchanged, frozen source/input hashes unchanged. No rebuild or substitute.

Inspected one-shot retry helper, pre-invocation plan, start marker, raw stdout/
stderr, timeout receipt and result are in tests/outbreak/map-import/T084/
sanitizer-D080-1 and retry_sanitizer.py. All original timeout evidence remains.
The reason for sanitizer initialization failure is unknown; no parser/runtime
diagnosis is claimed. Native/Wasm9639-case full-cell/oracle evidence remains PASS.

## Options for owner and lead

1. Release an exact installed-runtime diagnostic after reviewing the startup
   evidence, with scoped command/environment/output ownership.
2. Release sanitizer execution of the frozen source/corpus on another approved
   local environment/toolchain, preserving the same independent oracle/canaries.
3. Keep required sanitizer coverage blocked. Native/Wasm review can proceed,
   but it does not satisfy or waive the sanitizer/full-ticket gate.

## Work paused

All further sanitizer startup/corpus/flag/environment experiments. Source,
harness, native/Wasm corpus and new retry evidence are frozen for MAIN review;
no production correction or speculative integration is pending. Full-ticket
completion remains blocked on actual sanitizer coverage.
