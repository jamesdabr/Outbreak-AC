# T288 — Original Swamp integration closure

Recommend a new **Swamp-specific pack/profile and fixed native seed**, retaining the original CGZ bytes and all authored entities/media. This is the next stock-map baseline, not expansion. No source/assets changed or runtime started; writes CLOSED for MAIN.

- Worker: World /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket: T2881.1 / STOCK_FIRST_PROTOTYPE0.5 / D488; updated pin explicitly received from MAIN; reread before submission.
- Changed files: only own new `notes/analysis/T288-*` inspection scripts/JSON and this handoff. No Git/commit; existing work preserved.

## Exact original map and resource closure

`packages/maps/official/ac_swamp.cgz`: **23,987 bytes**, SHA256 `acb8d878f90fb4dfa1a53aa69b4500282bace127fe426a658f348a70a4fde9aa`; format10, **revision179**, title “ac_swamp by Undead & ExodusS”, factor8/256×256, header flags513. Embedded map notice is `cc-by-nc-sa-3.0`, comment “edited for AssaultCube (thanks original authors)”. Original waterlevel −60 is stored in tenths. Keep the bytes, name and revision consistent across native advertisement, browser loaded-map checks, receipt and spawn gates.

The automatic-config flag is set. `worldio.cpp:1098–1110` therefore skips default/external map CFG execution and executes the embedded config. Neither optional `packages/maps/ac_swamp.cfg` nor `packages/maps/official/ac_swamp.cfg` exists. Simply adding a remapped external CFG will NOT override this embedded configuration.

| Original content | Required closure |
|---|---|
| World textures | 64 configured slots, 61 referenced by native texuse semantics; retain all64/order. Paths are listed exactly in inspection JSON, including slot5's `../models/mapmodels/ratboy/toca_cardboardbox_reskin/skin.jpg`. |
| Sky | `packages/textures/skymaps/socksky/nightball_{lf,rt,ft,bk,dn,up}.jpg`; retain original six faces, fog1024/black fog colour. |
| Models | **282 entities using every slot0–54**. All55 configurations are MD3, resolving to **51 unique geometry files, 55 CFGs and 45 unique skins** (44JPEG/onePNG). Shared relative geometry/skins must retain native paths. All resolved files exist; exact slot/path/CFG text is in resource JSON. No `mdlattribute requires` references were found in these55 configs. |
| Ambient sound | **53 entities**, all nine configured tracks used: `packages/audio/ambience/{night_crickets,t_electricbuzz,t_gastank,t_hum03,t_night01,t_vents,t_waterpipe01,t_waterpipe02,water}.ogg`. All exist; current build already requests Vorbis. |
| Remaining entities | Preserve all656, including35 player starts,126 lights,113CLIP,12PLCLIP,8ladders, flags/items. Do not remove scenery/clips/sounds to make loading succeed. |

The above media union is230 distinct source files before map/notices/basepack. It is a source inventory, NOT a frozen final pack count. Carry accepted stock-combat97 as the base; preserve player/weapon notices and existing content. Source model loading uses own/parent fallback for default tris/skin and explicit relative paths for configured MD3s. MD3 configs include alpha tests, culling and the ceiling-fan mapmodel animation; preserve them.

## PNG-only alternatives and next source changes

**Supported source-level option for MAIN:** generate lossless, native-resolution PNG bytes at the **original virtual filenames**, with explicit manifest encoding/source hash/pixel provenance. `texture.cpp` uses IMG_Load/IMG_Load_RW; installed cached SDL_image2.6.0 `IMG.c:275–289` dispatches signature detectors irrespective of extension for formats with detectors, including PNG. Thus a `.jpg` virtual name need not contain JPEG encoding. This can preserve exact Swamp CGZ, texture slots, sky lookup and model CFGs. It is source-supported, **not yet tested in a Swamp browser build**. Original repository JPEGs remain unchanged; no decoder dependency is selected/added by this note.

