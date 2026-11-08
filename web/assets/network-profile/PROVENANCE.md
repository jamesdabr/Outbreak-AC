# T064 original network-profile DATA

Frozen separate derivative of accepted T053 audio-profile manifest `7def7d8da8a9567f8023f5675f6fa9369edcd930f635794c9c95ca106868e283`. No active pack overlay or build integration.

`pack-root` contains exactly79 files/388791 bytes. Exactly78 are byte-identical T053 copies, including browser.cfg, audio/model/font/texture data, bindings, MDLCFG permissions and all notices. Only `packages/maps/dev_outbreak_browser.cgz` changes: source534 bytes to561 bytes, revision1 to2. Map SHA256 `856173969726f632812fd8ebd2ada746831d7e81f7452dd98f7235a2bd398134`; manifest SHA256 `c9ecfa62f7e4ca7111a9d3a23a9c97b906d11399d32f6f312463c6697a3359d7`.

The new independently authored map records use the same scoped MIT notice as the original Outbreak proof map. Existing per-file notices and internal HX_MAPINFO bytes remain unchanged. This does not relicense upstream engine code or stock assets. Each manifest entry preserves the complete T053 source entry in its provenance, its source manifest/root/path/hash, final virtual path/size/hash/license/notice. The map additionally records exact old/new compressed and decompressed hashes and byte derivation.

Native v10 persistent entities use16-byte little-endian layout `<hhhhBBBBhbB`: xyz, attr1/yaw, type, attr2/3/4, attr5, attr6, attr7. Four previous starts become the eight exact ordered FFA anchors in T0643.7; type2, attr2=100, other attributes0, yaw scale10. All five LIGHT records retain their exact bytes and order after the starts. Header count at offset16 changes9->13; header revision at924 changes1->2. All other decompressed header/extra metadata and RLE geometry bytes remain exact. Title, external config, timestamp, texture lists, notices and geometry are not edited; no resdata/config entry is invented.

Gzip is explicit: header `1f8b08000000000002ff`, mtime0, raw DEFLATE level9, OS255, footer CRC32 and ISIZE of the decompressed map. Bounded validation rejects CRC/size errors, truncation, trailing streams, unsupported structures and decompression beyond1MiB. The validator independently checks the literal ticket anchor list and two-field-only header transition, exact light/RLE slices, canonical recompression, exact79-file membership/provenance and78 copies. The inspected original bounded parser validates the source RLE; exact geometry equality transfers those structural cells to the derivative. This is a specialized data validator, not execution of the native decoder.

`anchors.json` remains outside pack-root. It records all eight coordinates/encoded and degree yaws, intersected clearance cells, floor0/ceiling12, radius1.1, minimum horizontal separation16, seven pinned native source identities and citations. Source `world.h:150` keeps MINSPAWNS5; `tools.cpp:291-312` counts attr2=100 FFA starts and requires at least5; protocol.cpp/protocol.h include deathmatch among FFA-start modes; serverfiles.h:1001 intersects supported modes for dedicated rotation. Eight supplied starts satisfy this source-derived prerequisite without changing engine validation. No final squad deployment/grouping or gameplay balance is selected.

Reproduce data generation (owned files only, after inspection):

```sh
python3 -B web/assets/network-profile/build_network_profile.py
python3 -B web/assets/network-profile/validate_network_profile.py
python3 -B -m unittest discover -s web/assets/network-profile/tests -p 'test_*.py' -v
```

Observed:12 tests PASS; actual generated pack validation PASS; zero compiler/game/server/network subprocesses during generation/validation. `verification-evidence.json` records before/after6396 protected pack/helper/build/output/cache/native-source files unchanged. Runtime native decoding, actual dedicated mode selection, spawning/gameplay, browser rendering/audio/models and multiplayer remain NOT RUN. Later MAIN acceptance/pins/staging are required. Original revision1 offline/audio/T063 inputs remain unchanged.
