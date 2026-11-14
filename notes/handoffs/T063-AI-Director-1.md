# T063 genuine browser ENet peer/native component

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket: T0633.8 RELEASED; D050 prerequisite3.6 + D0523.8; governing browser foundation/GOVERNANCE/P0 0.5. Current ticket/D052 re-read before actual execution and submission; no authoritative status changed.
- Base: 13f0d8eea4822dee5c976661218d022be74342e3 plus shared existing/concurrent source work. No existing consumer/main/client/core/backend/gateway/vendor/SDK/native/source/build/QA/asset modifications, commits, push/reset or dispatch.
- New files only: `web/transport/tests/native-enet/T063/{peer.c,build.py,browser.cjs,run.py}`, `web/transport/results/native-enet-T063/**`, two fresh `web/server/run/T063-*` trees (one empty preflight-only), own question and this handoff.
- Component source/drivers now frozen. One actual native/browser/gateway baseline passed; no further runs after PASS.

## Acceptance evidence

**PASS — actual ENet core peer path.** Genuine enet_host_create(NULL,1,3), wait for browser-native WS OPEN, actual enet_host_connect to127.0.0.1:29863, real enet_host_flush/service and event dispatch through accepted backend → accepted real gateway → unchanged actual native UDP server. First actual baseline observed one ENET_EVENT_TYPE_CONNECT and one native channel1 RECEIVE from the same real event.peer, then a real ENet disconnect event. No synthetic native peer, echo endpoint, forged event, game parser or C++ consumer was linked/executed.

Browser measurement from component start: WS OPEN27.9ms; minimum genuine CONNECT+RECEIVE evidence60.9ms; complete probe86.3ms. These are observed functional timings, not latency/performance targets. Service yields through actual requestAnimationFrame, uses a new frame ID per tick, real backend32-datagram/64KiB frame budget and <=64 events/step. Four service frames/three actual events total including disconnect; failure counter0.

Actual received packet: **63 bytes, channel1**, SHA256 `a43640d15771057d9abd680ce6eda13525967ec19d059fc99d487911228e5ec2`; incoming/outgoing peer IDs0; actual connectID881814289 matches recorded live peer. Native target127.0.0.1:29863. Payload was copied synchronously into a bounded independent fixture buffer for SHA256 only, then its ENetPacket destroyed once. Actual received1/destroyed1/referenceCount0. Owned copied bytes cleared after hashing; no raw native payload/key/private bytes logged. No AssaultCube message type was decoded or classified.

**PASS — two real transport legs corroborated.** Gateway one admission/UDP allocation, source tuple127.0.0.1:62441 connected to fixed native29863, peak active/retired/UDP1. Actual gateway counters: browser→native4 datagrams/92bytes, native→browser3 datagrams/143bytes; browser core raw sent4/received3 after disconnect. Native stdout records actual client connect/disconnect; map reader succeeded and one servermap registered. Real native socket samples show only127.0.0.1:29863/29864/28762; six native threads and actual signed copied SDL2/hidapi loaded, no original framework. Gateway never parsed/rewrote ENet or gameplay.

Actual browser handshake through accepted gateway, read-only CDP observation: version13, fixed Host/Origin, outbreak-enet-dgram.v1, standard permessage-deflate offer; actual101 response selects protocol and no extension. No request-header rewriting. One private random capability consumed of two configured hashes, tokens never printed/stored in result; Node scans output against both tokens. One inherited frozen legacyGL initializer warning is retained explicitly, zero unexpected browser/page errors.

**PASS — real native shutdown and all owned cleanup.** Native PID=PGID95335, actual lifetime1.5640s; owned SIGINT exit0 in0.002107s, no kill/watchdog/crash or loaded-library mismatch, group absent and lsof native handles empty. Browser PID95344 stopped; Node child95343 reaped/group absent, context and temporary profile removed. Actual ENet disconnect request/service phase completed within the1s grace; recorded25.3ms drain-phase upper bound includes subsequent hash and backend-close work, so it is not a pure ACK latency. Actual backend WS close6.3ms. Node cleanup106ms, total child1.245s / parent2.2150s. Gateway idempotent close resolves with0 active/pending/retired UDP/TCP/timers/listeners; static0 handles. No owned fallback/repair action.

