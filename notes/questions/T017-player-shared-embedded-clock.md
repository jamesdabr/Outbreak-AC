# T017 local delta bound shares the embedded server clock

- Author / worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket and revision: T017 revision 0.3 RELEASED
- Phase and contract revision: P0 revision 0.3 prerequisite subset; BROWSER_FOUNDATION revision 0.3
- Exact clause or interface affected: Frozen experimental behavior, 250 ms local delta cap without changing server-owned deadlines; implementation boundaries 2 and 6 preserve embedded serverslice/localconnect and defer service separation.
- Status: OPEN (lead resolution is recorded separately)

## Question

How should the browser client-local 250 ms cap coexist with the retained embedded server's shared `lastmillis` clock? Capping client `curtime` changes `lastmillis`, and non-dedicated `serverslice()` directly derives `servmillis` and authoritative `sg->gamemillis` from that value.

## Evidence and impact

`source/src/main.cpp::mainloopframe` advances `lastmillis += curtime` before `updateworld` and `serverslice(0)`. `source/src/server.cpp::serverslice` computes `nextmillis = isdedicated ? enet_time_get() : lastmillis`, then advances `sg->gamemillis` by its difference. Thus retaining wall `totalmillis` alone cannot preserve embedded server deadlines. No changes to server.cpp or shared headers are authorized by T017.

The extraction, persistent frame state, guarded scheduler, input lifecycle, native syntax checks and helper tests can proceed independently. The delta helper can be tested independently, but its runtime integration for embedded local simulation awaits this resolution. No service disabling or shadow server clock is being inferred.

## Options for owner and lead

1. Approve an explicit integration clock/service boundary in a re-released ticket, with the owning worker and files identified. This preserves a true local cap and server timing under a reviewed interface.
2. Explicitly narrow the cap to clients connected to a separate server and identify the permitted behavior of the retained local startup path. This changes the frozen experimental requirement and requires a lead revision.
3. Explicitly approve bounded offline embedded simulation as a spike limitation, without applying that bound to a separate authoritative server. This also needs a recorded clarification/amendment.

## Work paused

Only runtime application of the 250 ms/reset delta helper is paused. Common frame extraction and input lifecycle continue. T017 will be submitted as partial unless this and actual Wasm TU compilation are resolved.
