# T129 metadata successor — review-ready checkpoint 1

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket: T129 revision1.0 RELEASED guarded preparation; CANDIDATE_PAIR_SMOKE0.6/D142 and unchanged admission0.4 API.
- State: REVIEW-READY, NOT FROZEN; no selfacceptance or ticket-status amendment. MAIN review/clearance and separate actual-size compatibility evidence remain required.
- Base: exactly copied nine frozen T117 sources, each verified against its immutable freeze before copy. Baseline hashes and old freeze identity are in web/runtime/pair-smoke-v2/preparation-T129-1/baseline.json. Original T117 sources,52-member freeze and all prior successful/failed evidence remain unchanged. No Git commands/mutations/commits or unrelated edits.
- Changed files: NEW exact nine web/runtime/pair-smoke-v2/{policy.py,supervise.py,ownership.py,observe.cjs,run.py,test_policy.py,test_observe.cjs,SCHEMA.md,README.md}, NEW preparation-T129-1 evidence and this own handoff. run.py is an unchanged byte-for-byte copy. No dependencies/assets/game source/public API/wire/topology/output selector changes.

## Acceptance evidence

PASS — inspected guarded FIXTURE_ONLY builtin suites, cwd /Users/jd1/code/apps/outbreak:

```sh
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node web/runtime/pair-smoke-v2/test_observe.cjs
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B web/runtime/pair-smoke-v2/test_policy.py --review-ready
```

Python48 tests,0failures,0errors (7.006s full suite). Node27 tests,0failures. All original40Python/24Node regressions retained with new source-root/preparation/four-kind fixture shape adaptations. Both report actual_effect_attempts:[] and fifo_open_or_mutation_attempts:[], with actual_runtime/authority/P0:false. Python audit/patch guards precede project imports; Node denies effectful imports/process/network/random/timer APIs. No actual controller/admission/inspector/native/browser/gateway/network/compiler/install effect occurred. Test files write only new owned preparation evidence. No historical FIFO was created/opened/read/hashed/written/chmodded/deleted/repaired; FIFO snapshots use injected stat metadata.

Exact evidence under web/runtime/pair-smoke-v2/preparation-T129-1:

| Record | SHA256 |
| --- | --- |
| review-ready-1.json | d4e65802e23ef3faef63fa29891c23121933454a7599dbcbac6ec9aec46af91a |
| python-result-1.json | 505d87a272e4d0ddfcd3a817787f777cbb721b21ab84dbb99dc02cf9a8f66fcd |
| node-result-1.json | 669efec68feb4a8e1126695447d9b51f65c0060fd62408557597190f4fded561 |
| source-diff-1.patch | 6d3059ee7d270242e6b37812bbba68625f4ccd641f3f8df80957bfba2eed053a |

Full outputs: python-test-1.log and node-test-1.log. Review record binds all nine current source/test/schema/doc hashes, retained preparation members, baseline/diff and governing ticket/contract/D142/preflight digests. Both result records bind the tested sources. No freeze or final preparation result has been created.

## Exact source and schema hashes

Paths relative to web/runtime/pair-smoke-v2:

| File | SHA256 |
| --- | --- |
| policy.py | 0408fa402c54bd966d8171039db5105c49eaead424740968313167a49e7c6937 |
| supervise.py | 73ac782e8876ca999bca4abf9d258fa7d1820b520ce9624959ec4a98a3207161 |
| ownership.py | df10029d14178a247efae36312556850808a9d34f2fd8929e5299c7973d828ba |
| observe.cjs | a6ecf544f5b6133be23a79c28523e264ea7e2b273cebf1b429cd345f7bbeca5f |
| run.py | b2d251c2bf071cab4cb93588c0df0ce2143bc89fbf338fe2d2d1fe2a794211bc |
| test_policy.py | 146c5398350eb1eced4793a738115a3d1ae56591897262af0d1db8a97706ba5e |
| test_observe.cjs | bfe32a7df79b82c9143c23f635fe9820a3ef18586c031c5fc8820789c2a5287c |
| SCHEMA.md | 387e40d17c2b2fe464034248b0c37819772dd4411c359d0992015347fbb9644f |
| README.md | 598d5a488b66bc6bc6b7bee141983f91a44519b46658169041fe62f1b1889a56 |

## Implementation status

