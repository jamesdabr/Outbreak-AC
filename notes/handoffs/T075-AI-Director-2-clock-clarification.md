# T075-1 clock interpretation addendum

This additive note follows T075-AI-Director-1 and MAIN's subsequent source review.
Original actual result/logs/freeze and first handoff remain unchanged. One actual
attempt, supervisor exit1, cleanup verified, no retry or frozen source edit.

**The measured1047ms is published main raw elapsed, not proven backend
inter-frame elapsed.** The observer's literal `actual frame gap exceeds backend
policy` is its failure label; it is not sufficient evidence of an actual backend
gap violation or BNE_VISIBILITY. Earlier wording about a frame gap should be read
with this distinction. The baseline remains FAIL because that frozen guard
terminated it; the actual game/backend root cause remains unestablished.

Independently read static sources after MAIN's clarification:

- main.cpp1643–1660 computes elapsed from SDL ticks/clock base minus totalmillis
  and publishes it with unsigned(frame.frames). Initial totalmillis can make
  the first reported raw elapsed include startup work.
- enet_websocket.js59–62 separately uses its performance clock and only rejects
  an interval>1000ms when lastFrame is **not null**. Initial backend frame has
  no prior-frame interval to reject.
- Frozen observe.cjs58 rejects every published raw_elapsed_ms>1000 without
  retaining the full sample/frame_id first. B's retained stage is BN_OPENING,
  focused/visible, raw_elapsed1047; that trace cannot distinguish an initial
  elapsed from a later backend inter-frame stall. Startup elapsed is plausible,
  not established as the actual cause from missing frame_id.

No source/threshold/backend behavior was changed. MAIN is preparing a separately
scoped observer correction for first-frame semantics, complete last failure
sample retention and genuine later-frame/backend error enforcement. That future
release is not assumed here. Current failure remains preserved and reruns frozen.

Question linkage: notes/questions/T075-AI-Director-startup-frame-gap.md remains
open; this addendum supplies the new bounded interpretation for MAIN's resolution.
Actual evidence freeze SHA5216474d0c9b02632284c93d50a0d327d46ae8b9cd72dfc607119bcf66f14cd8
continues to match. No new runtime evidence or successful baseline is asserted.
