# T031 seven unresolved legacy GL symbols block actual browser link

- Author / worker: Engine & Multiplayer
- Ticket and revision: T031 0.6 RELEASED
- Phase and contract revision: BROWSER_FOUNDATION/GOVERNANCE 0.5; approved D006 addendum 0.6
- Exact clause or interface affected: T031 full link; D006 source-fix restrictions and no undefined-symbol suppression
- Status: OPEN (lead resolution is recorded separately)

## Question

Please release narrowly scoped source fixes for the following real linker
failures. All 53 C++ and eight ENet C translation units compile to Wasm with
the exact D006 profile. The actual legacy-emulation link exits 1 on seven
distinct missing GL functions. These cannot be fixed by declarations alone
inside Engine's platform.h/tools.h allowlist; no shim/stub is proposed here.

## Evidence and impact

Exact actual command and inputs: `web/build/generated/t031/attempt-1/result.json`.
Exact wasm-ld diagnostics: `web/build/generated/t031/attempt-1/link.log`.
Profile includes LEGACY_GL_EMULATION=1, target PNG SDL2_image/libpng, SDK
OpenAL, memory growth, initial memory 64 MiB, stack 2 MiB. No unsafe GL option
or undefined-symbol-ignore flag was used. SDK libglemu.js does not supply
the missing symbols in this real link.

| Symbol | Actual object / source locations |
| --- | --- |
| glVertex2d | editing.cpp.o; source/src/editing.cpp:903–906,914–917 |
| glGetTexImage | main.cpp.o; source/src/main.cpp:428 (texture inspection/readback path) |
| glDeleteLists | rendermodel.cpp.o via source/src/vertmodel.h:162,295 |
| glCallList | same header:473,558 |
| glGenLists / glNewList | same header:548 |
| glEndList | same header:557 |

The renderer already has a vertex-array draw path directly after the
display-list branch. Model source compilation succeeds; lack of a browser
display-list implementation is a link issue, not evidence that the renderer
can be replaced or that missing calls should return fabricated success.

## Options for owner and lead

1. Assign minimal browser compatibility changes to exact owners: use the
   supported float vertex call for the edit-overlay coordinates; make the
   unsupported texture-readback command explicitly unavailable or implement a
   supported browser readback path; guard display-list create/replay/delete
   and force the existing real vertex-array path for browser model rendering.
   Preserve native paths. Owner/lead must freeze exact intended behavior and
   allowlists before those files change.
2. Approve a different documented SDK feature profile only if inspection
   demonstrates these exact functions are implemented. No such compatible
   setting has been found or enabled by this worker. Undefined-symbol
   suppression and successful no-op GL replacements are not valid fixes.

## Work paused

Successful full client link only, pending non-allowlisted source fixes.
Engine continues exact accepted-pack validation/packaging attempt, current
release/debug/native regressions and complete failure evidence. The pack is
now accepted by D006-pack-acceptance; its absence is not a blocker. No game,
rendering, decoding or multiplayer success is claimed.
