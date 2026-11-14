# D457 — Match the reviewed launcher to the next native candidate

MAIN changes only the fixed native BASE in the closed/accepted T266 launcher from failed visible-native-1 to the future visible-native-2 and updates its instructions. Prior launcher bytes are preserved at notes/preflight/T266-before-native-2.py. This happens before forming the next common source manifest, with no live build/runtime. No selector, fallback, binary copy or run permission is introduced; missing candidate2 still refuses. All route/ownership/deadline/input behavior remains.

D456's first native attempt remains failed/immutable. Player T272 source/targeted correction is active; next actual build still needs source review and fresh control. The active-service visual run remains separately scoped, including effective permission to close its owned groups; do not launch it under known-denied cleanup assumptions. QA stays paused.
