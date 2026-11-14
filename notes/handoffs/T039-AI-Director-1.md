# T039 isolated signed dependencies and real native rebuild

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket/revision: T039 1.2 RELEASED; status unchanged by worker
- Governing scope: AGENTS; BROWSER_FOUNDATION/GOVERNANCE/P0 0.5 plus approved D014 addendum 1.2; accepted T033 source/build identity and immutable T036 runtime failure evidence
- Changed files: NEW web/server/build_signed.py, verify_signed.py, deps-signed/**, out-signed/**, T039-build-report.json, T039-verification.json and this handoff only. No existing source/framework/binary/T033/T036/other-worker file was edited.
- Commit/push/reset/dispatch: none. Server launches: none in T039.

## Actual outcome

Contained framework copies were locally ad-hoc signed using the exact approved order and commands. Copied hidapi and SDL2 bundle/binary validation passes. Fresh real arm64 release/debug servers compile and link against copied headers/dependencies/rpaths only, and both new executables' code signatures verify. Original framework bytes and all checked historical T033/T036 artifacts remain unchanged.

This fixes validation of the **copies' code signatures**. It does not establish the cause of T036's SIGKILL or fix the OS-reported libpthread mutex corruption. Neither new server was launched; startup, shutdown, client traffic and causal comparison remain NOT RUN. MAIN must review/pin new artifacts before any separately released startup.

## Acceptance evidence

| Criterion | Result | Evidence / limits |
| --- | --- | --- |
| 1 contained copy, original preservation and exact inventory | PASS | Original/copied inventories enumerate 78 regular files and seven relative symlinks, reject absolute/escaping/broken links and special files, and compare exact content/modes before signing. Source/license/Info.plist/header inventory retained; no stock map/media copied. Original inventory equals final original inventory. |
| 2 exact local ad-hoc signing and actual verification | PASS | codesign --force --sign - --timestamp=none first on copied nested hidapi.framework, then copied SDL2.framework; both exit 0. Four bundle/binary checks exit 0; independent verifier repeats them and checks both new executables. Signature display explicitly reports Signature=adhoc. No --deep repair, identities, credentials, entitlements, timestamps, keychain/security/global trust changes or installs. |
| 3 fresh real release/debug rebuild with exact copied inputs | PASS (build/inspection) | 32 fresh object compilations and both links exit 0. Actual eight STANDALONE SERVER_OBJS plus eight ENet C units, no fake server/socket code or reused prebuilt ENet. Linker -t trace identifies copied SDL2; only copied framework rpaths appear in binary load commands. All source/header/object/library identities pinned and verified stable. Runtime NOT RUN. |
| 4 original/framework/T033/T036 preservation | PASS | Original framework inventory unchanged; hashes of 215 prior artifacts before/after equal, including old binaries/reports/attempt-1 and original failed T036 run tree/JSON/supplement. Independent verify_signed.py repeats these checks. |
| 5 fresh honest immutable handoff | PASS documentation | New report/handoff, no prior handoff overwritten. Signing/build evidence separated from unexecuted runtime and unproven shutdown causality. No T014/P0/MVP acceptance asserted. |

## Exact new artifact pins for MAIN review

| Artifact | SHA-256 |
| --- | --- |
| web/server/out-signed/release/ac_server | 14233cc7302d9c1f5e45aa5948a30d224d8f56a08ed3ffc6b0f314c6dd2964a9 |
| web/server/out-signed/debug/ac_server | 8385ae7aff23c07ac2319267db7b1582a6ae38b2b48edec437322ed5a9b5039c |
| deps-signed/SDL2.framework/Versions/A/SDL2 | 5faae862816a57f36e11164dfbf5500021a2fbe65a0b23297c9697738c1c9767 |
| deps-signed/SDL2.framework/Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi | 62e00aa847d78ed4d1f6188ade82c0b271b73c2278c6bac9b08056eb036e8de0 |

Both new servers are actual Mach-O arm64 executables. New dependency rpaths, exactly:

```text
/Users/jd1/code/apps/outbreak/web/server/deps-signed
/Users/jd1/code/apps/outbreak/web/server/deps-signed/SDL2.framework/Versions/A/Frameworks
```

The shared-library install names remain @rpath/SDL2.framework/Versions/A/SDL2 and @rpath/hidapi.framework/Versions/A/hidapi. No rpath points to source/xcode/Frameworks; linker -t output proves the actual SDL input was the copied framework, not merely a new search path over an original linked dependency. System libc/libSystem, libc++, zlib and pthread remain installed macOS inputs. No DYLD environment override is required or used by the build.

Exact original (unchanged) code-binary hashes remain SDL2 `1b11de3d606e85fed9cad1f54bc2a833e99e6fc1e67fb2e748cdb666dbd0f681`, nested hidapi `91530ffddb401bbc72d40c97313c0da25c67db209753b6aec5c8556b59930e00`. Old release/debug server hashes remain T033's pins. Old T036 JSON remains `d5fe52afdcf9a163803747f443e5f76b2278851bdfec4141c8035a25b3698c4a`.

## Copy and signing evidence

Original tree was enumerated before copy. Every symlink was relative, resolved within the original root and was preserved as a contained framework-layout link in the copy. No special or escaping member was accepted. copytree uses symlinks=True and compares all 78 files/modes/paths and seven link targets before signing. The complete before/after inventories and license subset are in T039-verification.json; Info.plist/headers/licenses are byte-identical to the original.

Actual signing commands, run from the repository with task-local TMPDIR:

```sh
/usr/bin/codesign --force --sign - --timestamp=none /Users/jd1/code/apps/outbreak/web/server/deps-signed/SDL2.framework/Versions/A/Frameworks/hidapi.framework
/usr/bin/codesign --force --sign - --timestamp=none /Users/jd1/code/apps/outbreak/web/server/deps-signed/SDL2.framework
```

Only three inventory entries changed after signing: copied SDL2 binary, copied nested hidapi binary, and copied outer Versions/A/_CodeSignature/CodeResources. Header/license/Info content and all seven contained symlink targets remain unchanged. No external acquisition or original mutation occurred.

Verification commands use `/usr/bin/codesign --verify --verbose=4` on each copied framework bundle and each copied arm64 code binary, then the two new server executables. All six final checks exit 0; `--display --verbose=4` confirms copied code signatures are ad-hoc. Local development signatures are not production signing/notarization or OS trust configuration.

## Actual build/reproduction

Working directory /Users/jd1/code/apps/outbreak. Apple clang 17.0.0 (clang-1700.0.13.5), arm64-apple-darwin25.5.0; installed macOS SDK 15.5. Native compiler/options match T033: release -O3/-fomit-frame-pointer, debug -O0/-g/_DEBUG, arm64, explicit SDK, fsigned-char, C++ gnu++11 and real STANDALONE; ENet gnu99 from repository C sources. The architecture-correct accepted tools.h hash remains e53d32d55e5b81ac5e5be3e8a2411a8363dae858631f06cfd3ed11b16eef6fcf.

Actual commands:

```sh
python3 web/server/build_signed.py
python3 web/server/verify_signed.py
```

Both exit 0. Drivers were read before execution. build_signed.py refuses existing new output roots/reports rather than overwriting prior attempts. Reproduction requires fresh authorized deps-signed/out-signed/report roots; do not delete accepted artifacts simply to rerun it. Verification is read-only except its own T039 verification report. Python bytecode writes are disabled during verifier helper import.

The build uses only copied framework headers/-F directories, fresh out-signed/<mode> objects and executables, system -lz/-lpthread, and the two copied rpaths above. Native link's -Wl,-t is an inspection trace; it does not replace/omit any real server/network code. Complete argv for 32 compilations and two links, logs, object signatures/hashes, source/header/compiler dependency hashes, framework inventory and signature output are in T039-build-report.json. Logs/dependency files are in out-signed/<mode>.

All original accepted compile inputs were checked before work. Current source hashes before/after equal, every consumed source/header dependency is checked again after compilation, system SDK header/library hashes are verified against accepted T033 records, and independent verify_signed.py rechecks current objects/binaries/copies against saved hashes. No stale or changed dependency was ignored. Source/build artifact/framework/old-run outputs are read-only in this ticket.

## Runtime and causal limits

No new release/debug executable, copied library, generated file or config was executed as a server/service. Only installed compiler/linker/codesign/file/otool tools and inspected local drivers ran. There was no listener, account, network endpoint, install, source change, security/keychain configuration or production identity operation.

T036's old run is retained as partial: real original-map read and sampled loopback binds succeeded, graceful SIGINT shutdown failed. Its matching PID's OS report states FOUNDATION/libpthread mutex corruption on a demo-worker stack. Invalid original code signatures are a separately verified defect; successful copied signatures **do not** establish causality or prove that failure resolved.

Outstanding for MAIN: independently review/accept/pin these new binary/framework inventories, then separately release any bounded startup comparison or native shutdown fix. T039 has no remaining build/signature blocker. Actual runtime/startup/graceful-shutdown/client/no-egress evidence remains NOT RUN for its new artifacts. Only MAIN changes authoritative status.
