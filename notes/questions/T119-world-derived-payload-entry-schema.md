# T119 actual admission rejects the existing derived-map entry field

- Author / worker: World/Match-Systems
- Ticket / revision: T1191.0 / D128
- Contract: CANDIDATE_RUNTIME_ADMISSION0.1; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5
- Exact boundary: ONE actual validate_admission call, failure preserved with no retry/source/schema/metadata workaround.
- Status: OPEN (MAIN resolution recorded separately)

## Question

Should MAIN release a separately reviewed admission component correction for the exact existing derived-map entry schema? The actual accepted network-profile manifest has78 copied entries with the seven expected fields and ONE derived map entry with those fields plus `derivation`. The current pure validator requires exactly seven fields for every entry and refuses the admitted real data. This ticket does not authorize a library or metadata correction.

## Evidence and impact

ONE fixed guarded validation from original cwd failed exit1 after23.892812666s with `AdmissionError: payload source entry fields`, at admission.py:372. No success object returned; native gate not reached because browser gate raised first. Captured traceback/code/environment/source/admission/artifact identities are frozen in notes/reviews/T119-world-actual-admission-1.json,14289bytes, SHA2563e8697f841add7fa99f9c198166e81a0e40b5ef45576ce1534427b768fc93a41.

Actual clean-root web/assets/network-profile/manifest.json:173076bytes, SHA256c9ecfa62f7e4ca7111a9d3a23a9c97b906d11399d32f6f312463c6697a3359d7; exact size/hash is bound by the unchanged common source manifest.78 entries have fields bytes/license/notice/path/provenance/sha256/virtual_path; packages/maps/dev_outbreak_browser.cgz additionally has derivation. The existing accepted pack report already explicitly identifies this sole derived file,78 identical copies,79files/388791bytes and two changed header fields. This is not an observed artifact byte drift or malformed-payload conclusion.

Child audit guard was installed before fixed library/helper import and retained; it denied subprocess/socket/process-control and all file/filesystem mutation effects. Parent capture remained within8MiB/120s, reaped child and exclusively wrote only the permitted original receipt. Twenty selected source/admission/manifest/pin/build artifact metadata records match pre/post. Source/helper expected hashes match. No inspectors, preparation rerun, native/browser/server/Node/network/runtime launch, artifact edits or retry.

## Options for MAIN

1. Release a narrowly tested successor pure component accepting only the exact approved derived-map field/schema while preserving unknown-field rejection for copied/other entries and all digest/source/derivation/payload gates.
2. Review a different explicit schema interpretation before any successor validation. Do not strip the historical derivation field, rewrite accepted manifests/admission/build evidence or waive current schema checks in this failed invocation.

## Work stopped

T119 actual call is terminal and not retried. Original receipt/source/helper/clean root/admission/artifacts remain unchanged. MAIN alone reviews failure and releases any preparation correction plus separately pinned new actual validation. Runtime authority/P0 acceptance remains absent; Player/QA holds unchanged.
