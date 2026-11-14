# T016 partial handoff — isolated toolchain preflight and engine probe

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T016 revision 0.3 RELEASED; partial submission, not accepted
- Phase / contract revisions: P0 0.3 prerequisite subset; BROWSER_FOUNDATION 0.3; GOVERNANCE 0.3; MVP/README 0.3. Gameplay documents remain draft context.
- Base commit and pre-existing edits: `13f0d8eea4822dee5c976661218d022be74342e3`, plus D003-source-baseline.json. All eleven listed source hashes matched before editing; platform.h/tools.h had no pre-existing delta. Original dirty paths are captured in `web/build/generated/before.json`. Protected combat source hashes still match at submission; main.cpp now differs under T017 ownership and was not touched by this worker.
- Changed authored files: `web/build/preflight.py`, `web/build/compile_probe.py`, `web/build/probe-config.json`, `web/build/README.md`, `source/src/platform.h`, `source/src/tools.h`; this handoff and `notes/questions/T016-engine-sdk-prerequisites.md`.
- Generated files: `web/build/generated/{before.json,result.json,validation.json,validation-0.log,validation-1.log,validation-2.log,validation-3.log,native-syntax.json,native-syntax-0.log,native-syntax-1.log,native-syntax-2.log,submission-check.json,headers.diff}`. No `.cache` or Wasm object was created. Task-local review snapshots are `/private/tmp/outbreak-t016-reviewed-scripts.txt` and `/private/tmp/outbreak-t016-submission-contracts.txt`.
- Commit or patch reference: no commit/branch/push authorized or performed; header patch in `web/build/generated/headers.diff`.

## Acceptance evidence

Environment: macOS 26.5.1 arm64; Apple clang 17.0.0 (clang-1700.0.13.5), target arm64-apple-darwin25.5.0; Python 3.11. Exact executable/version and source fingerprints are in `web/build/generated/submission-check.json`.

| Criterion | Result | Evidence / limits |
| --- | --- | --- |
| 1. Missing SDK gives precise nonzero report, no source mutation/download/install | PASS | `python3 web/build/preflight.py` exits 1; explicit missing-root JSON run also exits 1. Six tool paths, required version file and local config absence are reported. Preflight never executes SDK code and contains no acquisition path. `validation.json`, `validation-0.log`, `validation-1.log`. Source content unchanged across these validation commands; no cache or bytecode created. |
| 2. Actual clientgame.cpp compiles to Wasm, with SDK/command/identity/log evidence | NOT RUN | No SDK on PATH or at `/private/tmp/outbreak-web-sdk`. Probe exits 2 before compiler execution. `result.json` has actual source hashes, pin and planned commands but an empty actual `runs` array; no compiler version or object success. Acquisition is paused pending the question note. |
| 3. Real release and _DEBUG Wasm builds; supported browser trap, native preserved | NOT RUN | Both real commands are configured; browser ASSERT uses `__builtin_trap()`, with native branches unchanged. Native syntax-only client release/debug pass, but no Wasm debug compilation/code generation was possible. |
| 4. Repeated real probe isolates generated/cache output and preserves other files | NOT RUN | Missing-SDK driver reran twice, both exit 2; native output fingerprints unchanged and source snapshots unchanged. This portion passes (`validation.json`); real compiler/cache rerun remains unverified. Protected baseline hashes still match. T017's concurrent main.cpp edit is separately owned. |
| 5. Metadata states object_compilation_only, no runtime/network claims | PASS | `result.json.scope` is `object_compilation_only`; linked_runtime/renderer/browser_session/network claims all false; blocked status and no actual runs. |
| 6. Exact commands, dependency boundaries, output/cache and T014 prerequisites documented | PASS | `web/build/README.md`; exact pin/flags/translation unit in `probe-config.json`. Includes guarded SDK execution command with a real lead decision required, cache/temp controls and honest remaining gates. |

Exact missing-prerequisite reproduction from repository root:

