# T041 original survivor/pistol/rifle model data handoff

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket/revision: T041 revision1.5 RELEASED; submitted for MAIN review, no authoritative status change
- Governing subset: D018 additive1.5 to browser foundation/GOVERNANCE/P0 revision0.5; gameplay documents remain boundaries, not authority to implement state/collision/balance.
- Baseline: 13f0d8eea4822dee5c976661218d022be74342e3 plus existing accepted/active work. web/assets/models did not exist at start. All earlier asset/source/build/QA/server/contracts/notes preserved.
- Changed files: only NEW web/assets/models/** (original generator/license/config/MD3/PNG/manifest/validator/tests/geometry SVG/README/verification) and this new handoff. No overlay, source change, commit/push/reset, dependency acquisition, worker dispatch or other worker contact.

## Per-criterion acceptance evidence

1. **PASS structurally; actual runtime NOT RUN** — exact original canonical model files generated. Survivor: one body surface, **26 frames / 336 vertices / 168 triangles**, with eight distinct non-rigid run frames, eight distinct crouch-walk frames, standing/crouched/jump/attack/pain/falling/curled-lying poses, and valid ordered tag_weapon/tag_head records in every frame. Every native findanim name has an explicit valid range; no crawl/down enum or life-state mapping. Pistol and rifle: each three distinct pose frames (idle, shoot/setback, lowered magazine); one body surface, **96/48** and **144/72** vertices/triangles respectively. Original front/back palette distinctions and 64×64 RGBA PNGs. Visual dimensions use mdlscale100, feet z0, nominal standing height5.2 with native fixed-point quantization; all survivor horizontal frame spans<=2.2. No gameplay/hitbox/state or reload/recoil implementation is implied.
2. **PASS** — standard-library deterministic generator, no stock geometry/skin/config transformation, downloads or external content. Scoped own MIT notice, per-file sidecars and PNG/config notices. Exact **19 staged files / 115,915 raw bytes**. Manifest contains per-file path/size/SHA-256/format/provenance/notices, per-model frame/surface/vertex/triangle/UV metadata, all decoded native frame bounds and per-frame tag origins/basis, exact animation ranges and native scale/axis conventions. Upstream engine/media licensing untouched.
3. **PASS** — independent bounded MD3/PNG/config decoder validates header/section/end offsets, contiguous frame/surface counts, integer/float/radius/bounds validity, triangle indices/nondegeneracy/winding/normal agreement, finite bounded UVs, all tag names/order/positions/orthonormal right-handed bases, config allowlist/native names/ranges/exact original shader/skin references, PNG dimensions/chunk order/CRC/bounded decompression, exact original membership/notices/hashes and manifest bounds/tag metadata. **10 meaningful tests pass**, including malformed offsets/counts/indices/UVs/normals/frame bounds/tag bases/order, invalid animation range/name/reference, PNG corruption/duplicate header/oversized dimensions/truncation, path escape/undeclared/symlink rejection and output determinism. Unexpected files/symlinks are not deleted. Two full generation runs produce byte-identical pack files and manifest. No scripts/configs are evaluated.
4. **PASS (generated geometry evidence only)** — `web/assets/models/geometry-preview.svg` projects actual decoded triangles/vertices with sampled original palette texels: standing front/back, run, crouch idle/walk, lying pose, pistol and rifle. Cyan/pink markers show decoded weapon/head tag centers. SVG XML parses successfully, has scoped MIT metadata and explicitly labels itself not an engine screenshot. README supplies detailed geometry/native axes/scale/winding/yaw/tag/animation integration notes. No browser/modeling app/engine was used to render a preview.
5. **PASS for handoff/evidence; actual engine gates NOT RUN** — this new immutable handoff, exact commands/results and source/tool/output identities below and in verification.json. Actual native/Wasm model loading, browser vertex-array draw, model facing/skin/material/shadow selection, animation interpolation/attachment timing and third-person MVP gameplay are **NOT RUN**. No current pack/build overlay. All accepted T027/T032 payloads and manifest identities checked unchanged.

## Canonical staged files and identities

Stage root: **web/assets/models/pack-root**. Future native load names (not wired by this ticket): **outbreak/survivor**, **outbreak/pistol**, **outbreak/rifle**.

```text
packages/models/outbreak/LICENSE.txt
packages/models/outbreak/survivor/tris.md3
packages/models/outbreak/survivor/tris.md3.LICENSE.txt
packages/models/outbreak/survivor/md3.cfg
packages/models/outbreak/survivor/md3.cfg.LICENSE.txt
packages/models/outbreak/survivor/skin.png
packages/models/outbreak/survivor/skin.png.LICENSE.txt
packages/models/outbreak/pistol/tris.md3
packages/models/outbreak/pistol/tris.md3.LICENSE.txt
packages/models/outbreak/pistol/md3.cfg
packages/models/outbreak/pistol/md3.cfg.LICENSE.txt
packages/models/outbreak/pistol/skin.png
packages/models/outbreak/pistol/skin.png.LICENSE.txt
packages/models/outbreak/rifle/tris.md3
packages/models/outbreak/rifle/tris.md3.LICENSE.txt
packages/models/outbreak/rifle/md3.cfg
packages/models/outbreak/rifle/md3.cfg.LICENSE.txt
packages/models/outbreak/rifle/skin.png
packages/models/outbreak/rifle/skin.png.LICENSE.txt
```

Manifest: **web/assets/models/manifest.json**, SHA-256 **7a232c7e8e238b29285f452c9e38f31dfc073cc3d0b9568352bb7a233c6b2fd1**. Pack: **19 files / 115,915 raw bytes**.

| Asset | Bytes | SHA-256 |
| --- | ---: | --- |
| survivor/tris.md3 | 82156 | 9b6f1cc37bc404d0cc2a1a4e26ece431af275de971924707cd9f91ebf2fefb09 |
| survivor/md3.cfg | 2100 | 060e48df70ba96084f68ba1a2187598f628ada2ab18f78cca5eb80af190833da |
| survivor/skin.png | 1512 | 9fa0040fefbc054364fdaa1e859297ec9ac5f84f2459f38a18fcf16a045f5f96 |
| pistol/tris.md3 | 4100 | cef9e518dead445712f708bc5f6c6ea1b5709ddcf23944d228e0b7924897ea86 |
| pistol/md3.cfg | 2090 | 713069c9a07fafd6d7b315bb5d0a8fee268c1adab5ecb3e9aab297a6a2fe7a3f |
| pistol/skin.png | 1497 | 482917bedeaba79fa1c407a886473b85567a79f0667e4f91b18a64897121ff8f |
| rifle/tris.md3 | 5924 | 16995887d6fcaadc01c43c4fe8b94a8bb312b74d8cbc07f44b9c4c96bb99a1d5 |
| rifle/md3.cfg | 2090 | 713069c9a07fafd6d7b315bb5d0a8fee268c1adab5ecb3e9aab297a6a2fe7a3f |
| rifle/skin.png | 1496 | 147a1a18c92bd5341d1b80eec71bf0f21eaf8f0766766da2628496cc1838b62f |

SVG SHA-256: **e20c0f9d4870f1033024f11ce504b72b42fb9e670f55d6d006a3521c53574067**. Validation JSON SHA-256: **d5b66dc7b7983064cd0032983b341187b4115f27d9ad64ee4ccf5cce73bcd914**. These are data identities, not browser performance or runtime evidence.

## Commands and actual results

Working directory `/Users/jd1/code/apps/outbreak`, installed Python **3.11.9** standard library only. Authored entry points and imported helpers were inspected before execution.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/models/generate_models.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/models/validate_models.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/models/verify_models.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web/assets/models/tests -v
```

All ran successfully, exit0. Final verify executes/captures all **10 passing tests**, compares two full generation runs and manifest bytes, checks native findanim strings against the actual source table, writes/validates the SVG and records exact source/tool/output SHA-256/Python/platform identity in **web/assets/models/verification.json**. `validation.json` is the independent structural result; `manifest.json` remains deterministic without environment/timestamps.

Inspected native sources: md3.h loader/commands; model.h enums; vertmodel.h scaleverts/setanim/gentagmatrix/link rendering; rendermodel.cpp findanim/mdlscale/mdltrans/renderclient; rendergl.cpp culling; geom.h fromquat; physics.cpp movement axes. Exact file fingerprints are in verification.json. No native executable, compiler, engine, browser, modeling tool, server, service or external API was invoked. No source scripts or configs were evaluated.

## Native scale, axes, attachment and animation notes

- The MD3 loader divides signed coordinates by64 and swaps X/Y. md3::load later applies **scale/16**, where mdlscale100 sets scale1. Packed shorts therefore represent native engine coordinates×1024, with the file X/Y interchange. Tag origins undergo the same swap/scale. Configs specify mdlscale100 and mdltrans0.
- The construction's +Y forward is author-rotated −90° around Z before export so the resulting **native +X is forward**. This matches the source algebra of renderclient yaw+90, MD3 quaternion and fromquat conventions with physics movement. It is not an observed runtime-facing pass.
- File triangles are CCW outward; the loader's negative-determinant X/Y swap produces CW native triangles for the inspected GL_FRONT cull convention. Packed per-face MD3 normals agree independently with file triangle normals. Actual culling/material/shadow/direct-draw appearance remains NOT RUN.
- Standing survivor native bounds: x=[−0.3203125,0.400390625], y=[−1,1], z=[0,5.2001953125]. The 0.0001953125 height difference from nominal5.2 is the native fixed-point quantization. All frames, including the compact curled lying pose, meet horizontal spans<=2.2; crouch is about3.65 high, lying about1.15. These are visual references only, not collision/stance/hitbox policy.
- tag_weapon/tag_head occur in all26 frames in that exact order. Bases are identity/right-handed/orthonormal; origins follow authored forearm/head centers. Every decoded native-coordinate tag origin and frame bound is pinned in manifest metadata. No gameplay head-hit location or authoritative actor state is supplied.
- Survivor layout: idle0; run1–8; crouch idle9; crouch walk10–17; jump18; attack19; pain20; falling21; lying22; crouch attack23; crouch pain24; crouch death25. `death` maps21+2, `lying dead`/`decay` map22+1. Other names explicitly reuse documented idle/attack poses; `all` is debug0+26. No new crawl/down enum or life-state callback exists.
- Weapon layout: idle0, shoot/setback1, lowered-magazine2. gun idle0+1; gun shoot/attack/crouch attack1+1; gun reload2+1. Other exact native names explicitly reuse idle except debug all0+3. This is pose data, not firing/recoil/reload timing or mechanics.

## Remaining integration and preserved scope

All T027 map and T032 audio payloads were independently checked against their accepted per-file hashes. Accepted manifest identities remain **1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3** (41 map files) and **689941eae651adaef254cb3858f940e673661ef490c63c4821a290e9615907a3** (19 audio files). No overlay or current build/source modification.

MAIN must separately release integration of these load names, original skin selection, appropriate MDLCFG command permissions and actual native/Wasm/browser rendering/animation/attachments. Current accepted browser config isolates MDLCFG for a model-free proof; this ticket does not change it. Do not assume stock team-skin overrides or stock gun names select these assets. Native renderclient subtracts eyeheight to establish foot origin; preserve that convention rather than changing physics/hitbox data. Real third-person camera, crouch/down/revive/death/game-state mapping, materials/shadows and eight-player MVP gates remain unimplemented/unverified by this data task. No independent T041 data step is blocked, and only MAIN accepts this ticket.
