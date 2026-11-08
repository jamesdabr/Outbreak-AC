# T0925.19 / T0985.24 / T1041.0 native candidate tooling — PREPARATION ONLY

Governing CANDIDATE_NATIVE_FOUNDATION0.3 / CANDIDATE_BUILD_FOUNDATION0.2,
D087/D088/D090/D091/D098/D107; all old helpers, binaries, ledgers and frameworks immutable.
No actual signing/compile/tool probe/server has been run by this preparation.
Fixture commands/objects/signatures are conspicuously fake temporary data and
cannot authorize real effects or become accepted build evidence.

## Fixed public commands

```sh
python3 -B web/server/candidate/build.py --plan-only --candidate-id UNIQUE-ID
python3 -B web/server/candidate/build.py --execute --candidate-id UNIQUE-ID --pins ABS-MAIN-JSON --pins-sha256 OUT-OF-BAND-SHA
python3 -B web/server/candidate/verify.py --candidate-id UNIQUE-ID --pins ABS-MAIN-JSON --pins-sha256 OUT-OF-BAND-SHA
```

Only plan-only is preparation-authorized; it writes an exclusive NEW
web/server/candidate/preparation-ID/plan.json, never reserves an actual attempt,
signs/probes tools, discovers dependencies or claims source readiness. Actual
source observation was deferred while T091 was active; MAIN D090 now permits
read-only observation. A new manifest/complete MAIN pins/execution release remains
mandatory. No accepted source/native artifact/execution manifest is authored here.

Future execute root is web/server/candidate-attempts/ID with exact deps-signed,
release,debug,tmp,logs,verification directories. ID1–48 alnum/underscore/hyphen.
dirfd/O_NOFOLLOW/exclusive mkdir refuses aliases/existing attempts; no delete,
replacement or retry. Only copied nested hidapi then copied parent SDL2 is signed
with fixed codesign --force --sign - --timestamp=none. Physical copy preserves
confined framework links/modes; no hardlinks. Only signature binaries/resources
may change; licenses/headers/Info and other members stay exact.

Exactly8 fixed SERVER_OBJS CPP+8 ENet C excluding win32,32 fresh objects and2
links. No PCH/reuse. arm64, canonical CLT MacOSX15.5.sdk, signed-char; CPP gnu++11 /
STANDALONE, C gnu99; release O3/fomit-frame-pointer, debug O0/g/_DEBUG; original
include/SDL2/zlib/pthread semantics. No xcrun/latest selection. Installed launchers
/usr/bin/clang/clang++ must report Apple17/arm64/CLT before compilation. Actual
SDK version/files, canonical compiler/ld and tools are declared/hash-checked.
Unexpected installed headers/runtime requires a question, not flag workarounds.

## Authorization/source/protection

Exact public authorization/observation fields are the approved contract0.2.
Duplicate keys, booleans as integers, extra/missing fields, path escapes, unknown
tool/flag selectors, wrong HEAD/root/SDK/framework/manifest/decision/current bytes
or input membership fail. Tools roles exactly cc/cxx/codesign/otool/file; no
command/environment from pins. Expected digest comes separately from MAIN.

One source manifest covers all MAIN-listed browser/native/portable/doc/fixture
members. Every entry's ordinary path/hash/size/mode is stable and included in
inputs; this recipe requires its16 units,Makefiles,5 authoring files,decision and
source framework ordinary data. Additional reviewed members are allowed, not
executable selectors. It excludes itself; commit precedes manifest generation.
Actual consumed project headers must also appear in the package, not just an
unrelated historical glob. A preserved unconsumed test header is not a build input;
a genuinely included undeclared header fails dependency discovery.

Python3.11.9 interpreter/canonical imported stdlib/extensions under the approved
Python.framework are separate authoring inputs; built-ins are bound by the
interpreter. No arbitrary Python program role or package hook. The gate imports
its fixed stdlib helpers before authoring closure observation.

Preservation0.2 is exact {files,directories,links,absent_roots}; files canonical
ordinary→SHA, directories/absent roots sorted unique, links lstat raw target+mode.
Fixed protected forests source,web,bin_unix,packages,config and installed browser
SDK preserve all historical artifacts when present; package/decision docs are
also independently stable inputs. Opaque old framework or malformed fixture
symlinks are never followed/approved for consumption. Consumed source/tool/output
ancestors still reject links, except explicit confined staged-framework chains.
Full original membership/modes/raw links are also captured privately across the
checkout and SDK. Only the exact owned attempt (and newly created parent container)
is added; previous attempts/history are not exempt. No historical source-token /
sound/MD3 hash exceptions. Current literal bytes govern the new ledger.

