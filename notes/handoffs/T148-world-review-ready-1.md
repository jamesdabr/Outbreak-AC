# T148 World review-ready handoff

- Worker: World & Match Systems, chat 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket: T148 revision1.0, RELEASED D176; BLACKWOOD_ASSET_ASSEMBLY0.1 and BLACKWOOD_DATA_FOUNDATION0.1, governance/browser-foundation/P0 prerequisite0.5. Required governance/contracts and T080/D078 read; ticket and assembly contract re-read before submission.
- Status: REVIEW-READY, awaiting explicit MAIN clearance before final freeze. No authoritative acceptance or ticket edit.
- Base: current shared dirty repository; new web/assets/blackwood-profile root confirmed absent before work. No Git operation or existing source/profile edit.
- Changed files: only new blackwood-profile/{assemble.py,validate.py,test_assembly.py,README.md,LICENSE.txt,PROVENANCE.json,manifest.json}, pack-root/**, tests/attempt-50c1dbc7ec3a4623b365915470274520/** and this own handoff. Full new-root membership is in review-ready.json.

## Data result

PASS: exactly84 package files, 411990 raw file bytes, all ordinary0644/nlink1. Original79 network-profile entries preserve bytes, paths, licenses and notices; accepted Blackwood5 preserve bytes and source_path, with only LICENSE.txt and PROVENANCE.json destinations namespaced into notices/blackwood-candidate/. All5 Blackwood rows point at notices/blackwood-candidate/LICENSE.txt. No override or attribution collision. Both dev and Blackwood maps remain present; no automatic selection or configuration change.

Fixed input manifests, independently hash checked before parsing/copying:

| Source | Entries | SHA256 |
| --- | ---: | --- |
| web/assets/network-profile/manifest.json | 79 | c9ecfa62f7e4ca7111a9d3a23a9c97b906d11399d32f6f312463c6697a3359d7 |
| web/assets/blackwood-candidate/manifest.json | 5 | fa3049408e3ed0dbf2d4bc422b45c166b7fc0e0ac5d2fec4c8c5aadd53ae9711 |

Manifest schema1/profile BLACKWOOD_ASSET_ASSEMBLY_CANDIDATE_DATA, map blackwood_greybox_v1/revision1, mount /outbreak; exact9-field per-entry schema and pinned source mapping. raw_bytes is a sum, transfer_measurement NOT_OBSERVED. assembly_performed:true; existing_profiles_modified/runtime_verified/gameplay_verified/candidate_balance_accepted:false. Root provenance records generator/validator fingerprints, both manifests, all86 consumed file identities, explicit renaming and accepted provenance references using relative paths; no metadata self-reference or absolute user path. Root MIT license covers new code/docs only; copied assets retain scoped notices.

PASS: Blackwood CFG's five literal texture declarations resolve to three copied approved textures (ceiling.png, ground.png, wall.png). Text inspection only; no CubeScript execution. CGZ/CFG/anchors match accepted source byte-for-byte, including CGZ e68314e911130d2822fdfa65d77dfaba302d4f5c3552ff91c698b84768d5ddf1 and anchors159d3afe87123616e8346f6db00c2fd3a99325abbfa74a67b825bebfd89af05e. All four limitations preserved. Eight integer native technical FFA starts remain distinct from32 canonical Q10 foot-origin squad alternatives; no sidecar point becomes an actor/resource grant and extraction asymmetry is not relabeled balanced.

## Sources and bounded effects

New Python stdlib only; source inspected before execution. Main builder and validator have no CLI input/profile/path/command selector. Main assembly uses the two literal source manifests, checks source membership/bytes/hashes/notice closure and no-follow ordinary paths, refuses existing output slots before writes. Internal fixture/reproduction roots must be inside this profile's tests/attempt-ID descendants. Builder creates files exclusively and preserves original source bytes; no old builder/validator/test imports or executions.

New exact canonical manifest/provenance validation rejects unknown/missing fields and type/flag/mapping changes, not merely changed hashes. All copied bytes independently compare against the currently SHA-pinned source set. Pack traversal rejects aliases/specials, extra files and empty directories. Writes are confined to this profile's approved output slots or owned fixtures. Imports were additionally checked with a stdlib audit hook denying write/process/network mutation events: PASS, three modules imported, zero such effects.

No subprocess/Node/compiler/browser/server/network/install/Git, game boot/build/overlay, SDK changes, stock asset additions or source/profile mutation. Python -B avoided bytecode output. Pure stdlib command process61708 was polled to terminal exit0; no live owned child service or runtime.

## Reproducible verification

From /Users/jd1/code/apps/outbreak, Python3.11.9:

```sh
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/assets/blackwood-profile/test_assembly.py
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/assets/blackwood-profile/validate.py
```

Test command PASS, 10 meaningful groups, zero failures/errors, 2.269s logged. It generated the actual absent final package, then independently generated a second owned tree and compared all84 package files plus manifest/provenance, all86 bytestrings identical. Tests preserve all fixtures/logs/evidence rather than delete them. A later invocation validates final output and uses a fresh named attempt; it never overwrites the package.

Negative coverage: missing/tampered/extra file; extra empty directory; missing/extra/duplicate entry; traversal and normalized-path alias; destination notice collision; wrong notice/license/source hash/output hash/source path/virtual path/input pin; unexpected field/false runtime claim/bool-as-integer; duplicate JSON keys; file symlink/hardlink/permissions and parent alias; removed Blackwood or audio notice; removed texture/escaping CFG dependency; provenance fingerprint tamper; fixture-source manifest pin/bytes/notice/member/alias tampering; existing output and out-of-allowlist destination rejection. Source fixtures are copied first and validated against the real source mapping before tampering. Deliberate fixture links, a hardlink pair and altered modes are not package content.

Standalone final validator PASS:84 entries/411990bytes/three texture dependencies. Audit-hook import check PASS. No failed actual generation or test attempt occurred.

Evidence under web/assets/blackwood-profile/tests/attempt-50c1dbc7ec3a4623b365915470274520/:

- evidence.json: both complete before/after tables for86 accepted input files, including bytes/SHA/mode/nlink/device/inode/mtime_ns/ctime_ns. Tables equal; both source manifest and every pack member/notice unchanged. Generator fingerprints, test result and final data validation included.
- unittest.log: all10 group results.
- commands.json: exact generation/test/validator commands and recorded results, plus import audit check description/result.
- test_deterministic_reproduction-reproduction/: exact second-generation84-file package and two metadata files.
- review-ready.json: no-follow complete new-root graph, excludes only its named direct self-slot. 3185 ordinary file records,757 directory records,3 fixture symlinks; these counts exclude the inventory itself. No package links. This is review inventory, not final freeze.

Review-ready inventory:1184124bytes, SHA256 e6121c74aacd2113ff7eda9104ce42fcade74ad60cc50769926eca1916a0d0fe.

| Root file | Bytes | SHA256 |
| --- | ---: | --- |
| assemble.py | 1786 | 2a2e87702a276850b63404fde28ece0061cd7bf4a65df1d5bbb922f676d5c4b4 |
| validate.py | 11942 | ece160eff8eadabe2ccbdbcd25feffd0aa1b3494e70e56d25b839a62585f2612 |
| test_assembly.py | 11508 | bbaa9a7b17a6ac8ab49f5814d39a3c6259b47c6eb72f515cf2279578e68a9193 |
| README.md | 3685 | 8993f9219f6310876335b352d9956611f96bcdb56621b43b99549278150d0a69 |
| LICENSE.txt | 1306 | 3f69d516ff37101a31ae9265c1be920953c94065ed175c96ae646db84f6646b0 |
| manifest.json | 45719 | 8c4f7eef5f0deafb06bec60d62be529a684a30d56bbdc6dc3e5f38dd21c69e60 |
| PROVENANCE.json | 22897 | 48b1bbd659fa0193bce88a8d76a9146fa8e84bc981f20c4203c133e26b64b3c3 |

## Remaining gates

Implemented: data-only byte-preserving assembly, strict fixed-input validation, attribution/dependency closure and owned reproduction/negative tests. Simulated: corrupted test fixtures only, explicitly outside package. NOT RUN: native decode, map boot, renderer/shared capsule/navigation, balance/gameplay/performance, transferred-byte/startup/GPU measurements, authority-mode startup, builds or runtime integration. No fullP0/P2/P3/MVP/human acceptance claim.

No schema/input deviation or unresolved data question discovered. MAIN review/clearance is required before final freeze, and future consumption/build/runtime requires separate release. World stops package edits/tests here pending MAIN feedback. T143/T146/T147 remain disjoint; QA stays paused.
