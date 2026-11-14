# T083 native standard-library header discovery

- Worker/ticket: Engine & Multiplayer / T0835.6, D079
- Affected clause: PORTABLE_FORMAT_FOUNDATION0.1 tools; question missing runtime/flag before changes.
- Status: OPEN for MAIN; only native and native ASan/UBSan execution affected.

The inspected task-owned attempt-1 driver invoked installed
/Library/Developer/CommandLineTools/usr/bin/clang++ directly with its recorded
clean environment. Native build-0 exit1: wrapper.cpp cannot find iostream.
Production stdint-only envelope source is unchanged. No missing-header fallback,
installation, new include/sysroot flag, sanitizer suppression or SDK edit ran.
Evidence: tests/outbreak/envelope/T083/attempt-1/logs/build-0.stderr and its
command.json; frozen initial plan/corpus/input/tool identities are retained.

Recommend using installed /usr/bin/clang++ for both native builds, exactly the
launcher accepted and executed successfully in T078. Preserve all current test
flags and clean environment; record launcher identity/version before execution
in a new once-only task-owned attempt. This is a proposed tool-entrypoint
correction, not permission to add SDK/header acquisition or compiler flags.
Please approve that exact correction or specify the native tool/environment.

Native/sanitizer tests are currently NOT RUN beyond failed compilation, not
passed. Independent minimal Wasm/golden checks may continue within the existing
release and recorded tool/cache scope. No production/game/fixed API changes,
other-worker dispatch or source integration is proposed.
