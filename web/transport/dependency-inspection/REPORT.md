# T044 installed WebSocket dependency inspection — source only

Ticket T044 revision 1.6; QA/Performance. This is static inspection of existing
installed source, metadata and notices, not approval to import, construct, bind,
connect, implement or distribute a gateway. No dependency code was executed and
no package/library source was copied. T030 real artifact runs retain priority.

## Identity and reproducible inventory

Installed root:
`/Users/jd1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core`.
The manifest identifies **playwright-core 1.62.1**, Node **>=20**, Apache-2.0.
Its `lib/utilsBundle.js.LICENSE` explicitly identifies **ws 8.21.0**, resolving
the version uncertainty recorded in historical T035. This is bundled source,
not an independently installed top-level ws package.

`SHA256SUMS.txt` pins six actual installed files with absolute source paths:

| File beneath installed root | SHA-256 |
| --- | --- |
| lib/utilsBundle.js | `580f571bf063e2256b51b3946a035bc452fc0e22808d5547b198baea39923a32` |
| lib/utilsBundle.js.LICENSE | `57945338cba4878e373646733528017fbe3db1503ec2b431fd30d2a390c70c33` |
| package.json | `07c47543631fef9508760365dee9fbe958c562093ec8d122543949ed231f233f` |
| LICENSE | `45873d00a0dd243596deb4aa23b2493b3d1f0671921bf2538ea431d7380220eb` |
| NOTICE | `6d602191187b35b9b01d2cffa01c8469c2c8d9de8a96f1bf868e0f264f51c81d` |
| ThirdPartyNotices.txt | `a549d329bad8806fe279f0ecae0fc0270dec7e7c2dc8ec10f90e394f7c32b144` |

Hashes were measured with the installed `shasum -a 256` utility reading those
files, not by importing Node/Playwright/ws. Source references below are one-based
lines of this exact pinned bundle; package updates require reinspection.

Companion inventories are textual line-reference reports, not executable copies:

- `external-require-lexical-inventory.txt`: 193 literal require matches across
  the complete bundle. It intentionally preserves matches in comments/generated
  code strings; those are not claims of executed requires.
- `eager-entry-inventory.txt`: 449 wrapper/entry/import assignment references.
  A `var require_x = __commonJS({...})` defines a lazy module body; it does not
  execute that body. Top-level `require_x()` calls inside `__toESM(...)` do execute
  its body on entry. These two forms must not be conflated.

Inspection commands used `cat`, `sed`, `rg`, `head`, `tail`, `ls`, `wc`, `awk` and
`shasum`; report writes remain inside this new directory and own T044 notes.
No compiler, dependency import, script entry point, browser or network was run.

## Minimal entry/export path and initialization

`package.json.exports` explicitly maps `./lib/utilsBundle` to
`./lib/utilsBundle.js`; the exact installed absolute file is the smallest
available inspected entry for these exports. Future CommonJS code can require
that exact pinned file, or the exported package subpath only when module
resolution is deliberately pinned to this installation. This report does not
execute either expression. Do not import the package root/browser CLI merely to
obtain a WS server.

Names are exactly **`wsServer`, `ws`, `wsReceiver`, `wsSender`**. The export table
near 53056 creates getters; assignments near 90625 bind them to the imported
WebSocket/server/receiver/sender classes. `wsServer` is the server class; do not
assume the default `ws` class has the standalone package's `Server` alias.
The local package subpath is exported, but these utility names/options remain
Playwright bundle interfaces, not a promise of standalone ws packaging stability.
No extraction/rebundle or library copy is authorized here.

The getters do **not** make selective destructuring a selective import. Requiring
the file executes its complete top-level initialization:

- At 62348–62355 the ws stream, extension, compression, receiver, sender,
  subprotocol, websocket and websocket-server lazy wrappers are invoked eagerly.
- ws leaf definitions/constants start at 10493; buffer utilities at 10516,
  compression 10641, validation 11024, receiver 11225, sender 11857, event-target
  12350, extension 12579, websocket 12732, stream 13628, subprotocol 13726 and
  server 13771. Their constructors/connection functions are defined at require
  time; they do not create a socket merely because a class was loaded.
- Many unrelated imports are also eager: colors/debug/INI, dotenv, JPEG/PNG,
  source-map-support, Enquirer/Chokidar, zip readers/writers/graceful-fs/retry,
  proxy/open/CLI/schema utilities and protocol clients. Do not treat this as a
  side-effect-free ws-only module or prune it by ad-hoc source extraction.

### Transitive external requires

