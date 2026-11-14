# T034 measured legacy-GL fixes — stable source and object handoff

- Worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T034 0.8 RELEASED; submitted for MAIN review, not self-accepted
- Governing baseline: AGENTS; BROWSER_FOUNDATION/GOVERNANCE/P0 0.5 with D006 and additive D008 0.8. Gameplay contracts remain unimplemented context.
- Base: `13f0d8eea4822dee5c976661218d022be74342e3` plus D006/current dirty tree. All three owned files matched D006 hashes before editing; main matched accepted T028 `f773210a519ec6567f0fd3bb9c71d71df6ef742da0e3d17f2be1076de2b06adf`.
- Changed repository files: `source/src/main.cpp` only inside mapscreenshot/mapshot; `source/src/editing.cpp` private integer helper and eight assigned calls; `source/src/vertmodel.h` browser list paths/mdldlist declaration. This new handoff is the only new repository note.
- Evidence: `/private/tmp/outbreak-t034-player/` contains initial status, pre-edit source/object copies, per-file patches, source/header/command/object hashes, exact compile/nm logs, native partial-preprocessing outputs and helper fixtures.
- No commit/push/reset/revert, source/build/QA changes outside the allowlist, new dependencies, downloads/cache population, service/browser launch or host-profile access.

## Stable hashes for Engine rebuild

These source bytes are stable at submission:

| Source | SHA-256 |
| --- | --- |
| source/src/main.cpp | `2e90329cb81a4dd34705821c8ceba8613941e5dbd075b9e951704ae2b9e76967` |
| source/src/editing.cpp | `c0f97c81ea3199937302f5e198029cc7a667b1056b6738f8f1dfb91e97cebe00` |
| source/src/vertmodel.h | `1466a707c8eb7a3b76c098f0babff87baf4c6903657f7ddea93c3e0c419e1c98` |

**Header consumers must be rebuilt.** This worker compiled main/editing/rendermodel only; Engine owns the conservative all-unit rebuild and final link under D008. No prior object is promoted to a current all-client result by this handoff.

## Acceptance evidence

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1. Exact narrow browser fixes/native preservation | PASS — source/compile/helper | Editor's eight calls now use a private integer helper: browser glVertex2f, native glVertex2d. Browser mapshot emits an unsupported/no-image diagnostic and returns before sizing/allocation; unsupported texture readback is compiled out. Normal framebuffer screenshot stays. Browser mdldlist is readonly zero; list creation/call/deletion is compiled out and existing direct vertex/index/color/texture/shadow drawing remains. Native partial-preprocessed token streams match originals after the exact private helper normalization. |
| 2. Actual target symbols | PASS | All six current Wasm objects lack glVertex2d, glGetTexImage, glGenLists, glNewList, glEndList, glCallList and glDeleteLists imports. Before objects contain the measured failures; after main retains glReadPixels, editing glVertex2f, rendermodel glDrawElements. Per-object `llvm-nm --undefined-only` logs and hashes are saved. |
| 3. Native syntax + actual target release/debug | PASS | All six native syntax checks and six real Emscripten release/debug object compilations exit 0, with empty diagnostics. Objects have real Wasm magic. Headers/source are hash-pinned before/after each compile with no concurrent input changes. Native list/readback/double-coordinate paths remain. Exact argv/environment and hashes are in result.json. |
| 4. Scope/protected behavior | PASS | No GL no-op stubs, renderer replacement, packet/gameplay/camera features, prototype reverts or dependency changes. Protected combat hashes match D003. Main.cpp outside mapscreenshot is byte-identical to accepted T028. Browser mapshot remains explicitly unsupported; real model/browser drawing is NOT RUN. |
| 5. Immutable handoff/commands/logs/hashes | PASS — submission supplied | This new handoff and owned temp artifacts report all criteria. Contracts/ticket hashes and final owned source hashes were checked again before submission. MAIN remains acceptance/integration owner. |

## Implemented behavior

`mapscreenshot`: browser mapshot exits before reading dimensions, creating an SDL surface, allocating/readback or encoding any output. The native minimap glGetTexImage branch is unchanged. The ordinary screenshot glReadPixels path is unchanged and still imported in browser objects. No fabricated image or success result is produced for unsupported browser mapshot.

`editing.cpp`: private `editorvertex2(int,int)` maps the same bounded editor coordinates to supported float calls in browser builds; native conversions remain int-to-double through glVertex2d. Vertex order, box/border geometry and all other editor rendering remain unchanged.

