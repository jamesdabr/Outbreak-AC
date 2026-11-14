# Native parsed movement evidence under the fixed normal-pair profile

- Author / worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket and revision: T1171.0 preparation only
- Phase and contract revision: CANDIDATE_PAIR_SMOKE0.1/D123/D124; CANDIDATE_RUNTIME_ADMISSION0.1
- Exact clause: actual proof requires parent native-log parsed-receipt evidence, source-derived unchanged T067 parameters/argv and original T079 semantics
- Status: OPEN (lead resolution recorded separately)

## Question

Does “native log parsed-receipt evidence” mean independent native startup/two
connection+login/map-rev2 log evidence combined with the receiving real C++
client's published parsed cn/life/position/ordinal/timing receipts, as T079
actually retained? Or is a new native per-position receipt record required?

## Evidence and impact

Read-only source/server.cpp3745–3767 SV_SPAWN and3863–3945 SV_POS/POSC validate
and forward client state but emit no cn/life/position receipt log there. Original
web/transport/results/two-client-T067/runtime-T079-1/native.log has startup,
two loopback connections/logins and map rev2, not per-movement receipt records.
The frozen source-T079-1 parent cross-validates public browser parsed receipts
and actual gateway/native evidence; it does not parse native position ordinals.
T117 forbids changing source/config/argv or adding packet/private instrumentation.

## Options for owner and lead

1. Clarify native evidence as its actual fixed startup/connection/login/map facts
   plus independently checked real C++ receiving-client parsed movement proofs.
   This preserves the source-derived T079 evidence without claiming native
   internal clientsequence/cache or server authority observation.
2. Require new native per-position diagnostics under a separate reviewed source
   contract/build/release before real execution. Preparation can reject their
   absence, but cannot manufacture them or amend the fixed profile.

## Work paused

Only final adoption of this parent evidence interpretation waits for MAIN. Pure
admission/schema/ledger/privacy/deadline/observer/ownership/cleanup fixtures and
source preparation continue. No runtime authority, fake receipt or worker policy
amendment follows from either option.
