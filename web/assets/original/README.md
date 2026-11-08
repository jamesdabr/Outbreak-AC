# Original offline browser proof pack (T027)

This is independently authored procedural test content for D005's native-engine browser rendering proof. No stock map, image, font, model, audio or configuration file was copied or transformed. `glyphs.py` contains hand-authored stroke patterns; the remaining pixels and geometry are simple mathematical constructions. All original files have the permissive notice in `LICENSE.txt`; this notice does not relicense upstream engine code or stock media.

Generate and verify from the repository root with existing Python 3 standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/original/generate_pack.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/original/validate_pack.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/original/verify_pack.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web/assets/original/tests -v
```

The generator writes **41 declared files / 87,897 raw bytes** to `pack-root` and a deterministic `manifest.json` alongside it. It refuses symlinks and undeclared existing pack files rather than cleaning a directory. The validator checks all file hashes, exact membership, PNG CRC/scanlines/notices, font glyph coverage/rectangles, config command/reference allowlists, native header/entities/RLE, border and start clearance, and three approach routes with the native 1.1-unit player radius. Tests include malformed/truncated/oversized data and negative collision/path/reference cases. These are source-backed structural checks, **not an actual engine load**.

`verify_pack.py` generates twice and compares every output byte and manifest; records 15 tests, tool/source identities, Python/zlib identity and unchanged historical T018/T023 inventory hashes in `verification.json`. It also feeds the config/packages subset through the accepted metadata inventory, producing `inventory-profile.json` and `inventory.json`. The conservative parser leaves original bind/settings/map-reset commands unresolved (61 records, zero missing literals); the dedicated T027 validator checks the authored subset without evaluating CubeScript. `shared_build_ready=false` and `runtime_verified=false` remain explicit until real integration. `validation.json` describes only the structural result. None of these scripts starts an engine, browser, server, network request or installer.

Mount **only `pack-root` at `/outbreak`**, never the checkout or its stock assets. The canonical integration paths are:

| Role | Pack-relative path / identifier |
| --- | --- |
| Browser settings/bindings | `config/browser.cfg` |
| Font definitions | `config/font.cfg` |
| Mandatory native external-map defaults | `config/default_map_settings.cfg` |
| Fallback | `packages/outbreak/fallback.png` |
| Font atlas | `packages/outbreak/font.png` |
| Map identifier | `dev_outbreak_browser` |
| Native map | `packages/maps/dev_outbreak_browser.cgz` |
| External map config | `packages/maps/dev_outbreak_browser.cfg` |

The engine must initialize its client/GL/texture loader and canonical fallback before font loading. `config/font.cfg` defines **default, mono, huddigits, serverquality, bargraphs, radaricons**, with ASCII 33–126, 14×20 metrics, and a 256×128 RGBA atlas. Lowercase deliberately uses capital-form strokes. Spaces use the font's default advance. `font-preview.png` is a separate procedural readability preview on a dark background, not an engine screenshot or a pack dependency. It was visually inspected; white glyphs on transparent atlas pixels naturally disappear against a white image-viewer background.

`config/browser.cfg` contains explicit SDL key maps and binds: W/S/A/D forward/backward/left/right, Space jump, C crouch, R reload, Mouse1 attack. Key codes are derived from the current `source/include/SDL_keycode.h` and the native Mouse1 value, not copied keymap data. Browser pointer acquisition/Escape/focus handling belongs to T028. The profile sets fov 90, sensitivity 3, disables HUD weapon rendering/audio/music/shadows/water reflection/autodownload, hides radar/team/inline graphics, and restricts the map-script context to the six exact commands used by the authored map configs. There are no inherited includes, menus, docs, autostarts, auth, service, host-profile or public connection scripts. This minimal developer profile is not the final MVP feature set.

Additional original aliases satisfy literal core loads inspected in `renderparticles.cpp::particleinit`, `renderhud.cpp`, `rendergl.cpp::renderaboveheadicon` and native non-Apple startup: loading screen, seven particle images, neutral HUD/icon grids, window icon, voice icon, and default crosshair. Each PNG includes the complete MIT notice in a tEXt chunk, each config contains it as comments, and the map has an MIT HX_MAPINFO plus a full per-file license sidecar. The legacy `packages/misc/muzzleflash.jpg` and the six `packages/textures/skymaps/_{lf,rt,ft,bk,dn,up}.jpg` files **contain PNG bytes**: the literal filename is retained while procedural output stays PNG, and source uses `IMG_Load`. Source inspection of the available SDL_image 2.6.0 `IMG.c` shows that `IMG_Load` passes the suffix as a hint, while `IMG_LoadTyped_RW` chooses formats with available magic detectors regardless of the suffix. `IMG_png.c::IMG_isPNG` checks 89 50 4E 47 and restores stream position. The Emscripten port recipe defines `LOAD_PNG` and enables libpng when PNG is selected; these aliases do not require JPEG decoding in that inspected path. Actual linked SDL_image/Wasm decode of all seven aliases still requires engine integration verification. Source hashes are recorded in verification.json. These are neutral placeholders, not stock logos or final weapon/blood/flag artwork.

The six sky aliases are original solid blue RGBA PNGs. `texture.cpp::loadskymap(true)` constructs these exact `_side.jpg` names even while `loadsky` retains its default empty name, so they satisfy T028's required-file list without adding an inherited skybox name or script. The validator confirms PNG magic/CRC/pixels under every legacy suffix; no stock sky pixels were used.

No model/audio payloads are included. The map has no model/item/sound entities. Native player/weapon/entity model preloads and audio must remain omitted explicitly in the D005 map-only branch; they are not satisfied by the pack. `updateigraphs()` may enumerate an absent/empty `packages/misc/igraph` directory: source initializes its hardcoded slots and safely skips null graphics; `hideigraphs=1` makes this omission explicit. No dynamic inline graphic names are silently supplied from stock. Per-weapon crosshair selection may use the provided literal default fallback. The canonical native fallback JPEG is not bundled: T028 must use D005's `packages/outbreak/fallback.png` in its browser branch.

## Native format and coordinates

The map is **ACMP version 10**, size factor 6 (64×64 unit grid). Format source: `world.h::header`, `entity.h::persistent_entity`, `worldio.cpp::save_world/rlencodecubes/rldecodecubes/load_world`, `protocol.cpp::putuint/getuint`, `tools.cpp::calcmapdims`, `clientgame.cpp::gotoplayerstart`, and `physics.cpp` movement conventions. Nothing is saved by running the engine.

Header is 980 bytes plus one persistent HX_MAPINFO record. Texture permutations are complete 0–255 sequences; map revision is 1, ambient 80, water level −10000, flags 0 (external config), timestamps zero. Entities use little-endian `4h,4B,h,b,B` (16 bytes): four PLAYERSTARTs followed by five LIGHTs. Geometry is row-major y then x. SOLID writes type/wall/vdelta; SPACE writes type/floor/ceil/wall/floor-texture/ceiling-texture/vdelta/upper/tag. Repeat opcode 255 writes a count of following copies of the previous cell, split at 255. Gzip mtime is zero and its OS byte is explicitly 255. No room-over-room or geometry conversion exists.

All bounds below are half-open in native engine units:

- World 64×64. Playable courtyard **x=[8,56), y=[8,56)**, or **48×48** units; outside is solid, including the native two-cell MINBORD.
- Structure **x=[26,38), y=[24,40)**, or **12×16** units. Walls are two units thick; interior **x=[28,36), y=[26,38)**, or **8×12** units.
- West and east doorways occupy **x=[26,28)** and **x=[36,38)** respectively at **y=[30,34)**, each **4 units wide**.
- Ground z=0. Tall courtyard ceiling z=12; interior/door ceiling z=8. This is a single-level enclosed greybox with a higher surrounding ceiling; there is no roof traversal, open-sky/full-town or final Blackwood-scale claim.
- FFA starts: **(16,32,5), yaw 90°, team 100** and **(48,32,5), yaw 270°, team 100**. Team proof anchors: **(16,16,5), yaw 90°, team 0** and **(48,48,5), yaw 270°, team 1**. Source encodes yaw×10 in attr1. Native forward yaw 90° moves +X, 270° moves −X. These four anchors are a proof fixture, not an eight-player match acceptance claim.
- Lights at (16,16,10), (48,16,10), (16,48,10), (48,48,10), (32,32,6); radius 24, intensity 220.

QA approaches, checked by quarter-unit samples against solid square cells with a circular 1.1-unit radius:

1. Through: (16,32) → (48,32), through both doorways and interior.
2. North: (16,32) → (16,18) → (48,18) → (48,32).
3. South: (16,32) → (16,46) → (48,46) → (48,32).

Collision target: structure wall starts at **x=26, y=25**. From a clear point **(22,25)** moving +X, the actor center should stop around **x≤24.9** for radius 1.1; (24.8,25) passes the static clearance check and (25,25) fails. Actual engine tolerance/integration remains unmeasured. Ground contact, motion, collision, texture decoding and render/input diagnostics must be verified in the actual game by the assigned integration/QA workers before any runtime acceptance.
