# T053 audio-enabled derivative handoff

- World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf; T053 revision2.5 RELEASED under D033 additive2.5 to governing0.5. Submitted for MAIN review; status unchanged.
- Only NEW `web/assets/audio-profile/**` and this handoff written: builder/checker/verifier, eight tests, README, 79-file pack-root, deterministic manifest, validation and verification/provenance evidence. T049 helper imported read-only after inspection. No existing pack/source/build/native/QA/transport/contract/note edits, commits/push/reset or worker dispatch.

## Acceptance evidence

1. **PASS — exact derivative:** separate **79 files / 388,764 bytes**. All78 other files are byte-identical to accepted T049. Sole derived browser.cfg changes exact full lines **audio0→audio1** and **soundvol0→soundvol96**, adding only one byte overall. Musicvol0/hudgun0, permissions/bindings/restrictions/isolation/seal and every other config byte remain unchanged.
2. **PASS — source/ownership/provenance:** source manifest pinned to **9b7a01d6c1c29d0c0c68f95a418488963434ab54ac6b2dd0caa78b4bc21b299a**. All source entries/payload hashes/notices and original map/audio/model input closure reverified before copying and again after tests. Every output has source root/path/manifest pin/file hash, original provenance/notice/license, final virtual path/size/hash; browser.cfg records exact old/new lines and upstream T049 derivation. No copyright/license scope changed.
3. **PASS — validator/tests/determinism:** target byte validator independently reconstructs expected replacements without calling builder derive(). Two builds produce identical79 files and manifest. **8 tests pass**, rejecting bad pins/changed source bytes/missing or extra files, escapes/symlinks, extra permissions/unrelated setting changes, ambiguous lines and metadata/provenance/recipe tampering. Unexpected files/symlinks are preserved.
4. **PASS — protected roots unchanged:** complete SHA-256/size snapshots before/after match for original map41, audio19, models19, media-profile79 and active `web/build/out`17 files. All original manifest pins also rechecked. No overlay or active build/source mutation.
5. **PASS for delivery; actual runtime NOT RUN:** exact tools/Python/platform hashes, commands/test exit/output and protected snapshots are in verification.json. Actual playback/audio backend/model load/render/source/build integration are **NOT RUN**. No engine/browser/server launch, script evaluation, dependency/network access, sound mapping or asset generation.

## Stable output identities

- Stage: **web/assets/audio-profile/pack-root**, proposed later mount `/outbreak`.
- **Manifest:** `web/assets/audio-profile/manifest.json`, SHA-256 **7def7d8da8a9567f8023f5675f6fa9369edcd930f635794c9c95ca106868e283**.
- **Count/bytes:** 79 files / **388,764 bytes**, 78 copied and 1 derived config.
- **Derived config:** 2,287 bytes, SHA-256 **b84d1e940971a1fd9007c2691154e20ebd2f93d6956c5ac96c2d8e67db709bac**.
- Source config: 2,286 bytes, SHA-256 **1ee76c7f9f23362f32cf9e7e8dc260d55a387a9d2561ddd39d7c7702c884eacc**.
- Validation JSON SHA-256: **09483dad05dc34f7358839000e159dbdfe1b61c35453a7db00eeb383a5d4a8c8**.

Preserved upstream map/audio/model manifests:

```text
1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3
689941eae651adaef254cb3858f940e673661ef490c63c4821a290e9615907a3
7a232c7e8e238b29285f452c9e38f31dfc073cc3d0b9568352bb7a233c6b2fd1
```

## Commands and next gate

From `/Users/jd1/code/apps/outbreak`, Python3.11.9 standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/audio-profile/verify_profile.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/audio-profile/check_profile.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web/assets/audio-profile/tests -v
```

All exit0. verify_profile.py executes the builder twice and captures all8 passing tests. The standalone builder `build_profile.py` is documented for reproduction; actual final generation was invoked through verify_profile.py. Exact script/helper/output fingerprints and test stdout/stderr are in **web/assets/audio-profile/verification.json**; structural comparison is in validation.json. Ticket/governing addendum rechecked, unchanged.

No independent T053 data step is blocked. Player owns T052 audio source; MAIN must separately accept/release source/build/gesture runtime integration. This staged config requests audio but is not proof that any backend initialized, sample decoded or sound played. Existing active output remains untouched.
