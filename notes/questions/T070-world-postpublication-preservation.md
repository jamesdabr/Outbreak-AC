# T070 external verifier rejects its own new publication

- Author: World/Match-Systems.
- Ticket: T0704.2 RELEASED, D059 exact one-build release; T0664.0 frozen tooling.
- Governance: browser foundation/GOVERNANCE/P0 0.5; no source/tooling/flag changes or second build authorized.
- Affected clause: required post-publication frozen verifier against MAIN D059 complete pins.
- Status: OPEN; MAIN resolution must be recorded separately.

## Observed failure

One exact authorized build attempt-T070-1 completed exit0 and published network-out. All61 real fresh compiles PASS, link/JS syntax/Wasm validation exit0, actual79 preload slices/notices/metadata/attempt-bundle validation passed before publication. The separately required exact frozen verifier then exited2: `T066 verification refused: missing/extra/changed preservation`. No second build, verifier retry, source/tooling/flag/pin/output edit, runtime launch or cleanup has occurred.

Read-only comparison confirms all23474 current input hashes exactly match D059. All6073 pre-existing preservation entries remain present and byte-identical; removed=[], changed=[]. Current preservation has6090 entries: the only17 additions are the builder's new network-out four artifacts, metadata and12 notices. SDK57 Python bytecode files also remain byte-identical.

## Cause and impact

The shared Recipe.preservation() includes audio-out and network-out. D059 correctly pinned an absent network-out baseline. Builder's attempt-bundle verifier runs before publication and sees6073, then publishes. External verifier calls observe()/authorize() again; its preservation map now includes its own new publication and differs from the pre-build pins. This is a tooling defect, not a protected-file mutation. Original builder result/metadata truthfully retain LINKED_NOT_BROWSER_VERIFIED; overall T070 post-publication verification is FAILED/incomplete and not accepted.

Actual bundle ID:35bad2ff04cdc17df5193ca026969380e7c9dc4176596601972b4af163b90e0a. Outputs and diagnostics are frozen in web/build/generated/t066/attempt-T070-1 and web/build/network-out. The exact failed verifier receipt and read-only mismatch audit will remain separate from original result/metadata.

## MAIN decision requested

Recommend a separately released, additive read-only verification of this existing frozen attempt/publication that checks every old input and preservation identity exactly, explicitly validates the exact authorized new17-file publication against original attempt metadata/outputs/notices, and retains the original verifier failure. No rebuild is needed merely to investigate this bookkeeping defect. Existing frozen tooling/pins/result/metadata should remain immutable for that review; do not silently relabel the frozen verifier as PASS.

A future tooling-fix ticket could distinguish pre-existing preservation from the exact authorized new publication while preserving the other profile's outputs and all strict source/tool/output gates. Any changed tooling requires fresh future pins for a later build; this worker has not implemented an exception or amended D059.

## Work stopped

Actual build and exact verifier are terminal (exit0 and2). Further verification remedy, tooling change, repinning/rebuild/runtime work is stopped pending MAIN's explicit resolution. Authorized evidence/handoff preservation continues only. No protected files were reverted or deleted.
