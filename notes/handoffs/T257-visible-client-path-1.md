# T257 — Minimum path to a visible third-person browser slice

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket: T257 revision 1.0; D434 read-only inspection only.
- Changed file: this new handoff only. Shared source and prior evidence preserved; no Git inspection or action.
- Verification: source/document reads completed. All build, helper, server, browser, network and gameplay commands **UNRUN**. No implementation or simulation performed.

## Immediate source work

The approved body, weapons and Blackwood environment already exist. The shortest visible advance is to connect a living-player third-person camera and render the local body in the existing C++ browser client. No replacement engine or new asset pipeline is needed for this first slice.

| Proposed next source allowance | Concrete change |
| --- | --- |
| `source/src/clientgame.cpp` | Make the presentation-only third-person predicate usable in the network browser build. Currently `outbreakthirdperson()` depends on `outbreakactive()`, which is forced false for that build. Preserve `outbreakactive()` gameplay isolation: enabling it globally would also enable prototype gameplay paths. |
| `source/src/rendergl.cpp` | Add the living-player chase/shoulder branch in `recomputecamera()`; use actual player pose/yaw/pitch and a separate `ENT_CAMERA`. Existing `SM_FOLLOW3RD` code already demonstrates collision-aware camera movement with `moveplayer`. Reset correctly on death/spectating/edit/scoping and suppress first-person HUD weapon while in third person. |
| `source/src/rendermodel.cpp` | In `renderclients()`, draw the living local player when that third-person view is active. Present code draws remote players, but draws the local body only when dead or in the reflection case. Preserve those cases without duplicate drawing. `renderclientp()` already selects the approved survivor and pistol/rifle attachments. |

These are the minimum likely implementation files, subject to MAIN's explicit visible-slice source release. They preserve network transforms, spawn rules and gameplay authority. No camera codec/proof-component integration is necessary merely to get this view on screen. Main source locations: `clientgame.cpp:14–25`, `rendergl.cpp:503–600` and HUD gun condition near 961, `rendermodel.cpp:1060–1106`.

## Existing assets and build path

Use `web/assets/blackwood-profile/pack-root/`, mounted at `/outbreak`: the approved 84-file package includes the original network assets and Blackwood additions, with notices. Exact useful relative paths:

- `packages/models/outbreak/survivor/{tris.md3,md3.cfg,skin.png}`; equivalent `pistol/` and `rifle/` model directories. Survivor configuration already defines idle/run/attack/crouch/death animations. Keep their scoped licenses.
- `packages/maps/blackwood_greybox_v1.{cgz,cfg}` and `packages/outbreak/blackwood_greybox_v1.anchors.json`. The CFG uses original `outbreak/ground.png`, `wall.png` and `ceiling.png`; this is a greybox environment, not a finished art scene.

`source/src/main.cpp:1811+` already preloads all three models through the real model loader and fails on missing models. `source/src/browser_map_profile.h` already selects Blackwood name/revision 1 and map paths under `OUTBREAK_BLACKWOOD_CLIENT`; startup and receipt/spawn consumers must retain its genuine map identity gates. Do not force alive or bypass map receipt to obtain a screenshot.

The existing engine route is C++ → Emscripten/Wasm, SDL2/legacy GL, ENet WebSocket adapter → Node gateway → native ENet server. `web/build/network-out/` is the historical linked default-dev baseline, not a newly built Blackwood third-person game. `web/build/out/` is a separate offline candidate.

The Blackwood successor is already prepared at `web/build/blackwood/{build.py,recipe.py,config.json,verify.py}`. Its config selects the 84-file manifest, `OUTBREAK_NETWORK_CLIENT` plus `OUTBREAK_BLACKWOOD_CLIENT`, Emscripten 7.0.0 at `/private/tmp/outbreak-web-sdk`, SDL2 and the existing WebSocket adapter. Use fresh MAIN-reviewed source/control pins and exclusive candidate outputs after the visual edits; do not overwrite old builds or reuse their authorization.

Future command shapes, **UNRUN**, from repository root; placeholders require a new concrete release:

```sh
python3 -B web/build/blackwood/build.py --execute --candidate-id NEW_ID --pins ABSOLUTE_MAIN_JSON --pins-sha256 SHA256
python3 -B web/build/blackwood/verify.py --candidate-id NEW_ID --pins ABSOLUTE_MAIN_JSON --pins-sha256 SHA256
```

## Playtest route and actual hold conflict

The documented owned loopback topology is static `http://127.0.0.1:29866`, gateway `ws://127.0.0.1:29865/enet`, native UDP `127.0.0.1:29863`. This is an intended local route, **not an active playtest link**. Runtime must retain supervisor-issued immutable `OUTBREAK_NETWORK_BOOT` capability/configuration and real join/map/spawn flow. No separate manual static/server launcher or offline substitution.

`web/transport/tests/two-client/T067/supervise.py` documents the historical entrypoint and CLI (`--execute --pins ABSOLUTE_MAIN_JSON --pins-sha SHA256 --attempt NEW_ID`). Its old default-dev example is **not** a Blackwood launch instruction. `MVP/BLACKWOOD_CLIENT_FOUNDATION.md` explicitly requires accepted v4-derived admission/controller behavior, matched Blackwood native artifacts and fresh runtime pins; it rejects the older proposed v3 route. A ready-to-run Blackwood runtime command cannot honestly be supplied from the current release.

The material conflict is authorization/dependency readiness, not missing character assets: D434 leaves Player/native/QA holds unchanged. D248 and T167 preserve the native preparation human hold and unverified draft status; T149 remains READY without direct owner approval, and QA remains paused. MAIN can release the three-file visual source change independently, but must resolve the applicable runtime/native/Player gates and name the accepted v4 successor before any actual build/playtest dispatch. Do not run T167 drafts or silently transfer that work.

Once explicitly released, the first delivery should be the actual local playtest link and screenshots showing the full survivor standing and moving in Blackwood, including near-wall camera behavior and a real model load. Then add the enemy/basic-combat slice under its concrete source scope. Screenshots demonstrate visible progress; full eight-player authority/replication/combat acceptance remains outstanding.

References: `web/DEVELOPMENT.md`, `web/build/blackwood/README.md`, `MVP/BLACKWOOD_CLIENT_FOUNDATION.md`, `MVP/BLACKWOOD_ASSET_ASSEMBLY.md`, `web/assets/blackwood-profile/README.md`, D248, D434, T149 and T167. No additional audit or proof infrastructure proposed. Stopping for MAIN's source assignment.
