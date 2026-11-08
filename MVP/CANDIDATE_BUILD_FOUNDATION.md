# Reusable fixed-network candidate build prerequisite

Revision:0.2. Status: APPROVED MAIN D085, isolated P0 tooling prerequisite. Does not approve full P0/shared gameplay or execute a build.

## Fixed scope and ownership

Create new candidate_recipe.py/build_candidate.py/verify_candidate.py under web/build and new tests/candidate/**. Existing profile_client.py/T066/T072 wrappers/config/shell/asset helpers/SDK are immutable reusable implementation inputs, not edit targets. Initial successor supports ONLY the accepted NETWORK_CLIENT original-network-media recipe: exact61 fresh units/flags/backend/79-file pack/12 notices, safe legacy GL,64MiB initial/2MiB stack, no game object reuse. No compiler command/plugin/env from manifest, arbitrary profiles, download/install or game/server runtime.

Repository root is derived from the installed script location; SDK remains /private/tmp/outbreak-web-sdk for this first developer recipe. Ports prerequisite remains repository/web/build/.cache, documented and independently pinned. Clean checkout at another source root on this same host is a required later proof; this first recipe does not claim arbitrary SDK relocation. Existing source may differ from T070 only through explicit MAIN-reviewed source-manifest identities; historical hardcoded backend/shell/pack/alias flags remain intact. Player exclusively owns simultaneous md3.h exactfix; preparation fixtures must not treat unconsumed unrelated worker paths as compile inputs.

## Public CLI and authorization

build_candidate.py modes --plan-only or --execute (mutually exclusive), required --candidate-id ID; execution additionally --pins ABSOLUTE_MAIN_JSON --pins-sha256 SHA256. ID matches [A-Za-z0-9_-]{1,48}. Plan-only may report stdout and write NEW tests/candidate/preparation-ID/** only; it never reserves actual attempt/publication or invokes subprocess/network. Real destinations are fixed web/build/candidate-attempts/ID and web/build/candidates/ID. Refuse existing destinations, canonical path violations, escaping/undeclared links, overlap or unknown fields before effects. A failed reserved attempt/publication remains failure; no deletion/retry/replacement. Reserve absent destinations atomically with exclusive creation. Incomplete publication is never accepted; final exact inventory/manifest and independent review establish completion.

Authorization JSON exact top-level fields:
- schema_version: integer1
- kind: "CANDIDATE_NETWORK_BUILD_AUTHORIZATION"
- authority: "MAIN"
- status: "ACCEPTED"
- execution_release: "EXPLICIT_CANDIDATE_NETWORK_BUILD_EXECUTION"
- recipe: "network_v1"
- ticket: exact released execution ticket string, nonempty <=64ASCII bytes; this is recorded provenance, not an executable selector
- candidate_id: ID
- decision: canonical notes/decisions/*.md path, also hashed in observation inputs
- source_revision:40 lowercase hex Git revision, exact observed repository HEAD; actual source manifest separately binds the dirty/versioned overlay; do not infer clean status
- source_manifest: {path:"web/repro/source-manifest.json",sha256:64lowerhex}; actual exact source entries/hash/mode must match
- bindings: {repository:canonical actual repository root,sdk:"/private/tmp/outbreak-web-sdk",ports_cache:canonical repository/web/build/.cache}
- observation: exact recipe observation fields inputs,preservation,units,ports,aliases,alias_decisions,pack,tool_errors. Full actual current equality required, tool_errors empty. Do not drop original gates or exclude arbitrary generated trees.

MAIN creates accepted execution pins and separately supplies digest only after prep review. Workers may create conspicuously FIXTURE_ONLY documents inside temporary preparation fixtures with no real effects. A manifest claiming acceptance never self-authorizes; path/digest/authority/complete current closure gate precedes every real compiler boundary.

Source manifest schema1 exact fields schema_version(1),kind("SOURCE_INPUT_MANIFEST"),source_revision(40hex),entries(array). Each entry exact {path:canonical repository-relative path,bytes:nonnegative integer,sha256:64lowerhex,mode:integer420 or493}. Unique sorted entries; all ordinary files/no links for this initial source set. Contains all source/build/config/helper/selected payload/notices actually consumed, excludes itself to avoid recursive digest. Prerequisite files separately belong to observation tools/ports/aliases. Neither manifest nor source_revision replaces actual compiler-discovered closure.

## Build/verifier behavior and proof

Generate fixed commands from accepted recipe. Allow existing read-only helper composition/subclassing; override only new candidate paths/identity/authority and preservation phases, never mutate globals/monkeypatch the historical modules. Record exact current authoring tools too. Fresh task-owned physical frozen port-cache copy; all compiler/temp/module/Node writes within new attempt. Original SDK/cache/source/native/artifacts immutable. Record pre/post actual compiler dependency file membership/hash for every unit, including system/SDK headers; undeclared/new/changed dependency fails rather than a raw-hash exception. Record61 actual object commands/hashes/logs, link, JS syntax and actual Wasm validation, exact argv/env/exit, metadata, no runtime claims. Bounds: any compiler command<=120s, complete attempt<=3600s, bounded diagnostic logs with explicit overflow failure; track owned process timeout cleanup. No shell or suppressing undefined imports/errors.

Preservation is phase-aware: original protected byte/membership set stays exact. Existing earlier candidate publications/attempts are protected inputs. Only this new owned attempt and publication gain explicitly enumerated members. Validate all four runtime files, exact79 nonoverlapping index.data slices against approved manifest, metadata/bundle identity and12 notice bytes in both retained bundle and publication. Do not reproduce T070's postpublication preservation failure or exempt all outputs/generated directories. Terminal attempt inventory includes owned cache/objects/logs plus named result/freeze; freeze excludes only itself and a separately named verification receipt when appropriate, no self-reference. Failed attempts retain evidence without emitting success/acceptance.

verify_candidate.py --candidate-id ID --pins ABS --pins-sha256 SHA is read-only by default and prints a bounded report. An optional --receipt PATH may create one NEW receipt under that candidate's owned verification/ directory only, using exclusive creation; never overwrite. It checks source/tool/pins/result/command/object/alias/port/payload/metadata/notices/protection and exact original+new membership closure. It cannot write an accepted-artifact manifest or modify any result. Metadata records LINKED_NOT_BROWSER_VERIFIED and false runtime/audio/model/multiplayer/authority/P0 claims. Its private result-record layout must be documented/frozen in preparation and reviewed before actual execution; no other adapter may consume it until separately approved.

## Preparation acceptance

Pure fixtures with real subprocess/socket/compiler functions forbidden must cover wrong/missing/extra identity/source/tool/port/alias/member, malformed/duplicate JSON/type/path/link/overlap, existing target/reservation, corrupt/stale/reused object/commands/logs/metadata/payload/notices, late source/dependency change, failed-command/timeout, original+new phase inventory equality, independent receipt no-overwrite, and denial of self-acceptance/runtime claims. Label injected effect doubles/objects FIXTURE_ONLY; no real build from test-success. A read-only actual observation/plan is allowed after the Player exactfix is terminal; it is NOT execution authorization. Freeze new source/tests/docs/preparation evidence and submit for MAIN review. Actual builds/clean checkout/native signing/runtime require new tickets and pins.

## D091 shared-package/preservation amendment

D091-shared-source-and-preservation-records.md governs the common source-package interpretation, allowed existing Python authoring inputs and exact observation.preservation {files,directories,links,absent_roots} record. It supersedes conflicting earlier private map wording. Every manifest member is verified/stable; each recipe requires its consumed subset, permits other explicitly MAIN-listed source-package files, and still rejects undeclared consumed compiler headers. Protected historical symlinks are recorded opaquely without following, never granted as consumed input/output links. No actual build/runtime scope changes.
