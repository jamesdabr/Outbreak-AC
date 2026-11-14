# Fixed local visual playtest

Current MAIN review D492; historical preparation originated with T279/D476. Source ready for NEW stock-combat-1 and NEW local-14; MAIN must review and separately release the browser rebuild and execution. Native3 build verification is prior point-in-time evidence. Default invocation prints a no-effects message and returns before helper imports, FFI, reservation or listeners.

Future command, from `/Users/jd1/code/apps/outbreak`:

```sh
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -S -B web/visible/play_local.py --execute
```

The launcher refuses an occupied `web/visible/runs/local-14`, including a dangling link. It requires the actual `web/server/blackwood-candidate-attempts/visible-native-3/debug/ac_server`, its sibling `deps-signed` SDL2/hidapi frameworks, and its exact five-file `runtime-seed`. Attempts1 and2 failed and are retained; no fallback or reuse is allowed. It does not build, relink, sign, install or substitute a binary. The native executable retains its existing RPATH framework loading.

Other fixed dependencies are `web/visible/play.html`, the four `candidates/stock-combat-1/bundle/index.{html,js,wasm,data}` files from the separately reviewed stock-combat build, `/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node`, the T278 dedicated-host `web/transport/gateway.cjs` and browser adapter, and the existing vendored ws dependency. Python imports the inspected native builder's `RealOps`/`DarwinWaitid` definitions solely for original child ownership, deadline alarm and cleanup; it never calls build, stage or verifier entrypoints. That helper performs its existing Darwin FFI load only during future execution.

Future effects are confined to the new run directory and these loopback sockets:

- HTTP binds `127.0.0.1:29866`, requires Host exactly `outbreak.localhost:29866`: exact GET routes for `/web/visible/play.html` and the four bundle files under `/web/visible/candidates/stock-combat-1/bundle/`. No repository directory serving, query routes or arbitrary paths.
- WebSocket binds `127.0.0.1:29865`, with exact frontend endpoint `ws://outbreak.localhost:29865/enet`, Host `outbreak.localhost:29865` and Origin `http://outbreak.localhost:29866`. Existing subprotocol, strict cookie/credential rejection, two one-use capability hashes, session and backend limits remain.
- Native game UDP `127.0.0.1:29863`, plus inherited native information UDP `127.0.0.1:29864` and `127.0.0.1:28762`.
- The gateway's existing bounded ephemeral loopback UDP sockets targeting native port 29863.

Native arguments remain the inspected loopback, `-c2`, no-master configuration with `mandatory_auth:0` and the exact Blackwood rotation. There is no public bind or remote registration. Only inert seed/config bytes are copied into the new native working directory. Logs, hash-only gateway configuration and a cleanup result remain inside the owned run directory; raw capabilities stay in memory. Combined captured child logs are capped at 8 MiB.

After both children report actual startup, the launcher prints the public page address:

```text
http://outbreak.localhost:29866/web/visible/play.html
```

MAIN opens it manually once in its approved browser session. Reserved .localhost browser resolution is used without hosts-file/DNS configuration, alternate endpoint or numeric frontend fallback. No cookies are cleared or inspected. New-host resolution and cookie isolation still require actual observation; local6's numeric-host Cookie rejection is prior evidence only. No browser or profile is opened automatically. The first page response receives one fresh immutable `OUTBREAK_NETWORK_BOOT` with that exact WebSocket endpoint before the client script; the other gateway capability is unused. Reloading that page returns 410 rather than minting a new session. No capability, gateway configuration or credential-bearing URL is printed. Genuine network admission, join and spawn remain necessary; no Module/game/entity state is changed and no input is synthesized.

The interaction cutoff is 120 seconds from launcher entry, with startup included (normally leaving about 90 seconds for interaction). Gateway ownership closes after 110 seconds from its startup. The original whole-session deadline is 150 seconds, including cleanup. Blocking operations have bounded waits/timeouts and deadline checks; this is not a claim that Python can preempt an arbitrary stuck kernel call. Deadline uncertainty is failure, never a clean result.

Cleanup closes the owned HTTP server, asks the owned gateway to close its sockets, sends native SIGINT for its normal zero-exit shutdown, and uses the accepted helpers to observe original unreaped children. Mutating signals target only the exact original owned PID while its unreaped anchor remains valid; no group mutating signal or PID discovery is used. Any forced termination remains a failed session. Original-handle reap and independent group absence are still required. Pipes are drained/unregistered before closure; selector closure is independent. Lost ownership, nonzero exit, unfinished capture, missing gateway socket closure or other unknown cleanup produces `FAILED_OR_UNRESOLVED`, with original handles retained through the attempt. No unrelated or already-reaped PID receives a mutating signal.

`CLOSED_VISUAL_SESSION` records lifecycle cleanup only. The stored result is a pre-publication snapshot; the final printed summary and process exit must also succeed, including the check after result publication. Publication or whole-deadline uncertainty is failure. Actual living-character rendering, keyboard/mouse movement, model visibility and near-wall behavior require observation in the later released run. Engine initialization and gateway counters do not establish those facts. This limited prototype does not accept full P0/P1, authority, performance or MVP. T167 preparation is accepted; actual native/runtime effects still need their separate release, and QA remains paused.

D478 owner session:30-minute play window/1830-second whole deadline, gateway closes after1790seconds. Browser/gateway absolute session bounds are30minutes. At most two player pages use the existing distinct one-use capabilities; no fresh tokens or replay. Earlier two-minute/one-page descriptions above are historical and superseded for this owner-startup profile.


Swamp preparation is isolated in play_swamp_local.py and gateway_swamp_local.cjs, with local13/swamp-1 names. It is not the default and cannot run against this stock page. Completing its pack/build/page integration and a separate runtime review are required before execution. This commit review starts no game services.
