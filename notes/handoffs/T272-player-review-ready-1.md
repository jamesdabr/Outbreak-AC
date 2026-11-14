# Ticket handoff — T272 REVIEW-READY

- Worker: Player /01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T2721.0/D456; BLACKWOOD_NATIVE_BUILD_PREPARATION0.5, reread before submission. Authoritative status unchanged.
- Base/pre-existing edits: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work; no Git command. Prior visible-native-1/control/singleton and all historical evidence untouched.
- Changed files: ONLY web/server/blackwood_candidate/{stage.py,build.py,test_preparation.py,SCHEMA.md,README.md}; NEW preparation-1/plan-pass-10.json, preparation-1/pass-10/**, supervisor-fixtures-1/pass-10/**; own source-diff and this handoff notes. verify.py byte-identical; RealOps backend AST-identical to accepted pass9.
- Patch reference: notes/handoffs/T272-player-source-diffs-1.md against accepted pass9 snapshots. No commit.

## Acceptance evidence

PASS sole inspected guarded pass10:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B web/server/blackwood_candidate/test_preparation.py --pass-id pass-10 --plan-sha256 6f07ddfd1c22f7cef39ddeb47a2007477d834f6ced16e715be5fb116eaa5b8e2
```

23/23 SIMULATED checks passed in25.677495s before result publication,45,943 observed fake-output bytes before small summary,7,425,369 storage bytes before results. Nine expected guard self-check denials, zero unexpected denials. Existing256cases/300s/8MiB/128MiB limits and pre-import effect guards unchanged, with original cutoff through persistence.

Result: web/server/blackwood_candidate/preparation-1/pass-10/result.json SHA256 `088f6b3f0886ed1799879b605c624a1caf754967d708d2bd10b8d0fca2eaf017`. Six current sources match executed snapshots and plan/result pins. New artifacts include4,736 readable regular files, with no physical special/unreadable nodes.

Coverage: existing nominal126-command/32-object/two-link build + independent verifier/idempotent receipt success; a second complete build with explicit EPERM denial on all126 steps followed by independent verification;16 supervisor/strict-ledger cases and five candidate-manifest cases. Confirmed-empty EPERM passes. Live/unknown/error group, failed/unknown/nonzero reap, missing/nonzero/wrong-child prior observation, unexpected EACCES, unrelated cleanup error, deadline, log/receipt failure all refuse. Strict step validation rejects unknown denial enum or missing closure/observation facts. Candidate binding passes; wrong candidate, legacy selector, self-reference and invalid ID refuse; a synthetic legacy singleton remains unchanged. Original202 general cases retain their names and behavior except fixture manifest derivation; universe250, only23 selected checks run as authorized.

## Implementation status

Implemented explicit `EPERM_DENIED_WHILE_ANCHORED` signal outcome, never a sent-signal claim. Only PermissionError errnoEPERM qualifies; a prior exact typed original-child exit0 observation is required. Original-handle reap must return integer0, group absence must be independently positive, and every existing error/deadline/output/cleanup/persistence/source/closure condition must pass. Denial evidence remains in raw receipts/final ledger. All other errors remain fatal. No signal retry/post-reap mutation/PID discovery/fresh grace or OS privilege change. The underlying original-handle RealOps implementation is unchanged.

Implemented stage.manifest_path(validatedCandidateID) => web/repro/blackwood-source-manifests/ID.json. Authorization accepts only that candidate's derived path; active manifest cannot appear in its own source entries. No new CLI/path selector. Fixture data and schema match; independent verifier needed no edit because it uses stage authorization/strict step validation. Existing actual singleton/control/failed attempt are preserved. MAIN should use the new helper when constructing fresh candidate controls; no new real manifest was authored here.

Final source SHA256:

- stage.py: `5b4ad2ee3ee860899fbecb84a2d3b9f592e6828e39dec0d434a4a7139e0b9696`
- build.py: `5a5989bd9ca2f7a3045a0facdcd9adedb29f1bb4f3ba799129d72721f1dcb010`
- test_preparation.py: `0f94ca6de49b52869a8cd77b9463dea2b5199a59c76c70686094cea3181eb365`
- SCHEMA.md: `5c446b1c99ba466170bd540b40e38702060b1367e9c48e3862705866a2694f9f`
- README.md: `40936d1b62228010fe668dea6a43306a3f2ae2e0601f6f390ed0304ad25a1c8b`

SIMULATED only: denial, original exit/reap, group observation and all tool/compiler/inspector activity are injected fake effects under existing guards. No actual signal/tool/FFI/compiler/signing/framework-copy/build/observation/runtime/server/browser/network/Git execution or attempt retry occurred in T272. No claim that sandbox cleanup of a live service is available. Actual source/SDK/tool/runtime compatibility and later live playtest gates remain.

## Integration and questions

No targeted-check failure remains. MAIN reviews stable source/results before constructing fresh candidate-specific manifest/control and separately releasing visible-native-2. visible-native-1 must not be retried or rewritten. This handoff does not release any actual effects. Stop at REVIEW-READY, no live process handle remains; QA/T149 and other holds unchanged.