All fixed UDP29863/29864/28762, gateway ephemeral UDP62441 and TCP29865/29866 bind probes succeed after cleanup, errno recorded; TCP also no-LISTEN lsof exit1/empty with SO_REUSEADDR bind/close, no plain-bind/TIME_WAIT inference. Native staged files unmodified; only owned maprot/readmaps logs and private/entropy.dat added, all snapshots/hash sizes retained. Native stdin /dev/null; no inherited profiles/scripts/master/key/account/syslog/include; exact old-c1 argv/config/map/lib controls.

**PASS — real build/reuse/identities.** New wrapper compiles and component links against genuine seven core ENet release objects + accepted backend object, each byte-verified against accepted T058 build manifest; all corresponding current source/header inputs checked before reuse and runtime. Exact T058 release flags/SDK/frozen cache/safe legacyGL/ASSERTIONS0/64MiB initial/2MiB stack/growth/--js-library profile, no new flags/dependency/port/download. Only component test exports, no export-all. Native binary/frameworks never rebuilt, signed or modified. Actual source/tool/build/served/native/library/vendor/map/config/argv fingerprints and environments are in build/runtime/final reports. Current checks stale_inputs=[], diff --check passes.

## Preflight failure and exact D052 reconciliation

First supervisor invocation stopped before any native/browser/gateway process at historical sound.h dependency hash. `run-20261108T071124-a21e847a/result.json` remains immutable FAIL, native PID absent; port probes clean. No actual launch allowance consumed. Own question `notes/questions/T063-AI-Director-native-sound-pin.md` and read-only sound-pin-audit remain preserved.

MAIN D052/T0633.8 authorizes only the exact transition:

- historical/preserved original sound.h `0abee07769e72a97d396abc53808a9be999b50b850dc17c3a924724274d477ff`;
- current accepted D047/T059 sound.h `80f635fd48b40ec61524d52707ba7c6f80eb2ad2d8bead137099bdf462c11655`;
- pinned /usr/bin/unifdef SHA179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818, args -U__EMSCRIPTEN__ -DSTANDALONE, both410 identical normalized tokens, token SHA `d5ee369287f993eba162e788183abc96099b7b01f87f8a8c6149adf66e8c4c08`;
- D052 identity manifest SHA `5441fbb6ed7c9a5e5eae2fff6b89d19ceaa8e3f11d0e557357791a01eed471ec`.

Changed inspected supervisor pins that exact manifest/tool/original/current/native-token proof and reports both identities, rather than calling the old raw header current. Every other historical native dependency remains strict. This is neither general header-ignore policy nor source/binary mutation. New actual result/rationale is separate from first preflight. No native runtime failure or retry occurred; exactly one actual baseline. Execution escalation approved these precise authorized loopback actions; no automatic rejection.

## Exact commands and artifacts

Executed from repository root after entrypoint inspection:

```text
python3 web/transport/tests/native-enet/T063/build.py
python3 web/transport/tests/native-enet/T063/run.py --rationale 'Initial reviewed T063 genuine ENet core CONNECT and native channel RECEIVE through accepted gateway; exact pinned release-c1 and bounded owned cleanup.'
python3 web/transport/tests/native-enet/T063/run.py --rationale 'D052 exact sound.h historical/current native-view reconciliation added to inspected supervisor; preserve first preflight refusal, run first actual pinned release-c1 ENet baseline.'
```

