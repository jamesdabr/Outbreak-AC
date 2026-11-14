# Ticket handoff — source/native/Wasm ready; sanitizer blocked

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket / revision: T084 / 5.7, RELEASED; no self acceptance or full-ticket PASS.
- Contracts: PORTABLE_FORMAT_FOUNDATION 0.1 / D079, GOV/BROWSER/P0 0.5; numeric foundation unchanged. Ticket/contract re-read before submission. Format contract SHA256 d50bac8d4c768f6b1e843ca6688473baf948ce1e98393c3bfaa9c1cf519a5a90.
- Base: existing shared dirty tree, prior base commit 13f0d8eea4822dee5c976661218d022be74342e3. No reset/revert/branch/commit/push/dispatch or unrelated edits.
- Changed: NEW source/outbreak/map_import.h/.cpp, tests/outbreak/map-import/T084/**, own question T084-world-sanitizer-startup.md and this handoff. No accepted T080/old assets/helpers changed.

## Acceptance evidence

PASS — Exact public B API/error numeric values/types/constants; no unrelated public production symbols. C++11 bounded byte decoder for already-decompressed ACMPv10 dry-flat owned subset. No allocation/I/O/platform/exception/global mutable state or large scratch array. Explicit endian/signed arithmetic; checked header/count/offset bounds; factors6..8 and <=65536 cells. Unsupported water/config/metadata/entity/cell modifiers rejected.

PASS — Full first pass validates immutable input including late errors/trailing data before any cell or metadata write. Second pass emits only after complete validation. No entity deployment, gzip/config behavior, actors, world queries or nav integration. Caller allocation/nonoverlap/immutable-input preconditions remain as approved.

PASS — Actual identical production source compiled and executed native and direct Wasm against the independent Python struct/integer oracle: 9639 cases /76 batches,1376 positive/8263 negative. Every error value1..15 exercised. Both full binary outputs equal the complete expected output (not only matching summaries). Wasm has zero imports and only memory/input_ptr/output_ptr/output_bytes/run test exports; no suppressed undefined imports/runtime library fallback.

PASS — Owned pinned T064 map2 and T080 candidate cells independently reconstructed from source rectangle definitions/final source report, then compared field-by-field; synthetic factor6/7/8 grids, signed heights, metadata16-record/length boundaries, entity kind/field/range/count limits, all256 cell kinds/entity kinds, all candidate raw truncations, all short headers, raw bounds, capacity, revisions, late malformed cells/runs/trailing bytes and2048 deterministic mutations. All output/control/canary bytes checked against sentinels on each failure; all positive fields/cells compared. Input and unused trailing output storage also verified unchanged. Case labels and expected errors in attempt-2/cases.json; full corpus/expected/native/Wasm binary records retained.

PASS — Production stack-usage reports: native decode96bytes/stream0; sanitized compile decode160/stream32 (+small helpers); Wasm reports0linear-stack bytes. Builds enforce -Wframe-larger-than=4096; no large production arrays or recursion. These are bounded foundation claims, not gameplay/performance acceptance.

PASS — Attempt2 protected before/after38251 files unchanged (SDK, existing source/src/enet, assets, runtime/artifacts/build cache and numeric source). Same before snapshot from failed attempt1 also independently rechecked unchanged. No install/acquisition/SDK/global-cache modification, services, browser, full game/native/server builds or network. Unconsumed test controllers/new Engine envelope sources are not compile inputs. Task-owned sysroot copies/cache/logs only.

NOT RUN / BLOCKED — Required actual ASan+UBSan coverage. Installed Appleclang17 successfully built the combined-instrumented executable, but attempt1 batch0 timed out60seconds. Exact same executable/environment with EMPTY stdin also timed out10seconds before corpus processing, no output. No runtime/flag substitute or waiver inferred. [Open question](../questions/T084-world-sanitizer-startup.md) requests an identical local unsandboxed retry or MAIN-approved installed diagnostic. Native/Wasm evidence is complete; full_ticket_pass=false explicitly recorded.

NOT RUN — Native engine importer/rendering, shared capsules/navigation, game integration, complete P0/P1, gameplay/balance/human gates. This limited known subset is not general native map support.

## Reproduction and tools

Read owned verify.py, wrapper.cpp and wasm_runner.mjs before execution. Attempt2 plan.json records exact commands/environment/tool/source hashes before invocation. Appleclang17, SDKclang24/LLD, pinned installed Node24.19 and Python3.11; Darwin25.5 arm64. Production flags include C++11/O2/Wall/Wextra/Werror/fno-exceptions/fno-rtti/fno-builtin/fstack-usage/frame warning. Actual Wasm target wasm32-unknown-emscripten and copied frozen sysroot; direct linker explicit named exports/no-entry. Sanitizer flags address,undefined/fno-sanitize-recover=all/g; no new flags invented after timeout.

The once-only harness automatically allocates a fresh attempt directory.
`python3 -B tests/outbreak/map-import/T084/verify.py --native-wasm-only` generated attempt2, explicitly classifying sanitizer NOT RUN. Default mode includes sanitizer execution but MUST NOT be retried until the open runtime question is resolved. Do not overwrite existing attempts. Existing attempt2 binaries/corpus are reviewable without recompilation. Required future sanitizer execution can reuse the frozen binary/corpus under an explicit resolution and add fresh evidence without modifying the frozen source/harness.

Attempt1 failures/builds/partial outputs/empty-input result are retained, including FAILURE.md. Attempt2 result.json is the definitive native/Wasm evidence; its `passed:true` refers only to the selected independent targets; `full_ticket_pass:false` and sanitizer status prevent promotion to full acceptance.

## Frozen identity

Terminal freeze tests/outbreak/map-import/T084/terminal-freeze-1.json pins242 source/harness/corpus/output/object/log/result/question records, excluding itself/this handoff and ephemeral task caches/tmp/node/clang caches. SHA256 b13b7fbdcbc86a37bc2ad917536f1f453536e473a5c007a8eee8cd61f3f08398.

- map_import.h: a8ee019deec650add0cc885dba337ef70517106dc9719fceb0535ce6e664c90f
- map_import.cpp: 1da8d4c5c10f51463f5f4c9bc88ca5b3ea13effba22ab614bef56c0212b82604
- attempt2 result: e0ab0ec10dc20c9de30f79b11f9cf6f5b0c2549528d9861d4ae8f828c9d8bcf3
- corpus: ab18ae02ee2f578dc72608fcb93df46facf5b24addfe9701884fcb0936a7ce50
- full expected/native/Wasm output: 7580f9b1ed9565f8a9145cf1062a04fc148e01f4b044fc8c2eecf89c45787062
- Wasm: eddaf79907f075b9a4c19e9abd7a80aba08676fb37591155152313eb51c27ace
- frozen combined-sanitizer executable: 00b6cdd445a52229b119ce114f9d9844147f489f464ee6e3282312b2bde9d624

## Implementation status / integration and questions

Implemented actual unused source decoder and native/Wasm foundation tests.
Synthetic/malformed fixtures are separately labeled; no gameplay simulation was
substituted. Incomplete: sanitizer runtime coverage, blocked by the open question.
No integration/dependency/interface/asset change beyond exact new B API.
Frozen for MAIN review; further corrections require question/release. MAIN alone
accepts source/ticket scope; no phase/full-ticket acceptance claimed.
