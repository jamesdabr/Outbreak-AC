# T289 — Truthful Swamp browser profile

Engine /01a1b92b-53f9-7132-aeb9-72b637ac3a90; T2891.0 / STOCK_FIRST_PROTOTYPE0.6 / D491. Changed only `source/src/browser_map_profile.h`, `source/src/main.cpp` and this new handoff. Existing source/data/history preserved outside the localized edits; no Git action.

## Implemented

- Fixed `OUTBREAK_SWAMP_CLIENT` returns `ac_swamp`, revision179, and `packages/maps/official/ac_swamp.cgz`. Compile guards reject simultaneous Blackwood/Swamp flags and Swamp without Emscripten/network client or with STANDALONE. Blackwood/default-dev identities and paths remain unchanged.
- Only Swamp's private `cfg_path()` returns a null pointer (`0`, keeping the include-independent header self-contained): its original CGZ executes automatic embedded config. Startup now checks external CFG separately when non-null. Common configs/font/fallback/map/empty-sky placeholders remain mandatory; no general optional-file loop or fallback added.
- Startup logs the selected fixed map name/revision and states actual load and remote receipt/spawn are required. Existing stock player/gun preload validation and diagnostics remain unchanged.

All existing name/revision/loaded-bytes/advertised-bytes/mode/receipt/spawn predicates are untouched. No parser, actor state, original geometry/config, native seed, weapon behavior, asset/dependency or runtime-selector changes. Actual embedded Nightball sky/resources still come from T290's exact pack through existing loaders.

## Evidence and remaining work

Read accepted T288 closure: original CGZ23987 bytes, revision179, automatic config and no external ac_swamp CFG. Reviewed main startup and the sole `cfg_path()` call site. Source readback confirms only fixed identity branches/guards, optional external-CFG handling and truthful startup message changed; ticket and contract pins rechecked.

**NOT RUN:** compiler, helpers/tests, browser/game/runtime, services/network, FFI or Git. No simulation or new proof framework. MAIN's build waits for accepted T290346-file pack and matching T291 seed/launcher. Real Swamp load, original textures/sky/models/audio and genuine join/spawn/player/guns require actual runtime observation. This is the original-map baseline, not expansion or final MVP acceptance. Stable source submitted; stopping.
