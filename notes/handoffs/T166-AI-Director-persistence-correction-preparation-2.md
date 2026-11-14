# T166 focused persistence-cutoff correction and preparation2

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket / revision: T1661.1, RELEASED FOCUSED SOURCE + NEW GUARDED PURE PREPARATION ONLY D237; authoritative status unchanged by worker.
- Governing: RULES_INITIALIZER_FOUNDATION0.2/D231/D237; final preflight review b758b86e61cb89ecf735ea3b1698a9e5fa5e52fe4b47dac0aafcd5d8bcece69f. Initial three review corrections remain intact; only the remaining operation-persistence blocker is addressed.
- Base / preservation: ticket base unchanged, no Git operation. MAIN's eight-file archive, original preparation-1/handoff and baseline/candidate/wrapper/runner remain immutable. Live rules913ce... and World/T161 inputs untouched.
- Changed files this stage: ONLY verify.py,test_supervisor.py,SCHEMA.md,README.md; NEW preparation-2/{pins.json,plan.json,corpus.bin,expected.bin,cases.json}, its temporary durable FAILURE (removed after successful gate), and this own NEW handoff.
- Commit / patch reference: none.

## Focused correction evidence

PASS, source only — Files.put/sync_directory/remove accept an absolute per-call cutoff and compute min(original operation cutoff,original whole cutoff). That same effective bound is checked immediately before/after open/write/flush/file-fsync/file-close/directory-open/directory-fsync/directory-close, including independent eligible close/error paths. No mutable deadline reset or fresh allowance. A late return retains original handles/primary/secondary/late facts and cannot start the next child-associated step under the larger whole deadline.

PASS, source only — Supervisor.run explicitly supplies its original min(operation_end,whole_end) for both child logs AND persist_child receipts. No whole-only helper remains on the child-persistence path. Separate persist_outer_failure uses only remaining ORIGINAL whole time and labels the private processes.json envelope OUTER_FAILURE_LEDGER; it cannot resume child cleanup, change its verdict or create a new60s allowance. Child envelope is CHILD_OPERATION, with its own original cutoff. Outer ledger after whole expiry performs no I/O. The actual exception path invokes only that explicitly named failure phase.

PASS, authored fake definitions ONLY —12 new cases use actual Supervisor AND actual Files with fake FileIO, with Files still configured whole300. Selected log steps start near59.7 and return61 beyond operation end~60; trace assertions forbid any later child I/O start, preserve original process/filesystem handle and truthful reaped/unresolved facts, and require refusal. Includes late log open/write/flush/file-fsync/file-close/directory-open/directory-fsync/directory-close; late receipt write/file-fsync; permitted remaining-whole outer ledger retaining unchanged refusal; whole-expired outer ledger refusing before I/O. Total54 finite definitions<=128. NONE executed; no mocked-case pass is claimed by this source/preparation stage.

PASS, narrow-delta static check —canonical,corpus,commands,frame_evidence,zero_init_evidence function ASTs equal MAIN's archived original verifier; no numerical/frame/command algorithm edits. Other four source files equal archived original hashes. Exact future25-child graph unchanged:18 object/assembly/link+4 version+1 fixture child+2 targets; new54 cases stay within that one future fixture child. Compiler flags/API/precision/64KiB/300s/60s/byte bounds unchanged. No numerical reaudit, old-suite replay, fake memory shim or cap waiver.

## Sole guarded pure preparation result

