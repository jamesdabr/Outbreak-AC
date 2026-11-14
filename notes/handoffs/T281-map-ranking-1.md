# T281 — Existing map size and expansion shortlist

Venison is the largest existing official map by both non-solid geometry count and occupied bounding area. For expansion without first obtaining a no-derivatives exception, recommend considering **Swamp** first and **Lotus** alongside it: these are the only bundled maps whose embedded tags are `cc-by-nc-sa-3.0`. This is a recommendation for owner/MAIN selection and media-rights review, not permission to modify or a final map choice.

- Worker: World /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket / revision: T2811.0 / D479; STOCK_FIRST_PROTOTYPE0.1. Reread before submission; source/notes stable, writes CLOSED.
- Base/pre-existing edits: no Git operation. Maps, previews, configs, source, assets, candidates and historical notes unchanged.
- New files: `notes/analysis/T281-map-inspector-1.py`, `T281-map-metrics-1.json`, `T281-map-notices-1.py`, `T281-map-notices-1.json`, and this handoff. No commit authorized.

## Ranked result

All dimensions are native map cube/grid units, not metres. Non-solid cell count is an occupied-geometry proxy, not certified playable/walkable area. Corners, clipped regions, steep heightfields, decorative geometry, water and model/entity collisions affect actual traversal.

Top five by decoded non-solid cell count:

| Rank | Map / header author | Canvas | Non-solid cells | Occupied outer bounds | Bounds area | Noncorner, untagged cells | Embedded notice |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | Venison / fundog | 512×512 | 33,700 | 250×265 | 66,250 | 23,070 | CC BY-NC-ND 3.0 |
| 2 | Arctic2 / Halo & Snoosnoo | 256×256 | 27,690 | 216×222 | 47,952 | 25,438 | CC BY-NC-ND 3.0 |
| 3 | Power Station / wotwot | 256×256 | 24,927 | 169×217 | 36,673 | 22,478 | ac-default |
| 4 | Kazemat / YesWeCamp | 256×256 | 23,973 | 217×234 | 50,778 | 16,623 | CC BY-NC-ND 3.0 |
| 5 | Storage Depot / MitaMAN | 512×512 | 23,488 | 234×196 | 45,864 | 21,109 | ac-default |

“Noncorner, untagged” excludes CORNER cells and either TAGCLIP/TAGPLCLIP bit. It still includes heightfields and does not establish clearance, connectivity or absence of entity/model clipping. This proxy changes the leader to Arctic2; Venison has 10,494 tagged non-solid cells. No compressed-byte ranking was used.

Other metric leaders/rankings:

- **Canvas:** Depot, Industrial and Venison tie at 512×512 = 262,144 cells. The remaining maps are 36 at 256×256 and five at 128×128; there is no unique fourth/fifth canvas rank.
- **Occupied bounding area top five:** Venison 66,250; Coal 51,294 (249×206); Kazemat 50,778; Keller 48,697 (209×233); Arctic2 47,952. Bounding rectangles include interior solids/gaps.
- **Noncorner, untagged cells top five:** Arctic2 25,438; Venison 23,070; Power 22,478; Depot 21,109; Coal 20,161.
- **Vertical envelope:** Coal has the largest base-floor/ceiling envelope, 0..76. Venison is −8..22, Arctic2 −17..22, Power −2..24, Kazemat −9..20, Depot −16..18. These are native calcmapdims pre-vdelta extrema, not building height or navigable stacked-floor measurements. Distinct floor heights and heightfield cells establish varied geometry only; routes/multilevel traversal were not verified.

## Expansion recommendation and notices

Venison has substantial solid space outside its occupied bounds: left/right/top/bottom margins inside the mandatory two-cell border are 121/137/142/101 cells. Depot also has large margins, 80/194/186/126. Those are geometric room-to-expand measurements, not expansion rights or measured traversal.

Embedded HX_MAPINFO tags, decoded directly from the actual map bytes, matter:

