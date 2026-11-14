# T136 — Actual single capability diagnostic terminal FAIL

- Worker: Player / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e.
- Ticket / revision: T1361.2, D162 direct human approval plus explicit exact caller dispatch. No authoritative status change by worker.
- Phase / contract revisions: capability0.3/D108/D154/D162; browser prerequisite only; QA paused.
- Base commit and pre-existing edits: accepted T103 exact frozen component c9022e2af4875c3affa44977940653149fbfa1a83f248a416ddeb3e2b0390640; all18 retained files verified byte/size/mode unchanged after actual terminal. No source/doc/test/cache/reference edits or Git mutation. Earlier D155 pre-CreateProcess refusal/handoff preserved.
- Changed files: source-created NEW web/qa/capabilities/T103/run-1/report.json and owned browser-temp directory (private Chrome profile removed), own post-terminal question T136-player-websocket-guard-observed-leak.md and this handoff. No other run output files retained.
- Commit or patch reference: none.

## Acceptance evidence

ACTUAL FAIL: run-1/report.json,29744bytes, SHA256 `2e0fdca3546415b4d03efe98fc6853a653ffcad402337f29d428d554425d061a`. Error `denied HTTP/WS leaked or incomplete`; overall_scope PARTIAL. Exactly ONE actual caller/zero-argument probe call; no separate probe/import test and no restart. Chrome156.0.8078.80 launched headed with reviewed sandbox/flags and own profile; actual viewport1280x720/DPR1. Environment fixed Node24.19.0 SHA27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1, macOS arm64. Exact caller SHA2a227ef4960bce08fd640152fd39ecbb959a4fbca8322a8e6b5dd05df02a7a06/3968bytes verified before launch and by supervisor. No new install/dependency/game/native/gateway/remote call.

| Saved per-capability check | Report value | Observed scope / limit |
| --- | --- | --- |
| http_guard | NOT_OBSERVED | Cold HTTP allowed; denied HTTP actual CDP inspector block and zero HTTP sink requests. Early assertion prevented complete cold/warm classifier. |
| ws_guard | NOT_OBSERVED | Actual failure condition: both forbidden WS handshake upgrades reached owned sinks. No complete blocking proof. |
| child_guard | NOT_OBSERVED | No iframe reached; stopped on cold page. |
| cache | NOT_OBSERVED | Four cold200 responses only; no warm navigation/revalidation/cache-hit claim. |
| gpu | NOT_OBSERVED | Raw own WebGL/SystemInfo facts collected before failure; classifier not reached, no game GPU acceptance. |
| cleanup | PASS | Actual public close/exit/profile/process-group/port/lsof facts below; no fallback. |

Guard transcript completed before requests. Cold allowed HTTP data and allowed WS echo/subprotocol succeeded. Sink counts: http_requests0,ws_upgrades1,wrong_path_upgrades1,allowed_ws1. CDP WS errors for both forbidden paths were `Connection closed before receiving a handshake response`, not ERR_BLOCKED_BY_CLIENT; they reflect the tiny fixture servers destroying a reached handshake. Promise rejection alone was not mislabeled guard enforcement. Source stopped before warm page/iframe. No aggregate capability PASS or installed full-guard support.

Raw own-canvas renderer: ANGLE (Apple, ANGLE Metal Renderer: Apple M3 Max, Unspecified Version), unmasked vendor Google Inc. (Apple), WebGL1,128x72 buffer/errors[0]/context_lost:false. SystemInfo independently reports ANGLE Metal Apple M3 Max. These are bounded actual fixture observations only; saved gpu check remains NOT_OBSERVED, no game context/frame/performance/RSS proof.

CLEANUP PASS: Chrome root8919/public parent8918; source retained owned PGID8919, actual group gone. Chrome exit0/signalnull; private profile removed; context/pages/browser/server closed, both public CDP sessions DETACHED, closed_event/detach_completed true. All29876/29877/29878/control62476 rebind true; lsof exit1 stdout/stderr empty; all listeners closed, acquisitions_complete true, errors[]/fallback:false. No manual post-terminal cleanup/process signals or independent runtime verification was invoked. Caller8918 reaped; supervisor tool session44147 terminal exit0, inner caller exit1; no live owned process evidenced by source cleanup.

