# T276 — Gateway close diagnostics source ready

- Worker: World /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket / revision: T2761.0 / D471; source stable, writes CLOSED for MAIN review.
- Phase / contract revisions: VISIBLE_SLICE0.7; ticket and contract reread before submission, unchanged.
- Base commit and pre-existing edits: no Git operation. Wrapper matched retained `notes/preflight/MAIN-local4-gateway_local.cjs` before this change, including its existing local-4 path; retained source/history untouched.
- Changed files: `web/visible/gateway_local.cjs` and this new handoff only. No commit authorized.

## Acceptance evidence

- PASS (source): existing gateway_closed event/clean/admitted/to_udp/to_ws retained. Added exact fixed numeric tcp_accepted, tcp_rejected, upgrade_attempts, rejected, send_errors from existing counters.
- PASS (source): admission_reasons has all 13 ticket-listed literal keys plus other. Only literal recognized string reasons increment their fixed slots; every other diagnostic contributes only to other. No raw diagnostic/session/snapshot, URL, header, capability, payload, config or exception reflection.
- PASS (source): inspected gateway.cjs snapshot/record paths and gateway-limits.cjs diagnostic cap512. Fourteen reason counts are each at most512; fixed fields/numeric serialization keep this close event comfortably below16KiB. Existing total8MiB capture bound and all cleanup criteria/timers/lifecycle/policy/component schema remain untouched.
- PASS (syntax): `/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node --check web/visible/gateway_local.cjs` exited0 with no output; no wrapper execution.
- PASS (diff inspection): `diff -u notes/preflight/MAIN-local4-gateway_local.cjs web/visible/gateway_local.cjs` shows only the additive close-summary block/fields (normal diff exit1).
- NOT RUN: service/game/browser/network/probe/fixture/runtime. MAIN owns separately releasing local5; QA remains paused.

## Implementation status

Implemented additive read-only close summary. No simulations, admission fixes, policy changes or runtime result claim. Counts explain only retained bounded diagnostics; other includes existing non-admission reasons such as component closure.

## Integration and questions

Existing bounded snapshot consumed unchanged; no dependency/interface change or unresolved question. MAIN can repeat the exact syntax command and retained-source diff above before separately preparing the next run.
