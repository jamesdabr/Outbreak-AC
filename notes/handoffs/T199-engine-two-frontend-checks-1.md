# T199 two exact frontend syntax checks

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket/revision: T1991.0 /D323, MOTION_RECORD_FOUNDATION0.2.
- Changed files: NEW tests/outbreak/motion_record/T199/check-1/** and this NEW own
  handoff only. No source/header/SDK/tool/sysroot/cache/authority/old evidence
  change. No Git operation or worker dispatch. T196 source-write lease is closed.
- Submission: BOTH_FRONTENDS_PASSED for MAIN review; NOT_ACCEPTED.

## Exact outcomes

Exactly one native and one Wasm syntax-only call ran on the fixed production
p1_motion_record.cpp. Both original calls were terminal exit0, with no yielded
session, poll, retry, source correction or changed flags. The four complete
stdout/stderr logs contain0 combined diagnostic bytes, below8MiB.

| Target | Original tool result | Parent dispatch-to-terminal observation |
|---|---|---:|
|native /usr/bin/clang++|chunk d2061c; exit0; wall_time_seconds0.000014792; empty output; no session|0.118s|
|Wasm fixed clang++|chunk6311a1; exit0; wall_time_seconds0.025592792; empty output; no session|0.188s|

Each observation bound is below60s. Immutable-input postflight completed
38.73419729201123s after the original preflight start, below300s. The final
completion-observation.json separately records the full bound through this
handoff and final identity check. Times are parent/tool observation metadata,
not OS process lifetime, compiler benchmark, group absence or waitpid evidence.
No process/reap probe was authorized or performed.

**SYNTAX_ONLY / NOT_LINKED / NO_COMPILED_PROGRAM / NOT_FUNCTIONALLY_TESTED /
NO_EMITTED_FRAME_PROOF / NOT_ACCEPTED.** These exact frontends accept the fixed
declarations and production source; this does not establish codec behavior,
full native layout/ABI, golden results, alias preservation, emitted costs, normal
callee/frame closure, runtime, gameplay or full package acceptance.

## Commands and isolation

commands.json preserves each literal ticket argv, cwd, environment and log paths.
Native: `/usr/bin/clang++ -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk -std=c++11 -O2 -Wall -Wextra -Werror -I /Users/jd1/code/apps/outbreak/source/outbreak -fsyntax-only /Users/jd1/code/apps/outbreak/source/outbreak/p1_motion_record.cpp`.

Wasm: `/private/tmp/outbreak-web-sdk/upstream/bin/clang++ --target=wasm32-unknown-emscripten --sysroot=/Users/jd1/code/apps/outbreak/web/build/.cache/sysroot -std=c++11 -O2 -Wall -Wextra -Werror -I /Users/jd1/code/apps/outbreak/source/outbreak -fsyntax-only /Users/jd1/code/apps/outbreak/source/outbreak/p1_motion_record.cpp`.

Both ran from repository cwd through direct shell `exec /usr/bin/env -i`, with
login disabled and ONLY PATH=/usr/bin:/bin:/usr/sbin:/sbin plus separate literal
T199/check-1/{native,wasm}/tmp and cache values for TMPDIR and
CLANG_MODULE_CACHE_PATH. Separate target log directories retained whole streams.
Root absence was confirmed before creation; all six tmp/cache/log directories
were reserved before either call. No inherited compiler selector/flags/HOME,
user cache, extra source/define/option, version/dependency probe, wrapper TU,
object/assembly/link/program/Node or SDK copy.

Native launcher created only native/tmp/xcrun_db: ordinary0600/nlink1,499 bytes,
SHA256202037e35b49daf10bd7159bf5f1b54c0c738799a2be1891894d78fa0b2eeef9.
Retained launcher metadata, never executed or presented as an object/test.
No Wasm tmp/cache file or native cache file was observed. Complete observation
is in owned-temp-observation.json.

## Identity and scope evidence

Production remains10357/SHA2561ea174000c85907dbb63d1775feb3ee631b01eceb7bff28110b0c4bd10ad5c80.
Record header931/e9c589d975877950b8099427a80bebfb11bf360eebf8371a30b6523df970895f;
state445/4ac3aa394a62d6a459e89c8fe78c63737a4b7d76a8e96a90174cb841dbc250fc;
types2378/8f9222262be5cfbc5e16f10b040b6bef95385af0db58669cfc3d0cfcc6f8b621.
Direct source inspection gives the exact project chain production.cpp -> record
header -> state header -> types header -> system stdint.h. No other project
header is consumed; no project/parser/controller was imported to infer this.

All61 bound path identities compare unchanged in postflight, mismatches[].
They include the whole T196 eight-source package, the three consumed project
headers, current T199/D323/foundation0.2/T196/D315 controls, AGENTS, T196 handoff,
T188/T195 procedure handoffs, tool raw/resolved aliases, SDK/sysroot roots,
historical accepted G1 context data and T188's30 native/3 Wasm stdint SDK/resource
reference headers. Full records retain mode/nlink/mtime/ctime/bytes/hash or typed
link/directory facts, rather than one aggregate digest.

Native tool matches the specifically authorized ordinary nlink78 launcher,
SHA256179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818.
Wasm raw clang++ -> clang -> clang-24 and resolved ordinary binary match accepted
SHA2569a96f4220eefe21e72a4a9a20a88f4d6c26cad1b047cb02b5b22a96bef49c423.
SDK context is the fixed MacOSX15.5 and original read-only Wasm sysroot, not a
new copied SDK. Reference headers matched their accepted T188/G1 identities.
This is identified reference context, NOT a new compiler dependency trace or
whole-SDK inventory. No installed tool inspection by version/probe occurred.

## Evidence and stop boundary

Under tests/outbreak/motion_record/T199/check-1/: preflight.json, commands.json,
tool-observations.json, postflight.json, result.json, owned-temp-observation.json,
completion-observation.json and four native/wasm log files. Completion metadata
pins all retained evidence and this handoff after the final identity check.
Every empty log hash is e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.
Metadata authoring used visible inline standard-library read/hash/JSON/exclusive
owned file operations, no project import/helper execution or subprocess driver.

The two authorized calls are consumed. Stop for MAIN review. No source correction,
repeated compiler, catalog/oracle/control/generator/fixture/test/FFI/query/browser/
service/network/Git/runtime effect follows. The T196 native stdio/entry normal
runtime question remains OPEN as a future full-proof gate, independent of this
narrow syntax result. MR-CATALOG/12-child MR-ACTUAL512, complete ABI/module/frame/
caller/functional evidence and full-MVP/G2/current-G1/camera/shot/tick/browser/
human/Player/native/QA/T149 and held-worker gates remain. This handoff does not
change authoritative ticket status or grant subsequent source-write permission.
