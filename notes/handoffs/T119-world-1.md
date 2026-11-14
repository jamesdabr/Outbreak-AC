# T119 actual pure admission validation failure handoff

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket / revision: T1191.0 / D128
- Contracts: CANDIDATE_RUNTIME_ADMISSION0.1; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5.
- Original cwd: /Users/jd1/code/apps/outbreak. Exact artifact root: /private/tmp/outbreak-clean-D120-1.
- Exact admission: clean-root notes/decisions/D128-candidate-runtime-admission.json,33057bytes; separately supplied SHA25694b6a89ff876e31551658120c395eb046877dbd460934ec99ebf55b78695bc4a.
- Expected source/common manifest: bdaa8df7ec39d9408f97feda4560832d7ef26c3c /2583d893deac6c45fd6607aa7e40447a0f3d01e0410482bcc9f4a03810ddd5bc; D121-web-1 and D121-native-1.
- Writes: NEW original notes/reviews/T119-world-actual-admission-1.json plus own new question/handoff only. No code/helpers/tests/contracts/tickets/decisions/clean-root/SDK/cache/artifact/pin/admission/history/Git changes.

## Acceptance evidence

PASS — Read T119/D128/MAIN-D128-admission-authoring.json and accepted T113 API/schema/source/helper boundary. Inspected library read-only filesystem/gates, exact fixed native data-helper import, and wrapper. Pre-effect hashes matched: admission.py65677621a0c83440024c9c569c9523ea5003751622d762657f879b46ec897565; original actually imported stage.py b13b516fb82fb80dc13a70b5ac4264d5948117f1cb637d72620ec91a33a6a313. No project package __init__.py side-effect source present along either fixed namespace import path.

ACTUAL VALIDATION FAILED — ONE API call only:

```python
validate_admission(
    '/private/tmp/outbreak-clean-D120-1',
    '/private/tmp/outbreak-clean-D120-1/notes/decisions/D128-candidate-runtime-admission.json',
    '94b6a89ff876e31551658120c395eb046877dbd460934ec99ebf55b78695bc4a',
)
```

Initial fixed child argv: /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B -c CODE, original cwd, PYTHONPATH/PYTHONHOME unset, PYTHONNOUSERSITE=1; Python3.11.9 and dont_write_bytecode asserted. Full exact CODE/argv/env overrides captured in the immutable receipt. It installed audit guard BEFORE importing the library/helper, verified both hashes again, made the single call and would require an exact typed VALIDATED_BUILD_ARTIFACTS object before emitting bounded JSON. No executable/module/root/data selection from a document.

Guard denied subprocess/socket/os.system/fork/exec/spawn/kill/killpg and all open-for-write/filesystem mutations inside child, and remained installed through exit. Parent used bounded pipe capture and deadline, reaped initial child, captured exact stdout/stderr and exclusively created the one permitted receipt. It neither reran preparation nor invoked any inspector/compiler/Node/browser/native/server/runtime/network process. Parent wrapper/metadata hashing is orchestration only; the actual admission API was invoked once.

Outer yielded session57553 polled to authoritative exit1; validation child exit1; elapsed23.892812666017562s, fault null, child_reaped true, within120s and combined8MiB. Stdout empty. Stderr retains complete traceback ending **web.runtime.admission.admission.AdmissionError: payload source entry fields**. This is the actual metadata-gate refusal, not a build or runtime failure. No partial/success admission result fabricated. Because error interrupted child output, no successful audit-summary/result object was emitted; exact active guard code is retained in receipt.

PASS — Twenty selected ordinary metadata identities before/after match, including original validator/helper, actual admission, common source/prerequisite manifests, browser/native pins/result/report/freezes/receipts, browser build metadata/four runtime files and both native binaries. No source/admission/artifact byte mutation observed. Validator internally checks current-file identities and performs no mutation; it failed before its final success stability pass, so a full successful admission is **not** claimed.

## Failure diagnosis as read-only data

Trace reaches admission.py:372 inside browser_payload, which requires every source payload entry to have exactly path/bytes/sha256/virtual_path/license/notice/provenance. Actual source-bound network-profile manifest has78 entries with that field set and ONE existing derived map with the additional `derivation` field: packages/maps/dev_outbreak_browser.cgz. Manifest173076bytes, SHA256c9ecfa62f7e4ca7111a9d3a23a9c97b906d11399d32f6f312463c6697a3359d7 matches its901-entry common-source row. The accepted fixed pack report already identifies this sole derived file/78copies/79files388791bytes. Thus observed mismatch is strict source-entry interpretation; no hash drift, corrupt actual map or newly added field is inferred.

The native gate was NOT REACHED: gate.browser raised before gate.native. Later full native checks/final all-file stability/typed result are NOT COMPLETED by this actual call. Existing D122/D128 build acceptances and prior independent verifier evidence are preserved, not rerun or revoked by this different component's schema refusal.

## Frozen evidence / implementation status

Receipt notes/reviews/T119-world-actual-admission-1.json: **14289bytes; SHA2563e8697f841add7fa99f9c198166e81a0e40b5ef45576ce1534427b768fc93a41**. Contains exact child wrapper/code/env, actual exit/output/duration/bounds,20metadata pre/post identities and false runtime/P0. Receipt read-only hash rechecked after diagnosis. It is a FAILED actual validation receipt, not accepted admission or runtime authorization. No receipt rewrite, retry, source/schema/manifest/pin/admission substitution.

Actual metadata validation attempted only. Runtime/browser/native binary/server/gateway/socket/network/Node/inspectors/compiler/signing/preparation fixtures/P0/MVP **NOT RUN/unaccepted**. No harness or test rerun. Parent/child only wrote the permitted original receipt and own notes. No authoritative status/selfacceptance/dispatch or hold change.

## Integration and question

notes/questions/T119-world-derived-payload-entry-schema.md records precise mismatch/options for MAIN. MAIN alone reviews frozen failure and selects a separately released component correction/schema interpretation and NEW actual validation. This failure does not authorize mutation of historical derivation data or gates. T1191.0/D128/component0.1 re-read before submission. Player/QA holds remain unchanged; no future runtime controller authority inferred.
