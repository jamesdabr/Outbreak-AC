# T026 local SDK and real engine Wasm object handoff

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T026 0.5 RELEASED; submitted for MAIN review, no authoritative status change
- Phase / contract revisions: BROWSER_FOUNDATION 0.5, GOVERNANCE 0.5, D005; T022 accepted prerequisite
- Base commit and pre-existing edits: `13f0d8eea4822dee5c976661218d022be74342e3` plus D005 baseline and preserved shared worker edits. `web/build/generated/t026/before.json` records initial source hashes/status. No source/header file was edited by T026. Final source changes belong to the D005 Player/AI allowlists; listed in final-source-check.json. Existing protected combat and platform.h/tools.h content remain preserved.
- Changed authored files: `web/build/compile_probe.py`, `web/build/probe-config.json`, `web/build/README.md`; new `web/build/validate_sdk_archive.py`, `web/build/FULL_CLIENT_NEXT.md`; this handoff.
- Generated/local writes: `web/build/generated/**`, `web/build/.cache/**`, fresh `/private/tmp/outbreak-web-sdk/**`. Earlier sdk-inspection reports and question/handoff notes were preserved. No root/global/native/profile changes.
- Commit or patch reference: no branch, commit, push, reset or revert authorized/performed

## Acceptance evidence

Environment: macOS 26.5.1 arm64; existing Python 3.11; Apple clang 17.0.0 for native syntax only. Target compiler banner verified as Emscripten 7.0.0 / `777e6e5db7b4990bcaeb1b9998ed642cc84e6629`. Node 24.19.0 installed task-locally. No global activation or shell profile change.

| Criterion | Result | Actual evidence |
| --- | --- | --- |
| 1. Frozen hashes, exact two binaries, safe members/links, measured hashes, preserve unexpected existing root | PASS | All T022 acquired/inspected hashes verified before manager copy; SDK root was absent. Exact D005 binary downloads only. Own reviewed validator rejected escapes/specials/unsafe link ancestry and checked real archives before install; measured SHA-256 and members in `t026/sdk-archive.json` and `node-archive.json`. Publisher checksum remains null. Validator's internal-link/escape/hardlink/linked-parent cases all PASS in archive-validator-tests.json. |
| 2. Explicit inspected component install/activate, bounded clean env, installed identity/modules/config inspection before compiler | PASS | Install and activate exit 0; exact argv/env in setup-commands.json, logs install.log/activate.log. No full SDK meta-package/npm/bootstrap/update/sourcing. installed-identity.json confirms compiler source, all five recipes, wrapper template, exact revision/version, modules and local config. bootstrap.py and tools/install.py absence matches inspected publisher exclusion list, not an unexplained mismatch. |
| 3. Five exact ports, actual compiler, clientgame/main/server real release/debug Wasm results | PASS | Five downloaded archives independently rehashed to exact recipe SHA-512 in port-integrity.json. Final six probes each exit 0 and valid Wasm object magic/hash; exact actual argv, source hashes and diagnostics in attempt-4/result.json and associated logs/objects. No simulated TU. |
| 4. Re-run extended T016 driver with D005, main/server selection, only allowed fixes, exact failure evidence | PASS | Driver now defaults to all three TUs and supports --units selection; D005 path/hash recorded. Real compiler version parser fixed after initial sanity-log prelude exposed a first-line assumption. Original failed driver attempt is retained as result-attempt-1.json/compiler-version-attempt-1.log, exit 2. Actual completed attempts 2, 3, 4 each exit 0 for six real objects. No engine compatibility fix or non-allowlisted source edit was needed. |
| 5. Native syntax, preserved ownership/native outputs, repeat successful objects, object-only claims | PASS | Six native syntax checks exit 0, commands/logs in native-syntax.json. Both headers remain unchanged from D005. Each actual six-object probe records native_outputs_unchanged=true. Repeat-verification.json records matching hashes for unchanged clientgame/server inputs; main.cpp changed between early passes under its owner, truthfully recorded. Final source hashes stable during each compile. Metadata scope remains object_compilation_only; linked/browser/network claims false. |
| 6. Exact next full-client plan and unresolved symbol/source list | PASS | FULL_CLIENT_NEXT.md; full-client-sources.json inventories 53 C++ + 8 ENet C TUs; full-client-plan.json provides exact 61 candidate compile argv and full link argv, NOT RUN. LLVM symbol inventory leaves 396 unique undefined symbols after closure across three release objects; complete list in three-object-unresolved.json with readable and mangled per-object dumps. These are object dependencies, not measured full-link errors. |

All evidence paths in this table are under `web/build/generated/t026/` unless
otherwise named. Canonical latest driver output also remains
`web/build/generated/result.json`; a submission snapshot with all six actual
objects/logs/results is retained in `t026/attempt-4/` so later runs need not
overwrite this evidence.

