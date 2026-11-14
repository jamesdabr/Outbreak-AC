# T127 D147-pair-1 terminal refusal handoff

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket/revision: T1271.1 / D147 explicit finalized-pins dispatch; smoke0.7/admission0.4/GOVERNANCE/BROWSER_FOUNDATION/P0 0.5.
- State: ONE invocation terminal REFUSED_OR_FAILED. No retry/repair/workaround or runtime acceptance.
- Writes: no non-controller workspace writes during live CLI; only own new post-terminal question and this handoff. Controller created no retained output roots. Other-worker quiescence is not released by this handoff.

## Before invocation

Read T1271.1/exact D147 Markdown, accepted source/checkpoint/freeze records and fixed run/policy/supervise/observer/ownership effect/cleanup paths as DATA. Verified raw finalized pins55981916bytes/SHA256c10b343d5175c27591e340a8793fcc6c2b61de1eae99a77124692ae0155ffb4e. Exact1344file input map, preservation167141files/47397directories/9695opaque links/14specials/threeabsent roots observed. All nine source hashes match accepted checkpoint2 and pins; accepted freeze SHA942fffc368ffc0afb8c72a06c6bedd7ae8d467e0da865e6bb6c555c932a8f605. Exact destinations absent. No extra full inventory or actual gate/admission test.

The direct dispatch explicitly authorized only accepted fixed controller normal_pair subprocess/loopback effects and exact roots. Initial fixed Python controller ran via inspected stdlib-only supervisor; no manual effect hook or target selector. No project import outside the one controller call; no preparation/test/build/inspector/probe/admission invocation added.

## Exact command and bounds

Cwd /Users/jd1/code/apps/outbreak. PYTHONPATH/PYTHONHOME unset; PYTHONNOUSERSITE=1; other environment inherited. Python3.11.9 -B. Fixed child argv:

```sh
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B /Users/jd1/code/apps/outbreak/web/runtime/pair-smoke-v2/run.py --pins /Users/jd1/code/apps/outbreak/notes/decisions/D147-candidate-pair-runtime-pins.json --pins-sha256 c10b343d5175c27591e340a8793fcc6c2b61de1eae99a77124692ae0155ffb4e
```

One Popen child, start_new_session, stdinDEVNULL, separate captured stdout/stderr, original cwd. Supervisor allowed600s whole CLI (including pre-effect gates), with590s work/read deadline and<=10s owned-group timeout cleanup reserve; combined output<=8388608bytes. Original controller effect180s/owned-cleanup/dependency/privacy gates unchanged. Supervisor never wrote files. The yielded tool session53643 was retained/polled to authoritative completion, never restarted on observation timeout.

## Authoritative terminal evidence

```json
{
  "P0": false,
  "argv": [
    "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3",
    "-B",
    "/Users/jd1/code/apps/outbreak/web/runtime/pair-smoke-v2/run.py",
    "--pins",
    "/Users/jd1/code/apps/outbreak/notes/decisions/D147-candidate-pair-runtime-pins.json",
    "--pins-sha256",
    "c10b343d5175c27591e340a8793fcc6c2b61de1eae99a77124692ae0155ffb4e"
  ],
  "attempt": "D147-pair-1",
  "authority": false,
  "calls": 1,
  "child_reaped": true,
  "combined_output_limit_bytes": 8388608,
  "cwd": "/Users/jd1/code/apps/outbreak",
  "elapsed_seconds": 19.25273037503939,
  "environment": {
    "PYTHONHOME": "UNSET",
    "PYTHONNOUSERSITE": "1",
    "PYTHONPATH": "UNSET",
    "other": "inherited"
  },
  "exit_code": 2,
  "fault": null,
  "kind": "T127_ONE_FIXED_CONTROLLER_SUPERVISION",
  "stderr": "",
  "stderr_bytes": 0,
  "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "stdout": "{\"status\":\"REFUSED_OR_FAILED\",\"authority\":false,\"P0\":false}\n",
  "stdout_bytes": 60,
  "stdout_sha256": "8881d1d985bcd6b258512ceed8b1417fe12c748e206d891680870a131099be6f",
  "supervisor_maximum_seconds": 600,
  "supervisor_signals": [],
  "supervisor_workspace_writes": false
}
```

Actual controller exit2 after19.25273037503939seconds; fault null, child_reaped true, supervisor_signals empty. No timeout/overflow/fallback.60stdoutbytes,0stderrbytes; both well below8MiB. Raw stdout was exactly the generic CLI catch summary plus newline; no exception detail or runtime_started flag emitted.

## Post-terminal read-only evidence and cleanup facts

Only fixed metadata/output-path inspection after completion, no extra gate/controller/admission or live ps/lsof probe:

- Pins still55981916bytes and exact externalSHAc10b343d5175c27591e340a8793fcc6c2b61de1eae99a77124692ae0155ffb4e.
- All nine accepted checkpoint2 source hashes unchanged.
- /Users/jd1/code/apps/outbreak/web/transport/results/candidate-pair/runtime-D147-pair-1 ABSENT; parent candidate-pair ABSENT.
- /Users/jd1/code/apps/outbreak/web/server/run/candidate-pair-D147-pair-1 ABSENT; existing native run parent retained.
- All three serialized absent_roots still absent. Receipt/report/ledger/validated-plan/native log/private profile/partial attempt evidence unavailable because no attempt root exists.
- Initial controller process reaped by supervisor, no supervisor signal sent. No retained native/browser/observer process/tuple/private cleanup record; no cleanup PASS or independent whole-system port/process claim fabricated.

Observed refusal is before any retained reservation, consistent with fixed pre-effect gate ordering. Exact rejected condition is UNKNOWN from the intentionally generic catch; it is not reported as a particular pin/source/port/alias/admission mismatch. No browser/native/Node/inspector execution or runtime result is evidenced. The API/runtime-started distinction cannot be promoted from absent detail into a success claim.

## Stop and integration

Question notes/questions/T127-world-pre-reservation-refusal.md asks MAIN for precise diagnosis/next separately scoped action. No internal gate call, alternate import, extra probe, repair, pin/source/receipt rewrite, second attempt or retry. Failed finalized attempt is not replaced; initial unrelated author UNSEALED file remains outside this worker's changes.

No P0/gameplay/server-authority/performance/human/MVP acceptance. Player/QA holds unchanged. MAIN reviews exact refusal and alone releases quiescence/further work. Own question/handoff writes were deferred until controller terminal completion as explicitly dispatched. Pins/source/artifacts preserved; no other workspace mutation or worker dispatch.

