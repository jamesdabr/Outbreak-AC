# T036 actual native startup — partial handoff

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket: T036 revision 1.0 RELEASED; no authoritative status changed
- Governing context: AGENTS; BROWSER_FOUNDATION/GOVERNANCE/P0 0.5 and approved D010 runtime addendum 1.0; accepted T033 real binary and T027 original map
- Changed files: new web/server/startup_smoke.py; web/server/T036-20261108T051556-89f4ee4b.json; new web/server/run/T036-20261108T051556-89f4ee4b/** staged/runtime files; supplemental web/server/T036-termination-inspection-20261108T051556.json; own new T036 questions and this handoff only. No source/build artifact/accepted map/framework/config/contract/other-worker file was modified.
- Commits/push/dispatch: none. One real server was launched; no client was connected and no fixture substituted.

## Actual outcome

The accepted real arm64 release server loaded the repository SDL2 framework, read the accepted original map successfully, and exposed only the three approved loopback UDP sockets in all socket-bearing observations. It did **not** shut down gracefully after owned SIGINT: the child returned -9. The OS report for this exact PID identifies libpthread mutex corruption through SDL2 and demoworkerthread. Process group and ports were released within the time bounds. This is a failed graceful shutdown, not a runtime acceptance pass.

Original run evidence is immutable: web/server/T036-20261108T051556-89f4ee4b.json, SHA-256 `d5fe52afdcf9a163803747f443e5f76b2278851bdfec4141c8035a25b3698c4a`, plus its original run tree. No second server run occurred. Later inspection and supervisor preflight improvements do not overwrite or promote this failed run.

## Acceptance evidence

| Criterion | Result | Evidence and limits |
| --- | --- | --- |
| 1 bounded inspected supervisor/exact pins/config/argv/ports | PASS for executed scope | Supervisor was read before execution. Exact D010 binary, map/manifest, framework bytes and actual consumed source/header/SDK dependency hashes verified. Exact config bytes and argv, no inherited config/keys/master/include/service args; fresh non-symlink tree and owned port probes; no occupied ports. Bound output, new process group and 14-second kill watchdog. |
| 2 actual loader/startup/map/native behavior | PARTIAL | One real native process, loader/startup proven by actual UDP host/info sockets and native map read; OS report records five threads. Native map reader reports v10/sfactor6/rev1/nine entities/534-byte cgz. Console stdout/stderr remain empty, so expected startup/added-servermap console messages cannot be claimed. No real client/gameplay test. |
| 3 actual loopback binds and honest observation limits | PASS sampled binds; packet evidence NOT RUN | 51 lsof samples; first three empty during loader startup, remaining 48 contain exactly UDP 127.0.0.1:29863,29864,28762. No unexpected bound address/remote target was observed. lsof cannot rule out transient DNS/egress. /dev/bpf devices are root-only; no elevated packet capture or installation was attempted. |
| 4 owned shutdown/process/group/ports/files | FAIL graceful shutdown; PASS bounded cleanup/file accounting | Owned SIGINT at ~8.046s; -9 return after ~0.148s, lifetime ~8.194s. Neither supervisor watchdog nor SIGKILL fallback ran. Group gone and all three temporary UDP bind probes succeed; final lsof lists no target-port sockets. Five new files accounted; staged files unchanged. |
| 5 identities/tools/timing/diagnostics/failure record | PASS evidence; runtime failure remains | Original report stores exact argv/environment, accepted input hashes, tool versions, file hashes, socket samples, PID/group and timing. Supplement records exact owned-PID OS diagnostic, stack and read-only signature checks. Concrete failures raised in own questions, no source/map repair. |
| 6 immutable honest handoff | PASS documentation | Actual runtime versus source inference and missing packet/client evidence are distinct below. No T014/T015/P0/browser multiplayer/MVP acceptance is asserted. |

## Commands and frozen identities

Executed from repository root after source/supervisor inspection:

```sh
python3 web/server/startup_smoke.py
```

The exact same-project loopback runtime and process inspection were run via scoped sandbox approval because ordinary sandbox ps inspection had been denied. Approval succeeded; no packet-capture escalation, install or broad service permission was used. Supervisor exited 1, honestly reporting actual_runtime_pass=false.

Accepted binary SHA-256 `296601782e7ff1510b5c9900548bad34c28c97a73d9d571b4d5037c88a9e6005`. Accepted manifest SHA-256 `1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3`; map SHA-256 `c3f0226abdf143474804d9259428eb9ba641b3ac259251bdafef04962d5cb52d`; cfg SHA-256 `751937b8c2d1082281643895be6ffbe2c4de22f072012601bbd01361ce0e37de`. Original SDL2/hidapi hashes remain T033's accepted values, unchanged after run. Full input identities are in the original JSON, including compiler dependency hashes checked before process execution.

Child PID=PGID 61970, new session, stdin /dev/null. Exact D010 argument array uses -i127.0.0.1/-f29863/-c1/-LS5/-LF5 plus its exact isolated config/log/demo/vita paths and -Z0. Environment contains only PATH=/usr/bin:/bin:/usr/sbin:/sbin, LANG=C, LC_ALL=C. No shell, inherited DYLD, account/key/master arguments or system service. Exact parameter and rotation bytes are staged and hashed in the report. Cwd is the fresh run tree. Only accepted map/cfg/notices and original empty config data were staged.

Tool identity: native lsof 4.91, installed /usr/sbin/lsof; Python 3.11 identity in report; Darwin/macOS identity is pinned in accepted T033 and runtime uname output. Native loader dependency observation came from owned-PID lsof: actual accepted SDL2 path mapped, not a fake server. The exact-PID diagnostic further records arm64 SDL2 2.0.14 and nested hidapi images with their UUIDs.

Elapsed supervisor 8.526s, child lifetime 8.194s: both satisfy <=30s supervisor/<=15s child bounds. No unrelated process was signalled or port owner killed. SIGINT was sent only to owned group 61970. Post-reap group probe failed with ProcessLookupError, and all ports were free. No further live process remains from this run.

## Actual map, files and native threads

`logs/readmaps_log.txt` records zero official maps, one servermap, zero incoming maps, then:

```text
read map 'packages/maps/servermaps/dev_outbreak_browser': cgz 534 bytes, cfg 1622 bytes (883 gz), version 10, size 6, rev 1, ents 9, x 6:57, y 6:57, z 0:12, layout 59 bytes, spawns 1:1:2, flags 0:0
```

This proves the native map reader's success, not client rendering/collision/movement or an active multiplayer round. `logs/debug/maprot_debug_verbose.txt` contains the exact staged two-minute DM rotation values; no accepted map/config was patched to get that result. The two-minute value is only D010 smoke data, not MVP match rules.

Eleven staged files became sixteen final files; no staged file was modified. New files:

| File | Bytes |
| --- | ---: |
| logs/readmaps_log.txt | 320 |
| logs/debug/maprot_debug_verbose.txt | 958 |
| private/entropy.dat | 4096 |
| observer-stdout.log | 0 |
| observer-stderr.log | 0 |

All hashes and staged/final metadata are in the immutable run JSON. Native map/rotation and entropy files are real server writes; two observer logs are supervisor output. No vita/account/demo/host-profile file was produced. Source correlation: vita initialization/persistence calls entropy_save, explaining the relative private/entropy.dat write inside the isolated cwd. No secret/profile data was imported.

The live ps -M snapshot was early (~0.3s), before sockets appeared, and showed one thread; do not describe it as proof of all workers. The later owned-PID OS diagnostic authoritatively records five native threads and the faulting demo worker. Native worker existence is observed; healthy complete worker lifecycle is not established.

## Shutdown diagnostic and source inference

Per MAIN's explicit follow-up, read only matching ac_server DiagnosticReports and then the exact report whose PID is 61970: /Users/jd1/Library/Logs/DiagnosticReports/ac_server-2026-11-08-001605.ips. No unrelated app report or broad system log sweep was read. Selected evidence and source-report SHA are saved in web/server/T036-termination-inspection-20261108T051556.json.

Identity: process launch 2026-11-08 00:15:56.2989 -0500, capture 00:16:04.4879 -0500. Termination namespace FOUNDATION/code1, exception EXC_BREAKPOINT/signal SIGKILL. Application-specific message: `BUG IN CLIENT OF LIBPTHREAD: pthread_mutex corruption: mutex owner changed in the middle of lock/unlock`. Faulting stack: `_pthread_mutex_corruption_abort` -> `_pthread_mutex_firstfit_unlock_slow` -> SDL2 -> `demoworkerthread(void*)` +924 -> SDL2 -> pthread start.

This is authoritative classification of the observed failure, not proof of which source operation corrupted the mutex. Source correlation only: native demo worker indefinitely timed-waits on sem_demoworkerthread; native tools wrappers call SDL_SemWaitTimeout/SDL_DestroySemaphore; SIGINT quitproc calls exit; cleanupserver lacks a worker stop/join sequence. Concurrent static teardown is a plausible investigation target, **not** an implemented/proven fix.

Read-only `/usr/bin/codesign --verify --verbose=4` succeeds for accepted release executable and fails unchanged arm64 SDL2 and nested hidapi. These exact hashes/results are in the supplement. Signature defects are concrete separate findings; OS termination is FOUNDATION/libpthread, **not** CODESIGNING. Do not infer that re-signing fixes the mutex failure.

Two own questions preserve this progression: T036-AI-Director-invalid-sdl-signature-shutdown.md, followed by T036-AI-Director-pthread-termination-evidence.md with the authoritative report. No source/library/map fix was attempted.

## Supervisor updates and limitations

After the failed run, the allowed new supervisor was strengthened to reject invalid input code signatures before any next launch, sample native threads/loaded files only after the three sockets appear, and explicitly record nonzero child exit as an error. Those post-run changes were inspected but **not executed**; they do not retroactively alter the original run or its errors array. Current supervisor SHA-256 `1e1d2eb81e1308ac6433b0d9ff85990569d1856886be2d9619b450b6644b4a91` refers to the final post-run file, not a claim that these later checks ran in the original attempt.

Packet capture/zero transient DNS/master/syslog egress: NOT RUN. No suitable unprivileged capture was available; root-only BPF access was not requested. Sampled sockets and source-disabled registration/syslog do not prove absence of transient traffic. Client connect/protocol/gameplay/browser/multiplayer: NOT RUN by this ticket.

## Integration and next scope

T036 remains partial due graceful shutdown/native dependency findings. All original T033/T027/source/framework/run evidence remains untouched. T039 is separately released to repair **copies** of the known-invalid frameworks and build new artifacts; that new work begins only after this immutable T036 handoff and does not waive the pthread failure or authorize another startup. MAIN alone pins/reviews future runtime inputs and changes ticket status.