Measured binary archive identities (no publisher checksum supplied by inspected metadata):

| Artifact | Bytes | SHA-256 |
| --- | --- | --- |
| pinned macOS arm64 SDK wasm-binaries-arm64.tar.xz | 293601928 | `6912ef524fc1173c2b60cd454b04a2e74160c09df73caeb6efc63c122ff88c57` |
| node-v24.19.0-darwin-arm64.tar.gz | 52234372 | `8294b7aa9b03997481c06babf1e8b270c859358f27da57a11509afe537ac381d` |

Exact install/activation used the inspected existing Python directly with
clean PATH, EMSDK_ARCH=arm64, local TMPDIR, no shell sourcing and retained
validated downloads. The two actual commands are recorded completely in
setup-commands.json and match the component paths in the accepted T022 REPORT.
Their only extraction subprocess was system tar against already validated
local archives; installer logs show each exact file reused, no alternate
fallback. Actual compiler/port subprocesses then stayed in approved SDK/cache/
generated roots. Port log retrieval matches the five authorized URLs.

Reproduce the real probe:

```sh
python3 -B web/build/preflight.py --sdk-root /private/tmp/outbreak-web-sdk --json
python3 -B web/build/compile_probe.py --sdk-root /private/tmp/outbreak-web-sdk --dependency-authorization notes/decisions/D005-integrated-browser-foundation.md
```

Expected current exit 0 and six PASS records, subject to later source changes.
Use --units clientgame for the original T016 subset. No linker is invoked.
Full native syntax commands and exit codes are in native-syntax.json; they
use repository macOS framework headers only for host parsing, never in Wasm
commands. Existing deprecated sprintf warnings remain unsuppressed.

Final six-object source identities:

| Source | SHA-256 | Release / debug |
| --- | --- | --- |
| clientgame.cpp | `3091e51cabb80a76776a8307598c1b9986ea27772811f857ec3fd6d7376c4702` | PASS / PASS |
| main.cpp | `f97226e9c69b69bed91966e7a73938ef8611c6bf4320f5e55aa8f840fc38aa7b` | PASS / PASS |
| server.cpp | `c94bc767300bd215b51a6be0f43fb8fe0b31a026b4d9642677eb1f1f027db5ba` | PASS / PASS |

Each before/after TU hash matched. These hashes matched current files at the
final snapshot check. Later Player/AI edits still require new compilation;
these results do not accept final T028/T029 revisions or other service source
not compiled by this ticket. Intermediate main/server hashes are preserved
in attempts 2/3 and must not be confused with the final snapshot.

## Implementation status

Installed and activated only the pinned release and explicit Node component.
Reviewed installed wrappers/config and verified source identity before first
compiler use. The SDK wrapper executes Python with -E, so Python bytecode may
be generated under the authorized SDK root even with the parent bytecode
environment flag; no outside profile/cache path was selected.

Driver changes: real TU selection, exact version+compiler-revision banner
validation robust to diagnostic prefixes, clean explicit child environment,
local Python/ports/Node-cache paths, per-source before/after hashes and safe
dynamic log/object paths. No gameplay stubs, error suppression or native
build settings changed. The existing browser platform guards and portable
debug builtin trap compile successfully; Wasm debug disassembly includes
unreachable instructions (saved debug-clientgame.disassembly.txt). No native
assembly branch was changed.

The compiler explicitly warns LEGACY_GL_EMULATION is a link-only setting
ignored for object compilation. No renderer support is inferred from that
flag. All source diagnostics were kept. Three completed real six-object runs
were performed; the final rerun was justified by other owners' source updates.
Independent units were not replaced with fixture success.

Implemented/simulated/incomplete distinction: SDK setup and six real object
compilations are implemented and measured. Archive negative fixtures test
only member validation. No renderer, full-client link, browser session,
dedicated server, networking or game acceptance was executed or simulated.

## Integration and questions

No new T026 scope question is needed: D005 covered the actual operations and
no novel hook, extra port, identity/path mismatch or policy rejection occurred.
Normal SDK download/compiler network escalation was approved. No messages to
other workers/chats or work dispatch occurred.

Next integration requires MAIN's separate link release after stable source
and original-pack handoffs. Wait for the explicit PNG decoder/libpng decision;
the current five-port profile does not enable PNG/JPEG formats. Compile the
remaining 50 C++ units and 8 ENet C units, then perform the actual full link,
resolve errors with source owners and run real-browser QA. FULL_CLIENT_NEXT.md
contains the exact inventory, proposed commands and dependency categories.
There is no full-link error log yet because no full link was authorized/run.

Only MAIN may accept T026/T016 or update T017/T025 verification/status.
Before submission, reread ticket/contract revision markers: T026 remains 0.5
RELEASED; BROWSER_FOUNDATION/GOVERNANCE remain 0.5. No contracts, tickets,
decisions, earlier handoffs/questions or other owners' source were amended.
