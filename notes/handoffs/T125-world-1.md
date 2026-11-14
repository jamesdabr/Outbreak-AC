# T125 accepted-v4 actual pure validation handoff

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket / revision: T1251.1 / D137; admission0.4/D134; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5.
- Scope: ACTUAL_PURE_VALIDATION_ONLY through MAIN-accepted corrected v4. No runtime/controller launch authority or phase acceptance.
- Writes: NEW original notes/reviews/T125-world-actual-admission-1.json and this own handoff only. All code/source/test/schema/helper/SDK/cache/clean-root/artifact/admission/pin/history/Git files readonly.

## Acceptance evidence

PASS_ACTUAL_METADATA_ONLY — Read T1251.1/D137 and inspected exact frozen v3-to-v4 diff, API/helper import and fixed invocation. Accepted v4 explicitly routes compiler dependency reads through strict single-link checks and retains that context for final rechecks. No component/preparation tests rerun. Exact source/helper hashes verified before import and after actual validation:

- Original web/runtime/admission_v4/admission.py:70323bytes; SHA256ab7f866a9a6bbaa1c9b22e95a4aba1ac7d952303e315686cac4cead579398383.
- Actually imported original web/server/candidate/stage.py:SHA256b13b516fb82fb80dc13a70b5ac4264d5948117f1cb637d72620ec91a33a6a313.

Exactly ONE call through the literal accepted module, original cwd /Users/jd1/code/apps/outbreak, fixed /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B -c CODE:

```python
from web.runtime.admission_v4.admission import validate_admission
result = validate_admission(
    '/private/tmp/outbreak-clean-D120-1',
    '/private/tmp/outbreak-clean-D120-1/notes/decisions/D128-candidate-runtime-admission.json',
    '94b6a89ff876e31551658120c395eb046877dbd460934ec99ebf55b78695bc4a',
)
```

Fixed complete CODE/argv/cwd/environment is preserved in the receipt. Python3.11.9/dont_write_bytecode asserted; PYTHONPATH/PYTHONHOME unset, PYTHONNOUSERSITE=1. No fallback, dynamic module/version selection or document-selected executable/data. Guard installed BEFORE fixed library/helper import, retained through output/exit, denied further subprocess/socket/os.system/fork/exec/spawn/kill/killpg and write-capable open/filesystem mutation effects. Parent only supervised/captured the initial fixed child and exclusively wrote the exact allowed original receipt.

Yielded session29300 polled through authoritative completion: outer/child exit0; fault null; child_reaped true; elapsed44.18137345800642seconds, within120s. Stdout736bytes, stderr0bytes, within combined8MiB. No timeout/overflow/retry. Child audit reports denied_events[], installed_before_library_import true, retained_through_output true, writes/further processes/sockets allowed false. No inspector/compiler/Node/browser/native/server/network/runtime command ran.

PASS — Exact typed API result, independently required by trusted wrapper before successful output:

```json
{"schema_version":1,"kind":"VALIDATED_BUILD_ARTIFACTS","repository":"/private/tmp/outbreak-clean-D120-1","source_revision":"bdaa8df7ec39d9408f97feda4560832d7ef26c3c","browser_candidate_id":"D121-web-1","native_candidate_id":"D121-native-1","browser_bundle_id":"1e12a233072374531554ebb5309e307064df7f8b3588c72714abd82e77bf9e66","admission_sha256":"94b6a89ff876e31551658120c395eb046877dbd460934ec99ebf55b78695bc4a","runtime":false,"P0":false}
```

PASS —22 selected metadata identities byte/mode/size/hash identical before/after, covering accepted v4/helper, unchanged D128 admission, common/prerequisite manifests, both build pins/result/report/freezes/receipts, browser metadata/four runtime files, both native binaries and original T119/T123 receipts. Common source manifest2583d893deac6c45fd6607aa7e40447a0f3d01e0410482bcc9f4a03810ddd5bc unchanged. API completed its own current-input/dependency/payload/command/receipt/terminal-tree/alias checks and final stability rechecks; no historical whole-root verifier/baseline rerun or rewrite.

## Frozen receipt and preserved history

notes/reviews/T125-world-actual-admission-1.json: **16022bytes; SHA25635da0c37b31a3fd6e929b999f35d1e4a0a35be69972838810aa614f393f095a5**. Exact child wrapper/code/env, actual exit/output/duration/bounds/audit,22pre/post identities and false runtime/P0 are retained. Read-only receipt digest/invariants rechecked after completion. Validation evidence acceptance by MAIN remains false pending review; controller_authorized:false. D137 component preparation acceptance is recorded separately from actual validation evidence.

Old T119 FAILED receipt unchanged at3e8697f841add7fa99f9c198166e81a0e40b5ef45576ce1534427b768fc93a41; qualified T123 REVIEW_CONFORMANCE_ONLY receipt unchanged at170ecabcade557009ce067ed8901bab2a59c5f67579b1f588822c906c22f1077. Neither prior invocation was retried, relabeled or overwritten. Earlier frozen source/packages/evidence untouched; this is the separately released accepted-v4 actual call.

## Implementation status and integration

Actual pure current-file/build-artifact admission validation completed through exact accepted corrected v4. **NOT RUN/unaccepted**: controller integration/run, browser load/render/input/audio/model/runtime, native binary/server/gateway/network/service, gameplay/authority/multiplayer/performance/P0/MVP. No preparation/fixture/map-decoder/Node/compiler/signature inspector/Git invocation, source/caller/controller edit, metadata regeneration, dispatch/status/contract/selfacceptance or launch token.

No unresolved T125 question. MAIN reviews this exact receipt before any separately released controller/runtime integration. Public API success establishes reviewed artifact identities only, not effect authority. T1251.1/D137 re-read before submission; receipt/handoff frozen. Player/QA holds unchanged. Stand by; no additional validation or runtime inferred.
