# T022 source inspection handoff

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T022 revision 0.4 RELEASED; submission for MAIN review, no authoritative status change
- Phase / contract revisions: BROWSER_FOUNDATION 0.4, GOVERNANCE 0.4, P0 prerequisite subset 0.4; D004
- Base commit and pre-existing edits: `13f0d8eea4822dee5c976661218d022be74342e3` plus D004-review-baseline.json and existing worker outputs. No existing source/tooling/header file changed. main.cpp and server.cpp now differ from D004 under other workers' current assignments; all other D004 source hashes match. Existing T016 tooling/header hashes are captured and verified unchanged in `web/build/sdk-inspection/protected-files.json` and `validation.json`.
- Changed files: new `web/build/sdk-inspection/{extract_source.py,REPORT.md,sources-and-artifacts.json,manager-extraction.json,compiler-extraction.json,protected-files.json,validation.json,acquisition-commands.json}`, own question `notes/questions/T022-engine-sdk-execution-approval.md`, this handoff. Acquired official archives/metadata, non-executable extracted data and four negative archive fixtures exist only beneath `/private/tmp/outbreak-web-sdk-inspection/**`.
- Commit or patch reference: none authorized/performed

## Acceptance evidence

All results below concern acquisition/static inspection/proposal only.

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1. Official sources, exact manager commit, archive/file SHA-256, existing SDK identity; no moving substitution | PASS | `sources-and-artifacts.json`, both extraction manifests, REPORT identity table. Initial main lookup resolved manager commit, then archive acquisition used that immutable commit. Version 7.0.0 and approved release build identity confirmed in its frozen metadata; official release DEPS confirms compiler source commit. No latest SDK selected. |
| 2. Inspect install/activate/env, downloads/extraction, subprocesses/hooks, path/cache/tmp and actual required port recipes | PASS | REPORT findings table with exact source paths/line references and inspected-file hashes. Read manager Python/shell/env helpers, component/meta-package paths, compiler startup/config/cache/sanity/temp/build/ports/install/bootstrap sources and selected SDL2, SDL2_image, zlib, Vorbis and Ogg recipes. Conditional libpng/jpeg inspected but not proposed. No acquired code imported or run. |
| 3. Exact scoped later install/activation and real release/debug clientgame/main object-probe plan | PASS | REPORT exact commands and clean child environment; explicit component installs avoid npm meta-hook and extra Python. Source/config/binary member/hash inspection gates identified before compiler execution. SDK/config under task-local root; cache/ports/tmp/objects under Engine-owned paths; no shell/global activation. All commands are proposals, NOT RUN. |
| 4. Exact future hosts/artifacts and official expected hashes, truthful unknowns | PASS | JSON lists two exact Google bucket binary artifacts with publisher hash null, five exact port URLs with expected official recipe SHA-512 and archive_acquired false; REPORT distinguishes local source SHA-256, source commits and release-build identity, and lists permitted redirect hosts. No fabricated binary archive digest or signature claim. |
| 5. Executable-free inspection report and concrete next authorization, no acquired execution/global mutation | PASS | REPORT, new T022 question note. Acquisition/extraction commands in JSON; only curl, stdlib data processing and own reviewed extractor ran. `/private/tmp/outbreak-web-sdk` remains absent. No install, activate, emcc/em++, Node, port import/build, game/server or global activation executed. |

Official identities:

- Manager: `1693ce7359fc9694f198694f902a2cc061239b86`; acquired archive 178744 bytes; SHA-256 `fd37b19a256254cd90c1737062ee77ab4d82341c4c7bc890601b1a355034f345`.
- Compiler source: `777e6e5db7b4990bcaeb1b9998ed642cc84e6629`; acquired archive 33022062 bytes; SHA-256 `80dc86d6a15382f234688fd491bd30692dc1c9f019c67563ae701176b9964d16`.
- SDK: 7.0.0; release build `6afbd83493d647051772d491124187d4e9a0cda9`. This is not either archive's integrity hash or the manager revision.

Commands and tools: existing Python 3.11 stdlib and system curl. Exact successful acquisition/extraction argv in `acquisition-commands.json`; curl HTTPS requests fetched official immutable source archives and release metadata only. Normal sandbox DNS failed on initial metadata lookup, then scoped curl escalation was approved; no credentials or alternate project/system were used. A GitHub mirror DEPS URL returned 404; the manager's declared official Googlesource repository succeeded. No installer code ran even to obtain help/version.

Reviewed authored extractor before executing:

```sh
python3 web/build/sdk-inspection/extract_source.py /private/tmp/outbreak-web-sdk-inspection/emsdk-1693ce7359fc9694f198694f902a2cc061239b86.tar.gz /private/tmp/outbreak-web-sdk-inspection/manager
python3 web/build/sdk-inspection/extract_source.py /private/tmp/outbreak-web-sdk-inspection/emscripten-777e6e5db7b4990bcaeb1b9998ed642cc84e6629.tar.gz /private/tmp/outbreak-web-sdk-inspection/compiler
git diff --check
```

Both source extractions passed, writing only mode-0600 data files beneath
the allowlist. Four negative fixtures (parent escape, absolute path, link,
duplicate member) each exited 1 before destination creation. Exact argv,
diagnostics and preservation checks are in `validation.json`. These are
archive-inspection tests, not compiler, renderer or game evidence.

## Implementation status

Completed the T022 inspection/report/proposal deliverables. The safe source
extractor executes only our own reviewed stdlib code and never imports acquired
source. Machine-readable hashes cover each extracted file and the specific
inspection entry points. No existing T016 file, earlier question/handoff,
header or other worker output was edited.

No simulation or fixture is used as Wasm evidence. No binary SDK/Node archive
or port source was acquired; only source archives and first-party metadata.
Actual installation, activation, first-use port execution and four proposed
Wasm object probes: NOT RUN by design. T016/T017 remain partial; no linked
client, renderer, browser game, dedicated-server or multiplayer success.

## Integration and questions

`notes/questions/T022-engine-sdk-execution-approval.md` requests a new bounded
setup release after MAIN reviews REPORT's exact sources/commands/roots.
Important unresolved execution prerequisites are binary archive member/hash
validation (SDK manifest supplies no publisher hash), installed package/source
comparison, real compiler diagnostics and port preparation. The proposal
requires stopping instead of invoking a missing npm/bootstrap hook or widening
hosts/paths. No SDK pin or existing probe config was changed.

Before submission, reread revision markers: ticket remains 0.4 RELEASED;
BROWSER_FOUNDATION/GOVERNANCE/P0 remain 0.4. MAIN retains acceptance and
future execution authorization. No messages or work dispatch to other chats,
branch operations, commits, pushes, resets, reverts or services performed.
