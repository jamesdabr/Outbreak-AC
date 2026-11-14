# T138 source-consistent spawn history — review-ready

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket / revisions: T1381.0 RELEASED, smoke0.9/D159, admission0.4, governance0.5. T137 delivery accepted D161 before this implementation.
- State: REVIEW-READY, NOT FROZEN; submitted for MAIN independent source/evidence review. No selfacceptance or ticket/contract edits.
- Base/pre-existing edits: new fixed web/runtime/pair-smoke-v4 copied exact accepted T134 nine-file v3 baseline after checking all nine D156 hashes. No pre-existing v4 directory. Prior packages, freezes, pins, failure evidence and unrelated work preserved; no Git command or mutation.
- Changed files: only nine explicitly allowed new v4 source/test/schema/docs files, owned preparation-T138-1 evidence and this own handoff. No dependencies, game/native/browser source, build, flags, wire/API or effect scope changes.

## Implemented behavior

PASS initial/current separation: initial ordered1/2/3/4 ACK remains nonnegative-life and strictly [0,15000)ms after original source OPEN. Current settled own tuple must match the latest chronological recorded ACK, never an older match or numerically greatest life. Only same-cn nonnegative milestone4 continuations follow the handshake; event bounds/chronology and no-future-event check apply. All existing network/schema/map/error/counter/remote/render/timing/visibility checks remain.

PASS historical first-ACTIVE: a shared network-only helper checks its own schema, genuine handshake/current historical ACK and same-cn exact event prefix of later paired active, with nondecreasing public observation time. It does not impose settled timing/diagnostic getter equality on this raw historical sample. Existing current active/movement/capture tuple stability and receipt semantics remain. No sample is overwritten to pass.

PASS bounded primary error retention: only the failure constructor changes in supervisor; it calls pure failure_errors(). Receipt errors preserve sanitized report-then-closure order, deduplicate after redaction/240-character truncation and retain at most16 entries (first15 plus fixed additional-errors marker on overflow). Existing failed null hashes/empty captures remain permitted. Success-only inventory, cleanup, immutable graph, admission, deadline and final atomic seal logic is unchanged. No FAIL hash-linkage or sealing redesign from the unadopted T137 proposal was implemented.

observe.cjs, ownership.py and run.py are byte-identical to accepted v3. Node test harness changes only its owned preparation path. Python retains all61 original methods/cases, necessary v4 bookkeeping and seven focused methods (62–68); test28 additionally reproduces primary proof error followed by secondary terminal-capture error without PASS or digest upgrade. README/SCHEMA document the private semantics and unchanged acceptance boundary.

## Guarded verification

PASS — inspected fixture harnesses invoked from /Users/jd1/code/apps/outbreak:

```text
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node web/runtime/pair-smoke-v4/test_observe.cjs
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B web/runtime/pair-smoke-v4/test_policy.py --review-ready
```

Final Python68/0failures/0errors; Node33/0failures. Real effect attempts, historical FIFO touches and unreadable-leaf touches are all empty. Guards precede project imports and deny actual processes/sockets/browser/native/admission/network; only owned synthetic fixture paths may be mutated. Injected doubles remain conspicuously FIXTURE_ONLY. Existing full-preservation scale/boundary, privacy, identity, ownership/cleanup and no-false-PASS cases pass unchanged.

Focused tests cover multi-life0→1 with raw first-active0, life-number decrease, supported later ACK beyond15s without resetting initial deadline, missing/latest-conflicting/foreign/future/negative/order/extra-milestone errors, late initial ACK including a superficially timely later event, forged historical tuple/prefix/OPEN and supported life changes inside movement/capture that must still fail. Receipt tests cover real primary-plus-secondary masking path, write failure, bounds/dedup/truncation/redaction and retained failed null/empty semantics. Existing Node cleanup/capture failures remain passing.

The first Python run retained one bookkeeping error: test48's predecessor freeze path was incompletely adapted; 67 other cases including saved replay passed. Corrected test48 preserves the original T129 immutability checks and adds exact T134 source/freeze checks. Python run2 passed; final run3 includes additional focused assertions above and passes. All provisional logs/results/checkpoints remain; Node source/harness has not changed since its passing run, so no unnecessary Node rerun.

