# T053 separate audio-enabled data profile

**79 files / 388,764 raw bytes**, staged only at `web/assets/audio-profile/pack-root` for a later approved `/outbreak` mount. Source is the exact accepted T049 media-profile manifest `9b7a01d6c1c29d0c0c68f95a418488963434ab54ac6b2dd0caa78b4bc21b299a`.

Only the derived copy of `config/browser.cfg` changes:

```diff
-audio 0
+audio 1
-soundvol 0
+soundvol 96
```

The other **78 files are byte-identical**, and every other config byte is unchanged: musicvol0/hudgun0, all bindings, five MDLCFG permissions, original map restrictions, isolation/seal and scoped notices. No media is generated/transformed/preloaded or played. T053 attribution and exact old/new lines, input/result hashes and the earlier T049 config derivation are preserved in the manifest provenance.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/audio-profile/build_profile.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/audio-profile/check_profile.py
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/audio-profile/verify_profile.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web/assets/audio-profile/tests -v
```

Python standard library only. The inspected T049 generator is imported read-only for original map/audio/model closure and path validation; its entry point is never invoked. Source manifest pin, exact file sets and every payload/notice hash are checked before writing. The target validator independently constructs expected two-line replacement bytes instead of calling the builder's transform. Eight tests reject altered/missing/extra/symlink inputs, pin/hash/path changes, extra commands or unrelated settings, ambiguous source lines, metadata tampering and unexpected outputs without deleting them.

`verify_profile.py` compares two full builds and all manifest/file bytes, captures tests and hashes, and verifies unchanged before/after snapshots for the four protected pack roots and the active build. `manifest.json` has every final size/hash/virtual path, accepted source path/root/hash, original ownership/notices, upstream manifest identities and the sole explicit derivation recipe. Environment/tool identity is separate in `verification.json`.

- Manifest SHA-256: `7def7d8da8a9567f8023f5675f6fa9369edcd930f635794c9c95ca106868e283`.
- Derived browser.cfg: **2,287 bytes**, SHA-256 `b84d1e940971a1fd9007c2691154e20ebd2f93d6956c5ac96c2d8e67db709bac`.
- Source browser.cfg SHA-256: `1ee76c7f9f23362f32cf9e7e8dc260d55a387a9d2561ddd39d7c7702c884eacc`.

All original copyright/license scopes remain unchanged. **No overlay or active build mutation is performed.** Actual user-gesture audio initialization/registration/decode/playback, model loading/rendering, source integration and build selection remain **NOT RUN** and need separate MAIN acceptance/releases. The configuration request alone proves no audible or backend behavior.
