# T088 network_v1 private preparation/result records

Preparation schema for MAIN review under CANDIDATE_BUILD_FOUNDATION0.2/D091. This
document freezes private builder/verifier records only on submission. No other
adapter may consume these records before separate approval. Public CLI and MAIN
authorization/source-manifest fields remain exactly those in the addendum.
All serialized records use sorted, indented ASCII JSON plus newline. Duplicate
keys, nonfinite numbers, unknown authorization/source/result/command/freeze
fields and wrong typed identities fail. Integers reject bool and float aliases.

## Fixed entry points and boundaries

```
build_candidate.py (--plan-only | --execute) --candidate-id ID
                   [--pins ABSOLUTE_MAIN_JSON --pins-sha256 SHA256]
verify_candidate.py --candidate-id ID --pins ABSOLUTE_MAIN_JSON
                    --pins-sha256 SHA256 [--receipt ABSOLUTE_PATH]
```

ID is1..48 ASCII letters/digits/underscore/hyphen. Installed script derives
repository root. SDK is fixed /private/tmp/outbreak-web-sdk; ports cache is fixed
repository/web/build/.cache. No root/profile/command/environment/plugin argument.
Plan refuses execution pins and writes only a NEW tests/candidate/preparation-ID/
plan.json after read-only discovery; no actual attempt/publication reservation
or subprocess. Actual observation waits for MAIN's terminal source-owner signal.
When MAIN's source manifest is not yet present, plan-only records a null binding,
PENDING_MAIN_SOURCE_MANIFEST and proposed_source_entries with actual sizes/hashes/
modes. These are observations, never accepted manifest writes. Execution still
requires the complete actual MAIN manifest and explicit selected decision.
No execution is released by T088. Real execution needs later MAIN digest/pins and
an execution ticket, no substitution of a worker-authored observation.

Actual attempt: web/build/candidate-attempts/ID; publication:
web/build/candidates/ID. Both preflight absent and are exclusively mkdir-reserved;
partial reservation/failure is retained. No deletion, reuse, replacement or
rename-overwrite of existing targets. Canonical paths/no traversal/undeclared
symlink, ordinary files and source420/493 mode gates precede effects. SDK links
are only the inherited D044/D046 decision-declared chains, with exact targets.

## Observation and source packaging

The eight exact observation fields are inputs,preservation,units,ports,aliases,
alias_decisions,pack,tool_errors. All must exactly match current observation,
including types and full membership. Tool errors must be empty for execution.
Original fixed network flags/config/backend/shell/pack/alias/port checks remain;
new code additionally fixes the accepted literal compiler/ports/link flags.

inputs maps absolute regular file paths to SHA256: explicit production/helper/
config/payload/notice/source-manifest/selected-decision inputs plus installed
authoring tool/SDK/port identities. Source manifest excludes itself; all source
entries are unique sorted ordinary canonical repository members. Every recipe's
consumed subset and authorization decision must be present; explicitly MAIN-listed
members for native/portable sources, docs and fixtures are also valid. Every
listed member is checked and added to stable inputs; none selects a command or
weakens compiler-discovered dependency validation. Every entry's bytes/hash/mode
is rechecked. Current HEAD is read from Git metadata
without subprocess; a dirty overlay is bound separately by source identities.

preservation is the private phase-aware record:

```
{files: {ABS_PATH: SHA256}, directories: [sorted ABS_PATH...],
 links: {ABS_LINK_LOCATION:{target:RAW_LINK_TEXT,mode:LSTAT_PERMISSION_MODE}},
 absent_roots: [sorted ABS_PATH...]}
```

It retains the original Recipe protected file set, adds existing historical
build/candidate/evidence trees when present, and explicitly preserves directory
membership and originally absent roots. Historical directory/file symlinks are
walked with followlinks=false and preserved opaquely using lstat/readlink, including
old framework chains and intentionally malformed/dangling fixture targets. Their
location/text/mode must remain exact; no target is followed, approved or admitted
as a source/tool/output alias. Historical diagnostics are protection, not
source/compile inputs. Only the current owned attempt/publication subtree
is phase-filtered. The two parent containers may be created to reserve those
direct children; no other original additions/removals or byte changes pass.
No generated/output root is blanket-exempted from protection/verification.

Production source discovery excludes historical web/runtime/tests and other
diagnostic/evidence trees under D088. Genuine -M/-MD dependencies remain strict;
the fixture suite contrasts an unconsumed historical header with an included
undeclared header. Fresh checkouts need no old task caches as source inputs.

## Dependency and command records

Fixed recipe generates61 fresh object commands:53 CLIENT_OBJS CPP,7 ENet C and
one WebSocket C; unix.c excluded. No arbitrary manifest command. Instrumentation
adds a pre-scan -M/-MF/-MT using identical flags/includes/ports and a compile
-MD/-MF dependency file that includes system headers. Each pre/post Make rule
is parsed, actual member identities checked, and source presence required.
Copied-cache dependencies map to their exact original frozen cache identities;
only decision-declared aliases resolve links. No raw-hash or system-header waiver.
All pre/post closure membership/hash maps must match and are independently read
again by the verifier. Objects must not exist before their actual compile.

