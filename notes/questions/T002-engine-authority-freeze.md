# T002 authority and transaction choices for MAIN freeze

- Worker: Engine & Multiplayer
- Ticket/revision: T0021.0 / D056/D061, notes-only proposal
- Governing: product/parameters/interfaces0.2 draft constraints; P0 prerequisite0.5
- Affected clauses: boarding fairness/completion, universal revive/headroom, transport/session continuity, server catch-up health policy and shared parameter freeze
- Status: OPEN; recommendations only, resolution belongs MAIN

## Decisions requested

The concrete recommendation is in the three T002-engine proposal notes. No
implementation is blocked mid-flight: dependent gameplay has not been released.
These choices need explicit owner/lead resolution before the interface becomes
binding, rather than different workers interpreting the draft independently.

1. **Boarding request versus seat completion.** CONTRACT says first accepted request obtains a seat, but also completion of2s uninterrupted hold occupies it and clients cannot reserve seats. Recommend no reservation during the hold; on completion validate life/zone/damage/capacity and arbitrate equal-tick completions by original server receipt sequence then actor ID. Damage cancels unfinished hold; nonlethal damage after completed boarding does not release its seat. At departure process combat/down/bleed and valid hold completions before extracting living boarded occupants. Approve that interpretation or specify a different exact transaction point.
2. **Revive geometry and concurrent use.** Recommend real downed capsule blocking, no teleport/push/health grant through obstruction; completion rechecks crouched headroom, otherwise returns explicit NoHeadroom with no revival/resource award. Keep MVP navigation free of crawl-only traps. Decide whether5s hold may explicitly fail for that geometry or whether a separately specified recovery stance/displacement is required. Recommend fire/sprint/selection cancel ongoing use holds; completed boarding still permits ordinary combat and remains vulnerable. Freeze those conflicts before World/Player code.
3. **Private eight-slot identity and long-round continuity.** Current gateway/backend limits2caps/150s/180s and one boot/page are deliberately experimental. Recommend a separate eight-slot profile with anonymous room/participant identity, fresh one-use admissions and same-round LEFT only reconnecting as eligible spectator, never a replacement actor. Use trusted local coordinator/native control channel, no accounts/public service. Sessions remain through normal Results→Lobby; if operational lease is insufficient for the next round, renew only in Lobby with a new admitted generation, not hidden in-round retry. Decide the ordinary user flow and operational lease policy; do not tune existing components in place.
4. **Overload/no-rewind/number freeze.** Recommend T071-aligned50Hz/25Hz/80ms interpolation,4 catch-up ticks, input age160ms/future20ms,100ms input lease and current-world no-rewind shots. Server debt>200ms must visibly invalidate/abort an unhealthy attempt under an approved failure policy, not drop authoritative time or claim a completed normal match. Approve that failure policy and the three notes' numeric table (including T071 movement/camera/weapons, AI/wood/medical/deployment recommendations), or publish exact alternatives. Proposed damage/life batching includes same-tick trades and no alive-overkill spill into a newly created down pool; freeze this too.

## Evidence and impact

Legacy server.cpp SV_POS/POSC directly accepts coordinates; SV_SHOOT builds
GE_HIT from client target reports, and serverevents.h consumes them. Existing
friendly-fire penalties and local outbreakstate.h20s/3s/team-limited behavior
conflict with MVP authority/life constraints. They must be isolated, not renamed
as a shared authoritative system. T068/accepted components are useful foundation
evidence but contain no adopted Outbreak authoritative protocol or long-round
eight-player transport policy.

Current source remains frozen. T070 full prerequisite build, T067 observer
preparation and T071's proposal/tag question have their own authority; this note
does not stop, dispatch or amend them. No engine/hosting/provider change is
requested or inferred. MAIN's platform/interface/parameter and file-lease
decisions plus P0 gates precede dependent implementation.

## Work paused

No T002 notes work remains paused. All proposed code/protocol/lifecycle/parameter
adoption and gameplay execution remain unreleased pending MAIN review/freeze.
