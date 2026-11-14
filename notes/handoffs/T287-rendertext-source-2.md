# T2871.1 — Glyph color layout correction

Engine /01a1b92b-53f9-7132-aeb9-72b637ac3a90; STOCK_FIRST_PROTOTYPE0.4 / D484 / D486. Changed only `source/src/rendertext.cpp` and this new handoff. Prior question/handoff and unrelated source/history preserved; no Git action.

Implemented exactly the resolved allowance, guarded to `__EMSCRIPTEN__ && OUTBREAK_NETWORK_CLIENT && !STANDALONE`:

- Initial text color is set before glBegin(GL_QUADS).
- Inline TEXTCOLOR closes the completed glyph batch, invokes unchanged `text_color()` outside begin/end, then opens the next glyph batch.
- Native/offline initial order and TEXTCOLOR expansion remain unchanged.

This keeps color uniform rather than inserting a sparse color component into Emscripten's immediate vertex stream. Glyph positions/UVs, formatting stack, existing alpha/pulse calculation, cursor/inlined graphics, blend function and texture choice are unchanged. Empty batches around adjacent/initial color codes are valid no-draw batches. No model brightness, HUD suppression, assets, Player camera files or other renderer paths changed.

Source readback completed; revised ticket1.1 and D486 checked before implementation, ticket rechecked before submission. High confidence the identified record-layout mismatch is corrected; actual pale-overlay removal remains runtime-unverified. Dark model appearance remains separately unresolved; no artificial lighting change.

**NOT RUN:** compiler, helper/tests, browser/game/runtime, service/network, FFI or Git. No simulation or framework. MAIN must rebuild and observe HUD glyphs/inline colors/pulse plus world/body without the pale overlay; control and other renderer defects remain their own checks. Stable source submitted; stopping.
