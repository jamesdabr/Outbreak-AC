# T107 bounded SDK link-stub inventory handoff

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket / revision: T1071.1; D111/D112
- Contracts: native0.4; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5
- Baseline: selected current source/authority/T102 metadata individually hashed in JSON; no Git command, source revision selection or commit. Shared worktree preserved.
- Changed files: NEW notes/reviews/T107-sdk-link-stubs.json, notes/reviews/T107-sdk-link-stubs.md, own question notes/questions/T107-world-framework-directory-boundary.md, and this handoff. No existing file edited.

## Acceptance evidence

PASS — Fixed MacOSX15.5.sdk/usr/lib selected nonframework .tbd name inventory is complete: **511 names**, **130 leaf alias records**, **479 confined names**, **381 canonical ordinary targets**, **32 refused names**, **76 ordinary directories**, and **one excluded framework root**. Canonical ordinary bytes: **9130896**; sum counting confined alias names:31988770. Bounds2048names/128MiB passed. All names and refusals retained explicitly.

PASS — D112 pruning occurs before descent: excluded path only is swift/playgrounds/LiveExecutionResultsRuntime.framework. No framework child/alias/body read in the re-released collection. Directory aliases elsewhere refuse. Leaf chains check raw relative text/mode, lexical immediate targets, ordinary ancestors, selected-root confinement and ordinary .tbd terminal kind. No general symlink permission.

OBSERVED DISCREPANCY — Expected511 names and one excluded root match, but expected398 canonical targets is **not** the permitted confined count. **32 source aliases immediately leave usr/lib for SDK framework locations**, so their targets were not followed/read/hashed. Their raw text/mode/immediate paths and explicit null canonical target/refusal reasons are recorded. The remaining381 current confined targets are the available ordinary predeclaration. No outside canonical identity or hash is inferred; MAIN must not promote the32 refused names into consumed inputs from this report. This follows the ticket's explicit refusal requirement rather than bypassing confinement to match an expected count.

PASS — Required confined chains libc++.tbd -> libc++.1.tbd, libz.tbd -> libz.1.tbd, libpthread.tbd -> libSystem.tbd -> libSystem.B.tbd and libSystem.tbd -> libSystem.B.tbd verified. Each ordinary target includes bytes/mode/SHA256/all source names; all alias records preserve exact raw text/mode/immediate/canonical target and ordered chains.

PASS — SDKSettings is ordinary Version15.5, SHA25658a133735f0a55a624a1703067059f6e78925e51725ec6e1f966072e142c9c42. Existing candidate stage.py exact relevant source lines/hash plus historical lifecycle recipe/Makefile and T102 references recorded as data. No new flag/default C++ library choice, command selection or tool execution. All381 ordinary targets have recognized text headers and UTF-8/control checks; only first four lines observed, no YAML/body/schema parsing.

PASS — Two complete own-stdlib sorted inventories independently recomputed membership, aliases, directory modes, exclusions, refusals and every ordinary hash before exclusive report creation; exact equality passed. Source/authority references and SDKSettings also rehashed. A separate final read-only verification used os.walk(followlinks=False,onerror=raise) with framework pruning to rule out silent enumeration errors; all511 names/76directories/one exclusion, every381 target hash/mode/size, every130 alias raw text/mode and every named metadata reference still matched. No refused target was read. Ticket1.1/native0.4 re-read before submission.

Frozen report identities (do not rewrite):

| File | Bytes | SHA256 |
| --- | ---: | --- |
| notes/reviews/T107-sdk-link-stubs.json | 400056 | 69acf7a56bd9704f97817276b0f9f6c66b6b89e4df5ea97741efb44656957145 |
| notes/reviews/T107-sdk-link-stubs.md | 4634 | e7d60fbe86cb702f93d7110cf4ab86ca3a93a42101fd96a371d50803d7812a16 |

## Implementation status

Actual read-only DATA collection, not fixtures or a build. T1071.0 first stopped at the nested framework directory alias with no reports; its unchanged question was resolved by D112. The first1.1 strict zero-refusal assertion stopped on32 escaping aliases before reports. Final collection records all refused names, without changing the scope or reading their targets. No old observation/report was rewritten.

NOT RUN — Project import/entrypoint/tests, compiler/file/otool/version/signing, native/browser/runtime, network/service/install/staging and Git operations. No source/SDK/cache/clones/artifacts/pins/MVP/ticket/decision/history edits, dispatcher or selfacceptance. The only writes are the new report pair and own question/handoff.

## Integration and questions

Both reports are frozen for MAIN review with the398-versus381 discrepancy explicitly surfaced. No new dependency/schema/interface/flags or execution authorization introduced. MAIN supplements exact future inputs/system_sdk.files using only reviewed ordinary targets; actual linker trace must still validate current bytes and declared membership. This report does not claim all targets linked, a complete runtime library inventory, native build success, or P0/MVP acceptance.

Reproduction: fixed-root sorted followlinks=false walk with .framework pruning before descent; ordinary directory checks; resolve only confined .tbd leaf chains; compare every JSON member/alias/directory/exclusion/refusal; hash all ordinary targets and compare size/mode/source names; repeat independently, then recheck named metadata references/SDKSettings. Never read refused immediate targets or execute stored source text. Future scope changes require a new release; these reports remain unchanged.
