# T116 actual browser candidate build and verification handoff

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket / revision: T1161.0; immutable D121 execution MD and D122 native acceptance/browser release.
- Contracts: CANDIDATE_BUILD_FOUNDATION0.2/D091; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5; PLATFORM_DECISION0.1.
- Source/root: bdaa8df7ec39d9408f97feda4560832d7ef26c3c / /private/tmp/outbreak-clean-D120-1.
- Same common901-entry source manifest: SHA2562583d893deac6c45fd6607aa7e40447a0f3d01e0410482bcc9f4a03810ddd5bc.
- Browser pins: clean-root notes/decisions/D121-candidate-build-pins.json; separately supplied expected SHA25601b7ad7a683b8d88a3a12b892e7eec2b1712c21ca1b75d90fac3b50438554e1b.
- Writes: NEW clean-root web/build/candidate-attempts/D121-web-1/**, web/build/candidates/D121-web-1/**, absent exact parent containers and this own original handoff. No source/config/flags/pins/manifest/SDK/original cache/native/history/Git changes.

## Acceptance evidence

PASS — Read T116/D121/D122 and MAIN-D121-browser-pin-review.json, with actual native acceptance recorded before browser execution. Expected pins/common manifest matched, both browser destinations absent. Fixed builder/verifier/recipe/helper bytes match the previously inspected D116 versions; no source overlay/command selection or gate relaxation. Before browser, all455 D121-native frozen members plus its exact freeze/receipt matched. MAIN pure observation previously passed26396inputs/61units/sixports/fivealiases; actual builder independently required current equality before effects and every compiler boundary.

PASS — Exactly ONE fixed actual command, from /private/tmp/outbreak-clean-D120-1:

```sh
env -u PYTHONPATH -u PYTHONHOME PYTHONNOUSERSITE=1 /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/build/build_candidate.py --execute --candidate-id D121-web-1 --pins /private/tmp/outbreak-clean-D120-1/notes/decisions/D121-candidate-build-pins.json --pins-sha256 01b7ad7a683b8d88a3a12b892e7eec2b1712c21ca1b75d90fac3b50438554e1b
```

Yielded session59098 polled through authoritative exit0; result **LINKED_NOT_BROWSER_VERIFIED**. Actual terminal freeze elapsed1383908ms, below3600000ms. No observation timeout treated as completion, retry/source/pin patch or old object reuse. Prior failed D116-web-1 remains unchanged.

PASS —61fresh units and61fresh Wasm object identities; object_reuse=false, fixture_only=false. Actual61 pre-scan/61 compile records all retain exact fixed argv/environment and matching pre/post dependency maps;325 unique consumed dependency paths checked against current declared hashes (task-owned cache paths mapped back to original declared cache). Approved five SDK aliases and six frozen ports checked without arbitrary symlink permission. Physical task-owned cache copied/compared before compilation; original SDK/cache/source/preservation bytes and membership checked through final boundary and verifier.

PASS —125 actual child commands:61dependency pre-scans,61compiles, one link, one Node JS syntax check, one Node WebAssembly.validate check. All exit0, failure null, owned_process_reaped=true; maximum command2361ms, below120000ms; logs bounded/retained/hash-checked. Fixed original network backend/flags, legacy GL safety,64MiB initial memory and2MiB stack retained. No game/browser/native binary executed by these build/format validation commands.

PASS —79-file388791-byte approved payload validated as exact nonoverlapping index.data slices, plus12notice byte identities in retained bundle and publication. Four runtime files and build-metadata.json plus12notices yield exact17 publication files and2 directories (notices,verification), before optional receipt exclusion. Retained bundle/publication runtime hashes match. Runtime map/media decoding remains NOT RUN; packing proof is not rendering/audio/model/gameplay proof.

PASS — After genuine builder success exactly ONE independent verifier, same cwd/env/Python:

```sh
env -u PYTHONPATH -u PYTHONHOME PYTHONNOUSERSITE=1 /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/build/verify_candidate.py --candidate-id D121-web-1 --pins /private/tmp/outbreak-clean-D120-1/notes/decisions/D121-candidate-build-pins.json --pins-sha256 01b7ad7a683b8d88a3a12b892e7eec2b1712c21ca1b75d90fac3b50438554e1b --receipt /private/tmp/outbreak-clean-D120-1/web/build/candidates/D121-web-1/verification/receipt.json
```

Yielded session27176 polled to authoritative exit0; **VERIFIED_LINKED_NOT_BROWSER_VERIFIED**. Receipt exclusively created at exact authorized path. Independent verifier checked actual source/tool/pins/result/commands/objects/dependencies/aliases/ports/payload/metadata/notices/protection and exact original+new membership. No second verifier, compiler rerun, runtime or accepted-artifact manifest creation.

PASS — Final own stdlib read-only walk with error-raising enumeration independently matched every browser frozen file hash/size/mode and exact directory/file membership: attempt6507files/791directories, publication17files/2directories (literal exclusions only freeze.json and verification/receipt.json respectively). Receipt binds exact result/freeze identities. All455 native frozen members matched by kind/mode/size/hash/raw link, with native freeze34b6a769592cf514822f46fe1345d0d1bcd43fd6301b75e19f861e5234ecce6d and receipt44dc9c5095a3be81d680fd327397898027fe57d359ae09d0f9ba383c21db35fd unchanged. No native verifier rerun or baseline rewrite after browser output. MAIN separately performs its required graph review. Common source manifest/browser pins remain exact.

## Frozen artifact identities

Attempt base: /private/tmp/outbreak-clean-D120-1/web/build/candidate-attempts/D121-web-1/. Publication base: /private/tmp/outbreak-clean-D120-1/web/build/candidates/D121-web-1/.

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| attempt/result.json | 10047966 | 8ec2b1617cf71b1b642ab83e077cae92d13a72cab0d5ff50bbb078963c7030bd |
| attempt/freeze.json | 1396803 | 7811d17f69c39c47b03976899ceb95cd1d2b484c4889ae8de0f82cffda25906d |
| publication/verification/receipt.json | 1113 | c01b71a3dedbfce56c596b6a960eaa819d565cab7ebfc7e09d92bdc9715e6728 |
| publication/build-metadata.json | 10047877 | b8ad9731e131601bbce23ae94dbbab66b4cb7a981525219d702ca8a514a732d8 |
| publication/index.html | 1837 | 23f2ee9f9a86f7877ba9125d5fb9b79d94426c00e7692d0de74da022bf2b1775 |
| publication/index.js | 355708 | 762d30d215f982d084f2e2f7d9431955ba135ab6b038bae4d9c09c990a0c5a51 |
| publication/index.wasm | 1678699 | 5b0d2ee25b1e895dcdabc39d023fb0891c0a7887025400e165e146de3db101af |
| publication/index.data | 388791 | dcc9b311beae85a4c20945ca55e94c914b16b1694c00870b36d52a8afb4a78a8 |

Bundle ID: **1e12a233072374531554ebb5309e307064df7f8b3588c72714abd82e77bf9e66**. Full raw61-unit/125-command/dependency/log/payload/notice/environment records are in immutable result.json; complete owned graph in freeze.json; independent receipt binds both. These are actual build records, not fixtures or simulated execution.

## Implementation status and integration

Actual clean-root fixed network_v1 browser compilation/link/JS syntax/Wasm validation/payload publication and independent linked-artifact verification complete, sharing the exact common source revision/manifest with accepted native candidate. **NOT RUN**: browser load/render/navigation/input/audio/model decoding, native binary/server/gateway/network/game runtime, multiplayer/authority/performance/P0/MVP. All runtime/audio/model/multiplayer/authority/P0 claims false in metadata/receipt; linked verification does not accept these gates.

No public publication/service/network/browser/server/native binary/runtime/install/download launch; only local owned artifact publication. No source/tool/flag/config/pin/cache/SDK/native/history/Git/status/contract/dispatch/selfacceptance changes. Player/QA holds unchanged. No unresolved T116 question. MAIN reviews/accepts this evidence and alone releases any downstream admission/runtime work. T1161.0/D121/D122 re-read before submission; no rerun into frozen output or native baseline rewrite authorized.
