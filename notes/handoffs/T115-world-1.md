# T115 actual native candidate build and verification handoff

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket / revision: T1151.0 / D120 / immutable clean-root D121 execution authority.
- Contracts: CANDIDATE_NATIVE_FOUNDATION0.4, CANDIDATE_BUILD_FOUNDATION0.2/D091; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5.
- Source/root: bdaa8df7ec39d9408f97feda4560832d7ef26c3c / /private/tmp/outbreak-clean-D120-1.
- Common manifest:901entries; SHA2562583d893deac6c45fd6607aa7e40447a0f3d01e0410482bcc9f4a03810ddd5bc.
- Pins: clean-root notes/decisions/D121-candidate-native-pins.json; separately supplied expected SHA25632e5b59380018be22a085ededb1bdcee83c3bdc283292351a35a22a64fd5b23d.
- Writes: only NEW clean-root web/server/candidate-attempts/D121-native-1/**, absent parent container, and this own original handoff. No source/config/SDK/cache/original framework/metadata/pins/old evidence/Git edits or commit. Shared original edits preserved.

## Acceptance evidence

PASS — Read T115, D120, immutable D121, MAIN-D120 source/cache receipts and MAIN-D121-native-pin-review.json; inspected fixed build.py/stage.py/verify.py execution, command/write/process boundaries. Expected pins/common-manifest hashes matched,901 entries present, exact native destination absent. MAIN prior receipt reports900source/sevenlinks/6738cache members; pure native pins predeclare2197inputs/1196SDKfiles/901source entries. No staging/observation/plan/compiler rerun was introduced before the actual command.

PASS — Exactly ONE actual builder command from /private/tmp/outbreak-clean-D120-1:

```sh
env -u PYTHONPATH -u PYTHONHOME PYTHONNOUSERSITE=1 /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/server/candidate/build.py --execute --candidate-id D121-native-1 --pins /private/tmp/outbreak-clean-D120-1/notes/decisions/D121-candidate-native-pins.json --pins-sha256 32e5b59380018be22a085ededb1bdcee83c3bdc283292351a35a22a64fd5b23d
```

Yielded session99407 polled to authoritative exit0; result **NATIVE_LINKED_NOT_RUN**, errors[]. Actual recorded builder elapsed71969.973542ms. No observation timeout treated as completion, retry or patch.

PASS — Fresh32objects,16release/16debug, exact8CPP+8ENet units per mode, two real ac_server links, object_reuse=false. Recorded pre/post -M/-MD dependency equality/current declared-byte checks passed for every unit. Release consumed789 unique dependency paths; debug892. Each link trace contains59 ordinary input identities with archive-member records, own16objects and signed-copy SDL2; all current declared membership/hash guards passed, including the predeclared exact CLT runtime archive. Both fixed pthread.h/sched.h alias identities/targets checked before effects and when consumed; no generic alias permission/raw-byte exception.

PASS — Actual fixed /usr/bin/clang and clang++ identities: Apple clang17.0.0 (clang-1700.0.13.5), Target arm64-apple-darwin25.5.0, InstalledDir /Library/Developer/CommandLineTools/usr/bin. SDKSettings Version15.5 checked against fixed canonical MacOSX15.5.sdk. This is the native arm64 development build on the selected host; no runtime/performance measurements inferred.

PASS — Physical task-owned SDL2 framework copy verified against original96-member inventory without hardlinks; only copied nested hidapi then copied parent SDL2 ad-hoc signed. Four copy signature checks and two framework/final two binary file/dependency/load-command/signature/ad-hoc inspections passed. Both binaries contain exact owned deps-signed and nested-framework RPATHs with no old/original source RPATH leakage. Original framework unchanged under preservation checks.

PASS —126 recorded builder child commands:2compiler identities,2copied-framework signing,4copy-signature checks,20framework/binary inspection commands,32dependency discovery,32compilation,32object-file checks and2links. Every exit0, group_reaped=true, timed_out/overflow/kill_fallback=false. Maximum command1314.216834ms, below120s; whole attempt below1800s. Stdout/stderr logs/argv/environment/dependencies/signatures retained in report/freeze; verifier checked ordered exact commands and bounded log identities. No resulting binary executed.

PASS — After genuine builder success, exactly ONE independent verifier, same clean-root cwd/environment/Python:

```sh
env -u PYTHONPATH -u PYTHONHOME PYTHONNOUSERSITE=1 /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/server/candidate/verify.py --candidate-id D121-native-1 --pins /private/tmp/outbreak-clean-D120-1/notes/decisions/D121-candidate-native-pins.json --pins-sha256 32e5b59380018be22a085ededb1bdcee83c3bdc283292351a35a22a64fd5b23d --receipt /private/tmp/outbreak-clean-D120-1/web/server/candidate-attempts/D121-native-1/verification/receipt.json
```

Yielded session51308 polled to authoritative exit0, **VERIFIED_BUILD_ONLY_NOT_RUN**. Independent logic checked all unit/object/command/log/dependency/link/SDK/staged-framework/signature/RPATH/current-source/pins/preservation identities, re-ran only fixed read-only inspectors and exclusively created the exact receipt. No compiler/signing/server launch in verifier. Final own stdlib read-only check independently matched all455 frozen members by kind/mode/size/hash or raw link, plus report/freeze identities against receipt; no second verifier invocation.

## Frozen evidence

All paths below relative to clean-root web/server/candidate-attempts/D121-native-1/:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| report.json | 11477550 | 18f2ba91e99e70d04153b231d6fa9e0a946ca58ab5b46c79fe1322b188dc0337 |
| freeze.json | 63675 | 34b6a769592cf514822f46fe1345d0d1bcd43fd6301b75e19f861e5234ecce6d |
| verification/receipt.json | 874 | 44dc9c5095a3be81d680fd327397898027fe57d359ae09d0f9ba383c21db35fd |
| release/ac_server | — | c9ae0800ac1fc2d315ed4c4205590390049a307e6d14098009e2d53a5b87d094 |
| debug/ac_server | — | dc9ed65479df914ee7ad5ab8fa8ca985bcb1b8435849d6e7b13d13d4ae4ea4c5 |

Freeze includes455members, excluding only its own file and exact optional receipt. Report has complete raw command/log references,32object and64dependency paths/hashes, two59-input link maps and all inspection references. Source/SDK/cache/original frameworks/preservation checked unchanged through builder final guard and independent verifier. All prior D116/T112 graphs remain outside the new write root and untouched; no old baseline rewrite.

## Implementation status and integration

Actual native compilation/signing/link/read-only inspection and independent verification complete for this exact developer root/source. Runtime/native binary/server/browser/gateway/game/network, gameplay/authority/multiplayer/performance/P0/MVP **NOT RUN/unaccepted**. Claims remain false in builder/freeze/receipt. No download/install/global change/arbitrary flags/plugin/profile/Git/dispatch/status/contract edit/selfacceptance. No copied old objects or binaries.

MAIN reviews this handoff and alone accepts the artifact pair or releases T116 browser work serially against the same common source manifest. T116 remains nonexecutable here; Player/QA holds unchanged. No unresolved T115 question. Reproduction is evidence review/current-byte checks only: do not rerun into this frozen destination or rewrite its preservation baseline. Any new attempt requires a new release/ID. T1151.0 and native0.4/D121 authority re-read before submission.
