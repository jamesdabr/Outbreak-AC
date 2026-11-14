# T027 final pack handoff including original empty-name sky aliases

- Worker: World/Match-Systems / `01a1b92c-db5c-7a10-a0e4-46e1f5a092cf`
- Ticket/revision: T027 revision 0.5 RELEASED, D005/BROWSER_FOUNDATION/GOVERNANCE 0.5. Submitted for MAIN review; authoritative status unchanged.
- Baseline: `13f0d8eea4822dee5c976661218d022be74342e3` plus D005-baseline.json. All game/config/packages/bot checkout files, other workers' files and historical stock inventories preserved.
- This new immutable follow-up supersedes the 35-file counts/hash/test totals in T027-world-1.md after MAIN's same-ticket instruction to supply the six empty-loadsky aliases. The first handoff is preserved unchanged. Map/config/font content and collision coordinates are unchanged.
- Changed files remain exclusively new `web/assets/original/**` and own handoffs. No commits/pushes/branches/reset/revert, other worker messages, installs or services.

## Acceptance criteria

1. **PASS** — independently authored procedural PNG fallback, readable original bitmap font (94 ASCII positions; capital-form lowercase), browser/font/default-map/map configs. No stock data was copied or transformed. Per-original-file MIT notices are in every PNG tEXt chunk and config comment, with map HX_MAPINFO/sidecar and explicit manifest/license scope. Upstream engine/media licenses are untouched. Procedural dark-background font-preview.png was visually inspected; it is not an engine screenshot.
2. **PASS structurally; runtime NOT RUN** — native ACMP v10 original map and external cfg, decoded by validator into 4,096 cells, 2,224 open cells, four PLAYERSTARTs and five LIGHTs. Native header size/permutations/entity 16-byte encoding/SOLID-SPACE RLE/gzip CRC/bounds checked against source. Ground/structure/through/north/south approaches and 1.1-unit player-radius clearance verified structurally. Actual engine load/movement/collision is NOT RUN.
3. **PASS** — D005 canonical config/browser.cfg, config/font.cfg, packages/outbreak/fallback.png, packages/outbreak/font.png, packages/maps/dev_outbreak_browser.cgz/.cfg, plus original config/default_map_settings.cfg. Font names: default, mono, huddigits, serverquality, bargraphs, radaricons. Original W/S/A/D/Space/C/R/Mouse1 binds/settings omit inherited menus/docs/autostarts/auth/services. Source-level check confirms **all 13 paths in current T028 browsermain's required[] table exist** in the original pack, including the six sky faces.
4. **PASS** — original loading/HUD/particle/icon/default-crosshair aliases for inspected literal core paths. MAIN's additional six `packages/textures/skymaps/_SIDE.jpg` names are supplied as original solid-color PNGs. All images declare encoded_format=PNG in manifest. Models/audio/inline igraphs remain explicitly absent in the map-only profile; no later MVP feature acceptance is implied.
5. **PASS structurally; runtime NOT RUN** — **15 targeted tests pass**, including the new all-six-sky-alias PNG magic/CRC/dimension/manifest check. Previous malformed PNG/gzip, bounds/entity/RLE/route/font/config/hash/symlink checks pass. Two generation runs produce byte-identical pack files and manifest. Reused metadata inventory covers **40** config/packages entries with **zero missing literals** and **61 conservative unresolved records**; T027's validator checks the authored command subset without script evaluation. Actual SDL_image/Wasm engine decoding is NOT RUN.
6. **PASS** — exact **41-file / 87,897-raw-byte** membership; no secret/native profile/inherited stock-media payloads or undeclared files. Manifest records every path/virtual path/size/hash/provenance/own MIT notice. T018/T023 historical inventory hashes remain unchanged. Missing optional models/audio/inline graphics and false runtime/shared-ready fields are explicit.

## Final output and actual commands

Pack root: **`web/assets/original/pack-root`**, to mount as **`/outbreak`**. Identifier **`dev_outbreak_browser`**. Machine-readable manifest **`web/assets/original/manifest.json`**, SHA-256 **`1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3`**. Map remains **534 bytes**, SHA-256 **`c3f0226abdf143474804d9259428eb9ba641b3ac259251bdafef04962d5cb52d`**.

