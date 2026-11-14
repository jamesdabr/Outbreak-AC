# T1501.2 World corrected review-ready handoff — attempt2

- Worker: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Governing: T1501.2 / ANGLE_TABLE_FOUNDATION0.3 / D183,D188,D191. Revised ticket, contract and D191 read before correction and again before submission.
- Status: PASS_REVIEW_READY_NOT_FROZEN, DATA_ONLY. MAIN acceptance/freeze clearance pending.
- Writes: corrections only to existing own generate.py/verify.py/test_angles.py/SCHEMA.md/README.md (LICENSE.txt unchanged); new fixed attempt-2 allowlist; this new handoff. Original successful attempt1, prior question/handoff and MAIN original-source archive unchanged. No production/source/API/toolchain/accepted-asset/Git or other worker writes.
- No third attempt or automatic retry. No runtime/gameplay/consumer/QA authorization inferred.

## D191 correction

Production terminal_success now performs summary construction/accounting, fallible reporting, budget checks and failure-marker absence checks before its last success write. The summary honestly says VERIFIED_PENDING_TERMINAL_COMMIT. No production log/tick/validation follows successful result creation. An IO error during partial creation is caught and records a failure marker; the consumer refuses that state.

Production verify.terminal_state checks failure.json with lexists before opening result, after its read, and again through the standalone main's post-certification gate. Any marker path refuses consumption without opening its bytes: ordinary/malformed/dangling-link/nonregular markers all fail. Result must be canonical ordinary0644/single-link and unchanged around no-follow bounded IO, with explicit success status. Standalone main compares its pre/post terminal receipts too. Thus a historical or unexpected post-publication failure marker cannot be hidden behind PASS.

Added controlled tests use the actual production terminal-success/failure and consumer helpers in owned fixtures: reporting failure before commit leaves no PASS, reporter observes success absent then result exists afterward, and unexpected logging failure after a fixture commit leaves both marker/PASS and is refused. Ordinary/malformed/dangling-link/directory marker cases and partial result are refused. These are in-process callbacks/fixtures, no host fault injection and no actual final-output mutation. Preserved fixture failures are intentional and remain inspectable.

Resource field now explicitly says UNCONFIRMED; suggested Darwin bytes is a Python/platform source interpretation, not calibrated. resource_budget_verified:false. No raw ru_maxrss unit/calibration/budget/performance conclusion is promoted.

Mathematical algorithms and caps unchanged: before execution an AST comparison against MAIN-T150-review-ready-source-snapshot-1.json confirmed identical generator Intervals/rounded/initializer/material and independent RationalCheck/nearest/parse_initializer/structure/certify definitions. MAIN's snapshot stays an immutable external reference.

## Exact one fresh run

Original cwd /Users/jd1/code/apps/outbreak:

```sh
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/angles/T150/generate.py
```

New literal attempt-2 absent before invocation. Only one invocation; tool session22387 retained/polled to authoritative exit0. No standalone verifier rerun or generation retry. Recorded precommit elapsed39.480052792001516s; last precommit budget check enforces295s work/300s whole bound. All source inspected and AST syntax checked before execution. Fixed Python3.11.9 and inspected python3→python3.11 interpreter alias unchanged; no driver process launch/compiler/Node/browser/server/network/install/Git. -B prevents bytecode output.

Captured stdout is deliberately precommit evidence, not the final PASS authority:

```text
T150: first certified generation
T150: independent rational verification
T150: deterministic second generation
{"artifacts":{"angles.bin":{"bytes":101544,"sha256":"8151371e576116c6bc793e63f276205a0830580166dd7b5205d8b8ab3d3e7741"},"angles.inc":{"bytes":266487,"sha256":"a275cd06d37639ec527d0b12065404621c55289848efa9f24e173d02c3a082cf"},"certificates.json":{"bytes":2857174,"sha256":"b83b8076387c5858e8ea4b1e76e656e5221ac74a2df8ecb3f40e0a0225d555aa"}},"canonical_sha512":"e1c624f517e5deb87c749d472c430113dc9fb9c234eb85bd159bf9ef6ea29c482156123f86846824127d481f87f990dea3541f7c8f88729454abd911a118a417","elapsed_seconds":39.480052792001516,"entries":25386,"status":"VERIFIED_PENDING_TERMINAL_COMMIT"}
```

After authoritative exit, retained result.json actually exists with PASS_REVIEW_READY_NOT_FROZEN and root failure.json is absent. Result identity:1906bytes/SHA256ad69f58e41638157e6c30abced5fc11992ef67ac74a761ab47996efda070a2ec. Only this successful terminal receipt plus absent failure marker permits consumption; source/report stdout alone does not.

## Certified bytes and deterministic identity

PASS: all25386 Q30 values independently certified anew using the same separate direct rational polynomial/alternating-sum checker. All usedB64, symbolic quarter endpoints unchanged. Generator128 sine terms+one remainder,512 terms per Machin arctangent; independent checker16 direct polynomial terms per endpoint+one remainder. No approximate arithmetic, midpoint/tolerance or bound relaxation.

