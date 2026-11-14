# T071 position-only tag output needs inspection before P1 reuse

- Author / worker: Player / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket/revision: T0714.3 proposal-only; accepted T065 source remains frozen
- Contract/interface: P1 future local-body/weapon alignment; existing modelattach/MD3 position-output semantics
- Status: OPEN, static finding for MAIN; no current source/runtime failure claimed

## Question

When MAIN releases future P1 attachment/locator work, include an actual position-only tag-output regression check and, if confirmed necessary, a narrowly owned renderer fix. This note is not authority to patch current T070/T065 source or rebuild its artifact.

## Evidence and impact

In source/src/md3.h `md3::render`, the branch with no attached model but `a[i].pos` calls `link(NULL, a[i].tag)` without forwarding that output pointer. The attached-model branch calls `link(p, a[i].tag, a[i].pos)`. source/src/vertmodel.h `link` has an optional third `vec *pos` parameter. rendermodel.cpp `renderclient` uses position-only tag_head output, and P1 muzzle/attachment work must not assume such a lookup returned a position merely because loadmodel succeeded.

This is static inspection only; no code/test/browser execution or runtime misrender/hit failure was observed. New authoritative hit volumes must never depend on render-derived head/tag output regardless of the renderer result.

## Options for owner and lead

Inspect/test actual tag-link output during a separately released renderer slice. If required, approve an exact MD3/header allowlist and regression evidence, preserving native/prerequisite behavior and earlier artifact identities. Otherwise document why the existing path is correct. Do not mutate current frozen code through this proposal.

## Work paused

No T071 preparation is blocked. Only future use of position-only tag observations lacks verified semantics. T070's frozen build and T067 baseline remain independently governed; this note does not grant a rerun, source fix or gate waiver.
