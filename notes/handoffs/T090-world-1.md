# T090 local LLVM22 provisioning/startup handoff

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket/revision: T0905.13 / D085; GOV/BROWSER/P0 0.5 isolated tooling prerequisite. Ticket/decision re-read before submission. No self acceptance or phase/status changes.
- Base:13f0d8eea4822dee5c976661218d022be74342e3 plus preserved shared overlay. No commit/reset/revert/dispatch/global activation.
- Changed: NEW web/toolchains/T090/** and this own handoff only. Official archive, complete inventory/extracted tree, inspected local helpers, exact T087 marker copy, task temp/cache, driver/probe logs, provenance, verification/freeze. All prior source/tests/SDK/current artifact paths read-only; independent md3.h lease unconsumed/excluded.

## Acceptance evidence

PASS — Free-space preflight about62GiB; sufficient for archive+16GiB extraction
bound+margin. One public bounded curl attempt,31.0723s, exact release22.1.8
macOS ARM64 only; allowed HTTPS redirect github.com ->
release-assets.githubusercontent.com. No accounts/credentials/API/package
manager/other version/installer. Archive1479903744bytes; SHA256
f260f4f7c0d430828a81ae8a3826a1d63fc0963ec2459489308cc23b1f7eab4f.
Trust: official HTTPS+MAIN official API published digest; independent GPG
authentication NOT RUN/claimed. Raw redirect/download commands/headers/results
retained. Three-attempt/20minute maximum was not exhausted or exceeded.

PASS — Full pre-extraction canonical path/mode/size/hash/link inventory:
10408members,9596ordinary files,783directories,29relative symlinks,0hardlinks;
7857491466expanded bytes (~7.32GiB), below200000members/16GiB. Every link chain
resolves within root to a recorded ordinary member; no escaping/absolute/
traversing path, cycle, undeclared link hop or special device accepted. No tar
installer/hook/extractall ran. Ordinary members written and hash-verified before
preserving exact relative symlinks; file/directory modes preserved. Root directory
is implicit, confined and recorded.

Preserved failed inspection — First inspector required an explicit top-directory
tar entry; this official archive omits it. It stopped before extraction.
Original helper+failure receipt retained. Correction permits confined implicit
directory ancestors while retaining all non-directory-ancestor/link-target
checks. Second full inspection/extraction passed; no upstream bytes or contract
changed. No post-freeze correction made.

PASS — Actual compiler version22.1.8, revision
ca7933e47d3a3451d81e72ac174dcb5aa28b59d1, arm64-apple-darwin25.5.0.
clang++ -> clang -> clang-22 entirely inside extracted root. Compiler/runtime/
source/archive/helper/environment identities and exact dry-run/build/runtime
argv recorded before invocation. Matching LLVM22 sanitizer files only, no
Apple17/SDK24 sanitizer replacement/mixing.

PASS — Default driver inspection showed /usr/include search with no stdio.h and
no default SDK. Used only the ticket-permitted explicit existing CLT SDK:
-isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk, resolved to
MacOSX15.5.sdk. Recorded stdio.h hash and resource/include/link paths before
building. No explicit system C++ header override needed for this marker. It
does not establish iostream/string/parser-wrapper header compatibility.
No warning/error/undefined-symbol suppression, custom ignorelist or disabled
sanitizer check added. Build stderr empty for both variants.

PASS — Actual tiny startup results; exact same T087 marker bytes, one invocation
per variant, empty stdin, no project imports/file writes/sockets/faults:

| Variant | Result | Main entry / exit | Actual elapsed |
| --- | --- | --- | --- |
| address | PASS | exact stdout+stderr markers /0, reaped |0.401328s|
| address,undefined | PASS | exact stdout+stderr markers /0, reaped |0.252235s|

Per-run timeout10s; aggregate startup0.653563s<30s; no timeout/kill/retry needed.
Existing ASAN_OPTIONS=detect_leaks=0:halt_on_error=1 and
UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 retained. Clean PATH, owned
TMPDIR/CLANG_MODULE_CACHE_PATH only. Scoped platform escalation used as released;
no OS policy bypass, signing mutation, global install/cache activation or SDK edit.
Read-only otool-L/codesign-display and compiler driver outputs retained. Driver
links/rpaths point to the inventoried LLVM22 sanitizer directory; system linker/
SDK platform libraries remain existing CLT/OS inputs.

PASS — Independent post-startup verification of full extracted membership,
every ordinary hash/size/mode, directory modes and exact relative links.
24755 protected prior SDK/CLT-runtime/historical-evidence records unchanged,
existing SDK header unchanged. Old T083/T084/T087 timeouts/freezes and Emscripten
SDK preserved. No broad source snapshot that could conflate Player md3.h edits
with this tooling task; md3.h never consumed or written.

PASS — Full provenance/licenses recorded: discovered upstream
include/llvm/Support/LICENSE.TXT plus representative ArrayRef.h identify
Apache-2.0 WITH LLVM-exception and reference upstream license text. No root
license member exists; absence honestly recorded, no invented/replaced license
or extra-file acquisition/relicense. Entire official archive/header/license
notices retained; no game publication/redistribution performed by this ticket.

NOT RUN — Actual parser ASan/UBSan corpus, deliberate sanitizer fault validation,
game/client/server/browser/native integration or complete P0/MVP gates. Both
startup probes establish only that this local matched toolchain runs the marker.
No claim that an upstream fix/version universally resolves every environment.

## Implementation status / recommended next release

Provisioning and two released marker probes complete, frozen for MAIN review.
No parser/runtime feature/source integration or SDK substitution. Exact proposed
T083/T084 compiler recipes and future bounded corpus controls are in
[README](../../web/toolchains/T090/README.md); they were NOT executed. Use a NEW
MAIN-released adapter/attempt with this compiler plus recorded SDK, original
frozen sources/wrappers/corpora/oracles/canaries, existing no-recover/runtime
options and fresh owned output/cache. Inspect T083's actual C++ header discovery
before compiling; tiny stdio marker does not cover it. Do not call old once-only
drivers or overwrite frozen attempts. Main must separately release actual
ASan/UBSan source/corpus validation before accepting T083/T084 coverage.

## Frozen identity and evidence

Toolchain root:
web/toolchains/T090/extracted/LLVM-22.1.8-macOS-ARM64.
Review download-result.json, inventory.json, extraction-result.json,
driver-inspection, startup-1/plan.json+result.json, delivery-verification.json,
PROVENANCE.json and README.md. Full command/stdout/stderr/debug evidence retained.
One-shot download/inspection/probe allowances are exhausted; do not rerun them.

terminal-freeze.json pins10519 file/directory/link records (including complete
archive/extracted toolchain), excluding itself/this handoff and named ephemeral
task temp/cache directories. SHA256:
eab9452d7c2efbdbb2b892bb5dd70c2d3f6b32d8222b792ba13c86eeea2bdffb.

- Inventory:58680f93bad4b4e5fe3436e9b37d23130d783e52da5defe935bc8adba83ae702
- Provenance:be82184af5a40649d69bd6e4c05b48d536446f6c1a64048a2097cc452333a75e
- Startup result:bdcb9c6479c479c5f0e0f85cfebd4658a099f4233b7bcfa186d09abe64364d18
- Full delivery verification:5cd6ec1249aac2be984d75fe9e7ed78e1f7727e9c4b05c57ad652638e72d10d3
- Compiler:9a690e9e11d4774d63e95ed2ab90abd82889f949b0bb9db8208f7e18f278ea50
- ASan runtime:79dedefc49970df953758e8ca7572b8b5f590600f65446e206e2515a32741b3a
- UBSan runtime:15098ff5bc50ddaf4c36f597ec099e1bc36bb90a3c26ca1ff56a969ca936cd0a
- Address probe:85d0d4f2b0f043aeedf91461cd211116ae54e13ddb42670b66095ed14fe7c2d3
- Combined probe:4e4b71d484814a2a60c954cdba5522ea1b14bad7f7ab743a93ac83233da69f57

No unresolved T090 startup/runtime requirement. Subsequent parser execution and
any changes require separate MAIN release; no self acceptance or gate waiver.
