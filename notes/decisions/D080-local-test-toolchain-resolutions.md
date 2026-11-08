# D080 — Local test toolchain resolutions

Authority: MAIN under the owner's existing local implementation/test and worker-coordination authorization. Resolves notes/questions/T083-engine-native-launcher.md and notes/questions/T084-world-sanitizer-startup.md. No gameplay/interface/parameter changes or gate waivers.

## T083

Continue RELEASED T0835.6. Approve installed /usr/bin/clang++ launcher already used in accepted T078, with unchanged intended native and ASan/UBSan flags and clean environment. Inspect and record launcher/compiler identities before invocation. New once-only attempt directory under the existing T083 allowance; preserve attempt-1, failed command and partial handoff. Reuse unchanged corpus and independent oracle, actually run both native variants and compare the same production source to Wasm. No installation, new dependency, header/SDK/cache mutation or suppression. Any further missing runtime/flag requirement remains a question. A new final handoff must distinguish retained failures from subsequent results.

## T084

Continue RELEASED T0845.7. Approve one bounded identical-command retry of the inspected task-owned ASan/UBSan executable outside the default process sandbox using the platform's scoped escalation mechanism. Same recorded executable, input, environment and flags; task-owned new output only. Inspect command and harness first; record identities and timeout/kill/reap outcomes. No network/service/external API, installation, environment/global tool changes or sanitizer suppression. Preserve both timeouts. If startup succeeds, remaining bounded sanitizer corpus execution with these same controls is permitted. If it still stalls, stop affected execution and record evidence/question; do not waive coverage or repeatedly retry. Other native/Wasm checks may continue.

All original ticket write allowlists and source ownership remain in force. These are tool-entrypoint/execution-boundary clarifications, not a new product contract revision. MAIN has not accepted T083 or T084.
