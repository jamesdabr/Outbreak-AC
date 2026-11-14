# T1901.4 — D343 negative-half source correction

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket/revision: T1901.4, D343 SOURCE CORRECTION ONLY.
- Governing: CAMERA_FOUNDATION0.8; D343; complete independent review
  notes/reviews/T205-found-certificate-variants-review-1.md,
  SHA2567b45f3b96a91930bf199c65c59275a1401e92c2e2e155b5dc9d8c42c8ad59266.
- Status: **SOURCE CORRECTION SUBMITTED FOR MAIN REVIEW;
  NOT_COMPILED / NOT_EXECUTED / NOT_ACCEPTED.**
- Base: prior submitted T1901.3/D334 six-source snapshot, handoff4.
  Pre-existing project changes were preserved; no branch/commit/reset or mutation.
- Changed existing files ONLY: own release-1/verify.py,SCHEMA.md,README.md.
  NEW own notes: this handoff and negative-half-correction-5.diff.md.
- Ticket1.4 and foundation0.8 re-read before submission; no revision change.
  MAIN's awareness message about D345/T206 adds no source lease and was not
  used to expand this work. All three T206 notes remain immutable.

## Stable exact diff and identities

[Focused three-file unified diff](T190-AI-Director-negative-half-correction-5.diff.md):
21101 bytes, SHA25635b45bf9840b1225eec4925ed4629b61f916f58b7d2da977afac6c9423be044f.
It compares complete captured pre-edit texts with the final three source texts,
using three context lines. Pure textual comparison only; no source parser/import.
verify.py4 hunks,+130/−1; SCHEMA2 hunks,+59/−1; README4 hunks,+43/−6.

| File under tests/outbreak/camera/release-1 | Before SHA256 | Final bytes / SHA256 |
| --- | --- | --- |
|verify.py|995b2e282395d31eb6314219078225cd915e83eb40cd5a23993fb0bd66c2adf1|181597 / 5ea196f154ba633a2cebd9b837e82e8d5cbb86dbcdf69d4d530e42cbc19e071f|
|SCHEMA.md|516d2948bf92d0feea684b3a95e29155bbe98ea7fd4a851e696e382dfea45342|30348 / 94eea519872e8154234b8e32f582ce91916f1787d19c638cfcab78c5590ce587|
|README.md|99f2274b0505e83f8b7fc8dda60b00dd97961d3c1290aa15a24eaa84a9c2af99|23767 / d5b393ee3b466c9d0e401a626b18ea92ec2b5a7f112d5e6aac221e4c02fa570b|
|oracle.py|UNCHANGED|28921 / ca3febabfdcec5529c2aa4269b52fd1902b7b871a743f27a8594f3c4fb97dde6|
|wrapper.cpp|UNCHANGED|23324 / 80a85a84735d8b2162c04cbeff2e94598d2926f58db28b65e56741b5a10ae8e1|
|wasm_runner.mjs|UNCHANGED|6312 / 73420633781ae98355714d015a1f5f0a9607e586cf1d44c8dc82a30061c82732|

Final six-file package294269 bytes. Production camera remains
9cdb0bf7cae943812f3ff84616adbf18caf67445165ff8998918004be664748a,
sole headerf3ab259fed5172a7763b6c85ebf873e0f1f0d501b4aaf204b2dd6f6639732174.

## Exact adopted32 inputs

Only2592+4*i+2*s+p,i0..7,s0/1,p0/1. Original F1/Pistol,pitch−428,
EyeZ8192,actors0/boxes0,revision1,canonical unpatched rules/table and
complete original poisons remain. For i0..3, yaw32768,
Eye=(33894+1024*i,62236,8192), D=(−1280,6127,766),
first=priority World196611/zoneNone,normal(0,−1073741824,0).
For i4..7,j=i−4,yaw49152,Eye=(3300,33894+1024*j,8192),
D=(−6127,−1280,766),first=priority World196608/zoneNone,
normal(1073741824,0,0). Both original stances:
Crouch3738/3174/footZ5018; Standing5325/4608/footZ3584.

All share L06305,k22479607,qf2060911351,qs2038431744,
true root2940/6127,clampedfalse. Selected baseX/rotatedY displacement
product−2609192632320 divided byQ is exactly−607.5.
Ties-away displacement rounding gives−608 THEN integer Eye addition:
33286/34310/35334/36358. Rounding the positive absolute half instead gives
33287/34311/35335/36359. Source explicitly checks that one-unit discrepancy.

