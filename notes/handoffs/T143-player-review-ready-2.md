# T143 — REVIEW-READY2 raw denial-close lifetime correction

- Worker: Player /01a1b92b-cdb9-7202-ac82-dadb42d64f5e.
- Ticket / revision: T1431.0 same RELEASED/unfrozen lease; scoped MAIN-T143-review-ready-1-return correction only. No authoritative status change.
- Phase / contract revisions: capability0.4/D169, governance/foundation/P0 0.5 prerequisite scope unchanged; no new actual approval.
- Base commit and pre-existing edits: exact REVIEW-READY1 four files preserved in preparation-1/intermediate-2 with hashes matching the old145-case receipt. Earlier intermediate-1/143-case success, baseline T103 four-file copies and all histories remain unchanged. No Git/source takeover.
- Changed files: current T143 four files, NEW intermediate-2/fixtures-3/node-cache-3/tmp-3 and new baseline/scoped diff artifacts under preparation-1, this own new handoff. Old T103/report/freeze/installed sources and all earlier T143 notes/receipts/diffs/caches read-only.
- Commit or patch reference: none authorized/created.

## Acceptance evidence

PASS (FIXTURE_ONLY): inspected changed source/harness, then fixed Node24.19.0 SHA27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1, current fixtures-3 exit0/stderr empty.149 named cases PASS, including all prior145 in identical name/order/purpose and the original113 mapping.68 reference identities match before/after and rechecked before this handoff; exact Node invocation/env/stdout/time retained in fixtures-3/invocation.json. VM host imports/clock/timer effects0; pre-import forbidden package self-checks remain labeled fakes. All scratch is under preparation-1, no actual installed method call.

PASS (specific returned finding, actual shared helpers under fakes): makeDenyHandler now inserts a retained raw-settlement promise before the bounded wait. It tracks NOT_STARTED/PENDING/FULFILLED/REJECTED independently from wait completion. Two-second wait timeout leaves raw PENDING in the tracked set; cleanup cannot report ws_denial_closes_complete while any raw close remains pending. Raw rejection or a not-started recorded decision also prevents complete cleanup. Definite non-invocation releases only the placeholder, without inventing settlement. No new wait allowance or API.

Four added regressions use actual operationScope + makeDenyHandler + denialClosesComplete, with a scaled fake clock matching80s/120s and the real2s close-wait argument:

1. route.close never settles: after2s the bounded wrapper finishes with deadline error but raw PENDING remains in pending ownership. Actual cleanupFacts receives the actual computed completion flag and returns FAIL. A second bounded cleanup drain expires while the raw close remains retained; no host timer or resource exists.
2. Late fulfillment: raw ownership releases, raw state/settlement time/close_settled become truthful fulfilled facts. Original deadline/wait failure/error remains sticky; correlated denialFacts still FAIL and overall fault is not repaired.
3. Late rejection: raw rejection/error and time retained separately, pending ownership releases, but raw REJECTED prevents completion; original wait deadline is preserved and no rejection is unhandled.
4. Invocation refused at total cutoff: close factory not invoked, placeholder released with raw NOT_STARTED/close_settled:false; no fake raw settlement/complete cleanup.

Prior immediate-close/failure and all145 cases also pass, so the new regression exercises the missing pending raw operation rather than only a manually false cleanup flag. The full effectful future function is still UNRUN.

PASS (preservation): all18 accepted T103 members rechecked byte/size/mode against accepted freeze; T136 report remains29744bytes/SHA2e0fdca3546415b4d03efe98fc6853a653ffcad402337f29d428d554425d061a. Exact baseline and both earlier T143 source versions/receipts/diffs remain retained. T143/run-1 and any preparation freeze remain absent.

## Exact current review identities

