# Proposed native stop/wake/join lifecycle after signed-copy shutdown failure

- Author / worker: AI-Director
- Ticket/revision: T043 / 1.7 RELEASED
- Governing scope: browser foundation/GOVERNANCE/P0 0.5 plus D020 1.7
- Exact clause: T043/D020 failure follow-up: one source-backed lifecycle proposal, no source implementation or retries
- Status: OPEN (lead resolution/implementation release recorded separately)

## Question

Please release a narrowly owned native worker-lifecycle fix and new pinned build/runtime checks. Both actual runs load/read/bind successfully but fail after SIGINT; the new signed-copy report directly observes main-thread semaphore destruction concurrent with a worker fault. No source or library patch is implemented by T043.

## Measured evidence

New real run: web/server/T043-20261108T053231-e8b01b6f.json. PID/PGID 67908; accepted signed release 14233cc7302d9c1f5e45aa5948a30d224d8f56a08ed3ffc6b0f314c6dd2964a9. Both copied SDL2/hidapi hashes/codesign checks pass and owned-PID lsof proves those copied paths actually loaded. Exact D010 config/map/argv/ports are unchanged apart from approved binary substitution; combined PTY capture is diagnostic only.

Actual startup/map read/added-one-map logs pass; 43 socket samples, 41 socket-bearing, show only three approved loopback UDP addresses. After 6.650s observation, owned SIGINT gives -11 within 0.1355s, with no supervisor SIGKILL fallback/watchdog. Group and all three ports are gone/free.

Exact own-PID diagnostic `/Users/jd1/Library/Logs/DiagnosticReports/ac_server-2026-11-08-003239.ips` matches PID67908, launch 00:32:32.1474 -0500 and capture 00:32:38.9325 -0500. Its exact bytes/hash and selected six-thread stacks are preserved in web/server/T043-termination-inspection-20261108T053231.json. Exception EXC_BAD_ACCESS/SIGSEGV, invalid address0x5; termination SIGNAL11. Main thread: SDL2 -> sl_semaphore::~sl_semaphore()+24 -> exit -> quitproc(int)+16 -> enet_socket_wait. Faulting thread: pthread_mutex_unlock -> SDL2 -> demoworkerthread(void*)+924 -> SDL2/pthread start. Other workers remain in SDL semaphore waits.

This is direct evidence of concurrent exit/semaphore teardown and live worker access. The stack alone does not identify which semaphore instance main is destroying or every corruption mechanism. It does establish a precise lifecycle target. Signing did not make this startup/shutdown comparison pass, and the changed signal from T036's FOUNDATION/pthread corruption (-9) to SIGSEGV (-11) must not be relabeled a fix.

## Relevant current source

- server.cpp::quitproc invokes exit directly from SIGINT/SIGTERM handling; initserver(true) registers cleanupserver/ENet atexit and enters `for(;;) serverslice(5)`.
- server.cpp::cleanupserver destroys the ENet host/stops service/exits logging, but contains no native worker stop/wake/join.
- initserver discards returned map/config/demo worker handles. polldeferredprocessing retains the auth worker handle only in a function-local static; log.cpp::initlogging similarly hides its logger handle in a local static.
- server.cpp::demoworkerthread loops forever and timedwaits on static sem_demoworkerthread even when demo_save=0. Deferred auth worker also loops forever on servinfoauth_deferred.
- serverfiles.h::readmapsthread/readserverconfigsthread have unbounded outer loops and semaphore waits. updateservermap additionally waits while servermapdropbox is occupied, needing main-thread acknowledgement.
- log.cpp::logworkerthread waits on mainlogsem forever. tlog/xlog producers can block on threadlogfullsem; poll_logbuffers is what transfers threadlog into mainlog. exitlogging currently disables/clears sinks without joining its consumer.
- tools.cpp native sl_semaphore destructor calls SDL_DestroySemaphore; native sl_waitthread already provides real SDL_WaitThread and wrapper deletion. No global successful thread/semaphore shim is appropriate.

