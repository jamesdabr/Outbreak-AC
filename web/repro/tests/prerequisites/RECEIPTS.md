# T095 private receipt schema 1 / source-freeze checkpoint

Authority T0955.22, PREREQUISITE_PACKAGE0.2 / D092,D094. This private evidence
does not amend the exact public manifest schema. All large/generated fixture and
real package data stays outside the source Git whitelist.

`web/repro/prerequisite-bundles/T095/source-freeze.json` exact keys:
schema_version=1, scope=FROZEN_T095_PRODUCER_STAGER, producer_sha256,
stager_sha256, contract_sha256, fixtures_receipt_sha256. Every digest is SHA256 of
the actual frozen file. Producer additionally binds PASS FIXTURE_ONLY receipt's
producer/stager identities to the frozen code; stale fixture receipts reject.
This checkpoint precedes the sole actual --create operation/real manifest.

Producer creates new source-before.json/source-after.json: arrays sorted by
cache-relative path, raw ORIGINAL modes, ordinary kinds and file byte/hash fields,
using the same field shapes as manifest members but allowing exactly the five
D094 source modes. Root is implicit, matching the contract's member convention.
Arrays must remain identical; producer never chmods or deletes original entries.
`mode-mapping.json` maps each source octal string to exact {package_mode,entries}:
0644->0644,0755->0755,0600/0664->0644,0775->0755. Directory searchability required.
`dependency-provenance.json` records port object path/SHA/source-name origin and
the retained SDK/port archives/caches/notices role, without relicense claims.

`create-receipt.json` exact keys: schema_version=1, operation=CREATE,
status=STARTED|PASS|FAIL, manifest_sha256, bundle_sha256,
source_before_sha256, source_after_sha256, source_unchanged,
members,expanded_bytes,compression_seconds,total_seconds,error.
Unavailable fields are null. Error is null or a bounded exception type/message.
Successful creation records <=120s compression and<=180s complete packaging.
Partial archives/private evidence remain on failure; no output is replaced.

Stager's fixed new receipt path is prerequisite-bundles/T095/stage-FULLSHA.json,
derived from separately supplied trusted manifest SHA256, never an arbitrary ID.
Exact keys: schema_version=1,operation=STAGE,status=STARTED|PASS|FAIL,
manifest_sha256,bundle_sha256,destination,members,expanded_bytes,
partial_destination,error. Validation before cache reservation has no cache or
report effect. Once reservation begins, failure retains only owned partial cache
and this report; an existing cache/report refuses and is never removed/replaced.
No actual staging into current real cache is authorized/performed by T095.

Pure tests write fixture-attempt-N.json/.txt and conspicuous FIXTURE_ONLY fake
trees, preserving first failure and all positive/negative data. FIXTURE_PASS.json
selects latest successful source-bound suite; it is not real SDK/cache proof.
The independent verifier's receipt includes status/scope, manifest/bundle hashes,
sizes/member count, gzip/tar EOF facts, full source-byte/mode/provenance equality,
raw-source unchanged, mapping counts, actual stager NOT RUN and own source SHA.
It imports no producer/stager/SDK/project code, uses stdlib tarfile/gzip/zlib and
reads original cache directly; it never writes extracted cache members.

Public runtime CLI flags are fixed: producer --create only; stager --bundle
ABS_PATH --manifest-sha256 EXPECTED_SHA only. No root/output/SDK/command hooks.
Both public entrypoints install a deny-process/network audit boundary and deny
all SDK/original-cache writes; only fixed new package/manifest or new staged cache/
own receipt paths are permitted. Fixture tests install stronger fake-root-only
effects guard, deny even real-SDK access, and never execute their dummy data.
