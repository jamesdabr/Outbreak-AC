# Once-only movement preparation construction

Revision:0.1. Status: APPROVED MAIN D295 for exact future construction clauses only. No MotionState/header/body/test/codec/runtime release, full M4 adoption or owner horizontal-rate selection. P1_RULES0.2 numeric values and D284 diagnostic/call bounds remain unchanged.

## Fault storage and supported aliases

Fault must have valid live storage DISJOINT from ALL input/context/output/used-scratch storage throughout a call. This is an API precondition, not a promised recoverable Fault-overlap case. A function cannot write an error into overlapping Fault while preserving those bytes. No fabricated union/reinterpretation/lifetime fixture may pretend otherwise.

With an independently disjoint Fault, recoverable known-span output/input or output/used-scratch alias rejection may occur before mutation under the proposed checked address-span rules. Valid input-input aliases remain permitted when all values/identity contracts hold. Opaque resource backing/lifetime/certification remains a caller precondition, not a zero extent. Do not read native padding as a semantic value or copy an invalid object. False preserves the entire valid old output; this does not create a test domain for Fault overlap.

## Actual airborne motor cap

After the ordinary once-only Q1 horizontal velocity update and its retained acceleration remainder, if certified working_grounded is FALSE (including an accepted jump), apply cap C=16*65536 to ACTUAL prepared (vx,vy). Let L=ceil_isqrt(vx²+vy²), checked signed64/u64. If L>C, set each component to trunc_toward_zero(v_i*C/L); otherwise leave it unchanged. L0 never divides. Only then do the single existing position integration. This is not merely a target t cap. Target formation still uses its proposed conservative speed/air cap and the unchanged selected rates; no speed/rate tuning or owner selector is chosen.

Keep the already computed scalar acceleration remainder and horizontal position remainders; no banked whole budget/new dt/force/query. Do not reapply this preparation inside contact/step/hold/fork/pair responses or final support: existing collision projection rules remain. At old sprint vx24Q16, fresh jump/target16Q16/r_acc0 gives Q1 budget20971/intermediate1551893, then required prepared vx1048576. Frozen air cap is enforced on the motor's prepared actual velocity before trajectory construction. Source must prove this exact grouping and preserve original scratch/query/response budgets.

## Vertical table after support and jump decision

D284 entry support itself changes ONLY working ground/flag. The following table is ORDINARY once-only preparation after poststance SafeStart/support and jump eligibility, before one position integration. A supported eligible jump requires selected fresh request, completed Standing and all existing identity/eligibility rules; request selection alone is not eligibility. Denied jump uses the corresponding no-eligible-jump row and applies no impulse. Canonical jump outcome/retirement remains separately specified; this table grants none.

| Entry condition | Exact vertical preparation |
| --- | --- |
| Supported, no eligible jump | vz=0; gravity_remainder=0; position_remainder.z=0. No gravity decrement this tick. |
| Unsupported, no eligible jump | (g,r)=divmod(32*65536+old_gravity_remainder,50); vz=old_vz-g; gravity_remainder=r; retain old position_remainder.z. |
| Supported, eligible jump | First vz=12*65536; gravity_remainder=0; position_remainder.z=0. Then ONCE (g,r)=divmod(32*65536,50); vz=vz-g; gravity_remainder=r. Working ground becomes false. |

All operations checked, no saturation or hidden terminal velocity. Apply the existing vertical position integration ONCE: D.z=trunc_toward_zero((vz+position_remainder.z)/3200), retaining signed remainder. New jump therefore has vz744489/gravity remainder2, D.z232/position remainder2089. Other axes/stance/foot are not reset by this table. Supported no-jump removes stale vertical drift only in ordinary preparation, never at a diagnostic support test or after the solved path.

D284 final support only updates final ground/flag, with NO second gravity/path/velocity/remainder adjustment or reintegration. Contact/step/fork/hold/pair replanning does not reenter preparation; D150's projected state/remainders remain within that tick. The next ordinary tick applies this table once to the then-current state. Replay recomputes each retained tick once from authoritative complete state, never integrates an already integrated result again.

This closes the posted vertical ordering seam without changing12/32/50/3200 or adding calls/caps. Full typed state/stance/source/Fault/prediction/private-seam adoption, owner horizontal selector, accepted full G1/G2 and separate implementation/evidence/actual/tick/browser/human gates remain. All Player/nativeT167/QA/T149 holds unchanged.