Bounds: source elapsed1991.6609999999998ms, caller1993.4371250000002ms, outer supervisor2.151626625098288s (<150s).17events/19network/4HTTP/1page/1navigation; no overflow. Outer stdout511bytes,stderr0, no timeout or signals. Actual post-handle output778bytes; report+post-handle30522bytes (<8MiB). Early raw interval remains NOT_OBSERVED/PUBLIC_HANDLE_NOT_AVAILABLE_EARLY/complete_byte_bound_proven:false; launch_start245.30433399999998ms/handle_available1070.0126249999998ms, no invented early-byte zero. Combined observed bound PASS covers only the available interval; overall_scope remains PARTIAL.

Captured terminal supervisor receipt (not a source report rewrite):

```json
{
  "kind": "T136_SINGLE_CALL_SUPERVISOR",
  "caller_sha256": "2a227ef4960bce08fd640152fd39ecbb959a4fbca8322a8e6b5dd05df02a7a06",
  "argv": [
    "/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node",
    "/private/tmp/outbreak-T136-approved-caller-1.cjs"
  ],
  "cwd": "/Users/jd1/code/apps/outbreak",
  "environment_overrides": {
    "NODE_OPTIONS": "",
    "NODE_COMPILE_CACHE": "UNSET"
  },
  "tool_session_id": 44147,
  "tool_supervisor_exit_code": 0,
  "pid": 8918,
  "owned_process_group": 8918,
  "invocations": 1,
  "reaped": true,
  "exit_code": 1,
  "elapsed_seconds": 2.151626625098288,
  "supervisor_reason": null,
  "signals": [],
  "combined_observed_output_bytes": 511,
  "stdout": {
    "bytes": 511,
    "sha256": "6efeb00055fef8c2c0a15e33b953dc680f2975116cc9ef4c04d6362a33eb6d12",
    "text": "{\"kind\":\"T136_ACTUAL_FIXED_CAPABILITY_PROBE\",\"calls\":1,\"status\":\"FAIL\",\"overall_scope\":\"PARTIAL\",\"checks\":{\"http_guard\":\"NOT_OBSERVED\",\"ws_guard\":\"NOT_OBSERVED\",\"child_guard\":\"NOT_OBSERVED\",\"cache\":\"NOT_OBSERVED\",\"gpu\":\"NOT_OBSERVED\"},\"cleanup_status\":\"PASS\",\"elapsed_ms\":1993.4371250000002,\"report\":{\"path\":\"/Users/jd1/code/apps/outbreak/web/qa/capabilities/T103/run-1/report.json\",\"bytes\":29744,\"sha256\":\"2e0fdca3546415b4d03efe98fc6853a653ffcad402337f29d428d554425d061a\"},\"game_performance\":false,\"P0\":false}\n",
    "text_truncated": false
  },
  "stderr": {
    "bytes": 0,
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "text": "",
    "text_truncated": false
  }
}
```

## Implementation status

Actual: one released local diagnostic ran and failed closed on incomplete WS guard enforcement; owned cleanup completed. Its raw immutable report is preserved unchanged, including individual NOT_OBSERVED fields and failure facts. No later stage was simulated to replace missing data. Existing T103113-fixture preparation remains historical FIXTURE_ONLY, not runtime support evidence.

Incomplete: full blocking/target coverage, warm cache facts, iframe check, game GPU/input/audio/frame/RSS/performance/P0/human acceptance. QA remains paused. The source method was not tuned or repaired; no second actual call is authorized or performed.

## Integration and questions

Own question T136-player-websocket-guard-observed-leak.md identifies exact evidence and asks MAIN to decide future guard feasibility. Source/flags/topology/guard APIs/installed dependencies/contracts remain unchanged. Historical preparation graph verified intact; run-1/report.json newly retained as failure evidence only. This single-use release is consumed. Do not rerun/overwrite/repair; MAIN reviews the actual observations and separately scopes any further work.
