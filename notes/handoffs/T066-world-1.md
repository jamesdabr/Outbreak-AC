# T0664.0 frozen tooling preparation handoff

- Worker: World/Match-Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket reread before submission: T0664.0 RELEASED; D0544.0 under browser foundation/GOVERNANCE/P0 0.5; platform0.2/client0.3/main0.1. D055 subsequently accepted T061/T065 SOURCE components only; no execution expansion inferred.
- Base commit13f0d8eea4822dee5c976661218d022be74342e3; pre-existing shared changes preserved. No commits/push/reset/dispatch/status/contract edits.
- New: `web/build/profile_client.py`, network builder/verifier/config/shell, `tests/t066/test_profiles.py`, immutable `generated/t066/**`, this handoff. Authorized refactor only: audio builder/verifier and one fixture import in `tests/t060/test_tooling.py`. Audio-config, legacy drivers/config/shell, source/backend/SDK/cache/out/server/assets/old evidence unchanged.
- Frozen before handoff: `generated/t066/tooling-freeze.json` SHA256 `100f8e10f95c602afd46c5fe8193b3e4fef73849fdf2199722cc0a268c534a76`. No further implementation edits; later findings will be new questions first.

## Result

PASS PREPARATION. One shared `Recipe` implementation owns exact profile configuration, units, pack/tool/alias/preservation inventories, authority gate, future compile/link/publication and read-only bundle verification. Two explicit fixed builder/verifier wrappers bind audio or network; no module-global monkeypatch, arbitrary CLI config/profile/source/output/flag selection, second divergent build implementation or execution fallback.

Original audio tooling/tests/config were byte-snapshotted before refactor in `generated/t066/before/` with original hashes. Audio CLI options, config bytes, genuine53CPP+8ENetC including unix.c,79files388764B T053 pack, omissions, authority token/schema, t060 attempt root and audio-out target remain equivalent. Existing25 test bodies are unchanged; only fixture import now selects the wrapper's RECIPE object. Added regression independently compares all61 commands, exact link/JS syntax/Wasm validation commands, environment and omissions to accepted T060 attempt-plan-4; identical. Audio-config SHA315e6a8d0904c2927011652fbaaf12192c539915c90d992576eae290a578b0f6 unchanged. Old T060 reports/handoffs remain historical identities; new code uses the shared-core hash and requires fresh future MAIN complete pins.

Network recipe plans exactly53 genuine CLIENT_OBJS CPP +7 existing ENet core C +accepted enet_websocket.c,61 unique units, no unix.c. Every CPP adds only -DOUTBREAK_NETWORK_CLIENT; every C retains target/O2/HAS_SOCKLEN_T and adds exactly -std=gnu11/-fsigned-char/-DOUTBREAK_NETWORK_CLIENT; all include web/transport. Link adds only accepted enet_websocket.js via --js-library. SDK7.0.0/compiler777e6e5..., Node24.19.0, six archive/recipe hashes, safeGL,64MiB initial/2MiB stack/growth remain exact. Missing/both/duplicate socket implementations, missing JS library, changed flags/profile/output fail before execution.

Actual accepted network pack c9ecfa62f7e4ca7111a9d3a23a9c97b906d11399d32f6f312463c6697a3359d7 validates through exact hash-checked inspected T064 helpers:79files388791B, revision2/eight FFA anchors,78 copies, unchanged lights/geometry/notices and complete derived provenance. Accepted T058 C/JS/bridge/browsernet.h hashes are required; complete helper/source/header/tool inventory is pinned, including T064's original parser dependency. Network shell is byte-exact T056 except one title replacement to “network scene and join proof”; no injected boot/secret/query/input flow or false join-ready state. Supervisor remains immutable-boot owner.

