# D022 reaches running frames and input, but renderer diagnostics remain

- Worker: QA/Performance / `01a1b92d-28be-7110-9ac6-7ae01476c117`
- Ticket: T030 0.5, D022 exact actual-run continuation
- Status: OPEN (lead resolution separately recorded)

## Concrete remaining issue

Please assign the actual renderer diagnostics and the remaining focus/collision
observations without filtering warnings or weakening observer gates. D022's real
run no longer trapped before first frame, but it is not a renderer acceptance.

## Evidence

`web/qa/results/T030-real-D022-1.json`: exit 1, `browser_errors`, actual map
`dev_outbreak_browser`, running throughout 23 saved samples; counters advance from
frame/render 5/2 to 138/135. Runtime errors, page exceptions and stack arrays are
empty. All four actual response hashes match D022, with no failed/blocked request
or HTTP/body-capture failure.

The strict failure condition sees three console_errors: the two SDK GL-emulation
warnings and `TODO: glShadeModel`, unchanged/unfiltered. Separate browser warnings
also show **135** `WebGL: INVALID_ENUM: readPixels: invalid format`, **23**
`GL_INVALID_OPERATION: glDrawElements: Vertex buffer is not big enough for the draw call.`
and two invalid hint-target warnings. Do not attribute the result solely to benign
SDK logging: concrete GL diagnostics remain, and draw completion counters cannot
prove a correct image. No visual screenshot check or source-cause attribution was
performed.

Normal canvas click acquired pointer lock; W/S/A/D changed finite positions;
Escape released actual/diagnostic lock; normal resume click reacquired lock;
fresh W after resume moved x≈48 to x≈45.65. The about:blank-tab blur attempt sampled
`document.hasFocus()=true`, so real blur/held-key release is NOT RUN, not a pass.
D006 collision route was not attempted by this unchanged observer.

## Next scope / paused work

Assign renderer diagnosis with exact D022 artifact and retain all raw errors.
Separately release any improved focus/route observation needed after first runtime
evidence. No injected state, teleport, warning allowlist or private game API is
proposed. Correct rendering/focus/collision/audio/models/multiplayer/performance
gates remain unaccepted. Cleanup of browser/profile/server/port passed. QA made
no source/observer/build change or repeat run.
