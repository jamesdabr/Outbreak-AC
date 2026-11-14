# T161 appended hard-deadline correction preparation

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket / revision: T1611.1, still RELEASED NARROW CORRECTION PREPARATION ONLY D220; worker changed no authoritative status.
- Phase / contract revisions: isolated SPREAD_CONE_FOUNDATION0.2 / D214,D220 and MAIN's follow-up correction review.
- Base / pre-existing edits: same ticket base, no Git commands. Prior delivered fixture-pass-2, pins and handoff preserved unchanged; current three editable files backed up in the new namespace before correction.
- Changed files: verify.py,SCHEMA.md,README.md; NEW preparation-2/deadline-correction-3/**; this own new note. Production sampler/header/wrapper/runner and accepted dependencies unchanged.
- Commit / patch reference: none.

## Acceptance evidence

PASS, preparation/static/mock only — immediately before cleanup SIGKILL, the new code checks one fresh monotonic observation against original operation end and whole deadline. Expired means kill_skipped_expired=true,unresolved=true, explicit secondary refusal and NO mutating signal. Original deadlines/reserves remain; independent closes still execute. Reap retains its original-end reserve check, so no fabricated positive grace/new wait after hard expiry.

PASS, mocked only —20 exact-current-supervisor scenarios, including two new postspawn HARD-expiry cases. Fake Popen returns at time61 (beyond operation hard end~60) or301 (beyond whole300). Both produce0 signals of ANY kind,0 waits, closed acquired stdin/stdout/stderr, no success, returncode=null,original_handle_reaped=false,kill_sent=false,kill_skipped_expired=true,unresolved=true,absence_observed=false. Prior active-timeout59/end60 remains distinct and correctly permits bounded owned-group cleanup. No actual kernel/process behavior is claimed by these mocks.

PASS — only nested run executable AST changed versus this namespace's preserved pre-correction verifier. Header identity handling, response/corpus/commands/frame analyzer/precision/caps remain unchanged. Existing pinned pure corpus/oracle/command/frame plan artifacts were reused read-only; NO corpus families regenerated.

PASS — original complete failed attempt-1 hashes/identity/timestamp inventory matches; prior terminal11 files remain unchanged; four production/header/wrapper/runner pins retain original bytes; attempt-2 absent. Historical pins' current-source rows continue identifying their historical versions, preserved by the new baseline, not asserted to identify corrected live files.

NOT RUN — actual verifier, compiler, native/Wasm targets, SDK/sysroot copy, actual compiled-frame/timing/output acceptance. This correction stage actual_driver_invocations0,actual_children0,actual_signals0,actual_waits0,actual_compilers0,actual_targets0,sysroot_copies0. No final freeze or actual REVIEW-READY-result claim.

Inspected preparation command, exit0: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/spread_cone/T161/preparation-2/deadline-correction-3/check_deadline.py`. It AST-selects exact current supervisor/guard definitions and reads previous mock definitions as data; it does NOT run old preparation or actual verification entrypoints. Real launch/signals/waits/network/ctypes are denied. Its output path is occupied historical preparation; do not rerun into it.

New evidence root: tests/outbreak/spread_cone/T161/preparation-2/deadline-correction-3/. Contains baseline/{verify.py,SCHEMA.md,README.md}, baseline-identities.json, previous-terminal-identities.json, check_deadline.py, supervisor-fixtures.json, preparation-result.json, correction-plan.md and pins.json. All22 pin rows were rechecked unchanged immediately before this handoff.

SHA256:

- pins.json:7dfa79731e66e5bc1a12549d4e72308f2516ab059dd0988c028540e71762e0c7
- preparation-result.json:baf40da0c8f7805e9f5ae247702f0b9dcfa0b8b74603a14c19cfd094224dddb0
- supervisor-fixtures.json:4629e1053fb2f8cb540cfe25a174172850c43feabcc32cd2b000c59e456bec3d
- correction-plan.md:35677b828a7a1e6f4ec2bcd80b9e07aac609857f57250e547ce4286cbb2e22df
- verify.py:681d035a0ec61f7a623c683a44a4911d886de6d06eefa57df01a0889f880675b
- SCHEMA.md:6b80569df6b5fabd12ec991da2f89cb5a043fee6a73dd0ea219e59f5d0768818
- README.md:f0386f29a046eafb4da95244a6101ac4868dee594889069c2f049a4d5884dfff

## Implementation status and limitations

Harness deadline seam corrected with mock/static evidence only. A real kernel spawn/setup call can stall past its deadline: after it returns expired, the code reports the original unreaped/unresolved handle instead of initiating late termination/reap or claiming cleanup/hard-real-time OS control. Independent closes and partial retention remain best effort and late evidence cannot create success. Production math and all actual native/Wasm/frame/timing obligations remain at their prior unverified status.

## Integration and next authority

Current ticket/contract reread before submission. No mathematical/API/interface/dependency/corpus/cap/integration changes. MAIN may review this new stable correction and separately clear one actual literal attempt-2 invocation. T1611.1 still says “NO fresh actual driver/compiler/target execution until MAIN clearance”; stopping at that explicit gate. QA/T149/runtime/RSS/full-phase/human holds unchanged.
