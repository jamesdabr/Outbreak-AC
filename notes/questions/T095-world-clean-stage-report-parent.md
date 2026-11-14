# Frozen stager guard rejects missing report-parent scaffolding in clean checkout

- Author/worker: World/Match-Systems
- Ticket/revision: T0955.22
- Contract: PREREQUISITE_PACKAGE0.2 / D092,D094
- Clauses: "Freeze source code BEFORE constructing the real manifest with producer/stager hashes"; one actual producer operation/no automatic retry; new fixed-root clean-checkout stager.
- Status: OPEN; MAIN resolution separate.

## Question

May MAIN release a narrow stager/fixture correction and explicit successor
manifest-source identity/review procedure, preserving the completed one-shot
package/archive/current manifest/source checkpoint/receipt? The single actual
producer has already succeeded; worker will not silently edit frozen stager
bytes, rewrite its manifest identity, or rerun/repackage the original cache.

## Evidence and impact

Producer/stager frozen before actual manifest; source checkpoint
26177ee675cef16192afbfc712e28001780edd1e50b1d72bed390130ef7562c0.
One actual --create PASS,6738members/203069184expanded bytes,61535814bundle bytes,
compression8.3590s/full11.6730s; full original raw inventory/modes unchanged.
Independent stdlib tar/gzip/source verification PASS, including all bytes/modes,
six archive identities/provenance,40PAX members and strict gzip/zero-tail EOF.

Current manifest SHA256:
ca805d345d7f17c451e89f6d25e02b8e7cc44ac04b7928abf03078237d12c92d.
Archive SHA256:
2878a16023019e008b909e2730556de587c51041190e32656366cc53ee72d120.
Frozen stager SHA256:
3519ebccad7f7afb8c5f72761e576a237bf6632520ab7d63cbaeeee676462f4d.

Post-package read-only review found the CLI audit guard permits new report paths
only at/under web/repro/prerequisite-bundles/T095. If a clean source checkout lacks
web/repro/prerequisite-bundles (large artifacts intentionally not versioned),
report.parent.mkdir(parents=True) tries to create that intermediate parent and
the guard rejects it. A tiny pure fake-root reproduction confirms ValueError
before destination/report creation. No real staging/cache/SDK effect occurred.
Evidence: web/repro/tests/prerequisites/post-freeze-clean-report-guard.json.

Existing17fixture groups pass but their roundtrip setup first produces a fixture
bundle under T095, so that parent already exists. They did not exercise this
fresh-checkout CLI-guard combination. Package bytes remain valid; stager cannot
yet be claimed ready for that missing-parent layout. Actual real staging is NOT RUN.

## Proposed narrow correction/release

Permit ONLY required mkdir scaffolding at the fixed prerequisite-bundles parent
(directory creation, not arbitrary file writes there), retaining all other
process/network/SDK/original-cache/unknown-output restrictions. Add a pure fixture
with supplied bundle outside fake checkout, missing report hierarchy and absent
cache; exercise the public guard along with full stage logic. Also retain denied
write/linked-parent/overwrite/partial-failure tests.

Because source/manifest identities are already frozen and the single actual
producer operation is exhausted, MAIN should specify additive historical copies
and successor metadata rebinding (or a new ticket) before edits. Reuse the exact
verified bundle without another actual package/stage/compiler/SDK operation.

## Work paused

Stager/source/manifest corrections and any further producer/stager operation.
Independent package verification/provenance/final current-delivery freeze can
continue; all actual artifacts/source cache remain preserved. No source-hash
waiver, hidden manifest overwrite or clean-staging acceptance inferred.
