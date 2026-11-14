# T135 parent proof failed after real pair and captures

- Author / worker: World/Match-Systems
- Ticket/revision: T1351.1 / D157, smoke0.8/admission0.4
- Status: OPEN (MAIN resolution recorded separately)

## Actual terminal failure

ONE dispatched D157-pair-1 call exited1 after195.36321654205676s, runtime_started:true, statusFAIL, reruns_frozen:true. No timeout/overflow/supervisor signal/retry. Parent report errors=["timely native spawn ACK"], evidence_validated:false; observer reported OBSERVATIONS_COMPLETE/errors[]/two active clients/two moves/two real PNGs. FAIL receipt errors=["terminal captures required"], captures[], report_sha256:null,ledger_sha256:null. All raw files remain unchanged.

## Concrete retained data for MAIN review

policy.py:376 requires first four milestones1,2,3,4 and specifically mil[3].life==current own.life as part of the conjunction labeled timely native spawn ACK. Retained active A has own(cn0,life1,state0), with two milestone4 ACKs:186.5ms life0 and236ms life1, following OPEN119.1ms. Thus the first milestone4 life0 differs from current own life1; the label alone is not evidence of a late15s ACK. Active B has own(cn1,life0,state0), OPEN104.4ms and milestone4 at2370.9ms life0. This is static retained-data comparison, no extra gate call or decision that multiple ACKs should be accepted.

Runtime validates parent proof before assigning report captures. That proof failure leaves report captures[] although child captures and two actual files exist. Terminal capture_inventory then reports terminal captures required, so the receipt's final error differs from the report's primary error. No file/state/capture-validation threshold was waived or run manually.

## Question

MAIN should review strict ACK/current-life interpretation against actual multiple-ACK evidence, and secondary failure-reporting/capture-closure behavior, before any separately released correction or fresh attempt. Preserve original failed receipt/report/ledger/PNGs and both error layers; do not patch/reseal this run or promote child observations to accepted parent proof.

## Images / cleanup / stop

Actual partial images: runtime-D157-pair-1/view-A.png (881575bytes,SHA14e65736cf6cb905e33cc1e2b8800ec01264019a5076b7a195164dd9d45b2b0d) and view-B.png (890145bytes,SHA cfe9c157bd7b86d6453ed949fc1c222022223e641b5cc02284e19175d6374ae6), both1200x675/0600/nlink1. Parent accepted capture refs are empty; visual/pixel correctness awaits MAIN inspection. No mockup or substitute.

Recorded cleanup: native exit0/61.387ms, no kill fallback, groups reaped,139inspectors reaped, ports released, browser/context/gateway/static closed, profiles/entropy removed; targeted retained-path check confirms private paths absent. No manual live process/port probe. Exact source9/pins unchanged. Own post-terminal handoff notes only; no second call/repair/workaround. MAIN controls quiescence release and next scope. See notes/handoffs/T135-world-1.md.