Both bodies are BODY_FEASIBLE, not scalar-only. Their foot/top floor/ceiling
gaps are5018/7628 or3584/7475; minimum XY radius1126 gap2174.
Numeric feasibility does not prove runtime living/observer/caller eligibility.
Metadata retains runtime source authority NOT_PROVED.

## Bounded certificate and serialized coverage

The new negative_half_certificate supplements the ONE existing complete
independent oracle observation; its response remains the full expected160 bytes.
No constructor-derived complete camera output or target output is substituted.

The source checks exact row/default/context/poison/stance association;
four named accepted angle entries and normalized basis; original full-sum rig;
length/backoff/nonclamped q/qs; own rational root2940/6127;
floor-Q32 remainders2663/3464 and exact singleton gap[2940,2940];
complete actual first=priority World/None/normal/feature; selected negative
half coordinate in the full camera response; physical358 safety, original
projected margin and both original poison guards.

Complete original F1 exclusion uses the fixed uniform F1 source construction
and existing one-decode fixture/summary. Whole-segment floor/ceiling gaps
7832/7066 exclude every cell face/edge/corner. Five other outside planes
have positive full-segment gaps; selected target alone closes2940 at6127.
Actors/boxes are absent. Therefore no other physical obstruction can enter
the earliest or anchored11 priority set. Conservative closed swept XY bounds
span3x4 tiles (4x3 rotated), at most12cells/pass. This is mathematical
enclosure, not measured source/emitted work or accepted G2 behavior.
Only fixed scalar/rational/field loops, six outside gaps and two tile bounds
are added; no second decode/map traversal/sweep/root stream/search occurs.

Coverage binds the ACTUAL decoded serialized32 requests to i/s/p, eye/foot,
aim/stance/Pistol/F1/default/context/patch fields and successful certificates.
Decoded field names were checked against the read-only oracle source.
No oracle/control/generator was invoked.

Pure text section comparisons returned unchanged for D321/D325/D334 literal
tables; D325 row helpers/fixture+identity routines; D321 qk1 routine and
stratum11 mapping; D334 tangent routine/stratum4 mapping and previous coverage;
D325 previous coverage; and the whole publication/control/94-operation region.
The only construct_row change is the former negative-half gate.
The shared semantic dispatcher only gains the D343 supplementary check.
All other rows, unresolved seams, 4096/64/94 and original caps remain.

## Validation, preserved notes and limits

- SOURCE INSPECTION COMPLETED: complete adopted review/decision, exact32
  mapping, supplementary checks/docs, stable textual diff/section comparisons,
  ordinary sizes/SHA256, final ticket/foundation revision readback.
- NOT RUN: parser/AST/py_compile/import; own/project/helper/control/oracle/
  fixture/corpus/generator/preparation; compiler/link/SDK/FFI/query/Node/
  native/Wasm/browser/network/runtime, target/frame or performance verification.
  No setup/request/golden/control/result/preparation/attempt/final root created.
- Boundary deviation: one read-only pwd/Git status inspection was issued after
  context restoration before rereading the restrictive ticket. It changed no
  Git/project state; no further Git command or source execution followed.
- No production/header/authority/evidence/old-note edits, dispatch, new fixture/
  row/control/dependency/asset/interface or unrelated correction.

Readback confirms all three immutable T206 notes:
proposal a6e570646fdcf1fe1be8c7b64aacbe72269b9c0c07da28b5e2ea8455e258d4ed;
question19b1dcb6ebcd17176ad90ffb6814ceb4018da80c135eab27f512f3ae0586305e;
handoff994769d2b60f4ede1d70550b12210072dedf17007283f1a77c6e4da4edf26348.
Their separate D345 mathematical acceptance supplies no further source scope.

No complete source/catalog/realG2/currentG1/frame/caller/browser/gameplay/
human/full-phase acceptance is asserted. Other construction/source/protection
seams remain. Source-only work does not establish runtime behavior.
No new question or out-of-scope source change was needed.

Stop for MAIN review of this exact diff/handoff/source snapshot. No automatic
correction, preparation, execution or subsequent source lease follows.
