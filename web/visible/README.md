# Local stock-player prototype

The default build and page select `stock-combat-1`: the original AssaultCube player, pistol and assault rifle on the Blackwood greybox. Actual Chrome movement, weapon selection, firing, reload and one near-wall camera recovery sequence were observed under D490. This is a limited local prototype; survival, extraction, eight-player authority, audio integration and performance acceptance remain incomplete.

`build.py`, `config.json`, `play.html`, `play_local.py` and `gateway_local.cjs` form the current stock profile. The launcher reserves a fresh `runs/local-14`; it never overwrites an older run. It requires the separately prepared native3 debug binary/frameworks, cached Emscripten7 SDK and accepted local asset packs. No service starts without `--execute`. See LOCAL_PLAYTEST.md for the exact effects. Build/runtime outputs and copied stock media are intentionally not versioned.

Stock asset preparation is local and preserves the bundled notices. The original source assets are already in this repository. Starting from the accepted Blackwood84 pack, run the inspected `web/assets/stock-player-profile/assemble.py`, then `web/assets/stock-combat-profile/assemble.py` once into absent outputs. Each assembler refuses existing outputs; do not rerun over them. Blackwood assembly sources and its original prototype data are under `web/assets/blackwood-profile` and `web/assets/blackwood-candidate`. The pinned build configuration is machine-specific, not an installer or a portable one-command release.

Swamp is the selected expansion base. Its optional engine profile and separate `play_swamp_local.py` / `gateway_swamp_local.cjs` are **preparation only**. They require an accepted Swamp pack, matching Swamp build/page and the exact native seed. T290's first generation stopped before writing the pack; no Swamp browser runtime is accepted. The Swamp launcher rejects the stock page. Original Swamp geometry and all official assets remain unchanged. No expansion is implemented.

The three-file Swamp seed recipe is documented in T291's handoff. Its map bytes are copied locally from `packages/maps/official/ac_swamp.cgz`; that generated duplicate is not committed. The source config and provenance are retained alongside the seed recipe. No asset notice grants blanket commercial or public-build distribution rights.

Prior preparation history follows; its old run/candidate names describe historical evidence, not the current default.

---

# Visible Blackwood client

T279 / VISIBLE_SLICE0.9 / D476. Source prepared for NEW first-playable-3;
actual rebuild and local-8 session require separate MAIN release. Builds the existing C++ browser client with
`OUTBREAK_NETWORK_CLIENT` and `OUTBREAK_BLACKWOOD_CLIENT`, the approved
84-file Blackwood pack mounted at `/outbreak`, SDL2, PNG, OpenAL, Vorbis and
the existing ENet WebSocket adapter. Engine T258 owns the separate character
and camera presentation changes. Engine T278 separately owns the dedicated-host
transport update; MAIN reviews that source before rebuilding.

After MAIN inspects this source and separately releases the build, run from
the repository root:

```sh
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B web/visible/build.py --execute
```

Without `--execute`, the command only checks the local inputs and prints the
61 compile commands and one link command. Neither mode has been run for
first-playable-3 under this source-only ticket. There is no old-builder import, test framework,
preprocessor probe, dependency installation or alternate engine.

The only build destination is `web/visible/candidates/first-playable-3`.
It must be absent, including dangling symlinks. Existing candidates are never
overwritten or cleaned. The build copies `web/build/.cache` into that new
candidate, sets `EM_FROZEN_CACHE=1`, and puts compiler temporaries and Node
cache there. SDK, original cache, assets and old builders stay read-only.
Emscripten 7.0.0's frozen-cache checks reject missing cache libraries and
port-cache locks before download/build; there is no fetch fallback.

Outputs are `bundle/index.html`, `index.js`, `index.wasm`, `index.data`;
new objects/cache/temp files; and `logs/commands.txt` plus a stdout/stderr log
for each compile and link. A failed command stops the build and retains its
candidate/logs. Do not rerun into that directory; MAIN decides a new slot.
The driver does not start a server, browser, native executable or deployment.

The prospective static route is
`/web/visible/candidates/first-playable-3/bundle/index.html` on a separately
authorized local host. A successful link is only a build result. The next
acceptance is actual browser standing/moving survivor, attachments, Blackwood
environment, near-wall camera and input screenshots/playtest.

Runtime dependency: this is the network client. A living local actor needs
an authorized real server join/spawn; the build does not force alive state or
enable offline Outbreak combat. T167 preparation and native3 build verification
are prior accepted evidence; QA remains paused.
MAIN must obtain the narrow required runtime release before server/browser
playtesting. Full multiplayer, camera, gameplay and MVP acceptance remain
separate.

## Player-facing page (T261)

Use `/web/visible/play.html` through the separately authorized runtime session.
It will load the new first-playable-3 `index.js`, with `Module.locateFile`
routing both `index.wasm` and `index.data` to that candidate's `bundle/`.
The real canvas, engine loading/error hooks and recent client messages are
displayed; initialization does not claim a successful network join or spawn.

Click the canvas to focus. Its existing engine gesture handles pointer capture
and audio. Packaged bindings: WASD move, Space jump, C crouch, R reload,
primary mouse fire; mouse looks and Esc releases capture. No extra gameplay
binding, synthetic input, fake HUD or join control is added.

The authorized supervisor must install `window.OUTBREAK_NETWORK_BOOT` before
the client script starts, using exact origin `http://outbreak.localhost:29866`
and endpoint `ws://outbreak.localhost:29865/enet` for future `runs/local-8`.
This page does not create tokens, select a server or launch the runtime.
The dedicated-host transport change requires the new browser rebuild; old
candidates and runs remain immutable. Prior actual sessions rendered Blackwood
but did not establish a living character or movement; local6 identified Cookie
as the first failed admission field. The page retains actual snapshot status
and engine failure precedence. New-host resolution, cookie isolation, admission,
spawn and input remain unverified until MAIN's separately released session.
HTTP/WS bind only to 127.0.0.1; no numeric frontend fallback, cookie clearing or
hosts/DNS settings change is provided. See `LOCAL_PLAYTEST.md` for exact effects.
