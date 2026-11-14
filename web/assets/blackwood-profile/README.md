# Blackwood assembly candidate data (T148)

Review-ready DATA_ONLY package under BLACKWOOD_ASSET_ASSEMBLY0.1/D176.
Acceptance and final freeze belong to MAIN; this is not runtime integration.

The fixed builder verifies the SHA-bound network-profile manifest (79 files)
and accepted T080/D078 Blackwood candidate manifest (5 files), then copies
exact bytes into 84 sorted entries under mount `/outbreak`. Both maps remain.
Only Blackwood's LICENSE.txt and PROVENANCE.json destination names change, to
`notices/blackwood-candidate/`; their source bytes and source_path stay intact.
All five Blackwood rows use that namespaced Blackwood license. The other 79
paths, licenses and notices are preserved. The root license covers new assembly
code/docs only. No stock assets or new textures, models or sounds are added.

Run from the repository root using Python 3 stdlib with bytecode disabled:

```sh
python3 -B web/assets/blackwood-profile/test_assembly.py
python3 -B web/assets/blackwood-profile/validate.py
```

The test harness generates absent final outputs using the fixed builder,
or validates an existing package; every test invocation retains its fixtures,
log, deterministic second-generation tree and before/after input identities in
a new `tests/attempt-ID/`. It compares all 86 generated package/metadata files
between the actual package and the reproduction. Source fixture tampering
affects only controlled test copies. Never interpret fixture corruptions as
candidate content. No fixture is deleted and no accepted input is written.

The direct fixed production builder is also available for an absent package:

```sh
python3 -B web/assets/blackwood-profile/assemble.py
```

It refuses any existing pack-root, manifest or provenance before output writes.
There are no CLI path/profile/command selectors or overwrite flags. Internal
test roots are confined to this profile's tests/attempt-ID descendants.
Imports have no filesystem or process effects. Inspect source before running;
no old once-only tools are imported or executed. No subprocess, network,
Node, compiler, browser, server, installer, Git or game/CFG execution occurs.

Validation requires canonical exact manifest/provenance schemas and source
mapping, all input and copied file hashes/bytes, ordinary0644/single-link files,
no alias/traversal/extra members or directories, every scoped notice, and the
three approved texture dependencies referenced by five Blackwood CFG lines.
CFG text is inspected, never evaluated. Provenance pins generator/validator
source fingerprints and relative accepted provenance references without
self-reference or absolute user paths. Manifest raw_bytes is a file-size sum;
transfer_measurement is NOT_OBSERVED. Candidate/runtime/gameplay flags remain
false as required; assembly_performed alone is true.

Blackwood geometry, CFG, lights, anchors and metadata are byte-for-byte copies.
Canonical 32 Q10 foot-origin squad alternatives remain distinct from the eight
integer native technical FFA starts. Sidecar points are alternatives, not
resource/actor grants. Extraction-distance asymmetry and all four accepted
limitations remain: CANDIDATE_NOT_BALANCE_ACCEPTED,
NO_RUNTIME_CAPSULE_NAV_OR_GAMEPLAY_PROOF,
LEGACY_STARTS_ARE_NOT_CANONICAL_SQUAD_SLOTS, NO_RESOURCE_OR_ACTOR_GRANTS.

No automatic Blackwood selection, startup/config change, media/profile overlay,
map boot, build or game integration is performed or authorized. Copied config
is historical data, not authority-mode boot permission. Native decode, renderer,
shared capsule/navigation, balance, gameplay, performance, transferred bytes,
P0 and human acceptance remain unproven and need separate releases/evidence.
