# T051 actual standalone lifecycle verification

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket: T051 revision2.4 RELEASED; D030 runtime2.4; D010/D020 exact runtime controls; governing browser foundation/GOVERNANCE/P0 revision0.5. Re-read T051/D030 before submission. Lead alone changes authoritative status.
- Base commit: 13f0d8eea4822dee5c976661218d022be74342e3; pre-existing shared edits preserved. No source/header/framework/build/client/transport/QA/asset changes, branch changes, commits, pushes or dispatch.
- New files only: `web/server/startup_lifecycle.py`, `web/server/T051-*` reports, three isolated `web/server/run/T051-*` trees (one preflight-only, two actual cases), this handoff.

## Acceptance evidence

**PASS — actual accepted release and debug server startup and clean shutdown.** Exactly one release child launched, then one debug child only after release passed and its group/ports were verified released. No further actual launches or retries. Both used genuine accepted T045 standalone executables and unchanged accepted signed dependency copies, with actual code-signature verification before each launch and loaded-copy path/hash evidence while running.

| Case | PID = PGID | Observation | SIGINT to exit | Exit | Child lifetime | Supervisor |
|---|---:|---:|---:|---:|---:|---:|
| release | 75252 | 6.6098s | 0.002309s | 0 | 6.6121s | 7.0236s |
| debug | 75419 | 6.6258s | 0.002571s | 0 | 6.6283s | 7.1245s |

Each actual case recorded 42 owned socket samples, 41 with exactly the three intended UDP targets `127.0.0.1:29863`, `127.0.0.1:29864`, `127.0.0.1:28762`; no other target appeared in samples. Both observed six native threads, real dedicated startup, successful original-map reading and registration of one servermap. Copied SDL2 and nested hidapi were actually loaded; no original SDL framework was loaded. This is real native runtime evidence, not a helper or simulated server.

**PASS — owned shutdown and cleanup.** Owned SIGINT was sent after observation. Both real children returned0 within3s; neither watchdog nor kill fallback ran, no crash exit occurred. Child was reaped, owned process group absent, lsof found no remaining owned PID handles or target-port sockets, and all three temporary bind probes succeeded after each run. The accepted main path invokes cleanup before returning and again through main/atexit; this configured normal path exited cleanly with its repeated-cleanup guards. T045's instrumented idempotence fixtures remain separate evidence; runtime did not add internal join instrumentation.

**PASS — exact bounded input/file/process controls.** Fixed argv/config/maprot bytes match D010; no additional arguments, client, master, key, account, include, syslog or production service. Binary, actual compile-dependency and SDK input hashes were checked; accepted inputs matched again after both cases. Original map/config/notices were checked against accepted manifest before staging and copies verified afterward. Each child ran from its own fresh owned tree, stdin /dev/null, minimal PATH/LANG/LC_ALL environment, combined stdout/stderr via stdlib PTY, bounded8MiB. Observation<=8s, SIGINT grace<=3s, hard child watchdog14s and supervisor<=30s were enforced. No staged file was modified. New release files were owned map-rotation/readmaps logs, observer PTY log and `private/entropy.dat`; debug additionally generated `logs/docs/serverparameters.cfg` inside its own tree. Per-file sizes/hashes and before/after snapshots are in each report. No resulting file/script was executed.

**PASS — current/preserved identities.** `web/server/T051-final-verification.json` reports two passing actual cases, no accepted-input/source mismatch and no change to the old native outputs/dependency copies/T039/T043 evidence checked against T045's preservation manifest. Current source/header hashes remain exactly the T045 accepted identities; browser snapshot boundaries stay stable. Historical T036/T043 failures and T045 evidence were not rewritten.

**NOT RUN — packet-level zero-egress, clients, browser transport, multiplayer, authority, P0/MVP.** Socket samples and disabled-service source/config do not prove absence of transient traffic. No privileged capture or new dependency was used. No client connected or was simulated. This startup-only test does not exercise load, nonempty active demo/vita/auth work, worker-origin fatal handling or forced thread-creation failure; T045 limitations remain in force.

## Supervisor and preflight disclosure

The first invocation in the restricted filesystem/network sandbox stopped during preliminary loopback bind probes with EPERM on all three ports, **before any child process launched**. Its immutable report retains the initial inaccurate summary “occupied port”; the recorded exact errors are `[Errno 1] Operation not permitted`, so it is not evidence of a port occupant or native runtime failure. Read-only lsof found no target-port sockets.

The supervisor was corrected to distinguish refused/unavailable probes in the summary and to preserve permission-denied preflights without consuming the first actual launch. It still rejects a mode with any prior actual PID, any other preflight failure without review, and debug without exactly one clean release. The inspected unchanged bounded commands were then authorized through the execution approval mechanism with sandbox escalation; this changes execution permission, not server argv, library inputs or runtime controls. All three reports/trees are preserved. There were exactly two actual server launches, not three. No automatic approval rejection occurred.

Commands, from repository root (already executed; **do not rerun**):

```text
python3 web/server/startup_lifecycle.py release
python3 web/server/startup_lifecycle.py debug
```

The first command also has the preserved preflight-only invocation described above. Each actual invocation used reviewed `require_escalated` permission because the normal sandbox prohibits local UDP bind. Supervisor SHA256: `1256df2df4f15a07a9b676a1fb07715104bb1bbd8bc89499eef0faa2e3cd743d`. Full exact argv/tool commands/environment/codesign output/source dependencies/loaded files/threads/socket samples/capture/cleanup/files are in the per-case JSON.

Host/tool evidence: arm64 Darwin25.5.0, macOS26.5.1 build25F80; Python3.11.9 at `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3`; Nodev24.13.0 at `/Users/jd1/.nvm/versions/node/v24.13.0/bin/node` recorded for identity only (server/supervisor do not use Node); installed lsof4.91. No tool install or OS trust/account change.

## Stable evidence identities

Candidate executable SHA256 (unchanged):

- `web/server/out-lifecycle/release/ac_server`: `49a1d28a6251213e27464afb36b6d974215c9886045a38d00a9cfe66befb096a`
- `web/server/out-lifecycle/debug/ac_server`: `df4728a98c5fa1ebc03de88a8549e6dba05a25c4c04310673ded3ba009fa1995`
- Copied SDL2: `5faae862816a57f36e11164dfbf5500021a2fbe65a0b23297c9697738c1c9767`; copied nested hidapi: `62e00aa847d78ed4d1f6188ade82c0b271b73c2278c6bac9b08056eb036e8de0`.

Reports:

- `web/server/T051-20261108T060101-484f0948-release.json`: `a53329fe17c91d66221900ab92d94f9c797fa21d562411ac9883a199039f8f5f`
- `web/server/T051-20261108T060122-00aa9f9b-debug.json`: `e2b3af94a3265c10e85c122927ede78d331783cc249e03bd2281f67be8c353b4`
- Preflight-only `web/server/T051-20261108T060016-7803c93d-release.json`: `6423a1c5ca9233c60454b7380ac55044f1bcb78421a25799a88f8df2b95489c7`
- `web/server/T051-final-verification.json`: `7d70c3526dffa166b3ed322a69a62140b855276bbc35d61eb193038bd8187717`

Run trees use the matching report stems under `web/server/run/`. Full exact current source/header hashes appear in final-verification. Evidence is ready for MAIN review; no further launch is authorized by this completed two-case allowance.
