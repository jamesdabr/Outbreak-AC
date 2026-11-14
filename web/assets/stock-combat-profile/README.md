# Original pistol and assault rifle local pack

T2841.0 / STOCK_FIRST_PROTOTYPE0.3 / D483. Exact97-file successor to accepted
stock-player90: 89 unchanged files, one browser CFG override, and seven weapon
additions. Original MD2/config/license bytes are retained; two original JPEG
skins are decoded to native-size PNG with identical RGB and RGBA pixels.

Only CFG additions: MDLCFG `md2emit` before isolation/seal, `keymap 49 1`,
`bind 1 [weapon pistol]`, `keymap 50 2`, `bind 2 [weapon assault]`.
No new audio. Existing profiles and engine sources are untouched.

Weapons are by Markus Bekel (makkE), CC BY-NC-SA 2.5; retain
`packages/models/weapons/license.txt`. Player personal-use notice remains at
`packages/models/playermodels/license.txt`. Stock assets are not MIT. This is
local/private use only; public distribution is not authorized by this ticket.

After reading the complete assembler, the authorized single generation is:

```sh
python3 -I -B web/assets/stock-combat-profile/assemble.py
```

The assembler refuses existing outputs and symlink paths, pins all original
inputs, writes exclusively, checks exact closure/bytes/hashes/pixels/CFG delta
and unchanged inputs, and records source/derived provenance. It imports only
standard Python modules and installed Pillow. No build or runtime is performed.
MAIN owns subsequent integration and observation.

Assembly completed once, exit0, Pillow11.1.0:97 files /1,169,695 raw bytes.
All checks passed. Pistol skin retains128×128 pixels; assault retains256×128.
