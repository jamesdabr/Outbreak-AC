# T087 standalone sanitizer diagnostic handoff

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket / revision: T0875.10, RELEASED / D083. GOV/BROWSER/P0 0.5. Ticket and decision re-read before submission; no self acceptance or contract/status changes.
- Base/pre-existing edits: shared dirty worktree unchanged outside exact new allowance. Existing T084 partial handoffs/freezes were completed before this ticket and remain unchanged. No commits/reset/revert/dispatch/integration.
- Changed files: NEW tests/outbreak/sanitizer/T087/** and this own handoff only. Includes tiny entry.cpp, inspected one-shot diagnose.py, report, three named binaries, exact command/identity/environment records, raw stdout/stderr, owned-child samples, results and terminal freeze. Ephemeral compiler temp/cache stays inside new folder.

## Acceptance evidence

PASS — Three named variants compiled with installed /usr/bin/clang++, same tiny
C++11 main marker source, conventional recorded sanitizer/no-recover flags.
No project imports/input/sockets/file writes/deliberate faults. Compiler/runtime/
source/executable hashes and exact argv/environment recorded before invocation.
Actual compiler Appleclang17.0.0 clang-1700.0.13.5, arm64; macOS26.5.1/25F80.

Actual startup results (one run per variant):

| Variant | Main entry observed | Exit / cleanup | Result |
| --- | --- | --- | --- |
| address | no stdout/stderr marker | deadline10s, elapsed10.0032s including kill/reap; -9 | TIMEOUT |
| undefined | both exact markers | exit0/reaped,0.2989s | PASS startup only |
| address,undefined | no stdout/stderr marker | deadline10s, elapsed10.0034s including kill/reap; -9 | TIMEOUT |

PASS — Diagnostic runtime20.67285s total, below60s. Hard per-child deadline10s;
observed ~3ms timeout scheduling/cleanup overhead explicitly retained. Optional
sample invocation requested1second against only each still-running owned child,
inside its existing deadline. Samples returned0; no unrelated PID enumeration,
signaling, debugger/game attachment or unbounded tracing. Killed/reaped timeout
children; no further retry. Read-only otool-L/codesign-display/compiler-version/
OS-version diagnostics succeeded. Existing ad-hoc linker signatures displayed;
no signing mutation.

PASS — Existing ASAN_OPTIONS=detect_leaks=0:halt_on_error=1 and
UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 preserved. Clean minimal environment,
task-owned TMPDIR/CLANG_MODULE_CACHE_PATH only. Platform-scoped escalation used
as explicitly released. No suppressions, added sanitizer/environment flags,
runtime replacement, dependencies, installs or tool/global/SDK cache changes.

Observed runtime facts — address/combined otool dependencies and sample symbols
identify libclang_rt.asan_osx_dynamic.dylib; undefined identifies
libclang_rt.ubsan_osx_dynamic.dylib. Installed CLT17 runtime hashes recorded in
plan/execution records. Sample binary-image path inventories are unavailable
(explicit sample message), so no full resolved loaded-path inventory is claimed.

ASan sample chain shows malloc initialization -> AsanInitInternal ->
InitializeShadowMemory -> MemoryRangeIsAvailable -> get_dyld_hdr ->
dyld_shared_cache_iterate_text_swift -> _Block_copy/malloc -> nested
AsanInitFromRtl -> StaticSpinMutex::LockSlow/yield, before main. Both ASan-bearing
variants reproduce the pattern with no parser linked. This supports a local
reentrant ASan initialization hypothesis. Exact upstream defect/fix/version and
universal reproducibility remain unproven; sampling can perturb timing.

PASS —38251 protected prior files and all diagnostic source/runtime inputs
unchanged before/after. No production/old test/SDK/assets/game/bundle/controller/
pin or T086 input writes. No parser/game/browser/server/corpus execution or
external systems/network/service. All prior T083/T084 timeouts/evidence retained.

NOT RUN — Deliberate sanitizer fault validation, actual T083/T084 sanitizer
coverage, parser/game correctness, full P0/MVP acceptance. UBSan trivial startup
success does not satisfy their required source/corpus or ASan memory gates.

## Implementation status and next remedy proposal

Implemented factual bounded startup diagnostics and evidence; no parser fix or
runtime workaround. All three runs are complete and the one-shot STARTED guard
prevents repetition. [Full report](../../tests/outbreak/sanitizer/T087/REPORT.md)
separates observations/inference and precise next tests for MAIN approval:

1. Separate new UBSan-only frozen T083/T084 production/corpus/canary runs with
   -fsanitize=undefined and existing no-recover/UBSAN_OPTIONS, leaving ASan gate
   incomplete.
2. Read-only inventory of alternative installed matching compiler/ASan runtime
   pairs, or separately approved compatible environment if none exists. After
   MAIN selection/release, compile this same tiny marker source and prove
   address/combined startup before releasing actual frozen parser/corpus runs.

No alternate toolchain has been inspected/selected, no upstream fix/version is
asserted and these proposals authorize no further execution. MAIN review/release
is required. T083/T084 full acceptance remains pending actual sanitizer coverage.

## Frozen identity / reproduction

tests/outbreak/sanitizer/T087/terminal-freeze.json pins90 diagnostic source,
report, executable, command, log, sample and result files, excluding itself/this
handoff and ephemeral tmp/clang-cache directories. SHA256:
3853bc6a0752ed2524e844b07c3f56f856d4b603fa79de6e7d3fe20a1f0b181e.

- result.json: e5b362ec58fdbb3af2d7ffd714c480d47db688c7ca930fd02be492802f65fbe3
- REPORT.md:109133197b90f1153b76cf899e0bf5999c210f0d88d37832403dacc2814eb848
- entry.cpp:08516b0c34a17a743b23c737b6483220b94476576a19a0c69a80cf7b1c4ec459
- address binary:94bdc7c58d9197c29efdb619962157abb3157cd0ebfaa5e593e084678a480f21
- undefined binary:4666cc6f399e65ad68da13b8f1d1ee7f6645e9cd7b63ad02d72031817087de3f
- combined binary:75495419031ce1a479050ea3cb38532aef2dcc6581e37a40ebfa97ba16d65621
- installed ASan runtime:9a4166d249eab6e4f1430d211e65e22172ffdf3257ec116ffc8a845d938337ec
- installed UBSan runtime:82210656f6cc9a7ae3f1edc36eabbbed66f05b255582f3dc16b802d81f788c14

Review the frozen plan/each execution/result and raw samples; do not rerun the
one-shot diagnostic or frozen parser executables under this ticket. New evidence
requires a new explicit release. No unresolved T087 scope question; stop as
required after diagnostic submission. MAIN alone accepts diagnostic delivery.
