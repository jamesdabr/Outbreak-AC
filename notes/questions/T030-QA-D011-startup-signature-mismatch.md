# First real D011 artifact fails before first frame

- Author / worker: QA/Performance / `01a1b92d-28be-7110-9ac6-7ae01476c117`
- Ticket and revision: T030 0.5, actual-run continuation authorized by D011
- Phase and contract revision: P0 browser prerequisites; D005 schema / D011 exact artifact run
- Exact clause affected: T030 real startup/frame/map observation, D011 instruction to retain first real error and report for lead fixes
- Status: OPEN (lead resolution recorded separately)

## Question

Please assign source/toolchain diagnosis for the actual startup error
`RuntimeError: function signature mismatch`, then provide a newly verified
artifact identity/pins for the next run. No source or observer change was made.

## Evidence and impact

`web/qa/results/T030-real-D011-1.json`, exit 1, is the first cleared actual-engine
run of artifact
`8792410f512392c628063109856fc3e65d97a037590ff0f9d376f4e70a8e637c`.
All four actual HTTP response hashes match D011's HTML/JS/Wasm/data pins. Only
those four local files were requested; all returned 200, with no blocked request,
HTTP failure or failed request.

The first diagnostics sample is `phase: error`, `frame_count: 0`,
`rendered_frame_count: 0`, `map_name: ""`, `player_position: [0,0,0]`,
`input_locked: false`; runtime_errors contains exactly
`RuntimeError: function signature mismatch`. Browser page exception is
`function signature mismatch`. No stack/source callsite was captured by the
unchanged observer, so the responsible call cannot be identified from this
evidence alone.

Console also records two Emscripten GL-emulation warnings and `TODO: glShadeModel`;
WebGL warnings include two `INVALID_ENUM: hint: invalid target` entries. These are
distinct from the fatal signature error; no causal claim is made.

## Options for owner and lead

Assign a narrowly scoped real-runtime diagnostic/source fix to the responsible
owner using this exact artifact and fatal error. If additional stack/symbol
capture is needed, release that specific diagnostic action rather than weakening
the existing observer. Rebuild/reverify and provide fresh pins before rerunning.

## Work paused

Actual frame/render/map, input/focus and D006 collision-route checks are blocked
by startup. Audio/models remain intentionally omitted; multiplayer/authority/
performance remain unverified. Owned browser PID 61271 and server PID 61296
stopped, the temporary browser profile was removed and the server port closed.
