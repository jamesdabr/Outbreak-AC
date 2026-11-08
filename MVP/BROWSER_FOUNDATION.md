# Browser foundation execution contract

Revision: 0.5. Status: APPROVED FOR THE RELEASED EXPERIMENTAL PREREQUISITES ONLY. Authority: coordinating lead under the owner's explicit audit, subagent ticket drafting and worker-dispatch instruction. Decisions: D003, D004 and D005.

## Scope of approval

Only individually RELEASED T016-T020 and T022-T025 tickets may execute under this contract. Accepted first-wave ticket revisions remain historical evidence; new work uses individually pinned releases. The owner-approved browser-first/eight-player direction governs them. Unresolved gameplay values, production transport/engine selection, final support matrix and final performance thresholds remain deferred and do not authorize implementation. Existing T001-T015 and T021 remain unreleased unless explicitly updated. Completion of a prerequisite ticket does not accept T014, T015 or P0.

This contract is the approved governing subset for isolated build/runtime/tooling experiments. Other draft MVP documents provide boundaries but are not silently approved in full. A worker must ask about conflicting requirements, not choose an interpretation. No worker may edit contracts or tickets.

## Experimental decisions

- Candidate foundation: current AssaultCube C++ checkout compiled to WebAssembly with Emscripten. This is not a permanent engine selection.
- Experimental SDK pin: Emscripten 7.0.0, release metadata hash `6afbd83493d647051772d491124187d4e9a0cda9`, verified against official emsdk release metadata. Do not substitute `latest` or a different version without a note/lead revision.
- First evidence browser: desktop Chromium on macOS arm64 using keyboard/mouse. Record actual browser version and executable path. This is an experiment target, not a promise that other browsers/OS/mobile are supported.
- Attempt legacy GL emulation for the initial rendering proof. No broad renderer replacement, game-rule changes or unlogged omission of essential rendering is authorized.
- Prefer a single-thread browser experiment. Do not turn semaphore waits/thread creation into false successful operations. Shared service changes require the accepted T020 inventory and a separate explicit implementation allowlist.
- No production network transport is selected. T015/T021 implementation remains unreleased until the lead freezes its experimental schema/endpoint and owner/lead resolves any broader scope change.
- LLM tester observation/action details remain deferred. No screenshot requirement or model-provider integration is added.

## First-wave source ownership

