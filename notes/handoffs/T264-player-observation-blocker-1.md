# Ticket handoff — T264 current-input observation blocked

- Worker: Player /01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T2641.0 RELEASED READ-ONLY INPUT OBSERVATION D445; reread before handoff. Authoritative status unchanged.
- Phase / contract revisions: BLACKWOOD_NATIVE_BUILD_PREPARATION0.1; accepted T167/D444; D445 observation only.
- Base commit and pre-existing edits: HEAD metadata bdaa8df7ec39d9408f97feda4560832d7ef26c3c; preserved shared work, no Git commands.
- Changed files: ONLY new notes/preflight/T264/{observe.py,observation.json} and this own handoff. No accepted source/evidence or original file changed.
- Commit or patch reference: none.

## Acceptance evidence

Executed ONCE after full collector/direct-call inspection:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -S -B notes/preflight/T264/observe.py
```

Result: BLOCKED_INPUT_READINESS, exit0 publishing a blocked observation,12.007528s including publication. Collector SHA256 `fd273aa0bfedee05bbac8c226a1441b05b1e434e74dd304241ae1ebddedc608a`. Observation36,878bytes, SHA256 `c4d4315a926ee31ff101bcb064c4f7d4549d34a3a5726c7807949eed099bc1da`.

Captured successfully: HEAD metadata; all six accepted T167 source identities; four T163 source and three reference identities; five installed launcher role/hash/mode/link identities;96-member original framework inventory and unsigned binary identities; eight pinned Darwin ABI header identities; seven lazy Python source/extension/existing-bytecode roles;68 ordinary Python authoring identities. No fixed identity mismatch was recorded. Framework read took0.017400s. This is ordinary byte/metadata observation, not ABI/tool execution compatibility evidence.

Concrete blocker: accepted stage.View.preservation() raised PermissionError after11.925207s at:

```
/Users/jd1/code/apps/outbreak/web/repro/tests/prerequisites/FIXTURE_ONLY-a6a8xiso/repo/web/build/.cache/bad-mode
```

Read-only lstat confirms this pre-existing file is12bytes, mode0000, uid501/gid20; its .cache parent is0755. No chmod/delete/repair, escalation, exclusion or retry was attempted. The broad fixed preservation forest includes this fixture, so ordinary current-byte hashing cannot complete.

## Implementation status

Implemented and observed: short fixed-path stdlib collector, accepted stage-only explicit import with bytecode disabled, exclusive output, no self-reference, forbidden process/network/FFI events denied. Existing result refused on occupancy. Observation retains all completed fields and exact first error.

Incomplete/NOT RUN because of the preserved read failure: complete preservation/protected inventories, serialized32MiB-control/128MiB-record readiness, potential source/CLT/SDK closure and approved alias normalization. Their result fields are absent rather than reported as complete. No build-time inference or runtime/performance acceptance.

No build/verifier/harness or ctypes import, tool/version/compiler/signing/native/FFI/framework-copy/build/runtime/server/browser/network/Git invocation, actual attempt reservation, actual source manifest or execution authorization. No fixtures/tests/proof pipeline added. T149/QA and other holds unchanged.

## Integration and questions

The next concrete native-build dependency is MAIN resolution of this unreadable preserved fixture member under separate authority, followed by an explicitly released fresh observation/output path if needed. This ticket does not permit repairing originals or retrying the occupied output. The accepted builder/control caps and protection semantics were not changed. No live collector/process handle remains. Stop for MAIN review; preparation observations are not native execution authorization.
