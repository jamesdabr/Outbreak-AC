# Ticket handoff — T268 REVIEW-READY

- Worker: Player /01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T2681.0/D450; BLACKWOOD_NATIVE_BUILD_PREPARATION0.3, reread before submission. Authoritative ticket status unchanged.
- Base commit/pre-existing edits: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work; no Git command. Accepted T265/pass7 and T267 failure remain intact.
- Changed files: web/server/blackwood_candidate/{stage.py,test_preparation.py,SCHEMA.md,README.md}; NEW preparation-1/plan-pass-8.json, preparation-1/pass-8/**, supervisor-fixtures-1/pass-8/**; own T268 source-diff and this handoff notes. build.py/verify.py unchanged.
- Patch reference: notes/handoffs/T268-player-source-diffs-1.md, four files against accepted pass7 snapshots. No commit.

## Acceptance evidence

PASS sole inspected guarded pass8:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -B web/server/blackwood_candidate/test_preparation.py --pass-id pass-8 --plan-sha256 62140c6a73a8f17240624b3183089eccdc8babab1e24c6fa614f4928c2e30125
```

39/39 SIMULATED checks passed in18.001404s before result publication,24,487 observed fake-output bytes before small summary,8,199,880 storage bytes before results; nine expected guard self-check denials, zero unexpected denials. Existing256cases/300s/8MiB/128MiB caps and pre-import process/network/tool/FFI/old-code guards unchanged. Original final cutoff remains checked through persistence.

Result: web/server/blackwood_candidate/preparation-1/pass-8/result.json SHA256 `f2d1a78345a3b9e6b691f6e7bf3973734979dd63d9b58f6586752468809c1331`; matching source snapshots and per-case details retained in the two pass8 roots. All six current sources match executed snapshots. Post-pass lstat check found7,062 new regular files, all readable; zero new physical mode0000 files.

Coverage: existing complete126-command/32-object/two-link fake build plus independent verifier/idempotent receipt success; all19 D446 regressions rewritten to readable files with injected metadata/read denial;19 new D450 cases. New cases exercise all133 possible allowed copy paths without content open, unknown case/index/pass/suffix refusal, file-type/size/mode/owner/group/device/link/integer/field-shape checks, consumed source/dependency promotion refusal and actual authorization failure after inode/mtime/ctime mutation. Existing202 original case names retained, all221 prior names preserved; total universe240, only39 selected as authorized. No unrelated full rerun.

## Implementation status

Implemented: literal19-case/index roster independently matched against accepted plan-pass-7 SHA256a2dfd976759128145ae861390cb98473efbd77af7e3ab8185a22aed4e0faae40; Cartesian set with only seven original suffixes, at most133 copy paths. Copy lstat rows require regular/single-link/mode0/12bytes/uid501/gid20/device16777232, strict bounded integer identities and positive inode. Actual observation/control binds inode/mtime/ctime and existing full before/after comparison detects changes. No generic prefix or PermissionError fallback. All known opaque paths remain barred from ordinary/hash/source/manifest/dependency roles. Readable hashing remains unchanged.

Original seven literal metadata records are AST-identical to accepted pass7 source. Their production mandatory presence checks are unchanged and exercised by the retained targeted missing-known case. No copy presence requirement was added; the historical missing-known test intentionally removed one copy.

New simulations create readable0644 owned files only, then inject lstat and read-denial boundaries into actual preservation/protected-inventory helpers. No old unreadable file content was read or permission changed. All original pass7 data/old observations/results and T266 launcher were left untouched. The earlier physical-copy retention issue is corrected without producing another unreadable artifact set.

Final source SHA256:

- stage.py: `6ce52a93e926e19eda78040200abd1d9970d1826e296cbb4ba12c6070119b193`
- test_preparation.py: `6163ff4624b48d1df8fdfa79da7639122933d5da2ba849f18b3cf5d84cc087bb`
- SCHEMA.md: `9b34049e3e3599d4bab11cff4ff77e41e6c9e34726cd4dff2f99ad24d8f50755`
- README.md: `3190d4359e960370149a58f5715c6c8ea0f0867fb75134adb8bbc5abbe1311d2`

NOT RUN: actual preservation/current-input collection, T267 retry, actual project plan/build/verify/tools/version/FFI/compiler/signing/framework-copy/native/browser/server/runtime/network/Git. Actual native attempt root remains absent. Opaque content verification remains explicitly unavailable; simulations do not establish actual native/tool/ABI/runtime compatibility.

## Integration and questions

No remaining targeted-check failure, new dependency, asset or shared engine interface. Private preservation policy changes only as D450 authorizes. MAIN can review and separately release a fresh current-input observation against this updated source and stable T266 launcher, then form the concrete native build control/command. No actual observation or execution is released by this handoff. Stop at REVIEW-READY; no live process handle remains. QA/T149 and other holds unchanged.
