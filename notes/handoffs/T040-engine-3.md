# T040 attempt 3 — precheck incident, not an accepted graphics artifact

- Worker: Engine & Multiplayer
- Assignment: T040 1.3 / D028 graphics integration, same D006/D009 profile
- Status: partial/UNACCEPTED attempt evidence; no ticket/status edits
- Engine source/header/config/tooling changes: NONE
- Current web/build/out: original D022 bundle restored exactly and frozen

## Precheck and containment

D028's five published graphics/native CPP hashes matched current files.
The tracked-input comparison also found changed source/src/serverfiles.h,
not included in the published D028 hash JSON. Its current observed hash is
`efca26aaefb9d33cc8623bc84dcf06f3a1f10d0b9d9664fff78790dab2bed75f`.
The header diff contains STANDALONE lifecycle guards; their browser boundary
needs the requested explicit fresh pin/verification before acceptance.

I made an execution sequencing error: a failed Python precheck and the build
were issued in the same shell without fail-stop sequencing, so compilation
continued after the assertion. All 61 target sources and link completed, but
this attempt is **not submitted as an accepted/released-input artifact**.
An attempted own-process interruption found that compilation/link had already
finished. No browser/game/server or listener was started.

The unaccepted complete bundle was preserved under
web/build/generated/t040/attempt-3/unaccepted-header-bundle. Then the complete
known D022 artifact from attempt-2/artifact was copied into d022-snapshot and
restored to current out, overwriting only the same exact Engine-owned output
file membership. No source or other worker output was reverted. Every old
runtime and metadata pin was checked after restoration. Future precheck/build
commands will be separate tool invocations so precheck failure cannot fall
through into execution.

## Per-criterion status

| T040 / D028 requirement | Result | Evidence |
| --- | --- | --- |
| Snapshot prior accepted bundle and validate all released inputs before mutation | FAIL for sequencing; contained | Initial precheck identified sixth header correctly but build ran afterward. Old immutable attempt-2/artifact preserved every D022 file and supplied the exact restored d022-snapshot. precheck-incident.json and question note retain details. |
| Compile/link real sources, no source/flag/port/pack changes | PASS for actual compiler operations only; accepted-input gate NOT RUN | Actual 61/61 objects and link exit 0, unchanged profile/pack. Does not authorize the omitted header identity or permit QA dispatch against this unaccepted result. |
| Integrity/native-output preservation | PASS for restoration; new accepted bundle NOT RUN | Exact old five-file/runtime/notices identity restored. Actual build result remains under attempt-3, with source/object/command hashes, but no new accepted artifact is published. No source edits/new flags. |
| Publish new accepted input/artifact pins for QA | NOT RUN | Waiting for precise current serverfiles.h non-STANDALONE boundary/hash acceptance. Current out stays D022. Do not dispatch attempt-3 as accepted output. |
| Retain historical evidence and freeze | PASS | D011/D016/D017/T031/T040 prior evidence intact; unaccepted attempt retained separately; current D022 output frozen. No old handoff/question/decision edited. |

## Exact remaining prerequisite

notes/questions/T040-engine-D028-header-pin.md asks MAIN to verify and publish
the additional header's current hash/boundary, or provide corrected stable
inputs. The five published CPP pins remain separately verified; no source
fix, extra flag, dependency or runtime is proposed. After fresh explicit
input verification, existing T040 can perform the same-scope integration.

Evidence: generated/t040/attempt-3/precheck-incident.json, result.json,
link.log, unaccepted-header-bundle, attempt-3.stdout.log;
generated/t040/d022-snapshot/snapshot.json. The question includes the exact
old/current header hashes. This is honest failure/containment evidence,
not a passing artifact or a policy rejection. Only MAIN accepts inputs/builds.
