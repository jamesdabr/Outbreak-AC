# Native runtime SIGKILL and invalid arm64 SDL2 signature

- Author / worker: AI-Director
- Ticket and revision: T036 / 1.0 RELEASED
- Phase and contract revision: BROWSER_FOUNDATION/GOVERNANCE/P0 0.5 plus D010 runtime addendum 1.0
- Exact clause or interface affected: T036 criteria 2, 4, 5; accepted unchanged native framework input and clean owned SIGINT shutdown
- Status: OPEN (lead resolution is recorded separately)

## Question

Please investigate/release a narrowly owned native SDL2 dependency repair or otherwise decide the next native runtime diagnostic step. The exact accepted unchanged framework fails arm64 code-signature verification, and the accepted real server exited by SIGKILL after owned SIGINT. T036 cannot modify/re-sign the framework, rebuild source or change the accepted binary.

## Evidence and impact

Actual run: web/server/T036-20261108T051556-89f4ee4b.json, cwd web/server/run/T036-20261108T051556-89f4ee4b. Accepted release SHA-256 296601782e7ff1510b5c9900548bad34c28c97a73d9d571b4d5037c88a9e6005; SDL2 SHA-256 1b11de3d606e85fed9cad1f54bc2a833e99e6fc1e67fb2e748cdb666dbd0f681 matched accepted input before execution. Exact D010 argv/config/map were used, and all inspected compiler/header dependencies matched accepted build evidence.

The real native map reader succeeded: version 10, size factor 6, revision 1, 9 entities, 534-byte cgz, 1622-byte cfg, reported in logs/readmaps_log.txt. All observed socket entries were exactly UDP 127.0.0.1:29863,29864,28762; 51 samples total, first three sockets at ~0.680 seconds. No clients connected.

After ~8.046 seconds of observation supervisor sent SIGINT to its own recorded new process group, PID/PGID 61970. Child returned -9 after ~0.148 seconds; no supervisor fallback/watchdog SIGKILL was invoked. Process group and ports were released. Buffered stdout/stderr were empty, so startup/added-servermap console messages cannot be claimed. Server-produced readmaps/maprot logs and entropy.dat were retained.

Read-only `/usr/bin/codesign --verify --verbose=4 web/server/out/release/ac_server` succeeds. The same inspection on `source/xcode/Frameworks/SDL2.framework/Versions/A/SDL2` fails: `invalid signature (code or signature have been modified)`, `In architecture: arm64`. Exact raw results are recorded in the T036 supplemental inspection JSON. This makes the framework a concrete dependency validation failure. It is a possible explanation for SIGKILL, not proven causality without a separately authorized diagnostic.

## Options for owner and lead

1. Inspect the exact existing framework/signature and release a narrow dependency repair/signing owner and new measured/pinned runtime inputs, then re-release bounded startup. Do not silently overwrite/re-sign the accepted original.
2. Release a concrete additional read-only local runtime diagnostic if needed to establish SIGKILL cause. No system-wide log/private crash-report access, trace elevation, dependency installation or debugger run is inferred here.

## Work paused

Further server launches with the known-invalid framework are paused; supervisor now rejects code-signature failures before launch. Existing captured map/bind/shutdown/file evidence, source analysis and handoff continue independently. No source/framework/config/map repair, account, remote service or packet-capture escalation is performed. Zero-egress packet evidence remains NOT RUN because available BPF devices are root-only.