Each pre-scan,compile,link,syntax,wasm_validation record has EXACT fields:

```
{argv:[strings...], environment:{fixed key:string...}, exit_code:int,
 log:ABS_ATTEMPT_LOG, log_sha256:SHA256, log_bytes:int,
 elapsed_ms:int, failure:null|string, owned_process_reaped:bool}
```

Success requires exit0/no failure/reaped true; logs must match recorded
bytes/hash/path and be<=8MiB. Each real command<=120s; complete reserved attempt
<=3600s. No shell; real runner owns a new process group, drains bounded merged
output, kills/waits on timeout/overflow and retains fault records. Pure tests
inject named failure/timeout/overflow effects; they are not process-runtime proof.
SDK/Node/compiler/runtime execution is NOT RUN in preparation.

## Result, metadata and bundle identity

result.json has EXACT fields:

```
schema_version:1, kind:"CANDIDATE_NETWORK_BUILD_RESULT", candidate_id:ID,
recipe:"network_v1", ticket:AUTH_TICKET, status:"LINKED_NOT_BROWSER_VERIFIED",
fixture_only:bool, pins:{path:ABS_MAIN_PINS,sha256:SHA256},
source_revision:40hex,source_manifest:{path,sha256},observation:OBSERVATION,
environment:FIXED_ENV,object_reuse:false,claims:CLAIMS,compiles:[61 UNIT...],
link:COMMAND,syntax:COMMAND,wasm_validation:COMMAND,error:null,
preload_validation:INHERITED_SLICE_REPORT,notices:{REL_NOTICE:SHA256},
outputs:{index.html:SHA256,index.js:SHA256,index.wasm:SHA256,index.data:SHA256},
bundle_id:SHA256,metadata_sha256:SHA256
```

UNIT exact fields: source,object,pre_depfile,post_depfile,pre_scan,compile,
pre_dependencies,post_dependencies,object_sha256. Paths/argv/env are regenerated
from fixed code, never trusted as selectors. All claims are exact booleans false:
runtime,audio,model,multiplayer,authority,P0. No ACCEPTED flag/manifest is emitted.

Metadata is canonical result BEFORE adding metadata_sha256, avoiding recursion;
its bytes match exactly in retained bundle and publication. Bundle ID hashes
canonical {inputs:observation.inputs,outputs,pins_sha256,environment,commands},
where commands contains all ordered pre-scan/compile argv plus link/syntax/Wasm
validation argv. All sources, objects, commands and result remain reviewable.

Both bundles require the four runtime files, metadata and12 exact notice bytes
(17 files), no extras. Inherited parser verifies actual HTML hooks, Wasm magic,
79 unique nonoverlapping contiguous data slices and every approved payload
length/hash, not a fake manifest or compile-only assertion. Real execution also
requires actual Node JS syntax and Wasm validation records. Runtime is false.

## Terminal membership and independent verifier

Attempt roles: objects(61 exact .o),deps(122 exact .d),logs(125 fixed files),bundle
(17 exact files),cache/tmp/node-cache(all final ordinary files enumerated),
result.json,freeze.json. Unknown root/role/objects/deps/log files/directories fail.
Publication adds exactly the empty verification directory to the validated17
members; no arbitrary extra file or empty directory passes.

freeze.json EXACT fields:

```
{schema_version:1,kind:"CANDIDATE_TERMINAL_FREEZE",candidate_id:ID,
 status:"LINKED_NOT_BROWSER_VERIFIED",attempt:INVENTORY,publication:INVENTORY,
 receipt_path:"verification/receipt.json",elapsed_ms:int<=3600000}
INVENTORY={files:{REL_PATH:{bytes:int,sha256:SHA256,mode:int}},
           directories:[sorted REL_PATH...]}
```

Attempt freeze excludes ONLY itself; publication excludes ONLY the separately
named verification/receipt.json. Every other owned cache/temp/log/member is
recorded and independently matched. Failed attempts retain failure.json with
FAIL/error and partial actual command records; missing freeze/result or any
failure.json refuses success. No failed destination is removed/retried.

Independent verify regenerates current source/tool/authority/flags/commands,
checks pre/post actual dependencies, objects/logs/results, original phase union,
both bundles, metadata, payload/notices and terminal exact inventory. It never
executes commands or changes result/metadata. Read-only is the default.

Optional receipt is ONLY publication/verification/receipt.json, created once
with exclusive open, never overwritten. Existing receipt must match expected
canonical bytes even for read-only verification. Receipt EXACT fields:
schema_version,kind("CANDIDATE_VERIFICATION_RECEIPT"),candidate_id,status,
fixture_only,bundle_id,pins_sha256,result_sha256,freeze_sha256,claims,
verifier_inputs(candidate_recipe.py,verify_candidate.py,profile_client.py hashes).
Real status is VERIFIED_LINKED_NOT_BROWSER_VERIFIED, never acceptance. Injected
fixture contexts always emit FIXTURE_ONLY and are rejected by production context.
MAIN alone reviews evidence and creates later accepted-artifact/runtime pins.
