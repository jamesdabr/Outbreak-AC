# T204 one guarded R preparation — failed slot retained

- Worker: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Authority: explicit MAIN once-only dispatch; T2041.0/D333/G2_FOUNDATION0.6; MAIN-T187-R-source-preparation-review-1 and T204-caller-source-review-1 read. The exact named execution was already explicitly authorized; no additional permission or broader workflow was inferred from the confirm-cross-system-execution skill.
- **ONE INVOCATION, EXIT1, FAILED_OR_INCOMPLETE. NO RETRY / SOURCE FIX / NEW SLOT / ALTERNATIVE.** Preparation-1 and its failure records are preserved. MAIN acceptance is separate.

## Exact command and original tool terminal

Cwd /Users/jd1/code/apps/outbreak; login=false; owned PTY tty=true; initial yield_time_ms=1000; max_output_tokens=2000; no script arguments:

```text
/usr/bin/env -i PATH=/usr/bin:/bin LANG=C LC_ALL=C PYTHONDONTWRITEBYTECODE=1 /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -B /Users/jd1/code/apps/outbreak/notes/proposals/T204-R-preparation-caller-1.py
```

Exactly one tools.exec_command invocation used that command. Original returned object, retained as T204_original_tool_first in functions session storage:

```json
{"chunk_id":"74a369","wall_time_seconds":0.439249916,"exit_code":1,"original_token_count":51,"output":"{\"elapsed_seconds\": 0.5110221250215545, \"error_type\": \"ValueError\", \"message\": \"finite original SDK graph bound\", \"no_retry\": true, \"schema\": \"T204_ORIGINAL_CALLER_1\", \"status\": \"FAILED_OR_INCOMPLETE\"}\r\n"}
```

There was no session_id: original process terminal was observed in the initial return. No observation timeout, resumed handle, reset deadline, polling, signal or interrupt was needed. PTY combines output streams; the caller source emits this failure JSON to stderr. Caller elapsed0.5110221250215545s and tool wall0.439249916s are distinct reported clocks, not substituted for one another. Both are far below original300s; no success receipt or PREPARATION_RETURNED_OK was emitted. Complete source terminal success and caller postflight did NOT occur.

## Immediate preflight observations

Immediately before invocation, ordinary read-only shasum rechecked caller14050/SHA9064addc3db8fffadb5738e4f198ca2cda7e77fd650f428dd5b277722a945694, review720935f6a378341c74f4aad1b539e81a16420e79d93c5a6289050820d99e0e4f, and all13 source roles against the dispatch. ls -ld reported BOTH R preparation-1 and attempt-1 absent; its exit1 was the expected absence observation, not the preparation command.

MAIN's immutable notes/reviews/MAIN-T204-caller-preflight-1.json records all34 frozen role identities and hashes before dispatch. The caller itself snapshots all34 against exact dev/inode/mode/nlink/size/mtime_ns/ctime_ns/hash before the only prepare call. Since it reached source prepare and created FAILURE, its source ordering implies those prechecks and bootstrap completed. This is distinguished from an independently retained successful full preflight receipt: the caller did not emit one.

## Retained slot and failure facts

Only tests/outbreak/geometry/G2/regression-G1/preparation-1 was created. Read-only ls shows exactly these two files, total246 payload bytes:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| FAILURE | 48 | e901b6f6fe175fa44291e115aa441e28be03341d18f7010873ccdd5bc4c589e0 |
| failure.json | 198 | 22c484a77c98451ab68f82c5bf0eee57cedcd946f73d85627a1a85307abc02c8 |

FAILURE content is exactly `preparation incomplete; preserve on any failure` plus newline. failure.json:

```json
{
  "elapsed_seconds": 0.4705552910454571,
  "primary": {
    "message": "finite original SDK graph bound",
    "stage": "preparation",
    "type": "ValueError"
  },
  "secondary_retention": null
}
```

No manifest.json, success terminal, setup.bin, corpus.bin, expected.bin, catalog.json, coverage.json or simulated-regressions.json exists in the slot. All144 fake controls and16384 row/product generation were NOT REACHED; no passing control count or regenerated equality is claimed. R attempt-1 remains absent. No Q operation/root, compiler/target child/actual/query/FFI/SDK copy/network/Git was performed. Sources were only read and R's single approved bootstrap/prepare was executed.

## Failure localization from source, not a retry/probe

Read-only source inspection finds tree_snapshot at1248..1258 raises this exact ValueError when len(members)>8192. Its message says SDK, but tree_snapshot is also used by historical_inputs. prepare calls historical_inputs BEFORE bind_g0/tool/header/SDK/control/data work. historical_inputs visits G1 first, then T193/T195 and old source archives. Therefore the source-order inference is that the first G1 historical graph exceeded this shared8192-record cap during the pre-preparation historical snapshot; no original SDK traversal had yet been reached. This is a source inference from the unique error and fixed order, not a newly executed tree counter or a retained graph receipt. No extra graph scan, cap change, historical omission, preparation retry or expectation repair was attempted. MAIN must dispose the exact next step separately.

## Postflight observations and limits

After the original terminal, ordinary read-only shasum checked caller plus ALL34 frozen role hashes: each matches the caller EXPECTED table/MAIN preflight. In particular production b5b842a0f745205e877f765a61a0dcc6a5b5f53a0aebe0f99ee2e9cd07c4c804, Q verifier27c53d9ade3c64d7b242657eb828a33a6db6b97d36ad315ba1a2deffc70ea3ec, R verifier0e24349dcd72e3af7a1a5aa4ad44d2863d44786e826310215987ce2e3b7b60b4 and canonical Python4e28e811a89aeac6eed668ae641c7f85f5831e42e8dc6cd9a85a3bcc032ec46a are unchanged. The other ten source/header roles,18 current controls,D333,T204 likewise match. No source/control/evidence/history/SDK/tool was edited by World.

The caller's complete post-return34 descriptor-identity snapshots were NOT REACHED because prepare raised. Source historical before/after equality also did NOT complete. A post-terminal digest match is not full descriptor/topology or SDK/history protection proof. This failed operation provides no successful source/ownership/terminal acceptance. Bounded failure persistence produced the two readable files above; it is not successful preparation durability/marker removal. No original time/byte budget was reset. No artifact hash beyond the two failed-slot records is claimed.

PASS only: exact once-only dispatch, observed original exit, failure preservation, bounded read-only reporting. FAIL: guarded R preparation. NOT RUN/NOT QUALIFIED:144 controls, original five regenerated products, schema/data coverage, compiler/emitted/functional/current G1/G2/caller/runtime/MVP gates. All complete production/Q source reviews and downstream holds remain. This is the NEW post-terminal handoff; World stops pending named MAIN disposition.

Skill used: [confirm-cross-system-execution](/Users/jd1/.codex/skills/confirm-cross-system-execution/SKILL.md), to inspect and respect the explicitly approved entry point and local write boundary. It granted no extra execution.
