# T072 frozen additive published-output verification PASS

- Worker: World/Match-Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket reread before submission: T0724.4 RELEASED/D062, browser foundation/GOVERNANCE/P0 0.5; original T0664.0 recipe/D059 pins unchanged.
- Writes only NEW `web/build/verify_published_network.py`, `tests/t072/test_published.py`, `generated/t072/**` and this handoff. Base13f0d8eea4822dee5c976661218d022be74342e3/shared changes preserved. No old core/wrapper/config/source/SDK/pin/attempt/artifact/evidence edit, rebuild, compiler/Node/browser/server/network launch, commit or dispatch.
- New verifier/tests were frozen before actual verification; final code/evidence now frozen. Later findings require a new question. MAIN must separately accept/pin this verifier for any future runtime use; it is explicitly NOT a historical build input.

## Exact semantics

PublishedNetworkRecipe explicitly subclasses the unchanged hash-checked T066 Recipe. The sole phase normalization is preservation(): first pin exact original D059 document, original result/bundle identity, then independently validate BOTH exact17-file published/attempt trees against original four output hashes, metadata hash and12 current notice identities. Reject extra files/directories, missing/changed files, symlinks and any mismatch. Require the ENTIRE current preservation map to equal the original6073-entry baseline UNION those exact17 validated additions, with no baseline overlap, missing/changed original or unexplained addition anywhere. Only after this equality return the original baseline to unchanged Recipe.verify(). No unchecked directory exclusion, global monkeypatch, replacement input closure or allowance for another build.

All frozen Recipe.verify gates remain: exact complete original23474 input members/hashes, authority/profile/attempt/ports/aliases/environment, actual61 object/source/command/exit/log identities, notices, exact79 actual JS/data slices, metadata/result consistency and bundle identity. A second full observation repeats source/protection/publication checks at the end. Exact original T070 failed-verifier receipt and terminal-freeze hashes are mandatory; all162 old frozen artifact/object/log/evidence fingerprints remain exact.

## Evidence

PASS19 guarded stdlib fixture tests, zero subprocess calls. Fixtures deliberately contain synthetic sources/header-only Wasm/logs and override discovery/command generation in a TEST-ONLY subclass rooted in temporary directories; they are NOT actual compile/link/runtime evidence. Production adapter does not override those inherited methods. Negative cases cover changed/extra original source inputs, changed/removed protected files, extra preservation member, altered/missing/extra published files and empty directory, changed object/log/metadata/result/pins, wrong profile/authority/path/hash and rewritten historical failure. Every reject/pass is read-only on fixture files. `generated/t072/fixture-tests-1.json` records source identities/output.

PASS one ACTUAL read-only check of the existing frozen T070 publication. Exact argv was supplied to adapter.main under a subprocess-forbidding mock; no compiler/Node/package/browser/server/network calls. `generated/t072/actual-verification-1.json` records **PUBLISHED_OUTPUT_ADAPTER_PASS**, bundle35bad2ff04cdc17df5193ca026969380e7c9dc4176596601972b4af163b90e0a, all79 preloads,6073 original protected entries,17 exact additions and162 unchanged old evidence files. `run-record.json` retains argv and identical before/after old-file hashes. This is fresh read-only verification, not a rebuild or retroactive promotion of fixture results.

Historical evidence stays visible: original T070 external verifier remains exit2 with preservation mismatch; original result/metadata remain LINKED_NOT_BROWSER_VERIFIED. Original D059 pins SHA024f1f3a4f7f7c8175521f25083c1314d29f6d2219266b8731e5a574d3c21211 and all published bytes are unchanged. New receipt is separate; no historical PASS was manufactured.

## Frozen identities

| Repository-relative file | SHA256 |
| --- | --- |
| web/build/verify_published_network.py | fce172c094dfcfa32c3951d8d8de4078e7be734ca43edb00c681e0accb619b43 |
| web/build/tests/t072/test_published.py | 66154f20ec3daa016e6ab20a62fec954580048ee6a67cf77206f439be9d9dec6 |
| web/build/generated/t072/fixture-tests-1.json | 5816a1b5aa2d2286e914282850bdb4552ea860ebf0802adc803f4bc834532d73 |
| web/build/generated/t072/code-freeze.json | f7fae7c49ea1a192370e70d23d8ed837e91c0aa33e9d72db163d64cb70730997 |
| web/build/generated/t072/actual-verification-1.json | c6ad3a59ef16f70690215811c36a8574b99f9050c2256e80401fd820fba331f5 |
| web/build/generated/t072/run-record.json | b0bc99e51559ff5115c377fd6e42b1c3d6ee8574d8d7269b41df634725f31e6d |

Original core SHA remains a5d5e9c81676a96365d34fff5bfadcaa249d3e894251ae8e10ae338fc3048b34. Original result SHA f0c5989000883d536dddc7697b4eded622fc481224d8be7ed08dd62ab583231f. Published hashes remain the exact T070 handoff table.

Inspection/test reproduction: `python3 -B -m unittest discover -s web/build/tests/t072 -p 'test_*.py' -v` (recorded execution additionally forbids subprocess boundary).

CLI interface takes ONLY exact absolute `--network-root`, `--attempt`, `--pins` and expected `--pins-sha256` for T070. It writes a NEW fixed generated/t072/actual-verification-1.json receipt and refuses an existing receipt. Already executed equivalent CLI scope:

```sh
python3 -B web/build/verify_published_network.py --network-root /Users/jd1/code/apps/outbreak/web/build/network-out --attempt /Users/jd1/code/apps/outbreak/web/build/generated/t066/attempt-T070-1 --pins /Users/jd1/code/apps/outbreak/notes/decisions/D059-network-build-pins.json --pins-sha256 024f1f3a4f7f7c8175521f25083c1314d29f6d2219266b8731e5a574d3c21211
```

Receipt immutability prevents silently rerunning that command over existing evidence. Actual browser join/spawn/remote movement/media/audio/models/pointer/performance/authority/P0/MVP remain NOT RUN/unverified. MAIN owns artifact/verifier acceptance and any later execution release.
