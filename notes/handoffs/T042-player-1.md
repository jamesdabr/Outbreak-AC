# T042 preserve allocated browser world storage — stable source/object handoff

- Worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T042 1.6 RELEASED; submitted for MAIN review, not self-accepted
- Governing baseline: AGENTS; browser foundation/GOVERNANCE/P0 0.5; D019 additive 1.6; actual D016/D017 evidence supplied by MAIN.
- Base: `13f0d8eea4822dee5c976661218d022be74342e3` plus accepted dirty tree. worldio.cpp had no pre-existing diff and SHA-256 `fd01e3c171da5a89b2a5bee2c0b4a80d06d49738d6d1ddc41b7d7dbb816d97cc`.
- Changed source: `source/src/worldio.cpp` only, the resource-table-to-entity pointer reassignment's `#ifndef __EMSCRIPTEN__` guard and adjacent explanation.
- Stable final worldio.cpp SHA-256: `8b6d1e7aa7197be1d5030954f48662bcaab85412b222cea027762fbdb1c488c1`.
- Own notes: this handoff and `notes/questions/T042-player-rle-repeat-bounds-separate.md` (read-only unrelated decoder observation requested by D019).
- Evidence/precise patch: `/private/tmp/outbreak-t042-player/`, especially `T042.patch`, `result.json`, `helper-result.json`, `helper-input.json`, `check.log`, initial status and hash snapshots.
- No other source/build/assets/QA/contracts/decisions/earlier notes edited; no commit/push/reset/revert, dependency/port/cache additions, host-profile operations or game/browser/server launch.

## Acceptance evidence

| Requirement | Result | Evidence |
| --- | --- | --- |
| Preserve real browser allocation/mips, retain validation/native behavior | PASS — exact source/helper | Only the legacy reassignment is compiled out in browser builds. The actual setupworld allocation, real RLE decode and every subsequent structural/config/media validation call remain byte-for-byte intact. No fake mapinfo entry, stock metadata, decoder-success stub or new API. Native preprocessed tokens equal the baseline; restoring the exact guard region reconstructs the entire original worldio.cpp. |
| Focused ownership/capacity regression | PASS — native host helper with real types/fragments/map | Actual setupworld, sqrdefault, rldecodecubes, guarded reassignment and cube.h's real sqr/entity/vector/ucharbuf/hashtable types consume the actual original map's RLE bytes. Browser-selected helper keeps allocated ownership, decodes valid geometry, preserves entity bytes and untouched mip storage, and retains truncated-input rejection. Native-selected helper confirms the inherited alias/capacity mismatch without executing the unsafe native decode. |
| Optional ASan helper | NOT RUN to completion / TIMEOUT | Real AddressSanitizer helper compilation succeeds. Execution did not finish within 8 seconds and the subprocess was terminated. No sanitizer pass or diagnosed sanitizer-runtime cause is claimed. Plain ownership helpers both exit 0. This is not an ASan game profile. |
| Whole-TU native release/debug syntax and actual Wasm release/debug | PASS | All four complete worldio.cpp compiler invocations exit 0 with empty diagnostics. Target objects have Wasm magic; source/header hashes are stable across each compile. Exact argv/environment/tool/command/object hashes are in result.json. |
| Stable immutable handoff/scope | PASS — submission supplied | Stable source hash above, exact narrow patch and all results supplied. Prior T028/T034/T038 source and every D003-protected combat hash remain unchanged. Ticket/decision/contract hashes were rechecked before submission. MAIN owns acceptance, Engine rebuild/link and actual QA recovery verification. |

**Actual browser recovery is NOT RUN here and is not claimed.** The invalid ownership/capacity path is concrete source/helper evidence; the D016 trap's resolution requires a new linked build and real QA rerun.

## Narrow implementation

After real `delete[] world; setupworld(hdr.sfactor);`:

```cpp
#ifndef __EMSCRIPTEN__
    // Browser original packs have no stock resource table; keep setupworld's
    // full world/mip allocation instead of aliasing the smaller entity buffer.
    if(!mapinfo.numelems || (mapinfo.access(mname) && !cmpf(cgzname, mapinfo[mname]))) world = (sqr *)ents.getbuf();
#endif
```

The browser still allocates actual `mipsize` squares and initializes wmip through setupworld. Empty resource metadata no longer changes its world pointer to entity storage. The native condition/assignment remains unchanged. The decoder, error flags, map dimensions, lighting, config execution and media validation were not modified.

## Focused regression details

