# T135 D157-pair-1 actual runtime — terminal FAIL

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket/revision: T1351.1 / D157 explicit finalized dispatch; smoke0.8/admission0.4/GOVERNANCE/BROWSER_FOUNDATION/P0 0.5.
- ONE call, runtime_started:true, finalFAIL/reruns_frozen:true. Child observations/captures do not override parent refusal.
- Live-write quiescence honored: no notes/source/other workspace writes until authoritative terminal completion. Only fixed controller owned result/native roots written while live; afterward own new question and this handoff. MAIN alone lifts other-worker quiescence.

## Pre-effect identity and command

Read T1351.1/D157 and accepted v3 checkpoint3/freeze/current source effect/diagnostic/capture paths. Finalized pins55070971bytes, SHA256**90acb0962ede34f68a56dbe874bdefa41d5a34107fe61c3d59418e9b81995027**,1353consumed inputs; preservation163575files/47167dirs/9695opaque links/14specials/threeabsences. Exact nine current source hashes matched accepted D156/checkpoint3 AND pins; accepted freeze**2a4827ed1b471598be4872c6f20cc3b61d0fe2a0ab11dfc2a9ae9549c41ce149** matched. Exact two destinations absent. Original .git mode-only boundary is the accepted fixed D152 boundary; no administrative content attestation or arbitrary exclusion.

Original cwd /Users/jd1/code/apps/outbreak; PYTHONPATH/PYTHONHOME unset, PYTHONNOUSERSITE=1; fixed Python3.11.9 -B, other environment inherited:

```sh
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B /Users/jd1/code/apps/outbreak/web/runtime/pair-smoke-v3/run.py --pins /Users/jd1/code/apps/outbreak/notes/decisions/D157-candidate-pair-runtime-pins.json --pins-sha256 90acb0962ede34f68a56dbe874bdefa41d5a34107fe61c3d59418e9b81995027
```

Normal platform approval granted for this exact supervisor/command; no rejected-action workaround/default-permission/alternate launch. Reused reviewed stdlib supervisor behavior only: one new-session child, stdinDEVNULL, captured stdout/stderr, <=600s whole CLI and combined8388608bytes,590s observation/work deadline plus<=10s owned-child cleanup reserve. Controller original180s effect deadline/owned cleanup unchanged. Supervisor no workspace writes.

Session48033 retained/polled to authoritative exit1; elapsed**195.36321654205676s**; child_reaped:true,fault:null,supervisor_signals:[];112stdoutbytes/0stderrbytes, no timeout/overflow/fallback. Exact stdout:

```json
{"P0":false,"authority":false,"reruns_frozen":true,"runtime_started":true,"status":"FAIL"}
```

StdoutSHA036316a11af9f95d5584e595a109e561481261d32258a5d55705d55711c03a79; empty stderrSHAe3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855. No second controller/gate/admission/probe/build/repair call. No restarting after observation waits.

## Actual observations and rejection layers

Pure pre-effect gates passed sufficiently to enter actual fixed runtime. Native/Node/two isolated Chrome instances/local gateway/static/inspectors and ordinary canvas actions actually ran; original admitted D121 builds/source/root unchanged. Loaded-private-image record identifies exact admitted SDL2/hidapi paths; system_image_bytes NOT ATTESTED.

Observer statusOBSERVATIONS_COMPLETE,errors[],sample_faults{},two active clients,two moves,two real captures,evidence_complete:true, elapsed6135.686167ms. Parent report statusFAIL/errors["timely native spawn ACK"],evidence_validated:false,proof absent/empty,captures[]. Its recorded runtime/cleanup elapsed14868.839957984164ms. The parent gate is authoritative: the two movement rows and PNGs remain useful **unaccepted partial evidence**, not passed normal_pair/visual/gameplay proof.

Retained A active own(cn0,life1,state0); OPEN119.1ms; milestone4 ACK186.5ms life0 then236ms life1. Parent policy.py:376 requires mil[3].life==current own.life, so firstACKlife0 conflicts with currentlife1. Retained B own(cn1,life0,state0),OPEN104.4ms,ACK2370.9ms life0. Failure message is a conjunction label; no actual15s-lateness conclusion or ACK-policy amendment inferred. MAIN reviews semantics; worker ran no internal proof function.

FAIL receipt statusFAIL/errors["terminal captures required"],elapsed107995.41025003418ms,captures[],report_sha256:null,ledger_sha256:null. Parent proof failed before top-level capture refs were assigned, then terminal capture closure also refused. Both layers preserved. Existing report/ledger have independent hashes below but are NOT retroactively bound into failed receipt or resealed.

## Actual PNGs for MAIN inspection

