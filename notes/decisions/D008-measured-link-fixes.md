# D008 Measured full-client and native debug blockers

Approved lead additive execution amendment revision 0.8 to browser foundation/GOVERNANCE/P0 0.5 and T031 0.6. No gameplay scope or acceptance gates change. Source evidence is actual T031 attempt-1 link.log and actual T033 arm64 debug compiler failures, not guessed dependencies.

All 61 real browser units compile. Actual full link fails only on listed glVertex2d, glGetTexImage and display-list imports. Native server release links; debug ASSERT emits unsupported x86 int $3 on arm64. Fix these narrowly under exclusive source ownership, then repeat changed-object/header consumers and actual links.

Player T034 owns source/src/main.cpp only in mapscreenshot mapshot handling, source/src/editing.cpp only eight integer 2D editor vertex calls, and source/src/vertmodel.h only browser display-list paths. For Emscripten, editor int coordinates may use supported glVertex2f (same bounded editor coordinates) through a narrow private helper/guards, never generic GL symbol emulation. Browser mapshot/minimap texture readback is unsupported in this experiment: fail visibly before allocation/readback with a precise diagnostic and no fabricated image; normal framebuffer screenshot path remains intact. Keep native glGetTexImage behavior unchanged. This is optional developer screenshot functionality, not an LLM screenshot requirement.

For browser models use the EXISTING direct vertex/index drawing path instead of display-list cache: compile out list creation/call/deletion, force browser mdldlist off, retain model vertex/color/texture/draw/shadow logic. Do not replace GL entrypoints with no-op stubs, omit all model drawing, change geometry or weaken undefined-symbol checks. Native branches unchanged. Actual model rendering is still unverified until original model assets are added and tested.

Engine T031 additionally owns tools.h for this exact debug fix: select fflush + __builtin_trap for Emscripten OR native arm64 (__aarch64__/__arm64__), preserving other architecture branches and release behavior. No new macro/behavior changes beyond architecture-correct trapping. Native debug check should prove emitted ARM trap and nonzero failed assertion via a tiny isolated fixture, not crash the actual server. AI T033 remains read-only source and reruns real debug build after Engine signals stable header.

T034 may use already installed Apple clang and pinned inspected Emscripten with existing frozen cache, own /private/tmp/outbreak-t034-player/** outputs; no new ports/downloads or build/cache mutations. Native release/debug syntax of affected TUs and actual Wasm objects current main/editing/rendermodel are required, or precise compilation failure. No serving or game execution by Player. Header edits invalidate every consuming object: Engine must track dependencies/conservatively rebuild all 61 units for final stable link, and AI all native affected TUs. Separate workers preserve other edits and no one edits another allowlist.

T031's compile/link execution remains authorized with D006 exact flags/ports/pack. No unrelated flags, transport, gameplay or broad renderer rewrite. Document omitted mapshot and browser direct-draw profile in build metadata/compatibility report. Source/object evidence alone cannot prove browser runtime or original model rendering.

## Independent T035 proposal release

MAIN additionally releases QA T035 revision 0.8 for read-only browser transport/interface/acceptance planning in new own notes only, while the real bundle is unavailable. This is the separately authorized proposal permitted by T021; no networking implementation, dependency, service or transport selection is approved. T030 real-build execution takes priority once exact artifact hashes are supplied.
