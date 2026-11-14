# T112 actual browser build failure handoff

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket / revision: T1121.0; D116 immutable execution MD; D117 native acceptance/browser release.
- Contracts: CANDIDATE_BUILD_FOUNDATION0.2/D091; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5; PLATFORM_DECISION0.1.
- Source/root: b984954033c85161836542463e0250ca95baf713 / /private/tmp/outbreak-clean-D115-1.
- Common901-member manifest: fc812d21ca0796bccacd59938b7a7b2202f51e09abe870b0369988d386aeeb6f.
- Pins: clean-root notes/decisions/D116-candidate-build-pins.json; separately supplied expected SHA25654a7b93888aab0e5856ccc007a4ad8ca5666a1a4a28f78e7912b80e85d8b4b31.
- Writes: only new clean-root web/build/candidate-attempts/D116-web-1/**, reserved empty web/build/candidates/D116-web-1/ and absent parent containers, plus own original T112 question/handoff evidence. No source/config/metadata/SDK/cache/native/history/Git changes.

## Acceptance evidence

PASS — Read T112/D116/D117/pin review/contracts, inspected fixed entrypoints/recipe/helper commands and process/write boundaries. Before execution expected pins/common manifest matched, both browser destinations absent, and455 native graph records plus freeze/receipt matched MAIN-D117-native-build-review.json. Explicit reviewed assignment authorized this inspected clean-root operation; no additional execution inferred.

ACTUAL ATTEMPT FAILED — Exactly ONE command, from the required clean root:

```sh
env -u PYTHONPATH -u PYTHONHOME PYTHONNOUSERSITE=1 /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/build/build_candidate.py --execute --candidate-id D116-web-1 --pins /private/tmp/outbreak-clean-D115-1/notes/decisions/D116-candidate-build-pins.json --pins-sha256 54a7b93888aab0e5856ccc007a4ad8ca5666a1a4a28f78e7912b80e85d8b4b31
```

Original yielded session89195 polled through authoritative exit2; stderr `candidate build refused: noncanonical compiler dependency`. No observation timeout treated as completion, no retry or patch. failure.json is retained, SHA256cb91ecdce4f37ee0d0bf42392938526be0742dc6f9e054a08f3df807b100fbf7.

PARTIAL ACTUAL COMPILATION — Three fresh Wasm objects: crypto.cpp, audiomanager.cpp, autodownload.cpp. Their recorded pre/post dependency maps match. Fourth unit client.cpp completed pre-discovery but was not compiled: parse_dependencies rejected the raw `source/src/../../web/transport/enet_ws_bridge.h` token before later dependency checks. Exact clean-root include in client.cpp:8 and retained deps/03.pre.d (SHA25637ba195dbfaffada2fb3249a4d6318be593be25ac0c9e3f2d85843c9aa277421) explain the trigger. No compiler diagnostic failure or missing declaration is inferred.

PASS — All seven completed child records have exit0, failure null, owned_process_reaped true and <=120s. Elapsed milliseconds in order:208,475,128,306,125,196,126. Logs retained/hash-checked, all empty (SHA256e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855). No command timeout/log overflow observed. Failure stopped before client object/link/JS syntax/Wasm validation/payload publication. No process was relaunched for diagnosis.

PASS — Own stdlib post-failure read-only verification checked all26396 pinned input hashes;5976 protected file hashes;796 protected directories present; formerly absent roots except exact permitted output parents still absent; all901 source member size/mode/hash identities; unchanged pins/common manifest; exact original cache5956-file membership/hashes. No project imports or old verifier rerun. All455 native frozen records plus native freeze43af042e55b7886b2686c4457a1cd07d80df6b93f9f2e0362d0296645c702240 and receiptb4f370b8becd293ac839942b2bea635d98b1eedddc89c766e75aa4344edd08b2 remain unchanged. MAIN separately performs its required graph review.

PASS — Frozen failure snapshot created as own original-repository handoff evidence, not a builder success record:

- notes/handoffs/T112-world-failure-freeze.json:1413338bytes; SHA256**9b5d0e1678136a8366fed6f77a933c810e7b5493acdff169500137e64aa73515**.
- Full failed attempt inventory6764 records including root/directories/cache/threeobjects/sevendepfiles/sevenlogs/failure record; publication inventory contains only its reserved root. Two consecutive inventories equal.
- Original failed attempt has no result.json or freeze.json; none was fabricated. Publication has no runtime files or verification receipt. Retained evidence is not an accepted artifact manifest.

## Implementation status

Actual build attempt/three compiled objects only; intended61-unit linked candidate **incomplete**. Link/JS syntax/Wasm validation/exact79-file payload/12notice publication are **NOT RUN**, not failures invented beyond the observed gate. Success-only independent verifier **NOT RUN** because builder failed. Native actual build is previously MAIN-accepted and unchanged; it was not rerun or its preservation baseline rewritten.

Browser/audio/model/multiplayer/authority/runtime/performance/P0/MVP **NOT RUN/unaccepted**. No browser/server/binary/service/network/install/download/deployment launch, arbitrary flags/tool/env/profile, Git action, dispatch/selfacceptance, source or metadata edit. Player/QA holds unchanged.

## Integration and question

notes/questions/T112-world-noncanonical-dependency.md asks MAIN to release any narrow successor preparation/source correction separately. Current failure/raw dependency spellings/objects/cache/logs/publication reservation stay immutable. No automatic normalization, alias waiver, retry or pin regeneration. T112 ticket1.0 and D116/D117 authority rechecked before submission. MAIN reviews this failure observation and alone selects subsequent work.
