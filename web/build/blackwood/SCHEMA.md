# Blackwood fixed recipe schemas — version 1

T2111.2/D364 proposed source pins and invocations are in
notes/proposals/T211-guarded-source-plan-3.md (plans1/2 are superseded history).
Focused result.source_hashes binds all16 roles; unchanged full
result.source_sha256 binds its original8 local roles. Full startup and external
pre/post/through-interval protection still bind all16. Existing metadata-00..13
admit MAX_SAFE; field-device/inode reject MAX_SAFE+1 without additional leaves.

T164/D224 releases preparation only. None of these schemas grants execution.
`recipe.py` defines the executable exact-key contracts; this document describes
those contracts. JSON rejects duplicate keys, floats, nonfinite numbers and
unknown fields. Integers exclude booleans. Canonical bytes are sorted-key,
ASCII-escaped, two-space-indented JSON plus one newline. SHA-256 values are
lowercase 64-character hex; revisions are lowercase 40-character hex. Paths
have no empty, dot, traversal, backslash or control-character components.

## Identity and configuration

Installed repository location comes from `recipe.py`, not a caller selector.
Candidate IDs match `[A-Za-z0-9_-]{1,48}`. Recipe is `blackwood_network_v1`;
profile is `BLACKWOOD_NETWORK_CLIENT`. `config.json` must exactly equal
`FIXED_CONFIG`, including types, array order and every nested value. Its exact
keys are schema_version, recipe, profile, sdk_root, sdk_version,
compiler_revision, common_cxx, common_c, ports, link, libpng_sha512, manifest,
pack_root, js_library, shell, map. Map keys: name, revision, cgz_bytes,
cgz_sha256, cfg_sha256. No arbitrary flags, roots, environment or tool selection.

The inherited SDK is `/private/tmp/outbreak-web-sdk`, Emscripten 7.0.0 at
777e6e5db7b4990bcaeb1b9998ed642cc84e6629. The sole new C++ define is
`-DOUTBREAK_BLACKWOOD_CLIENT`, alongside the existing network define. C flags,
ports and link flags remain literal. SDL image support is PNG only. The
53 ordered genuine C++ units match Makefile CLIENT_OBJS; seven ENet C units
and the existing WebSocket C backend complete 61 units. No object reuse.
There are 61 prescans, 61 compiles, one link, Node syntax check and Node
WebAssembly.validate check: exactly 125 nominal commands.

## Source and authority

The only successor source manifest is the MAIN-owned
`web/repro/blackwood-source-manifest.json`. The worker does not create it.
`SOURCE_INPUT_MANIFEST` has exactly schema_version (1), kind,
source_revision, entries. Entries are sorted unique repository-relative
objects with exactly path, bytes, sha256, mode (420 or 493 decimal). Every
entry is rehashed and must match actual mode and bytes. The manifest excludes
itself and includes all consumed repository inputs and the authority decision.
HEAD is read from Git metadata without invoking Git. Old manifests are inputs
only where explicitly bound as asset provenance, never source-control aliases.

