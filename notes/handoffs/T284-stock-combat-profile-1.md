# T284 — Original pistol/rifle pack

- Worker: AI & Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket / revision: T2841.0 RELEASED; reread before generation/submission.
- Contract: STOCK_FIRST_PROTOTYPE0.3 /D483; revision unchanged on reread.
- Base / pre-existing edits: accepted stock-player90 manifest SHA256 `812a3d822e290774cef051a040bdeb03fd1b47f431fe53b7fef2537b5217ce37`; new output directory confirmed absent. Existing project files preserved. No Git commands.
- Changed files: ONLY NEW `web/assets/stock-combat-profile/{assemble.py,README.md,manifest.json,PROVENANCE.json,pack-root/**}` and this own handoff. No commit authorized or made.

## Acceptance evidence

Read mandatory governance/product/parameter/interface documents, assigned contract/ticket, original weapon configs/license, accepted base assembler/config and source hashes. Fully inspected own final assembler before execution; no old project helper imported/executed.

Executed exactly once from repository root:

```sh
python3 -I -B web/assets/stock-combat-profile/assemble.py
```

Exit0, installed Pillow11.1.0. No retry, cleanup, install, subprocess or external call.

- PASS exact97 filesystem/manifest closure, all written bytes/lengths/hashes and metadata readback;1,169,695 raw pack bytes.
- PASS89 base files copied unchanged, one approved browser CFG override, seven new weapon files.
- PASS5 original byte copies: pistol and assault world MD2/config plus weapons/license.txt.
- PASS2 actual written PNGs match original JPEG decoded RGB and RGBA pixels: pistol128×128, assault256×128. No resize/recolor/orientation transform. Compressed JPEG and PNG bytes are intentionally distinct.
- PASS exact five-line CFG addition, independently inspected with fixed `diff -u`: `keymap 49 1`, `bind 1 [weapon pistol]`, `keymap 50 2`, `bind 2 [weapon assault]`, and `scriptcontext MDLCFG md2emit` before MDLCFG isolation/seal. All other bytes preserved.
- PASS all original inputs re-read unchanged at assembly completion. No new audio.
- PASS original weapon CC BY-NC-SA2.5 Markus Bekel/makkE notice copied unchanged; inherited player personal-use notice copied unchanged. Stock is not MIT; local/private scope only, no public distribution authorization.

Stable metadata SHA256:

| File | Bytes | SHA256 |
|---|---:|---|
| manifest.json |58703| `8e8ab354b21260cc2393e5d9cb0da29c860ea869231be11e88e81706719ecd7e` |
| PROVENANCE.json |26900| `91dc44e87d424562d0ecd3613cd7e2d8270c891569b6498eef35bdf17bdcc1a6` |

Assembler SHA256: `ef7cffa188300db7a9cebd92fd32018796b9c733584c753ee2453fd288f138a3`.
PROVENANCE records source/derived identities and decoded pixel hashes; manifest retains current mount/entries schema and `/outbreak` mount.

## Implementation status

Implemented: actual local97-file asset pack and finite data verification. Simulated behavior: none. NOT RUN: source/compiler/build/browser/runtime/network/FFI. No weapon attachment, selection, firing, reload, movement or gameplay acceptance claimed. Sound remains separately incomplete.

## Integration and questions

MAIN integrates this new manifest/pack with separately owned T285 source, then builds/observes runtime. No existing builder/profile/source changed; no dependency or shared interface added. Do not rerun exclusive assembler into existing outputs. No unresolved data conflict. STOP after this handoff; other leases remain paused.