Second listed command was preflight-only FAIL; third performed the single actual launch/PASS. Commands are history, **do not rerun** after baseline PASS. Fresh original component/native outputs only, old accepted evidence untouched. Read-only final identity/header checks executed separately with no service/browser launch. Earlier static-validation.json records preflight-only stage (actual_launches0), not final acceptance; current final-verification.json records actual_launches1/PASS.

Host arm64 macOS26.5.1/Darwin25.5, Python3.11.9, Chrome156.0.8078.80/Playwright1.62.1. Exact accepted Node `/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node` SHA27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1; WS_NO_BUFFER_UTIL=1/WS_NO_UTF_8_VALIDATE=1, PATH=/usr/bin:/bin, ticket-owned TMPDIR. Native environment only PATH/LANG/LC_ALL. Browser sandbox enabled, unsafe default args removed, temporary profile, no external application URL. Packet-level zero-egress NOT RUN; observations are not capture.

Current outputs under `web/transport/results/native-enet-T063/`:

- peer.o `a073e2094d25a02f74fe41fccb75a06b8466beac855d0a795079b5ada7396896`
- peer.mjs `f1c2f36a891bce06bc7bc8908ff5296f0638dc86c8fc5c8a209183c6b0ae4a20`
- peer.wasm `31f17c650564b83ad02cecc9865562cc91ea0897fd08a3691809433b3a9954a3`
- build.json `1f34abf77e1286d7c699a0c5929027ade8aac5857926a68ebd8fac82a74fc5ae`
- **actual PASS** run-20261108T071518-d7bf1476/result.json `d55de739eac087639970ee57212ec0921d91c59e09696fe27a9d01c1cf6671f2`
- preserved preflight run-20261108T071124-a21e847a/result.json `e1ae6d2e654a0a1ffdcf53a744a14a592a967475a78ca4aa25e1df2d8891ead5`
- final-verification.json `4f6ad7eec985a4895564a967124bef309f4ffbe0507a5a2abeb5395e284907d6`

Native run tree: `web/server/run/T063-20261108T071518-d7bf1476`; raw bounded combined PTY capture is in corresponding result directory/native.log; Node JSON/stdout/stderr retained. No native payload in those metadata reports. Exact original-c1 argv and config byte hashes are in runtime JSON. Unchanged native binary49a1d28a6251213e27464afb36b6d974215c9886045a38d00a9cfe66befb096a; gateway f70dacb108df16d2f228b866a392927fda61b4e2895fa041ced9f8ab3bb3613e and policy bbc53104cf2b9b87abfcb5711ef830cb2e1180bfda4800d6021ed42363a9a831 match D050.

Current new source SHA256:

| File (web/transport/tests/native-enet/T063/) | SHA256 |
|---|---|
| peer.c | 2b592eb5e95852df826905b8facb3feb93dfaa9716047be51e54aa7ac8b4f4e3 |
| build.py | 3def63ee6da486b5a54a7b0a806d3f1c3864ac9612f23e09953fd0e69fb35950 |
| browser.cjs | 42b36b7556fdc9b03e6500a3d41416e830158dfec210df2e99b52f478ecd72da |
| run.py | ce067214c059b3480adee04ffa140557d483cb1c602eca8922788053e1353c8c |

## Limits / next gate

This proves one actual browser ENet peer/core event path to the unchanged native server through the real gateway. It does **not** prove AssaultCube game auth/intro/WELCOME/map-ident/spawn/movement, two players, continuous reconnect, authority, P0/P1/MVP or production transport. No game message emitted/emulated; native reply never fed into the C++ game parser. Client-reported hit/movement debt, untrusted map/1GiB reassembly exposure and whole-process memory/CPU containment remain unresolved. The fixture's64KiB copy/64 event bound is not an ENet reassembly allocation bound. Inherited ASSERTIONS0 runtime limitation retained.

MAIN reviews actual result before consumer/native game integration release. T061/T062/T060 remain independently owned; no source changes after this handoff freeze and no additional baseline runs under this passed allowance.
