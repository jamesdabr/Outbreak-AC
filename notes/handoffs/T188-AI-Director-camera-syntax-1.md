# Ticket handoff — T188 two-target syntax checks

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T1881.0/D302; TWO SYNTAX CHECKS ONLY under CAMERA_FOUNDATION0.3. Submitted for MAIN review; no authoritative acceptance change.
- Inputs: reviewed T186 camera source12659/SHA2569cdb0bf7cae943812f3ff84616adbf18caf67445165ff8998918004be664748a; actual frozen camera/geometry/rules/types/map_import/fixed headers. G1 D300 accepted; complete real G2/current regression and full camera evidence remain mandatory.
- Changes: NEW `tests/outbreak/camera/T188/check-1/**` evidence/temp/cache/log directories and this NEW handoff only. No existing source/header/tool/SDK/cache/authority/evidence edited; no Git/worker action.

## Observed result

**Native and Wasm syntax checks PASSED.** Exactly one authorized invocation per target, original calls both terminal exit0; neither yielded an ongoing session or required restart/poll. All four stdout/stderr files are empty: **0 combined diagnostic bytes** under8MiB.

| Target | Original tool handle | Exit / completion |
| --- | --- | --- |
| Native /usr/bin/clang++ | chunk47beea | exit0, terminal on first observation, no session to resume |
| Wasm fixed clang++ | chunk2d64ef | exit0, terminal on first observation, no session to resume |

Both terminal results were observed within a parent dispatch-to-observation bound of **0.101 seconds**, below each60s ceiling. Required input postflight/result metadata completed at49.413 seconds; final completion-observation metadata at104.646 seconds, under the original300s whole actual interval. These are tool/parent observation bounds, not OS/compiler performance benchmarks or process-group absence probes. Raw tool-reported wall values are retained without upgrading them to hardware measurements.

**NOT_LINKED / NO_COMPILED_PROGRAM_OR_QUERY_EXECUTION / NOT_FUNCTIONALLY_TESTED / NO_FRAME_OR_NORMAL_CALLEE_PROOF / CAMERA_NOT_ACCEPTED.** Frontend declaration/static-assert compatibility does not qualify real geometry, function behavior, complete ABI/wire layout, normal-callee lowering, native/Wasm frames, runtime or full camera acceptance.

## Exact commands and isolation

`commands.json` records the two literal ticket argv lists unchanged: native fixed-isysroot and Wasm fixed-target/read-only-sysroot, C++11/O2/Wall/Wextra/Werror, source include, -fsyntax-only and the single camera.cpp. No -c/-S/object/link/extra source/define/version/probe invocation. No geometry.cpp compilation or fake dependency. Shell exec of `/usr/bin/env -i` replaces the shell with the authorized compiler environment; it does not invoke a project controller/helper.

Only environment entries: PATH=/usr/bin:/bin:/usr/sbin:/sbin; TMPDIR and CLANG_MODULE_CACHE_PATH are literal separate native/wasm check-owned paths. No inherited flags/compiler selector, HOME reassignment, SDK copy or user-cache path. Both target tmp/cache/log directories were reserved before either launch; output root was absent. Standard-library inline operations read/hash JSON/data and author owned metadata ONLY; they never launch compilers/programs or import project code. Compiler invocations were the two direct original tool calls, with no wrapper/controller file or retry/source fix.

## Input/role preservation

Preflight verifies source plus all six project-header hashes; inspects fixed accepted G1 compiler roles as DATA; native hash179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818 matches the explicitly accepted ordinary nlink78 launcher role. Wasm resolved hash9a96f4220eefe21e72a4a9a20a88f4d6c26cad1b047cb02b5b22a96bef49c423 matches; raw chain clang++→clang→clang-24 is retained. No generic alias/hardlink exception or tool version command.

Recorded SDK roles: fixed MacOSX15.5.sdk and original read-only web/build/.cache/sysroot roots, plus30 native/3 Wasm SDK/resource header references derived from accepted G1 fixed.d stdint dependency data and camera's project include graph. This is an identified reference closure, NOT a new compiler dependency trace or whole-SDK forest inventory; fixed argv allowed no extra dep/probe option. All50 recorded current source/header/tool/alias/SDK-root/reference/control identities compare exactly before/after, including bytes/hash/mode/link/stat fields where applicable. D302 was independently hashed before launch and rechecked afterward with the same digest. World T187 geometry.cpp is deliberately NOT an input and was neither compiled nor repinned.

## Retained evidence pins

Under `tests/outbreak/camera/T188/check-1/`:

| File | SHA256 |
| --- | --- |
| preflight.json | 3e34e30b28ff3378c0d3dd3e2726c6429c13601b6215fd5af65ea04bc0bff49c |
| commands.json | f03cebcc2b07815712ed9956f421c4546592f14ea655ef1260b3c708d08ea4b6 |
| tool-observations.json | 904998970d98974f37bfd943ebf5de683ad473001045cf37f73996d70a924709 |
| postflight.json | ab870589806b272fa0f5296a94a5750adaee374ca1780f7eeb32e63f4c5e7a2e |
| result.json | e4322ffebcbe2bbc54ff985f0f39087378957de8c1e7d22674e26985714b61da |
| completion-observation.json | 0c38233209a7a5ea13e910d5c66dfae31087d74845afefe1815ce0aecab30139 |
| owned-temp-observation.json | f78bab654d0295e96d0a70dcde800da3ca4611da5de762e612b332e19fda5b43 |

`native/log/{stdout,stderr}.txt` and `wasm/log/{stdout,stderr}.txt` retain the four empty diagnostic streams. Source and all six exact header hashes, current tool raw/resolved records, SDK/control identities and full argv/environment are in preflight/postflight, not replaced by a single aggregate digest. Tool-observations retains both original complete returned statuses, including original chunks/exit/no session. No object/assembly/module/executable/test artifact was requested.

The native compiler launcher created `native/tmp/xcrun_db` inside its explicit owned TMPDIR: ordinary0600/nlink1,499 bytes,SHA256202037e35b49daf10bd7159bf5f1b54c0c738799a2be1891894d78fa0b2eeef9. It is retained as launcher temporary metadata, not executed/modified or mislabeled as an object/test. The owned-temp observation records its identity; no extra compiler call was made.

Current controls at submission: T1881.0 SHA256b8c6f0d6f7efc6ea87689256abdd0afd0850f1db7da5fd0d70b55bd4aa68c1ac; D302-camera-source-review-and-syntax-check.md b7d67df124c15567ed1297937184109c2a67c58025541365e3f022c12b31e787; CAMERA_FOUNDATION0.3 f409d280210de01d444221a3d6c293eb7cd6956271ed800f3542b2b92e54ddde. No authority/status edit.

## Stop boundary

This completes the two allowed syntax calls; no invocation remains, repeat/correction/automatic downstream job is authorized. No helper/query/geometry test, corpus/oracle/data generation, Node/browser/server/program/network/SDK-copy/FFI/process probe or privilege effect. Full real G2/current G1 regression, camera functional/source/composition/normal-frame/caller/transaction/browser/human evidence and all Player/native/QA/T149/fullphase holds remain. Stop for MAIN independent review.
