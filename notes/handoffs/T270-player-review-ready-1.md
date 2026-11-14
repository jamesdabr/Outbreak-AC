# Ticket handoff — T270 REVIEW-READY

- Worker: Player /01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T2701.0/D453; BLACKWOOD_NATIVE_BUILD_PREPARATION0.4, reread before submission. Authoritative status unchanged.
- Base/pre-existing edits: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work; no Git command. T268/pass8 and T269 failed observation remain intact.
- Changed files: ONLY web/server/blackwood_candidate/{stage.py,test_preparation.py,SCHEMA.md,README.md}; NEW preparation-1/plan-pass-9.json, preparation-1/pass-9/**, supervisor-fixtures-1/pass-9/**; own source-diff and this handoff notes. build.py/verify.py, T266 launcher and all old artifacts untouched.
- Patch reference: notes/handoffs/T270-player-source-diffs-1.md against accepted pass8 snapshots; no commit.

## Acceptance evidence

PASS sole inspected guarded pass9:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B web/server/blackwood_candidate/test_preparation.py --pass-id pass-9 --plan-sha256 cb18de2c8d60205e26048f29ec27494e6b85f281207b9c5bf8fb2ae53273c6a2
```

27/27 SIMULATED checks passed in18.717096s before result publication,24,487 observed fake-output bytes before small summary,6,281,148 storage bytes before results. Nine expected guard self-check denials, zero unexpected denials. Existing256cases/300s/8MiB/128MiB caps/pre-import effect guards unchanged, with original cutoff through persistence.

Result: web/server/blackwood_candidate/preparation-1/pass-9/result.json SHA256 `63071587ebd243b428b5a2019a2d47758e6512b8274f082c86e9f177ebd672bf`. All six current sources equal executed snapshots and pinned plan/result. Post-pass lstat inspection of the NEW roots found5,174 readable regular files and zero physical special nodes; no new mode0/FIFO/socket artifacts.

Coverage: existing complete126-command/32-object/two-link fake build and independent verifier/idempotent optional receipt success;26 targeted tree checks. Deterministic complete metadata rows include injected unreadable/FIFO/socket/symlink nodes without opening fixture content or following the simulated links. Actual authorization rejects member addition/removal, inode/time/mode/owner/link/size/raw-target changes. Strict row shape/kind/version/count/digest/root checks refuse; outside-root unreadable/special still refuse; readable forest source/manifest/dependency promotion refuses. Production-mode tests require both roots and all seven originals, and reject missing/changed originals or missing forest. Original202 general native case names remain unchanged; only superseded19 D446+19 D450 per-file schema cases retired from live harness, retaining their snapshots/results. Universe228; only27 selected tests executed, no unrelated full rerun.

## Implementation status

Implemented the D453 boundary: exactly web/repro/tests/prerequisites and web/server/blackwood_candidate/supervisor-fixtures-1 are pruned from content-hash traversal and represented by strict `opaque_fixture_tree` rows in preservation and protected inventory. Each row has fixed kind/version, positive entry count and SHA256 over the root plus every descendant's deterministic sorted depth-first metadata stream. Entries include relative name/type/mode/device/inode/link/uid/gid/size/mtime/ctime/raw-link target. Rows are discarded after hashing; no complete metadata ledger is retained. Root/ancestor type checks and traversal errors refuse incomplete membership. Both roots are mandatory in production.

All forest descendants, readable or otherwise, are excluded from ordinary/hash/consumed roles. Actual source/input content hashes and outside-root unreadable/special refusal remain. The original seven D446 literal metadata records are AST-identical to accepted pass8 source and checked for identity/presence inside the first production forest. D450's per-copy list and individual opaque-file schema are removed, rather than expanded. No new generic path selector/scanner framework, package or gameplay interface.

SIMULATED: new files are readable; lstat/raw-link/read-denial boundaries inject invalid metadata into the actual inventory helpers. No historical unreadable/special node was opened, permission changed, repaired or deleted. Fixture content integrity is explicitly unavailable: same-size content changes with unchanged metadata are not claimed detectable. Complete current before/after metadata fingerprints are required; actual build inputs still require their content hashes.

Final source SHA256:

- stage.py: `ed71a0986688b0d6639ae9fc18d5ef00df117b1fc6ba7b08ede70cf706dccb88`
- test_preparation.py: `0b582ba160e54cddd9295c054a13910752ab682c08bed314fe27fb29b7136334`
- SCHEMA.md: `744a17eedaa7c1316715ffdacd19fd5cf8c7a587d1c70ca59c4f8eba6256fcb4`
- README.md: `bf7d25f4f00bbaf3b2697c16a6cb7aa087a9e2a5c60a1b9b4a6624ea59bad748`

NOT RUN: actual retained-forest/current-input observation, T269 retry, actual project plan/build/verify/tools/version/compiler/signing/FFI/framework-copy/native/server/browser/runtime/network/Git. Actual attempt root remains absent. No native/tool/ABI/gameplay acceptance is claimed.

## Integration and questions

No targeted-check failure remains. MAIN reviews this source/result before separately releasing the fresh current-input observation against stable source/T266, then forming the concrete native build control/command. This handoff does not release an observation or build. Stop at REVIEW-READY, no live process handle. QA/T149 and other holds unchanged.
