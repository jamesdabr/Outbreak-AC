# T111 actual native release/debug build and independent verification

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T1111.0 RELEASED / immutable D116. Submitted for MAIN artifact review; no authoritative status/self-acceptance.
- Governing: native0.4/D111 and accepted private schemas; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5 actual build prerequisite only. Ticket/D116/native/governance/README, MAIN-D115 clean/source/cache receipts and MAIN-D116 pin review inspected before execution; ticket/native markers re-read before submission.
- Root/source: /private/tmp/outbreak-clean-D115-1 / b984954033c85161836542463e0250ca95baf713. Same reviewed source, fresh root/objects; all prior roots/D110/D114 artifacts/pins/manifests immutable.
- Writes: only absent candidate-attempts parent and NEW D116-native-1/** including exact optional verification/receipt.json; this own original-repo handoff. No source/schema/flags/pins/manifest/SDK/original framework/cache/other artifacts/Git mutation, extra root logs, archive copying, installs or dispatch.
- Outcome: **ONE actual builder exit0 / NATIVE_LINKED_NOT_RUN; ONE independent verifier exit0 / VERIFIED_BUILD_ONLY_NOT_RUN. Neither resulting binary executed.**

## Exact execution and authority

Pre-effect read-only checks matched fixed Python3.11.9, reviewed stage/build/verify file hashes, absent parent/attempt, exact pins digest and common manifest. No plan/observation/pin regeneration. MAIN-D115 receipts establish900 ordinary sources/seven framework links and6738 staged-cache members; MAIN pure authorization supplied2197 inputs/1196 SDK files/96 framework members/901 source entries. The exact observed compiler-runtime archive is declared by D116; no source/flag correction or old object reuse.

Executed exactly once each from /private/tmp/outbreak-clean-D115-1:

```text
env -u PYTHONPATH -u PYTHONHOME PYTHONNOUSERSITE=1 /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/server/candidate/build.py --execute --candidate-id D116-native-1 --pins /private/tmp/outbreak-clean-D115-1/notes/decisions/D116-candidate-native-pins.json --pins-sha256 876614d924782d5833fa33aaa30d853bad7eab1ca65ec0ed4f5a259fc61968ab
env -u PYTHONPATH -u PYTHONHOME PYTHONNOUSERSITE=1 /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B web/server/candidate/verify.py --candidate-id D116-native-1 --pins /private/tmp/outbreak-clean-D115-1/notes/decisions/D116-candidate-native-pins.json --pins-sha256 876614d924782d5833fa33aaa30d853bad7eab1ca65ec0ed4f5a259fc61968ab --receipt /private/tmp/outbreak-clean-D115-1/web/server/candidate-attempts/D116-native-1/verification/receipt.json
```

Builder session66762 and verifier session81268 were polled to authoritative exit0, never restarted on yield. Verifier began only after builder terminal success. Ambient PYTHONPATH/PYTHONHOME/user-site disabled; child Runner environment fixed as reviewed. No alternative launcher/root/flags/selector or source/library substitution.

## Acceptance evidence

| Criterion | Actual result |
| --- | --- |
| Current authority/source/SDK/tool admission | PASS existing digest/root/HEAD/901-source-manifest/current ordinary input/alias/preservation gates. Both fixed compiler launchers reported required installed Apple17/arm64/CLT identity; no old sound/MD3/header hash waiver. |
| Fresh copied framework/signatures | PASS physical source inventory/copy/no-hardlink checks; nested hidapi then parent SDL2 copied-framework ad-hoc signing, four signature checks and two full library inspections. Source framework/original SDK/libraries unchanged per before/final gates. |
|32 genuine native objects | PASS exactly16 release plus16 debug, each with fresh -M discovery, actual compile/-MD, file/Mach-O and hash checks; no PCH/object reuse. Raw .pre.d/.d/logs retained.892 unique current compiler-dependency paths across modes, independently rechecked in verifier. Both exact SDK aliases validate before effects and when consumed; unknown aliases remain forbidden. |
| Two actual links / exact linker inputs | PASS release/debug link processes and link inventories. Each has59 canonical recorded link input files, including16 own fresh objects, owned signed framework, declared SDK inputs and exact CLT compiler-runtime archive. Each trace reports281 archive-member names; these are trace records, not a claim every member's code enters the binary. Every used canonical file bound to current declared hash. |
| Actual binary inspections | PASS structural arm64 Mach-O/signature bounds, fixed file/otool/codesign checks, allowed dynamic dependencies/ad-hoc identity and exact two absolute candidate RPATHs. No original-framework RPATH or relocation/notarization/bit-reproducibility claim. |
| Command/log/time/process bounds | PASS126 ordered actual builder command records:32 discoveries,32 compiles,two links plus identity/signature/inspection steps. All exit0/group_reaped=true; timeout/overflow/kill_fallback allfalse. Max command1303.302ms; runner-recorded elapsed69257.999ms, below1800s.146563 total stdout/stderr bytes; full bounded logs retained. These are execution-bound receipts, not hardware/game performance metrics. |
| Original and new terminal preservation | PASS builder full final and independent verifier gates for current original/source/SDK/preservation graph.455 terminal file/directory/link members frozen, excluding freeze itself and separately named optional receipt. Own read-only final check independently matched exact membership, modes/bytes/hashes/raw links and all32 object/pre/post dependency-file identities after verification. |
| Independent fixed verifier/new receipt | PASS one actual read-only verifier run, independently reconstructing command ordering, actual object/dependency/link/binary/protection/freeze checks and rerunning fixed file/otool/codesign inspectors only. Exclusive exact verification/receipt.json created; report/freeze unchanged. |
| Current identity after completion | PASS pins876614d924782d5833fa33aaa30d853bad7eab1ca65ec0ed4f5a259fc61968ab and common manifestfc812d21ca0796bccacd59938b7a7b2202f51e09abe870b0369988d386aeeb6f still match. No metadata rewrite or accepted-native manifest authored by worker. |
| Native/server/browser/runtime/authority/P0/MVP | NOT RUN / not accepted by this delivery. No binary/game/server/gateway/browser/socket/network execution, publication, performance/humanmedia or gameplay test. All corresponding recorded claims remain false. |

This is genuine installed native compilation/signing/link/inspection evidence from a fresh reviewed-source checkout, not fixture objects or copied old binaries. Independent build verification does not itself constitute MAIN artifact acceptance or runtime success.

## Artifact and evidence identities

All artifacts under /private/tmp/outbreak-clean-D115-1/web/server/candidate-attempts/D116-native-1/:

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| release/ac_server | 581640 | 3d0e1d3cb9dfbe121a3a50ff3ac6b3b3d36cb0500f8c5223aecde69624563de4 |
| debug/ac_server | 901736 | 03e200cf20df4c1a571a5b9083f0f8003a1b8cd126bcb4811986642a7e661e87 |

- report.json SHA256e91d6b267ee34210fb90304176dd081796bf5c09563a3994217839297c160779; status NATIVE_LINKED_NOT_RUN, errors empty, object_reuse=false.
- freeze.json SHA25643af042e55b7886b2686c4457a1cd07d80df6b93f9f2e0362d0296645c702240;455 terminal members.
- verification/receipt.json SHA256b4f370b8becd293ac839942b2bea635d98b1eedddc89c766e75aa4344edd08b2; status VERIFIED_BUILD_ONLY_NOT_RUN, both binary/report/freeze/pins identities exact, all claims false.

Exact argv/environments/exit/log hashes, source/SDK/actual dependency graphs, pre/post .d, object/link/signature/Mach-O/RPATH evidence and complete before/terminal inventory are retained in those records. Verifier stdout/receipt reported the same binary hashes. No output from either binary exists because neither was launched.

## Integration and limitations

No unresolved failure/question for the assigned actual build/independent verification. Historical T105/T109 failed graphs and all prior source/preparation receipts stay immutable; this new success does not relabel those failures or change their source/pin identities. D116 artifacts remain bound to this canonical root and exact source/pins.

MAIN reviews complete actual artifact graph before native admission and any separately released browser role. Browser must remain serial and use its own exact authority; MAIN's later preservation comparison is separate from this native verifier's frozen baseline. This handoff dispatches/releases no next work and accepts no runtime or full P0/MVP gate. Preserve all completed evidence unchanged.