`make-helper.py` reads source fragments as data and decompresses the accepted original `packages/maps/dev_outbreak_browser.cgz` using Python's gzip library into the task temp directory. It does not execute the generator, CubeScript or the game. `helper-input.json` pins original compressed/raw map hashes and identifies source fragments/types. The helper reads the real v10 header/entity section and original RLE stream.

Measured by the compiled host helper:

- Actual map: sfactor 6, 64×64 = 4096 base cubes; 9 serialized persistent entities.
- Real entity vector: capacity 16 × sizeof(entity) 24 = **384 bytes**.
- Real base world: 4096 × sizeof(sqr) 16 = **65,536 bytes**.
- Actual setupworld world/mip allocation: 5488 squares = **87,808 bytes**.

With an empty real hashtable, browser-selected guard leaves `world == allocated`, distinct from `ents.getbuf()`, and wmip[0]/wmip[1] retain the original allocation/offset. The actual decoder succeeds, consumes all original encoded bytes, produces 2224 SPACE cells plus SOLID cells totaling 4096, preserves all entity object bytes and leaves the allocation's mip tail zeroed. Removing the final encoded byte returns false, sets overread and emits the existing warning through a diagnostic capture, demonstrating retained real decoder error behavior. No fake validation result is supplied.

The native-selected helper shows `world == entitybuffer`, `world != allocated` and `wmip[0] == allocated`, and asserts entity capacity is smaller than required world storage; it restores the saved allocation only for safe helper cleanup, without decoding through the known undersized native pointer. That is test cleanup, not a game-source native fix. Diagnostic capture and the impossible-under-empty-table cmpf branch assertion are the only test substitutes; real allocation/types/vector/decode logic are extracted/retained. This helper does not run full load_world, config/media validation, mip generation/rendering or WebAssembly/browser startup.

The optional ASan executable was built with `-fsanitize=address -fno-omit-frame-pointer`; it timed out at 8 seconds with `ASAN_OPTIONS=symbolize=0:detect_leaks=0:abort_on_error=1`. Its timed-out process was terminated by the bounded runner. The plain browser/native helpers pass separately. Do not infer a sanitizer pass from compilation alone.

## Commands, identity and actual objects

Environment: Darwin arm64, Apple clang 17.0.0; inspected installed Emscripten 7.0.0/compiler `777e6e5db7b4990bcaeb1b9998ed642cc84e6629`. From repository root:

```sh
python3 /private/tmp/outbreak-t042-player/check.py
python3 /private/tmp/outbreak-t042-player/make-helper.py
python3 /private/tmp/outbreak-t042-player/run-helper.py
git diff --check -- source/src/worldio.cpp
```

All runner commands exit 0; the helper runner explicitly records its ASan child timeout rather than treating it as a pass. Authored entry points were read before execution. Native commands use existing source/enet/SDL framework headers, `-fsyntax-only` and optional `-D_DEBUG` against **whole worldio.cpp**. Target commands use pinned em++, `--target=wasm32-unknown-emscripten -std=gnu++11 -fsigned-char`, existing SDL2/SDL2_image PNG/zlib/Vorbis flags, source/bot/enet includes, release `-O2` or debug `-O0 -g -D_DEBUG`, `-c` and own output paths.

`EM_FROZEN_CACHE=1` forbids cache acquisition/build. Temp/TMPDIR/Node output stays under `/private/tmp/outbreak-t042-player/`. `result.json` records exact argv and command hashes, compiler/wrapper executable hashes, source/header inputs before/after, environment and object hashes. No compiler/profile/emulation flag or accepted pack input was changed.

| Actual complete-TU object | SHA-256 |
| --- | --- |
| worldio-release.o | `e4e240da0543cd597f533045a1d7c861b0bf9e163f40217517e6b7238ad4d76e` |
| worldio-debug.o | `dad265de9b466ac6af283e2d02dd4a806a2fc6b8a42f5cfff45c0993c25d8730` |

## Integration and separate observation

Engine can rebuild worldio.cpp at stable source hash `8b6d1e7aa7197be1d5030954f48662bcaab85412b222cea027762fbdb1c488c1`, relink under unchanged accepted flags/assets, and provide fresh exact pins for QA. Previous D016 failure/D017 same-Wasm diagnostic remain untouched. No actual trap recovery, frame/render/input pass or MVP completion is asserted by this worker.

Required decoder inspection also found an unrelated malformed-RLE repeat-count capacity issue; the new question note records the exact unchecked source loop. It is source-derived, not exercised as an overflow; no parser/bounds/native behavior change was attempted. It does not block this narrow ownership handoff or authorize broader fixes.

Ticket/decision/contract/source hashes were rechecked before submission. Source is stable pending MAIN acceptance or a further precise release.