Before each compiler boundary revalidate current source/SDK/tool inputs and
framework identity; actual clang -M discovery precedes each compile, -MD follows.
Both dependency sets/current bytes must match, be predeclared and be stable before
link/final verification. No newly discovered file is silently adopted. Copies map
only declared header origins; unsupported aliases fail. Link -t traces exact32
fresh objects, owned signed SDL and declared CLT/SDK files (archive members recorded
as metadata with pinned whole archive). Native binaries have exactly2 absolute
candidate RPATHs; source/old dependency RPATHs rejected. Artifacts root-bound, not
relocatable/notarized/bit-reproducible claims.

## Private record schemas (submitted for MAIN review)

No other adapter consumes these until separately approved.

* report.json schema1 / NATIVE_CANDIDATE_BUILD_RECORD: recipe,candidate_id,
  pins_path+digest,status,claims(false native_runtime/gameplay/multiplayer/authority/P0),
  object_reuse(false),container_preexisting,protection_before,steps,tool_identity,
  stage_before/after,sign_steps/signature_steps,framework_checks,modes,errors,elapsed_ms.
  Status RESERVED→FAILED or NATIVE_LINKED_NOT_RUN; none means accepted/native runtime.
* Each ordered step: index,kind,argv,environment,timeout_s120,exit,timed_out,
  overflow,kill_fallback,group_reaped,elapsed_ms,stdout_path/stderr_path and SHA.
  Logs exclusively logs/NNN.stdout/.stderr;<=8MiB command/64MiB attempt with explicit
  overflow failure. Whole attempt<=1800s; reserve cleanup time inside deadlines.
  Own compiler/signing/inspection child groups only, TERM/KILL fallback recorded.
* Mode record: ordered16 units,binary,link_step,link_inputs,inspection. Unit row
  contains generated source/object/.d/.pre.d/discover/compile commands,3 step indices,
  exact dependencies(actual path→{origin,sha256}) and object/dep hashes. Link inputs
  actual canonical file→{origin,sha256,archive_members}; no reuse/old framework.
* Inspection: path,sha256,kind(MH_EXECUTE2/MH_DYLIB6),5 step indices for file,
  otool dependencies/load commands,signature verification and adhoc display.
  Independent arm64/fat Mach-O/load/signature-payload bounds are checked; objects
  must be MH_OBJECT1, binaries ordinary owner-executable. Tool output also verifies
  actual signatures, architecture, allowed dylib links and exact candidate RPATHs.
* freeze.json schema1 / NATIVE_CANDIDATE_FREEZE: candidate_id,status,files inventory,
  optional_receipt="verification/receipt.json",false claims. Terminal inventory
  includes every allowed owned file/directory/link(mode/hash/size/raw target) except the
  freeze itself and that one separately named optional receipt. It includes report,
  caches/logs/deps/objects/framework, not only final binaries. Failed attempts persist.
  D098 rejects unapproved owned links before sealing; an attempt with invalid owned
  paths has no freeze. A FAILED report is retained only when its own path/ancestors
  are safe; unsafe paths are never followed or removed to manufacture a receipt.
* Independent verifier rebuilds expected commands/record ordering, validates all
  current hashes/dependencies/pins/SDK/source/protection and full terminal closure;
  reruns only bounded read-only file/otool/codesign checks (no compiler/signing/
  artifact launch). Default stdout only. Optional --receipt must be the exact NEW
  owned verification/receipt.json, exclusive create/no overwrite; existing receipt
  is checked but never rewritten. Receipt schema1 / CANDIDATE_NATIVE_VERIFICATION:
  candidate_id,status VERIFIED_BUILD_ONLY_NOT_RUN,pins/report/freeze digests,
  binaries{mode:{path,sha256}},false claims. Never an accepted-native manifest.

## Prep tests and remaining execution gates

test_preparation.py uses temporary FIXTURE_ONLY files, fake Mach-O objects/signature
text and effect-double commands; subprocess/socket/signing/compiler/network effects
are forbidden. It exercises full build-record/verifier/receipt shape, not a real
build. Inspect this code before tests. Source/SDK/framework/tool read-only observation
after D090 is not an actual compiler dependency/identity probe or execution authority.
Any unsupported discovery, sign, alias, command, header change, nonzero/timeout,
stale/corrupt/reused object/log/RPATH, extra terminal member or protection failure
must stay FAIL. Actual build/signature/native runtime and clean-checkout acceptance
require separate MAIN pins/releases/review; full P0/gameplay remains unaccepted.

## T098 targeted correction and preserved T092 evidence

