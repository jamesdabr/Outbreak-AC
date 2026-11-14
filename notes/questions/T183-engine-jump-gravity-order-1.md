# Exact once-only vertical preparation at a selected jump

- Author / worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket and revision: T1831.0 / D289, notes-only materialization packet
- Phase and contract revision: P1_RULES0.2; QUERY_CALLER_BRIDGE0.2/D284; proposed H section4/draft2 Q1; accepted T180 notes/D288
- Exact clause or interface affected: MotionState.velocity.z/gravity_remainder/position_remainder and once-only preparation at an admitted jump or supported no-jump start
- Status: OPEN (lead resolution is recorded separately)

## Question

Please cite or freeze the exact integer vertical preparation recurrence after D284 entry support and jump eligibility. H specifies jump12Q16, gravity32Q16 and ground/no-jump gravity-remainder reset, but does not state whether a newly eligible jump's same-tick gravity decrement occurs before/after the impulse or begins next tick, whether the jump clears a prior gravity/vertical position remainder, and how supported no-jump preparation handles a nonzero stored vertical velocity after an earlier clipped/held candidate.

## Evidence and impact

H `notes/proposals/T002-P1-headers.md` section4 gives scalar position integration and those jump/ground clauses; draft2 Q1 closes horizontal budget recurrence only. D284 deliberately changes ground/flag certification, not path/velocity/remainder or extra integration. T180/D150 preserves projected canonical velocity and acceleration/gravity remainders through holds/restoration; it is not permission to zero them at a diagnostic support test.

For fresh zero remainder, one gravity budget is divmod(32*65536,50)=(41943,2). A jump impulse is786432. Thus applying that decrement after the impulse yields744489/r2 this tick, while a last assignment of the impulse gives786432 and requires an explicit remainder decision. Both cannot be the same deterministic state. This is fixed paper arithmetic, not generated game data or a choice of behavior.

The packet proposes exact paired stance/state/public/private/Fault/alias and jump selection/outcome clauses independently. It does NOT choose a new vertical recurrence, tune gravity/jump, grant another dt, alter D284 or ask the pending owner braking-selector question again. Source/goldens requiring these vertical results cannot freeze truthful expected bytes on inference.

## Options for owner and lead

1. Cite an already approved exact recurrence/order, including all three remainder effects, initial supported/non-supported state and jump-denial case, and bind it unchanged.
2. Freeze a short checked integer once-only vertical table for supported/no jump, unsupported/no jump and supported/eligible jump; specify impulse/gravity order and remainder effects while retaining the frozen12/32/50 values and existing position denominator3200. Distinguish ordinary preparation from D284's diagnostic, which cannot rewrite solved velocity/remainders.

No option or numerical result above is selected by this question.

## Work paused

Only future vertical preparation bodies and exact vertical golden fields wait for this clause (alongside all existing full typed/G1/G2/source gates). The authorized T183 notes packet, paired-state construction, private resource/call and ordered Fault proposal, finite existing-case mapping and new handoff continue. No source, test, fixture/oracle/dataset, compiler/runtime or closed T180 artifact is changed.
