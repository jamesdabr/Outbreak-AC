# Ticket handoff — T265 REVIEW-READY

- Worker: Player /01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T2651.0/D446; contract BLACKWOOD_NATIVE_BUILD_PREPARATION0.2, reread before submission. Authoritative ticket status unchanged.
- Base commit and pre-existing edits: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work. No Git command. Accepted T167/D444 and failed T264 evidence retained.
- Changed files: ONLY web/server/blackwood_candidate/{stage.py,test_preparation.py,SCHEMA.md,README.md}; new preparation-1/plan-pass-7.json, preparation-1/pass-7/**, supervisor-fixtures-1/pass-7/**; own new T265 notes. build.py/verify.py unchanged.
- Commit or patch reference: none. Four-file diffs from accepted pass-6 snapshots: notes/handoffs/T265-player-source-diffs-1.md.

## Acceptance evidence

PASS one targeted guarded pass after own/direct-call inspection:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B web/server/blackwood_candidate/test_preparation.py --pass-id pass-7 --plan-sha256 a2dfd976759128145ae861390cb98473efbd77af7e3ab8185a22aed4e0faae40
```

20/20 SIMULATED checks PASS in14.399840s before final result publication,24,487 observed fake-output bytes before small summary,5,109,535 storage bytes before results. Nine expected guard self-check denials; zero unexpected denials. Existing caps256cases/300s/8MiB output/128MiB storage unchanged; original terminal cutoff remains active through persistence.

Result: web/server/blackwood_candidate/preparation-1/pass-7/result.json SHA256 `fea0496db75f5ebf71f8fbdcac1d51ecee9ed638fda0dd94fec1c533a7302b79`. Per-case details and the second matching result remain under supervisor-fixtures-1/pass-7. Six source snapshots match current source bytes and the pinned plan/result.

Coverage:19 targeted D446 checks plus the existing full126-command/32-object/two-link fake build and independent verifier/optional-receipt success. Seven fake opaque artifacts preserve by exact metadata with zero content reads; unknown unreadable still attempts normal hashing and refuses; readable bytes still change preserved hashes. Unknown path/field, bool mode, hashed-input promotion, source/dependency consumption, missing known artifact, file type, device/inode/size/mode/owner/group/link/mtime/ctime changes refuse. The missing-known test exercises production presence enforcement against a synthetic root via explicit mock, without importing actual inode-bound artifacts. Original202 case definitions and all prior results remain intact; universe now221, only20 selected checks executed as authorized.

Before the sole pass, MAIN requested mandatory production presence of all seven paths. Updated the unexecuted plan accordingly; earlier draft preserved in notes/handoffs/T265-player-unexecuted-plan-7-draft-1.md. No prior operation or pass root existed for that draft; no retry/occupied overwrite occurred.

## Implementation status

Implemented: exact seven D446 literal path/metadata identities; strict `opaque_files` preservation map and matching protected-inventory rows; all seven required in production preservation validation/protected inventory. Opaque entries never open for content and cannot enter ordinary/hash/consumed source/header/dependency roles. Type-strict exact comparison rejects unknown metadata/paths; unreadable files outside the seven retain normal read refusal. Readable hashing, process/deadline/alias/ownership/output rules unchanged. Private preservation schema adds only the D446-authorized field; no gameplay/shared engine interface change.

Final source SHA256:

- stage.py: `48412ffbbbb3c8f07253c988e0dca76ef2cc2e0a960f5f09668b0fee02a0ff81`
- test_preparation.py: `9707cb57fca5fadf9d226a1d7aee1ebd40c55036b3ff061d9add94f34ee7e427`
- SCHEMA.md: `85a8d45775c21b554fd8b67ca23f1c9462dcba6d3e3cdc047aa01aca005dd570`
- README.md: `d30537d8180c3ec5e82bd4b343eae29a5e44a770d2c2e126e4e6fc82c2a6d049`

SIMULATED only: seven metadata records in targeted fixtures are replaced with freshly created fake-file identities inside existing effect guards. No actual seven artifacts opened/chmodded or otherwise changed. Content integrity for those seven remains explicitly unavailable under D446.

NOT RUN: T264 retry/new current-input observation, original preservation scan, actual project plan/build/verify/tool/version/FFI/compiler/signing/framework-copy/native/browser/server/network/runtime/Git. Actual attempt root remains absent. T264 observation SHA remains c4d4315a926ee31ff101bcb064c4f7d4549d34a3a5726c7807949eed099bc1da. No manifest, execution control, dependency or asset added.

## Integration and questions

No remaining targeted-check failure. MAIN reviews this narrow correction before separately releasing a fresh current-input observation with the updated stage pin/schema. That observation supplies the missing inventory/control size readiness for a concrete native build command; actual build/runtime remains separately gated. No new proof framework or unrelated full rerun. Stop at REVIEW-READY with no live process handle; T149/QA and other holds remain.