New bin/inc are byte-for-byte identical to successful attempt1. Certificate math/rows/pi/schema are also identical; only legitimate generate.py/verify.py source fingerprint fields differ. First temporary, second reproduction and new final three artifacts all match exactly within attempt2. Root artifacts ordinary0644/nlink1.

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| angles.bin | 101544 | 8151371e576116c6bc793e63f276205a0830580166dd7b5205d8b8ab3d3e7741 |
| angles.inc | 266487 | a275cd06d37639ec527d0b12065404621c55289848efa9f24e173d02c3a082cf |
| certificates.json | 2857174 | b83b8076387c5858e8ea4b1e76e656e5221ac74a2df8ecb3f40e0a0225d555aa |

Canonical SHA512 remains:
`e1c624f517e5deb87c749d472c430113dc9fb9c234eb85bd159bf9ef6ea29c482156123f86846824127d481f87f990dea3541f7c8f88729454abd911a118a417`

No production header/getter/table consumer or gameplay interface is added.

## Bounds, tests, resource accounting

Actual generator maxima8109integer bits/66interval operand bits/130interval product bits; contracted limits16384,2^(B+8),2^(2B+16) preserved. Both new generations together2048 atan terms and6497792 sine terms. Independent checker max9624integer bits,16 direct terms per endpoint/812224 polynomial terms total; all25386 entries certified, precision64. Higher precision branches not represented as actually exercised evidence.

30 controlled in-process cases PASS:25 expected refusals/5 positive checks. Original22 math/format/path/import cases retained; eight terminal-state/order/reporting additions passed. test.log SHA25601b27f7b8803f3edfe419ceeceafda51c1906de96f67f634ff39d33d3ff2bd0a. Guarded import probes of three new modules observed zero mutation/process/network effects.

Actual retained attempt2 nonfixture file bytes9716411, fixture bytes6862069, each below32MiB; certificate2857174bytes below8MiB. Fixed CLI output and30-line test log below8MiB. Counts include terminal-helper fixture records according to their actual location; driver retained counters are bookkeeping snapshots before final result, not exact final file-size sums.

Raw resource_maxrss138133504; units explicitly UNCONFIRMED/source interpretation only, not unit calibration, actual RSS/budget/performance acceptance. Runtime/gameplay/P0 and resource_budget_verified remain false.

Fixture aliases: fixtures/alias→occupied and fixtures/pass-plus-failure-dangling-alias/failure.json→missing-target. They are retained links, never followed for writes/marker reads. The directory-shaped failure marker is an intentional nonregular fixture, not a root output. Controlled post-publication fixture contains intentional PASS+failure; it must remain unconsumable and does not describe the successful actual root.

## Preservation and exact evidence

input-identities.json contains before/after16 protected references, including current contracts/ticket/D183/D188/D191/advisory, accepted numeric/core/hash and T147/T148 freezes, and MAIN original-source snapshot. All equal. It also contains full no-follow56-row original attempt1 graph snapshots (including its root, files/directories/fixture link), all metadata/bytes/hash/link targets equal. A targeted post-terminal read-only recheck matched every recorded reference identity and all56 original-history rows. Attempt1 remains successful exit0 evidence; it was not relabeled or rerun.

All six source identities remained equal during execution, then raw hashes rechecked after terminal. Root source fingerprints:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| LICENSE.txt | 1239 | 1aa31fc3b91eb5bdff974859c02ea16317e6073345cce35412bfcea490da41f7 |
| README.md | 3626 | 427b8bf52d8631800e6835f182cafbea09a31f001f31a356309cd175c75afb15 |
| SCHEMA.md | 7827 | 9d6c979c331623fce2ed8eef285986db9e898649ca8ff26397b2a4bd952bac1f |
| generate.py | 19721 | 9ad55dd1318450f9c476192ea3fb09ff0d42978b65492456e69efb480874b246 |
| test_angles.py | 10221 | 0957f8a77940b512c9373bebb8c8f93b9457cf8525cfaa9456c2d6dd01f604d0 |
| verify.py | 17095 | 7495303923549a7a360b9018a17df35ea56efd92235b8aba8d8b188eed91f40e |

New attempt2 contains only contract-approved root artifacts/result/plan/input-identities/sources/commands/test.log and temporary/, reproduction/, fixtures/ data. No root failure.json or unauthorized inventory/receipt/freeze. Original source bytes are recoverable via MAIN's immutable snapshot, bound in new before/after references; current source has only the correction lease.

Actual implemented/certified: immutable mathematical artifact, independent checker, reproduction and production terminal-helper fixture coverage. Simulated: intentionally corrupted/failed owned fixture states only. NOT RUN: native/Wasm/renderer/consumer/input/aim basis/gameplay, runtime/memory-capability calibration, performance/fullP0/P1/MVP/human acceptance. QA/T149/Q1 and future PackageB gates unchanged.

World stops edits/tests/execution at this new REVIEW-READY submission. Await explicit MAIN review/clearance; final freeze must bind both attempt histories and external authorities. No third attempt.