| File under web/qa/capabilities/T143 | Bytes | SHA256 |
| --- | ---: | --- |
| `probe.cjs` | 52324 | `47899064951c1c3925bf70b296efb0d84463688381554f0a490c79ac14d667e3` |
| `test.cjs` | 49861 | `63e1307f308eb6934949913e9fb9089e3a4f8e34e83349002a7d4911bfeb8824` |
| `SCHEMA.md` | 23638 | `99e1c3bdf75b61702eaaf8b0ff18be976f61032707152f0d81b85fb09b1db21d` |
| `README.md` | 4490 | `d869e4e814131b607f7a3133f6fcc6dce7d1416fcacada7026969d80247b9191` |
| `preparation-1/source-diff-3.patch` | 93502 | `56a2538f3328b3c26b781ee5bf23327b24ccc20911540b49136c5ab4187dc102` |
| `preparation-1/review-return-diff-3.patch` | 30394 | `446de8f3ec86c011d19c4b5e355e01e77e2a82ec95fc0713c4ee6007e9935156` |
| `preparation-1/fixtures-3/receipt.json` | 68373 | `2ae75f8198ab48e902b7cb47138a50da180527ca9c4099b54918bd77c76bb74d` |
| `preparation-1/fixtures-3/references-before.json` | 13662 | `51c712fda777144966efd5d884768f4eb2a60613a0dfcba1b69ba818d7e7553a` |
| `preparation-1/fixtures-3/references-after.json` | 13662 | `51c712fda777144966efd5d884768f4eb2a60613a0dfcba1b69ba818d7e7553a` |
| `preparation-1/fixtures-3/invocation.json` | 822 | `95f61c4393980acee1d280a8a0e73e02b26eb814deb9bfc827fc53b6cf538e06` |

source-diff-3.patch is the full current four-file diff from exact accepted T103. review-return-diff-3.patch is the focused four-file diff from submitted REVIEW-READY1. Both were recomputed independently and matched before submission. Old source-diff.patch/source-diff-2.patch and earlier fixture references remain immutable; current reference graph binds them plus intermediate-1/2 and prior receipts/handoff/review finding.

## Implementation status

Implemented only the returned private lifecycle correction and exact schema/docs/test evidence. Pending-denial ownership follows underlying raw promise settlement, no longer the deadline wrapper. New row fields raw_close_state/raw_close_error/close_wait_error/raw_settled_at_ms distinguish unknown pending, raw completion and wait failure; close_settled/closed_at_ms only mark raw fulfillment. cleanup.ws_denial_closes_complete uses the actual raw-owned set plus recorded FULFILLED states. Successful public close still does not itself prove a packet was blocked: registered-decision/page-pre-open-close/no-native-denied-socket/zero-sink evidence remains unchanged.

Simulated:149 builtin/VM cases with fake Page/context/route/CDP/server/process/clock/delayed raw close values. No valid runFixedProbe, actual Playwright/package method, browser/native/process/socket/inspector/network/system probe or live fixture. Inherited invalid-argument runner refusal still happens before host effects. No alternate guard, allowed-path, regex, binary parser/payload/echo, cache/GPU classification, policy, dependency, flags, budget, public export or performance claim change.

Incomplete/unproven: actual installed selective enforcement/cache/target/binary/lifecycle/cleanup support, game suitability, native backpressure/bufferedAmount/startup/timing transparency, frame fidelity, worker/browser-wide protection, true RSS and P0. D108 raw early output stays NOT_OBSERVED/PUBLIC_HANDLE_NOT_AVAILABLE_EARLY/complete_byte_bound_proven:false/overall PARTIAL. QA paused; the prior owner-approved actual call is consumed.

## Integration and questions

No new question blocks this exact return. Source/schema are REVIEW-READY2 BEFORE FREEZE; MAIN independent tests/review/clearance pending. No freeze or new actual execution is authorized. Keep all intermediates; do not rerun into occupied fixtures-3. Any further scoped correction gets fresh preserved evidence/diff/review identities. Standby after delivery.
