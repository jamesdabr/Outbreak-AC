# T038 browser setfont command ABI — stable source/object handoff

- Worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T038 1.1 RELEASED; submitted for MAIN review, not self-accepted
- Governing baseline: AGENTS, browser foundation/GOVERNANCE/P0 0.5 and D012 additive 1.1; D011 actual startup-failure evidence.
- Base: `13f0d8eea4822dee5c976661218d022be74342e3` plus current accepted dirty tree. rendertext.cpp had no pre-existing diff and SHA-256 `46147ee0f587893edcafd01d29b673d6f91e76f85d2e550c0012786e890549e6`.
- Changed repository source: `source/src/rendertext.cpp`, only guarded command registration/private wrapper following existing setfont.
- Final stable rendertext.cpp SHA-256: `b8d6481f8681b3b7223d5d75f1a46b67417252dd10e39b22598b0f43e4d36e68`.
- New note: this handoff. Evidence/patch: `/private/tmp/outbreak-t038-player/` (`T038.patch`, `result.json`, `check.log`, `start-hashes.json`, actual objects/IR and helper logs).
- No other source/build/QA/assets/contracts/decisions edited; no commits/push/reset/revert, downloads/cache additions, service/browser launches, emulation flags or error suppression.

## Acceptance evidence

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1. ABI-correct browser registration/native/direct behavior | PASS — source/target IR/helper | Browser registers `COMMANDN(setfont, setfontcommand, "s")`; private `void setfontcommand(char*)` calls real bool setfont and discards the ignored result. Public command name/signature and bool function body remain unchanged. Native partial-preprocessed source is byte-identical to the pre-edit file. No font/config bypass. |
| 2. Actual native and target compilation/stable evidence | PASS | Native release/debug syntax and actual Emscripten release/debug whole-rendertext.cpp objects all exit 0 with empty diagnostics. Both objects have Wasm magic; full source/header fingerprints are unchanged during each compile. Tool, argv and object hashes are in result.json. Additional real target LLVM IR proves wrapper void return, direct bool return and actual registration reference. Extracted helper passes browser/native selection tests. |
| 3. Other retained startup command inspection | PASS — read-only review | Audited actual retained config commands, registration macros and dispatcher against source declarations; detailed results below. No second concrete mismatch found in this bounded set. Exact attribution of D011's first runtime fault remains INFERRED, not proven by objects/helpers. |
| 4. Immutable stable handoff/scope | PASS — submission supplied | Stable source hash above; exact patch/commands/logs/hashes provided. T028/T034 source and all D003-protected combat hashes remain unchanged. Governing ticket/decision hashes rechecked before submission. MAIN owns acceptance, Engine rebuild/link and subsequent exact-pin QA. |

## Change and target ABI evidence

Only browser builds replace the registration target:

```cpp
#ifdef __EMSCRIPTEN__
static void setfontcommand(char *name)
{
    (void)setfont(name);
}
COMMANDN(setfont, setfontcommand, "s");
#else
COMMAND(setfont, "s");
#endif
```

The actual target debug IR in `rendertext-debug.ll` defines:

- `define hidden ... zeroext i1 @_Z7setfontPKc(ptr ...)` — existing direct bool API.
- `define internal void @_ZL14setfontcommandPc(ptr ...)` — the string-command wrapper.
- The static registration calls real addcommand with `ptr @_ZL14setfontcommandPc`.
- The wrapper calls real `_Z7setfontPKc`; it neither fabricates a font nor reports a different result through the script API.

This corrects the source-proven Wasm indirect-call return mismatch without broad dispatcher changes. It does **not** prove that this callback was the first failing D011 indirect call: that remains a source-supported inference until the corrected real browser startup is observed.

## Retained startup registration audit

Read-only scope: original `config/browser.cfg`, `config/font.cfg`, `config/default_map_settings.cfg` and `packages/maps/dev_outbreak_browser.cfg`, plus their native declarations/registration macros. `audited-configs.json` records the precise config hashes and command sets; no configs or inherited scripts were executed.