- Venison, Arctic2, Kazemat, Coal, Keller and Industrial carry `cc-by-nc-nd-3.0`. The bundled notice explicitly says not to alter, transform or build upon the map; obtaining an exception is an owner/MAIN rights decision, not worker authority.
- Power and Depot carry `ac-default`. The bundled notice says DO NOT MODIFY, restricts distribution to the unmodified AssaultCube package, prohibits commercial use, and requires explicit author permission for uses outside that notice. Power's embedded comment credits edits/custom media to makkE, wotwot and Toca; Depot credits Mike “MitaMAN” Poeschl.
- **Swamp** (Undead & ExodusS) carries `cc-by-nc-sa-3.0`, with the embedded comment that it was edited for AssaultCube and thanks original authors. Its 256×256 canvas contains **14,449 non-solid cells** (20th overall), bounds169×145, and 11,627 noncorner/untagged cells. Left/top margins77/99 offer more immediate expansion room than right/bottom6/8. The bundled preview depicts an outdoor overgrown stone area with steps and doorways; this is visual theme evidence, not route verification.
- **Lotus** (DogDancing & $N!P3R*) has the same adaptation tag/comment, **14,052 non-solid cells** (24th), bounds134×193, and **13,333 noncorner/untagged cells**. It beats Swamp on the latter proxy and bounding area25,862 versus24,505. Margins19/99/1/58 favor right/bottom expansion. Its preview depicts a stone interior with pillars and openings.

Thus Swamp is the larger of the two adaptation-tagged candidates by non-solid count, while Lotus is preferable by the filtered-cell proxy. The bundled share-alike notice allows adaptation subject to attribution, noncommercial and share-alike terms. Neither tag establishes blanket rights for every texture/model/sound or an unrestricted public release. No asset relicensing, author contact, final selection or map modification was performed.

Notice sources: [embedded metadata evidence](../analysis/T281-map-notices-1.json), `config/menus_licenses.cfg` (fixed license descriptions), and `packages/maps/official/official_readme.txt` (preserve the official directory; do not edit/rename/delete/add there). The maps contain embedded configs; no external matching .cfg files were present for the shortlisted maps. Embedded config comments were inspected as text only, not executed.

## Actual bundled previews

These are existing illustrative JPEGs, not newly captured game/runtime evidence:

- [Venison](../../packages/maps/official/preview/ac_venison.jpg)
- [Arctic2](../../packages/maps/official/preview/ac_arctic2.jpg)
- [Power](../../packages/maps/official/preview/ac_power.jpg)
- [Kazemat](../../packages/maps/official/preview/ac_kazemat.jpg)
- [Depot](../../packages/maps/official/preview/ac_depot.jpg)
- [Swamp](../../packages/maps/official/preview/ac_swamp.jpg), [Lotus](../../packages/maps/official/preview/ac_lotus.jpg)
- Other metric leaders: [Coal](../../packages/maps/official/preview/ac_coal.jpg), [Keller](../../packages/maps/official/preview/ac_keller.jpg), [Industrial](../../packages/maps/official/preview/ac_industrial.jpg).

## Method and acceptance evidence

PASS: inventoried and decoded **44/44** official .cgz maps, all native format10, with no decoding errors, no geometry trailing bytes and no native two-cell-border violations. Full per-map inventory, authors/titles, types, heights, bounds and preview paths are in [metrics JSON](../analysis/T281-map-metrics-1.json); no map was omitted on size grounds.

Native source inspected: world.h header/types/clip flags, entity.h persistent entity size, serverfiles.h header/entity/RLE decode, worldio.cpp client RLE/embedded records, tools.cpp fixmapheadersize/calcmapdims, protocol.cpp integer/string formats and protocol.h header-record types. The scripts use the same signed floor/ceiling decoding, compatibility correction, run repeats and inclusive non-solid outer bounds. This is a direct format inspection, not a new game decoder integration or native equivalence test suite.

Both small stdlib scripts were inspected before their authorized execution. They read maps sequentially with decompression capped at64MiB/map (refuse at the cap), import no project code, execute no config and write only JSON to stdout. Shell redirection created the two new evidence files. Exact commands, from repository root, both exited0:

```sh
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -S -B notes/analysis/T281-map-inspector-1.py > notes/analysis/T281-map-metrics-1.json
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -S -B notes/analysis/T281-map-notices-1.py > notes/analysis/T281-map-notices-1.json
```

For reproduction preserve these evidence files and redirect into new T281-prefixed output paths rather than overwriting them. JSON readback ranked the results; existing Venison/Swamp/Lotus previews were viewed locally. No map/source writes, game/config execution, native/compiler/service/browser/network/Git/FFI, new framework, or final map selection. NOT RUN: actual traversal/clearance, navigation connectivity, model collision, runtime verticality or performance. QA and unrelated work remain paused. Expansion requires a separate named ticket and rights/scope choice by owner/MAIN.
