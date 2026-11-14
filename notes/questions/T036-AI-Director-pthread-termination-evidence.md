# Owned native shutdown report identifies libpthread mutex corruption

- Author / worker: AI-Director
- Ticket and revision: T036 / 1.0 RELEASED
- Phase and contract revision: BROWSER_FOUNDATION/GOVERNANCE/P0 0.5 plus D010 1.0
- Exact clause or interface affected: T036 criterion 4, real owned SIGINT shutdown
- Status: OPEN (lead resolution is recorded separately)

## Question

Please use the authoritative owned-PID termination report to scope the next native shutdown investigation/fix. No source change is requested by inference alone. This follow-up refines the earlier invalid-signature question: code signing remains a separate static dependency finding, not the observed termination classification.

## Evidence and impact

MAIN explicitly authorized read-only inspection of only the owned PID's DiagnosticReports. The matching file is `/Users/jd1/Library/Logs/DiagnosticReports/ac_server-2026-11-08-001605.ips`, PID 61970, process launch 2026-11-08 00:15:56.2989 -0500, capture 00:16:04.4879 -0500. Its application/image identity and UUIDs match this run's binary/frameworks. No other app report or broad system log was read.

Saved selected evidence: web/server/T036-termination-inspection-20261108T051556.json, including source report SHA-256, PID/time identity, exception/termination, native thread count, faulting stack and read-only code-signature results.

The report states termination namespace FOUNDATION, code 1; exception EXC_BREAKPOINT with SIGKILL; application-specific information: `BUG IN CLIENT OF LIBPTHREAD: pthread_mutex corruption: mutex owner changed in the middle of lock/unlock`. It records five native threads. Faulting thread 3 has `_pthread_mutex_corruption_abort` -> `_pthread_mutex_firstfit_unlock_slow` -> SDL2 offsets 766436 and 148880 -> `demoworkerthread(void*)` +924 -> SDL2 -> `_pthread_start`.

The supervisor sent only owned SIGINT; its watchdog/fallback did not run. This is an actual native shutdown failure, not successful cleanup merely because the ports were released. It occurred ~0.148 seconds after SIGINT, with -9 return code. Bounded process/group/port cleanup nevertheless passed.

Source correlation (not proof of the corruption's cause): server.cpp's native demo worker loops indefinitely and calls sem_demoworkerthread.timedwait(500); tools.cpp forwards that to SDL_SemWaitTimeout, and the native semaphore destructor calls SDL_DestroySemaphore. SIGINT quitproc calls exit; cleanupserver destroys host/stops service/exits logging but has no worker-stop/join sequence. Concurrent teardown is a plausible investigation target, not an implemented or proven root-cause fix.

Read-only codesign verifies the accepted release executable but fails the unchanged arm64 SDL2 and nested hidapi signatures. The OS termination report does **not** classify this as CODESIGNING, so do not attribute this run's termination to the signature result. No library was re-signed, replaced or executed separately.

## Options for owner and lead

Release a narrowly owned native worker/shutdown investigation against this precise stack and cleanup path, with a bounded reproduction contract, then freeze source/binary inputs for a new startup attempt. Treat framework signing/integrity separately if a native dependency repair is needed. Do not turn workers/semaphores into successful no-ops, omit real server behavior or mark graceful shutdown passed.

## Work paused

Further T036 server launches and all source/dependency repairs remain paused. The original failed run is immutable; handoff will preserve actual successful map/bind observations and failed graceful shutdown, with missing packet/client evidence NOT RUN.
