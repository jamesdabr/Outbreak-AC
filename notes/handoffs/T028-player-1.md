# T028 minimal browser startup and diagnostics — source/object handoff

- Worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T028 0.5 RELEASED; submitted for MAIN review, not self-accepted
- Governing revisions: AGENTS; BROWSER_FOUNDATION 0.5; GOVERNANCE 0.5; P0 0.5 prerequisite subset; D005. Draft gameplay contracts remain unimplemented context.
- Base: `13f0d8eea4822dee5c976661218d022be74342e3` plus D005's pinned dirty source. Initial main.cpp matched its D005 hash exactly. Existing T017 and protected combat work were retained.
- Changed source: `source/src/main.cpp` only. Own new notes: this handoff and `notes/questions/T028-player-empty-sky-aliases.md`.
- Final main.cpp SHA-256: `f773210a519ec6567f0fd3bb9c71d71df6ef742da0e3d17f2be1076de2b06adf`.
- Evidence/patch: `/private/tmp/outbreak-t028-player/`, especially `T028.patch`, `status-before.txt`, `submission.json`, `contracts-start.json`, `wasm-result.json` and `required-assets.json`.
- No commits/branches/push/reset/revert, other-worker edits, SDK installation, dependency acquisition, game/service launch or public hosting performed.

## Acceptance evidence

| Criterion | Result | Evidence and limits |
| --- | --- | --- |
| 1. Isolated original browser startup/native preservation | PASS — source/helper/object; runtime NOT RUN | Browser entry changes cwd to virtual `/outbreak`, checks explicit original files and bypasses desktop arguments/profile/config/service/menu bundles. Browser quit skips inherited saves/hooks. Native source after removing only `__EMSCRIPTEN__` conditionals has identical tokens to D005, checked with `/usr/bin/unifdef`. Extracted startup fixture covers cwd, required files and config/font/texture/map failure reporting. Real pack startup is not exercised. |
| 2. Actual engine world/render/player/local path retained | PASS — source/object; real movement/map/render NOT RUN | Retains `empty_world`, GL/player/collision path, explicit real `load_world`, real `localconnect`, `serverslice`, `updateworld`, renderer and native input bindings. Bot mode is excluded by selecting ordinary DM; audio/HUD weapon preloads are omitted and logged explicitly. Entry click uses existing `tryrespawn()` through normal server validation, never a shot. This is offline local protocol, not standalone multiplayer. |
| 3. Exact read-only real-event diagnostics | PASS — source/extracted JS/C++ tests; real-browser observation NOT RUN | Schema is exactly D005. Loading begins at browser entry; running requires a returned `gl_drawframe`, positive `maploaded`, canonical actual map name. Render count increments only after each actual frame draw returns (including a requested screenshot redraw). Publishes current real position/map/lock/frame counters; captures engine fatal errors and browser error/rejection events. Immutable snapshots/arrays, no command/actions. Node fake-window publisher and extracted frame fixtures pass. |
| 4. Input/clock/cancel/persistence | PASS — source/helper; integrated lifecycle NOT RUN | T017 cap/reset and input release/reacquisition remain; fixtures pass through blur/visibility/Escape/capture/error/stop paths. `quit`/`cleanup` cancel/unregister before resource cleanup; fatal publishes error first and stop preserves error. Browser quit returns with loop stopped and performs no desktop onQuit/settings/history/entropy/xmap saves. No unload persistence/audio promise. |
| 5. Native release/debug + actual Wasm release/debug | PASS | Native syntax exits 0, empty diagnostics. Actual Emscripten 7.0.0 release/debug main.cpp objects both exit 0 and have Wasm magic; source hash before/after equals final hash. Commands/config came from T026's ready successful object probe; own outputs/temp/Node cache only, existing compiler cache frozen. See `wasm-result.json`. This is real target object compilation, not a linked game. |
| 6. Startup inventory/required paths/remaining blockers | PASS — documented below; link/runtime NOT RUN | Exact call boundaries and required canonical/proved paths listed below. Six original sky aliases are currently missing and explicitly raised in the new question. No inherited scripts were executed to discover dependencies. Full-client linkage/GL behavior/service integration remain outside this evidence. |

All eight protected combat hashes still match D003 exactly (`protected-hashes.json`). No balance/protocol/camera/revive feature was added. Native/standalone server clocks were not edited.

## Implemented startup and exclusions

New browser entry `browsermain` is selected only under `__EMSCRIPTEN__`; native main is otherwise unchanged. Direct retained startup calls, in order:

