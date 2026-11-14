# T147 — Final frozen delivery under D178

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket: T1471.0 / SHARED_HASH_FOUNDATION0.1 / D174. Final append-only freeze clearance D178 read and followed. Authoritative acceptance remains MAIN-owned.
- Base/shared edits: unchanged from review-ready handoff; no Git/status or clean-checkout claim. Exclusive production ownership remains AI-Director; no transfer/integration implied.
- New changes after review-ready: only attempt-1/{final-inventory.json,final-receipt.json,final-freeze.json} and this new handoff. Every reviewed source/harness/doc/attempt/dependency byte was preserved. No source correction, compile/link/test rerun, cache regeneration, project import, runtime/network/app/browser/server or old driver invocation.
- Prior review-ready handoff: `notes/handoffs/T147-AI-Director-review-ready-1.md`, SHA256ae85267d33cb20b2e150c568631d574222663b734f939bbf196f9f62b6b2f13f. It contains per-criterion evidence and all eight reviewed source/harness/doc identities; those identities are also verified/bound by the final freeze.

## Final freeze evidence

All paths below under tests/outbreak/hash/T147/attempt-1 unless otherwise stated.

| Append-only artifact | SHA256 |
| --- | --- |
| final-inventory.json | 97e9e087449a08a8a97352039b55eca2b29bf69581703fa3342fafcf9c019ff8 |
| final-receipt.json | feb2d90440adac4ea56de5ab475b9bc336a927e24749780af2542c4492a94350 |
| final-freeze.json,869348 bytes | 2308ef47860b8288492293925e88bbe25cf4e08f400e132ed31f094fd7d82132 |

PASS — final manifest binds complete owned tests/outbreak/hash/T147 tree plus source/outbreak/{p1_types.h,p1_hash.h,p1_hash.cpp}, including all eight reviewed production/harness/document files, original plan/process receipts, corpus/cases/expected/native/Wasm outputs, objects/executables, compiler dependencies, copied sysroot/cache/temp/log metadata and final inventory/receipt. Final included membership:1959 regular files,117 directories,0 symlinks; regular-file bytes62096222. No other package exclusions.

The ONLY self-slot exclusion is `tests/outbreak/hash/T147/attempt-1/final-freeze.json`. Its869348 bytes and identity are separately published above, avoiding circular content hashing. Adding that self file gives1960 regular files/62965570 regular-file bytes physically across the stated roots;117 directories remain. This new handoff is a separate notes delivery wrapper that binds the freeze, not a member of the package graph.

PASS — inventory explicitly records historical pre-self-slot directory metadata. Final receipt was written, freeze self-slot exclusively reserved, THEN final directory metadata/membership recorded. Final freeze writes into that existing slot. Read-only post-write traversal exactly matched the captured final graph, including directory metadata. File kind/mode/uid/gid/dev/inode/nlink/size/mtime/ctime and SHA256 are recorded; atime is explicitly excluded because reads may change it. No project code was imported to inventory: only inspected inline Python standard-library pathlib/os/stat/hashlib/json, writing the three new approved append slots. Occupied slots would refuse, no overwrite/retry.

PASS — external authority receipts are bound separately from owned membership:

- D178 `notes/decisions/D178-T147-reviewed-freeze-clearance.md`: SHA256557aa86014c62e763f9c843a5f7f4256831e24eb586c533858f67841198f0d9c.
- MAIN independent receipt `notes/reviews/MAIN-T147-independent-review-1.json`: SHA25643359910bc62ccd81c731e5f4cf237282ceb18f349a841cd0472eee5f162d545.
- Governing SHARED_HASH_FOUNDATION, T147 ticket and prior review-ready handoff also bound externally. Authority identities/metadata remained equal across final freeze.

## Implementation and acceptance limits

Unchanged real production hash/core module from review-ready:340 independent-oracle cases,334 successes/six refusals, native/Wasm raw outputs equal; MAIN independently recomputed the full corpus/hashlib results and found no source findings. No additional compiled execution occurred during this freeze. Final freeze PASS means exact package identity/append-only handling, not self-acceptance or a new runtime test.

No formal crypto audit, full typed API/rules/angle integration, P0, gameplay, performance/platform or human acceptance follows. Existing source ownership/gates/QA pause preserved. No owned process remains live. This delivery is final frozen for MAIN acceptance; stop/standby, no further edits or execution without a separate assignment.