The ws closure's external requires are Node built-ins **buffer, crypto, events,
http, https, net, stream, tls, url, util, zlib**, plus conditional native addons
**bufferutil** and **utf-8-validate**. The permessage-deflate module requires zlib
when defined even if later server negotiation disables compression; constructing
inflaters/deflaters remains use-time behavior. Sender initialization allocates
a four-byte mask buffer and defines a random pool; filling/using random mask data
occurs during sends, not a connection launched at import.

The complete bundle additionally references Node built-ins **assert,
child_process, constants, dns, fs, fs/promises, http2, os, path, process, readline,
stream/promises, tty**, alongside the ws set. `node:`-prefixed aliases are listed
separately at their precise lines in the lexical inventory. These are real module
loads/definitions; requiring child_process/net/dns is not itself spawning or
connecting. No arbitrary host is selected by module loading alone.

Additional external paths/conditional use:

- **bufferutil**, buffer-util lines 10574–10586: attempted at require time unless
  `WS_NO_BUFFER_UTIL` is truthy; load failure caught, JS mask/unmask fallback used.
  Presence/native code side effects are **not verified by execution** here.
- **utf-8-validate**, validation 11208–11220: Node buffer `isUtf8` is preferred;
  otherwise the addon is attempted unless `WS_NO_UTF_8_VALIDATE` is truthy.
  A pure-JS fallback exists. Runtime availability of the Node builtin was not
  probed; do not claim a native addon was/was not loaded.
- **fsevents**, 35336–35359: Chokidar's eagerly reached helper attempts an optional
  external require in try/catch. This is distinct from actually starting a watch.
  Its installed resolution and native initialization are not pinned by the six
  files above. `CHOKIDAR_PRINT_FSEVENTS_REQUIRE_ERROR` can make failures observable.
- **module** and **worker_threads**: source-map-support `dynamicRequire(mod,request)`
  near 24421 is called by later installation paths near 24833/24854, not the base
  class/export load. No `.install()` was invoked by this inspection or is needed
  for a gateway.
- Apparent external **ajv/dist/runtime/{validation_error,uri,ucs2length,equal}**
  and **ajv-formats/dist/formats** literals are generated-code references/string
  templates (for later schema/codegen use), not evidence that Node requires those
  paths during ws import. `require('enquirer')` / custom-prompt examples in comments
  similarly are not extra external modules loaded by those lines.

The lexical inventory plus these distinctions cover inspected external require
sites; they are not a proof of runtime module resolution. No addon/library was
copied, downloaded or imported. A future import must either explicitly disable
optional ws addons in its child environment or separately pin/review them; the
unrelated fsevents attempt must also be observed/reconciled before a blanket
claim that all require-time native code is inspected.

### Concrete entry side effects and use-time boundaries

| Source | Static entry/use finding |
| --- | --- |
| debug common/node, ~984 / 1420 | Initialization calls `enable(load())`, reads DEBUG/env/TTY/color settings and can save/delete DEBUG in the child process environment. No log/file/network sink is started just by loading a namespace. |
| is-wsl, 58211–58282 | Top-level `isWsl()` unless test env overrides; non-Linux short-circuits. On Linux it can read /proc/version and stat WSL/container paths, including /.dockerenv, /run/.containerenv and /proc/self/cgroup on the relevant branch. Platform-sensitive filesystem reads exist. |
| graceful-fs, 39173–39255; import 62501 | Eager import publishes a shared queue on fs/global and wraps shared Node `fs.close` / `fs.closeSync`, then patches a clone. TEST_GRACEFUL_FS_GLOBAL_PATCH can broaden patching. NODE_DEBUG=gfs4 can register an exit assertion. The wrappers run later on close calls; the shared mutation happens at import. |
| signal-exit, ~62530–62753 | Constructs a SignalExit/Emitter and defines a symbol-keyed global emitter. Signal listeners and process emit/reallyExit patching are in `.load()`/registration, not equivalent to constructing that object. Do not call unrelated exported onExit/open/CLI APIs. |
| source-map-support, ~24409 onward | Loads helpers and defines caches/install/stack/file retrieval functions; actual source-file reads/hook installation need those later functions. No install is needed for WS reuse. |
| dotenv/open/process utilities | Loading definitions is not `.config()` (env-file read), opening a browser, spawning powershell/xdg-open, or parsing/acting on CLI args. These use-time capabilities are in the same module and should not be invoked by the gateway. |
| wsServer/WS constructors | `new wsServer({port,...})` creates/listens on HTTP immediately; `server:` installs upgrade listeners on supplied server. `noServer:true` avoids an automatic listener but still constructs server state. `new ws(url)` begins client connection. None were invoked here. |

No unconditional socket/listener/watch/subprocess/download was identified in the
inspected entry flow, but this remains **static evidence, not an import-time
side-effect trace**. Optional uninspected addons prevent an unconditional purity
claim. Run a future approved import in an isolated child process, not inside the
main game observer/supervisor, so fs/env/global effects end with that child.

