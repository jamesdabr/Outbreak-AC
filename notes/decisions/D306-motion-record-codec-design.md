# D306 — Prepare the isolated motion record codec contract

Release Engine T1911.0 NOTES ONLY while World constructs G2 and AI constructs the camera harness. The accepted T189 headers supply the actual sole MotionState home; T183's reviewed living-state/60-byte encoding proposal supplies design context. Neither approves a validator, codec or movement body. No production/API/semantic adoption occurs in this decision.

The next useful independent deliverable is one concise, implementation-ready proposed contract for pure living MotionState validation and its fixed60-byte encoding. Isolate record validity from world feasibility, actor authority, jump eligibility, motor selection and tick commit. In particular the pending owner horizontal selector is irrelevant to record validity and remains pending. Existing p1_types/input/header/evidence bytes and all full-MVP/Player/QA gates remain unchanged.

MAIN will review and explicitly adopt or return the proposal before any new source lease. Do not turn this notes assignment into a new full movement plan or a source/generator/compiler/test operation. The worker must name genuine unresolved issues and continue independent notes; it cannot amend behavior itself.
