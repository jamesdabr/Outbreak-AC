# T040 D017 exact-byte startup trap diagnosis

- Worker: Engine & Multiplayer
- Assignment: T040 1.3 with D017 additive diagnostic 1.4; no scope/status edit
- Allowed execution: ONE same-object diagnostic re-link, only --emit-symbol-map added and separate output directory; offline symbol/source inspection
- Changed files: new generated evidence under web/build/generated/t040/symbol-map; own question T040-engine-world-allocation.md and this handoff. No engine source/header, original output, QA evidence, profile/flag/port/pack change.
- Base: D016 artifact T040-3800e5ef78bcb84033e30c72e276ebebc342b6f97185fbfcb434de021d87a7ab, 61 accepted objects from attempt-1, same source/config/shell/original pack.
- No commits/push/reset/revert, browser/server/game launch or other-worker message/dispatch.

## Diagnostic results

| Requirement | Result | Evidence |
| --- | --- | --- |
| Read D017/ticket and inspect exact SDK symbol-map behavior | PASS | Read link.py:2434–2440 and building.py:1144 onward; map emitted from names, then name section stripped. No debug/behavior flag added. |
| Exact accepted objects/args/shell/pack, one re-link | PASS | All 61 objects and every recorded source/config/pack input checked before execution. relink.py and relink-result.json record original and diagnostic argv plus original environment. Only --emit-symbol-map and output directory differ. One invocation, exit 0. |
| Diagnostic Wasm exactly equals original D016 | PASS | Both SHA-256 `6165af498f65cc7a51a877801679978a5672fea7c78f27c1ae143cd09c1ab229`. Original stack attribution is valid. |
| Six mapped/demangled functions and precise operation | PASS | index.html.symbols, mapped-stack.json, exact-offset disassembly and source correlation below. llvm-cxxfilt invoked for all six names; SDK map already contains readable names. |
| Preserve original out/QA/source; no speculative fix | PASS | All original out files including metadata/notices match before/after/final preservation snapshots. No source edited. MAIN independently assigned the loader fix to Player T042/D019; Engine awaits its accepted stable hash before any new integration. |

## Exact mapped original stack

| Index | Original Wasm offset | Function |
| --- | --- | --- |
| 3179 | 0x1714c9 | emscripten_builtin_malloc |
| 3202 | 0x174f63 | operator new(unsigned long) |
| 1694 | 0xaf316 | loadfile(char const*, int*, char const*) |
| 775 | 0x31048 | execfile(char const*) |
| 2001 | 0xcc072 | load_world(char*) |
| 1064 | 0x4dbd4 | main |

The exact trapping instruction is `i32.load offset=4` after local.get 0 in
the allocator, followed by chunk flag masking and tree-child traversal at
offsets 16/20. It reads a dlmalloc chunk-size header through an invalid tree
pointer; it is not a GL call or an application read of the newly allocated
config buffer. The SDK malloc_chunk::head field is at +4 for this Wasm32
layout. dlmalloc's tree-chunk chunksize traversal is the matching source
operation; optimized output has no line-level DWARF, so no fabricated exact
allocator C line/heap pointer value is claimed.

loadfile's 0xaf316 calls new for `new char[len+1]` (stream.cpp:1097).
load_world's 0xcc072 is the first execfile call after the two map-read/title
logs: `execfile("config/default_map_settings.cfg")` at worldio.cpp:1102.
The next map-specific execfile call is 0xcc07a. Therefore this trap occurs
before the default map config is interpreted. The title log is from
load_world, not proof that that config had already executed.

## Source-backed corruption cause

world.cpp:656–663 allocates/zeros a real sqr[mipsize] world array and installs
its mip pointers. worldio.cpp:1058 then redirects world to ents.getbuf()
when mapinfo.numelems is zero, immediately before rldecodecubes writes the
map. The global table starts empty (world.cpp:247, tools.h:567–574). The
located population path is the native resource-index startup in
main.cpp:1938–1948; browser main returns browsermain at 1702–1703 and does
not execute it. setmapinfo elsewhere manages unrelated comment/license
strings, not that table.

The accepted map header is ACMP/version10, factor6, nine entities: 4096
16-byte sqr records, so decoding writes **65536 bytes** through the aliased
entity allocation. setupworld's genuine world allocation is discarded from
the world pointer without resizing/retyping entity storage. This provides a
specific earlier heap overwrite consistent with the observed subsequent
allocator-header fault. The exact first runtime corrupting store/chunk value
was not instrumented; the proven symbol attribution and source ownership bug
remain distinct from dynamic recovery evidence.

Question T040-engine-world-allocation.md records exact paths/limits and no
implementation. MAIN has now independently selected the same concrete
candidate and assigned T042/D019. No allocator rewrite, larger-memory mask,
fabricated resource-index entry or speculative source change was performed.

## Reproduction and retained evidence

`web/build/generated/t040/symbol-map/relink.py` was authored/read before
executing once. It loads the exact accepted attempt-1 argv/environment, checks
all identities, runs em++ with --emit-symbol-map and separate index.html,
then checks final Wasm and original output. Do not rerun it: D017 authorized
one diagnostic relink and the script refuses a second completed attempt.

Retained files in that directory:

- relink.py, link.log, relink.stdout.log, relink-result.json — exact operation/exit/hash comparison
- index.html.symbols and diagnostic HTML/JS/Wasm/data — actual map and link output
- mapped-stack.json — six original indices/offsets/names and demangler argv
- fault-instructions.txt, loadfile-callsite.txt, load-world-callsite.txt — bounded actual disassembly
- source-correlation.json — read-only accepted map-header facts/byte count
- source-snapshots/ and source-snapshot-check.json — diagnosed engine bytes, copied only when matching accepted D016 hashes
- final-preservation.json — final original output preservation check

Only LLVM offline disassembly/demangling, own stdlib inspection and the one
approved compiler link ran. No actual browser run, sanitizer build, new flag,
port acquisition or source edit. Actual startup recovery, frames/rendering,
motion/collision/audio/models/network remain unverified. Keep D016 original
outputs frozen until MAIN accepts T042's stable source and authorizes the
next same-profile T040 integration attempt.
