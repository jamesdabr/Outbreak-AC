# T279 — Dedicated-host candidate and launcher source ready

- Worker: World /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket / revision: T2791.0 / D476; source stable, writes CLOSED for MAIN review.
- Phase / contract revisions: VISIBLE_SLICE0.9; EXPERIMENTAL_TRANSPORT0.4 and EXPERIMENTAL_BROWSER_BACKEND0.3 read as context. Ticket/visible contract reread before submission, unchanged.
- Base commit and pre-existing edits: no Git operation. Preserved current native3 debug path, MAIN's existing cleanup/publication corrections, actual page lifecycle status and T277 fixed summary slots. Old candidates, runs, history and Engine-owned transport source untouched.
- Changed files: exactly `web/visible/{build.py,config.json,play.html,play_local.py,gateway_local.cjs,README.md,LOCAL_PLAYTEST.md}`, this handoff and one allowed temporary inline syntax file. No commit authorized.

## Acceptance evidence

- PASS (source/readback): builder OUTPUT, config output and fixed-output error now agree on `web/visible/candidates/first-playable-2`. Page script/locateFile and launcher exact four-file bundle table use that candidate. Build source changed only the output constant/error; 61 units, SDK7/frozen cache, flags/libraries/84 assets and occupied-output refusal retained.
- PASS (source/readback): launcher/wrapper both fix `runs/local-7`; HTTP Host requires exactly `outbreak.localhost:29866`; immutable boot endpoint is `ws://outbreak.localhost:29865/enet`; displayed page is `http://outbreak.localhost:29866/web/visible/play.html`. HTTP binds literal127.0.0.1, native3 debug/seed/arguments/info sockets remain unchanged. One-page/two-hash capability behavior, deadlines/logs/original-child cleanup and existing status/diagnostic fields retained.
- PASS (syntax/JSON only): canonical Python3.11 `-I -S -B` used stdlib `ast.parse` on both Python files and `json.loads` on config; fixed candidate/root/route/Host/bind/native consistency assertions passed. No project import or execution. Sole inline script extracted to `/private/tmp/outbreak-T279-za8wx0my.js`.
- PASS (syntax): fixed `/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node --check` on that inline file and on `web/visible/gateway_local.cjs`, both exit0/no output.
- PASS (docs): new source readiness distinguished from prior native3 verification and local6 Cookie rejection. Dedicated hostname resolution/cookie isolation/admission/spawn/input remain unverified; no numeric fallback, cookie clearing or hosts/DNS settings change.
- NOT RUN: build driver even in plan mode, SDK observation/cache copy, compiler, FFI, service/browser/runtime/network/probe/Git. No candidate/run reservation, fixture suite or new framework. QA remains paused.

## Implementation status

Implemented only the fixed successor paths/hostname and documentation. No simulations or new gameplay behavior. Depends on separately reviewed Engine T278 transport changes, MAIN's real first-playable-2 rebuild and separately released actual local-7 session. Prior rendered Blackwood evidence does not establish a living survivor or movement for this successor.

## Integration and questions

No interface or dependency added. No unresolved question. Future commands, only after MAIN's separate releases, from repository root:

```sh
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B web/visible/build.py --execute
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -S -B web/visible/play_local.py --execute
```

Exact future effects/dependencies remain documented in README.md and LOCAL_PLAYTEST.md. MAIN owns transport integration, build and actual hostname/cookie/admission/input observation; no phase acceptance follows this handoff.
