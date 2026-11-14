# D017 exact stack and source-proven world/entity buffer alias

- Author / worker: Engine & Multiplayer
- Ticket/revision: T040 1.3 with D017 diagnostic addendum 1.4
- Governing baseline: browser foundation/GOVERNANCE/P0 0.5; D006/D009 unchanged build
- Exact affected clause: read-only diagnosis only; worldio.cpp is outside Engine's source allowlist
- Status: OPEN (lead resolution recorded separately)

## Question

Please review and release a narrow loader fix for `source/src/worldio.cpp:1058`.
On the browser startup path, the resource-index table remains empty and this
line replaces the correctly allocated world array with the entity-vector
buffer immediately before world decoding. This is the strongest source-backed
cause of the measured allocator corruption. No speculative fix was applied.

## Exact runtime attribution

The single D017 relink added only --emit-symbol-map and changed output dir.
Its final Wasm SHA-256 **exactly equals D016**:
`6165af498f65cc7a51a877801679978a5672fea7c78f27c1ae143cd09c1ab229`.
Therefore the original function indices are safely mapped:

`3179 emscripten_builtin_malloc -> 3202 operator new(unsigned long) ->
1694 loadfile(char const*, int*, char const*) -> 775 execfile(char const*) ->
2001 load_world(char*) -> 1064 main`.

At exact original trap offset **0x1714c9**, disassembly reads:
`local.get 0; i32.load offset=4`. The adjacent operations mask off low chunk
flags and traverse child pointers at offsets 16/20. This corresponds to
reading a dlmalloc tree-chunk header (`chunksize(t)`) through an invalid chunk
pointer, not an engine GL instruction or normal new[] buffer write.

`loadfile` calls new[] at stream.cpp:1097 (`new char[len+1]`), matching call
3202 at 0xaf316. In load_world, 0xcc072 is the **first** execfile call after
the map title log: worldio.cpp:1102 `config/default_map_settings.cfg`.
The trap happens while allocating that config's input buffer, before that
default config is interpreted. Its commands therefore cannot be the earlier
corrupting operation in this observed stack.

## Source correlation

1. world.cpp:247 defines `mapinfo` and its alias `resdata`. tools.h:567–574
   initializes the table with numelems=0.
2. The only located population path is main.cpp:564–567 setresdata(), called
   from the native startup resource-file loader at main.cpp:1938–1948.
   Browser `main` returns browsermain() at 1702–1703 in the diagnosed source;
   browsermain does not run that native resource-index path. The original
   pack intentionally supplies no inherited stock resource-index file.
   setmapinfo() elsewhere updates unrelated license/comment strings.
3. worldio.cpp:1056–1058 calls setupworld(hdr.sfactor), then evaluates
   `if(!mapinfo.numelems || (...)) world = (sqr *)ents.getbuf();`.
   With the table empty, it redirects world to the entity buffer.
4. setupworld (world.cpp:656–663) had allocated/zeroed a real sqr[mipsize]
   array and assigned wmip pointers to it. The alias line discards that world
   pointer; it does not resize or retype the entity vector allocation.
5. worldio.cpp:1071 passes the substituted pointer to rldecodecubes. That
   function writes sqr fields/16-byte memcpy repeats until cubicsize cells
   are decoded (worldio.cpp:172–242).
6. The unchanged accepted map's raw header is ACMP/version10, factor6,
   nine entities. It decodes 4096 16-byte sqr records = **65536 bytes**.
   Its accepted map SHA remains
   c3f0226abdf143474804d9259428eb9ba641b3ac259251bdafef04962d5cb52d.
   Entity storage is a different allocation/type; no world-sized reserve is
   performed there. Subsequent map stats/light and logged title precede the
   allocator trap while opening default config.

Static source establishes an invalid world write destination on this browser
path. Actual instruction mapping establishes the later allocator-header fault.
No heap snapshot/watchpoint was taken, so the exact runtime chunk pointer,
allocation capacity, and first corrupting store have not been dynamically
measured. This diagnosis does not claim an instrumented root-cause test.

## Options for owner and lead

Release the exact browser/offline loader allocation ownership correction,
preserving the actual setupworld allocation and native behavior, with an
explicit approved original-pack validation policy if required. Missing or
invalid metadata should be handled explicitly rather than aliasing cube
writes into entity storage. Do not fabricate checksum-table entries, increase
heap size to mask the overwrite, or change the renderer/asset format.

An exact loader ownership test plus rebuilt real browser run should then
verify recovery; successful static mapping alone does not prove startup fixed.
Engine cannot edit this source under T040.

## Work paused / evidence

Only a source fix/new integrated artifact waits for MAIN's decision. D017
diagnosis is complete. The original web/build/out and all QA evidence remain
unchanged; no browser/server was launched. Evidence is under
web/build/generated/t040/symbol-map/: relink-result.json, index.html.symbols,
mapped-stack.json, fault-instructions.txt, loadfile-callsite.txt,
load-world-callsite.txt and source-correlation.json. One diagnostic relink was
performed; no other build flags/ports or source edits were used.