Only D142 metadata policy and fixed successor identity were implemented. HERE/newcontroller now names pair-smoke-v2; no selector/fallback to the old controller. Original repository root/admission_v4/stage helper/output derivation/topology/tools remain fixed. The copied ordinary-input movement, native/gateway/parsed receipt proofs, authentication self-row, narrow otool rule, no-follow private cleanup, loaded mapping checks, acquisition ownership/disposal, bounded streaming, terminal seal and all prior fixes remain.

Full-preservation metadata uses128MiB byte bounds,250000 map entries and4000000 aggregate nodes. Depth32,arrays100000,strings4096 and finite safe numeric/type/duplicate rules remain. Trace in SCHEMA.md covers authorization lstat/bounded read, gate parser, private-plan serializer before effects, validated-plan/ledger writes, original/prospective inventory serialization and child plan/pins byte/UTF-8/duplicate/complexity checks. Child raw pins and plan are bounded before read/trust. Ordinary admission/source JSON retains earlier32MiB/100000map/1000000nodes (admission8MiB). Combined streamed evidence8MiB,512events/1MiB retained snapshots and every runtime deadline remain unchanged.

Preservation now has exact fifth field specials. It contains exactly the seven literal FIFO paths from MAIN's preflight, exact {kind:fifo,mode,nlink:1,device,inode}, sorted and disjoint from files/directories/links. Snapshot checks known path/FIFO type before its ordinary-file branch and uses only no-follow lstat metadata. Current metadata is checked against original before/after. Snapshot, effective baseline, additions, original-UNION ledger and final/prospective receipt inventory carry all four maps; owned.specials must be empty. No generic special exception, historical exclusion, symlink following, consumed FIFO or owned special is allowed.

Tests44–46 cover exact seven roles, wrong/missing/foreign/retyped/symlink/socket/device/hardlink/type/conflicting roles, changed inode, consumed-role confusion and owned-special negatives. Injected snapshot opens nothing even for a known FIFO retyped ordinary, and guards record zero FIFO touches. Test47 verifies128MiB authorization read selection/refusal before oversized read. Test48 rehashes frozen T117 sources/freeze unchanged. Original terminal late-failure/prospective receipt tests now retain specials too.

## Synthetic size and resource observations

These are deterministic FIXTURE_ONLY in-memory metadata generators, never real whole-forest admission. Their repeated row values/hash data are explicitly synthetic and create no actual accepted artifact/pins files.

- Python:167033 synthetic preservation-file rows,53,468,908 compact authorization bytes and64,666,449 private-plan bytes; parse/shape/serialize/reparse successful. This exceeds MAIN's45,418,557-byte compact floor, old32MiB/100000-map/1000000-node caps. Scale case4.403s; resource.getrusage(RUSAGE_SELF).ru_maxrss raw681132032 on darwin, recorded without cross-platform unit conversion.
- Node:167033 synthetic file rows,53,450,620 compact bytes; strict metadata parse successful. Scale case1115.517ms; process.memoryUsage().rss510754816 bytes after that case, an instantaneous process observation.
- Both parsers accept exact128MiB bytes,250000-entry maps and4000000-node records, reject one beyond each, and retain depth/array/string/duplicate/nonfinite/unsafe-number negatives. Node also tests escaped-key duplicate detection and Unicode code-point strings.

These process/time/memory observations describe fixture execution only. They are not gameplay memory/performance measurements, actual browser/native timing or a claim the complete real graph is compatible.

## Integration and pending policy

MAIN's later integration update reports T130's separate authorized whole-forest hashing failed on an unreadable historical regular fixture after about5.55GB. That is not a failure of these fixtures and is not repaired or bypassed here. This D142 candidate still refuses unreadable ordinary files; it introduces no unreadable-role exception, permission change, retry or generic specials expansion. MAIN is enumerating those roles and will record any additive policy resolution. Preserve this checkpoint/evidence; do not freeze until policy/review/clearance is resolved.

Actual whole-forest integration/current admission via this caller, runtime pins/run, OS inspectors, native/browser services, real loaded-image/cleanup/deadline/movement proof and hardware/human/P0/MVP remain NOT RUN. v4/T125 evidence remains a separate dependency, not a launch token. Player/QA/T103 holds remain unchanged. Requested MAIN action: review the exact D142 candidate/diff/evidence and resolve the separately reported historical unreadable-fixture policy before final compatibility/clearance.
