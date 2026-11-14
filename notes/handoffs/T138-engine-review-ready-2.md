# T138 returned overflow correction — review-ready checkpoint4

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket/contract: unchanged T1381.0, smoke0.9/D159, admission0.4. MAIN returned checkpoint3 for one in-scope correction. Same unfrozen v4 package; prior handoff/evidence retained.
- Changed since checkpoint3: only policy.py failure_errors(), test_policy.py test66 assertions, and SCHEMA.md private overflow description, plus new owned preparation evidence and this own handoff. Lifecycle/source/effects/success sealing code unchanged. No Git or frozen predecessor edits.

## Correction and evidence

PASS — checkpoint3 incorrectly allowed overflow to discard a distinct closure error. Checkpoint4 reserves closure and fixed truncation marker within16 entries. On overflow, retain first14 primary entries plus marker and distinct closure. If closure already occurs within first15 retained rows, preserve that occurrence and append marker. A duplicate closure whose first occurrence was outside the retained prefix is now retained once. Redaction/240-character truncation precede deduplication/selection; primary order remains. Marker text itself is not duplicated. Failed null hashes/empty captures and all successful terminal gates remain unchanged.

Test66 now covers16 and20 primary entries with unique closure, duplicate closure outside the kept prefix, duplicate closure inside the prefix, closure equal to marker, plus existing redaction, deduplication and240-character checks. The former closure-dropping expectation was removed. All61 original Python cases and seven focused methods remain.

PASS guarded Python command from /Users/jd1/code/apps/outbreak:

```text
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B web/runtime/pair-smoke-v4/test_policy.py --review-ready
```

68tests/0failures/0errors, actual effect attempts[], FIFO/unreadable touches[]. Full unchanged D157 public-data pure proof replay still PASS as REPLAY_OF_RETAINED_FAILURE_EVIDENCE, not runtime or retroactive acceptance. Node source/harness unchanged since passing33-case run; not rerun per MAIN. No actual CLI/admission/native/browser/network/inspector/probe/service/build/install/pins/retry or forest audit. Player's separately authorized T136 work grants no effects here; QA remains paused.

## Checkpoint identities

Paths below beneath web/runtime/pair-smoke-v4/preparation-T138-1:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| review-ready-4.json | 11829 | d0f81e58248c74b30f134433220949cfce59a6762d4aa0e0a58af405d54d7a63 |
| python-result-4.json | 1491 | 41b4c6d7dcd68a3175db75a5b3344eb9ce520e19c2bd33e80bda12c9eaecad9a |
| saved-evidence-replay-4.json | 1044 | 2cea23a8d336ec79653784d8c7560225b8d5f8e95c85b7e33884d62658772f99 |
| source-diff-4.patch | 33302 | 883559f5425d87d33a643eec1479e31addeafc70db188d6ba3879f25eccc5829 |

All nine current hashes directly rechecked against checkpoint4:

| File | SHA256 |
| --- | --- |
| policy.py | 640227a9c4f7e8dc8b74a34645dda75d9146c0e9c98969815283fee780cbe3a5 |
| supervise.py | 402e19ab4c361ceb17e8348419a546530226ad17f0bde372d167591ff4f6091f |
| ownership.py | cb5765c175ebd936263469e7ce9aa3154ae3116176caca969e51c8cba3ea0c18 |
| observe.cjs | 57a8f4e88a0ff25d65728e99f463ecdba6252d17ae98e717f834cbd66c253b93 |
| run.py | ed890015af0b3e0356d251d72b7d93e9e232db29b5b6789472ba0452a1203531 |
| test_policy.py | 8c6971c70cfc70f2ab13a966159b42fbaab51820b07ea66e2ff7898197298064 |
| test_observe.cjs | a766661f024433b297ac72e18008ff061815a516c9a68d25a37efd84577fb6a4 |
| SCHEMA.md | 624e26c8c36d85fa6067bfa2d16aa8df8099576795c3c30cfe61501e6658318f |
| README.md | 880b3e0eae5ae7444b12203db00d8d52f12f228ea50f8251cc775477f5db7fe4 |

Baseline/node record/source mapping and full original handoff remain notes/handoffs/T138-engine-review-ready-1.md. Only its checkpoint3 overflow description is superseded by this corrected checkpoint4. Ticket1.0 and smoke0.9 re-read before correction; no governing revision change. Await MAIN independent review and explicit freeze clearance. No freeze, selfacceptance, runtime/P0 or gameplay claim.
