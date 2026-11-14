# T290 corrected generation release after pre-write guard failure

- Author / worker: AI & Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket and revision: T2901.0.
- Contract: STOCK_FIRST_PROTOTYPE0.6 /D491.
- Exact clause: one exclusive generation; no retry.
- Status: OPEN (lead resolution recorded separately).

## Question

May MAIN release one corrected generation after the authorized attempt failed before writes? The source now uses exact-line membership for the CFG duplicate guard. No retry has run, no scope/content/count change is proposed.

## Evidence and impact

Command: `python3 -I -B web/assets/swamp-profile/assemble.py`, repository root, exit1.
Trace: `main()` line127 -> `need()` line32, `ValueError: unexpected CFG`.
Original guard `all(line not in cfg for line in addition.splitlines())` mistook approved new `scriptcontext MAPCFG mapmodel`/`mapsound` as present because the base has `mapmodelreset`/`mapsoundreset`. This is my assembler defect, not a source/contract conflict. Corrected to `all(line not in cfg.splitlines() for line in addition.splitlines())`.

Failed assembler SHA256: `52120c7273f4da5e80973db041616b9c27252ba1667f0d05791a89c3ec7d899d`.
Failure occurs before conversion loop and before `pack.mkdir()`/exclusive writes. Fixed read-only existence checks confirmed pack-root, manifest.json and PROVENANCE.json absent. Only new assembler and README sources exist under profile. No original input modified, no cleanup or overwrite performed.

Prior finite read-only closure checks passed:230media/17notices/249new/no base overlaps, expected114JPEG/onePNG/55CFG/51MD3/nineOGG; all input sizes and shared model rows consistent. All17 notice text views match inventory, using UTF-8 replacement only for metadata display (original notice bytes remain unchanged).

## Options for owner and lead

Recommended: inspect the single-line exact-membership fix and explicitly release one corrected exclusive generation at unchanged new output paths. Alternative: leave generation paused for independent review. Neither option changes contract behavior.

## Work paused

All generation and output acceptance checks await a new explicit release. Source repair is prepared but not executed. No build/runtime/service/network action is requested. No unrelated work resumes.
