# T282 — Original player/skins pack delivered

AI & Director · T2821.0 · STOCK_FIRST_PROTOTYPE0.1/D479. Mandatory docs, full contract/ticket and assembler inspected; ticket/contract reread before delivery. Only new `web/assets/stock-player-profile/{assemble.py,README.md,manifest.json,PROVENANCE.json,pack-root/**}` and this handoff written. Originals/old packs/source/candidates/SDK untouched; no Git operation.

**Generated exact90 pack files**,936,614 raw bytes, mounted at `/outbreak`:83 byte-identical Blackwood members,1 browser.cfg override,3 byte-identical stock MD2/CFG/license files and3 lossless decoded-pixel PNG skins. One authorized assembly invocation,exit0,no retry:

```sh
python3 -I -B web/assets/stock-player-profile/assemble.py
```

Installed Pillow11.1.0; no dependency install/project generator imports. The inspected fixed-path assembler refuses existing output pack/metadata and symlinks,uses exclusive writes,preserves failures,has no subprocess/network/build/runtime behavior.

Actual checks **PASS**:90-member exact closure,all file sizes/hashes,83 unchanged base copies,original `tris.md2`/`md2.cfg`/`license.txt` byte equality,all3skins’ native320×200 decoded RGB **and RGBA** pixel equality,exact three whitelist additions,original-input byte preservation and metadata readback. No resize/recolor/palette/orientation/color-profile transform. JPEG compressed bytes are not claimed identical to PNG.

CFG diff is exactly these additions before retained `isolatecontext MDLCFG`/`sealcontexts`;all other CFG bytes unchanged:

```text
scriptcontext MDLCFG md2tag
scriptcontext MDLCFG mdlshadowdist
scriptcontext MDLCFG mdlcachelimit
```

Frozen stock paths under `pack-root/packages/models/playermodels/`:

| File | Bytes | SHA256 |
|---|---:|---|
|tris.md2|249676|4b4c61f40c62f612f488eec644cd41dce151790b1eb9da39c4b16b6e9fd040eb|
|md2.cfg|97|5ba275c4e01b8d45dcde81f6261f3e31666329bf7b6fc0b19699cb0223068827|
|license.txt|1431|f7489171be41ac97871dfd78fb384f524873c5c497b54999884aff876f311a36|
|skin.png|82842|48636afee683bc9452bf32c68c2ff3723dc2e76e94ddc7ef771a7d6534ea0b11|
|CLA/01.png|107638|d6ba5e2a7a0c6646964ebd1831c6ec6294682fa712cb97e44843e19a1379e0fe|
|RVSF/01.png|82842|48636afee683bc9452bf32c68c2ff3723dc2e76e94ddc7ef771a7d6534ea0b11|

Manifest retains current top-level/mount/entries shape and accurate per-file notices/source hashes. `PROVENANCE.json` records all input/derived identities,three pixel hashes/dimensions/transforms,CFG delta and observed finite checks. **Stock is not MIT:** exact bundled personal-use notice preserved,identifying Darren Pattenden/Markus Bekel;all six additions point to it. D479 authorizes private local prototype only,no public distribution. Existing base notices remain unchanged;root MIT notice does not relicense stock material.

| New metadata | Bytes | SHA256 |
|---|---:|---|
|manifest.json|53357|812a3d822e290774cef051a040bdeb03fd1b47f431fe53b7fef2537b5217ce37|
|PROVENANCE.json|24917|168d22cf75c3e9a8fc9bf99ad59a78cda31f865436280cc6a4df4c20db0c5efd|

Assembler SHA2567b8d8e5337d1045c4d68b88a66c5ded9418753fcca79f3c6811144e70f486cab. Source Blackwood84 manifest unchanged at8c4f7eef5f0deafb06bec60d62be529a684a30d56bbdc6dc3e5f38dd21c69e60.

No fixture framework,engine/compiler/browser/runtime/FFI/network execution or build-config edits. No rendered-player/playable/game acceptance claimed. MAIN reviews the generated pack and separately integrates the new manifest/hash/90 count with T280’s fixed paths;old84-file build configs remain untouched. No question:expected90 matched. Stable handoff,STOP;guns/maps and paused unrelated work not resumed.
