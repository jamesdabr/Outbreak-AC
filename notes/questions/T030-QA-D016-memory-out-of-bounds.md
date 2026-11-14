# D016 corrected artifact reaches map-read log then traps

- Author / worker: QA/Performance / `01a1b92d-28be-7110-9ac6-7ae01476c117`
- Ticket: T030 0.5 continuation, D016 exact actual-run release
- Governing observation: D005 schema, accepted T037 evidence capture
- Status: OPEN (lead resolution separately recorded)

## Question

Assign diagnosis/fix of actual `RuntimeError: memory access out of bounds` from
the corrected D016 artifact. Its first captured stack location is
`index.wasm:wasm-function[3179]:0x1714c9`. No source callsite is inferred from a
function index alone. Additional symbolization/debug-build activity needs the
corresponding lead scope and artifact identity; QA has not executed it.

## Evidence and impact

`web/qa/results/T030-real-D016-1.json`, exit 1, artifact
`T040-3800e5ef78bcb84033e30c72e276ebebc342b6f97185fbfcb434de021d87a7ab`.
Actual diagnostics: phase error, frame_count 0, rendered_frame_count 0, empty map,
position [0,0,0], unlocked input, runtime_errors containing the exact memory trap.

Informational console reached:

```text
read map packages/maps/dev_outbreak_browser.cgz rev 1 (32 milliseconds)
Outbreak original browser courtyard proof
```

This is a loader log, not proof of a running/fully loaded/rendered map. The prior
D011 signature mismatch was not the first captured failure in this corrected
run; the engine still did not recover to frame/render/input acceptance.

The full stack and eight startup info entries are retained. GL-emulation,
glShadeModel and INVALID_ENUM warnings also remain unfiltered. Local preflight
matched all four D016 file pins; response hashes captured for HTML/JS/Wasm match.
The saved data response body was unavailable to the observer and index.data also
reports ERR_ABORTED. All four server GET logs say 200. Do not claim complete
four-file response-hash verification or assign a cause to the data-capture error
from this evidence alone.

## Options / work paused

Use the captured real stack for the next narrowly scoped diagnosis, then provide
new verified pins if rebuilt. Do not change source/observer gates or filter the
warnings to manufacture success. Actual frames/rendering/input/collision remain
blocked; audio/models/multiplayer/performance remain omitted or unverified. Owned
browser/profile/server cleanup passed. No patch or repeat run was performed.
