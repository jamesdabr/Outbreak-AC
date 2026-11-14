# Ticket handoff — T291 Swamp seed and successor source ready

- Worker: Player /01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T2911.0 / STOCK_FIRST_PROTOTYPE0.6 / D491; current ticket/contract reread before submission. T288 accepted notes inspected. Authoritative status unchanged.
- Base/pre-existing edits: current local12 launcher/wrapper and reviewed native3/cleanup helpers preserved. No Git/branch/commit action. Baseline play_local.py SHA256b8e5ba799b388b267923f109cc7f4700fd8ff1925eebfaca8d2bf47bee7d2519; gateway_local.cjs SHA256987f868e4622de68c5b6556aae8603179d0b7fc8744b6f18e9be9a05936bd630.
- Changed files: ONLY web/visible/play_local.py, web/visible/gateway_local.cjs; NEW web/visible/seeds/swamp-1/{packages/maps/servermaps/ac_swamp.cgz,config/maprot.cfg,notices/swamp/PROVENANCE.json}; own new diff and this handoff notes. No scripts/other files in the seed.
- Patch reference: notes/handoffs/T291-player-source-diff-1.md. No commit.

## Acceptance evidence

PASS finite inspected stdlib one-time exclusive seed creation and byte readback, no project/helper imports. Source CGZ was ordinary/single-link,23987bytes and matched the pinned original SHA before copying. Output creation refused an occupied seed root and used exclusive files with mode0644. Readback checked bytes/hash/mode/nlink, exactly three files/six required parent directories, no symlinks or extras.

| Seed-relative path | Bytes | SHA256 |
| --- | ---: | --- |
| packages/maps/servermaps/ac_swamp.cgz |23987|acb8d878f90fb4dfa1a53aa69b4500282bace127fe426a658f348a70a4fde9aa|
| config/maprot.cfg |110|9769eb5c2da7eb813e199ea981e7c86c46eff418c97f3abfd89775a6d7bfeb9a|
| notices/swamp/PROVENANCE.json |1486|4652125271f098fad58c1c30c86e3b6950e28667010633582907a5696f6933bc|

CGZ is byte-identical to packages/maps/official/ac_swamp.cgz. Provenance records actual title “ac_swamp by Undead & ExodusS”, format10/revision179, source identity/hash, automatic embedded configuration, exact embedded cc-by-nc-sa-3.0 notice/comment, native mount and rotation mapping. Local/private only; it does not grant redistribution or apply map permissions to separate media. No external map CFG or new license file added; authored geometry/config/entities unchanged.

Rotation is exactly the existing Blackwood dm literal with only the first map token replaced:

```
ac_swamp dm weight:100 repeat:100 time:2 mintime:2 maxtime:2 minplayers:0 maxplayers:8 maxteamsize:8 manual:0
```

Final LF retained; remaining bytes match the original rotation suffix. Archived stage.py ROTATION/SEED_ROWS were only read as source data, never imported/edited.

PASS source readback/stdlib AST parsing, without launcher import/execution: fixed RUN local13 in both files; bundle route/disk root candidates/swamp-1/bundle; exact fixed three-file seed lengths/hashes/rotation. Validation rejects wrong membership including empty extra directories, symlink/special/type/hardlink/mode mismatch and missing/changed bytes before reading bounded file contents. Source rejection branches were inspected, not dynamically exercised by a new test framework.

AST comparison confirms native BASE/debug binary/NODE/PAGE_ROUTE/NATIVE_ARGS unchanged; drain/spawn/observe/send_term/HTTP handlers and the entire session creation/lifetime/capability/shutdown/reap/resource cleanup try/finally remain identical. Wrapper differs only in comment and fixed local13 RUN. Two one-use page allocations, loopback/Origin/Host/ports,30min/1830s cutoff,1790000ms gateway timeout and log bounds remain unchanged.

Final source identities:

- web/visible/play_local.py SHA256 `14b54f153add27af22a2ae1f85970f47dc00b97fbda6d9bfa4ec04902039e5d2`
- web/visible/gateway_local.cjs SHA256 `505f2b00911047bc424e53f495c184d33f23f2d484eec944d925b65a6a0cc072`

## Implementation status

Implemented source/data only. Successor reuses the unchanged verified native3/debug binary/framework paths and reviewed cleanup helpers. Old Blackwood candidate runtime-seed/SEED_ROWS/ROTATION are no longer used for successor map selection. Native seed copy now contains original Swamp CGZ, rotation and provenance; ordinary server config/log directories are created by unchanged existing runtime code.

SIMULATED: none. No new tests/proof framework. No unsafe filesystem node generated.

NOT RUN: launcher (including --execute), wrapper/Node, helper/build/verifier imports, FFI/compiler/build/game/browser/services/network/Git. No run/local13 reservation, capabilities, child process, socket or runtime result created. Existing local12 process/run/logs/seed and all archived builders/controls/manifests/candidates/native assets remain untouched. Current live local12 still uses its already-loaded source and captured routes; this worker did not signal or query it.

## Integration and questions

No source/data blocker remains. MAIN must review the stable seed/launcher alongside T289 source and T290346-file pack, author/build the Swamp bundle and matching page, and separately authorize successor execution. Same ports mean existing local12 lifecycle remains MAIN's responsibility; this ticket does not stop or replace it. Actual Swamp map179 load, scenery/sky/audio, join/spawn/player/guns and cleanup remain runtime checks before expansion. No map expansion or wider QA release. Stop stable; no live worker process or further source work.