From `/Users/jd1/code/apps/outbreak`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/original/generate_pack.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/original/validate_pack.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/original/verify_pack.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web/assets/original/tests -v
```

All exit **0**; verify_pack also executes/captures the 15-test suite. `verification.json` records Python/platform/zlib identity, exact source/tool hashes, two-run determinism, test stderr/exit, unchanged historical inventory checks, the 13 T028 required paths and current main.cpp hash. `validation.json` records only structural validation. No native/WebAssembly compile, link, game/browser/server run, actual motion/collision or multiplayer verification was executed by this ticket. Those remain **NOT RUN**, not failed or accepted by proxy.

## Encoded PNG versus legacy JPEG suffix: source evidence

Each new face is **1,497 bytes**, SHA-256 **`fbc88d58b95ee8277ef7ddc075bb6a01637612092cf7a1fad2b17f80edf7d5bb`**, first eight bytes **89 50 4E 47 0D 0A 1A 0A**. Pixels are independently generated opaque RGBA (56,78,104), not stock sky data. PNG CRC and scanline decoding pass under all six .jpg names. The existing original muzzleflash.jpg alias also contains PNG data.

Inspected available source, read-only:

- `source/src/texture.cpp::loadskymap`, around lines 556–588: even default empty loadsky constructs `packages/textures/skymaps/_{lf,rt,ft,bk,dn,up}.jpg`; reload=true returns failure if a face remains fallback. `textureload` around lines 336–357 uses IMG_Load/IMG_Load_RW.
- `web/build/.cache/ports/sdl2_image/SDL_image-release-2.6.0/IMG.c`: supported[] around lines 54–80 includes PNG with IMG_isPNG/IMG_LoadPNG_RW. IMG_Load around lines 178–205 derives the extension as a type hint. IMG_LoadTyped_RW around lines 275–289 calls each available magic detector; suffix comparison is only for formats without a detector. The PNG .is branch therefore does not require the filename suffix to say PNG. Emscripten preloaded-image fast paths may run first; if absent, this detector loop is the fallback.
- `.../IMG_png.c::IMG_isPNG`, around lines 203–225: reads 89 'P' 'N' 'G' and restores stream position. Compile-time PNG support is still required.
- `/private/tmp/outbreak-web-sdk/upstream/emscripten/tools/ports/sdl2_image.py`, around lines 64–75: selected png format defines LOAD_PNG and enables USE_LIBPNG. No JPEG decoder is needed for these actual PNG bytes in the inspected magic-detector path.

Inspected IMG.c SHA-256: **`f09b302f10e76cc14ce15167e7745f3bbdbbaa705e08692cf42558d0727b2968`**. IMG_png.c SHA-256: **`fa85dca99eb2d2158f05bd934333330a507d440eef0832b9e3239f7ccf1a2318`**. These are source-inspection evidence, not a claim that the forthcoming PNG-only browser link actually decoded the assets. All seven PNG-under-.jpg aliases still require actual linked SDL_image/browser verification. No main/texture/SDL/cache source was modified or executed here.

## Complete final 41-file pack list

All paths relative to pack-root; all per-file hashes are in manifest.json:

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
packages/textures/skymaps/_bk.jpg
packages/textures/skymaps/_dn.jpg
packages/textures/skymaps/_ft.jpg
packages/textures/skymaps/_lf.jpg
packages/textures/skymaps/_rt.jpg
packages/textures/skymaps/_up.jpg
```

## Exact world/collision coordinates for Player/QA integration

Native engine units, half-open bounds; these are structural expectations, not observed engine physics:

- 64×64 world, factor6. Courtyard x=[8,56), y=[8,56), 48×48; outside solid, native two-cell border retained.
- Structure x=[26,38), y=[24,40), 12×16; two-unit walls. Interior x=[28,36), y=[26,38), 8×12.
- West/east doors x=[26,28) / [36,38), both y=[30,34), four units wide.
- Ground z=0; tall surrounding ceiling z=12; interior/door ceiling z=8. No room-over-room, roof traversal, town-scale or eight-player spawn claim.
- FFA starts (16,32,5), yaw90/team100; (48,32,5), yaw270/team100. Team proof anchors (16,16,5), yaw90/team0; (48,48,5), yaw270/team1. Attr1 stores yaw×10; native forward yaw90 is +X, yaw270 is −X.
- Through route (16,32) → (48,32). North route (16,32) → (16,18) → (48,18) → (48,32). South route (16,32) → (16,46) → (48,46) → (48,32). All pass static quarter-unit sampling with radius1.1.
- **Real-wall test target: move +X from (22,25) toward solid wall beginning at (26,25). Expected actor-center limit x≈24.9 for radius1.1. (24.8,25) is structurally clear; (25,25) is blocked.** Actual collision tolerance must be measured in the game.

## Remaining work and scope

No independent T027 generation/structural step is blocked. MAIN can pass these final names/coordinates to Engine/Player/QA. Actual engine load/render/input/collision and all PNG alias decoding remain integration prerequisites. Models/audio/final HUD art and full eight-player survival/extraction features remain explicitly incomplete. No stock file distribution or external service access occurred. Only MAIN accepts this ticket or authorizes further integration changes.
