# T0021.1 Engine handoff — complete P1 record/wire/seam proposal

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T0021.1, RELEASED notes-only under D096; submitted for MAIN review, no self acceptance
- Phase / contract revisions: GOV/BROWSER_FOUNDATION/P0 0.5; CONTRACT/PARAMETERS/INTERFACES0.2 draft constraints; P1-combat0.2 draft; approved PLATFORM_DECISION0.1/P1_RULES0.1; accepted fixed/envelope/dry-flat public APIs unchanged
- Base and pre-existing edits: ticket base13f0d8eea4822dee5c976661218d022be74342e3 plus preserved prerequisite work; observed HEAD at final read31d433b993d393b1902f7f57285a1d5ea6d2042d. Notes do not change source closure, accepted T097, D106 staging or any pre-existing edits. No clean-checkout claim.
- Changed files: NEW notes/proposals/T002-P1-headers.md, T002-P1-wire.md, T002-P1-seams.md; NEW notes/questions/T002-engine-P1-boundary.md; this NEW handoff. Earlier T002 proposals/questions/handoff immutable.
- Commit/patch reference: no commit, Git mutation, source/header/config/SDK/assets/tooling/evidence/contract/ticket/decision edit or worker dispatch.

## Acceptance evidence

All PASS below means **proposal coverage/static inspection only**, never adopted
interface, implementation, P0/P1 acceptance or actual execution evidence.

| T0021.1 criterion | Result and location |
| --- | --- |
| Complete public C++11 namespace ob record/function graph, explicit header homes, only specified opaque storage | PASS proposal: headers sections1–9; exact include graph, fields/enums/bounds, init/destroy/spec/inspection, 8MiB aggregate/64KiB stack requirement, no mutable public World/by-value World. |
| Frozen rules, deterministic state/remainders, query/motion/camera/combat algorithms, atomic commit | PASS proposal: headers sections2–6; no tuning parameters, immutable accepted helpers, exact angle/hash/PRNG proposals, query failure states, candidate/outbox atomicity, operational guard vs canonical checkpoint, TrustedResults. Actual algorithms/performance NOT RUN. |
| Exact complete P1 wire bodies, identity/sequence/cache/baseline lifecycle and examples | PASS proposal: wire sections1–6; IDs1..25, 36-byte header/max1100, header flags0 distinct from ENet reliable metadata, all offsets/lengths, baseline332-prefix/max1144/two980-byte chunks, request namespace/cache and canonical ACK distinction. Actual codec tests NOT RUN. |
| MAIN preliminary review: view_ack/scope_ack and RESYNC canonical ingress | PASS proposal response: headers section5 InputAdmission/admit_input_batch, ReplicaIntent/admit_replica, stamped bounded PeerTickInput.replicas and receipt-order stage1 processing, staged base/recapture/IDs, exact ConsumedPeer/ConsumedBatch retirement; wire section5 cross-reference. No callback scope/base grant. |
| MAIN preliminary review: local prediction schedule/gaps/duplicate estimate/lease/reconcile | PASS proposal response: headers section7 PredictionInput.simulation_tick/fresh/neutral, explicit per-tick hold records and128 bound, lease expiry, replay retirement and worked seq11/12 trace. Local deterministic schedule is explicitly separate from unknowable future server receipt timing. |
| Complete native/private-room and build/source integration seams | PASS proposal: seams sections1–6; AppStart includes WS cap/ticket; exact private JSON/control bytes, bounded result mapping to TrustedResult, native/gateway admission/compensation/lease/allocation policy, one pump, legacy bypass closures, ordinary SDL bridge, one-way mirror, exclusive file stages and proposed76-browser/27-native unit expectations. Actual source closure/build/runtime NOT RUN. |
| Later MVP preserved; no provider/tester API, scoped unresolved choices | PASS proposal: seams section7 and new boundary question; P2–P5 extensions await later freeze, eight-player/squads/900s/Blackwood/revive/loot/wood/Predator/Director/extraction/tester/human gates remain. Scenario boundary remains explicitly proposed/open, no implementation authority. |
| Read-only/new-note scope, final consistency and freeze | PASS static: reread tickets/T002.md and both approved addenda immediately before handoff; inspected exact accepted fixed.h/envelope.h/map_import.h; rg search found no obsolete1116/304/body1..24/admit_input API leftovers. Hashes below freeze four deliverables. |

Verification actually performed: read-only cat/sed/rg inspection, shasum, git
rev-parse HEAD and `git diff --no-index --check /dev/null <each-new-note>` on
all four frozen files. Each whitespace check produced empty diagnostics and
exit1 because the new-file diff exists; this is not a test/compiler pass.
No code imports, scripts/tests, compiler/Node/browser/native process/service,
network/install, simulator or benchmark. No OS/toolchain/hardware performance
claim is made. Samples/counts/byte arithmetic are specified/manual, not measured.

## Frozen deliverables

SHA256, captured with `shasum -a 256` from workspace root:

| Path | SHA256 |
| --- | --- |
| notes/proposals/T002-P1-headers.md | 79fa17d45f11d480a66a57435a258811722c075e1dddc1926428958f2cb01709 |
| notes/proposals/T002-P1-wire.md | b625e2e9d8161c3fff5c2afc0f0976fc1f6d03e62d0fdb4a2ba52c15c4aeac16 |
| notes/proposals/T002-P1-seams.md | b50cd481a3cf4d4acf5822fa17f87e254f12dfaf441c9b718ccbf2b87ceb1855 |
| notes/questions/T002-engine-P1-boundary.md | 294cd64c3ce5c2a6c565a123a250a4ae65f25489bb1afb2abdaa9ca1561f8b18 |

This handoff is the freeze receipt, not a self-hashed fifth member. Any requested
successor edit requires reviewed successor hashes; earlier proposal/evidence
freezes remain unchanged. MAIN's preliminary reviewed drafts are superseded by
these hashes for review, not retroactively modified/accepted.

## Implementation status

Implemented: five new Markdown notes only. Simulated/test doubles: none.
Incomplete/unreleased: all proposed headers/codecs/core/adapter/control/build/
gameplay implementation, real native+Wasm tests, actual two-browser normal/impaired
combat, full population/performance and human evidence. Existing prerequisite
evidence is only historical foundation, never relabeled authoritative P1 proof.
Storage/stack/tick/source-unit bounds are proposed requirements, not measured fits.

## Integration and questions

MAIN must review exact records/bodies/header graph, algorithms/table artifact,
map/anchor pins, private control formats and technical resource caps before
dependent releases. New T002-engine-P1-boundary.md asks only how the combat-only
P1 evidence build terminates before P3 exists; proposed private EndP1Scenario/
scope-abort is not adopted product behavior. No new dependency/asset is installed
or made binding. Future stages identify exact owners and serialize overlapping
main.cpp/core/renderer edits; no worker has been dispatched by this handoff.

Reproduce this static submission review by reading the three proposal notes,
comparing body records against wire offsets/common layouts, checking the ingress/
replay worked trace and seam ownership table, then rerunning only the read-only
hash/whitespace commands above. No build or runtime command is part of T002.
