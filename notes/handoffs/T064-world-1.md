# T064 frozen DATA handoff

- Worker: World/Match-Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket: T0643.7 RELEASED, reread before submission; D051 prerequisite3.7, browser foundation/GOVERNANCE/P0 0.5. T053 DATA and T060 PREPARATION dependencies accepted; no build/runtime authority inferred.
- Base commit:13f0d8eea4822dee5c976661218d022be74342e3. Pre-existing source/header/build/notes changes preserved. New network-profile directory was absent at start.
- Changed: only NEW `web/assets/network-profile/**` (three Python generator/parser/validator files, one test file, exact79-file pack, manifest, anchors/validation/evidence JSONs and provenance Markdown) and this handoff. No source, old pack/helper, build/cache/out/SDK/server/QA/transport/contract edit, commit or dispatch.
- Generator/data/manifest/tests are frozen at the identities below. New findings will be raised as new question notes before any further edit.

## Acceptance evidence

PASS: deterministic79files/388791B derivative of exact T053 manifest7def7d8da8a9567f8023f5675f6fa9369edcd930f635794c9c95ca106868e283. All78 other files are exact copies, including browser.cfg/audio/HUD/MDLCFG/bindings/models/fonts/textures/notices. Sole derived file `packages/maps/dev_outbreak_browser.cgz` now561B, source534B. No extra packaged file, resdata record or active overlay. All complete source entries/provenance/license/notice identities retained in manifest; map's scoped original MIT notice and HX_MAPINFO remain exact. See PROVENANCE.md for the byte derivation.

PASS: native v10/16-byte entity structure, exact ordered eight released FFA anchors/yaws/attrs, total13 entities, five original LIGHT records unchanged in order/bytes. Only header integer count offset16 changes9->13 and maprevision offset924 changes1->2. Every other decompressed header/extra/RLE byte is identical to parsed original. Canonical explicit gzip mtime0/header/CRC32/ISIZE/level9 and bounded inflation/structure checks pass. Source parser's original RLE decoding plus exact RLE equality validates4096 geometry cells without claiming native execution.

PASS: all eight anchors are distinct, minimum horizontal separation16, radius1.1 clear, intersected exterior cells floor0/ceiling12, z5 vertical clearance. anchors.json records exact positions/encoded and degree yaws, touched cells, geometry/clearance and seven pinned native source hashes/citations. MINSPAWNS remains5; eight attr2=100 starts satisfy the source-derived FFA/deathmatch spawn prerequisite. This is not actual dedicated mode selection or final squad grouping.

PASS: `python3 -B -m unittest discover -s web/assets/network-profile/tests -p 'test_*.py' -v` —12 tests in1.815s. Determinism is independently checked by building two temporary roots and comparing full manifest/report/all79 byte strings. Negative cases include missing/extra files, changed config/notices despite updated hashes, wrong attr2/yaw/duplicate position/revision, altered header/extra/light/RLE, forged provenance/license/runtime/report, unsafe paths/symlinks, gzip CRC/truncation/trailing data/mtime and a >1MiB decompression bomb. No source edits or native tools in fixtures.

PASS: source syntax inspection and actual generated pack `validate(...)` PASS; generation/validation under a subprocess-forbidding mock made zero compiler/game/server/network calls. `verification-evidence.json` contains identical before/after6396 protected old pack/helper/build/output/cache/audited-native-source fingerprints. T060 frozen files and original revision1 profiles/out remain unchanged. All execution was Python stdlib plus hash-checked inspected original helpers. No CubeScript evaluation, compiler, browser, native decoder, server, dependency acquisition, network, package tool or active overlay occurred.

NOT RUN: actual native CGZ decode, dedicated mode selection/rotation, native spawn/gameplay, browser runtime/audio/model rendering, genuine multiplayer. DATA alone does not establish these; MAIN must accept/pin/stage separately. T063 ENet-only original revision1 baseline is unchanged.

## Frozen identities and reproduction

| Repository-relative file | SHA256 |
| --- | --- |
| web/assets/network-profile/manifest.json | c9ecfa62f7e4ca7111a9d3a23a9c97b906d11399d32f6f312463c6697a3359d7 |
| web/assets/network-profile/pack-root/packages/maps/dev_outbreak_browser.cgz | 856173969726f632812fd8ebd2ada746831d7e81f7452dd98f7235a2bd398134 |
| web/assets/network-profile/anchors.json | cd3d6c4ce73f13c0347ec3b095af4dde59e9b740ce52573592ecce26678a5b75 |
| web/assets/network-profile/build_network_profile.py | 342fd0dfc170f0ca5d2bfabac0c7d49b9d6d46481f019376952601148047d409 |
| web/assets/network-profile/map_format.py | 9d52664cd5ed8fc451bb7b60a50efd40ceae7e1924fe7e0721a4d9f2e915385e |
| web/assets/network-profile/validate_network_profile.py | 31d15e6d46b43fd06a99ebea2831099f67c9460f2b7850da55ccbf754c9689f0 |
| web/assets/network-profile/tests/test_network_profile.py | 68277afd91eefcf2505b05a4ab537a2ece831e161fdd2192cef68b67e7e6b33c |
| web/assets/network-profile/validation.json | b30995fba12e40cbce2f157a27f8ced26e8ac90d5538a12a82d82efd35e9c6e2 |
| web/assets/network-profile/verification-evidence.json | c98a9853d47424386c6f578967ad60f55d4508308476da679dcb09b6f0b6526d |

Read-only verification: `python3 -B web/assets/network-profile/validate_network_profile.py`. Generation after inspection: `python3 -B web/assets/network-profile/build_network_profile.py` (writes only its isolated owned pack/manifest/anchors). Tests as above. No runtime/build acceptance requested or asserted by the data handoff; authoritative ticket status remains MAIN-owned.
