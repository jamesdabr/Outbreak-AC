# T075-1 failed on client B startup frame gap

- Author / worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket and revision: T0754.8, one actual invocation under D068.
- Phase/contract: browser foundation/GOVERNANCE/P0 0.5; client0.3/main0.1;
  backend0.2/transport0.2; frozen T0674.2 preparation D067.
- Exact affected clause: preserve actual failure, no retry/source/flags/limits
  fixes; raw frame gap1000ms and whole180s baseline limits remain unchanged.
- Status: OPEN; resolution belongs to MAIN in a separate decision.

## Question

The one authorized actual attempt has failed and its supervisor exited1.
What separately scoped investigation, if any, should follow the observed B
startup timing failure? No rerun, driver/source change or limit/flag amendment
is authorized by this question.

## Evidence and impact

`web/transport/results/two-client-T067/runtime-T075-1/result.json` records
`observer.errors=["actual frame gap exceeds backend policy"]`. B's last retained
trace at observer2391.34325ms is `BN_OPENING:0:true:visible` with raw_elapsed1047ms,
exceeding1000ms. This is the observer's actual measured guard failure; the trace
does not prove B latched BNE_VISIBILITY or became hidden. It does not establish
whether startup work, GPU compilation, OS/browser scheduling or another cause
produced the interval. No timing spoof/flag change/retry was attempted.

A previously reached observed `BN_ACTIVE:4` at734.481291ms, spawn_requests0,
recorded honestly as native spawn without a published request. Initial exact
event/identity snapshots were not retained by the frozen observer before paired
readiness, so this partial trace is not complete per-client proof acceptance.
B did not reach a retained ACTIVE sample; paired `active=[]`, `moves=[]`.
Bidirectional movement was NOT RUN. Native log confirms actual LAN-only map
revision2/561 and two connections; this is not B completed game join/spawn proof.

Cleanup completed: native4718 SIGINT exit0 in3.685625ms, no fallback kill;
Node/native/browser groups and known owned PIDs gone; contexts/profiles removed;
gateway closed in0.405875ms with zero timers/TCP/UDP/pending/retired resources;
static closed. Original report source_stable true. Actual cleanup supplement
verifies all fixed and recorded ephemeral ports, including both gateway UDP
tuples61734/62986, by owner/no-LISTEN and bind/errno checks. No unrelated process
was signaled. Runtime evidence and native staging are preserved, reruns_frozen true.

Two frozen observer evidence limitations are now observable and should be scoped
explicitly if MAIN wants later preparation changes: (1) on observer failure it
does not add final gateway tuples to its own rebind list; additive cleanup proof
was recorded without changing the original report; (2) early per-client join
success/failure trace retains stage/count/timing, but not the full published
milestone/identity/error snapshot. No frozen source was edited to remedy either.

## Options for owner and lead

1. Review this failed actual attempt as-is and release a bounded static timing /
   observer evidence investigation. Preserve current runtime limits and artifact.
2. Separately release an additive observer preparation change for bounded full
   failure snapshots and final-tuple cleanup bookkeeping, with new source hashes
   and fixtures before any new runtime pins. This alone would not fix frame timing.
3. Defer further runtime work. Current data cannot support a successful baseline.

## Work paused

All further actual baseline invocations and source/flags/assets/limits changes
are stopped. Independent authorized work completed here is failure evidence,
additive owned-cleanup verification, immutable fingerprints and handoff only.
