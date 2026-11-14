# T262 — Original walker asset delivered

- Worker: AI & Director /01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket/contract: T2621.0/D439, VISIBLE_SLICE0.3; source AND one local asset generation, not SOURCE ONLY. Ticket reread before delivery.
- Changed files: ONLY the eight new allowlisted files under `web/assets/walker/` and this handoff. Old assets/packs/generators/candidates/source untouched. No Git operation.

**Produced the concrete asset.** Original unarmed low-poly infected humanoid with mottled olive skin, worn dark clothing, exposed chest rag, clouded eyes, asymmetric reaching arms and an uneven eight-pose walk. Native MD3v15, one body surface, **25 frames, 480 vertices, 240 triangles**, no tags/weapon; **64×64 RGBA8 skin**. Idle, walk/run, attack, pain, forward fall and prone hold are distinct. All27 native animation names map to valid ranges; unused crouch/gun names are compatibility aliases, not behavior.

Exact command executed ONCE from repository root after complete own/reused-source inspection:

```sh
python3 -I -B web/assets/walker/generate.py
```

Exit0. Actual generated-file readback checks PASS: MD3 magic/version/header/surface offsets/counts/indices/UVs/frame bounds/radii/feet origin/nondegenerate geometry/distinct animation poses; PNG64×64/filter layout/CRCs; config/reference/range completeness and license consistency. The generator uses only stdlib, fixed outputs and exclusive creation, refuses existing outputs/symlinks, and does not spawn children. No retry or failure cleanup occurred.

`web/assets/walker/preview.svg` is a six-pose projection of the **decoded generated MD3 vertices/triangles**, shaded with colors sampled from the **decoded generated PNG**. It is explicitly labeled asset preview, not a gameplay screenshot. XML readback passed. No browser/engine preview or game runtime was invoked.

| Generated output | Bytes | SHA256 |
|---|---:|---|
|pack-root/packages/models/outbreak/walker/tris.md3|104404|97dea8e600ac7710410748c5949d52ee2c40ac93bae19cdcb0a4bda3bbc8e3a0|
|pack-root/packages/models/outbreak/walker/skin.png|2380|e64bf340cf91f12895d7b0262ec9d48088c06e06753d1f01c873d4c95b349f67|
|pack-root/packages/models/outbreak/walker/md3.cfg|2245|72496085b721abcc7aceec76917fcb515e945fe153bbcd8f6154a4d523545259|
|pack-root/packages/models/outbreak/walker/LICENSE.txt|1439|0552d007ce2bdf01034be5ef4f80dd2f00890012bb3b74a12a28fe8146d0a690|
|preview.svg|82756|8a6f19db59531c0772ff516260f77634b1aba0f7d53e10dfc9997d0de7398dcc|

Paths in table are relative to `web/assets/walker/`. Inspected generator SHA256 ea9504bf74f800b3549fcbee9d48eae91bd01c10d4727bf189b6985a1d05e1c0. Root/pack notices match. MIT T041 `web/assets/models/generate_models.py` MD3/PNG/clockwise-face/coordinate conventions are adapted with copyright and attribution; walker geometry/poses/palette are original, no external media/dependency. Feet origin, native +X front, loader scale100 and zero translation follow the existing engine convention. Visual bounds do not define collision/attack timing.

Remaining: MAIN asset inspection, separately authorized pack integration, then actual in-engine skin/scale/winding/animation verification alongside the visible baseline. No pack assembler, toolchain, browser, native/server process, network, enemy simulation, replication or P2 balance work ran. No new framework/proof packet. STOP for MAIN inspection/integration scheduling.