## Parser/server options and exact limits

Server constructor 13828–13855 merges defaults with provided options, and
completeUpgrade 14111 forwards the parser options through WebSocket.setSocket
12912 into Receiver's constructor 11268. Options are real in this pinned source:

| Proposed setting | Supported? Exact source semantics |
| --- | --- |
| maxPayload:4096 | Yes. Positive 32-bit integer. `haveLength` 11587 checks cumulative data-frame payload before reading the full payload; decompression path also checks. Error 1009 / WS_ERR_UNSUPPORTED_MESSAGE_LENGTH. Default is 100 MiB, not safe to inherit. Control payloads have their protocol-specific limits; maxPayload is not a connection-byte/rate budget. |
| maxFragments:16 | Yes, but counts retained **nonempty payload fragments** in `_fragments`, 11645/11686, not all wire frames. Empty continuation fragments/control frames do not increase that array. Error 1008 / WS_ERR_TOO_MANY_BUFFERED_PARTS. Default 131072. It cannot promise “at most 16 wire frames per message/connection.” |
| maxBufferedChunks:32 | Yes. `_write` 11305 rejects admission when `_buffers.length` already reaches the limit. This is TCP stream-chunk count, not datagram count/bytes; a chunk may contain many WS frames, and its byte size is not capped by this option. Default 1048576. |
| perMessageDeflate:false | Yes, server default false; do not negotiate compression. Incoming reserved compression bit without extension is rejected by Receiver. `send` only compresses with a negotiated extension; explicit compress:false is still clearer. zlib module definition loading is not compressed traffic acceptance. |
| skipUTF8Validation:false | Yes; keep protocol validation. This is not binary-only admission. Text still parses/emits with isBinary=false and gateway must reject it. |
| allowSynchronousEvents:false | Supported; defers message/ping/pong delivery through setImmediate instead of repeated synchronous events. Not a frame/time/rate budget. |
| closeTimeout:2000 | Supported through server options to constructed WebSocket. Default CLOSE_TIMEOUT is 30000 ms. Parent still needs owned deadline/terminate fallback. |
| noServer:true / manual handleUpgrade | Supported. Parent owns explicit loopback HTTP server/header/deadline/admission checks and calls handleUpgrade only after approving request. Cannot combine port/server/noServer ambiguously. |
| path:'/enet' | Supported; `shouldHandle` strips query then compares raw pathname. It does not validate query/capability parameters. Parent must reject extra destinations/invalid tokens itself. |
| exact Origin / subprotocol / version13 | No automatic restrictive policy. verifyClient is an optional hook; default accepts. handleProtocols chooses a response protocol, but returning false/undefined does **not** by itself abort upgrade. Missing protocol can still upgrade. Source accepts WS version 8 or 13. Parent must reject wrong/missing Origin, wrong/missing exact subprotocol, unwanted version and token before handleUpgrade. |
| masking | Receiver server mode requires client MASK and rejects unmasked frames (1002); client mode rejects masked server frames. Library handles masking/control/opcode/continuation validation; do not implement a second parser. |

Origin/path/token checks must precede UDP-session allocation. If a wsClientError
listener is installed, the source emits that event instead of doing its default
abort; its owner must actually reject/destroy the socket, not merely log it.
There is no built-in session cap, datagram minimum length, fixed-destination
restriction, capability verification, queue byte cap, message/control-frame rate
cap, maxBufferedAmount option, idle/pong watchdog, or bounded UDP operation queue.
Those are future gateway policies needing MAIN's frozen interfaces/ownership.

**Unsupported interpretation requiring resolution:** T035's count limits must not
be claimed as total WS wire-frame/CPU/raw-byte bounds. In particular, empty
fragment/control-frame floods are not bounded by maxFragments:16, and queued TCP
bytes are not bounded by maxBufferedChunks:32. No adapter/option is invented here.
MAIN must adopt the actual semantics plus a reviewed complementary policy or
request a different inspected dependency. Passing normal loopback traffic cannot
waive those limits. ENet reassembled allocation bounds remain a separate T035
issue; these WS options do not address them.

## Ownership, backpressure, errors, liveness and teardown

- Receiver emits **one complete message** only after FIN (11709 onward), with
  `isBinary` flag. Default `nodebuffer` may return the original single-fragment
  buffer; concat returns its input unchanged in that case (10522). Unmasking can
  mutate underlying received buffers. `arraybuffer` conversion sometimes returns
  the underlying whole ArrayBuffer, otherwise slices. Therefore there is **no
  universal ownership copy** guarantee for application callbacks.
