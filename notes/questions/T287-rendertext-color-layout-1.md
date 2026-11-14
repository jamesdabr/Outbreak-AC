# T287 — Text submission repair needs rendertext.cpp

- Author / worker: Engine /01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket and revision: T2871.0
- Phase and contract revision: STOCK_FIRST_PROTOTYPE0.4 / D484
- Exact clause or interface affected: T287 limits writes to vertmodel.h/renderhud.cpp/renderparticles.cpp; necessary HUD glyph submission lives in rendertext.cpp.
- Status: OPEN (lead resolution is recorded separately)

## Question

Please release a narrowly scoped browser-network-only edit to `source/src/rendertext.cpp` for the existing `draw_text()` initial color and inline TEXTCOLOR transitions. No such edit has been made under T287.

## Evidence and impact

Actual Chrome screenshots show huge pale polygons across body/world and missing ordinary HUD text while the two equipment icons remain recognizable. In `rendertext.cpp:410–412`, `draw_text()` calls glBegin(GL_QUADS), then glColor4ub once, then emits glyph UV/positions through TEXTSKELETON. Its TEXTCOLOR macro also changes color only on text formatting codes.

Cached `/private/tmp/outbreak-web-sdk/upstream/emscripten/src/lib/libglemu.js:3154–3170` appends four color bytes into immediate vertexData whenever glColor is called **inside** begin/end and registers a per-vertex color component. It does not repeat that value automatically on subsequent vertices. glTexCoord2f adds8 bytes; glVertex2f adds16 bytes. Thus an ordinary glyph batch with one initial color has4 +24N bytes, while the emulation stride expects28N bytes. Vertex positions/UVs are interpreted at the wrong offsets. This is a concrete layout defect, consistent with the observed screen-space polygons. Source confidence high; actual visual resolution still needs MAIN's rebuild/test.

The model fallback already emits a color per vertex when using per-vertex light and preserves current color afterward. No demonstrated stale-state or brightness correction in the currently allowed files would repair the text record layout. No ambient/skin/lighting change is proposed. Dark stock rendering remains unconfirmed as a defect rather than the existing skin/map lighting.

## Options for owner and lead

Recommended minimal change: under the network-browser guard, set initial glColor4ub **before** glBegin, and have TEXTCOLOR close the current complete glyph-quad batch, call existing text_color outside begin/end, then reopen GL_QUADS. The emulator then uses its uniform current color; glyph vertices contain only their existing UV and position. Preserve all original formatting, alpha/pulse calculations, layout, textures and native/offline behavior. No text redesign or generalized wrapper needed.

Alternative: retain a color stream and emit the actual current text color for every glyph vertex, but this touches more glyph/color plumbing. Suppressing HUD/text or changing model brightness would conceal symptoms and is not recommended.

## Work paused

Only the required rendertext.cpp repair is waiting for a source allowance. No T287 source files changed, no unrelated repair or proof expansion performed. Source inspection is complete; no independent justified patch remains in the current allowlist. MAIN's separate build/runtime verification remains required.
