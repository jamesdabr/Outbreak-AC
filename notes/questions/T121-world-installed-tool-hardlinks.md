# T121 installed fixed tools conflict with universal single-link admission

- Author / worker: World/Match-Systems
- Ticket / revision: T1211.0 / D131
- Contract: CANDIDATE_RUNTIME_ADMISSION0.2
- Exact clause: no hardlinks for ordinary roles versus actual reviewed fixed installed tool inputs; no worker policy change permitted.
- Status: OPEN (MAIN resolution recorded separately)

## Concrete static incompatibility

Actual accepted native pins declare /usr/bin/clang, /usr/bin/clang++ and /usr/bin/otool as fixed tool roles/current input files. All three lstat as ordinary0755 files,118928bytes, current SHA256179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818, matching their accepted declarations. Each has st_nlink78 and shares inode1152921500312571586. No aliases were inferred merely from equal content; this is direct lstat metadata.

Frozen T113 admission.py:132 and current available T120 admission_v2/admission.py:137 require st_nlink==1 in _FileSystem.ordinary for every file. The native authorization input loop calls record -> ordinary on all2197 declared inputs, so these actual installed tools conflict. Native pins SHA25632e5b59380018be22a085ededb1bdcee83c3bdc283292351a35a22a64fd5b23d. T113 source65677621a0c83440024c9c569c9523ea5003751622d762657f879b46ec897565; current successor936a6e724da56fcd2f53f056c859c3ea0e44444a23c97cbc85b8c1fd06fa3ada. Both retain the same guard/input path. Known sole map derivation issue is separate and already assigned T120.

This is a new consumer/admission-policy compatibility conflict with actual accepted system metadata, not a malformed candidate/source/artifact observation. Admission0.2 itself states the universal no-hardlink rule, so the worker cannot silently call this an implementation-only waiver. No actual validator was called in this audit; static guard evaluation establishes the mismatch but not a new actual failure receipt.

## Question / options for MAIN

1. Record an explicit narrow policy/role interpretation for these exact installed system launcher paths and review a separately released consumer correction, preserving strict single-link rejection for project/artifact/log/cache roles and all current hash/ordinary ancestry checks.
2. Retain universal rejection and identify a separately authorized compatible tool/input strategy. No system copy/repair/chmod/unlink or pins/artifact rewrite is performed here.

## Work boundary

Continue independent authorized read-only remaining-format audit; this note grants no code change, dispatch, validator retry or runtime. Source/SDK/tools/artifacts/admission/prior evidence remain unchanged. MAIN alone chooses amendments and sends scope to the component owner. Final T121 report will recheck current successor and pin reviewed identities.
