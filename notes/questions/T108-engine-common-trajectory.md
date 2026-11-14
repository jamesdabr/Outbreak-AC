# Common time convention for step/slide actor trajectories

- Author / worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket and revision: T1081.0, notes-only pair-query addendum
- Phase and contract revision: P1_RULES0.2/D112; frozen T0021.1 proposals, not approved interfaces
- Exact clause or interface affected: T002-P1-headers.md section4, move_one/MoveResult, same tick-start trajectories, step up/forward/down, <=4 slide contacts/<=4 residual pair passes
- Status: OPEN (lead resolution is recorded separately)

## Question

What common time/path convention must Engine use to feed BOTH actors' piecewise
step/slide trajectories to the new pair-only linear sweep? In particular, how
do up/forward/down step legs and stance-size changes align with another actor's
motion within the same20ms, without adding movement time or treating actors as
updated in roster order?

## Evidence and impact

The frozen move_one public result exposes final MotionState/contact/pass counts,
while its movement paragraph requires world slide/step paths and bilateral
same-start pair resolution. Neither defines time spans for those legs. World B
can implement the exact two-linear-trajectory primitive in the new addendum;
Engine C cannot safely substitute final start→end chords for actual paths. A
two-leg wall slide can contact an actor on its first leg while its chord misses,
or its chord can cut through an obstruction avoided by the actual path. Steps
also have vertical legs/possible zero-duration transitions that cannot silently
receive extra dt. A changing-height capsule is not the fixed-height linear
primitive's input domain.

The pure query contract, symmetry/contact semantics, bounds and tests can be
reviewed independently. Full multi-contact/step integration must wait for an
explicit caller trajectory convention; no source implementation is released.

## Options for owner and lead

1. Specify a bounded common timeline for the actual world-resolved piecewise
   trajectories, including step/stance transitions and conservative quantization.
   Engine privately builds/replays those paths from the shared tick-start state,
   intersects common linear intervals and calls the World primitive; no new
   cross-owner geometry helper is needed. Recommend this preserves the required
   step/slide behavior, but exact timeline/zero-duration treatment needs review.
2. Specify a different joint world/pair solver that advances common residual
   intervals while retaining the approved step, slide, speed, dt and pass limits.
   Its precise numeric/caller convention should be proposed and approved before
   source release; an endpoint chord or sequential actor update is not an
   automatically equivalent substitute.

These are design options, not delegated changes to approved movement behavior.

## Work paused

Only the common-timeline caller integration claim/implementation waits for this
decision; complete pure pair-query proposal and static handoff continue under
T108. No frozen note/header/record/numeric/wire/source is amended. MAIN may review
the additive primitive separately and request a narrowly scoped successor note
for the caller convention before dependent Engine C release.
