# Stock player profile — T282 / D479

Separate fixed 90-file `/outbreak` pack: accepted Blackwood84, replacing only
`config/browser.cfg` with the exact three additional MDLCFG permissions
`md2tag`, `mdlshadowdist`, `mdlcachelimit`; isolation and `sealcontexts` remain.
The other 83 base members are copied byte-for-byte.

Six additions under `packages/models/playermodels/`:

- Original `tris.md2`, `md2.cfg`, `license.txt`, unchanged bytes.
- `skin.png`, `CLA/01.png`, `RVSF/01.png`, lossless copies of the decoded RGB
  pixels of the matching bundled JPEGs. No resizing, recoloring, palette,
  orientation or color-profile transformation; JPEG compressed bytes are not
  claimed identical. Both decoded RGB and RGBA equality are checked.

**Stock files are not MIT.** The original bundled notice is preserved exactly
at `packages/models/playermodels/license.txt`. It identifies Darren Pattenden
and Markus Bekel and directs non-personal use to the author. This profile is
for the D479 private local prototype only; no public redistribution is
authorized. Existing base entries retain their own notices/licenses. The base
root LICENSE does not relicense stock additions.

One inspected local assembly command:

```sh
python3 -I -B web/assets/stock-player-profile/assemble.py
```

Assembly completed once with exit0 using installed Pillow11.1.0:90 files,
936,614 raw pack bytes. All three skins retain native320×200 decoded pixels;
RGB and RGBA equality, all copied bytes/hashes and exact CFG delta passed.

Uses installed Pillow and stdlib only, fixed source/output paths and pinned
inputs. Imports no old project generator/validator. Refuses existing output
pack/metadata or symlinks, writes exclusively, preserves partial output on
failure, and does not overwrite, clean or retry. Finite checks verify90 exact
members, all bytes/hashes, copied bytes, decoded native-size skin pixels and
the exact CFG delta. `manifest.json` keeps the current mount/entries shape;
`PROVENANCE.json` records input/derived hashes, transforms, Pillow version,
per-file rights and observed checks.

Original assets and packs remain untouched. No build, engine/browser/runtime,
network, dependency install or fixture framework. MAIN reviews/integrates the
new manifest and exact90 count separately; old 84-file build configurations
are not silently changed. Stage1 is original player/skins; stock weapons and
map selection/expansion remain separate work.
