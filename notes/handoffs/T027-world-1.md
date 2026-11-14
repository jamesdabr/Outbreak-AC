# T027 original minimal browser proof pack

- Worker: World/Match-Systems / `01a1b92c-db5c-7a10-a0e4-46e1f5a092cf`
- Ticket/revision: T027 revision 0.5 RELEASED; submitted for MAIN review, no authoritative status change
- Governing subset: D005; BROWSER_FOUNDATION/GOVERNANCE/P0 revision 0.5, product/parameters/interfaces revision 0.2 draft context. Ticket and governing revisions rechecked before submission, unchanged.
- Base: `13f0d8eea4822dee5c976661218d022be74342e3` plus D005-baseline.json dirty source. `web/assets/original` did not exist at start. All earlier stock inventory/source/worker files preserved. No game/source/config/packages/bot checkout paths were modified.
- Changed files: only new `web/assets/original/**` (generator, original glyph patterns/license, validators/tests, original pack-root, manifest, metadata inventory, verification/readability artifacts, README) and this handoff. No commit/push/branch/reset/revert or worker dispatch.

## Acceptance evidence

1. **PASS** — deterministic original RGBA8 PNG fallback, hand-authored 5×7 stroke atlas rendered at 2×, original font/browser/default-map/map configs. No stock font, raster, config, map, model or sound bytes were copied/transformed. All 94 printable non-space ASCII positions are nonblank; digits are distinct, lowercase deliberately uses capital forms. A dark-background procedural `font-preview.png` was visually inspected and reads clearly. PNGs contain full per-file MIT tEXt notices; configs contain full commented MIT notices; the map has an MIT HX_MAPINFO record and full per-map notice sidecar. `LICENSE.txt` explicitly limits the grant to these original outputs/tools, without relicensing upstream engine.
2. **PASS (structural; runtime NOT RUN)** — generated `pack-root/packages/maps/dev_outbreak_browser.cgz` (**534 bytes**, SHA-256 `c3f0226abdf143474804d9259428eb9ba641b3ac259251bdafef04962d5cb52d`) and external cfg using inspected current native v10 header/entities/SOLID/SPACE/RLE/gzip encoding. Validator decodes **4,096 cells**, **2,224 open cells**, **4 player starts** and **5 lights**, verifies MINBORD, textures/tags/entity attributes, player eye/head bounds, and through/north/south routes with native 1.1-unit radius clearance. Dimensions/collision coordinates are below. No native map was loaded or modified; engine-runtime validity remains an explicit integration check.
3. **PASS** — all D005 canonical paths exist, plus mandatory original `config/default_map_settings.cfg`. `config/font.cfg` defines default/mono/huddigits/serverquality/bargraphs/radaricons. Browser config supplies SDL-backed W/S/A/D/Space/C/R/Mouse1 mappings/settings, explicit omitted features, and only the minimal map command context. No inherited native menus/docs/autostarts/auth/services/profile include is present. Full integration names are in the manifest, README and list below.
4. **PASS** — additional original PNG aliases match proved literal startup/HUD/particle/crosshair/icon paths in main.cpp, renderhud.cpp, renderparticles.cpp and rendergl.cpp. Each manifest entry gives provenance. Dynamic inline igraph files are absent and hidden explicitly; updateigraphs safely initializes slots and skips absent graphics. Models/audio are absent, not substituted by successful stubs or claimed as final MVP features. The legacy muzzleflash.jpg literal contains original PNG data; actual SDL_image/Wasm decoding remains NOT RUN.
5. **PASS (structural; runtime NOT RUN)** — **14 targeted tests pass**, including corrupted/truncated PNG/gzip, CRC/bounds/scanline/notice checks, glyph/atlas coverage, font out-of-bounds, native RLE long-run splitting/overruns/truncation/types/border, entity encoding/blocked starts, independent radius/path checks, unexpected stock config references, hash tampering, undeclared files and symlink rejection. Two real generation runs yield identical bytes for every pack file and manifest. Existing metadata inventory consumes 34 config/packages entries with **zero missing literals**, retaining **61 conservative unresolved records** for settings/binds/map commands/runtime load; the dedicated validator checks original command structure without evaluating scripts. Actual engine/WebAssembly load is NOT RUN.
6. **PASS** — exact 35-file membership is enforced; **78,915 raw bytes**. Per-file hash/size/virtual path/original provenance/notice are in `original/manifest.json`. No native profiles, secrets, inherited media references or undeclared payloads. All four historical T018/T023 inventory fingerprints checked by verify_pack.py remain unchanged. Optional omissions and false runtime/shared-ready flags are explicit. No stock assets were served, re-licensed or distributed.

## Commands, results and identities

