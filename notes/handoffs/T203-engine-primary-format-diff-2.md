# T2031.1 focused primary-format notes diff

D337 NOTES ONLY. This modifies only the OWN proposal. Historical handoff/question,
reviews/references and all source stay unchanged. No program/parser/tool probe ran.

Before 46349/b772efdc0c8084788c1c36822aa82cfc7047badaf093b70d6973787c742f7964;
after 67759/649da2463eaa1d0d28d26514d504b961af7f8ded6523a7363465c5c70efb95c0.
Native protocol sections5–7 are byte-identical, SHA256471bb82b65d5aa2a1ff82a4edbf8022954c54573f3121381de59c29094683655.

```diff
--- T2031.0/notes/proposals/T203-image-address-qualification-1.md
+++ T2031.1/notes/proposals/T203-image-address-qualification-1.md
@@ -1,18 +1,21 @@
 # T203 exact linked-data and loaded-image qualification proposal
 
-Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90; T2031.0/D332;
+Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90; T2031.1/D337 (D332);
 MOTION_RECORD_FOUNDATION0.2. **NOTES_ONLY / NOT_ADOPTED / NOT_IMPLEMENTED /
 NOT_EXECUTED / NOT_ACCEPTED.** T200 source is closed and unchanged. D332 selects
 the callable architecture in principle, not the source/ABI/loader replacement.
 
-This selects ONE method: Wasm normal-object relocations plus a same-link-child
-map, checked against every linked operand and initializer; native RTLD_FIRST
+This selects ONE method: Wasm normal-object AND retained final relocations plus
+a same-link-child RAW-NAME map with serialized BSS, checked against every linked
+operand and initializer; native RTLD_FIRST
 absolute-file loading plus a common slide from ALL FIVE qualified regular
 callables, followed by exact named-object equality. No alternate discovery path,
 ignored operand, address guessing, additional child or generic dyld API.
-Capability C1 below is OPEN: the exact installed linker/map/object-format
-source references were not supplied or discovered locally. That is a blocking
-preflight/implementation-format question, not permission to assume support.
+C1's missing documentary basis is resolved by D337's pinned primary LLVM sources
+and accepted G1 clang AND LLD logs at the same revision. Exact current installed
+binary/alias preflight and actual output qualification remain future gates.
+This correction changes only this OWN plan; original1.0 handoff/question and all
+reviews/reference copies remain unchanged historical records.
 
 ## 1. Preserved scope and proposed source disposition
 
@@ -104,8 +107,9 @@
 |i64.const expr|R_WASM_MEMORY_ADDR_SLEB64 (15), only if pinned emitter actually uses it for a memory32 address|EXACT64-bit representation of the same bounded memory32 address A|
 |integer load/store memarg expr|R_WASM_MEMORY_ADDR_LEB (3)|EXACT u32 memory offset A AND exact alignment exponent|
 
-The numbers/record interpretation must be corroborated by C1's fixed primary
-format reference before implementation/adoption, not inferred from these names.
+The numbers/record interpretation are bound to the exact primary WasmRelocs.def,
+Wasm.h, WasmObjectFile.cpp and WasmObjectWriter.cpp references in section4. Source
+defined support is not a passing actual MR build or implementation adoption.
 Memory64, relative/TLS relocation forms, address-as-global substitutions and
 fixed-width relocations on a CODE LEB operand are outside this chosen plan and
 refuse. i64.const is not a license for an address outside memory32. DATA pointer
@@ -152,40 +156,83 @@
 
 Retain each actual normal .o, saved producer .s, .su/.d, plus independently emitted
 diagnostic .s/.su/.d. Compare complete source/definition/frame/dependency/body/call
-unions as T200 requires. Add the same -fdata-sections -ffunction-sections to BOTH
-normal and diagnostic commands, as proposed in section4; require individually
+unions as T200 requires. Add -fdata-sections -ffunction-sections to BOTH WASM
+normal and WASM diagnostic commands ONLY, as proposed in section4; require individually
 named DATA sections rather than infer a symbol's size from the gap to its neighbor.
 
 Supported data assembly declarations are .type sym,@object, exactlyone defining
 label, a literal .size sym,uint, .section .bss/.data/.rodata plus a literal symbol
 suffix, optional .p2align exponent/fill, and bounded byte/short/int32/int64/asciz/
 ascii/skip/zero directives. Bytes are encoded under fixed target LE and exact
-string escape grammar frozen with C1; unrecognized strings/directives refuse.
+string escape grammar frozen in the later source lease; raw object bytes and
+source-qualified exact initializer bytes must agree, and unsupported escapes/
+directives refuse rather than being guessed or used as an address source.
 Pointer-valued directives require their distinct declared pointer-field role
 and actual DATA relocation. No broad interpretation of opaque assembly text.
 All sizes/initializers must match actual object segment bytes and DATA-symbol
 offset/size, plus the independently MAIN-qualified source declaration/type span.
 
 Object Wasm header/version1 and bounded section extents are decoded completely.
-The custom linking section must be unique, version2. Required subrecords are
-SEGMENT_INFO5 and SYMBOL_TABLE8. DATA symbol kind1 has flags ULEB, name UTF8,
-then, for a defined symbol, segment_index/offset/size ULEB fields. Record byte
-offsets/lengths are retained, not merely decoded names. Segment info supplies
-name/alignment exponent/flags; DATA payload supplies bytes. Counts/offsets cannot
-overrun their enclosing custom subsection or actual DATA segments. Unknown flags,
-ambiguous segment names, duplicate relevant entries and invalid extents refuse.
-
-The complete index space includes function/global/section/tag/table symbols.
-C1 MUST freeze the exact LLVM linking-v2 per-kind/name-presence/flag decoder
-from primary source for the selected binary, including undefined/explicit-name
-rules; no guessed skip length is specified or authorized here. This missing
-reference is an explicit remaining format prerequisite. Parsing only DATA while
-guessing how to advance past other kinds cannot implement this plan. Calls,
-types and __stack_pointer still need their exact existing symbol/index joins.
+The custom linking section must be unique, metadata version2 ULEB32. Each nested
+subsection has type u8, size ULEB32 and an EXACT bounded payload; every byte must
+be consumed. SYMBOL_TABLE8 starts with count ULEB32. Each entry starts kind u8
+(known0..5, also the canonical one-byte ULEB emitted by this writer) then flags
+ULEB32. Every entry's raw start/end byte offsets and decoded fields are retained.
+
+Exact per-kind grammar from parseLinkingSectionSymtab and the matching MC writer:
+
+|Kind|Payload AFTER kind/flags|Binding/index/name constraints|
+|---|---|---|
+|0 FUNCTION|element index ULEB32; string if DEFINED OR EXPLICIT_NAME|Defined index is in defined function portion; undefined index identifies its actual function import. Defined name is read; undefined with explicit name reads it and also retains import field/module; otherwise name comes from that exact import. Signature joins its actual type.|
+|1 DATA|name string ALWAYS; if defined COMMON: size ULEB64,alignment u8; if defined non-COMMON: segment ULEB32,offset ULEB64,size ULEB64; undefined has no further fields|Normal segment bounds/offset+size checked against actual segment bytes. COMMON/ABSOLUTE/TLS are decoded correctly then refused by the selected DATA policy; undefined needs exactlyone qualified definition in the other actual object, never a guessed body.|
+|2 GLOBAL|same index/name-presence rule as FUNCTION, using global index space|Type/mutability and exact import identity preserved; undefined weak global invalid. No function/data-as-GOT substitute for qualified __stack_pointer.|
+|3 SECTION|section index ULEB32 ONLY, no ordinary name string|LOCAL binding required; index refers to an actual CUSTOM section, not a numeric section type ID. Name derives from that section; this cannot authorize executable DATA/code.|
+|4 TAG|same index/name-presence rule as FUNCTION, using tag index space|Signature/import identity preserved; undefined weak tag invalid. Selected executable subset still refuses exception/tag use.|
+|5 TABLE|same index/name-presence rule as FUNCTION, using table index space|Element/limits/import identity preserved; undefined weak table invalid. Selected executable subset still refuses element/indirect-call initialization.|
+
+DEFINED means (flags&0x10)==0, not a name-section heuristic. Actual import kind
+spaces are function0,table1,memory2,global3,tag4; symbol kinds above are DIFFERENT.
+Defined/undefined index must agree with the matching imported-prefix/defined
+range, and each index's declared type must agree. No skip-length guess for any
+kind, no reading a name for an undefined nonexplicit indexed symbol.
+
+Known flags: binding mask0x3 GLOBAL0/WEAK1/LOCAL2/COMMON3; visibility mask0xc
+DEFAULT0/HIDDEN4 (other visibility values refused); UNDEFINED0x10,EXPORTED0x20,
+EXPLICIT_NAME0x40,NO_STRIP0x80,TLS0x100,ABSOLUTE0x200. Unknown bits refuse.
+COMMON must not be ABSOLUTE; its one-byte alignment exponent is<=32 in the format
+decoder before the selected-policy refusal. Non-COMMON DATA still carries its
+index/offset/size triple even if ABSOLUTE; decode it and refuse, do not invent an
+alternate short record. Undefined non-DATA name handling is as in the table.
+Nonlocal duplicate names refuse; local records keep object-qualified identity
+and cannot introduce duplicate/ambiguous DATA roles in one object.
+
+SEGMENT_INFO5 payload is count ULEB32 then count entries string(name),alignment
+exponent ULEB32,linking flags ULEB32, in DATA-segment index order. LLVM allows
+alignment<=32; the selected finite image bounds/qualified producer alignment are
+stricter. Count must cover every DATA segment needed by any qualified role;
+missing/ambiguous relevant entries refuse. Segment flags STRINGS1/TLS2/RETAIN4
+are known; unknown bits or TLS storage refuse; STRINGS/RETAIN must match qualified
+source/producer roles and no coalescing. Raw DATA bytes remain independently bound.
+
+INIT_FUNCS6 is count ULEB32 then priority ULEB32,symbol index ULEB32 pairs; index
+must identify FUNCTION. This chosen no-constructor subset requires absent or
+zero-count init list, not an uninspected skipped list. COMDAT_INFO7 is count,
+unique nonempty name string,flags ULEB32 (must0),entry count,then kind/index ULEB32
+pairs (kind0 DATA,1 defined FUNCTION,5 CUSTOM SECTION). Indices must exist and an
+entity cannot belong to two groups. Selected no-coalescing subset requires
+absent/empty groups; nonempty groups refuse rather than lose DATA/body identity.
+TARGET_ARCH9 is one exact string,if present it must be the qualified wasm32 role.
+Unknown linking subsection types refuse even though the generic upstream reader
+can skip some; no executable/initializer meaning is ignored. Calls/types and
+__stack_pointer retain their exact independent symbol/index/type/init joins.
 
 For CODE relocation records, decode unique reloc.CODE custom section, target
 section index, bounded relocation count, and each (type ULEB, offset ULEB,
-symbol_or_type_index ULEB, type-specific signed addend). Offsets are relative to
+symbol_or_type_index ULEB32, type-specific signed addend). In the pinned MC writer
+the relocation type is emitted as one byte for these values0..27; the reference
+decoder reads ULEB32. Accept the corresponding canonical one-byte type and the
+exact declared type-specific fields, not extra padding as an unpriced record.
+Offsets are relative to
 the target section PAYLOAD, including its count/body/locals prefixes; never
 relative to the module or instruction opcode by assumption. Retain absolute
 file offset and function/body/instruction/operand ordinal from the bounded CODE
@@ -206,6 +253,30 @@
 bounded/provenance-recorded nonexecutable metadata and cannot authorize a CODE
 or DATA operand. Unknown executable relocation forms refuse.
 
+Exact relocation decoder disposition (same grammar for object and final metadata):
+
+|Types|Index meaning|Addend|Encoded target field / selected policy|
+|---|---|---|---|
+|0 FUNCTION_INDEX_LEB,26 FUNCTION_INDEX_I32;1 TABLE_INDEX_SLEB,2 TABLE_INDEX_I32,18 TABLE_INDEX_SLEB64,19 TABLE_INDEX_I64,12 TABLE_INDEX_REL_SLEB,24 TABLE_INDEX_REL_SLEB64|FUNCTION symbol|none|0 CODE call is admitted by full function/type/body join;26 fixed32 only in an explicitly qualified metadata role; table/relative executable forms refuse|
+|6 TYPE_INDEX_LEB|actual signature index, NOT symbol table index|none|CODE type use joins exact signature,not a name or data symbol|
+|7 GLOBAL_INDEX_LEB|upstream permits GLOBAL or FUNCTION/DATA GOT roles|none|selected CODE admits only actual qualified GLOBAL; DATA/FUNCTION GOT substitution refuses|
+|13 GLOBAL_INDEX_I32|GLOBAL symbol|none|only qualified nonexecutable fixed32 metadata; no CODE LEB substitution|
+|10 TAG_INDEX_LEB|TAG symbol|none|decoded then refused by no-tag executable subset|
+|20 TABLE_NUMBER_LEB|TABLE symbol|none|decoded then refused by no-table-use executable subset|
+|3 MEMORY_ADDR_LEB,4 MEMORY_ADDR_SLEB,5 MEMORY_ADDR_I32,11 MEMORY_ADDR_REL_SLEB,21 MEMORY_ADDR_TLS_SLEB,23 MEMORY_ADDR_LOCREL_I32|DATA symbol|SLEB32|3/4 CODE and5 qualified DATA fields per section2; relative/TLS/local-relative executable forms refuse|
+|14 MEMORY_ADDR_LEB64,15 MEMORY_ADDR_SLEB64,16 MEMORY_ADDR_I64,17 MEMORY_ADDR_REL_SLEB64,25 MEMORY_ADDR_TLS_SLEB64,27 MEMORY_ADDR_LOCREL_I64|DATA symbol|SLEB64|15 symbolic i64.const memory32 address only; memory64/I64 pointer/relative/TLS forms refuse|
+|8 FUNCTION_OFFSET_I32,22 FUNCTION_OFFSET_I64|FUNCTION symbol|SLEB32/SLEB64 respectively|only qualified nonexecutable debug field with exact function span/section origin|
+|9 SECTION_OFFSET_I32|SECTION symbol|SLEB32|only qualified nonexecutable debug field tied to exact custom section|
+
+ULEB index/offsets are32 except defined DATA offset/size64; an address addend's
+sign and field width are never guessed from the printed assembly. Relocations
+must be offset ordered, in bounds and NONOVERLAPPING; the latter/operand-boundary
+test is stricter than upstream parseRelocSection and remains mandatory.
+Relevant padded fields:3/4 are5 bytes,15 is10,5 is4. Other admitted fixed32 fields
+are4 and fixed64 fields8; type/index LEB is bounded5. For unsupported decoded
+types (including reference-decoder sizing quirks on table/relative64 forms),
+refuse rather than relying on a guessed field size. Unknown type numbers refuse.
+
 ### 3.2 Same-link-child map: selected concrete normalizer
 
 Require an untruncated, ordinary, single-link wasm-link.map,<=1MiB, emitted by
@@ -215,33 +286,73 @@
 their original category. Source/normal object hashes and exact argv bind the
 producer; the map alone is not accepted as independent source identity.
 
-Selected map grammar: one exact LLVM header with six columns Addr, Off, Size,
-Out, In, Symbol in that order; their literal header positions establish the
-three text-column starts. The numeric prefix is three whitespace-separated
-fields, hex without prefix or '-', with no sign/overflow. Each following row
-has text beginning in EXACTLYone of Out/In/Symbol columns; no arbitrary indentation
-heuristic. Out rows establish output section, In rows establish the exact one
-of two normal object paths plus `:(input_section_name)`, and Symbol rows belong
-only to that active input section. No multiline/wrapped/quoted path, tabs inside
-a name, unknown object path, orphan symbol row or section-scope carry across an
-unrecognized row. Standard nondata section rows must also be fully classified
-against the fixed format reference; they cannot masquerade as data or reset
-scope invisibly. Exact raw row byte offsets/lengths/columns are retained.
-
-Map format C1 must demonstrate those columns/row fields against the pinned
-linker source. This is a PROPOSED strict accepted grammar, not a claim that a
-current unrun linker has emitted it. If actual capability cannot supply this
-unambiguous information, return the plan BEFORE effects; do not parse another
-format speculatively or make the map optional.
+The literal header from MapFile.cpp is
+`    Addr      Off     Size Out     In      Symbol\n`.
+writeHeader uses three `%8llx` fields separated/followed by one space; VMA=-1
+instead uses `       -` for field1. Under these fixed byte/memory caps all values
+fit8 hex digits, so numeric slices are [0,8),[9,17),[18,26), spaces8/17/26, and
+text begins at byte27 plus indentation0/8/16. Numeric Off/Size are hexadecimal,
+NEVER '-'; Addr is unsigned hex or the exact '-' sentinel. Expand/wrap/extra
+columns/overflow refuse. No arbitrary whitespace-token parser that loses hierarchy.
+
+Exact hierarchy and numeric semantics from the pinned MapFile/OutputSections:
+
+|Row|Text column|Addr|Off|Size / parent|
+|---|---:|---|---|---|
+|output section|27|'-'|OutputSection.getOffset()|full section header+body size; label sectionType or sectionType(customName)|
+|DATA output segment|27|segment.startVA|DATA.getOffset()+segment.sectionOffset|raw segment payload size; parent is CURRENT DATA section|
+|DATA input chunk|35|chunk.getVA()|chunk.outputSec.getOffset()+chunk.outSecOff, or0 only if unmaterialized|chunk size; parent is CURRENT output segment, never just DATA|
+|DATA symbol|43|DefinedData.getVA()|input chunk Off+DefinedData.value|DefinedData.getSize(); parent exact input chunk|
+|CODE input function|35|'-'|CODE.getOffset()+function.outSecOff|encoded function size; parent CODE|
+|CODE symbol|43|'-'|same chunk-relative formula|function size; parent exact function chunk|
+|GLOBAL child|35|assigned global INDEX,not a memory address|0|0; text actual global name,parent GLOBAL|
+
+MapFile iterates all output sections, and within DATA all segments, then each
+input chunk, then that chunk's symbols. Section and segment rows share column27:
+distinguish by Addr='-' plus exact known section label versus numeric Addr plus
+CURRENT DATA and exact qualified segment name. Never reset section state merely
+on an unindented string or conflate segment/input chunk. A new known output section
+ends prior DATA segment/chunk state. Nondata core/custom output section rows also
+bind actual final section order/name/offset/size; CODE/GLOBAL children have the
+typed interpretation above. Other section classes have no fabricated child rows.
+Unknown output/child forms, orphan rows and scope carry across unknown records
+refuse. Raw row start/end offsets and all parent identities are retained.
+
+Input text must identify exactlyone of the two approved normal object spellings
+and `:(input_section_name)`; no archives, synthesized unqualified file, whitespace/
+wrapped/quoted path or basename-first fallback. No symbol name is demangled and
+remangled. Options.td says demangling defaults ON and Symbols.cpp calls demangle
+unless disabled: --no-demangle is MANDATORY. The special source `__main_argc_argv`
+to `main` spelling rewrite exists even without demangling; it has NO role in this
+no-main callable subset and refuses if encountered. LOCAL names still require
+the enclosing actual object/chunk identity, not a global printed-name lookup.
+
+Important Off is a SOURCE-DEFINED MAP COORDINATE, not blindly a final byte pointer.
+For a final section beginning F, with actual decoded outer section-header length
+H, MapFile's output-section Off is F. DATA segment.sectionOffset is relative to
+the DATA body (starts after its count), and chunk.outSecOff includes segment
+header+in-segment position but excludes outer H. Thus segment-header file offset
+=mapSegment.Off+H; input/symbol byte file offset=mapInputOrSymbol.Off+H. A segment
+row points at its header, not at its raw bytes. CODE function map offsets likewise
+need outer H before joining decoded body-length/locals/instructions. Require all
+these equalities against independently bounded final byte decoding; never add
+an assumed constant header size or use Off as a DATA linear-memory base.
+
+With selected --emit-relocs, all selected BSS chunks MUST be serialized and
+materialized, so an input outputSec-null/Off0 branch for such a chunk refuses.
+No offsets are invented for nonexistent BSS bytes. This is exact source-defined
+capability, not proof any actual unrun MR map/module already matches it.
 
 The two proposed no-merge/no-GC flags preserve independently named input data
 segments. A map input-section row supplies output linear VM base B and section
 size; require its object/section/size/alignment match SEGMENT_INFO and source
 role. A DATA symbol at object segment offset O then has linked S=B+O. Its symbol
 row MUST confirm that same address/size and exact qualified identity. Duplicate,
-omitted, ambiguous, merged or contradicted rows refuse. If the installed map
-does not expose zero-fill allocation/address/size for a BSS input segment, that
-is capability failure, not an invented address from an accessor or neighbor gap.
+omitted, ambiguous, merged or contradicted rows refuse. With emit-relocs a
+BSS-only DATA section/map MUST exist; absence or an unmaterialized BSS row is an
+actual artifact/flag/format failure, never grounds to invent an accessor/neighbor
+address. Every DATA symbol's offset/size is also joined to the final linking
+symbol's actual serialized segment and the final relocation operand below.
 
 ### 3.3 Exact normalization and linked byte values
 
@@ -273,7 +384,7 @@
 one-past70512 is not a permitted byte-load offset. These are paper examples,
 not generated corpus/SUT evidence or selected actual module addresses.
 
-### 3.4 Complete DATA/zero initialization
+### 3.4 Retained final metadata and complete DATA/zero initialization
 
 All final active DATA segments have explicit memory0 constant i32 offsets,
 bounded payloads and no overlaps. Globals have qualified constant expressions;
@@ -282,16 +393,79 @@
 memory growth is allowed by this chosen subset. Unknown forms refuse.
 
 For file-backed symbol extents, reconstruct EXACT initial bytes from qualified
-source/normal object and compare against the final memory0 DATA placement;
-DATA pointer fields are relocated to their separately qualified target and
-encoded32 bits, not compared to the object placeholder. BSS may be omitted from
-serialized final DATA only when the map proves its allocated interval/size and
-the union of active initializers leaves EVERY byte of that interval initially
-zero (or explicitly covers it with exact zero bytes). Never infer BSS base from
-"memory starts zero" alone. Uncovered file-backed initializers, mismatched bytes,
-nonzero overlap into BSS, alias/coalescing and allocation beyond4 fixed pages
-refuse. Memory zero by Wasm instantiation is an initialized-storage fact, not
-proof of any computational/host stack cost.
+source/normal object and compare against final memory0 DATA placement. DATA pointer
+fields are relocated to their separately qualified target and encoded32 bits,
+not compared to the object placeholder. The chosen corrected plan MANDATES
+--emit-relocs: Writer.cpp sets emitBssSegments for this mode, and DataSection's
+requiredInBinary/isNeeded path then retains the BSS data and map hierarchy even
+if EVERY source storage byte is initially zero. Do not depend on a string/dummy
+sentinel, change last_id/cache/state, import memory or run an initializer to force
+presence. Absence of DATA/map/BSS bytes under this selected mode REFUSES.
+
+Every BSS input has its independently qualified object offset/size/map placement
+and actual SERIALIZED final payload bytes, all zero. Check all payload bytes,
+not just a first byte/hash label or the surrounding writable memory interval.
+Check deterministic inter-chunk alignment padding against the decoded segment
+layout and zero-initialization qualification; no unowned pointer/data is added
+by padding. Entire active DATA intervals are disjoint/nonwrapping within4 pages;
+nonzero BSS overlap, missing/extra bytes, alias/coalescing or uncovered file-backed
+initializers refuse. The old1.0 omitted-BSS fallback is REMOVED from this selected
+plan: memory's default zero never supplies an unobserved base or file offset.
+Instantiating the resulting explicit zeros preserves initial state, not a new
+test fixture or computational/host stack allowance.
+
+--emit-relocs also requires qualifying final custom linking and relocation
+metadata; it is not only a BSS-presence switch. Retain the complete actual final
+module, parse its unique linking-v2 SYMBOL_TABLE with the SAME exact per-kind
+grammar above and all present known subsections, and bind every final DATA entry
+to its actual final DATA index/offset/size. Segment-info,if present,must agree
+with those decoded segments and map names; final absence of segment-info does
+NOT permit a missing DATA segment or guessed name because actual DATA indices/
+payloads plus the independently required full map still bind it. Normal object
+segment-info remains required for its source/input roles. No final absolute/
+common/TLS/weak/ambiguous data substitution or extra unresolved executable symbol.
+Final function/global indices/types/names must agree with actual full body/init
+proof; linking entries alone do not establish a function or storage extent.
+
+Parse EVERY final reloc.* section: one per target section, actual section-index
+and payload bounds, ordered/nonoverlapping rows and EXACT referenced symbol/type
+kind/addend/width. Decode the target section independently. Object symbol indices
+are NOT assumed equal to final indices: build a unique object-qualified/local or
+strong-definition-to-final mapping via the exact normal/input/map placement and
+function/type/global joins. Section symbols bind the named actual CUSTOM section,
+not a core section ID. Debug-only section identities and relocations stay fully
+bounded/qualified separately, never authorize CODE/DATA accesses.
+
+For each object CODE relocation, locate the final field by already joined actual
+function/instruction/operand ordinal; derive its final payload offset from actual
+decoded bytes, not a copied object offset or constant prefix size. Require exactly
+one matching final relocation type/resolved-symbol/addend at that field. Perform
+the converse check so no unexpected final executable relocation is left over.
+Then require actual linked operand equals the exact source/object/map A under
+section3.3, including padded field width and complete opcode/call/type/local
+correspondence. Global/type/call index relocations use their exact semantic
+index mappings, not DATA arithmetic. For DATA pointer fields do the equivalent
+object-field-to-final-segment-byte join and exact encoded value check. No fixed32
+record may masquerade as a CODE LEB, and unknown executable relocation forms
+refuse. A target with zero actual relocation rows may have an absent or one
+explicit zero-count relocation section only; absence is never allowed for a
+required nonzero object/final relocation relation.
+
+Retained final relocation custom sections are verification metadata. The runtime
+loader ignores these custom records; the host/runner MUST NOT reapply them or
+patch the candidate image a second time. Source-supported linker output has
+already written final code/data values. Missing final linking/required relocs,
+duplicate metadata targets, wrong symbol/addend/final address, unexplained debug
+forms or a leftover object/final row refuse before instantiation. Full module
+hash binds customs as well as executable/data bytes; no stripping them for a
+different candidate after qualification.
+
+If final DATA_COUNT is present, decode its one ULEB32 and require exact equality
+to the actual serialized DATA segment count; duplicate/trailing/count mismatch
+refuses. Its presence is not proof of an initializer. Other retained known
+name/producers/target_features/DWARF customs keep their qualified bounded schema,
+full raw identity and section-relative records; unknown forms/effects are not
+silently skipped merely because emit-relocs added more metadata.
 
 Source/object/map/module identities plus per-operand and per-object provenance
 are persisted in wasm-address-join.json. The whole linked code/type/local/call/
@@ -304,20 +478,37 @@
 ## 4. Exact same-child artifacts and capability references
 
 Preserve normal/diagnostic distinct stems and SAME functional/optimization flags
-for each unit/target. Proposed additions on both normal and diagnostic compiles:
--fdata-sections -ffunction-sections. Normal still uses -save-temps=obj -MD/-MF;
+WITHIN each target. WASM-ONLY proposed compile additions on both normal and
+diagnostic: -fdata-sections -ffunction-sections. These options are NOT added to
+Apple Darwin commands by this plan. Native uses its separately qualified existing
+normal MachO literal symbol/extent/initializer proof and adopted PIC/module flags,
+with matching native normal/diagnostic options. LLVM Wasm references do not prove
+Apple compiler capability; any native option lacking its own qualified basis
+remains a named future capability gate, with no probe or weaker object proof.
+The pinned bundle proves the Wasm LINKER options and formats below; it does not
+include Clang's driver option table. Thus explicit -fdata-sections/-ffunction-sections
+compile-option adoption remains conditional on an exact pinned Clang option
+reference or accepted same-target invocation DATA before source/effect release.
+Retained G1 assembly corroborates named sections, not a new option probe. The
+same separate capability condition applies to normal -save-temps metadata and
+native PIC/module/diagnostic options; do not infer Apple support from wasm-ld.
+Normal still uses -save-temps=obj -MD/-MF;
 diagnostic still uses -S -MD/-MF. Retain actual normal .o/.s/.su/.d plus normal
 .bc/.ii when emitted; no separate assembler/object dump child. Proposed Wasm
 link additions, literal ordered tuple:
 
     --no-gc-sections
     --no-merge-data-segments
+    --no-demangle
+    --emit-relocs
     --Map=<absolute-attempt-root>/wasm-link.map
 
-No final --emit-relocs assumption is needed: object relocations plus same-link
-placement map are joined to actual final decoded instruction values. Final
-metadata/strip policy must retain the existing names/types/locals needed by the
-complete body proof. Unknown name/index/initializer forms refuse.
+This ordered tuple applies ONLY to the SAME EXISTING WASM wasm-ld link child,
+not the native linker. No --compress-relocations or --strip-* option is admitted.
+Retain and qualify final linking/reloc.* sections, serialized BSS zero bytes and
+all existing names/types/locals needed by the complete body proof as section3.4
+requires. Source-defined capability of these flags is documentary; actual MR
+output must still satisfy every join/budget. Unknown forms refuse.
 
 Native link/compile replacement, requiring later adoption, uses MR_NATIVE_MODULE
 instead of MR_NATIVE on wrapper and corresponding diagnostic build, target-width
@@ -351,26 +542,45 @@
 - Accepted G1 attempt-4/diagnostics/wasm/wrapper.s:47/58/69 symbolic bases;
   97/106 symbolic memory offsets; later .type/.section/.skip/.size data objects.
   Its .ident reports clang24 commit84ba7b37f02df5a5567e31a1bcfa0f607e578f12.
-  This proves that producer syntax exists, not the selected link-map capability
-  or current MR object metadata. No G1 module was parsed/loaded or proof rebased.
+  This proves that producer syntax exists, not current MR emitted metadata.
+  No G1 module was parsed/loaded or proof rebased.
 - Accepted G1 inspected-plan.json supplies known typed tool/alias reference
   context: fixed clang24 hash9a96...c423, wasm-ld/lld hashb851...ad5c, native
-  launcher179301...c1818 and canonical Python4e28...c46a. A clang .ident does not
-  prove the linker has the same source revision. Fresh exact actual tool aliases,
-  hashes/times/dependencies remain a later preflight obligation.
+  launcher179301...c1818 and canonical Python4e28...c46a. Accepted G1
+  attempt-4/logs/23.stdout explicitly names clang commit84ba7b37f02df5a5567e31a1bcfa0f607e578f12;
+  logs/24.stdout independently names LLD24.0.0 at that SAME commit. This is NOT
+  inferred from clang's .ident. Fresh exact actual tool aliases/hash/time/
+  dependencies remain later preflight; neither historical version command reran.
 - Installed MacOSX15.5 dlfcn.h explicitly declares NOW0x2/LOCAL0x4/FIRST0x100;
   loader.h/nlist.h define regular/reexport/resolver/weak/section/init records.
   These were read/hash inspected only; no function/library was called.
 
-C1 conflict: the installed SDK has no discovered LLVM Wasm.h/WasmRelocs.def/
-linker-format source reference in its inspected include/share locations; no
-accepted MR map or object-format qualification was supplied. Need MAIN to freeze
-primary LLVM tool-conventions linking-v2/relocation and EXACT selected lld map/
-no-merge/no-GC implementation references/identities before implementation-format
-clearance or actual effects. No current binary strings/probe/parser/network
-operation is substituted. If those exact options cannot supply the required
-one-to-one BSS/data map and full object symbol/relocation interpretation within
-the same child, THIS plan is returned; no weakened join or unpriced child.
+C1 DOCUMENTARY BASIS RESOLVED BY D337. The complete inert reference catalog is
+notes/references/T203-llvm-84ba7b37/README.md and MAIN analysis is
+notes/reviews/MAIN-T203-primary-format-review-1.md. Both exact accepted version
+logs identify revision84ba7b37f02df5a5567e31a1bcfa0f607e578f12 for their respective
+tools. All ten local .txt copies retain upstream notices and are READ-ONLY DATA;
+none was imported, parsed as a program, built or executed. Exact source locations:
+
+|Immutable upstream path (all at revision84ba7b37)|Git blob SHA|Plan fact|
+|---|---|---|
+|[llvm/include/llvm/BinaryFormat/Wasm.h](https://github.com/llvm/llvm-project/blob/84ba7b37f02df5a5567e31a1bcfa0f607e578f12/llvm/include/llvm/BinaryFormat/Wasm.h)|c351ea42e5636898c2856a0b47dcb71914a9e01c|metadata2,subsection/symbol/segment kinds and flags|
+|[llvm/include/llvm/BinaryFormat/WasmRelocs.def](https://github.com/llvm/llvm-project/blob/84ba7b37f02df5a5567e31a1bcfa0f607e578f12/llvm/include/llvm/BinaryFormat/WasmRelocs.def)|9213350e4329b9c820781e65b39716ff957d73b3|exact relocation numbers0..27|
+|[llvm/lib/Object/WasmObjectFile.cpp](https://github.com/llvm/llvm-project/blob/84ba7b37f02df5a5567e31a1bcfa0f607e578f12/llvm/lib/Object/WasmObjectFile.cpp)|007aeff0d1f6b8b55a0e47b933fd08be56b19d0b|parseLinkingSection/Symtab/Comdat and parseRelocSection exact per-kind/name/index/addend grammar|
+|[llvm/lib/MC/WasmObjectWriter.cpp](https://github.com/llvm/llvm-project/blob/84ba7b37f02df5a5567e31a1bcfa0f607e578f12/llvm/lib/MC/WasmObjectWriter.cpp)|43f71cc43bf8ff5611771a01d34e43bd7a8f2933|writeLinkingMetaDataSection and writeRelocSection emitted record fields/offset sorting|
+|[lld/wasm/Options.td](https://github.com/llvm/llvm-project/blob/84ba7b37f02df5a5567e31a1bcfa0f607e578f12/lld/wasm/Options.td)|a54979527b186975ffe42453272508218c839d11|no-gc/no-merge/no-demangle/emit-relocs/Map spelling and defaults; compress-relocations not selected|
+|[lld/wasm/MapFile.cpp](https://github.com/llvm/llvm-project/blob/84ba7b37f02df5a5567e31a1bcfa0f607e578f12/lld/wasm/MapFile.cpp)|53db9df8e02b4dd7f3f1bccfc929758315b9b242|exact header,writeHeader,0/8/16 indentation,section/segment/input/symbol hierarchy,DefinedData VA/size|
+|[lld/wasm/Symbols.cpp](https://github.com/llvm/llvm-project/blob/84ba7b37f02df5a5567e31a1bcfa0f607e578f12/lld/wasm/Symbols.cpp)|26fff7c802eba1fb73dfed22c62020ab6cbda557|maybeDemangleSymbol default,raw no-demangle,main special rewrite|
+|[lld/wasm/Writer.cpp](https://github.com/llvm/llvm-project/blob/84ba7b37f02df5a5567e31a1bcfa0f607e578f12/lld/wasm/Writer.cpp)|7ed266a06ca8cf0b31b6e95f547a71d74c2bb0ce|emitBssSegments under emitRelocs,populateSymtab,linking/reloc section retention,finalizeSections then writeMapFile|
+|[lld/wasm/OutputSections.cpp](https://github.com/llvm/llvm-project/blob/84ba7b37f02df5a5567e31a1bcfa0f607e578f12/lld/wasm/OutputSections.cpp)|d9017fefffdd1ac33759fcde3b246c110b1f9f5d|DataSection finalizeContents/writeTo/isNeeded,body/segment-header/raw-byte/map offsets,relocation traversal|
+|[lld/wasm/OutputSections.h](https://github.com/llvm/llvm-project/blob/84ba7b37f02df5a5567e31a1bcfa0f607e578f12/lld/wasm/OutputSections.h)|4b0329dd16cf21b1aacfe33772614d1c9b25ceb0|retained segment list and exact header/body offset/size interfaces|
+
+Future exact installed binary/alias preflight, actual emitted map/module/custom
+section/body/initializer qualification and budgets are NOT resolved by documentary
+source availability. If those actual outputs fail this exact source-defined
+method, preserve/refuse; do not weaken it, retry/probe, change state/import memory
+or add a child. Prior1.0 C1 question/handoff remain historical and unedited;
+D337/current correction records the documentary disposition separately.
 
 ## 5. Native pre-load image qualification (DATA only)
 
@@ -614,7 +824,7 @@
 |W01|admit|i32.const actual request symbol+1, correct object/reloc/map/final70001|
 |W02|admit|i64.const same memory32 symbol+1, exact64-bit70001|
 |W03|admit|symbolic byte load offset+1, exact relocation/address/alignment|
-|W04|admit|unrelocated numeric constant remains exact, no symbol wildcard|
+|W04|refuse|map has demangled C++ spelling rather than required raw identity (no re-mangling fallback)|
 |W05|refuse|wrong symbol identity even if forged placement has same numeric address|
 |W06|refuse|source addend1 but actual relocation addend2|
 |W07|refuse|correct metadata but final linked70002 rather than70001|
@@ -623,10 +833,10 @@
 |W10|refuse|DATA relocation points into wrong operand/opcode/width field (one offset mutation)|
 |W11|refuse|addend produces target-width wrap instead of bounded mathematical A|
 |W12|refuse|one-past object used for byte load|
-|W13|refuse|final file-backed initializer byte differs|
-|W14|refuse|nonzero active initializer overlaps qualified zero BSS|
-|W15|refuse|map row names other normal object/input section|
-|W16|refuse|forbidden TLS DATA flag on referenced symbol|
+|W13|refuse|one serialized BSS initializer byte is nonzero (same exact-byte initializer gate also governs file-backed storage)|
+|W14|refuse|BSS-only final DATA/map branch is absent despite required emit-relocs; no invented offsets/default-zero fallback|
+|W15|refuse|DATA output-segment row is placed/treated as an input-chunk row (one hierarchy/indent mutation)|
+|W16|refuse|actual FINAL CODE relocation addend differs from matched source/object/map,even if earlier metadata is correct|
 |N01|admit|all five same slide; exact512/2048 objects; source char alignment1 with deliberately non8-aligned fixture address|
 |N02|refuse|one actual callable address gives different slide|
 |N03|refuse|returned pointer is writable/in-range but names the wrong object|
@@ -636,8 +846,16 @@
 |N07|refuse|U+slide+size overflows unsigned64|
 |N08|refuse|response normal/source declared extent2047 rather than2048|
 
-5 retained run admits +4 retained write admits +4 W admits +1 N admit =14;
-82 refusals. All are proposed expectations, none observed. Wrong exact-field
+Revision1.1 reallocates W04/W13/W14/W15/W16 ONLY inside the same sixteen W cases;
+all48 run/24 write/8 native cases and their prior removal list are unchanged.
+W01..03 accepted fixtures now include complete raw-name DATA hierarchy, serialized
+zero BSS, exact final linking/reloc metadata AND an unchanged unrelocated numeric
+instruction, so positive whole-body/numeric comparison still has a source case.
+No scenario is hidden as a second outcome under one case label. Explicit unknown
+TLS/duplicate/offset/field/initializer refusal predicates remain mandatory even
+when this finite union allocates a different negative mutation to a shared gate.
+5 retained run admits +4 retained write admits +3 W admits +1 N admit =13;
+83 refusals. All are proposed expectations, none observed. Wrong exact-field
 joins discriminate before any target/char effect; ordinary whole code/type/local/
 call and backing/guard correctness are still checked by actual512 evidence.
 
@@ -665,6 +883,18 @@
   ordinary logs/reports/other records. Same8MiB capture files can bring this to
   59MiB;remaining owned ordinary records must fit5MiB AND the overall64MiB gate.
   No source/cache copy or hidden map expansion. Actual overrun refuses.
+  --emit-relocs adds at most262144 serialized storage/padding bytes under the
+  existing four-page memory bound, not another memory allocation or source
+  sentinel. Final linking/reloc.* custom payloads together get a <=1MiB subcap
+  INSIDE the existing8MiB Wasm image reservation (including CODE/DATA/debug
+  metadata). Outer headers/names and those zero bytes also count in that same
+  complete8MiB file and the64MiB owned artifact aggregate. No extra artifact,
+  metadata, fixture or captured-output allowance is created by the new flag.
+  All final raw metadata is retained in the hash-bound module; derived bounded
+  join report uses exact section/symbol/operand indices and raw byte ranges to
+  avoid duplicating unbounded name/record expansions. The256KiB join-report cap
+  and2MiB proof-report category still apply; inability to persist full required
+  evidence within them refuses,never drops records or promotes a truncated PASS.
 - proof-report2MiB category: native normal/body/frame<=768KiB,Wasm<=768KiB,
   address-join<=256KiB,loaded-host records<=256KiB. Map/object/assembly raw files
   remain retained artifact evidence, not duplicated into expanded stdout.
@@ -675,6 +905,14 @@
   initializer segments. Each function body/local/edge also stays within existing
   bound1024 functions/4096 local groups/depth128. All joins use exact indexed
   records, bounded scans; no full-size allocation from a forged extent.
+  Retained final metadata has <=4096 symbol entries,<=256 DATA roles,<=4096 CODE
+  relocations,<=128 DATA relocations and<=4096 total approved debug-only relocation
+  rows. At most32 reloc.* target sections,unique per actual target,within the1MiB
+  custom-payload subcap; unknown forms refuse. Counts are independently bounded
+  BEFORE allocation. Normal input segments can number<=256,but with no merging
+  and serialized BSS the selected final active DATA count MUST ALSO fit the
+  unchanged128-initializer cap. If that actual input cannot fit,no cap rises:
+  return/refuse before load. Same-child source support is not measured fit.
 - host code bindings exactly5;common-slide calculations5;initial address/cap
   calls4;512 rows each2 address calls+1run+2 char operations;final binding/address/
   cap rechecks as above. Exactly512 public SUT selections and1024 char copies,
@@ -703,8 +941,11 @@
 
 ## 10. Required MAIN disposition and stop
 
-Review/return C1 exact installed LLVM object/map/flag capability and the finite
-96-case reallocation; review the fixed loader0x106/regular-export/common-slide/
+Review this exact primary-source correction and finite96-case reallocation;
+C1 documentary reference basis is resolved by D337,while exact current installed
+roles, remaining target compile-option capability and all actual emitted-format/
+zero-data/final-relocation/budget gates stay required. Review the fixed
+loader0x106/regular-export/common-slide/
 exact-object protected-load model and host cost scope; freeze complete host/
 ctypes/libffi/loader/native format roles and all exact manifests/paths/options.
 Only then adopt an exact wrapper/host/controller/schema/flag source replacement
```
