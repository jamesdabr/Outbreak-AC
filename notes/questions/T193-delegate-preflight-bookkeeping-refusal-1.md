# T193 metadata preflight stopped on an incorrect historical-source comparison

- Author / worker: MAIN delegate /root/review_head_equality.
- Ticket and revision: T1931.0 / D309.
- Phase and contract revision: G2_FOUNDATION0.3.
- Exact clause affected: preflight exact changed production identity, unchanged consumed headers, historical G1 dependency-reference context; refusal before launch.
- Status: OPEN (lead resolution recorded separately).

## Question

May the delegate correct its inline metadata-only historical dependency walk to compare only the seven unchanged project headers against accepted G1 dependency identities, while retaining the already correct explicit T193 geometry.cpp74169/current-SHA and accepted-prefix checks? No compiler has been invoked and no output root has been created. This asks for bookkeeping disposition, not changed source, flags or an additional compiler invocation.

## Evidence and impact

Original inline stdlib-only preflight command returned terminal exit1, chunkde06e9, traceback `File "<stdin>", line29, AssertionError`. Its source/current-prefix checks passed first. The erroneous branch was:

`if str(repo/'source/outbreak') in path: assert project[path]==entry['identity']; continue`

That mistakenly includes the historical geometry.cpp entry, whose31382-byte G1 source is deliberately different from the named74169-byte G2 translation unit. The ticket already binds the latter and requires its first31382 bytes to preserve the G1 hash. The comparison should apply only to unchanged project header entries; the changed source must retain its explicit T193 checks instead of being equated to its accepted ancestor.

A subsequent read-only inspection confirms output root absent, current source74169/SHA2560d999988280531d74ded6bfa27ae35e032233886267ddb1deb5def276cc4bf3b, first31382 bytes SHA256c232100352425092561f6fc9701c77db17f643893510fde780839db21be17d21, and all seven project-header byte hashes match historical G1 entries. No actual immutable-input mismatch is evidenced by this authoring error. The compiler invocation counters remain native0/Wasm0. No production/header/control/SDK/cache/evidence file was changed; the preflight script did not reach its mkdir/write statements.

## Options for owner and lead

Authorize the exact metadata walk correction and retain this failure note; keep both compiler calls unconsumed and all commands/inputs/limits unchanged. Alternatively leave T193 stopped. The delegate does not reinterpret the before-launch refusal clause as permission to retry itself.

## Work paused

All remaining T193 preflight metadata construction and both fixed syntax calls await MAIN disposition. Read-only inspection and this own question note do not consume or substitute for an authorized frontend outcome. World source protection remains in effect until MAIN disposition or stable postflight/handoff.
