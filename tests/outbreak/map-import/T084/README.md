# T084 bounded dry-flat import foundation

Authority: T084 revision 5.7, PORTABLE_FORMAT_FOUNDATION revision 0.1 / D079.
Production API is exclusively source/outbreak/map_import.h/.cpp, namespace ob.
Input is already-decompressed immutable ACMPv10 data with separate valid caller
allocations for cells, metadata and error. No gzip, config execution, actors,
collision queries, navigation or game integration is implemented.

The decoder checks null/size, magic/version/header/factor/entity bounds,
revision/dry-water/no-inline-config, capacity, bounded informational metadata,
allowed entity records and the complete row-major SOLID/SPACE/repeat stream.
All output is deferred until a successful complete first pass. The second pass
uses the identical immutable input and one previous-cell record. No allocation,
large scratch array, mutable global, exception, external I/O or platform library
is used by production code. Signed fields are decoded with explicit arithmetic.

Failure classifications used by the implementation:

| Error | Rejected condition |
| --- | --- |
| Null / Size | null raw/cells; raw length outside 980..1048576 |
| Magic / Version | non-ACMP or version other than 10 |
| Header / Factor | header size outside bounds/available bytes; factor outside 6..8 |
| Entities | count/range/offset or invalid allowed entity fields |
| Revision | revision outside 1..INT32_MAX |
| Unsupported | wet/inline config, metadata flags other than 65, entity kind other than LIGHT/PLAYERSTART, cell vdelta/tag |
| Capacity | fewer than side² available output cells |
| Metadata | malformed length/NUL terminators or more than 16 informational records |
| CellType / CellData | unknown ordinary cell kind; truncated cell or invalid floor/ceiling |
| Run / Trailing | repeat without predecessor/count, zero/overshoot; any payload after exact side² cells |

This is the known owned dry-flat subset. Texture/material bytes are ignored as
nongeometry only; relevant geometry modifiers are rejected. Legacy entity starts
are inspected/skipped and cannot replace canonical Q10 deployment anchors.

Verification uses the same production .cpp for native, ASan+UBSan native and
direct Wasm. Test-only wrapper buffers are static and distinct from production
stack. Every failure compares every destination/control/canary byte with its
sentinel, without using a preservation hash. Success checks all cell fields,
metadata, input immutability, surrounding canaries and untouched trailing cells.
The Python oracle independently uses struct and integer/grid logic. Owned T064
and T080 maps additionally compare against independently constructed source
geometry grids, not a decoder-generated cell hash. No old helper is imported.

The one-shot `verify.py` records exact commands/environment/tools/inputs before
execution, copies the inspected existing sysroot into its own attempt cache and
uses explicit named Wasm test exports with no runtime imports. It does not call
Emscripten's driver, fetch libraries, build ports or launch services. Existing
SDK/game/assets/native artifacts and numeric source are preservation inputs;
unconsumed test controllers and other workers' new source are not dependencies.

Inspect verify.py/wrapper.cpp/wasm_runner.mjs before execution. Evidence output
directories are once-only; never overwrite a submitted attempt. See the final
handoff and attempt result for actual PASS/FAIL/NOT RUN, tool flags and preserved
failures. Native engine rendering, shared capsule/navigation, gameplay, full P0/P1
and human MVP gates remain outside this foundation.