`vertmodel.h`: browser model display-list caching is disabled at registration and compile time. The list-cache early return is removed only for browser builds. Static models continue through the same existing vertex/index loop; dynamic vertices, UV/color setup, lighting, shadow handling and vertex accounting remain. Browser cleanup owns no list, so no list API is called. Native list behavior, including existing cleanup argument order, is preserved without unrelated fixes.

## Verification and commands

Host: Darwin arm64, Apple clang 17.0.0. Target: inspected pinned Emscripten 7.0.0/compiler `777e6e5db7b4990bcaeb1b9998ed642cc84e6629` from the D005/D006 toolchain. Commands ran from `/Users/jd1/code/apps/outbreak`:

```sh
python3 /private/tmp/outbreak-t034-player/check.py
python3 /private/tmp/outbreak-t034-player/helper-check.py
git diff --check -- source/src/main.cpp source/src/editing.cpp source/src/vertmodel.h
```

All exit 0. The authored scripts were inspected before execution. `check.py` records each actual subprocess; it does not invoke Engine's driver or write Engine-owned output/cache. For each of main.cpp, editing.cpp and rendermodel.cpp, native commands are:

```sh
clang++ [-D_DEBUG] -fsyntax-only -Isource/src -Isource/enet/include -Isource/xcode/Frameworks/SDL2.framework/Headers -Isource/xcode/Frameworks/SDL2_image.framework/Headers -Fsource/xcode/Frameworks -idirafter source/include source/src/<unit>.cpp
```

Actual target argv uses `/private/tmp/outbreak-web-sdk/upstream/emscripten/em++`, `--target=wasm32-unknown-emscripten -std=gnu++11 -fsigned-char`, release `-O2` or debug `-O0 -g -D_DEBUG`, `-sUSE_SDL=2 -sUSE_SDL_IMAGE=2 -sSDL2_IMAGE_FORMATS=["png"] -sUSE_ZLIB=1 -sUSE_VORBIS=1`, absolute source/bot/enet includes, `-c` and task-owned output. No link-only flags or undefined-symbol suppression are added. Release flags equal the measured T031 baseline; debug changes only optimization/debug settings. `baseline-compile-records.json` preserves the exact original per-unit flags/commands; `result.json` records exact new argv.

The environment reuses inspected SDK/config/ports paths with `EM_FROZEN_CACHE=1`; temp/TMPDIR/Node cache point only under `/private/tmp/outbreak-t034-player/`. No port acquisition/cache addition occurs. `llvm-nm` is the installed `/private/tmp/outbreak-web-sdk/upstream/bin/llvm-nm --undefined-only <object>`.

Before symbols (saved measured T031 release objects): main glGetTexImage; editing glVertex2d; rendermodel glCallList/glDeleteLists/glEndList/glGenLists/glNewList. After objects: none of those seven unsupported names. Current object hashes:

| Object under task temp root | SHA-256 |
| --- | --- |
| main-release.o | `18eaf2415d377ae906ed6dbc7fad9aa83817ecefd0fd1c7ddbd1f94cdb9655c2` |
| main-debug.o | `48bb45470a091af2d013d22b9774cecdb56b1643828b80b9d57ae141c8fbd3ef` |
| editing-release.o | `81a7383ff7bb3df6bba724e425f92cb11d822d2f49d7254d077fe276188e215d` |
| editing-debug.o | `24c9c3803d97536a05baf4df5179e90efd192f87bea2d9638b729f1edb6138a0` |
| rendermodel-release.o | `94a016edac5ba80c316755152007c0aaf357a2a5c6ae53465d0c9323ce3db7bd` |
| rendermodel-debug.o | `9aee0b5ad17224f97632e84b8974632f6337459a565582673a1fa8d066c5ffd2` |

`helper-check.py` extracts the actual early mapshot guard and editor helper. Fake diagnostic/GL API signatures verify that mapshot does not enter allocation and normal screenshot does; the editor helper preserves 49 bounded integer coordinate pairs in browser/native selections. These are isolated helper tests, not rendering or screenshot gameplay evidence. Existing direct-model rendering is supported by retained source and actual draw imports here, not a model fixture pretending to be a real browser render.

## Integration and limitations

No new unsupported symbols appeared in these three objects. Full-client recompile/link remains T031/Engine ownership; this handoff does not claim successful full linkage. Actual browser startup/input/map rendering, normal screenshots and original model drawing remain NOT RUN under this ticket. Optional browser mapshot is intentionally unavailable with a precise diagnostic, as approved in D008. No LLM screenshot requirement or debug state API is introduced.

No new questions are required: the measured code matches D008. MAIN can relay the stable hashes to Engine for rebuilding all header consumers. This worker will keep the submitted source stable pending another precise release.
