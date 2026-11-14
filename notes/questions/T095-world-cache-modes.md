# Existing prerequisite cache has modes outside approved package schema

- Author/worker: World/Match-Systems
- Ticket/revision: T0955.20
- Contract: PREREQUISITE_PACKAGE0.1 / D092
- Clause: reject modes other than644/755; preserve644/755; missing/unsupported mode/structure requires question before real packaging, original cache read-only.
- Status: OPEN; MAIN resolution separate.

## Question

What explicit source-to-package mode policy is approved for the existing cache's
523 noncanonical entries? Current contract cannot package this cache unchanged.
No actual producer invocation, manifest generation or original-cache mutation
has occurred. Independent strict-parser/stager fixture work can continue.

## Evidence and impact

Read-only scan of web/build/.cache:5956files/782directories,203069184ordinary-file
bytes, no links/special/hardlinked files found. Modes:5396entries0644,
819entries0755,224entries0600,261entries0664,38entries0775. These last523entries
conflict with approved manifest/archive mode set420/493.

The cache includes compiler-generated port build .o files as expected, alongside
six source archives/sysroot/port data; no blanket rejection of every dependency
object was applied. Further provenance verification remains pending.

## Options for owner and lead

1. Amend/release an explicit canonical package-only mapping0600/0664->0644 and
   0775->0755, preserving original cache bytes/modes and recording original full
   cache identities/modes in private evidence. Manifest/staged modes remain
   canonical644/755. Recommended if canonical staging is the intended contract.
2. Amend allowed manifest/archive modes to preserve all inspected modes, and
   reconcile downstream clean-build/cache permissions requirements explicitly.
3. Provide a separately approved canonical source cache/procedure. Worker will
   not chmod/edit/replace current cache or silently omit entries.

## Work paused

Actual producer --create, real manifest and any source-mode normalization logic.
Pure fixtures for strict canonical inputs/unsafe modes and other independent
producer/stager logic may continue. No private contract amendment or source fix.
