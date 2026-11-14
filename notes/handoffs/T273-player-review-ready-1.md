# Ticket handoff — T273 REVIEW-READY

- Worker: Player /01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T2731.0/D462; BLACKWOOD_NATIVE_BUILD_PREPARATION0.6, reread before submission. Authoritative status unchanged.
- Base/pre-existing edits: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work; no Git command. Historical attempts/controls/manifests, actual SDK/tools and game/client/T266 source untouched.
- Changed files: ONLY web/server/blackwood_candidate/{stage.py,build.py,verify.py,test_preparation.py,SCHEMA.md,README.md}; NEW preparation-1/plan-pass-11.json, preparation-1/pass-11/**, supervisor-fixtures-1/pass-11/**; own source-diff and this handoff notes.
- Patch reference: notes/handoffs/T273-player-source-diffs-1.md against accepted pass10 snapshots. No commit.

## Acceptance evidence

PASS sole inspected guarded fake-only pass11:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B web/server/blackwood_candidate/test_preparation.py --pass-id pass-11 --plan-sha256 fe20e2dd996dba4713c06a7426ab7090562c101f6ef3925fcddd2e365b7e340d
```

7/7 selected cases passed in23.074262s before result publication,44,525 observed fake-output bytes before small summary,4,766,735 storage bytes before results. Nine expected guard self-check denials, zero unexpected denials. Existing256cases/300s/8MiB/128MiB caps and pre-import effect guards unchanged, with original cutoff through persistence.

Result: web/server/blackwood_candidate/preparation-1/pass-11/result.json SHA256 `44409f2a42fd004212f8d15966e99b1dbc0093f6b7fb2c11a1162e76f3d16ee7`. Six current sources match executed snapshots and plan/result pins. All2,116 new regular files are readable; no physical special/unreadable nodes added.

Six new focused cases cover four exact alias/canonical-target successes;20 raw-edge text/mode/type/missing refusals;24 target hash/hardlink/symlink/missing-input/missing-SDK/SDK-hash refusals; unknown alias and extra-hop refusal; explicit pthread intermediate-edge and symlink-ancestor refusal; complete four-alias raw trace with canonical records and independent verifier success. Existing nominal complete126-command/32-object/two-link/receipt success also passed, using the same four-alias trace. Both release/debug traces contain all four raw spellings; canonical records contain only the three canonical target keys, preserving origin/hash/archive-member format. Original250 case bodies remain an AST-identical prefix; six cases appended, universe256. No unrelated full rerun.

## Implementation status

Implemented a pure fixed stage.sdk_link_path validator for exactly:

- SDK/usr/lib/libc++.tbd -> libc++.1.tbd
- SDK/usr/lib/libz.tbd -> libz.1.tbd
- SDK/usr/lib/libSystem.tbd -> libSystem.B.tbd
- SDK/usr/lib/libpthread.tbd -> libSystem.tbd -> libSystem.B.tbd

Every edge requires exact raw text/symlink type/mode0755 and ordinary ancestors. The terminal requires canonical ordinary single-link identity/ancestors, matching resolution, declared input plus SDK entry, and equality of both declared hashes with current target bytes. pthread explicitly checks both edges. Unknown aliases/extra hops/changed targets refuse. Builder and independent verifier each reconstruct their own trace through this shared fixed validator; no call to builder's reconstruction from verifier. Canonical record schema unchanged. Existing object/framework/archive/command/EPERM/ownership/deadline/cap and separate two-header alias rules unchanged; no supplied alias map or new selector.

Final source SHA256:

- stage.py: `39a53fcb4bc8a2c07d25b3d1857e2139f41f3f4403b025e06fdcb2dba95076ba`
- build.py: `62833b6521f9958cd134aae45fec3fc1386ce07dc19cc50f7ab536a3f6397132`
- verify.py: `add9ea086f06ce1398d1cd56b3fd68742c2a559a177701ce3305e274755e42c5`
- test_preparation.py: `078d419fac02c6c7339571d721e458cd5c1399705933de708b98db1df1940106`
- SCHEMA.md: `ba04b9c698901c3110f6a107a1eeb5da8d77ea1b8a01110cae90674530072bcb`
- README.md: `8a6d6108b07b583988d550296a2fa70f7a12aac9f590878f7d7416e2c09a45d9`

SIMULATED: all SDK metadata/aliases, tools, compilation/linking/signature/inspection and verifier effects use synthetic files/fake boundaries under the existing harness. No actual SDK observation or writes, tools/process/signals/FFI/compiler/build/actual verifier/runtime/network/Git/attempt retry occurred. No accepted native artifact/runtime result is claimed. Historical failed artifacts and their controls/manifests remain immutable.

## Integration and questions

No targeted-check failure remains. MAIN reviews stable source/results and separately authors fresh candidate3 manifest/control before any actual build. Failed candidates must not be retried or rewritten; D461 verification remains unreleased here. Stop at REVIEW-READY, no live process handle remains. QA remains paused; full MVP gates remain.
