# T146 deadline correction — checkpoint2

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket/contract: unchanged T1461.0 RELEASED preparation / D173, NATIVE_RSS_CALIBRATION0.1. MAIN returned checkpoint1 for cleanup/await deadline handling.
- State: REVIEW-READY, NOT FROZEN; no actual effect or acceptance authorized.
- Changed: own reaper.py, calibrate.py, test_reaper.py, SCHEMA.md; new owned preparation evidence and this handoff. Prior checkpoints/logs/results/handoff preserved. child.py/README unchanged; no other source/controller/SDK/Git changes.

## Correction

PASS — await_terminal checks deadline BEFORE initiating a new wait4; already captured terminal history remains readable after expiry without an OS call. signal_if_unreaped now requires an absolute deadline, checks before its live poll and rechecks immediately before kill. Cleanup checks before initial uncached poll/TERM, passes the unchanged whole deadline into signals/waits, and checks again before any KILL path.

Expired uncached ownership stays unreaped/returncode:null, error CLEANUP_DEADLINE_UNREAPED; no guessed status or late signal/reap. Descriptors always close in finally. Expiry after TERM preserves term_sent:true while kill_sent/fallback stay false. A skipped KILL is not reported as fallback; an actually sent KILL still marks failure. ECHILD/nondeadline errors retain unproved ownership, without trying a fallback merely because they are RuntimeErrors. Sole exact-child/cache semantics unchanged.

Schema documents the mandatory deadline signal signature, cached-only access after expiry, exact failure code and descriptor/fallback behavior. Earlier checkpoint1 deadline description is superseded by this correction only; unit/ABI/budget/Chrome scope and all other preparation behavior remain as in handoff1.

## Guarded verification

PASS — inspected edits/fixtures, then only:

```text
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/qa/memory/T146/test_reaper.py
```

37tests/0failures/0errors; actual_effect_attempts[]. Original33 cases retained/adapted to the mandatory signal deadline. New34–37 exercise:

- Already expired cleanup: zero wait4/kill calls, both descriptors closed, truthful unreaped/error/null status.
- Expired await/signal: zero initial wait/signal; expiry between live poll and signal causes no kill.
- Expiry after TERM: no KILL/fallback, unresolved ownership preserved, descriptor closed.
- Cached terminal after expiry: no further OS wait/signal, cached status/cleanup retained.

All real process/spawn/exec/wait/kill/ctypes-library/Mach/mmap/socket/host queries/helper clocks remain audit/patch/import denied before project imports. Mocks only; actual_process/actual_wait4/actual_mach:false, units_confirmed:false, budget NOT_EVALUATED, Chrome NOT_OBSERVED, P0:false. run-1 remains absent. No child/process launch, actual calibration, integration, compiler/probe/API/system/process audit or old suite execution occurred.

## Immutable checkpoint identities

Paths beneath web/qa/memory/T146/preparation-1:

| Record | Bytes | SHA256 |
| --- | ---: | --- |
| review-ready-2.json | 8119 | 1a9811e613d6ce586f78c49f368dc777922d463b37afbc16cb48ac9a3ba325c1 |
| fixture-result-6.json | 848 | 8042f14b768e947a55cd0f5664b127544e54c28d94bb312bb50b6d13264e5590 |
| source-diff-2.patch | 64474 | d9b7e40f7704b14af010e70f16a9b28ca06241ccbd5af2d49a9b241b9cb1ed4f |

Checkpoint2 binds latest exact six hashes, refreshed governing references, retained original checkpoint identity, SDK declarations and owned evidence. Authored with builtin metadata/hash/diff/JSON only, writes restricted to two exact new records; no project imports/reruns during authoring.

| Source | SHA256 |
| --- | --- |
| reaper.py | f42ddfa1a243d1da685f8d740fd1e22c3a82f4e6047c46239e17a80e76b949ba |
| calibrate.py | 88faf4d9a4f1da22e757175c4738917a823ccdeb36c3eee76aef64dd123734d9 |
| child.py | 74c826213dcfb13d65a94741808f3447192591961f7c2a888e6d394863c615cb |
| test_reaper.py | 662ceb0162a0f8aa29ea276f8cab09ce05c89e959d7bfc935aac54083c8bd37a |
| SCHEMA.md | 624b146bc7f567223eaa880b6773f74e7d6f4228cc05cd74fd408a57b98360a6 |
| README.md | 960c66c6783a04f122d5ac7c5b55bd23813b4e9d569400b2c3cc989e09b72db5 |

Ticket/contract reread unchanged. Await MAIN review and explicit freeze clearance; no freeze or new effects. Future actual caller/owner approval and unit review remain separate. QA paused; other worker ownership untouched. Engine returns to standby.