Network prospective metadata has explicit NETWORK_CLIENT profile and truthful omissions: native join/spawn/two-client runtime pending, legacy client-reported movement/hits are not Outbreak authority/P0/MVP, actual proof-audio/model rendering pending. It does not describe network gameplay as an embedded offline simulation. Both profiles use fresh real61 objects only, exact future command/exit/log/object/output hashes, actual79 preload slices, JS syntax/Wasm validation, notices/metadata/source-output checks and publish only after validation to absent target; no object/link success is simulated. Current actual builds remain NOT RUN.

## Tests, observations and preservation

PASS34 stdlib tests under subprocess-forbidding guard: original25 plus network variants and audio-plan equivalence. Network negative groups exercise real map2 bytes/derivation, actual79 fixture slices, output corruption, current-source change, missing/extra inventory, alias change, audio/network authority/profile/attempt mixing, missing library/unsafe flags/other outputs and duplicate/missing/unix+backend sources. Fixtures use temporary fake repository/decision roots; they are not accepted pins, objects or linked game artifacts. Exact stdout/command count: `generated/t066/test-results-1.json`, SHA0fa1e066ff0d3348ca8b4b31a9b6d37302e81d6becbee5bac4c39ea148fe7255.

PASS syntax/import and full read-only observations/plans, zero SDK/compiler/Node/version/link/package/browser/server/network subprocesses:

- Network `generated/t066/attempt-plan-1/plan.json`:23474 observed inputs,61 commands,79-file validated pack, five exact D044/D046 aliases/supporting identities, `tool_errors:[]`. SHA67f694ffc8a546f591c8349a015951e327317519763cbfd215bce3ff00bb3989.
- Audio `generated/t066/audio-plan-1.json`:23380 observed inputs, same complete tool closure/no errors, unchanged audio commands/pack. SHA f82df88cc76226920bb91adc190ec747a61751c65d5ee0374501ec2ba24d543d. This observation was written under T066; no new t060 attempt/artifact was created.
- Both label NOT_EXECUTED, accepted_source_pins false, execution_ready false. The retained pending-source flag describes the unapproved complete build input inventory, not a denial of D055's individual T061/T065 source acceptance. Neither observation grants MAIN pins or execution release.
- `generated/t066/preparation-check-1.json`: identical before/after6073 protected native/offline/cache products and401 static accepted pack/helper/old-evidence/legacy files; audio-out/network-out absent. SHA7f1385cab9790811790731169574237444f082cc9f0d2e71892bb33c38039525.

Current inventory remains deliberately conservative/broad (including source/header fixture arrivals); MAIN must freeze the complete current closure before actual execution. Snapshot/preservation also covers either profile's output if it exists in a later separately released run. No original source/pack/backend/SDK/cache mutation or active overlay occurred.

Reproduce tests after inspection, with subprocesses forbidden as in recorded guarded run:

```sh
python3 -B -m unittest discover -s web/build/tests/t060 -p 'test_*.py' -v
python3 -B -m unittest discover -s web/build/tests/t066 -p 'test_*.py' -v
```

Read-only network planning via CLI requires a NEW owned attempt name: `python3 -B web/build/build_network_client.py --plan-only --attempt web/build/generated/t066/attempt-NEW`. Existing attempt history is refused. No actual compile/version/runtime command has run under T066.

## Future MAIN pins / both interfaces

No accepted pins document was created. Future execution requires an absolute MAIN-owned `notes/decisions/*.json` path plus independently expected document SHA256, exact current inventory, separate explicit release and new absent attempt/output target. Ownership/approval is MAIN/operator responsibility; self-declared JSON or a dry plan is not authority.

Audio preserves exactly T0603.2 schema: keys `schema`1, `authority`MAIN, `status`ACCEPTED, `ticket`"T060 revision 3.2", `execution_release`EXPLICIT_AUDIO_BUILD_EXECUTION, `attempt`, `inputs`, `preservation`, `units`, `ports`, `aliases`, `alias_decisions`. Root generated/t060, target audio-out. Network requires those exact keys PLUS `profile`"NETWORK_CLIENT original-network-media", with `ticket`"T066 revision4.0", `execution_release`EXPLICIT_NETWORK_BUILD_EXECUTION, generated/t066 attempt and network-out. Cross-profile docs/attempts/configs are rejected.

