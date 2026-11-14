# T043 signed-copy startup comparison — graceful shutdown failed

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket/revision: T043 / 1.7 RELEASED; no status change by worker
- Governing documents: AGENTS; browser foundation/GOVERNANCE/P0 0.5; D010 controls and approved D020 runtime addendum1.7; accepted T039 binary/copy hashes and T027 map
- Changed files: NEW web/server/startup_signed.py; web/server/T043-20261108T053231-e8b01b6f.json; web/server/run/T043-20261108T053231-e8b01b6f/**; web/server/T043-termination-inspection-20261108T053231.json; own T043 lifecycle question/proposal and this handoff. No existing source, driver, framework, binary, prior run/evidence, asset, config, contract or other worker file was changed.
- Source/commit/push/dispatch: none. One real signed-copy server run only; no retries/source fix/client connection.

## Actual outcome

The accepted signed-copy release server passes signature/input preflight, actually loads both copied libraries, reports native startup, reads/registers the original map and exposes only approved loopback UDP sockets in observations. The real owned SIGINT shutdown **still fails**, now with SIGSEGV(-11), not a graceful exit0. The process/group/ports are released without supervisor kill fallback. This is not a native runtime acceptance pass or proof that signing fixed T036.

Immutable run report: web/server/T043-20261108T053231-e8b01b6f.json, SHA-256 `0fe224a71542f1c98e3bd4928b0e56cd2e5033a704122ce81c148ae58a4a6d9a`.

## Acceptance evidence

| T043 acceptance clause | Result | Actual evidence / limits |
| --- | --- | --- |
| Inspected bounded supervisor; exact accepted binary/framework/map/config pins | PASS | New supervisor inspected before execution; SHA recorded below and in run JSON. Actual codesign checks pass for signed release/SDL2/hidapi code. Current consumed source/header/SDK dependencies match accepted T039 records. Binary, framework, manifest/map/cfg/notices and exact D010 config/argv all pinned. |
| Actual bounded signed-copy process and real startup/map/threads | PASS observations | PID67908, fresh cwd/session/group; combined PTY logs report dedicated startup, one added servermap and rotation entry. Native map reader succeeds on v10/size6/rev1/nine entities. Live ps and owned OS report both show six native threads. Not a fixture or static source result. |
| Actual loaded copied dependencies and loopback-only sampled binds | PASS samples/identity | 43 samples, first two empty during startup and 41 showing exactly UDP127.0.0.1:29863,29864,28762. Owned-PID loaded-file observation records both exact copied framework paths/hashes, no original framework path. No wildcard/public/extra target observed. Packet capture remains NOT RUN. |
| SIGINT<=3s graceful exit / owned cleanup | FAIL graceful exit; PASS bounds/cleanup | SIGINT after6.650s, return-11 in0.1355s, lifetime6.786s; no fallback/watchdog. Supervisor7.142s. Group gone, all three bind probes available and final lsof empty. Crash is not accepted because cleanup succeeded. |
| Sandbox writes and immutable failure/owned diagnostic | PASS evidence | Eleven staged files unchanged; four new files fully hashed. Exact own-PID OS report preserved byte-for-byte in supplemental base64 plus source SHA/identity/stack. Prior artifacts/frameworks remain unchanged. |
| Compare T036; precise lifecycle proposal; no repairs/retries or widened claims | PASS proposal/reporting | Comparison below; source-backed question T043-AI-Director-native-worker-lifecycle.md. No source/library change/rebuild/second run. Client/traffic/gameplay/browser/MVP evidence NOT RUN. |

## Exact execution, inputs and capture

After reading T043/D020/D010/T036/T039 and the new supervisor:

```sh
python3 web/server/startup_signed.py
```

Executed through scoped sandbox approval for the exact owned loopback process/inspection, as required by earlier sandbox restrictions on native process observation. Approval succeeded. No packet capture escalation, dependencies/install, account/keychain/global security change or external endpoint was used. Supervisor exit1 honestly records actual_runtime_pass=false.

Supervisor SHA-256 `3636adad53e9b9fcbfdfdf4a9d7a37661ada65a8a5751dcd6d7667566d85cb1e`. The file remains unchanged after this run. Existing startup_smoke.py is unchanged. No configurable service arguments are accepted; every service argument is literal approved D010 data.

| Accepted input | SHA-256 |
| --- | --- |
| out-signed/release/ac_server | 14233cc7302d9c1f5e45aa5948a30d224d8f56a08ed3ffc6b0f314c6dd2964a9 |
| deps-signed/SDL2.framework/Versions/A/SDL2 | 5faae862816a57f36e11164dfbf5500021a2fbe65a0b23297c9697738c1c9767 |
| copied nested hidapi code | 62e00aa847d78ed4d1f6188ade82c0b271b73c2278c6bac9b08056eb036e8de0 |
| original manifest | 1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3 |
| original dev_outbreak_browser.cgz | c3f0226abdf143474804d9259428eb9ba641b3ac259251bdafef04962d5cb52d |
| original map cfg | 751937b8c2d1082281643895be6ffbe2c4de22f072012601bbd01361ce0e37de |

Exact original sandbox config bytes, map/notice copies and source/header/framework/tool hashes are in the run JSON. Parameter file is exactly D010's four lines (demo_save0, mandatory_auth0, syslog/file thresholds5); map rotation exactly its temporary two-minute DM line. No -m/-Y/-C, account/admin/service command or inherited profile. Empty original config data and the allowed parents only. No missing Vita file was filled with user/account data; native informational messages about absent isolated Vita files are retained.

Child PID=PGID67908, new session; cwd web/server/run/T043-20261108T053231-e8b01b6f. Environment only PATH=/usr/bin:/bin:/usr/sbin:/sbin, LANG=C, LC_ALL=C. stdin /dev/null. Stdout and stderr share a Python standard-library PTY for line buffering; the 8MiB bounded combined stream is clearly labeled and no PTY input is injected. This diagnostic capture differs from T036 pipes; it does not change binary/config/network policy.

Native tool environment remains installed Python3.11/lsof4.91/macOS26.5.1/Darwin25.5.0 arm64; exact versions/argv saved. Codesign verifies actual inputs before launch, file/otool inspect accepted identities, and owned-PID lsof verifies actual loaded copied paths/hashes after sockets appear. The supervisor reserves time below the <=8s observation bound for its pending bounded lsof call; actual observation6.650s, child6.786s, total7.142s. The14s watchdog did not fire.

## Actual startup, map, sockets, threads and files

Combined captured log (616 bytes) includes:

```text
logging started: console(INFO), file(DISABLED), syslog(DISABLED), timestamp(DISABLED)
server is LAN-only - without connection to masterserver
dedicated server started, waiting for clients...
added 1 servermaps
read 1 map rotation entries from 'config/maprot.cfg'
```

It also retains the native instruction suggesting a private key and absent Vita-file messages; no such key/account action was taken. Native map-reader log reports534-byte map,1622-byte cfg, version10,size6,rev1,nine entities,spawns1:1:2. No map-load failure is reported. This establishes native map read/registration, not browser rendering/collision/movement, client protocol or match authority.

Actual loaded-file hashes match both signed copies. Live ps has six thread rows. Every one of the41 socket-bearing lsof observations contains exactly the same approved three UDP loopback bindings. No client or probe packet was sent to the server; availability checks were only temporary owned binds before/after. Lack of sampled unexpected sockets is not evidence of zero transient DNS/master/syslog traffic.

Eleven staged files remain byte-identical. Four new files:

| File | Bytes | Role |
| --- | ---: | --- |
| logs/readmaps_log.txt | 320 | real native map scanner |
| logs/debug/maprot_debug_verbose.txt | 958 | real native map-rotation processing |
| private/entropy.dat | 4096 | real native config/vita worker entropy persistence |
| observer-combined_pty.log | 616 | supervisor combined stdout/stderr capture |

Every staged/final/new hash is in the run report; no file was silently deleted/rewritten to make startup pass. No vita/account/demo or host-profile file was produced.

## Exact owned-PID shutdown report and comparison

Per D020, read only the matching ac_server DiagnosticReport whose PID is67908: /Users/jd1/Library/Logs/DiagnosticReports/ac_server-2026-11-08-003239.ips. Supplemental web/server/T043-termination-inspection-20261108T053231.json preserves exact original bytes in base64 and source SHA-256 `6eb8291dea292e82ee169cd33b4feea7ea9138e117d4f50371017ae099998df7`, identity and six relevant thread stacks. No unrelated app report, broad system-log sweep, debugger or privileged trace was used.

Report identity: launch2026-11-08 00:32:32.1474 -0500, capture00:32:38.9325 -0500. Exception EXC_BAD_ACCESS/SIGSEGV, KERN_INVALID_ADDRESS0x5; termination namespace SIGNAL,code11. Main thread is in SDL2 -> sl_semaphore::~sl_semaphore()+24 -> exit -> quitproc(int)+16 -> enet_socket_wait. Faulting thread4 is pthread_mutex_unlock -> SDL2 -> demoworkerthread(void*)+924 -> SDL2/pthread start. Other native workers remain in semaphore waits.

This directly observes live worker accesses concurrent with the main exit/semaphore-destructor path. It does not identify the exact semaphore instance or justify a speculative patch. The proposed fix therefore targets the explicit missing native worker lifecycle, with source references and validation below.

| Observation | T036 original dependencies | T043 verified signed copies |
| --- | --- | --- |
| Original map read | Success | Success; native registration/startup logs also captured |
| Approved loopback binds | 48 socket-bearing/51 total samples | 41 socket-bearing/43 total samples |
| Loaded dependencies | Original SDL2; invalid static signatures | Both copied code paths/hashes observed; signatures verified |
| Capture | Separate buffered pipes, empty at failure | Combined line-buffered PTY,616 bytes |
| Owned SIGINT result | -9; FOUNDATION/libpthread mutex corruption | -11; SIGNAL/SIGSEGV in demo-worker mutex unlock while main destroys semaphore |
| Graceful shutdown | FAIL | FAIL |
| Owned group/ports cleanup | Passed | Passed |

Signing was an independently verified defect/repair variable. This comparison demonstrates that verified signed copies **do not make clean shutdown pass**; it does not prove signatures caused or did not contribute to every earlier symptom. The observed concurrent native teardown is the next precise repair target.

## Source-backed proposal and outstanding scope

notes/questions/T043-AI-Director-native-worker-lifecycle.md maps actual source: quitproc immediately calls exit; cleanupserver has no worker stop/join; map/config/demo handles are discarded, auth/logger handles hidden; their loops wait indefinitely; logger producers can block on the threadlog queue; native semaphore destructors destroy SDL state while workers are still present.

The single proposal is normal-context native shutdown: signal-safe request only; stop submissions; retain real handles; synchronize stop/completion, wake nested map/config/demo/auth waits and define queue/dropbox ownership; keep logging transfer active while producers finish; join producers; drain/stop/join logger before sinks close; then idempotent host/data/static teardown. It includes native/browser boundaries and real validation requirements. Helper names/file/API ownership remain proposals for MAIN to freeze; no source edit, no disabled-worker substitute and no repeated runtime trial was performed.

Packet capture/zero transient egress, all client/protocol/browser/gameplay tests: NOT RUN. T043's startup observations are real, but graceful shutdown is unresolved. MAIN must release any lifecycle fix/build/new runtime pins separately; this handoff does not accept T014/T015/P0/MVP.

Final preservation: signed binary/framework inputs remain exact accepted hashes, current relevant source/header hashes match T039, all215 previously pinned T033/T036 artifacts remain unchanged. Source/build/framework/oldrun/accepted assets are read-only here. T043/D020 revisions were re-read before submission; only MAIN changes authoritative status.
