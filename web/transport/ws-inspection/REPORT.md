# T048 ws 8.21.0 standalone source inspection

Scope: exact official source acquisition and static inspection under D025/T048
2.0. This directory contains **unexecuted inspection material**, not an
installed/approved runtime dependency. No npm command, package import,
lifecycle script, WebSocket constructor, client/server/listener, gateway,
browser or ENet adapter was executed/implemented.

## Acquisition and provenance

Only the two approved HTTPS endpoints were requested:

- [Exact version metadata](https://registry.npmjs.org/ws/8.21.0): HTTP200,
  2384 bytes, ws / 8.21.0, exact approved tarball URL, no redirects,
  ssl_verify_result=0. Metadata SHA-256
  `93704f27b5aefb9970f720af5e59f1078d08585e1d6452b9fec3b26c6578bf17`.
- [Exact archive](https://registry.npmjs.org/ws/-/ws-8.21.0.tgz): HTTP200,
  34987 bytes, no redirects, ssl_verify_result=0. Archive SHA-256
  `d08b726b3aae3a0fed5218a0d9a4b2ac8d75d4ad453a9271db55fe38e94eb4cf`.

The archive SHA-512 matches the metadata SRI **before** extraction:

```text
sha512-Vsp28b7DRcimFQvrqu2Wek3z1iYxDCWqHYB8Qsnk/S4RfaCQzPGPyBNuVjJV3cd6UiKtUtp6sNM77gWvzcCH+g==
```

Measured SHA-512 hex:
`56ca76f1bec345c8a6150bebaaed967a4df3d626310c25aa1d807c42c9e4fd2e117da090ccf18fc8136e563255ddc77a5222ad52da7ab0d33bee05afcdc087fa`.
Legacy metadata SHA-1 also matches, but is not substituted for SHA-512.
Registry signature metadata was preserved; signing keys were not fetched or
signatures independently verified. SRI/TLS are not a runtime safety test.

The first normal-sandbox metadata request failed DNS (exit6); its stderr and
transfer report remain. The same exact URL then succeeded via approved scoped
network escalation. There was no version/host/mirror/credential fallback.
Successful curl ran with clean environment, `-q` to disable curlrc, verified
TLS, HTTPS-only protocol, max redirects0, 30-second timeout, metadata cap256KiB
and archive cap2MiB. Headers/transfer JSON/stderr are retained separately.

Own stdlib processing verified SRI, bounded gzip expansion, then validated the
entire tar inventory before writing. All 19 members are regular relative
`package/` files: no links/devices/special/absolute/parent-escape/duplicate
members or file-as-parent paths. Counts are below128 and actual regular data
151087 bytes is below16MiB, matching registry fileCount/unpackedSize. Source
was extracted only beneath `inspected-source/package/`, as mode0600 data.
`acquisition-and-inventory.json` pins every member's size/SHA-256 and records
the exact metadata/archive identities. No acquired code was imported even to
inspect its exports.

## Manifest, license and module closure

package.json: name ws; version8.21.0; MIT; Node engine >=10.0.0. This engine
range is manifest data, not a tested portability matrix. There are no regular
dependencies. Optional peer packages are bufferutil ^4.0.1 and utf-8-validate
>=5.0.2; both have optional peer metadata. None was acquired/resolved/imported.
Development dependencies are listed in the preserved manifest, not installed.
Scripts are only test, integration and lint; no install/preinstall/postinstall/
prepare lifecycle script is declared. None of those development scripts ran.

Exports select index.js for require, wrapper.mjs for Node import, browser.js
for browser resolution, plus package.json. Browser.js deliberately throws;
browser players must use their native WebSocket API, not this Node package.

index.js eagerly loads eight entry modules and attaches Server,
WebSocketServer, WebSocket, Receiver, Sender, createWebSocketStream,
PerMessageDeflate, extension and subprotocol onto the default WebSocket class.
wrapper.mjs exposes corresponding named/default exports. This differs from
Playwright's custom wsServer/ws/wsReceiver/wsSender utility export names.

The 19 files are LICENSE, README.md, package.json and 16 JS/MJS files. Node
entry closure is index.js plus all13 lib modules; the alternative ESM wrapper
reaches those same lib modules. `module-inventory.json` hashes every script,
records literal require/import locations and verifies all relative targets
exist within this exact package. It is lexical/source inspection, not a
runtime module-resolution trace.

| Module group | Inspected role / entry effects |
| --- | --- |
| constants.js | Detects Blob availability, allocates empty Buffer/local symbols and defines binary modes/close timeout; no listener. |
| buffer-util.js, validation.js | JS buffer/mask/UTF-8 utilities; conditional optional native-addon loads described below; token table allocated locally. |
| receiver.js, sender.js | Defines stream parser/sender classes. Sender allocates a four-byte local mask buffer; random pool fill is send-time. No socket is constructed at entry. |
| permessage-deflate.js, limiter.js | Requires Node zlib and defines compression/queue logic; local trailer/symbols allocated. Shared limiter and compression streams are use-time, not started merely by importing the class. |
| extension.js, subprotocol.js | Defines header grammar/token parsing/formatting, no network calls at entry. |
| event-target.js | Defines own event classes/adapters; registration takes later calls. |
| websocket.js, websocket-server.js | Defines classes and own prototype/static properties. Constructing a client URL starts connection; server port option binds; noServer avoids implicit HTTP listener. None constructed. |
| stream.js | Defines createWebSocketStream; invoking it later wires stream listeners/backpressure. Not called. |

External requires in this closure are Node builtins buffer, crypto, events,
http, https, net, stream, tls, url, util, zlib, plus the two optional addons.
No standalone fs/graceful-fs/debug/chokidar/fsevents/dotenv/process-spawning
utility dependency was found. This is not a claim that Node builtins contain
no native code or no internal initialization.

`lib/buffer-util.js:115–131` tries bufferutil at import unless
WS_NO_BUFFER_UTIL is truthy. `lib/validation.js:136–152` prefers Node buffer
isUtf8; only when unavailable can it try utf-8-validate, unless
WS_NO_UTF_8_VALIDATE is truthy. Set both to1 **before** any future package load.
Without those settings, caught addon-load failures do not prove no native
initialization occurred. Pure-JS here means optional package addons disabled;
Node's native builtins remain part of the separately pinned runtime.

Standalone LICENSE's complete copyright/permission/disclaimer body matches
the ws8.21.0 section of the actual Playwright sidecar after whitespace/header
normalization. Preserve the exact standalone MIT file on any later authorized
reuse. The full Playwright bundle has additional Apache/third-party notices;
this report does not copy/redistribute it or relabel it MIT-only.

## Comparison with actual bundled implementation

Rechecked actual installed utilsBundle SHA-256
`580f571bf063e2256b51b3946a035bc452fc0e22808d5547b198baea39923a32`
and license sidecar SHA-256
`57945338cba4878e373646733528017fbe3db1503ec2b431fd30d2a390c70c33`.
`bundled-comparison.json` records11 selected conditions compared within their
actual module boundaries, including buffer/fragment/payload checks, defaults,
version8/13 acceptance, addon guards and bufferedAmount. The bundler renames
some local variables, e.g. version -> version2. Whole-source byte equivalence
or identical runtime resolution is **not** claimed.

The standalone entry avoids the unrelated eager utilsBundle flow identified
in accepted T044: graceful-fs patches, global queue, debug/platform probes,
signal-exit helper and conditional fsevents. It still performs its own eager
ws closure loading/local allocations and optional-addon selection. Import
purity/availability has no runtime PASS here.

## Exact parser/admission limits

All following mechanisms are statically present, with the same material
semantics as T044. Candidate numeric settings below remain future proposal
values, not a frozen gateway contract or a tested resource guarantee.

| Setting / behavior | Actual standalone evidence and limit |
| --- | --- |
| maxPayload4096 | Receiver61–63,439–449; cumulative data-message payload limit, default server100MiB. Not connection memory/bytes/time/CPU budget. |
| maxFragments16 | Receiver510–532 and decompression565–579 count retained **nonempty payload buffers**. Empty continuations and control frames do not increase that count. Not a total wire-frame/control-rate cap. |
| maxBufferedChunks32 | Receiver98–117 counts `_buffers` queued TCP chunks; not bytes or WS frames. One chunk can contain many frames/bytes. |
| perMessageDeflate:false | Server default false; keep disabled. Receiver rejects unnegotiated RSV compression. Node zlib module loads at entry without implying compression accepted/streams created. |
| allowSynchronousEvents:false | Defers data/ping/pong delivery with setImmediate; not a rate/CPU budget. |
| skipUTF8Validation:false | Keep UTF-8 protocol validation. Does not make traffic binary-only; gateway must separately reject isBinary=false. |
| path:'/enet' | Server224–234 strips query before comparing path. No capability/query/destination validation. |
| Origin/subprotocol/version | Server handleUpgrade accepts WS8 or13 and defaults unrestricted Origin. False handleProtocols omits selected protocol but does not itself abort upgrade. Parent must explicitly reject wrong/missing Origin/protocol/version/token before any session allocation. |
| masking / message boundaries | Server receiver requires client masking; controls/opcodes/continuations validated; complete data message emitted only after FIN. Do not add a second ad-hoc parser. |

There is no builtin total wire-frame/control-rate cap, queued-byte cap, session
admission cap, datagram destination policy, ENet fragment/reassembly allocation
bound, or idle/pong watchdog. D025's complementary-policy requirement remains
unresolved future transport design, not solved by these options or an echo test.

## Buffer ownership, backpressure and teardown

buffer-util concat returns the original buffer for one fragment; toBuffer can
retain Buffer/ArrayBuffer views; unmask mutates received data. Receiver binary
delivery can share those buffers (receiver596–635). Sender may pass references
to the socket; retain immutable owned message data until completion, never a
temporary Wasm heap view. No universal ownership-copy guarantee exists.

WebSocket.send (websocket.js:455–484) returns no drain Boolean. CONNECTING
throws; closing/closed paths schedule callback errors. Callback success is
local write completion, not remote application/UDP/server acknowledgement.
bufferedAmount at120–124 sums socket writable length and sender buffered
bytes, with no automatic application cap. Receiver/socket pause/drain paths
provide mechanisms, not an application byte/age/admission policy.

Server.close at159–211 removes listeners and can wait for tracked clients;
it does not terminate clients or own-close a supplied HTTP server.
WebSocket.close starts its close handshake/timer (default30s); terminate
destroys its socket. A proposed closeTimeout2000 still needs a parent deadline
and forced cleanup. autoPong is not periodic heartbeat/liveness monitoring.
setSocket disables raw socket timeout; explicitly own post-upgrade deadlines.
wsClientError listeners must actually reject/destroy the socket rather than
only log. Attach error/close handlers and close every owned resource/timer.

## Proposed later runtime scope — NOT AUTHORIZED / NOT RUN

1. A separately released import-only child, using the already installed
   `/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node` (24.19.0 from the
   accepted SDK) with exact executable hash and this archive/member manifest
   rechecked. Isolated ticket temp cwd; clean environment with PATH=/usr/bin:/bin,
   WS_NO_BUFFER_UTIL=1, WS_NO_UTF_8_VALIDATE=1; omit NODE_OPTIONS/NODE_PATH,
   credentials/proxy/profile environment. Direct absolute index.js path,
   never bare require('ws')/Playwright bundle resolution or npm install.
   Parent deadline <=5s and bounded stdout/stderr <=64KiB. Compare export
   identities, loaded module paths, fs.close/closeSync identity, environment,
   globals/process-listener/active-resource deltas. No constructor, connect,
   listen, watch, subprocess, compression or helper call. This entry is still
   inspection material; using it at all requires the next explicit release.
2. Only after that review, a separately released <=10-second numeric-loopback
   dependency self-test may own one HTTP listener and helper WS endpoints,
   noServer/manual upgrade and exact parent admission. Test message4096/4097,
   16/17 nonempty fragments, empty/control-frame behavior, chunk-count behavior,
   binary discrimination, masking/errors, byte accounting and forced cleanup.
   Candidate parser settings above must be frozen then; session/rate/byte/ENet
   policies need their own explicit complementary contract. No real gateway,
   native server, arbitrary host, port forwarding or game-state API is implied.

These are proposals, not implemented scripts or accepted transport decisions.
Installed module import, listener cleanup, parser enforcement, browser joins,
multiplayer and gateway memory/rate bounds all remain NOT RUN.

## Preservation / evidence

Raw metadata/archive/headers/transfer reports retained. All source files have
per-file SHA-256 in acquisition-and-inventory.json; module-inventory.json and
bundled-comparison.json preserve the static checks. Final fingerprints and
runtime-freeze comparison are recorded separately before handoff. Current
web/build/out, engine/QA/server/assets/contracts and earlier T044 files were
read-only throughout T048. T040's next MAIN-accepted graphics rebuild takes
priority; no such source acceptance is inferred from this dependency work.