- Sender.toBuffer may reuse Buffer/ArrayBuffer memory (10549); uncompressed sends
  write header/payload references to the socket (12323). The future gateway must
  retain immutable owned data until send callbacks/UDP callbacks complete and
  never retain temporary Wasm heap views. This inspection creates no buffer bridge.
- `ws.send` (13101) does not return a TCP drain Boolean. CONNECTING throws; closed
  state schedules callback error and can increase buffered accounting. Callback
  success means local write progress, not remote application delivery.
- `bufferedAmount` (12838) includes socket writable state length plus sender
  buffered bytes. No automatic high-water cap is applied. Receiver write false
  pauses socket; drain resumes unless manually paused. Public pause/resume support
  exists, but application admission/age/byte limits remain external policy.
- Parser errors lead to ws error/close; sender/socket errors have distinct paths
  (13537–13624). Attach error/close handlers to every owned HTTP/WS/socket object;
  do not swallow parser errors or rely on an unhandled EventEmitter error.
- `autoPong` defaults true; receiver emits ping and pong (13555). There is no
  autonomous periodic ping or timeout watchdog; parent must track liveness.
  `setSocket` sets raw socket timeout to 0 (12937), so an HTTP idle timer is not
  a post-upgrade liveness policy.
- `ws.close()` begins the protocol close with a timer; `terminate()` destroys
  its socket. `wsServer.close()` stops/removes server listeners but does **not**
  automatically terminate tracked clients; noServer/external-server modes can
  wait for clients and do not own-close the caller's HTTP listener. Close all
  clients, bound/terminate stragglers, close caller-owned HTTP/UDP resources, clear
  queue references/timers and await server/process closure. Future child-process
  exit also contains unavoidable whole-bundle global patches.

No masking/close/queue/transport behavior has a runtime PASS from T044. The source
supports mechanisms; runtime lifecycle/error guarantees need explicit testing.

## License/provenance and portability

Root LICENSE is Apache-2.0; NOTICE identifies Microsoft/Puppeteer provenance.
ThirdPartyNotices.txt explicitly delegates inlined component notices to the
bundle's `.LICENSE` sidecar. Its ws@8.21.0 section (2021–2044) contains the MIT
permission/disclaimer and copyrights for Einar Otto Stangvik (2011), Arnout
Kazemier/contributors (2013) and Luigi Pinca/contributors (2016). Preserve these
notices if that software is copied/distributed in any future approved artifact.

Reusing/redistributing the **whole** utilsBundle is not “MIT ws only”: retain the
whole sidecar and applicable Apache LICENSE/NOTICE/ThirdPartyNotices for its other
components. This is source notice identification, not a new asset/license
clearance or authority to copy the bundle. Optional externally resolved addons
would need their own provenance/license/hash review. The exact installed bytes
are locally measured, not a publisher-signed or independently reproduced package.

The absolute Codex runtime cache path is machine-specific. Bundle relocation,
Playwright update, Node/platform change or using another package resolver can
change optional-addon selection and eager platform probes. Freeze the exact
entry/manifest/sidecar hashes and Node executable/version in a future execution
ticket. Do not assume top-level import availability or absence of addon effects
from this text inspection.

## Proposed future scoped self-test — NOT AUTHORIZED/NOT RUN

First approve a bounded **import-only child** with the exact bundle/manifest/license
hashes above, existing Node executable, isolated temporary cwd, clean explicit
environment, WS_NO_BUFFER_UTIL=1 and WS_NO_UTF_8_VALIDATE=1, and no constructor,
client, listener, watch, subprocess, dotenv config or unrelated utility call.
Inspect/freeze fsevents resolution beforehand or explicitly observe it under the
new scope. Capture loaded module paths, env/fs/global/listener/handle deltas, exact
export class/method identities and exit within 5 seconds. No runtime/availability
claim is made until that independently reviewed child runs.

Only in a subsequent explicitly released loopback dependency self-test: construct
noServer:true with exact supported limits, parent-owned numeric-loopback HTTP
server, two owned helper endpoints and total ≤10-second lifetime. Test 4096/4097
bytes, text/binary discrimination, 16/17 nonempty fragments, empty fragments,
32/33 controlled parser chunks (clearly test-only chunk injection), masking,
wrong/missing Origin/protocol/path/version, compression RSV, close/error and slow
consumer buffer reporting. Verify owned cleanup without calling it game/network
acceptance. Its helpers cannot pass real two-browser/native ENet gates.

MAIN must first resolve count-limit semantics and whole-bundle import side effects,
approve any reuse and release exact implementation/self-test scope. No handwritten
WS parser or silent omitted bound is recommended. T021/T015 implementation and
experimental transport/engine selection remain unreleased.
