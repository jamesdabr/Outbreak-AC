# T163 compiled private profile-helper schema

Authority: T1631.1 / BLACKWOOD_CLIENT_FOUNDATION0.1 / D217 / D219.
This is the source/helper subset of Package A only. Package C's v3 admission/
controller choices are unadopted; later successors require exact accepted v4.

OUTBREAK_BLACKWOOD_CLIENT is valid only with __EMSCRIPTEN__ and
OUTBREAK_NETWORK_CLIENT and without STANDALONE. Invalid combinations produce:

```
OUTBREAK_BLACKWOOD_CLIENT requires __EMSCRIPTEN__ and OUTBREAK_NETWORK_CLIENT without STANDALONE
```

Without the define the identity is dev_outbreak_browser/revision2, with paths
packages/maps/dev_outbreak_browser.cgz and .cfg. The valid define selects only
blackwood_greybox_v1/revision1 and corresponding packages/maps CGZ/CFG. There
is no runtime map selector, negotiation or fallback. Private header includes
no engine or system dependency and holds no mutable state.

name_matches is null-safe exact equality. loaded_matches additionally requires
selected revision and positive actual loaded byte length. startup_loaded requires
load_result==0. observed_matches validates received AND loaded names/revisions,
positive loaded bytes and actual mode==GMODE_DEATHMATCH. pre_change additionally
requires advertised length>0 and exact equality with loaded length. post_change
also requires actual load_result>=0 and !incompatiblemap. spawn_matches requires
an accepted receipt plus valid loaded identity/bytes/mode. These helpers preserve
the existing positive/exact local-versus-advertised size semantics; they do not
replace actual file parsing or attest a file hash from a length. Actual maploaded
is computed by load_world from the selected immutable CGZ (dev561/Blackwood734).

receipt_name/revision report selected name/revision only when the actual accepted
receipt flag is true, otherwise empty/0. This is receipt history, not a fabricated
startup identity. Production bnmap is set only in the validated real callback
after load_world and cleared by original teardown; current peer/lifecycle/spawn
ACK and generic SV_MAPIDENT paths remain real and unchanged.

## Fixed unit wire layout

Every request is96 bytes, explicit little endian:

| Offset | Type | Input |
| --- | --- | --- |
| 0 | char[32] | received name, NUL terminated |
| 32 | char[32] | actual loaded name, NUL terminated |
| 64 | s32 | received revision |
| 68 | s32 | loaded header revision |
| 72 | s32 | actual loaded bytes |
| 76 | s32 | advertised bytes |
| 80 | s32 | mode (deathmatch fixture constant2) |
| 84 | s32 | actual load result |
| 88 | u8 | accepted receipt0/1 |
| 89 | u8 | incompatible0/1 |
| 90 | u8 | null bits:0 received name,1 loaded name |
| 91 | 5 bytes | reserved zero |

Wrapper validates both string allocations contain NUL and controls are within
their fixed ranges before calling the actual production header helpers. All
nonnull strings describe accessible32-byte storage. Signed decoding widens before
representable narrowing. Requests, output and guards are distinct allocations.

Every response is192 bytes:

| Offset | Type | Actual observation |
| --- | --- | --- |
| 0 | char[32] | selected name |
| 32 | char[48] | selected CGZ path |
| 80 | char[48] | selected CFG path |
| 128 | u32 | selected revision |
| 132 | char[32] | receipt-bound name |
| 164 | u32 | receipt-bound revision |
| 168 | u32 | predicate bits |
| 172 | u32 | observation bits (expected3) |
| 176 | 16 bytes | reserved zero |

Strings are zero padded. Predicate bits0..6: name_matches,loaded_matches,
startup_loaded,observed_matches,pre_change,post_change,spawn_matches. Remaining
bits are zero. Observation bits0/1: entire96-byte request unchanged and both
8-byte a0..a7 output guards intact. All remaining bits are zero. Output is fully
initialized before field encoding; no native structure padding is serialized.

The same finite corpus is checked against independently explicit Python string/
integer expectations for each of four targets: native dev/Blackwood macro-emulation
fixtures and import-free Wasm dev/Blackwood. These are helpers, not native engine
or browser runtime. Cases include both identities/foreign/empty/prefix/case/null,
signed revision/size extrema,734-versus561 mismatches, modes, load statuses,
incompatible flags, pre-receipt/spawn and combined gate states. Positive equal
lengths are deliberately accepted according to the preserved comparative rule.

Wasm exports are exactly memory and request_address,response_address,
request_capacity,response_capacity,run. Capacities96/192 are pinned before link.
Each profile/target<=1024 cases,response<=256 bytes, all four raw outputs<=1MiB.
Each of seven invalid define combinations has separate named native and Wasm
syntax commands with actual header double inclusion and helper body excluded.
Only exit1 plus exactly one matching profile diagnostic/no warnings/empty stdout
counts as expected refusal. Missing or unrelated diagnostics refuse the attempt.

## Source and supervisor evidence

Exact original main/client/clients2c bytes were snapshotted under attempt-1/baseline
before source edits. baseline.json is historical pre-edit metadata. The driver
permits exactly that preparation membership and exclusively creates STARTED;
an occupied or extra preparation member cannot trigger another run. Source.patch
and source-audit.json bind all changed call sites and preserved parser/load/ACK
order. Compiling the private helper does not execute the parser or whole client.

D212's accepted supervisor and44 guarded actual-method regressions are copied as
inspected source DATA, never imported or executed from the old root. Only a fixed
expected_profile_guard option is added for named compile-refusal probes. Work ends
5s before min(start+60s,whole300s deadline); independent original-handle cleanup
uses remaining time, never extra grace. The295s guard cooperates with cleanup.
Primary/secondary/unresolved/partial-output and independent retention facts survive
refusal; known reaped groups are not signaled; late0 is refusal. Fake boundaries
deny real launch/fork/exec/signals/wait/network and restore all patches. Fake
supervisor outcomes are separate from actual compile/helper observations.

No hard-real-time arbitrary kernel/Popen/descriptor/filesystem stall, process-tree
RSS/lifetime or performance attestation is implied. All actual operations/logs
share8MiB child-output cap,60s operation/300s whole, own copied sysroot/cache/tmp.
REFUSE precedes work; reports flush before bounded canonical result+directory sync,
then marker removal is final required effect. Nonzero outer status/unknown or
contradictory terminal state refuses. Runtime inventory is explicitly historical;
review/freeze/acceptance remain MAIN steps. No full-client build or runtime here.
