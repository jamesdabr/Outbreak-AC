# T041 original survivor and weapon model data

Independently authored low-poly MD3 version15 geometry, procedural 64×64 RGBA palettes and minimal native configs. No stock geometry, skin, config, external model/font/media or modeling-tool output is copied or transformed. The exact staged subtree is `pack-root/packages/models/outbreak/`, separate from accepted map/audio packs and all current build/source paths. **No overlay or actual engine load has occurred.**

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/models/generate_models.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/models/validate_models.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/models/verify_models.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web/assets/models/tests -v
```

Generator and validators use only installed Python standard library. `verify_models.py` compares two full generation runs, validates data, emits `geometry-preview.svg` from actual decoded vertices/triangles/UV palette samples, XML-parses that static SVG, runs/captures ten targeted tests, records tool/source/output hashes and verifies accepted T027/T032 manifests and every payload remain unchanged. It does not execute CubeScript, launch a model app/browser/engine, compile code or contact services. `manifest.json`, `validation.json` and `verification.json` keep geometry identity, structural results and execution evidence distinct.

The pack contains **19 files / 115,915 raw bytes**: three canonical assets for each of three models, a `.LICENSE.txt` sidecar for every one of those nine assets, and `packages/models/outbreak/LICENSE.txt`. All originals are covered by scoped MIT notices; PNGs embed the notice and configs repeat it as comments. Upstream engine/stock licenses are not changed. Unexpected files or symlinks cause rejection; the generator never cleans an output directory.

| Native load name | Canonical files | Frames | Surface | Vertices | Triangles |
| --- | --- | ---: | --- | ---: | ---: |
| outbreak/survivor | survivor/{tris.md3,md3.cfg,skin.png} | 26 | body | 336 | 168 |
| outbreak/pistol | pistol/{tris.md3,md3.cfg,skin.png} | 3 | body | 96 | 48 |
| outbreak/rifle | rifle/{tris.md3,md3.cfg,skin.png} | 3 | body | 144 | 72 |

All file paths in the table are below `packages/models/outbreak/`; they do not replace upstream playermodel/gun names. Each surface has one explicit original shader/skin and four palette UV quadrants with inset UV coordinates. The survivor's forward-facing head visor and chest panel differ from its back. Pistol and rifle have distinct box silhouettes and lengths. The SVG is a **decoded geometry/data projection**, with cyan weapon-tag and pink head-tag centers, not a runtime screenshot, accurate texture rasterizer or proof of rendered appearance.

## Native units, winding and attachment notes

Inspected sources: `md3.h` header/surface/tag/vertex loaders and md3load/md3skin/md3anim commands; `model.h` animation enums; `rendermodel.cpp::findanim/mdlscale/mdltrans/renderclient`; `vertmodel.h::scaleverts/setanim/gentagmatrix` and linked rendering; `rendergl.cpp` GL_FRONT culling; `geom.h::fromquat`; `physics.cpp` yaw movement. Actual source hashes are in verification.json.

The MD3 loader decodes signed vertex shorts divided by64, **swaps X/Y**, then `md3::load` applies `scale/16`; `mdlscale 100` sets scale1. Therefore packed shorts represent **native engine coordinates ×1024** (with the file X/Y interchange). Geometry is initially constructed with +Y forward, then author-rotated −90° around Z so exported **native +X is forward** before the file X/Y interchange. The source renderclient yaw+90 plus MD3/fromquat transforms then agrees algebraically with native movement yaw: yaw90 is +worldX, yaw0 is −worldY. This is source/math evidence, **not observed engine facing**.

File triangles are counterclockwise outward; the negative-determinant loader X/Y swap makes them clockwise in engine coordinates, matching the inspected GL_FRONT culling convention. Per-face outward normals use the MD3 16-bit polar/azimuth encoding and independently agree with file triangle cross-products. File frame bounds/radii, though ignored by parts of this loader, contain the decoded data and remain finite/valid. Every surface/frame has contiguous data, consistent vertex topology and bounded indices/UVs.

The survivor's standing native-coordinate bounds are x=[−0.3203125,0.400390625], y=[−1,1], z=[0,5.2001953125]. The nominal height5.2 is represented within **0.000196 units** by the native 1/1024-unit quantization. Horizontal spans stay within2.2 units in **every frame**, including the compact curled lying pose. Crouch idle is about3.65 high and lying about1.15 high. These are prototype visual dimensions only, not approved hitbox, stance, crawl, movement or damage rules.

At mdlscale100 with mdltrans0, the model origin is standing foot level. Existing renderclient subtracts eyeheight from player origin; future integration must inspect/use that source convention instead of moving the asset's feet or changing collision. Identity, right-handed orthonormal `tag_weapon` and `tag_head` matrices occur in every survivor frame. Tag positions track the authored forearm/head centers; `frame_tags_engine` pins every decoded native-coordinate tag origin. Child weapons are authored +X forward with an origin at the hand/grip region and no additional tags. Native linked rendering propagates parent animation; explicit fallback ranges are provided rather than relying on undefined frames.

Current accepted browser config still isolates MDLCFG for a model-free proof. A **separately released integration** must permit the exact md3load/md3skin/md3anim/mdlscale/mdltrans commands and select these load names/materials; no source or config permission change is made here. Avoid inherited stock skin overrides when integrating original skin.png. Actual model scale/facing/attachment, material selection, culling/shadows and vertex-array interpolation still require native/Wasm/browser verification.

## Explicit frame layout and animation aliases

| Survivor data | Frames |
| --- | --- |
| Standing idle | 0 |
| Run cycle: eight distinct non-rigid limb poses | 1–8 |
| Crouch idle | 9 |
| Crouch-walk cycle: eight distinct non-rigid limb poses | 10–17 |
| Jump/knee-tuck pose | 18 |
| Standing attack / pain | 19 / 20 |
| Falling / curled lying dead | 21 / 22 |
| Crouch attack / pain / death | 23 / 24 / 25 |

The survivor maps every exact native findanim name. `run`→1+8, `crouch walk`→10+8, `death`→21+2, `lying dead`/`decay`→22+1; the remaining required poses have their explicit frames above. `point` reuses the attack stance. Unauthored gestures (`flipoff`, `salute`, `taunt`, `wave`), landing, flag, mapmodel, trigger and survivor gun names explicitly reuse neutral idle. `all` is a debug 0+26 range. These aliases do not claim actual gesture/gameplay implementations. There is no invented downed/crawl enum or life-state event.

Each weapon has frame0 idle, frame1 slight slide/barrel setback, frame2 lowered magazine. `gun idle`→0+1, `gun shoot`/`attack`/`crouch attack`→1+1, `gun reload`→2+1; every other native name explicitly reuses idle except debug `all`→0+3. These are only pose data, not firing/recoil/reload logic or synchronization. Configs use only md3load, md3skin, md3anim, mdlscale, mdltrans with exact original references and valid native names/ranges.

## Structural validation and limits

The independent parser bounds total MD3 data to8 MiB and enforces <=64 frames, <=8 tags/surfaces, <=512 vertices and <=1024 triangles/surface; this output uses one surface and much smaller counts. It checks exact little-endian header/section offsets, section non-overlap and end sizes, every frame/surface count, triangle indices/area/winding/normals, finite bounds/radii/UVs/tags, orthonormal/right-handed tag bases and ordered per-frame names, tag positions within model bounds, PNG power-of-two dimensions<=128 and exact chunk/CRC/decompression bounds, allowed literal configs, native animation ranges, exact file/skin membership/notices/hashes, and manifest bounds/tag metadata.

Ten targeted tests cover malformed/truncated/oversized/count/offset/index/UV/normal/frame/tag/range/reference/PNG/membership/symlink cases and deterministic outputs. These are parser/data tests. Native/Wasm model loading, actual vertex-array rendering, animation/attachment timing, material selection, shadows, gameplay third-person camera/life-state/hitbox integration and the eight-player MVP are **NOT RUN**, not accepted by this asset ticket.