| Ticket | Worker | Exclusive source/output ownership |
| --- | --- | --- |
| T016 | Engine & Multiplayer | web/build/**; source/src/platform.h and source/src/tools.h only for narrowly guarded browser compile support if the released ticket includes them |
| T017 | player combat | source/src/main.cpp and new web/runtime/** only as explicitly listed in the ticket |
| T018 | World/Match-Systems | web/assets/**; all game/config/asset source files are read-only |
| T019 | QA/Performance | web/qa/**, including its own labeled fixtures/results; game source and build output are read-only |
| T020 | AI-Director | Its own notes/handoffs/T020-* and notes/questions/T020-*; all source/contracts are read-only |

New root shared files, source modules, build settings owned elsewhere and public headers outside this table require a note before editing. No two workers may edit the same file. Do not commit, push, merge, reset, clean or revert pre-existing edits. Existing combat prototype files remain unchanged except where an explicitly listed main.cpp change is necessary; the current main.cpp itself has no uncommitted prototype delta at release.

## Tool and execution boundaries

Approved work is local to this repository and ticket-specific temporary paths. Build drivers, native syntax checks, manifest generation and loopback QA tests are authorized after inspection. SDK/tool caches may be local to `/private/tmp/outbreak-web-sdk` or the Engine-owned `web/build/` subtree. No system/global package installation, shell-profile changes, native AssaultCube user-profile writes, unrelated repository execution, public network server binding, production account access or public deployment.

The Engine worker may prepare a pinned SDK setup procedure and inspect official installer code before execution. If an external installer is unfamiliar or the local cross-system skill requires additional explicit approval, create a narrowly scoped question identifying the exact command, download source, writes and cleanup; continue independent build-driver work. Missing tools must be reported honestly. Bundled Playwright may be reused without adding a system/global package. Installing browser binaries or other new dependencies needs an explicit scoped lead decision.

## Integration file conventions

These are file boundaries, not permission to invent a wire protocol:

- Engine build defaults: final integrated artifacts under `web/build/out/`; T016 compile-only probes under `web/build/generated/`; local caches under `web/build/.cache/` if used. A preflight must report absent SDK/libraries distinctly from a compile failure.
- World manifest defaults: `web/assets/generated/bootstrap-manifest.json` plus its human-readable provenance/dependency report. Generator must produce deterministic output and paths relative to the repository; reject escapes. Include at least a schema version, roots, entries with source path/virtual path/size/SHA-256/provenance classification, and unresolved references. The `complete` and `shared_build_ready` flags cannot be true while dependencies/permissions remain unresolved.
- QA server accepts an explicit document root and binds loopback only. Actual game testing defaults to `web/build/out/`; QA fixtures live only beneath `web/qa/tests/fixtures/` and are reported as fixtures, never as the game. No SDK or native configuration directory is served.
- Runtime branch uses `__EMSCRIPTEN__` guards, a persistent one-frame callback and browser scheduling. The T017 browser-only local gameplay delta is capped at 250 ms and reset on resume. In the explicitly offline map experiment, the retained embedded local simulation uses that bounded clock too; this is not wall-clock standalone authority. Native and separate dedicated-server clocks remain unchanged. Future network-client timing requires a separate contract. Clear held movement/fire/jump on focus, visibility or pointer-capture loss; reacquire via user gesture. Preserve the native loop semantics; no browser path may claim that an embedded offline server demonstrates standalone multiplayer.

Implementation details within a ticket may vary while preserving these boundaries. If a proposal cannot meet a frozen convention, stop affected work and raise a question.

## Evidence

Each handoff records source baseline and pre-existing edits, exact tools/commands, changed files, per-criterion PASS/FAIL/NOT RUN and evidence paths. Tooling fixtures, missing SDK, syntax-only results, Wasm object compilation, linked game artifacts and actual browser gameplay are distinct outcomes. No worker may promote one to another or mark authoritative ticket status. Only the coordinating lead releases, reviews and accepts work.

## D004 next-wave boundaries

- T022: Engine may acquire/read official emsdk manager source into /private/tmp/outbreak-web-sdk-inspection and record hashes, but may not execute it, activate an SDK or fetch/build ports under this ticket. A precise inspected proposal precedes any later setup authorization.
- T023: World may extend web/assets inventory tools/schema/fixtures and select ac_complex only for metadata inspection. No CubeScript execution, media copying, native map mutation or packaging.
- T024: QA may add an explicitly labeled WebGL capability fixture and probe under web/qa. Actual engine/game gates stay NOT RUN. Reuse installed Chrome/Playwright with normal flags and owned loopback processes.
- T025: AI owns only source/src/server.cpp for the __EMSCRIPTEN__ non-STANDALONE deferred local/no-auth branch and new web/runtime/tests/offline_auth* helper fixtures. Process at most one queued request per poll, without threads or semaphore waits. Require current in-range ST_LOCAL identity, matching clientsequence, SV_SERVINFO_RESPONSE, wantauth=0 and needsauth=false; reject other current requests with normal auth failure, discard stale requests safely. Reuse the existing completion path and its checks. Preserve native/standalone behavior; do not enable network browser auth or claim complete service separation.
- T017 revision 0.4 owns main.cpp for wiring the bounded offline delta. It must not change server.cpp; T025 must not change main.cpp. Wasm verification stays pending until an approved ready SDK exists.

## D005 integrated foundation wave

Individually released T026-T030 are authorized by D005. Read notes/decisions/D005-integrated-browser-foundation.md for the exact reviewed SDK execution, original asset/profile paths, diagnostics schema, truthful single-thread operations and exclusive source ownership. All earlier gameplay drafts and later gates remain unchanged. No source or policy restriction may be broadened by a worker.

D072 adds only the separately versioned APPROVED SHARED_NUMERIC_FOUNDATION.md0.1 isolated portable arithmetic prerequisite and individually released T078. Existing0.5 browser behavior/contracts and complete P0 gates remain unchanged; no production game implementation or platform acceptance is implied.

D075 adds only separately versioned BLACKWOOD_DATA_FOUNDATION.md0.1 candidate DATA prerequisite/T080. Existing0.5 runtime contracts/fullP0 gates stay unchanged; no final map/gameplay/phase acceptance.

D077 adds only EXPERIMENTAL_IMPAIRMENT.md0.1 fixed controlled-loss/delay test-controller PREPARATION/T082. Existing0.5 game behavior and fullP0 gates unchanged; no impaired runtime until separate MAIN pins/release.

D079 adds only PORTABLE_FORMAT_FOUNDATION.md0.1 exact bounded envelope/map-decoder source prerequisites T083/T084. Existing0.5 runtime contracts/fullP0 gates unchanged; no gameplay/app/protocol integration or phase acceptance.

D084 separately approves PLATFORM_DECISION.md0.1 foundation/support/reference/initial measurement subset after actual normal/impaired relay evidence; full P0 remains open. D085 separately approves CANDIDATE_BUILD_FOUNDATION.md0.1/T088 reusable fixed-network build tooling preparation. Existing runtime contracts/artifacts/limits remain unchanged; T089 exact MD3 compatibility fix and T090 isolated LLVM startup are individually scoped prerequisite tickets.
