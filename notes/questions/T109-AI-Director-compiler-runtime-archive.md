# T109 actual link guard refuses undeclared compiler-runtime archive

- Author / worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T1091.0 / D114, one actual build allowance exhausted.
- Phase/contract: native0.4; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5 actual build prerequisite only.
- Exact clause: every actual linker input must be a fresh owned object/framework or declared current CLT/SDK file; unknown inputs refuse. T109 requires preservation/stop/question with no retry, code or pins workaround.
- Status: OPEN; MAIN resolution recorded separately.

## Question

The authorized D114-native-1 builder exited1/FAILED at link_inputs after successful actual release linking. The only unique undeclared trace file is /Library/Developer/CommandLineTools/usr/lib/clang/17/lib/darwin/libclang_rt.osx.a. Should MAIN separately inspect and declare this exact installed compiler-runtime prerequisite, then issue a NEW attempt/pins/release? No data collection, source change or retry beyond this failure report is inferred.

## Evidence and impact

Checkout /private/tmp/outbreak-clean-D113-1; sourceb984954033c85161836542463e0250ca95baf713; pinsd07f14586b528ef2587ea90918ba0a22e3d0011d1a1e5f78f03838b9adad1990; common manifestd1e199d7f0d882b3f5d470a0c85c0a6f6ecacaea5c758493252ecede45bbbc29. Both metadata hashes still match after failure.

Recorded step66, kind link, actual /usr/bin/clang++ fixed release argv, exit0,173.095ms, empty stderr, group_reaped=true and no timeout/overflow/kill fallback. Builder then reports exactly Refused: undeclared/changed/non-SDK linker input. The archive is inside CLT but absent observation.inputs, so the existing declaration gate refuses it. All16 actual fresh release objects and pre/post dependency gates completed; no debug mode or independent verifier ran.

Full trace is retained at owned logs/066.stdout,34370 bytes, SHA256b36fa8d9a49afc14950dc57d1b42332902c3583482c128407b52729daf947a54. It reports281 distinct member names of that one archive, in archive(member) form. Representative members: truncsfbf2.c.o, truncdfbf2.c.o, extendbfsf2.c.o. This is reported trace membership, not a claim that every member's code entered the final binary. Existing code already parses that record form; no generic parser/flag change is assumed necessary.

The release linker produced an unverified ac_server file,581640 bytes, SHA256fcb2d7f352805fd982c2b857ecc5f889337cb2f7bcd69c7e98a26c6b124ef47a. Binary inspection/independent verification were never reached; it is not an accepted native artifact and was never executed.

Owned root /private/tmp/outbreak-clean-D113-1/web/server/candidate-attempts/D114-native-1:

- report.json SHA256468d0a7c96b13eda75b7c510f78ebbc072e0b59c4c93bdd421443744a069cafc.
- freeze.json SHA2568f29f5052dfd54707ae6013c18e26761c8b55e2e25f943501fa81cb662f10907; all288 terminal file/directory/link members independently matched by read-only stdlib checks.
- All67 actual child records exit0/reaped; no timeout/overflow/kill fallback. Overall FAILED is the post-link guard, not a linker process failure.

## Options for MAIN

1. Inspect/pin the exact installed archive and review the complete retained actual trace for any other declaration gaps, then issue fresh authority/attempt. No generic compiler/library wildcard or hash waiver.
2. Keep the current pins/recipe unchanged and leave native build blocked at this declaration guard. Existing failed evidence remains immutable.

These are options for review, not implementation authority. No SDK/runtime archive bytes were copied, no pins/source regenerated and no D110 artifacts used or changed.

## Work stopped

Actual builder allowance is exhausted. No retry/patch/workaround, verifier/receipt, debug/link continuation, binary/server/browser/network/runtime or artifact acceptance. Own failure handoff is the only remaining reporting work.
