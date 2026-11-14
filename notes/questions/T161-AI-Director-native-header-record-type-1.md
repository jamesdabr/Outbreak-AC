# T161 preflight record-type failure and fresh-attempt disposition

- Author / worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket and revision: T161 / 1.0, RELEASED; status not changed by worker.
- Phase and contract revision: isolated SPREAD_CONE_FOUNDATION0.1 / D214.
- Exact clause affected: contract's accepted native SDK identity and “preserve failure/occupied attempt, no automatic retry”; ticket's fresh attempt-1/** lease.
- Status: OPEN (lead resolution is recorded separately).

## Question

Please dispose of the preserved preflight failure and authorize the exact record-type correction and any fresh output slot through the appropriate ticket/contract revision. No automatic rerun or occupied-attempt edits were made.

## Evidence and impact

After MAIN reaffirmed T161 following completion of the direct-human-requested read-only AI review, the worker created the two new pure source files and the five allowed harness/docs files. The only actual driver invocation was:

```
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B tests/outbreak/spread_cone/T161/verify.py
```

It exited1 after0.22616874997038394 seconds, before any child spawn, compile, target execution, sysroot copy or corpus generation. `tests/outbreak/spread_cone/T161/attempt-1/failure.json` SHA256e18377e518a791e26cfba3a41557ed2ba369513c7fdbbb1994725f1400a4a347 contains processes[], combined_child_bytes0, no secondary errors and the misleading first error “Accepted native header changed: /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/pthread.h”. The empty owned logs/tmp/node-cache/module-cache directories were reserved before preflight; no original cache/tool/source/evidence was changed.

Root cause is a NEW verifier bug, not demonstrated SDK drift: while reading historical dependency JSON as data, the verifier compared `sha(Path(name))` indiscriminately with each recorded value. Both accepted T154 and T157 dependency records store this header as the opaque link record `symlink:pthread/pthread.h`, not a SHA256 string. Current resolved referent is `/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/pthread/pthread.h`, SHA2569d621c730d1d96b600893b0e3e4c45822a24d565e7b6b166973c41a6a2eb02e7. A separate read-only standard-library record-kind comparison over the781 native-header rows in the two historical dependency maps found2 symlinks and ZERO changed records. No old driver/import or compiler was invoked for that diagnosis. The initial chat claim of a changed installed header was explicitly corrected immediately after this diagnosis.

Prepared files retained unchanged after failed attempt (SHA256):

- source/outbreak/p1_spread_cone.h:5a3d7be39ff47205f8a172ec22ba4645451bb7d484f8a42791296f9b08475be9
- source/outbreak/p1_spread_cone.cpp:f7eb32f1a52a657fd6d8839c46dc69d7258bb27b44ab3afc172ba4f0d038bdb8
- tests/outbreak/spread_cone/T161/verify.py:eb9b53e87e0f3170b11295333fa06f92349ccc20356a1d98dde18ce488b42add
- tests/outbreak/spread_cone/T161/wrapper.cpp:f76a2ea2e2db4cae39c73490aae1d2013de7349a10eec4b58e1dd21486ebcef6
- tests/outbreak/spread_cone/T161/wasm_runner.mjs:e163696f44133538ee896e7214c56a65890348103953dddc1241c2170544ab79
- tests/outbreak/spread_cone/T161/SCHEMA.md:e39143a86cea7e28c13ac60ee34c73521c89a92ae4f008afca1b229c3a27c3e1
- tests/outbreak/spread_cone/T161/README.md:a6bdcc3baf1f0b65ad719f45c654299fbed7ce8d476b6222b6247775befafb44

The code implements only the two adopted pure APIs, refined N at four sites, immutable accepted dependencies, staged outputs and the source nonzero/width/work ledger. The harness is prepared for the full required union, exact32-byte responses, bounded child ownership/cleanup and complete same-O2 diagnostic frame closure. These remain SOURCE PREPARATION, not passing compilation/corpus/oracle/frame/timing evidence. Python syntax parsed; no native/Wasm criteria are verified. No REVIEW-READY or freeze claim.

## Options for owner and lead

Recommended: retain attempt-1 as failed; re-release a narrowly scoped successor allowing correction of native-header identity handling to compare ordinary hashes versus opaque link records by kind, bind referent identity explicitly where consumed, and authorize a new exclusive attempt slot. Keep all case/byte/time/precision/frame limits and the original production API unchanged. Review other preflight paths before that one authorized invocation. Do not reuse or overwrite attempt-1.

Alternatively return the prepared implementation for static review before releasing any successor execution. Neither option authorizes legacy AI fixes, QA/runtime, old-suite execution, source/tool/cache changes outside this ticket or broader integration.

## Work paused

Affected: further T161 harness edits/execution and any REVIEW-READY/freeze submission pending MAIN disposition of the consumed attempt. Source preparation and failure evidence are preserved. There are no independent released legacy AI fixes; that human-requested review remains delivered. Current T161 ticket/contract were re-read before this note and still specify attempt-1 only/no automatic retry. No source/interface/authority edits made after failure; QA/runtime/RSS/full-phase/human holds unchanged.