## One proposed fix boundary for MAIN to freeze

Proposed ownership only, not dispatch: native lifecycle in server.cpp and its included serverfiles.h plus logger lifecycle in log.cpp; a narrow declaration in protos.h only if MAIN freezes the cross-TU logger shutdown interface. Existing tools thread primitives can be reused; if their completion visibility must change, tools.cpp requires an explicit additional allowlist. No protocol/transport/gameplay change, SDL replacement or browser-thread emulation is proposed.

1. Make native signal handlers record only a sig_atomic_t shutdown request/desired status. Consume it from normal standalone main/server-loop context; do not run exit, destructors, SDL locks or logging inside the signal handler. Preserve the lead-approved signal exit-code policy. End the update loop without accepting/submitting new work.
2. Retain owned handles for all five started worker kinds: map reader, config/vita reader, demo, deferred auth and logger. Represent stop/completion state with real thread-safe synchronization (e.g. C++11 atomics, not an unsynchronized new volatile bool). Preserve never-started and partial-startup cleanup cases.
3. Before any host/game/config/semaphore/static destruction, request map/config/demo/auth stop and wake their specific semaphores. Add stop checks after wake and in nested wait loops, especially updateservermap's occupied-dropbox loop. A worker must not publish new ownership after shutdown. Define cleanup of unpublished versus already-published map objects and staged/completed auth jobs without fabricating success, touching reused clients or double-deleting. Preserve existing active demo/vita cleanup policy; demo_save=0 must not merely hide a still-running worker.
4. Keep the logger available while nonlogger producers finish. Avoid a deadlock where main joins a worker blocked on a full threadlog queue: continue the existing main-thread log transfer/wake work while collecting real producer completion, then perform each real join exactly once. Do not poll a made-up successful thread handle or destroy semaphores to force wakeups.
5. Once producers are joined, drain remaining log transfer/consumer data, request logger stop, wake mainlogsem, join the logger, and only then close logging sinks. Log consumer must be able to exit when stopped and empty. Late producers and partial startup require explicit behavior, not silent use of a closed sink.
6. Finish host/service/data cleanup and allow normal process exit/static destructors only after worker joins. Make cleanup idempotent so normal return plus existing atexit/fatal paths cannot double-join/double-free. Limit the initial fix to normal requested native shutdown and defined main-context cleanup; a worker-thread fatal/self-join path needs explicit handling, not guesswork. Preserve browser non-STANDALONE single-thread behavior and native-client local protocol behavior.

No new public helper names or architecture are frozen by this note. MAIN must set the exact file/API ownership and cancellation/logging policy in the implementation ticket before code changes.

## Proposed validation for that future release

- Real native release/debug builds and all relevant header consumers against accepted signed dependency copies, current source/header/object hashes, no stale artifact reuse.
- Controlled lifecycle fixtures for never-started/partial startup/idempotent cleanup, worker waiting/stop/wake/real join, map dropbox handoff cancellation, auth queue ownership and logger full-queue shutdown. A helper/fixture pass is not actual server shutdown evidence.
- A separately released single bounded real startup on the same approved loopback/argv/map/config pins: capture real workers/logs/binds; SIGINT must exit0 within3s without fallback, no live owned group/ports, no crash diagnostic. SIGTERM and busy-work scenarios need explicit follow-up scope, not speculative runtime loops.
- Preserve server functionality: no disabled workers disguised as success, no skipped authoritative validation, no changed wire messages, no public services/global dependencies. Confirm native/client/browser regression boundaries as appropriate to the approved source scope.

## Work paused

No source edits, re-signing, rebuild or additional server run is authorized/performed by T043. The single failed signed-copy run and old T036 evidence remain immutable. Packet capture/client/gameplay evidence remains NOT RUN. Independent handoff/preservation work is complete; MAIN decides and releases the lifecycle repair.