`inputs` and `preservation` are complete absolute regular path->SHA256 maps with exact membership, not subsets. Units are ordered61; ports carry six exact archive path/SHA256/SHA512 and recipe path/SHA256 records. Aliases and alias_decisions retain exact five D044/D046 logical chains/roots/text/target hashes/supporting identities and both decision JSON SHAs. The core/selected wrappers/configs/shells, backend C/JS/headers, pack/provenance/helper closure and actual tool libraries/scripts are explicit inputs. Stable input/preservation checks run before artifact/compiler mutation, after cache copy/compile/link and before publication. No reuse; original frozen cache is copied into new attempt; all temp/node/cache paths and clean environment recorded, no acquisition fallback.

Future commands below are NOT RUN and require a separately accepted MAIN pin document/release (replace placeholders):

```sh
python3 -B web/build/build_network_client.py --execute --attempt web/build/generated/t066/attempt-MAIN --pins /Users/jd1/code/apps/outbreak/notes/decisions/MAIN-NETWORK-PINS.json --pins-sha256 MAIN_EXPECTED_SHA256
python3 -B web/build/verify_network_bundle.py --network-root /Users/jd1/code/apps/outbreak/web/build/network-out --attempt /Users/jd1/code/apps/outbreak/web/build/generated/t066/attempt-MAIN --pins /Users/jd1/code/apps/outbreak/notes/decisions/MAIN-NETWORK-PINS.json --pins-sha256 MAIN_EXPECTED_SHA256
python3 -B web/build/build_audio_client.py --execute --attempt web/build/generated/t060/attempt-MAIN --pins /Users/jd1/code/apps/outbreak/notes/decisions/MAIN-AUDIO-PINS.json --pins-sha256 MAIN_EXPECTED_SHA256
python3 -B web/build/verify_audio_bundle.py --audio-root /Users/jd1/code/apps/outbreak/web/build/audio-out --attempt /Users/jd1/code/apps/outbreak/web/build/generated/t060/attempt-MAIN --pins /Users/jd1/code/apps/outbreak/notes/decisions/MAIN-AUDIO-PINS.json --pins-sha256 MAIN_EXPECTED_SHA256
```

Actual full audio/network link, verifier on real new bundles, browser/native-c2 game runs, remote movement/spawn, model/audio/pointer/media/performance/authority/P0/MVP remain NOT RUN. No unresolved implementation scope question; MAIN owns review and later execution.

## Frozen code identities

| Repository-relative file | SHA256 |
| --- | --- |
| web/build/profile_client.py | a5d5e9c81676a96365d34fff5bfadcaa249d3e894251ae8e10ae338fc3048b34 |
| web/build/build_audio_client.py | 6d9f57b802b62d41fa8438e7a5e81000ccec7ecc33dc450844ee4cb713aa6058 |
| web/build/verify_audio_bundle.py | b275c290950179882bea1230e082e3ecc2c3c543dead617aff968715263393a7 |
| web/build/build_network_client.py | 4f38cb59324ecad89aa8f3daeb9e25e5aa2ca3bc952d7557940b4bd4057110c0 |
| web/build/verify_network_bundle.py | e5f67bce041eebd4d7e82a19c9a11881f7280ebd959337175d01485b580e3d49 |
| web/build/network-config.json | 8b812996585a268aa79acfc113bdd392af3b87b45486fb92fa3b9882b4dc62ba |
| web/build/network-shell.html | 6fccbeb1094a4f09998db25b123d2b9287b75da013f80d6e72a0444efa751399 |
| web/build/tests/t060/test_tooling.py | 3bf7421f18fbabe6f827b70820f663eae873b8861ca1e814c281e232ed235829 |
| web/build/tests/t066/test_profiles.py | 16bfcfe04c600c6b79b98e7bd77734d513cb27471e1fc4acae482729be3709d5 |