1. Publish loading observation; `chdir("/outbreak")`; `getfilesize` required-file checks; `setlocale`; `pushscontext`; memory entropy initialization; disable screenshot entropy bootstrap.
2. `SDL_Init(TIMER|VIDEO)`, `enet_initialize` for retained local protocol, `initclient`; select `GMODE_DEATHMATCH`/nextmode and initialize existing gun/crosshair names.
3. `execfile("config/browser.cfg")`; disable audio, HUD gun, autodownload/autogetmap; windowed browser sizing; log omitted bots/model preloads/audio.
4. `initserver(false)`; allocate one inert `__outbreak_map_lifecycle` container; `empty_world(7,true)`; SDL video subsystem; `setupscreen`; `gl_checkextensions`; `gl_init`.
5. Load original fallback into notexture/noworldtexture and reuse it as startscreen; `updateigraphs`; execute original font config and require `mono`/`default`; `loadingscreen`; `particleinit` (original literal aliases).
6. Explicit actual `load_world("dev_outbreak_browser")` with nonzero result treated as visible failure; real `localconnect`; `resetcamera`; unlocked input; `browserstart`; yielding callback registration.

The inert container is required because `clientgame.cpp::startmap` unconditionally calls `menureset(downloaddemomenu)`, which dereferences its argument. It has no inherited menu contents, service callbacks or player-facing download UI. No native menu tree/config is loaded. This maintains the retained map-loader invariant without editing another worker's source.

`entropy_init` is retained because the real local handshake/frame entropy functions dereference its allocated memory pool. Its existing optional `private/entropy.dat` read is relative to the isolated virtual `/outbreak` tree; no host profile/home/package path is configured or mounted and browser quit never saves it. This does not initialize production auth/accounts.

Excluded from browser startup: `rndmapname`; desktop argument/scl parsing and dedicated/URI/demo/initscript flows; `sethomedir`, profile templates, `initclientlog` rotation; native SDL version/platform-icon/mac warp setup; all native autostarts; stock fallback and inherited font bundles; audio initialization/default-sound registration/sounds configs; score/server/search/serverinfo/kick/ban/force-team/admin/reference/apply/download menu setup; inherited scontext/keymap/mapmodelattributes/menus/scripts/prefabs/securemaps/admin/servers/pcksources/authkeys/authprivate configs; cert directory/history/autodownload setup/xmaps; compressed resdata; saved/defaults/autoexec and afterinit/autoexec hooks; player/HUD gun/entity model preloads; docs; startup force-grab and native log-line argument setup.

Browser frames retain actual world/server/audio-manager/ray-table/render order. Audio manager remains naturally nosound without backend initialization. Browser frames skip `pollautodownloadresponse` and `afterauth`/legacy URI continuation. Browser normal quit skips onQuit, `writeinitcfg`, `writeservercfg`, `writepcksourcecfg`, delete/writecfg, `savehistory`, model attribute/entropy/xmap writes; it retains client/audio/server/SDL cleanup after cancellation. Native startup/frame/quit behavior remains unchanged.

## Required generated files and pack closure

The T027 original pack root must be mounted at `/outbreak`. Required relative paths checked early:

- `config/browser.cfg`, `config/font.cfg`, `config/default_map_settings.cfg`
- `packages/outbreak/fallback.png`, `packages/outbreak/font.png`
- `packages/maps/dev_outbreak_browser.cgz`, `packages/maps/dev_outbreak_browser.cfg`
- `packages/textures/skymaps/_lf.jpg`, `_rt.jpg`, `_ft.jpg`, `_bk.jpg`, `_dn.jpg`, `_up.jpg` (each full path under that directory)

The first seven are present in the generated pack at submission. **The six sky aliases are absent** (`required-assets.json`). `texture.cpp::loadskymap(true)` unconditionally requests them with the default empty sky name, and worldio turns missing faces into load warnings. The new question provides exact source evidence and the existing T027 original-alias route. This is a predicted source/asset closure issue, not an observed runtime test result. Main cannot author those assets or change texture.cpp.

Retained transitive calls also need T027's inventoried original particle/HUD/crosshair aliases and original world textures. Particle literals include `packages/misc/base.png`, `smoke.png`, `explosion.png`, `bullethole.png`, `blood.png`, `scorch.png`, `muzzleflash.jpg`; map texture slots reference `packages/textures/outbreak/ceiling.png`, `ground.png`, `wall.png`. The generated pack manifest remains the owner of complete alias/provenance/format data. Main does not copy stock media or execute inherited configs to close dependencies.

