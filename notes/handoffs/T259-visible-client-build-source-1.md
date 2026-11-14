# T259 — Visible client build source ready

- Worker: World & Match Systems; T2591.0/D435, VISIBLE_SLICE0.1.
- NEW files only: web/visible/build.py,config.json,README.md and this handoff. Existing builders,SDK,cache,assets,candidates and Engine's presentation files unchanged by World. No Git operation.
- Source stable; writes CLOSED. MAIN reports T258 received under D436 and will separately run the build. World stops without executing it.

Future command from repository root:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B web/visible/build.py --execute
```

Straightforward61compile+1link commands from existing browser profile:53C++/7ENetC/WebSocket adapter,NETWORK_CLIENT+BLACKWOOD_CLIENT,approved84-file Blackwood pack,same SDL/PNG/OpenAL/Vorbis/link flags and existing shell. Default invocation is read-only command display. No old builder import,test framework,proof pipeline or tool probe.

Future writes: ONLY fresh web/visible/candidates/first-playable-1 and its required parent,with objects,bundle,logs,private cloned cache,Node cache and temp files. EM_FROZEN_CACHE=1; installed Emscripten7.0.0 rejects missing cache libraries/port locks before fetch. Occupied/dangling candidate refuses; failed build preserves logs/partial output. Outputs bundle/index.html,index.js,index.wasm,index.data; per-command stdout/stderr logs and commands.txt. No server/browser/deploy starts.

Verification: complete source/config text inspected against existing commands; approved pack manifest SHA8c4f7eef5f0deafb06bec60d62be529a684a30d56bbdc6dc3e5f38dd21c69e60 confirmed; named cached port markers/libraries present; candidate absent. Driver/plan/build/compiler/tests/runtime NOT RUN. No cache/output scaffold created.

Source SHA256: build.py1d71fc5151b643fe0199aa48ac743844aefbb7edd5b79ed73a4f31158293b75a; config.json610399461cb62aed105dceec7124688c6d2f64032dfa6e5c28ae564e24948ab3; README.mda2738c8bb703cd49dd926a75442dafa3ef0602079fca3307f6f41c4e9534943f.

Concrete runtime dependency: main.cpp initializes network player CS_SPECTATE/clientnum-1 and deliberately omits localconnect; genuine remote join/spawn is required for a living local survivor. No forced-alive/offline combat workaround. Native/T167/QA human holds remain; MAIN must obtain the narrow runtime release before server/browser playtest. Build success alone will not establish visible rendering or gameplay acceptance.
