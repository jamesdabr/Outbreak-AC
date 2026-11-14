# Separate read-only observation: malformed RLE repeat count is not bounded to remaining cubes

- Author / worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket and revision: T042 1.6 RELEASED
- Phase and contract revision: browser foundation/GOVERNANCE/P0 0.5; D019 additive 1.6
- Exact clause or interface affected: D019 says not to fix unrelated malformed-map bounds and to record separate concrete problems.
- Status: OPEN (lead resolution is recorded separately)

## Question / observation

During the required decoder inspection, `worldio.cpp::rldecodecubes`, case 255, reads `n = f.get()` and performs `loopi(n) memcpy(s++, t, sizeof(sqr))` without checking `n <= e - s`. The outer `while(s < e)` does not bound the copies inside this branch. Thus a malformed repeat count can exceed even correctly allocated destination capacity. This is distinct from the valid-map entity/world alias fixed by T042.

## Evidence and impact

Source-derived observation only: after one ordinary cube, a repeat count larger than the remaining declared output count reaches the unchecked copy loop. No malicious/malformed overflow fixture or full game was executed. The accepted original map's real RLE stream decodes successfully in the focused ownership helper; a truncated stream returns the existing error result. The current guard deliberately leaves decoder behavior byte-for-byte unchanged.

## Options for owner and lead

If warranted, release a separate bounded-decoder validation ticket with explicit malformed-input/error policy and tests. This note grants no implementation authority and does not broaden T042.

## Work paused

None of T042's scoped source/compile/helper work. No bounds fix or parser change was attempted. Future malformed-map hardening is outside this ticket.
