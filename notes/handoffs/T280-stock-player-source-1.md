# T280 — Original player source ready

Engine /01a1b92b-53f9-7132-aeb9-72b637ac3a90; T2801.0 / STOCK_FIRST_PROTOTYPE0.1 / VISIBLE_SLICE0.11 / D479. Source-only construction against the frozen T282 interface.

Changed only `source/src/main.cpp`, `source/src/rendermodel.cpp`, `source/src/rendergl.cpp` and this new handoff. Existing browser presentation/network source was preserved outside the localized edits. No Git or asset/config/history changes.

## Concrete diff

- **Preload:** replaces custom survivor/pistol/rifle preload with `loadmodel("playermodels")` and actual texture loads for base/CLA/RVSF PNGs. Requires all six frozen stock paths. Missing files, model failure or fallback/missing textures remain fatal. Immutable model diagnostics now report the actual `playermodels` result and separate actual skin-load results, without old custom-model labels. Startup message names the stock profile without claiming preload has already happened.
- **Render:** browser-only `renderclientp()` calls the original `renderclient()` with `playermodels`, no attachment, and the negative loaded texture ID for exact default `CLA/01.png` or `RVSF/01.png` chosen by `team_base(d->team)`. Existing MD2 loader/config, model scale/translation and ordinary animation selection remain. Native/offline branch unchanged.
- **Camera:** restores `chasecam.move = -1` immediately after `reset()`, matching the native follow camera's backward movement intent. Existing independent `ENT_CAMERA`, actual player pose/yaw/pitch, collision-aware `moveplayer` steps, pitch offset and reset behavior remain. No player pose/input or join/spawn/life-state changes. Existing single local-body render gate and HUD-gun suppression retained.

## Required pack interface

Under `/outbreak/packages/models/playermodels/`:

```text
tris.md2
md2.cfg
skin.png
CLA/01.png
RVSF/01.png
license.txt
```

T282 must supply its accepted stock-player profile and the exact MDLCFG allowances for unchanged stock config before MAIN's build. The original loader's PNG fallback, `mdlscale 155`, `mdltrans 2 2 24` and default MD2 animation path are reused, not reauthored. Guns are intentionally absent from stage1.

## Verification and remaining risks

Source readback completed: checked all six file indices, real texture failure detection, truthful diagnostics, team skin selection, existing negative texture override, unchanged native/offline guards, and camera reset clearing movement followed by the new explicit backward move. No simulation or executable verification performed.

**NOT RUN:** compiler, helpers/tests, Wasm, browser, services, network, FFI, screenshots or gameplay. Actual stock skin/config/animation rendering and camera clearance are not demonstrated by source review. MAIN must build after T282 acceptance and observe standing/moving character, crouch, pitch extremes, near-wall/ceiling clipping and scope/death/spectate transitions. Obstruction can still bring the camera close to the body; visual defects need actual observation. No force-alive or final multiplayer/authority acceptance claim. Broader goal/QA/unrelated leases remain paused. Stable source submitted; stopping for MAIN review/build.
