# T287 — Concrete text layout blocker

Engine /01a1b92b-53f9-7132-aeb9-72b637ac3a90; T2871.0 / STOCK_FIRST_PROTOTYPE0.4 / D484. Notes-only result: no source changes.

Inspected the actual stock/IAB and Chrome screenshots, model fallback/current color, world/client-array cleanup, HUD/particle paths and cached GL immediate emulation. Found a concrete mismatch in `rendertext.cpp` glyph submission: one color emitted inside glBegin is treated by the emulator as a color attribute present in every vertex record, but subsequent glyph vertices supply only UV/position. This shifts interpreted record offsets and fits the huge screen-space polygons/missing HUD glyphs. High source confidence; runtime cause/resolution not yet confirmed.

The necessary source is outside this ticket's three-file allowlist. Exact evidence and proposed minimal browser-only uniform-color/glyph-batch repair are in `notes/questions/T287-rendertext-color-layout-1.md`. No HUD suppression, ambient boost, skin redesign or speculative particle changes made. Dark stock body has no independently demonstrated compatibility fix yet; preserve real lighting and inspect after overlay removal.

**NOT RUN:** helpers/tests, compiler, browser/game/runtime, services/network, FFI or Git. Player's camera lease untouched. No framework or asset/history writes. MAIN needs a precise rendertext.cpp release, then its actual build/visual comparison. Stopping at this scoped question/handoff.
