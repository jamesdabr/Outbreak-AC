# T168 — Expired persistence descriptor ownership

Worker /root/review_native_candidate; T1681.0, DEFAULT_DEV_BUILD_PREPARATION0.1, D238.

The D238 review says to release acquired handles; MAIN's clarification prohibits starting close after the original effective cutoff. These differ only when a raw write returns late with an acquired descriptor.

Asked MAIN whether to release the raw descriptor independently without buffered flush, or retain its strong ownership and report unresolved release after expiry.

MAIN resolved: use the second option. Unbuffered IO; release only while the original effective cutoff remains. After expiry retain and report SKIPPED_EXPIRED/UNRESOLVED; no new close/flush/fsync, grace or retry after ambiguous close error. Outer FAIL evidence may use remaining original whole time without continuing expired child IO. CLI-exit OS cleanup is not claimed within-budget cleanup. No actual fault/native effects authorized.

This is a recorded implementation clarification, not a worker contract amendment or actual-effect approval.