```sh
python3 web/build/preflight.py --sdk-root /private/tmp/outbreak-t016-no-sdk --json
python3 web/build/preflight.py
python3 web/build/compile_probe.py --sdk-root /private/tmp/outbreak-t016-no-sdk
python3 web/build/compile_probe.py --sdk-root /private/tmp/outbreak-t016-no-sdk
```

Expected exits are respectively 1, 1, 2, 2. The explicit nonexistent root makes the first, third and fourth checks reproducible even after an SDK is later provided. No directory at that nonexistent root was created.

Additional native regression checks (all exit 0; client checks retain one existing deprecated sprintf warning):

```sh
clang++ -fsyntax-only -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers -Isource/xcode/Frameworks/SDL2_image.framework/Headers -Fsource/xcode/Frameworks -idirafter source/include source/src/clientgame.cpp
clang++ -fsyntax-only -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers -Isource/xcode/Frameworks/SDL2_image.framework/Headers -Fsource/xcode/Frameworks -idirafter source/include -D_DEBUG source/src/clientgame.cpp
clang++ -fsyntax-only -DSTANDALONE -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers source/src/protocol.cpp
git diff --check
```

Host framework/include paths above are **native syntax checks only**. None appear in the Wasm driver's target commands. No native linking or executable launch occurred. `native-syntax.json` records commands/exits/logs. Python scripts also passed AST parsing before execution.

## Implementation status

Implemented: read-only SDK inspection, exact 7.0.0 experimental pin, explicit real-client release/debug command generation, local output/cache/temp control, stale own-object removal on rerun, symlink output rejection, compiler identity capture/version check, source/config hashes, per-command diagnostics, Wasm object magic check, native-output fingerprints and explicit object-only metadata. Without a lead dependency authorization argument the driver refuses to execute even an available SDK, protecting against unapproved first-use downloads. A provided authorization file is recorded by path/hash; the operator must verify its authority and exact scope.

Header changes: browser platform selection excludes SDL_syswm and the native GL extension header suppression/include sequence, using SDK SDL_opengl declarations instead. Native header branch is unchanged. Only browser debug ASSERT selects the portable builtin trap; native GNU/non-GNU traps remain textually unchanged. No stub, gameplay change, error suppression or renderer rewrite was added.

Simulated/test-double behavior: none used to claim compilation. The nonexistent SDK path is solely a negative tooling test. No echo, fixture, standalone protocol object or copied implementation substitutes for the client probe. Native standalone protocol syntax is supplementary regression evidence only.

Incomplete: actual SDK/LLVM/Node runtime inspection, acquisition/activation, first-use ports, release/debug Wasm compilation and compiler-specific header/flag validation. The SDK release metadata identity is recorded from D003, not independently verified locally. The candidate flags and selected SDK headers may expose additional compiler diagnostics once provided; those must be reported without edits outside this allowlist.

## Integration and questions

Open: `notes/questions/T016-engine-sdk-prerequisites.md`. No installer or first-use dependency download was run. The missing SDK is an external prerequisite; this partial handoff cannot be accepted as completion of T016.

No public/shared gameplay interface was changed. No new installed dependencies or packaged assets. No game services, browser, native client/server, public endpoint, branch, commit, push, reset or revert was launched/performed. Other workers' directories remain untouched.

After a concrete lead setup decision and local SDK/entry-point inspection, reproduce with the SDK-root and dependency-authorization commands in README. Driver output will record actual compiler exits and logs. If compilation needs non-allowlisted source changes or any cache outside the approved roots, stop that action and raise a new question. T014 still requires full link, approved asset packaging, runtime/renderer integration and actual browser map evidence; T015 requires actual separate-server browser transport evidence.

Before submission, reread T016, BROWSER_FOUNDATION, GOVERNANCE and P0 revisions; all remain revision 0.3. No authoritative status is changed here. MAIN retains review/acceptance responsibility.
