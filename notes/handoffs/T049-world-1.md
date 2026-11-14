# T049 original media stage handoff

- World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf; T049 revision2.1 RELEASED, D026 additive2.1 to governing0.5. Submitted for MAIN review, status unchanged.
- New files only: `web/assets/media-profile/{assemble.py,validate.py,verify.py,README.md,manifest.json,validation.json,verification.json,tests/test_merge.py,pack-root/**}` and this handoff. Existing packs/source/build/QA/contracts/notes untouched; no commits/push/reset, dispatch, dependency install/download or service execution.

## Criterion evidence

1. **PASS — exact assembly:** 79 staged files / **388,763 raw bytes**, from the exact approved map41/audio19/models19 manifests. All source file memberships, per-file sizes/hashes, original ownership/notices and path confinement checked before copying. All78 unmodified copies independently compared byte-for-byte against pinned sources.
2. **PASS — sole derivation:** new `config/browser.cfg` inserts exactly md3load/md3skin/md3anim/mdlscale/mdltrans MDLCFG permissions, one newline-terminated command per line, immediately before the existing isolatecontext MDLCFG. Exactly147 added bytes; all other config bytes/settings/restrictions/isolation/seal preserved. Audio0, musicvol0, soundvol0 and HUD omission remain unchanged. No source-pack config was edited.
3. **PASS — manifest/provenance:** every final file has final virtual path/size/hash, original input root/manifest pin/path/hash, preserved notice/license, and exact browser derivation recipe/hash. Deterministic manifest excludes environment/timestamps. Source packs/manifests verified unchanged. Runtime gates remain explicitly unverified.
4. **PASS — independent verification/tests:** two assembly runs yield identical79 files and manifest. Separate validator reconstructs expected copied/derived bytes without using builder derivation logic. **8 tests pass**, covering hash pin/payload mutations, extra source/output files, path escape/symlinks, collisions, extra permissions/changed settings, provenance/recipe/membership tampering and determinism. Rejected unexpected files/symlinks are preserved. All17 active `web/build/out` files matched before/after SHA-256/size snapshots.
5. **PASS — delivery/scope; runtime NOT RUN:** exact source pins, tool/Python/platform/output identities, test command/exit/stdout/stderr and active snapshots in verification.json. No overlay, active build/source/config changes, media decoding, engine/browser/server/modeling-app launch or playback. Actual media loading/rendering/animation/attachment/audio-gesture tests are **NOT RUN**.

## Final identities

Stage root: **web/assets/media-profile/pack-root**, proposed later mount `/outbreak`; **79 files / 388,763 bytes**.

- **Manifest SHA-256:** `9b7a01d6c1c29d0c0c68f95a418488963434ab54ac6b2dd0caa78b4bc21b299a`
- Derived browser.cfg: **2,286 bytes**, SHA-256 `1ee76c7f9f23362f32cf9e7e8dc260d55a387a9d2561ddd39d7c7702c884eacc`
- Original browser.cfg SHA-256: `ae5853e303fbc6efcf6fdf39517b47cc46eb88fec4d3963edc56b9c005c30d3e`
- Exact147-byte inserted-block SHA-256: `b3c2ca8fecf6d5d9b9d6f6cad91d306aede131f0432c1d8c9a90d37a7a7a96cb`
- Validation JSON SHA-256: `4d6f2ed4f05a910d7fc6966a6149d37162744d977f3c410275872a6e8c085366`

Input manifest pins preserved:

```text
map     1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3
 audio  689941eae651adaef254cb3858f940e673661ef490c63c4821a290e9615907a3
models  7a232c7e8e238b29285f452c9e38f31dfc073cc3d0b9568352bb7a233c6b2fd1
```

## Commands and remaining work

From `/Users/jd1/code/apps/outbreak`, Python3.11.9 standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/media-profile/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/media-profile/validate.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web/assets/media-profile/tests -v
```

All exit0. verify.py assembles twice and captures all8 passing tests. `assemble.py` is the standalone generator, also documented for reproduction; final generation was executed through verify.py. Scripts were inspected before execution. Test fixtures are newly authored text in owned temporary directories, not media/runtime simulations.

No independent T049 step is blocked. MAIN must separately release active pack selection, model/actor/camera integration and real audio gesture/sample hooks. This stage leaves the current original41-file graphics profile unchanged. Only MAIN accepts the ticket or releases runtime work.
