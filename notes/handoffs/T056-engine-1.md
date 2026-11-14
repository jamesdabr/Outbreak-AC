# T056 responsive shell and lifecycle status

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T056 2.6 RELEASED; submitted, no worker self-acceptance
- Phase / contract revisions: browser foundation/GOVERNANCE/P0 0.5 plus D035 prerequisite 2.6; D034 measured layout failure
- Base commit: 13f0d8eea4822dee5c976661218d022be74342e3. Shared tree has pre-existing worker edits; none reset or committed. Player main/audio sources remain untouched.
- Changed files: web/build/shell.html; NEW web/build/generated/t056/{fixture.html,observe.mjs,before-runtime-pins.json,result-1.json,verification.json,SHA256.json}; this handoff.
- Commit / patch: no commit/push. Stable shell SHA-256: `8772af0952c619d85ea9ae502d364d7af9117ea162caf0dab1ac1a635667a8de`.

## Acceptance evidence

| Criterion | Result | Evidence |
| --- | --- | --- |
| Initial intrinsic 960×540, responsive 16:9, max width1200, reserved status/error area | PASS, shell-only | Pure CSS flex viewport layout, size-contained canvas area and container-relative width. No DOM sizing helper or live drawingbuffer writes. Exact fixture measurements in generated/t056/result-1.json. |
| Same canvas/accessibility/module/error hooks and input boundary | PASS by inspection | id=canvas, tabindex=0, aria-label, status/alert roles, Module hooks, console output and real SCRIPT token retained. No pointer/fullscreen/input handlers added. |
| Truthful lifecycle status | PASS in fixture | Empty updates retain loaded/error/stopped. Nonempty late progress also cannot regress lifecycle state. Runtime initialization after error cannot claim loaded. Initial empty status says Starting engine; initialized text says Engine loaded — starting game, without claiming ready. Existing error text remains visible after stop. |
| Two viewport rectangles, aspect and no overflow | PASS in fixture | 1280×720: loading/loaded canvas (40,43),1200×675,bottom718. 960×540: (36.4375,41),887.109375×498.984375,bottom539.984375. All12 observations positive,16:9 within1px, entirely inside viewport, zero page scroll and document dimensions equal viewport. |
| Errors reserve space, preserve message | PASS in fixture | Error/stopped and 400-line synthetic error cases measured at both viewports; error panel scrolls internally with complete text retained. Even long-error canvas remains positive/contained: 887.109375×498.984375 at1280×720;647.109375×363.984375 at960×540. |
| Bounded installed Chrome fixture, normal security, local only | PASS | Headless Chrome156.0.8078.80, Playwright1.62.1, Node24.19.0, Darwin25.5.0 arm64. Test552.719459ms, cleanup81.089625ms. chromiumSandbox=true, no unsafe flags; actual argv recorded. Only owned ephemeral127.0.0.1 fixture URL served, page routing/CSP deny other content; zero blocked/unexpected page requests/errors. |
| Owned browser/profile/server cleanup | PASS | Browser exited, temporary profile removed, owned HTTP server closed. No timeout or forced kill needed. Actual cleanup fields in result-1.json. |
| Frozen runtime output | PASS | All17 output files, including exact D032 four runtime files and notices, match pre-test full hashes; verification.json records this. No rebuild or game/audio source edits. |
| Actual SDL/game responsive sizing, pointer/input, graphics/audio/performance | NOT RUN | Fixture uses inert SCRIPT replacement, no engine/Wasm/SDL/audio. MAIN must integrate accepted inputs under a separate release and observe the actual game. |

## Implementation status

Shell-only implementation. main fills the viewport and caps content width at
1200. Status/error panels use natural space up to25% viewport height each,
with internal scrolling for long text. Remaining area centers a canvas whose
CSS width is the minimum of available width and available height×16/9.
aspect-ratio maintains the canvas rectangle; object-fit:contain prevents
stretching if an engine later supplies a different intrinsic aspect. Initial
attributes are960×540. No JavaScript layout helper or buffer resizing exists.

Read-only SDK inspection: libsdl.js SDL_SetVideoMode calls
Browser.setCanvasSize; libbrowser.js updateCanvasDimensions writes intrinsic
dimensions and normally removes inline dimensions when native/CSS sizes
match. Its special fullscreen/forced-aspect branch may write inline important
dimensions. This ticket does not alter that behavior or request fullscreen;
the synthetic fixture cannot establish actual SDL sizing behavior. Source
paths/hashes and inspected line ranges are in verification.json.

The lifecycle marker gates progress text after loaded/error/stopped;
onRuntimeInitialized only changes a loading status. onAbort retains the
reason in the alert, onExit reports its actual code, and error listener /
printErr forwarding remain intact. These are shell presentation states,
not game readiness or a replacement for diagnostics.

## Integration and questions

No new dependency, engine/input interface, asset or build setting. No overlap
with Player T052 or MAIN T055. Existing out is frozen; MAIN owns combined
audio/shell integration after accepting exact inputs. No unresolved shell
scope question and no authority to launch an actual game test here.

Inspected own observer before execution. Executed:

```sh
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node --check web/build/generated/t056/observe.mjs
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node web/build/generated/t056/observe.mjs result-1.json
git diff --check
```

All exit0. The fixture contains exact current shell markup/style/hooks with
only SCRIPT replaced by an explicitly labeled inert comment. It serves no
game output. The observer records exact viewport/status/rectangle/scroll,
shell/fixture/observer hashes, actual browser argv/tools and cleanup. Source
and evidence pins are in generated/t056/SHA256.json, excluding itself.
The fixture PASS accepts only these synthetic shell cases; actual-game and
performance acceptance remain pending MAIN's separate integration release.
