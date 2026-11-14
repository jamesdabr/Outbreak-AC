# T207 once-only R preparation — failed inventory guard

- Worker: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Authority: T2071.0/D344/G2_FOUNDATION0.7 and MAIN's literal exact dispatch, notes/reviews/MAIN-T207-exact-dispatch-1.md. Read caller and independent caller/effect review before execution.
- **ONE INVOCATION / ORIGINAL SESSION TERMINAL EXIT1 / FAILED_OR_INCOMPLETE. NO RETRY, REPAIR, SOURCE CHANGE, ALTERNATIVE OR NEW SLOT.** R preparation-2 retains its failure marker/evidence; prior preparation-1 remains immutable. MAIN acceptance is separate.

## Fixed dispatch and preflight

Immediately before the one invocation, standard shasum verified caller14096/SHA81af01d60501465b2e66513c474284c355a755ad1b1f1bc57e9cf4f08319d1ef; independent review72bfcc21a4fb01efab307a2b7bff8225e23a48208cb7bd44ce310d6d66cab688; MAIN preflight8b1f6616dc361bc17703b68743dccaef4b788f6580978cef8be15e959181e59e; and R verifiera2646666a9fd88aed44b0309c9e93325803d5a74a4391f9254e95ec0682bdc5b. ls confirmed all four proposed roots absent (R preparation-2/attempt-1 and Q preparation-1/attempt-1). MAIN's preflight/dispatch bind all34 full identities/hashes. No parser/import/probe/rehearsal occurred before the authorized bootstrap.

Cwd /Users/jd1/code/apps/outbreak; login=false; tty=true; initial yield_time_ms=1000; max_output_tokens=8192. Exact command, no extra script argument:

```text
/usr/bin/env -i PATH=/usr/bin:/bin LANG=C LC_ALL=C PYTHONDONTWRITEBYTECODE=1 /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -B /Users/jd1/code/apps/outbreak/notes/proposals/T207-R-preparation-caller-1.py
```

This NEW T207 command was invoked once, not a T204 replay. Both command flags/environment and source/caller are exactly MAIN's dispatch.

## Original tool objects and terminal

Initial exec_command object, retained as T207_original_tool_first in functions session storage:

```json
{"chunk_id":"3399f7","wall_time_seconds":1.0026485,"session_id":65249,"original_token_count":0,"output":""}
```

One write_stdin poll of SAME session65249, chars empty, yield_time_ms1000/max_output_tokens8192, returned the terminal object retained as T207_original_tool_poll1:

```json
{"chunk_id":"7aea69","wall_time_seconds":0.000013958,"exit_code":1,"original_token_count":61,"output":"{\"elapsed_seconds\": 1.8919164580293, \"error_type\": \"ValueError\", \"message\": \"closed definition inventory source/outbreak/p1_geometry.cpp:q_axes_feature\", \"no_retry\": true, \"schema\": \"T207_ORIGINAL_CALLER_1\", \"status\": \"FAILED_OR_INCOMPLETE\"}\r\n"}
```

No session restart, second command, observation timeout, signal, interrupt or deadline reset occurred. Original terminal exit1 was observed on that sole live handle. PTY combines streams; caller source prints failure JSON to stderr. Caller1.8919164580293s/source1.8225236660800874s/tool per-call wall values are distinct observations. No PREPARATION_RETURNED_OK or successful source/caller terminal was emitted. Original300s was not exhausted; no output/metadata cap exhaustion is reported.

## Retained files and product/control status

Read-only ls shows exactly two files in R preparation-2,289 payload bytes total:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| FAILURE | 48 | e901b6f6fe175fa44291e115aa441e28be03341d18f7010873ccdd5bc4c589e0 |
| failure.json | 241 | 6ef026ce1b24dae24964a6b9dcf615a2f538d6be3e63ee587512a78fa116695a |

FAILURE is `preparation incomplete; preserve on any failure` plus newline. failure.json is:

```json
{
  "elapsed_seconds": 1.8225236660800874,
  "primary": {
    "message": "closed definition inventory source/outbreak/p1_geometry.cpp:q_axes_feature",
    "stage": "preparation",
    "type": "ValueError"
  },
  "secondary_retention": null
}
```

No manifest/success terminal/simulated-regressions/setup/corpus/expected/catalog/coverage product exists. Full144 fake controls did NOT complete or produce a retained receipt. Original16384 row generation and five exact regenerated P5 equality gates were NOT REACHED. No generated data/control PASS is claimed.

## Source-only localization, with no corrective execution

Ordinary text inspection after terminal finds production line922 declares `unsigned q_axes_feature(const uint8_t (&axes)[3])`. R source_frame_catalog line2459's closed return-type pattern includes uint32_t/uint64_t and other named types but omits literal unsigned. Its group() scanner therefore cannot find that definition and raises the exact closed-inventory guard at2477. This is text/source inference supporting the reported refusal, not a separately invoked parser/control or compiler result. No catalog/code/pin was amended.

The source construction order places source_role_regressions after the supervisor/terminal/guard/analyzer/focused/D260 methods in the preparation's dictionary construction; source_role_regressions calls source_frame_catalog before its16 cases. The next G2 sixteen-case function is later. Earlier calls returned far enough to reach this guard, but their receipts were not retained because the whole construction failed. No complete count/acceptance is inferred for them. This is a harness source-inventory failure, not a production geometry counterexample or failed real corpus row.

Unlike T204's history-bound refusal, T207's fixed order reached the controls only AFTER initial source/dependency/history/G0/tool/header/SDK snapshots. That ordering implies those preflight calls returned; it does NOT establish complete before/after protection, successful SDK/role acceptance or a durable completed preparation. Those later comparisons/terminal and caller's34-role post-return snapshots were NOT REACHED.

## Read-only postflight and limitations

After original terminal, standard shasum checked ALL34 frozen roles:13 current source roles,18 CURRENT_CONTROLS,D344,T207 and canonical Python; all hashes match caller EXPECTED/MAIN preflight. Caller/preflight/review hashes also remain exact. Key sources remain productionb5b842…c804, Q verifye778b93f…1fdc and R verifya2646666…dc5b. No source/authority/header/wrapper/runner/tool/dependency/SDK/history was edited by World.

Prior T204 failed preparation-1 still has exactly its original hashes: FAILURE48/e901b6…9e0 and failure.json198/22c484…02c8. Its caller9064addc…5694 and preflight8d92579f…ddc1 remain unchanged by read-only shasum. T207's caller81af01…d1ef and preflight8b1f66…e59e also remain unchanged. R attempt-1/Q preparation-1/Q attempt-1 are still absent. No Q operation, actual(), compiler/target child/query/FFI/SDK copy/network/Git ran.

Post-terminal digest matches are not full descriptor/topology or whole SDK/history equality proof. Caller post-return34 descriptor checks, source full before/after graphs/dependency/tool/header/SDK comparison and success terminal did not complete. MAIN must independently review the original command and failed slot. Bounded failure persistence yielded readable marker/failure facts, not successful marker removal/durability acceptance.

PASS only exact once-only dispatch/original handle retention/observed failure preservation and bounded read-only reporting. FAIL guarded R preparation. NOT QUALIFIED full144 controls/five products/source-frame/normal-callee/emitted/query/functional/current G1/G2/caller/runtime/MVP gates. No next operation or source correction is authorized. World stops pending named MAIN disposition.