Alternative: derive PNG paths and explicitly remap all world/model/sky references. This needs an approved browser-only post-embedded-config hook or a separately identified derived map/header, because the external CFG is skipped; `loadskymap` itself hardcodes `.jpg`. Do not silently mutate original CGZ bytes, fake advertised byte counts/revision or substitute fallback sky. Adding JPEG support is a third separately justified dependency/build choice, not part of this lease.

Concrete next bounded implementation split:

1. New `web/assets/swamp-profile/{pack-root,manifest.json,README.md,assemble.py}` from stock-combat97; add unchanged `packages/maps/official/ac_swamp.cgz`, original resolved media and notices. Decide the image-encoding option explicitly. Keep original media paths and all source/derived attribution; pin final membership only after dedicated assembly closure.
2. `browser_map_profile.h`: fixed truthful `ac_swamp`, revision179, official CGZ path; retain existing name/revision/size/mode/receipt/spawn checks. Browser startup currently requires a nonexistent per-map CFG and empty-sky placeholders: replace those **Swamp-specific requirements**, not the checks for actual loaded identity. Keep network spawn genuine.
3. Browser CFG isolation must allow embedded `loadsky`, `mapmodel`, `mapsound` in addition to existing map/reset/fog/texture commands. Existing MDLCFG already has md3load/skin/anim, shadow/cache/trans; add exactly the currently missing used commands **mdlattribute, mdlvertexlight, mdlalphatest, mdlcullface** before isolate/seal. Do not globally unseal contexts. No new arbitrary commands/evaluation.
4. New fixed seed e.g. `web/visible/seeds/swamp-1`: original CGZ at `packages/maps/servermaps/ac_swamp.cgz`, map notice/provenance and `config/maprot.cfg` with only the existing rotation's map token changed to `ac_swamp`. The original embedded config suffices; no external map CFG needed. Reuse verified native3/debug binary/frameworks unchanged; update successor launcher's exact seed rows/membership/rotation/startup checks instead of changing archived native builder `SEED_ROWS`/`ROTATION`, which are Blackwood-specific. Ownership helpers remain read-only/reusable.
5. MAIN selects fresh Swamp browser candidate and run slots; update build manifest/root/count, page/bundle routes, launcher exact serving table and visible Blackwood labels to Swamp. Keep approved outbreak.localhost, ports, capabilities, current limits/lifetime and original-child cleanup. Then separately build/run and observe map, authored scenery/audio/sky and genuine player/guns before expansion.

## Notices, evidence and limits

Preserve the17 located model/texture/sky notice files listed with full text in resource JSON, map's embedded notice, original-player personal-use and weapon notices, and `docs/package_copyrights.txt` audio provenance. Do not apply Swamp's map license to all media. Relevant restrictions include Mitaman `metal_trim_4_v.jpg`/`rgrates0006.jpg` unknown-source/unmodified-package distribution limits, Zastrow no-alter language, Kurt dummy copyrights, mixed Makke exceptions and author-specific attribution/share-alike terms. These need MAIN's explicit treatment for derived local encodings; no blanket redistribution/commercial permission follows. No author contact or rights changes performed.

PASS: finite stdlib read-only gzip/struct inspection using reviewed T281 semantics, full geometry consumption, actual embedded config/entity/resource readback, targeted native/default-CFG/loader/PNG-dispatch source inspection. Evidence: `notes/analysis/T288-swamp-inspection-1.json` and **`T288-resource-paths-4.json`**. First resource JSON was preliminary MD2-only lookup; attempts2/3 stopped on inspector assumptions (empty files retained), corrected to native MD3 default/configured lookup and literal Cube words. No project/map CFG executed, no asset generated, no compiler/game/browser/service/network/FFI/Git or generic framework. Reproduce the two new scripts with canonical Python3.11 `-I -S -B`, redirecting to fresh own-note paths.

No resolved media file is missing. Unclosed items are the explicit encoding/notice decision, final assembled membership/pixel checks, and actual map/model/audio/browser rendering; these belong to the next named source/data tickets and MAIN runtime, not further inventory here. QA and unrelated work remain paused.
