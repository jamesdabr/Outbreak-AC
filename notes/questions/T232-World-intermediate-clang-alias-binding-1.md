# T232 — Intermediate clang alias missing from sealed metadata graph

- Author / worker: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket and revision: T2321.2, D408 SOURCE CONSTRUCTION ONLY.
- Phase and contract revision: G2_FOUNDATION1.8, D391/D398/D408, adopted T229 sections1–8.
- Exact clause or interface affected: D391 requires a complete literal typed-alias/input graph; D408 permits ONE NEW inspected input collector3/input-inventory2 and forbids automatic retry or silent role/graph refresh.
- Status: OPEN (lead resolution is recorded separately).

## Question

Collector3's one authorized metadata pass succeeded against its declared finite graph, but subsequent fixed-text role review found an omission in the collector: the accepted Wasm compiler role follows TWO aliases. The sealed inventory records `.../bin/clang++` and resolved `.../bin/clang-24`, but not intermediate `/private/tmp/outbreak-web-sdk/upstream/bin/clang`. May a separately named source/metadata amendment bind this exact additional intermediate alias, preserving collector3/input2 unchanged, before final caller construction resumes?

This is a missing binding in my new inventory, not an observed historical mutation or a failure of the accepted tool hash. I have not added a guessed identity, silently refreshed the inventory, created another collector, rerun collector3 or created the executable caller.

## Evidence and impact

The immutable P4 execution-plan.json (SHA256453f13c7d559aafaf8d76ce77491b880befc0502c8c4522fcbe6b89e386096fb), lines657–675, declares the compiler role `/private/tmp/outbreak-web-sdk/upstream/bin/clang++`, its immediate target `clang`, resolved `/private/tmp/outbreak-web-sdk/upstream/bin/clang-24`, and the accepted resolved payload165339888/SHA2569a96f4220eefe21e72a4a9a20a88f4d6c26cad1b047cb02b5b22a96bef49c423.

Collector3 lines293–299 compares the immediate role/full accepted legacy record, resolved/full accepted record and realpath result, then adds those TWO paths. It does not separately seal intermediate aliases. The successful realpath comparison therefore establishes the resulting resolution during collection, without supplying an independently retained full typed descriptor for every hop.

After publication, exact fixed-text `rg -o` for the JSON key `"/private/tmp/outbreak-web-sdk/upstream/bin/clang":` in input-inventory2 produced no match. A standard read-only `ls -ld` and `readlink` on THAT EXACT named immediate target (not a host scan) returned:

```
lrwxr-xr-x@ 1 jd1 wheel 8 Nov 6 12:52 /private/tmp/outbreak-web-sdk/upstream/bin/clang -> clang-24
clang-24
```

These text observations do not claim a complete nanosecond descriptor/hash pin or authorize adoption of a new row. They identify the specific missing alias, which is already implied by the accepted immediate target. An unchanged final realpath alone is insufficient to claim the requested complete typed alias graph.

Collector3 SHA25635553a8ce94c65ffcc31751ce574659935f5b08ef5a9692659e922bbd67e7da6 was fully displayed/read in three consecutive source ranges before its only invocation. Exact fixed7ENV/canonical Python3.11.9-I-S-B/repo cwd/loginfalse, original300 metadata cutoff, strict flags and bounded streaming/ownership/output guards. Original exec chunk8a5346/session49864, terminal chunk299923/exit0:

```
status NAMED_METADATA_ONLY
nodes18502 directories1240 anchors1305
bytes5426013
sha2568cd88fff2c3158cf246218d67ab112cdb6d1b5933b5a514c92c9b95fc5ef2eda
```

Family counts: sources13,controls18,authorities35,preserved-construction-DATA6,dependencies11,invoked-callers9,historical-DATA25,stdlib81,native-headers273,wasm-headers173,SDK-roots3,tool-paths7,ABI-DATA11,other-named-material4. Families overlap; their sum is not the unique node count. All15 historical roots matched their original expected graphs, including A2's2170/same75d6 and unchanged A1's2169/652ace; full SDK2010, G0 original2509nonself files/326dirs plus freeze, original headers/tools/dependencies matched. Qualified stdlib50module/81file inventory2 was checked unchanged; no new profile/stdlib collection occurred.

The result validates the enumerated rows, not completeness of the missing intermediate alias role, whole-interval protection, current source functionality or any future operation. Existing inputcollector1/comparison1/stdlib collectors1/2/stdlib inventory2 and all source/history remain untouched. No project parser/import/compile/helper/control/corpus/preparation/test/compiler/probe/FFI/runtime/network/Git or output scaffold ran. Proposed P5/A3/Q roots were all absent at the collection check.

## Options for owner and lead

1. Release a NEW narrowly named metadata collector/inventory successor that adds the exact intermediate alias and validates unchanged old rows, with an explicit role/provenance delta. Keep collector3/input2 and all older evidence immutable; inspect before one newly authorized pass.
2. Explicitly authorize a separate bounded metadata-only companion binding for this exact alias, leaving inventory2 immutable, and specify how the final caller and external preflight must bind the union. No implicit self-hash cycle or unreviewed runtime discovery.

Recommendation: option1 supplies the simplest single complete future graph. Neither option is permission to execute project code, change an old tool expectation, rerun preparation, weaken alias protection or silently repair a sealed record.

## Work paused

Final executable caller creation and complete source packet sealing are paused on the missing alias binding. `notes/proposals/T232-R-preparation5-caller-1.py` remains absent. The successful metadata DATA and this exact gap are preserved for MAIN review. No further collector run is authorized by this question. Governing contracts/tickets/statuses remain lead-owned and unchanged.