| Commands | Registration/declaration review |
| --- | --- |
| font | `COMMANDN(font,newfont,"ssiiiiii")`; void newfont with 2 string pointers + 6 integer pointers. Matches dispatch's 8-pointer/void target ABI. |
| fontchar, fontskip | void functions with respectively 4 and 1 int pointers; `iiii`/`i`. Match pointer arity and void result. |
| setfont | The concrete bool-result mismatch addressed here. Original font.cfg executes `setfont default`. |
| keymap | void `(int*,char*)`, `is`; 2-pointer/void target ABI. |
| bind | COMMANDF-generated static void `(const char*,const char*)`, `ss`; 2-pointer/void target ABI. Bound movement actions are stored at startup, not executed by bind. |
| scriptcontext, isolatecontext | void `(char*,char*)`/`(char*)`, `ss`/`s`. Match pointer arity and void result. |
| sealcontexts | COMMANDF-generated void zero-argument wrapper. |
| mapmodelreset | direct void zero-argument function. |
| mapsoundreset, texturereset | COMMANDF-generated void zero-argument wrappers. |
| texture | COMMANDF-generated void `(float*,char*)`, `fs`; 2-pointer/void target ABI. |
| fov, sensitivity, hudgun, audio, soundvol, musicvol, dynshadow, stencilshadow, waterreflect, hideradar, hideigraphs, hidecompass, hideteam, autodownload, fog, fogcolour | Variable registrations use dispatcher variable paths, not a bool-return string-command target. VARF-family setters generate void zero-argument hooks where present. No concrete return/argument mismatch found in these inspected paths. |

Also inspected the stored movement/fire/crouch/jump actions' `d` dispatch shape: source functions are void(bool), matching the special void(bool) dispatcher; reload is a void zero-argument COMMANDF wrapper. These checks are bounded to retained startup/config/input registrations, not a claim that all project commands or runtime callbacks are ABI-audited. No speculative changes were made elsewhere.

## Actual checks and reproduction

Environment: Darwin arm64; installed Apple clang 17.0.0; pinned inspected Emscripten 7.0.0/compiler `777e6e5db7b4990bcaeb1b9998ed642cc84e6629`. From repository root:

```sh
python3 /private/tmp/outbreak-t038-player/check.py
python3 /private/tmp/outbreak-t038-player/helper.py
git diff --check -- source/src/rendertext.cpp
```

All exit 0. Authored entry points were read before execution. Compiler logs are empty. Exact subprocess argv, SHA-256 of serialized argv, SDK compiler/wrapper executable hashes, source/header hashes before/after, environment and object hashes are saved in `result.json`.

Native commands use `clang++ [-D_DEBUG] -fsyntax-only`, existing repository source/enet/SDL framework includes, `-Fsource/xcode/Frameworks -idirafter source/include`, and actual rendertext.cpp. Native `unifdef -U__EMSCRIPTEN__` output is byte-identical to the baseline, including original registration/direct function.

Actual target commands use the inspected installed em++ with `--target=wasm32-unknown-emscripten -std=gnu++11 -fsigned-char`, existing SDL2/SDL2_image PNG/zlib/Vorbis flags and repository source/bot/enet includes; release `-O2`, debug `-O0 -g -D_DEBUG`, `-c rendertext.cpp`, own output paths. The supplemental ABI check uses the same target/ports/debug flags with `-S -emit-llvm` and own `.ll` output. `EM_FROZEN_CACHE=1` forbids cache population; temp/TMPDIR/Node output remains under `/private/tmp/outbreak-t038-player/`. No broad callback-emulation/compiler flags were added.

| Actual object | SHA-256 |
| --- | --- |
| rendertext-release.o | `ec693ea694cf1e0f6108c0c1ef6b2dc74b9e7009dd759daaa44e8f21afd0e0fe` |
| rendertext-debug.o | `cd9d7449837b85518c5dd3282fc85143fdf0ad941800eba60d1cb90785e8871c` |

The tiny extracted helper uses the **real unchanged setfont function body and actual scoped registration source**, with a fake two-font registry and real command macro shape. It checks successful font selection, missing-font false/direct behavior and unchanged current font, unchanged public script name/signature, native original registration and browser void wrapper declaration/call. It is helper evidence only: no texture decode, actual font.cfg execution, linked engine or browser startup was run by this worker.

## Integration and outstanding evidence

MAIN can relay stable rendertext.cpp hash `b8d6481f8681b3b7223d5d75f1a46b67417252dd10e39b22598b0f43e4d36e68` to Engine for the affected-object rebuild and same-profile link. Previous exact D011 artifacts/evidence remain untouched. The corrected build requires fresh artifact pins and QA's actual real-browser run; zero-frame failure resolution, map rendering, movement/input and full MVP remain unproven here.

No new question is needed: source matches D012 and no additional concrete mismatch was found in the inspected retained set. Keep this source stable pending MAIN review or a further precise ticket.