## Actual verification and reproduction

Environment: Darwin arm64; Apple clang 17.0.0; T026 pinned Emscripten 7.0.0/compiler `777e6e5db7b4990bcaeb1b9998ed642cc84e6629`. From repository root:

```sh
clang++ -fsyntax-only -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers -Isource/xcode/Frameworks/SDL2_image.framework/Headers -Fsource/xcode/Frameworks -idirafter source/include source/src/main.cpp
clang++ -D_DEBUG -fsyntax-only -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers -Isource/xcode/Frameworks/SDL2_image.framework/Headers -Fsource/xcode/Frameworks -idirafter source/include source/src/main.cpp
python3 /private/tmp/outbreak-t028-player/verify.py
clang++ -std=c++11 /private/tmp/outbreak-t028-player/startup-helper.cpp -o /private/tmp/outbreak-t028-player/startup-helper
/private/tmp/outbreak-t028-player/startup-helper
clang++ -std=c++11 -D__EMSCRIPTEN__ /private/tmp/outbreak-t028-player/frame-helper.cpp -o /private/tmp/outbreak-t028-player/frame-helper
/private/tmp/outbreak-t028-player/frame-helper
clang++ -std=c++11 /private/tmp/outbreak-t028-player/lifecycle-helper.cpp -o /private/tmp/outbreak-t028-player/lifecycle-helper
/private/tmp/outbreak-t028-player/lifecycle-helper
node /private/tmp/outbreak-t028-player/diagnostics-test.js
python3 /private/tmp/outbreak-t028-player/wasm-check.py
git diff --check -- source/src/main.cpp
```

All final commands/checks exit 0. Native/helper compiler logs are empty. A missing fixture-only `string` typedef was corrected during startup-fixture preparation; actual native/Wasm source checks did not have that error. Extracted helpers substitute engine/platform/window APIs and execute no engine script, real map or browser game. They verify startup order and required-path/config/font/decode/map failure cases, real-frame source cap/reset/cancellation and returned-draw accounting, lifecycle release/reacquisition, exact diagnostic keys/frozen arrays/error retention.

`wasm-check.py` consumes T026's provided ready result/config and validates its D005 authorization identity. Its exact subprocess command is `/private/tmp/outbreak-web-sdk/upstream/emscripten/em++ --target=wasm32-unknown-emscripten -std=gnu++11 -fsigned-char -sUSE_SDL=2 -sUSE_SDL_IMAGE=2 -sUSE_ZLIB=1 -sUSE_VORBIS=1 -sLEGACY_GL_EMULATION=1`, with `-O2` or `-O0 -g -D_DEBUG`, repository source/bot/enet includes, `-c source/src/main.cpp`, and own release/debug output paths. `wasm-result.json` records full absolute argv/environment/hashes. `EM_FROZEN_CACHE=1` prevents cache population; temporary/Node outputs stay under T028's temp root. Both object files have Wasm magic and stable source hashes. The only target diagnostic is the expected warning that `LEGACY_GL_EMULATION` is a link setting ignored during object compilation. No renderer compatibility conclusion follows from it.

## Integration and remaining work

Only MAIN accepts T028. Source and target-object work is submitted; there is **no linked full client, actual Chromium game, real map rendering/collision/input test or multiplayer proof** in this handoff. There is no lead-specified integrated artifact available to test. Remaining work includes six original sky aliases; full-client object/link closure; T029 service/single-thread/local-auth integration; actual GL compatibility; deployed virtual-pack loading and runtime QA. Model/HUD weapon/local-character preloads and audio backend remain explicitly omitted, not P1/MVP passes. Storage persistence and unload guarantees are not implemented.

D005 diagnostics are developer observations only, not the deferred LLM tester API. Mandatory integrated checks remain pointer acquisition/denial, Escape/reentry, held controls across blur/hide/resume, raw versus bounded timing, real movement/collision, continuous returned game draws, resize/errors, and clean cancellation without post-cleanup callbacks. A separate server/network gate remains required.

Before submission the ticket/contracts were re-read and hash-verified unchanged at revision 0.5. Historical handoffs/questions and other-worker source were not edited. Protected combat hashes remain pinned. The sole open T028 question is `T028-player-empty-sky-aliases.md`; independent authorized source/compile/helper work is complete.