Authorization has exactly schema_version, kind, authority, status,
execution_release, recipe, ticket, candidate_id, decision, source_revision,
source_manifest, bindings, source_acceptance, observation. Fixed values are 1,
CANDIDATE_BLACKWOOD_BUILD_AUTHORIZATION, MAIN, ACCEPTED,
EXPLICIT_BLACKWOOD_NETWORK_BUILD_EXECUTION and this recipe. Ticket is a trimmed
nonempty ASCII string of at most 64 characters. Controls are ordinary JSON
files directly under installed notes/decisions, supplied with their raw digest.
Decision is a directly contained notes/decisions/*.md consumed input. Bindings
exactly identify repository, SDK and original ports_cache. source_manifest is
exactly {path, sha256}. The JSON authorization excludes its own bytes from
observation inputs; its digest is separately pinned and repeatedly checked.

source_acceptance has exactly ticket, decision, handoff, evidence, files.
Ticket is T163; each reference is {path, sha256} and uses the actual D223,
T163 final handoff and MAIN final review pins. Files are the four sorted
accepted source rows {path, bytes, sha256, mode}, mode 420. Their exact hashes
are SOURCE_PINS; no intermediate source acceptance is recognized.

## Observation and protection

Observation has exactly inputs, preservation, units, ports, aliases,
alias_decisions, pack, tool_errors. Inputs map canonical absolute ordinary
consumed paths to raw SHA-256 values. Units are the exact ordered 61 paths.
Tool errors must be empty for execution. SDK/compiler/Node/interpreter identity
uses retained bytes, never version probes during preparation or verification.

Preservation has exactly files (absolute path to raw SHA-256), directories
(sorted absolute paths), links (absolute path to {target, mode}), specials (the
exact D352 fourteen metadata-only original roles below), absent_roots
(sorted absolute paths). Historical links are opaque and never input
permission. Protected roots are source, web, tests and the SDK. Only the
current attempt/publication subtrees are excluded. Phase union permits only
their two new parent containers. Parent timestamps are outside this schema;
no timestamp preservation claim is made. File membership, content, directory
membership and raw link text/mode remain bound. Consumed input mode is checked
by Gate; all owned inventory modes are explicit.

Aliases are the five exact D044/D046 SDK role chains. Alias rows have path,
link_text, resolved_path, resolved_sha256. Alias decision records have sha256,
root, aliases, supporting_files. Port rows have name, recipe, recipe_sha256,
archive, archive_sha256, archive_sha512. Six literal port recipes and retained
archives are checked. Named native launcher role arming permits only the
fixed /usr/bin clang, clang++ and otool launcher exception at mode 0755.
Dependencies and read operations always require single-link ordinary files,
even after role arming; strict dependency state survives rearming and late
rechecks. Alias or launcher permission never grants header consumption.

Pack report has exactly manifest, profile, files, raw_bytes, map,
source_manifests, source_mapping_sha256, entries_sha256, limitations. It binds
the accepted T148 84-member / 411990-byte payload, original 79+5 manifests,
source mapping, license and notice associations, both original and assembled
actual bytes, and original limitations. Each manifest entry has exactly path,
virtual_path, bytes, sha256, license, notice, source_manifest, source_path,
source_sha256. CGZ is revision 1 / 734 bytes; accepted map CFG and sidecar
are unchanged. CFG order, referenced textures and common MAPCFG allowlist
are checked. Twelve outer scoped notices have exact names and hashes.

## T211 / D352 source correction (UNRUN)

Current preservation is exactly files/directories/links/specials/absent_roots,
no four-key historical-success fallback. specials is sorted with exactly seven
literal HISTORICAL_FIFOS and seven HISTORICAL_UNREADABLE paths under original
`/Users/jd1/code/apps/outbreak/web/repro/tests/prerequisites/`. No glob, alternate
root or general unreadable/special exception. FIFO rows exactly
{kind:fifo,mode:420,nlink:1,device,inode}; unreadable rows exactly
{kind:unreadable_regular,bytes:12,mode:0,nlink:1,device,inode,mtime_ns,ctime_ns}.
device/inode are nonboolean integers0..MAX_SAFE/1..MAX_SAFE respectively,
MAX_SAFE=2^53-1=9007199254740991; ns are canonical
unsigned decimal strings0 or1..20digits/nonzero first digit. Missing/retyped/
replaced/late roles, fields/types/modes, cross-table duplicates and unknown
special/unreadable additions refuse. Two no-follow lstat observations capture
metadata without content open/read/hash; unreadable CONTENT IS NOT ATTESTED.
All initial/current/final/receipt/phase-union gates retain exact specials
equality. Manifest/consumed/header/tool/alias/cache/owned roles gain NO privilege;
owned inventories stay ordinary-only, with no repair/chmod/recreation.

FileSystem.whole_end inherits ORIGINAL execute entry+3600. write_new's effective
cutoff is min(explicit original command hard,whole_end), or whole_end. Owned
mkdir/create/chmod/every partial write/flush/fsync/directory sync/eligible release/
raw copy read and write/final unlink check immediately before the next step;
late returns refuse. Copy is unbuffered; no new grace/ambiguous-close retry.
Directory failure receipt is {kind:BOUNDED_DIRECTORY_SYNC,path,error,release};
copy failure is {kind:BOUNDED_PHYSICAL_COPY,source,target,bytes,phase,error,releases}.
Release rows exactly fd,path,phase,bytes,status; status is
SKIPPED_EXPIRED_UNRESOLVED, RELEASED_LATE or CLOSE_ERROR_AMBIGUOUS_UNRESOLVED.
Strong unresolved handle ownership is retained. Existing write persistence
receipt/command log/strict consuming reap/EPERM-FIRST-ESRCH remain unchanged.
Outer FAIL ledger only uses remaining original whole; final marker unlink is
LAST mutator, with late-return refusal and no following publication. Kernel
stalls are not claimed preemptible. Independent verifier gets one original3600s
entry cutoff, inherited by optional receipt and checked at final return; default
read-only and full current-slot/marker/original/owned gates remain.

Focused SOURCE tests/T211/test_deadline_history.py has32 deadline and64 history
single-case maps. Full148groups/256leaves remains unchanged. All are UNRUN and
require separate MAIN inspected caller/source plan/release before a job, under
original300s/8MiB/128MiB/256-leaf caps. Top schema1/kinds/61/125/profile/assets
remain fixed; no current source acceptance or actual build follows.

## Plans, commands and results

Plan has exactly schema_version, kind, status, recipe, candidate_id,
source_revision, source_manifest, source_acceptance, observation, commands,
environment, claims, pending. Kind is BLACKWOOD_BUILD_PLAN, status always
NOT_EXECUTED. Pending values are only EXECUTION_PINS_NOT_SUPPLIED,
MAIN_SOURCE_MANIFEST_MISSING and T163_NOT_ACCEPTED. Execution's immutable
plan has pending=[] and still says NOT_EXECUTED; it is a pre-execution record.
Commands object has compiles, link, syntax, wasm_validation. Compile plan rows
have source, object, pre_depfile, post_depfile, pre_command, command.

Environment has exactly PATH, EMSDK, EMSDK_PYTHON, EM_CONFIG, EM_CACHE,
EM_PORTS, EM_FROZEN_CACHE, NODE_COMPILE_CACHE, EMCC_TEMP_DIR, TMPDIR,
PYTHONDONTWRITEBYTECODE. PATH is /usr/bin:/bin:/usr/sbin:/sbin; Python is the
fixed canonical 3.11 interpreter. Cache, ports, node cache and temporary paths
are owned attempt paths. No inherited HOME or caller environment selectors.

COMMAND has exactly argv, environment, exit_code, log, log_sha256, log_bytes,
elapsed_ms, failure, owned_process_reaped. Success requires exact regenerated
argv/environment/log, integer exit 0, retained raw log identity, elapsed_ms
0..120000, log_bytes 0..8388608, null failure and true owned_process_reaped.
Failure is a bounded structured JSON string or NOT_COMPLETED; null only means
success. Process receipts retain primary error, independent cleanup failures,
action order, PID, reaping state, exit, partial output identity and deadlines;
retention errors remain in the refusal record before propagation.

UNIT has exactly source, object, pre_depfile, post_depfile, pre_scan, compile,
pre_dependencies, post_dependencies, object_sha256. Dependency maps include
actual system headers and map owned copied-cache paths back to original pinned
inputs. Prescan/compile closures must match, contain the real source and,
for the three accepted consumers, browser_map_profile.h. All objects must be
fresh Wasm objects and are rechecked immediately before link.

RESULT has exactly schema_version, kind, candidate_id, recipe, ticket, status,
fixture_only, pins, source_revision, source_manifest, source_acceptance,
observation, environment, object_reuse, claims, compiles, link, syntax,
wasm_validation, error, preload_validation, notices, outputs, bundle_id,
metadata_sha256. Kind is CANDIDATE_BLACKWOOD_BUILD_RESULT. Status is INCOMPLETE,
FAIL or LINKED_NOT_BROWSER_VERIFIED. Complete success requires all 61 UNITs and
125 successful COMMANDs, object_reuse=false, error=null. Pins is {path, sha256}.
Claims exactly runtime, audio, model, multiplayer, authority, P0: all false.
Fixture context is explicitly marked; a production verifier rejects fixture
filesystem/context mismatch and fixture-only records.

Outputs map the four exact runtime basenames to actual SHA-256. Notices map
the twelve fixed relative names to SHA-256. Preload validation has status,
files, raw_bytes, actual_preload_slices, canvas, runtime_decoding. Slices have
path, start, end, sha256 and are reconstructed from actual JS and data bytes:
exactly 84, unique, contiguous, gap/overlap/suffix free, all matching mapped
payload bytes. HTML must contain the expected canvas and index.js script;
Wasm magic is checked here and future real Node validation is separately
required. Preparation simulation proves neither executable JS nor Wasm.

bundle_id hashes canonical {inputs, outputs, pins_sha256, environment, commands},
where commands is all 125 ordered argv vectors. build-metadata.json is canonical
RESULT minus metadata_sha256, avoiding self recursion. Both bundle copies must
match those exact bytes. The outer bundle is exactly index.html, index.js,
index.wasm, index.data, build-metadata.json and twelve notices: 17 files.
Only notices/ is allowed in the attempt bundle; publication adds verification/.

## Owned terminal state and verifier

Attempt is web/build/blackwood/attempts/ID; publication is candidates/ID.
Both must be absent before exclusive reservation; occupied or partial output
is never retried, cleaned or reused. Attempt roles are objects/ (61 files),
deps/ (122), logs/ (125), bundle/, cache/, tmp/, node-cache/, plan.json,
result.json, freeze.json and transient failure.json. Unknown roles refuse.
The future cache copy is physical, exclusive and checked against the original.

Inventory is exactly {files, directories}: files map sorted relative paths to
{bytes, sha256, mode}; directories are sorted relative paths. It has no parent
timestamp or self-hash fields. Freeze has exactly schema_version, kind,
candidate_id, status, attempt, publication, receipt_path, elapsed_ms. Kind is
BLACKWOOD_CANDIDATE_TERMINAL_FREEZE; inventories cover complete owned state.
Attempt excludes only direct freeze.json and transient failure.json;
publication excludes only verification/receipt.json. No blanket cache exclusions.

The durable refusal marker is created immediately after attempt reservation,
before publication/work. It dominates every success-looking record. All
validation, cleanup, reporting plus flush, result/freeze writes and directory
syncs happen while it remains. Marker removal is the final required effect;
no later CLI print occurs. Failures retain marker/partial outputs; existing
records are never overwritten to manufacture success. Whole future build
budget is 3600 seconds, each command 120 seconds inclusive of reserved cleanup;
merged output is at most 8 MiB per command, not 8 MiB across the entire build.
No grace period or unbounded cleanup wait is introduced. Arbitrary kernel
stalls are outside this process-level timing attestation.

Verifier reconstructs current authority/source, immutable plan, all commands,
closure, objects, logs, preservation, data slices, notices, metadata, bundle
identity and freeze inventory without spawning processes. Default is read-only.
Optional receipt is exclusively publication/verification/receipt.json; an
existing exact byte match is a no-op, any other existing content refuses.
Receipt has schema_version, kind, candidate_id, status, fixture_only,
bundle_id, pins_sha256, result_sha256, freeze_sha256, claims, verifier_inputs.
Kind is BLACKWOOD_CANDIDATE_VERIFICATION_RECEIPT; status is FIXTURE_ONLY in
fixtures or VERIFIED_LINKED_NOT_BROWSER_VERIFIED for future real evidence.
Verifier inputs bind recipe.py and verify.py. No runtime claims follow.

## Supervisor frame and retained group identity

Each retained command log is child merged output, followed by the literal LF /
BLACKWOOD_COMMAND_SUPERVISOR_V1 / LF delimiter and canonical supervisor JSON.
The last delimiter is authoritative; the preceding bytes remain the exact child
output, independently bound by byte count and SHA-256. COMMAND log_bytes and
log_sha256 cover the entire framed file. The inherited 8 MiB per-command file
cap includes this frame; 16384 bytes are reserved before child-output growth
for bounded supervisor state. No additional output artifact or COMMAND key is
introduced. This framing is independently parsed on build and verification.

Supervisor JSON has exactly schema_version, kind, fixture_only, pid,
leader_exit_observed, original_handle_reaped, exit_code, group, primary,
cleanup, cleanup_actions, child_log_bytes, child_log_sha256, hard_deadline_ms,
work_deadline_ms. Version is integer 1; kind BLACKWOOD_COMMAND_SUPERVISOR.
Group has exactly anchor_acquired, anchor_confirmed_before_signal,
signal_attempted, signal_result, closure, closed, permission_observation. Success requires all four
boolean facts true, primary null, empty cleanup, leader exit 0, original handle
reaped with exit 0 and canonical ordered cleanup actions. A successful group
record is either ABSENT_ANCHORED/ABSENT_ANCHORED or
SENT_ANCHORED/ABSENT_AFTER_ANCHORED_CLEANUP (signal_result/closure), both with
permission_observation:null. D263 additionally permits only
TERMINAL_EPERM_UNKNOWN/ABSENT_AFTER_TERMINAL_EPERM with the exact resolved
observation below. The frame
keeps direct-handle reaping distinct from group closure. Failed records may
retain unresolved facts; they cannot pass independent log reconstruction.

Before future launch, the supervisor requires default SIGCHLD ownership and
the fixed Darwin libc waitid nonreaping primitive. It observes
the session leader without reaping, retaining that PID/group identity anchor.
Cleanup confirms the unreaped anchor before group SIGKILL, including when the
leader has exited and a descendant holds or has closed stdout. The original
Popen handle is independently consumed with strict original-PID waitpid within
the SAME absolute remaining budget (D269/D271), never Popen.wait/poll.
No Popen poll or early wait can silently release the anchor. Only read-only
signal-zero absence probes may follow reaping; a remaining or reused PGID is
ambiguous and never receives another kill signal. Failure to confirm anchor,
signal, reap or observe closure retains an accurate refusal. No unrelated PID
enumeration or discovery is used. Group absence never substitutes for handle
reaping. Actual platform behavior is future separately released evidence.

T174 / BUILDER_TERMINAL_GROUP_CLOSURE0.1 adds required nullable
permission_observation to every group. A deferred observation is exactly
{phase:"PRE_REAP_SIGNAL",errno:1,pid:originalPID,terminal_exit_code:0,
mutating_signal_attempted:true,message:boundedString,
resolution:"POST_REAP_ABSENT"|"UNRESOLVED"}. Integer fields exclude booleans;
pid equals the independently retained original PID; message is string<=240
characters retaining the observed PermissionError. Normal group pairs require
null. Missing/unknown keys, malformed types/values and unresolved observations
refuse independent reconstruction.

Only errno1 from the existing eligible PRE-REAP anchored SIGKILL, immediately
after a fresh native terminal exit0 on the original still-unreaped handle/PID
and within its original deadline, may become TERMINAL_EPERM_UNKNOWN. No cached
exit boolean, EOF, no-event/running/nonzero/signal observation or ownership loss
qualifies. EPERM is UNKNOWN, never absence or permission to repeat a signal.
Verify original handle/PID before signal/reap. Reap that handle within the
original cutoff, then the FIRST distinct nonmutating post-reap observation
must be timely ESRCH/ProcessLookupError. PRESENT/EPERM/unknown/error/late or
mismatched ownership refuses immediately, without a deferred probe loop or any
post-reap mutation. Successful deferred cleanup records
ABSENT_AFTER_TERMINAL_EPERM and resolution POST_REAP_ABSENT, retaining the earlier
observation. Its exact normal action sequence includes observe_group_absence.
Successfully signaled normal paths retain their existing bounded closure loop.
All unrelated primary/cleanup/persistence/deadline errors remain fatal.

The producer and all command-log readers share this closed schema through
inspect_command_log. No public game/wire/API field changes. Prior source/log
snapshots remain historical, never rewritten into the new shape. T174 pass10
retains124 prior groups/214 leaves plus24 groups/42 leaves, total148/256<=256.
Fake native/process/clock/storage boundaries exercise actual Effects.run and
reader; no real process/FFI/tool/build proof follows. Candidate final2 inventory
remains PENDING_MAIN_REVIEW under T174/D263, not acceptance.

T1771.1/D269/D271 replaces only the consuming boundary, with no added private
wire field. Exact original process/PID and returncode None precede each direct
waitpid(originalPID,WNOHANG); at most6000 observations including EINTR and pauses
<=0.01s clipped to the unchanged hard=min(commandStart+120,wholeStart+3600).
No wait-entry time allowance or60s replacement. ECHILD, mismatched/bool PID,
bool/noncanonical/nonterminal status or cached/lost/changed ownership refuses.
A verified canonical exit/signal status immediately assigns process.returncode
and existing exit_code/original_handle_reaped facts BEFORE post-call cutoff
validation; late valid consumption therefore retains truthful reaped facts but
fails, and no following OS effect is eligible. Nonzero/signal exits remain fatal
to builder success. No Popen.wait/poll fallback or positive-PID proxy.

All existing log fields, nullable permission observation, exact deferred pair
and first timely separate post-reap ESRCH remain unchanged. Cached returncode
alone is never verified consumption. The focused16-case job exercises actual
helper and Effects.run with fake boundaries and Popen wait/poll forbidden; the
separate full148group/256leaf regression remains unchanged in coverage. All
sources freeze before the first job; no edit between/after, retry or repair.
Both observed PASS may produce pending final3 whole-module+focused-home graphs,
never acceptance or an actual build/FFI/process/runtime claim.

The verifier repeats consumed controls, full original preservation/phase union,
complete owned terminal inventories and explicit refusal-marker absence at its
final gate. Receipt publication has both pre-write and post-write final gates;
default read-only verification ends with the same final gate. Opaque unconsumed
history and previously absent marker paths are therefore re-observed, rather
than relying only on the consumed-input Gate cache.

D235 fixes the Darwin adapter. The pinned Python omits os.waitid; the source
uses a lazy stdlib ctypes binding restricted to /usr/lib/libSystem.B.dylib,
symbol waitid. Import, plan-only and read-only verification never import
ctypes or resolve/load/call that library. tools() records the five literal
CTYPES_INPUTS Python/extension files as ordinary bytes without importing them,
the eight DARWIN_WAIT_HEADERS (wait/signal plus pid/id/uid and backing type
headers), and the exact D235 decision as a repository/source-manifest input.
The dyld library identifier is not an ordinary FileRef or alias exemption.

Only separately authorized actual command backend setup may import ctypes,
with bytecode writes disabled, and resolve the one fixed function. Platform
is Darwin/arm64/LP64/little-endian. Explicit signed/unsigned widths and
signedness, full Sigval/Siginfo field declarations, 104-byte size, alignment8
and all ten field offsets are checked. The complete structure is zeroed before
every call and EINTR retry. P_PID=1, WNOHANG|WEXITED|WNOWAIT=0x25, signed32 pid,
unsigned32 id/uid, matching PID/SIGCHLD, zero si_errno and CLD1/2/3 terminal
status are fixed. No-event is separately validated. EINTR retries the same
nonreaping observation only within its original absolute work/cleanup deadline;
ECHILD, unknown return/status/layout/ownership and late results refuse. This
does not add a child command, selector or fallback and does not reap the leader.

Preparation denies real ctypes audit events and uname/process effects before
new imports. The actual adapter factory runs only with a fictional ctypes
module and fake platform/clock/native boundary. The observer matrix covers
normal/no-event/signal exits, full layout/offset/platform/width rejection,
EINTR/ECHILD, binding/symbol/returned-field faults and deadlines. Supervisor
faults separately inject the observer. There is no actual native call or
underlying WNOWAIT support proof until a separately released real build.

## D236 final excluded receipt-slot validation

The optional publication/verification/receipt.json inventory exclusion does
not exempt its content or identity. Whenever present, the verifier reads it
through the strict consumed-input Gate, requires exact canonical receipt
bytes and the ordinary single-link mode0644 {bytes, sha256, mode} record,
and includes that observed record in subsequent consumed-identity rechecks.
A previously observed receipt disappearing refuses even in default read-only
verification. Before publication the slot may be absent; after an explicit
receipt request it must be present at the final boundary.

After the lengthy final observation, authority and complete owned-inventory
checks, the verifier checks the slot, rechecks consumed identities, and checks
the slot again to catch an absent slot appearing during those rechecks. Explicit
refusal-marker absence remains the final required observation. The default
verifier performs no writes; correct concurrent creation can be validated,
while wrong content/identity, replacement or observed deletion refuses.
Requested publication remains exclusive and has both pre- and post-publication
gates. These checks do not claim filesystem atomicity after return.

## D238 inclusive command persistence cutoff

Command log persistence receives hard=min(original command start+120,
original attempt start+3600). No log creation begins when that cutoff is
already exhausted, including after late supervisor-receipt preparation.
The actual exclusive writer checks the same absolute cutoff at entry,
before open/chmod/fdopen/every short write/flush/fsync, and after each return
before another effect. It uses raw buffering=0 with closefd=False; no buffered
close can initiate an implicit pending write. Each raw-object/descriptor release
is independently eligible only before that cutoff. A close started in time but
returning late refuses and prevents another release. No ambiguous close is
retried.

On expiry, skipped releases are SKIPPED_EXPIRED_UNRESOLVED. Strong raw/FD and
process/selector ownership remains in the private in-memory UNRESOLVED_HANDLES
registry until process exit; no expired close/flush/fsync is initiated and OS
exit cleanup is not budget proof. An accepted operation requires successful
actual handle releases before cutoff. Blocking calls are not universally
preempted: late returns are refused without later child-phase mutations.

PersistenceRefusal carries an in-memory receipt with actions, eligible/skipped
releases, actual returned write counts, known-prefix SHA256, unresolved write
return, flush/fsync/release facts, primary/release errors, elapsed snapshot
and cutoff/late state. Failed COMMAND log fields are qualified by those facts;
an unresolved retained identity has null log_sha256 and no complete-file claim.
Raw child-prefix byte/hash facts survive even when no log is created. The
successful COMMAND.elapsed_ms is sampled after retention and eligible release
returns, not before them. Failure serialization is not claimed as completed
child persistence; no expired command is converted into success.

The producer's outer FAIL ledger is a distinct phase while failure.json
still dominates. It may write only result.json exclusively, using the original
attempt start+3600 cutoff through the same persistence helper. Whole expiry
skips that ledger; a late ledger write prevents its subsequent flush/fsync/close.
No new grace or child continuation follows. ProcessRefusal can retain the outer
ledger facts in memory without adding RESULT/COMMAND schema keys or files.
The guarded persistence matrix exercises actual Effects.run, the actual raw
writer and actual outer execute/failure-ledger paths with fake file/process
primitives, including late I/O, receipt preparation, skipped release ownership,
partial writes, inclusive success timing and exhausted whole budget.