The exact five submitted T092 source/docs files were archived before correction
under preparation-T098-20261108-1/T092-source/ with original-to-archive SHA mappings
in T092-source-archive.json. Old T092 freezes, results and once-only writers were
not rewritten. The old freeze binds the archived source bytes; current corrected
source requires the separately submitted T098 freeze and review.

otool -L parsing now validates either one exact inspected-file thin header or
exactly the x86_64/arm64 FAT2 architecture sections for that same inspected file.
Each section must contain dependency rows with actual compatibility/current
version syntax (optional weak marker); repeated/empty/unknown/mixed/foreign
headers, unindented rows and arbitrary diagnostics fail. Every dependency in
both slices still passes the existing dylib scope checks; raw stdout remains
complete in its bounded log. No flags, target, SDK or library selection changed.
retained-otool.json contains exact SDL2/hidapi stdout fields from the immutable
T051 release report, with its path/hash provenance. Tests substitute only the
inspected artifact prefix for their temporary FIXTURE_ONLY copies.

Owned attempts are distinct from opaque protected history. Before any owned
record/log/dependency/object/binary read, paths and all ancestors must be ordinary,
canonical and confined; new log/report/freeze/receipt paths are checked before
exclusive creation. Only exact source-framework link locations, raw texts, modes
and confined resolved chains may occur under deps-signed/SDL2.framework. Extra
aliases there, or any link in tmp/logs/records/other owned paths, are rejected
before producer sealing and independently before verifier reads, even with a
resealed fake freeze. Allowed framework chains remain usable for declared copied
headers. D091 historical link preservation remains opaque and unfollowed.

The original25 archived tests and the corrected38-case suite are pure guarded
fixtures. New cases include retained FAT2/thin formats, malformed/forged sections,
foreign dylibs in either inspection phase, resealed tmp/log/ancestor/record/dep/
object/binary/receipt/extra-framework links, valid framework chains, and producer
refusal to seal an injected link. No current tool probe/sign/compile/runtime has
been run; no fixture artifact is accepted native evidence.

## T104 exact installed SDK pthread alias

D107/native0.3 adds only the fixed SDK/usr/include/pthread.h link with raw target
pthread/pthread.h, lstat mode0755 and canonical ordinary terminal
SDK/usr/include/pthread/pthread.h. SDK remains the exact canonical CLT
MacOSX15.5.sdk. The recipe-source constant binds this identity; no new public
authorization/observation/system_sdk/report schema field or alias selector exists.

authorize validates ordinary ancestors of both names, exact raw link type/text/
mode, exact confined canonical ordinary terminal and matching current target
hash in both existing inputs and system_sdk.files before reservation/tool effects.
Only the canonical ordinary target is pinned; alias names cannot be ordinary map
entries. Each actual occurrence of that exact alias in dependency_paths repeats
the identity/ancestor/target/pin/hash validation, then normalizes to its canonical
declared target. The raw .d text/log evidence is unchanged and retained; existing
canonical pre/post dependency membership/hash checks still apply. Existing staged
framework alias handling is unchanged. Build.py and verify.py remain byte-identical
and consume this shared helper as before.

Unknown aliases even to the same bytes, source aliases, the historical MacOSX.sdk
selector, altered raw spelling/mode/terminal, nested/escaping/dangling links and
undeclared/changed targets refuse. There is no generic SDK canonicalization,
old-header equivalence waiver, flag/SDK/tool/target change or new execution grant.

Before correction, the prior stage.py/test_preparation.py/README.md and unchanged
build.py/verify.py were archived exactly under preparation-T104-20261108-1/
prior-source/ with mappings in prior-source-archive.json. Original T092/T098/f0
source/evidence/freezes and D106 clean clone remain historical and untouched.
retained-pthread-dependencies.json records exact matching raw lines and full .d
hashes from retained actual release tools/log/server dependency files. Those lines
use the old SDK selector; the positive fixture substitutes only the already-fixed
canonical SDK root to model the future recipe, without running a compiler.

Common fixture changes now use a physical fake SDK tree, a real fake-owned
pthread.h symlink (lchmod applies only inside temporary fixture storage) and its
canonical target. Only ordinary canonical fake SDK files enter pins; FakeRunner
emits the raw alias and FixtureView maps all SDK access into temporary storage.
All original38 test bodies are preserved; new alias regressions cover raw retained
format/full simulated builder+independent verifier, pre-effect refusal, mode/text/
ancestor/ordinary/declaration/target changes, same-byte unknown aliases and a guard
against any real CLT/Python/tool file read. All real process/socket/compiler/signing
guards remain. Fake commands/objects do not become actual native build evidence.