| Client | Actual owned path | Bytes | Dimensions | SHA256 |
| --- | --- | ---: | --- | --- |
| A | /Users/jd1/code/apps/outbreak/web/transport/results/candidate-pair/runtime-D157-pair-1/view-A.png | 881575 | 1200x675 | 14e65736cf6cb905e33cc1e2b8800ec01264019a5076b7a195164dd9d45b2b0d |
| B | /Users/jd1/code/apps/outbreak/web/transport/results/candidate-pair/runtime-D157-pair-1/view-B.png | 890145 | 1200x675 | cfe9c157bd7b86d6453ed949fc1c222022223e641b5cc02284e19175d6374ae6 |

Files ordinary0600/nlink1, actual PNG signature/header dimensions read as data, hashes agree with child capture rows. Actual screenshot+retention270.486ms(A)/273.341ms(B); combined1771720bytes. Child rows retain public before/after state; no private-state injection/mockup/generated substitute/manual capture. Parent final capture validation/reference assignment did not complete; receipt captures empty. MAIN must inspect actual images before pixel/scene claims; worker has made none.

## Retained artifacts

All following relative to /Users/jd1/code/apps/outbreak/web/transport/results/candidate-pair/runtime-D157-pair-1/. Ordinary0600/nlink1 files at post-terminal inspection:

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| receipt.json | 524 | 7989efeea064c5fe226905b0383265a41bde3e38e6a506446cb8f90d2d1552bb |
| report.json | 215766 | 28255af21afdfd336744a4444b277515dfa1633bdb3ee46dbe3cd6f5379dc9b9 |
| ledger.json | 7951 | 6311c4be7f1bf788cbd89b287be70caad8ff93f2181589f46c19a86fe856fa10 |
| validated-plan.json | 57230419 | e7721207d3eaf4701ae3ad7810843fb751aa676e4ccaf2b5808a7d374cf03a69 |
| native.log | 1168 | 34ee7b83b2a177072fbfb48c117383bfcd95bca8b6b7aaf7d832a67e772b3c09 |
| stdout.log | 60189 | 71148efe3c96b4e7a1e905be2548429ae51972a66f97fb58f0867819196dbd62 |
| stderr.log | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| view-A.png | 881575 | 14e65736cf6cb905e33cc1e2b8800ec01264019a5076b7a195164dd9d45b2b0d |
| view-B.png | 890145 | cfe9c157bd7b86d6453ed949fc1c222022223e641b5cc02284e19175d6374ae6 |
| browser-ownership.json | 374 | de0b6240e5ea99ae5736c25a2a465dca84ed0c7bcb655203bfcad9c643f305c6 |

Native sandbox: /Users/jd1/code/apps/outbreak/web/server/run/candidate-pair-D157-pair-1/. No output/receipt rewrite, profile/capability/token copying or old-D147 reuse. Validated plan and ledger are metadata, not runtime authority for another call.

## Recorded cleanup and targeted post-terminal checks

Native exit0, shutdown61.38708395883441ms; kill_fallback:false; groups_reaped:true; all139inspector handles reaped. Keys released, contexts/browsers stopped, gateway/static closed; gateway close0.7354580000010174ms; handles_empty/ports_released/private_removed/ownership_complete:true. Private cleanup rows removed browser-temp-A/browser-temp-B and native private/entropy.dat. Targeted post-terminal lexists checks confirm all three absent. No live manual ps/lsof/socket cleanup probe or extra signals; facts above are retained controller records, not a separate system-wide attestation.

Finalized pins digest/size and all nine accepted checkpoint source hashes rechecked unchanged. No full historical verifier/baseline rerun, image/receipt mutation or source/policy patch. Admitted source/opaque historical leaves kept under controller's existing guards; unreadable84bytes still NOT ATTESTED.

## Stop and next boundary

Question notes/questions/T135-world-parent-proof-and-capture-refusal.md records primary ACK-life check and secondary terminal capture-reporting refusal for MAIN. Preserve entire failed attempt/receipt/report/ledger/PNGs. No waiver, retry, second run, install/rebuild/pin rewrite or manual bypass.

No accepted normal_pair/visual result, server authority, gameplay/performance/hardware/system-image/human/P0/MVP claim. Actual source run produced partial evidence only; MAIN reviews images and failure before selecting separately released work. T136 remains separately blocked and QA held; quiescence remains MAIN-controlled until announced lift. Own notes authored only after terminal.

MAIN D158 subsequently acknowledged the terminal FAIL, lifted temporary repository-write quiescence, and reported opening/hash-verifying both PNGs as unaccepted failure evidence. Engine owns T137 notes-only read-only diagnosis. World finishes this handoff and stands by; no second call, reseal, retry, implementation, or runtime is authorized. T136 remains blocked pending direct human approval; QA remains held.

