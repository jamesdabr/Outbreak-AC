# T285 — Original pistol/rifle source ready

Engine /01a1b92b-53f9-7132-aeb9-72b637ac3a90; T2851.0 / STOCK_FIRST_PROTOTYPE0.3 / D483. Changed only `source/src/main.cpp`, `source/src/rendermodel.cpp` and this new handoff. Existing source/history preserved outside the localized patch; no Git action.

## Implemented

- Browser preload now requires the seven frozen T284 additions, loads both actual original world models and PNG skins, and fails on missing files/model or fallback texture. Existing player preload remains. Immutable diagnostics retain player/skin observations and add real pistol/assault model and skin outcomes. Startup message states the selected stock model profile, omitted HUD/other weapon visuals and unbundled stock weapon audio without prematurely claiming load success.
- Browser `renderclientp()` selects `weapons/pistol/world` only for actual `GUN_PISTOL`, `weapons/assault/world` only for actual `GUN_ASSAULT`, otherwise no attachment. Existing `renderclient` creates the normal `tag_weapon` attachment; MD2's existing attachment rendering reuses the original synchronized model coordinates/animation. No new tag, decoder or transform needed. Team PNG override, T283 triangle fallback and native/offline branch remain.

Exact additional pack paths:

```text
packages/models/weapons/pistol/world/tris.md2
packages/models/weapons/pistol/world/md2.cfg
packages/models/weapons/pistol/world/skin.png
packages/models/weapons/assault/world/tris.md2
packages/models/weapons/assault/world/md2.cfg
packages/models/weapons/assault/world/skin.png
packages/models/weapons/license.txt
```

MAIN's actual build waits for accepted T28497-file pack, including its MDLCFG `md2emit` allowance. No other weapon models or audio assets are requested. Native notice/asset files untouched.

## Verification boundary

Source readback completed: model paths and six-plus-license requirement, actual load failure checks, all snapshot arguments, actual-selection mapping and existing MD2/renderclient attachment path inspected. Read the actual T283 runtime screenshot: recognizable body and floor artifacts, not verified input/movement. No floor/input/audio repair attempted.

**NOT RUN:** compiler/tests/helpers, Wasm, browser/game/services/network/FFI or gameplay. No simulation, fake weapon/ammo/pose/alive or new proof framework. Actual pistol/rifle alignment, skin, selection, firing/muzzle effects, animation and reload remain MAIN's visual/runtime checks. Input capture and stock weapon audio remain independently incomplete. No balance/protocol/gameplay/authority changes or acceptance claim. Stable source submitted; stopping.
