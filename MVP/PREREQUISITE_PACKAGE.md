# Frozen browser build prerequisite package

Revision:0.2. Status: APPROVED MAIN D092 for T095, isolated local P0 packaging. No SDK acquisition/installation/compiler/game/runtime or complete P0 acceptance.

## Purpose and files

Current Emscripten7 network recipe requires a preseeded repository/web/build/.cache. Package that validated DATA into a documented immutable prerequisite, so a clean source checkout does not depend on undisclosed historical workspace files. Reusing frozen SDK/port libraries is permitted; reusing compiled game objects is forbidden. Old cache/SDK/receipts remain immutable.

NEW web/repro/package_prerequisites.py and stage_prerequisites.py, prerequisites.json, tests/prerequisites/** and prerequisite-bundles/T095/** only. Scripts use Python standard library, repository root from their location, no imported project execution/SDK/node/compiler/manager/network/service. Actual package creation after own code inspection/tests is allowed under T095. Actual staging into the real source cache is NOT allowed; only isolated labeled fixture staging under own test directory. New clean-checkout staging needs a later execution ticket.

Producer command: python3 -B web/repro/package_prerequisites.py --create. Fixed source repository/web/build/.cache, fixed NEW output web/repro/prerequisite-bundles/T095/ports-emscripten-7.0.0.tar.gz and NEW web/repro/prerequisites.json; refuse prior outputs. No arbitrary input/output/command hooks. Validate installed SDK/version/compiler/Node and six existing port archive/recipe identities against the accepted inspected source metadata; fully hash original cache before/after, no cache mutation. Empty original cache or game objects fails. Valid compiler-generated sysroot/port SDK libraries are not game objects; identify provenance instead of rejecting every .o in dependency archives.

Inventory every cache file/directory, canonical sorted relative names/modes/sizes/SHA256, ordinary entries only; reject symlink/hardlink/special/escaping/traversing inputs, modes other than644/755, duplicate/case-colliding members and unbounded size. Limits100000members/1GiB expanded/512MiB compressed. Archive canonical data only: sorted names, uid/gid0, empty uname/gname, mtime0, preserved644/755, gzip filename empty/mtime0, deterministic PAX paths if needed. No install hooks/executable scripts run. Preserve dependency source archives/licenses and record upstream provenance; no new license interpretation/relicense/public redistribution claim.

## Exact prerequisite manifest

JSON exact top fields schema_version(integer1),kind("FROZEN_BROWSER_PREREQUISITES"),recipe("network_v1"),sdk,ports,cache,producer.

sdk exact fields root("/private/tmp/outbreak-web-sdk"),version("7.0.0"),compiler_revision("777e6e5db7b4990bcaeb1b9998ed642cc84e6629"),node({path:canonical fixed SDK Node24.19.0 path,sha256:accepted27db838...}),alias_decisions(array of exact {path:repository-relative D044/D046 JSON,sha256:accepted digest}). Existing inspected alias chains remain authoritative; package does not activate/configure SDK.

ports: exactly ordered sdl2,sdl2_image,zlib,vorbis,ogg,libpng records, each exact {name,archive:cache-relative canonical path,archive_sha256,archive_sha512,recipe:sdk-relative canonical path,recipe_sha256}; exact hashes from accepted six recipes/archives. Do not select latest/substitute libraries.

cache exact fields bundle({path:"web/repro/prerequisite-bundles/T095/ports-emscripten-7.0.0.tar.gz",bytes:integer,sha256}),expanded_bytes(integer),members(array sorted unique). File record exact {path:canonical cache-relative,kind:"file",mode:420|493,bytes:integer,sha256}; directory record exact {path,kind:"directory",mode:420|493}. Paths no absolute/empty/dot/traversal/backslash/control characters. Root implicit. Casefold collisions reject. Every actual tar member must equal declared type/mode/size/hash; undeclared/missing/duplicate/link/special/trailing content fails. Archive stream/PAX structural metadata may exist only to encode the declared ordinary member names, not independent payloads.

producer exact fields source({path:"web/repro/package_prerequisites.py",sha256}),stager({path:"web/repro/stage_prerequisites.py",sha256}),provenance(array of exact {path:repository-relative read-only accepted metadata/license record,sha256}). Paths identify data/source, never executable commands or import hooks. Every digest64lowerhex, lengths bounded, strict duplicate JSON keys/types/unknown fields.

The manifest is authored only after producer/stager code frozen. It may be versioned source metadata since it does not reference its own source commit; the separate source-input manifest is generated after the reviewed source commit per D091. Its bundle is a supplied prerequisite outside the source revision, not a hidden game output.

## Stager and evidence

Stager command: python3 -B web/repro/stage_prerequisites.py --bundle ABS_PATH --manifest-sha256 EXPECTED_SHA. Manifest path fixed repository/web/repro/prerequisites.json, expected digest supplied by MAIN release. Bundle may be read from a supplied local location only after exact size/digest; destination fixed derived repository/web/build/.cache. No arbitrary repository/output/sdk/flags selection. Verify code identities, SDK/Node/recipes/approved aliases, full archive inventory and member bytes BEFORE reserving absent destination. Reject existing destination or linked ancestors. Reserve cache exclusively, manually copy only validated ordinary records, verify complete resulting bytes/modes/member equality. Do not extractall/follow archive links/run contents or alter SDK/global settings. Failures preserve only owned partial output and new own report, never delete/replace an existing cache or retry under same ID. No staging into current real cache during T095.

Pure fixture tests use own temporary fake data/SDK/manifest root with actual process/network/SDK/Node/compiler effects forbidden, conspicuously FIXTURE_ONLY. Cover valid roundtrip/determinism; wrong source/producer/stager/SDK/port/recipe/hash/manifest; path/traversal/absolute/duplicate/type/size/overflow/link/hardlink/special/PAX/case collision; missing/extra/truncated/trailing payload; late mutation; pre-effect refusal/existing destination/no overwrite; exact original cache preservation. Fake fixtures are not a validated real SDK/cache. After inspection and tests, one actual producer invocation and independent read-only archive/member/cache verification are authorized, bounded<=120s compression and<=180s full packaging, no auto retry. Freeze source/private receipt schema, artifact/provenance/real verification and handoff. Stager real execution stays NOT RUN until clean-build release.

## D094 permission amendment

D094 authorizes exact source-to-package mode normalization0644→0644,0755→0755,0600/0664→0644,0775→0755, only in NEW archive/staged output. Original source cache raw modes/bytes remain unchanged and fully recorded. Reject other modes; no original chmod or skipped entries. This supersedes earlier wording that rejected every non644/755 source entry or required preserving source modes verbatim. Manifest/archive/staged schema still permits only644/755.
