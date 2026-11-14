# T290 — Pre-write assembly failure

- Worker: AI & Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket: T2901.0; STOCK_FIRST_PROTOTYPE0.6 /D491, reread before delivery.
- Base: accepted stock-combat97 manifest `8e8ab354b21260cc2393e5d9cb0da29c860ea869231be11e88e81706719ecd7e`; original input files preserved; no Git commands.
- Changed: ONLY NEW `web/assets/swamp-profile/assemble.py`, README.md, this own handoff and own question `notes/questions/T290-AI-Director-corrected-generation-release-1.md`.
- Commit: none.

## Acceptance evidence

PASS read-only reconciliation:230media+17notices+audio provenance+CGZ=249new, no base97 overlap,346expected. Pinned inventory SHA256 `91d851a4d971d27c370a74160d4d05f6b14167d69622920348b60aed3b25e2a5`; new input identity-set SHA256 `3939e7dd8bb7e569e3c76b71873fc7f1df2491c229f5a8c87709ac959544ae9d`. Full own assembler inspected before execution. No project helper imported or executed.

FAIL the sole authorized command `python3 -I -B web/assets/swamp-profile/assemble.py`: exit1 before writes, `ValueError: unexpected CFG` at line127. Faulty substring guard treats existing mapmodelreset/mapsoundreset as new mapmodel/mapsound commands. Exact-line fix prepared; no rerun.

PASS fixed existence checks: pack-root, manifest.json and PROVENANCE.json were not created. No cleanup/overwrite/original mutation. NOT RUN:346 output closure/hashes,135 byte-copy checks,114pixel equality checks, resulting CFG check; execution stopped before output generation. No successful pack count/bytes/hash claimed.

## Implementation status

Implemented: assembler and README source, with single-line guard repair prepared after failure. Simulations: none. Incomplete: actual pack and provenance/manifest. Build/compiler/browser/game/services/network/FFI/install/Git NOT RUN.

## Integration and questions

Open question links exact failure/fix and requests explicit corrected-run release because ticket prohibits retries. No content/interface/parameter/dependency change proposed. MAIN must not build from this absent pack. Stop pending release; all other leases paused.
