# T195 — Corrected G2 passed both fixed frontend checks

- Worker: MAIN delegate /root/review_head_equality.
- Ticket/revision: T1951.0 / D314; G2_FOUNDATION0.4 and reviewed D311 source correction.
- Submission: completed the two individually authorized syntax-only calls; **BOTH_FRONTENDS_PASSED**, for MAIN review. No authoritative acceptance/status/source change by this delegate.
- Writes: NEW tests/outbreak/geometry/T195/check-1/** and this NEW own handoff only. All production/headers/SDK/tools/sysroot/authority/old proof read-only. No Git/worker dispatch.

## Actual outcomes and limits

| Target | Original tool returned object | Result |
| --- | --- | --- |
| Native /usr/bin/clang++ | chunk_id f16730; wall_time_seconds0.000008542; exit_code0; original_token_count0; output empty | Terminal on first call, no session, exactly one invocation |
| Wasm fixed raw clang++ | chunk_id1ba78e; wall_time_seconds0.000010541; exit_code0; original_token_count0; output empty | Terminal on first call, no session, exactly one invocation |

Each compiler wrote separate owned stdout/stderr logs. All four complete diagnostic streams are empty: **0 combined diagnostic bytes**, below8MiB. No tool truncation, yielded process, poll, timeout, retry, changed flags or source correction occurred.

Parent dispatch-to-terminal-observation bounds were native0.151s and Wasm0.182s, below each60s limit. Immutable-input postflight completed44.6073623750126s after preflight; completion observation59.41190412500873s, below300s. These are observation bounds; tiny raw tool wall values are retained metadata and are not represented as OS process lifetime, compiler speed, platform/game performance or physical resource measurements.

**SYNTAX_ONLY / NOT_LINKED / NO_COMPILED_PROGRAM_OR_QUERY_EXECUTION / NOT_FUNCTIONALLY_TESTED / NO_EMITTED_FRAME_OR_NORMAL_CALLEE_PROOF / NOT_ACCEPTED.** Frontend acceptance establishes declaration/template/static-assert compatibility for this exact source under these fixed calls. It does not prove production geometry, independent catalogs, generated code/libc imports, emitted stack/callee fit, full ABI/wire behavior, gameplay or integration. T193's previous frontend failures remain historical immutable failures; T195 is a separately released operation against separately identified corrected source.

## Inputs, roles and preservation

Output root was absent before preflight. Current geometry.cpp was verified **74884 bytes/SHA2565163a100e558022cc26e3e9693a470677e5a3b79570d68a12c0961ae457b0cb8**. Its first31382 bytes retain accepted G1 SHA256c232100352425092561f6fc9701c77db17f643893510fde780839db21be17d21. The complete recursive project-include graph is exactly seven consumed headers: p1_store.h, p1_geometry.h, p1_types.h, p1_rules.h, map_import.h, p1_hash.h and p1_query_wide.h; all seven whole identities match accepted G1 dependency roles.

Historical old geometry remains explicitly HISTORICAL_SOURCE_AT_G1_PROOF. Its archived31382-byte identity is compared to the preserved prefix, not asserted as current changed-source identity. No old manifest or failure record was rebased. The exact current source is bound independently by T195's required digest/size.

Native tool SHA256179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818 matches its specifically accepted ordinary nlink78 launcher role. Wasm clang++→clang→clang-24 raw chain and resolved ordinary SHA2569a96f4220eefe21e72a4a9a20a88f4d6c26cad1b047cb02b5b22a96bef49c423/nlink1 match. Both fixed SDK/sysroot roots are bound before/after. No generic alias/hardlink exception was introduced.

Accepted G1 actual geometry.d reference data supplies189 native and125 Wasm SDK/resource-header roles. Native/unchanged resource references compare exactly; historical copied-Wasm-sysroot paths are explicitly mapped to the original read-only sysroot with ordinary byte/hash/mode/nlink equality and separately bound current original timestamps. This is identified reference context, **not a new compiler dependency trace or whole SDK inventory**. No version/dependency/probe call or SDK copy occurred.

All **336 unique bound paths/identities** compared unchanged in postflight: source/seven headers, current controls, reviewed World handoff/diff, fixed compiler raw/resolved aliases, SDK/sysroot roots/reference headers and historical dependency-data file. Mismatches[]. Current controls are T1951.0, D314, G2foundation0.4, T1871.2 and D311. Source/input protection remained in force throughout the check and stable postflight. Completion of this handoff now returns subsequent source disposition to MAIN; no delegate source permission exists.

## Exact command/environment isolation

commands.json records these unchanged literal argv:

Native: `/usr/bin/clang++ -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk -std=c++11 -O2 -Wall -Wextra -Werror -I /Users/jd1/code/apps/outbreak/source/outbreak -fsyntax-only /Users/jd1/code/apps/outbreak/source/outbreak/p1_geometry.cpp`.

Wasm: `/private/tmp/outbreak-web-sdk/upstream/bin/clang++ --target=wasm32-unknown-emscripten --sysroot=/Users/jd1/code/apps/outbreak/web/build/.cache/sysroot -std=c++11 -O2 -Wall -Wextra -Werror -I /Users/jd1/code/apps/outbreak/source/outbreak -fsyntax-only /Users/jd1/code/apps/outbreak/source/outbreak/p1_geometry.cpp`.

Each was directly launched through shell `exec /usr/bin/env -i`, repository cwd fixed, with ONLY PATH=/usr/bin:/bin:/usr/sbin:/sbin, separate literal check-owned TMPDIR and CLANG_MODULE_CACHE_PATH. Target paths are T195/check-1/native/{tmp,cache} and T195/check-1/wasm/{tmp,cache}. stdout/stderr were redirected directly to that target's new ordinary log files, retaining complete streams. No inherited flags/compiler selectors, HOME reassignment/user cache/profile, additional source/define/target/flag, -c/-S/object/assembly/link, project helper/controller/import or alternate executable.

Fully visible inline standard-library-only metadata operations inspected filesystem/hash/JSON data and authored owned evidence. They imported no project module and launched no subprocess/compiler. Correct preflight succeeded once (chunk697399, exit0); no T195 metadata refusal or correction cycle occurred. Initial read-only documentation lookups guessed two incorrect D311 filenames before reading the discovered exact D311 path; those missing-file reads had no compiler/output-root/source effect and were not metadata preflight retries.

The native launcher created owned native/tmp/xcrun_db: ordinary0600/nlink1,499 bytes/SHA256202037e35b49daf10bd7159bf5f1b54c0c738799a2be1891894d78fa0b2eeef9. Retained as launcher temporary metadata, never executed or presented as object/module/test evidence. No other target tmp/cache file was observed at postflight.

## Retained evidence pins

Paths below are relative to tests/outbreak/geometry/T195/check-1/:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| preflight.json |346339|881f468821356c05bb5c3835b06ef156eff94db1dc93cef5e51ba2e272d04a6f|
| commands.json |1913|619c57fd2f8d579bbbf3d9236e9d9bf11f13120e133bce182b5032c9b0c1ddc8|
| tool-observations.json |1276|26a1682de773c158a0cec60ff0191149d388356eff15917665fda80e4cc06cba|
| postflight.json |117112|38fb1329eee65aea594a020adbc65bcd7f4d84aa0c5b986222ae36642722c70d|
| result.json |3013|12e425eb0e6775eef968b72d36d12d75fecc491bfc03a18eae3172e784072cc7|
| completion-observation.json |339|a072e4a23f6e2959dc0e43df05eb8d8c36c1ee49393aeafa2e8a8569c3d97748|

All four zero-byte diagnostic logs have SHA256e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855. Original tool return objects and dispatch/terminal timestamps are retained in tool-observations. Full typed input records and current pre/post identities are retained separately, not replaced by an aggregate checksum.

## Stop boundary

Both T195 calls are consumed and this delegate stops. No repeat/source fix/downstream compiler, parser/generator/oracle/fixture/corpus/test/query/runtime/Node/FFI/service/network/Git effect follows. Full real current-source R, full Q, source/normal-callee/emitted-frame/functional evidence and camera/movement/shot/tick/browser/performance/human/full-MVP/held-worker gates remain. MAIN must separately review and release any further work.