PASS — after inspecting the corrected source, ONE permitted invocation was observed to exit0:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/rules_initializer/candidate-1/verify.py --prepare
```

Literal destination is NEW preparation-2; guards permit only its five fixed records plus FAILURE. Original preparation-1 was never opened for writing or rerun. Durable initial refusal, explicit file flush/fsync and parent-directory fsync, bounded named stdlib-only reads and denied process/network/signal/wait/tool/compiler/SDK-copy/project-import paths remain. Five records were durably published and re-read/hashed before marker unlink+directory synchronization. Observed stdout: prepared:true,actual_proof:false,rows262,requests4192,expected7864,pins_sha256=c1744e41ab610fafaa8a9746092d846400a97daf9b34c7d440344ebea75c08d0. No retry/source edit after that terminal publication.

Exact3 factory+143 validator/mutation+116 basis=262 rows. Corpus4192 bytes/SHA25600143098f1f8c4889b14ed10011c14c9748d5f6775699fcadf118c5b48e6fdd4; expected7864 bytes/SHAb0efcfd86cb818d3de1f1f906b2783619a946cfe07a0131b9b84621ba60d65bf; cases33851 bytes/SHA620820c431803270b10fc01130a87802b25b42d0911339d0fe3a8a1217fbf8f0. All THREE match original preparation-1 byte-for-byte. Thus no response/request/family/order change or reduced proof.

Named source/data input bytes1870152, generated five-record bytes110206, combined1980358<8388608; fixed tool binaries separately streamed as named identity reads, no probing. Elapsed before final publication~0.370s within original300. Final output one small JSON summary. All120 named ordinary inputs rechecked unchanged, including16 opaque historical blobs, plus fixed tool/alias context checks. No broad SDK/unrelated-tree scan.

Historical policy: original five preparation-1 files, MAIN archive's eight sources+manifest, original handoff and final review are pinned as exact raw historical blobs, not executed or parsed for current authority/source expectations. In particular old source/authority rows continue identifying old versions and are not retargeted to this correction. New records independently bind current controls/current four source versions. Future protection graph explicitly includes old preparation/archive roots.

NOT RUN — actual fixture/compiler/link/tool/version/target/SDK-copy/project-import or installation. All invocation counters0. Future attempt-1 and supervisor-fixtures-1 remain absent. No actual deadline-boundary, frame/zero-init/output/process/terminal candidate proof or acceptance follows from pure generation. No actual REVIEW-READY/freeze claim.

## Stable source/preparation pins

Under tests/outbreak/rules_initializer/candidate-1:

- verify.py48506 bytes:8438bf98f05981f7e47dfd1a13631df761d0094dc0b8c793ca3cf72577cb763f
- test_supervisor.py36524 bytes:6acaf1f7b98b93ef21b592630131d6b61f6270ca55ab71f424c3ebf78da9c4ae
- SCHEMA.md17081 bytes:0858abfdb40aa5603105e6360ff9bbfaf478ad6e1823af9d9885176d75577c7e
- README.md4733 bytes:5bd3df83d94c70aebbeaab7fb83457f6968efcc4aa53a6f31c7d9ffd5347c568
- preparation-2/pins.json32692 bytes:c1744e41ab610fafaa8a9746092d846400a97daf9b34c7d440344ebea75c08d0
- preparation-2/plan.json31607 bytes:0fcfbfd7fe947c99fa0bb18a2332404e8b52ed2eb50855b92fca1cbb97ab5b2f
- preparation-2 corpus/expected/cases identities stated above; FAILURE absent after successful durable gate.

Unchanged protected identities: baseline full9982-byte913ce462a5c3896d766adc66751f278d188462ee6b3b97973269d976b3cf00b2; candidate full10008-byte333b6d0717fbb9b75b74aa96426f8180ad443b49c1acf5711f2a73a7c218da5e; wrapper2c917b4363d66f71a759ef7c8acd3bbfc4a00358f090ddc81c54cd8f3668d862; runner84f8646ac35f3101ec7d2c5bb347eaeabbdcb5acd78f14172491f81bd344ca2b. Original preparation-1 pins remains e8037e25ce15fae4dcfbf901eab501c250996d2bf8b358b816f4813cb66c2dda. All16 historical hashes are explicit in new inputs; no historical file edited. Live cpp remains913ce... .

## Integration and next authority

Current ticket/contract reread before handoff; still focused source+pure preparation only. Source/pins remain stable after generation; no extra candidate-root slot, fixture root, actual attempt, freeze or installation. MAIN may review this exact correction and new preparation, then separately release any actual proof. Initial durability/whole-clock/signal-restoration fixes stay resolved in source. Full unchanged T16197755-row proof and separate live installation/source-path/consumer-pin steps remain mandatory later. QA/T149/runtime/RSS/gameplay/P0/performance/full-phase/human gates unchanged.
