# T193 — Two fixed frontend calls rejected the G2 layout assertions

- Worker: MAIN delegate /root/review_head_equality.
- Ticket/revision: T1931.1 / D309/D310, G2_FOUNDATION0.3.
- Submission: completed bounded syntax-check scope, **BOTH_FRONTENDS_REJECTED**, for MAIN review. No authoritative status or production source change.
- Writes: NEW tests/outbreak/geometry/T193/check-1/**, own NEW preflight-failure question/receipt, and this own NEW handoff only. No other source/header/tool/SDK/sysroot/cache/control/old-evidence edit or Git operation.

## Actual results

Exactly one fixed native invocation and one fixed Wasm invocation ran. Both original tool calls returned terminal exit1 without ongoing sessions, polling, retry or changed flags. Complete compiler diagnostics are retained in each target's log directory; neither diagnostic stream was truncated or normalized to a pass.

| Target | Original tool return | Outcome | Complete stderr |
| --- | --- | --- | --- |
| Native fixed /usr/bin/clang++ | chunk90b69d; wall_time_seconds0.0000105; exit_code1; original_token_count0; output empty | Nine errors, geometry.cpp767–771 |5109 bytes, SHA25662d950ebef2058887baee0a58e09579e38147b57fb778d8b752923ec37833a08 |
| Wasm fixed raw clang++ | chunk58924b; wall_time_seconds0.000007958; exit_code1; original_token_count0; output empty | Nine errors, geometry.cpp767–771 |5109 bytes, SHA2561a01c6a0e047363118530ae8ba683b11dba9adac571c5c97bd898d8886c96c80 |

Both stdout files are empty. Combined diagnostics10218 bytes, below8MiB. Shell stdout/stderr redirections saved complete compiler streams directly into owned log files; the original tool's empty output is consequently not a claim that the compilers emitted no errors.

Both frontends diagnose `offsetof` on non-standard-layout `QueryWork<8>` under the unchanged `-Werror,-Winvalid offsetof` policy (actual diagnostic flag spelling `-Werror,-Winvalid-offsetof`). The nine member assertions name candidate, walker, conversion, tag, pose_indices, counters, fault, feasibility and control. The emitted diagnostics do not establish that the asserted numeric offsets are false; they reject these `offsetof` uses on that type. No warning suppression, replacement assertion, source fix or additional check was attempted. Further source disposition is MAIN's responsibility.

Parent tool dispatch-to-terminal-observation bounds are native0.172s/Wasm0.176s, each below60s. Required immutable-input postflight completed42.19257137493696s after corrected preflight; final completion observation59.20949954201933s, below300s. These are observation bounds, not exact OS process lifetimes or compiler/hardware performance benchmarks. Raw tool wall metadata is preserved separately without promoting it to such a measurement.

**SYNTAX_ONLY / NOT_LINKED / NO_COMPILED_PROGRAM_OR_QUERY_EXECUTION / NOT_FUNCTIONALLY_TESTED / NO_EMITTED_FRAME_OR_NORMAL_CALLEE_PROOF / NOT_ACCEPTED.** No passing geometry or G2 source-package acceptance is asserted from rejected frontend checks.

## Exact commands and isolation

commands.json records unchanged literal ticket argv. Native: `/usr/bin/clang++ -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk -std=c++11 -O2 -Wall -Wextra -Werror -I /Users/jd1/code/apps/outbreak/source/outbreak -fsyntax-only /Users/jd1/code/apps/outbreak/source/outbreak/p1_geometry.cpp`. Wasm: `/private/tmp/outbreak-web-sdk/upstream/bin/clang++ --target=wasm32-unknown-emscripten --sysroot=/Users/jd1/code/apps/outbreak/web/build/.cache/sysroot -std=c++11 -O2 -Wall -Wextra -Werror -I /Users/jd1/code/apps/outbreak/source/outbreak -fsyntax-only /Users/jd1/code/apps/outbreak/source/outbreak/p1_geometry.cpp`.

Each was launched directly through shell `exec /usr/bin/env -i`, with ONLY PATH=/usr/bin:/bin:/usr/sbin:/sbin and its separate literal check-owned TMPDIR and CLANG_MODULE_CACHE_PATH (native/tmp, native/cache; wasm/tmp, wasm/cache). Repository cwd was fixed. No inherited compiler flags, HOME reassignment, user profile/cache, SDK copy, extra source/define/target/flag/version/dependency command, -c/-S, object/assembly/link/program/Node/query call or project controller/helper invocation. Inline metadata code used only fully visible standard-library filesystem/hash/JSON operations; it launched no subprocess and imported no project code.

The native launcher created native/tmp/xcrun_db, ordinary0600/nlink1,499 bytes/SHA256202037e35b49daf10bd7159bf5f1b54c0c738799a2be1891894d78fa0b2eeef9. It remains retained as launcher temporary metadata, not an object/module/program or test result. No other file was observed under target tmp/cache subdirectories at postflight.

## Immutable-input preservation and historical roles

Corrected preflight verified exact source74169/SHA2560d999988280531d74ded6bfa27ae35e032233886267ddb1deb5def276cc4bf3b and first31382-byte prefixc232100352425092561f6fc9701c77db17f643893510fde780839db21be17d21. Actual recursive project includes resolve to exactly seven consumed headers: p1_store.h, p1_geometry.h, p1_types.h, p1_rules.h, map_import.h, p1_hash.h, p1_query_wide.h. Every unchanged header matched its accepted G1 dependency identity.

Installed compiler roles match required native SHA179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818 with its specifically accepted nlink78 launcher role, and Wasm resolved SHA9a96f4220eefe21e72a4a9a20a88f4d6c26cad1b047cb02b5b22a96bef49c423, raw clang++→clang→clang-24 chain preserved. No generic hardlink/alias exception was added.

The accepted G1 actual geometry.d dependency reference closure was read as DATA:189 native and125 Wasm SDK/resource-header references. Native and unchanged resource identities compare exactly to historical roles. Historical copied-sysroot paths map to the original read-only sysroot with identical ordinary byte/hash/mode/nlink roles and separately recorded actual current timestamps. This is identified reference context, **not a fresh dependency trace or inventory of entire SDK forests**. Both fixed SDK/sysroot root identities are recorded. No SDK/header changes were made.

Postflight compared all334 unique bound paths/identities across current source/headers, compiler aliases/resolved tools, SDK roots/reference headers, current five controls and historical dependency-data file: all unchanged, mismatches[]. The current T1931.1/D309/D310/G2foundation0.3/T1871.1 controls remained stable. Archived old geometry remains explicitly HISTORICAL_SOURCE_AT_G1_PROOF; it was not retargeted to changed live source. The source protected interval has now reached stable postflight and this completed handoff; MAIN owns any subsequent disposition.

## Preserved initial metadata failure

Before either compiler invocation or output-root creation, the first inline metadata command failed exit1/chunkde06e9 because the delegate incorrectly compared changed live geometry to the old G1 source entry. Its exact command and returned error are preserved in notes/handoffs/T193-delegate-prelaunch-metadata-failure-1.md, SHA256c8f820a36202befed65636fd33a46053ccb17a3f6830f79ad693552f91519c70; companion question SHA2563a26a93c34cb22ad3aeee36dba0d58a9ab85b25192a7f9a1146c5cc69deda442. Read-only follow-up confirmed root absent, intended current source/prefix and unchanged seven header hashes.

MAIN D310 then explicitly authorized one corrected metadata preflight, which passed (chunk9f0ee6, exit0) before the original two compiler calls. This does not relabel the failed preflight as passed or create a generic retry/mismatch waiver. No second compiler attempt occurred.

## Retained evidence

All paths below are relative to tests/outbreak/geometry/T193/check-1/:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| preflight.json |345630|edebf97d2638ca5376b88b01d1b8a1263798cc74469ac1ac8c5cea84a24224df|
| commands.json |1913|571cf108ecb55de6eb4d6b2c411157586d5a50a3d611db4e9080ca96f560d6dd|
| tool-observations.json |1285|5dc3c63689df74c9eda2114c05d0484b245ccdf70f8b24c6377fc94861fe2674|
| postflight.json |116425|9d10a318e6b1f70565616d28a6e638708026c7c7d164347e938151533229f981|
| result.json |3001|ce5ed68924db3311ed24fadd81e2eb7c353d955b02312e0ad3661f07a154c769|
| completion-observation.json |319|9621f7e745edef2d09b3fa5df6c43930ba71ac168f86fa282047e687129e16bf|

Four complete diagnostic files and owned xcrun_db are retained alongside these records. The complete original tool return objects and dispatch/terminal timestamps are in tool-observations; result.json records failure honestly, limits and all334-input preservation. No output content was repaired after rejection.

## Stop boundary

Both original fixed syntax calls are consumed. No retry, source correction, altered flags, actual R/Q preparation, source parser/test/oracle/data generation, codegen/link/native/Wasm query execution, FFI/service/browser/network/Git action follows. Complete G1 regression/full G2 source/functional/callee/frame proofs, camera/movement/shot/tick/browser integration, performance/human evidence and all Player/nativeT167/QA/T149/full-MVP holds remain. Stopped for MAIN review.