## Retained failure evidence replay

PASS **REPLAY_OF_RETAINED_FAILURE_EVIDENCE** through new pure policy.proof() on unchanged D157 report.observer and native.log, using actual classification of saved data rather than synthesizing a fixture authority. Read bytes/mode/nlink/SHA matched MAIN-T135-terminal-artifact-review.json before use; originals compared unchanged afterward. MAIN review SHA3d092d8f69b7b7a8237f11089ee726f692ad11c45b619f6b733704a579e1655c.

- report.json:215766bytes,0600,nlink1,SHA28255af21afdfd336744a4444b277515dfa1633bdb3ee46dbe3cd6f5379dc9b9.
- native.log:1168bytes,0600,nlink1,SHA34ee7b83b2a177072fbfb48c117383bfcd95bca8b6b7aaf7d832a67e772b3c09.

Full proof returns two movement directions, two loopback native connections/logins, maprev2 and two gateway UDP tuples; no further proof failure was found. It includes existing capture-state/metadata proof but does not perform new capture_files reads, runtime closure/admission or image pixel acceptance. This is saved-data interpretation only, not an actual invocation, accepted normal_pair, retroactive repair or P0/gameplay evidence. D157's original FAIL remains immutable and unaccepted.

## Exact review-ready identities

All evidence below is under web/runtime/pair-smoke-v4/preparation-T138-1:

| Record | SHA256 |
| --- | --- |
| baseline.json | aa1f01e500467b8fc2a1952704984a42fbf17e522577fcd691f53e112cef8b7c |
| source-diff-3.patch | 76ead365535c0e1b2af6c51cbee586655f46bfeaad181b686dd0311253a2a865 |
| python-result-3.json | 65668c62dd93186647c53845aeab76d95ad4c7ed4a5de5e0bbfef6a17367107c |
| node-result-1.json | e5bdb14fc48b989f54e773aa4f65d5ec5306fc3b9bf350f5a91b36ab9814e00a |
| saved-evidence-replay-3.json | 2cea23a8d336ec79653784d8c7560225b8d5f8e95c85b7e33884d62658772f99 |
| review-ready-3.json | 54c3480f9503a561ac00a72cbbfb3127888f9125602230c2cf12e9b1ebea40ca |

review-ready-3 is9997bytes, binds exact nine current source hashes, governing revisions/hashes, baseline/diff and all existing owned evidence files. Current nine hashes were directly rechecked afterward:

| File | SHA256 |
| --- | --- |
| policy.py | 4f10e112fc39c780a2800ff8067791bbc1ca47a908f14d10925d0fac021302fe |
| supervise.py | 402e19ab4c361ceb17e8348419a546530226ad17f0bde372d167591ff4f6091f |
| ownership.py | cb5765c175ebd936263469e7ce9aa3154ae3116176caca969e51c8cba3ea0c18 |
| observe.cjs | 57a8f4e88a0ff25d65728e99f463ecdba6252d17ae98e717f834cbd66c253b93 |
| run.py | ed890015af0b3e0356d251d72b7d93e9e232db29b5b6789472ba0452a1203531 |
| test_policy.py | 1a17b7e1562e4d1da2d5e14f8e38a1de26b1c85eff87a20d7147eecd53a1ceaa |
| test_observe.cjs | a766661f024433b297ac72e18008ff061815a516c9a68d25a37efd84577fb6a4 |
| SCHEMA.md | 9b47e00dbf37078666fac7806db9f1a55a366daa54639d918277dea31f3efb14 |
| README.md | 880b3e0eae5ae7444b12203db00d8d52f12f228ea50f8251cc775477f5db7fe4 |

## Pending MAIN gates

NOT RUN: actual CLI/admission verification, native/browser/inspector/service/network, new pins/runtime retry/build/install/Git, full-forest audit, pixel/art/human acceptance. No gameplay or source instrumentation changes. Synthetic PNGs remain fixtures, not application screenshots. T136 owner-approval block and QA hold remain unchanged.

Ticket1.0 and governing smoke0.9 were re-read before submission. Await MAIN independent review and explicit final freeze clearance. No freeze or further execution is implied by this handoff; returned in-scope corrections may be made only under the unchanged released preparation scope.
