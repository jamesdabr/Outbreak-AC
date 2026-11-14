# T095 original prerequisite package handoff — package PASS, stager defect retained

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket/revision: T0955.22, PREREQUISITE_PACKAGE0.2 / D092,D094; candidate shared source rules D091, GOV/BROWSER/P0 0.5. Ticket/contract re-read before source freeze/actual operation. No self acceptance/status/phase changes.
- Base:13f0d8eea4822dee5c976661218d022be74342e3 plus preserved overlay. No commits/reset/revert/dispatch.
- Changed only NEW web/repro/package_prerequisites.py, stage_prerequisites.py, prerequisites.json, own tests/prerequisites/**, prerequisite-bundles/T095/**, own T095 questions and this handoff. Main README/source-input manifest and all old SDK/cache/production/tests/artifacts read-only.

## Acceptance evidence

PASS — Standard-library standalone fixed-root producer/stager, no project/SDK/
compiler/manager/Node imports or execution. Producer CLI --create only; stager
--bundle ABS_PATH --manifest-sha256 EXPECTED_SHA only, no root/output/SDK/command
hooks. Strict duplicate-JSON/types/unknown-fields/digests/schema/path/member/size
checks, canonical tar/PAX/gzip bytes, no links/hardlinks/specials/case collisions.
Both public CLIs deny process/network and non-owned writes with audit boundaries.
Known stager report-parent guard defect is reported below, not waived.

PASS — SDK7.0.0/compiler revision777e6e5db7b4990bcaeb1b9998ed642cc84e6629,
actual Node24.19 hash27db838.../compiler+tool alias target hashes, D044/D046 exact
approved alias chains/supporting files, six ordered retained source archives and
recipe identities verified through accepted static metadata. No SDK selection,
acquisition, activation, compilation or shell/installer hooks. Existing compiled
SDK/sysroot/port dependencies are prerequisites, not game object reuse.226Wasm
port objects match fixed port build roots and retained source basenames,
including two SDL2_image Objective-C objects. Six source archives/licenses and
seven accepted SDK/port notices preserved/hashed; no new license interpretation,
relicense or public redistribution claim.

PASS — D094 original-mode question resolved before actual packaging. Private
source-before.json/source-after.json fully record every original raw file/mode/
size/hash/directory; equal SHA256
69725560d2e91648b3b41294492a8cd4c2fa01e0dca962fe9027a6149153bd79.
Source5956files/782directories/203069184ordinary bytes. Package-only mapping:

| Raw source mode | Entries | New package/staged mode |
| --- | ---: | --- |
|0644|5396|0644|
|0755|819|0755|
|0600|224|0644|
|0664|261|0644|
|0775|38|0755|

Other modes reject; directory searchability retained. No original-cache chmod,
entry omission, replacement, unlink, SDK/global-cache mutation or source change.

PASS —17pure fixture groups under conspicuous FIXTURE_ONLY fake SDK/data roots,
process/network effects and even real-SDK access denied by audit hook. Valid
archive+manifest determinism, canonical normalized roundtrip/raw-mode
preservation, long Unicode/PAX, wrong source/code/SDK/Node/recipes/aliases/notices/
provenance, strict JSON/path/type/hash/size/overflow/member/case/link/special/
PAX/CRC/ISIZE/truncation/trailing, no-overwrite/existing cache/linked ancestors,
late source/bundle/manifest mutation and owned partial-failure preservation.
Independent stdlib archive reviewer also fixture-tested. These are invented
fixtures, not actual SDK/cache staging proof.

Preserved fixture/preflight findings — First denied04755 fixture assumed chmod
retained setuid; filesystem returned0755. Failed logs/trees retained; synthetic
stat test models forbidden mode without policy bypass. Read-only port preflight
found the private .c.o-only check too narrow for two valid IMG_ImageIO.m.o files;
corrected before source freeze to retained-source-backed port .o/Wasm evidence.
Original/derived/final fresh preflights remain; final preflight3 checks all226.
Optional installed-source observation14matches plus2absent installer-only files
is documented against D005's binary-SDK/bootstrap-bypass recipe; no repair,
installer dependency or alternative SDK inferred.

PASS — Producer/stager/private receipt schema and17-group source-bound fixture
receipt frozen BEFORE real manifest existed. source-checkpoint.json SHA256
26177ee675cef16192afbfc712e28001780edd1e50b1d72bed390130ef7562c0;
source-freeze.json175a5959c5005e118755a3933d137c6e8493ed503599eab7d0730927b7d36d5d.
Producer code63a6b83ad63b2fbc1924053587d1fdd90892fb119931ba7fc03b592b6ade6d64;
original stager3519ebccad7f7afb8c5f72761e576a237bf6632520ab7d63cbaeeee676462f4d.

PASS — ONE actual inspected command:
`python3 -B web/repro/package_prerequisites.py --create`.
Exit0; compression8.359028s<=120; complete11.672955s<=180. No automatic retry.
Archive61535814bytes,6738members/203069184expanded bytes within512MiB/100000/
1GiB. Sorted ordinary records only; uid/gid0, empty uname/gname, mtime0, empty
gzip filename/mtime0. Manifest exact schema1 binds original producer/stager,
SDK/aliases/ordered six ports/cache/member/provenance identities, without a
self-referential source commit.

PASS — Independent read-only verification imports no producer/stager/SDK code;
uses stdlib tarfile/gzip/zlib and compares EVERY tar byte/member/mode with original
cache and manifest, six archive SHA512s/recipes/provenance,40PAX members, strict
single gzip CRC/ISIZE/EOF and9728zero tar-tail bytes. Full original raw inventory
still identical. No extracted real cache written. Receipt
independent-real-verification.json SHA256
9fad9c9789e8a8c4a0ef069a41aba5fe8466b1694a6c1e6e53408be3d6481337.

FAIL / FOLLOW-UP REQUIRED — Fresh-checkout public CLI audit guard rejects
mkdir of missing web/repro/prerequisite-bundles parent while creating T095 report
hierarchy. Existing roundtrip fixtures first created a fixture bundle, so they
precreated that parent. Post-freeze tiny fake-root diagnosis confirms ValueError
before cache/report effects. Package bytes remain valid; source/manifest left
frozen, no silent correction/repackaging. Question
T095-world-clean-stage-report-parent.md recorded. MAIN separately releases
T101/D101 after this original handoff; that successor will own narrow fix and
explicit manifest stager-hash rebinding. Do not interpret this as stager-ready
acceptance.

NOT RUN — Actual staging into ANY real .cache, clean source commit/source-input
manifest, fresh browser/native build, compiler/SDK/Node/process/network/services/
browser/game runtime, deploy, complete P0/MVP. Actual stager stays NOT RUN pending
separate clean-build execution release, even after any T101 fixture/source fix.

## Original frozen identities / review

Original public manifest:
web/repro/prerequisites.json SHA256
ca805d345d7f17c451e89f6d25e02b8e7cc44ac04b7928abf03078237d12c92d.
Exact bundle:
web/repro/prerequisite-bundles/T095/ports-emscripten-7.0.0.tar.gz SHA256
2878a16023019e008b909e2730556de587c51041190e32656366cc53ee72d120.

Original producer, stager, public manifest, fixture source/selection, reviewer,
schema and top-level test logs/failures/observations/authority snapshots are
preserved under frozen-original/. Future authorized live source/metadata changes
must be reviewed as successors, not used to rewrite this historical CREATE or
its source-freeze/reviewer receipt.

terminal-freeze-original.json pins44immutable private artifact/snapshot/evidence
records (including the actual archive), excluding itself/this handoff. SHA256
e3676385d5184dd7b2fa52c6efb260d650d8529eaddfe7d49ab003aca57ad3f7.
Original provenance75ffc9844a1ccb3d5d29daa7873654d775894a0803a37e3cd7980a5ffdd595dd.
All generated FIXTURE_ONLY trees remain retained as invented evidence but are
outside the terminal byte-hash set/source whitelist; definitions/results/failure
logs are frozen snapshots. No cache/bundle/fake SDK/generated evidence enters
source Git merely by existing locally. Only explicitly reviewed producer/stager/
manifest/fixture definitions/static metadata may be selected by MAIN.

## Integration and next work

Review REPORT-original.md, PROVENANCE-original.json, source checkpoints, exact
raw/canonical inventories/mapping, dependency provenance, source-bound fixture
receipts, independent review and preserved original files. Do not rerun the
exhausted producer or stage current real cache. T101/D101 is the explicit next
assignment for known stager guard/successor metadata; no other source/package/
SDK/runtime execution is implied. MAIN owns acceptance and later clean-build
release. Original T095 delivery is frozen before successor work starts.
