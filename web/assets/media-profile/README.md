# T049 separate original media stage

A deterministic composition of the exact accepted T027 map (41 files), T032 audio (19) and T041 models (19), with **79 files / 388,763 raw bytes**. Stage: `web/assets/media-profile/pack-root`, for a later approved mount at `/outbreak`. **No overlay, active-build selection, source/config mutation or media execution is performed here.**

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/media-profile/assemble.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/media-profile/validate.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/media-profile/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web/assets/media-profile/tests -v
```

`verify.py` performs two actual assembly runs, independently validates the exact merge, runs/captures eight negative/positive fixture tests, and checks before/after hashes for all 17 active `web/build/out` files. It writes only this new subtree. Python standard library only; no image/model/audio transformation or script evaluation. Unexpected source manifest/file hashes, file sets, private/traversal/symlink paths, input collisions, undeclared outputs or altered config bytes are rejected without deleting unexpected files.

Input manifest SHA-256 pins:

| Source root under web/assets | Manifest SHA-256 |
| --- | --- |
| original | 1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3 |
| audio | 689941eae651adaef254cb3858f940e673661ef490c63c4821a290e9615907a3 |
| models | 7a232c7e8e238b29285f452c9e38f31dfc073cc3d0b9568352bb7a233c6b2fd1 |

**78 files are byte-identical copies**. The only derived file is `config/browser.cfg`: these exact 147 bytes (five newline-terminated commands) are inserted immediately before the existing `isolatecontext MDLCFG` line:

```text
scriptcontext MDLCFG md3load
scriptcontext MDLCFG md3skin
scriptcontext MDLCFG md3anim
scriptcontext MDLCFG mdlscale
scriptcontext MDLCFG mdltrans
```

Everything else, including map permissions, both isolation commands, sealing, audio0/musicvol0/soundvol0/HUD omissions, all notices and all media bytes remains unchanged. The derived config is 2,286 bytes, SHA-256 `1ee76c7f9f23362f32cf9e7e8dc260d55a387a9d2561ddd39d7c7702c884eacc`; original source hash `ae5853e303fbc6efcf6fdf39517b47cc46eb88fec4d3963edc56b9c005c30d3e`.

`manifest.json` records every final source/virtual path, bytes/hash, original input root/manifest pin/path/file hash, original scoped MIT notice and the exact derivation recipe/hash. Manifest SHA-256: `9b7a01d6c1c29d0c0c68f95a418488963434ab54ac6b2dd0caa78b4bc21b299a`. `validation.json` is the independent exact-merge result. `verification.json` keeps Python/platform/tool identity, test output, deterministic two-run evidence and protected active-build snapshots separately.

Tests use newly authored inert text fixtures; they do not decode or play real media. Actual engine models/materials/animations/attachments/rendering, audio backend/sample registration/user-gesture playback and active media-build/QA integration remain **NOT RUN**. This is staged data/permissions only. No gameplay, camera, hitbox, source protocol, sound or actor-state behavior is implemented or accepted by this task. All three accepted source packs/manifests stay unchanged.
