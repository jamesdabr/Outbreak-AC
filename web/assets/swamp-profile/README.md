# Original Swamp local asset profile

T2901.0 / STOCK_FIRST_PROTOTYPE0.6 / D491. Exact346 paths: accepted stock-combat97
plus249 new paths from T288-resource-paths-4 (230media,17notices,audio provenance,
original Swamp CGZ). Selected map is ac_swamp revision179; original embedded
automatic config/entities/geometry are preserved. Inert base Blackwood data remains.

The114 original JPEGs are encoded as native-resolution PNG bytes at their original
virtual `.jpg` filenames. Both RGB and RGBA decoded pixels are preserved; no resize
or recolor. Manifest/provenance explicitly mark encoding/source/pixel hashes.
T288 inspected SDL_image signature detection in IMG_Load/IMG_Load_RW as support;
Swamp browser rendering remains for MAIN runtime verification. Other new files
(55model CFGs,51MD3,nineOGG,onePNG,17notices,audio provenance,CGZ) retain original bytes.

Only browser CFG changes are MAPCFG loadsky/mapmodel/mapsound and MDLCFG
mdlattribute/mdlvertexlight/mdlalphatest/mdlcullface before respective isolation/seal.
No original profile, map CFG, engine source, or build config is modified.

Mixed author notices remain at their original paths and are associated per file.
The embedded map CC BY-NC-SA3.0 notice applies to the map, not all media. Player
personal-use and weapon CC BY-NC-SA2.5 notices remain. Mitaman unknown-source
restrictions, Zastrow no-alter language, Kurt copyrights and other individual
terms are retained; this local/private encoding decision is not redistribution
clearance. Stock is not MIT. No public distribution or rights changes authorized.

After full assembler inspection, run exactly once from repository root:

```sh
python3 -I -B web/assets/swamp-profile/assemble.py
```

This refuses existing outputs and symlinks, pins inputs, writes exclusively and
performs finite membership/byte/hash/pixel/CFG/input-preservation checks. No project
imports, map CFG execution, subprocess, network, build or runtime. Do not rerun
into existing outputs. MAIN owns integration and actual runtime observation.