All commands ran locally from `/Users/jd1/code/apps/outbreak`, with existing Python **3.11.9** standard library. Exact Python/platform/zlib identity and source/tool SHA-256 values, test output, structural results and historical checks are in `web/assets/original/verification.json`.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/original/generate_pack.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/original/validate_pack.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web/assets/original/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/original/verify_pack.py
```

All exit **0**. Generator: 35 original files/78,915 bytes. Validator: structural PASS, runtime NOT RUN. Unit suite: 14 passed. Verify: two full generation runs byte-identical, all exact files/hashes/counts/config references valid, zero missing inventory literals, historical stock inventories unchanged. Manifest SHA-256: `fe1acef204e2521e96257a0492f5a09241c64852b4af2550cb08ce84f9b083ee`.

Native/WebAssembly compilation, linking, engine/CubeScript execution, browser game load, fresh input/collision observations, audio/model runtime and multiplayer: **NOT RUN**, outside T027 execution scope. Structural helper tests are not game-runtime or eight-player evidence. No server/browser/network/install process was launched.

## Integration names and final pack file list

Mount **`web/assets/original/pack-root` as `/outbreak`**. Use map identifier **`dev_outbreak_browser`**. The canonical fallback is `packages/outbreak/fallback.png`, atlas `packages/outbreak/font.png`, config `config/browser.cfg`, fonts `config/font.cfg`. Initialize the actual client/GL/texture/fallback machinery before loading fonts. The original browser config should run before the map so its isolated map-script command permissions are available. Models/audio/preloads stay explicitly omitted in the D005 map-only branch.

Every path below is relative to pack-root; all are original and separately hashed in manifest.json:

```text
LICENSE.txt
config/LICENSE.txt
config/browser.cfg
config/default_map_settings.cfg
config/font.cfg
packages/crosshairs/default.png
packages/maps/dev_outbreak_browser.cfg
packages/maps/dev_outbreak_browser.cgz
packages/maps/dev_outbreak_browser.cgz.LICENSE.txt
packages/misc/base.png
packages/misc/blood.png
packages/misc/bullethole.png
packages/misc/com.png
packages/misc/compass-base.png
packages/misc/compass-rose.png
packages/misc/ctficons.png
packages/misc/damage.png
packages/misc/explosion.png
packages/misc/htficons.png
packages/misc/icon.png
packages/misc/items.png
packages/misc/ktficons.png
packages/misc/muzzleflash.jpg
packages/misc/radaricons.png
packages/misc/scope.png
packages/misc/scorch.png
packages/misc/smoke.png
packages/misc/startscreen.png
packages/misc/teamicons.png
packages/misc/voteicons.png
packages/outbreak/fallback.png
packages/outbreak/font.png
packages/textures/outbreak/ceiling.png
packages/textures/outbreak/ground.png
packages/textures/outbreak/wall.png
```

This covers the retained loading/font/particle/core HUD literal paths and original map texture references. `packages/misc/muzzleflash.jpg` is PNG by magic despite its legacy filename; native texture.cpp uses IMG_Load. Its actual Emscripten SDL_image interpretation must be checked by integration, not inferred from the Python PNG validator. No packages/misc/notexture.jpg is included: T028 must use the canonical original PNG. Inline packages/misc/igraph files, per-weapon custom crosshairs, models and audio remain absent/optional for the map-only profile; literal default crosshair is supplied. HUD/particle symbols are neutral procedural placeholders, not final flag/equipment/weapon/blood artwork.

## Map and collision coordinates for QA

Native engine units; bounds half-open:

- World: 64×64 (factor 6). Playable ground/courtyard x=[8,56), y=[8,56): **48×48**. Everything outside is solid, including native two-cell border.
- Small structure: x=[26,38), y=[24,40): **12×16**. Two-unit walls. Interior x=[28,36), y=[26,38): **8×12**.
- Doorways: west x=[26,28), east x=[36,38), both y=[30,34), **4 units wide**.
- Floor z=0; courtyard ceiling z=12; interior/door ceiling z=8. Single-level enclosed greybox with taller surrounding ceiling, no room-over-room/roof access or town-scale claim.
- FFA anchors: **(16,32,5), yaw 90°, team 100**, and **(48,32,5), yaw 270°, team 100**. Additional team proof anchors **(16,16,5), yaw 90°, team 0**, **(48,48,5), yaw 270°, team 1**. Attr1 is yaw×10. Native forward yaw90 moves +X; yaw270 moves −X. These four anchors are not eight-player acceptance.
- Lights: (16,16,10), (48,16,10), (16,48,10), (48,48,10), (32,32,6), radius24/intensity220; ambient80. Native map flags0 select the provided external/default configs; timestamps0.
- Through path: **(16,32) → (48,32)** through both doors/interior.
- North path: **(16,32) → (16,18) → (48,18) → (48,32)**.
- South path: **(16,32) → (16,46) → (48,46) → (48,32)**.
- Collision probe: from **(22,25)** moving +X toward wall square beginning **(26,25)**. With native radius1.1 the center should stop near **x≤24.9**. Static clearance: (24.8,25) passes; (25,25) fails. Actual engine tolerance/motion integration remains unmeasured.

These names/coordinates are ready for MAIN to pass to Player/Engine/QA. No other worker was contacted directly.

## Outstanding integration work

No independent T027 step is waiting for a scope decision. MAIN still needs the actual engine to load/render/move/collide against this pack and confirm PNG legacy alias decoding. Keep native stock services/preloads/profile writes excluded as D005 specifies; no code changes were made here. If actual load reveals additional literal dependencies, release a scoped follow-up instead of preloading stock files. Models/audio and the complete eight-player survival/extraction systems remain later requirements, not waived by this map-only pack. Only MAIN reviews/accepts this ticket.
