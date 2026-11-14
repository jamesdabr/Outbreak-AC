# T031 pinned SDK unsafe GL default conflicts with safe profile wording

- Author / worker: Engine & Multiplayer
- Ticket and revision: T031 0.6 plus D008 additive 0.8
- Phase and contract revision: D006 addendum 0.6; BROWSER_FOUNDATION/GOVERNANCE 0.5
- Exact clause or interface affected: D006 safe compatibility / “Do not add ... GL_UNSAFE_OPTS” and exact link flag list
- Status: OPEN (lead resolution is recorded separately)

## Question

Please approve explicit `-sGL_UNSAFE_OPTS=0` for the final link, or clarify
the intended measured profile. The inspected, pinned SDK 7.0.0
`src/settings.js:477` defaults `GL_UNSAFE_OPTS = true`. D006 describes the
profile as safe and prohibits adding GL_UNSAFE_OPTS. Omitting the flag does
not select the safe implementation in this SDK. I have not added an
unapproved option or represented a running renderer as safe.

## Evidence and impact

Exact SDK source:
`/private/tmp/outbreak-web-sdk/upstream/emscripten/src/settings.js:477`.
Its libglemu.js has separate guarded implementations under GL_UNSAFE_OPTS
and warns when unsafe emulation is selected. The first two actual link
attempts used D006's exact explicit flag list and failed at wasm-ld before
any browser/runtime execution; therefore there is no runtime/performance
result to reinterpret. Existing build documentation's “safe” label denotes
the intended contract, not a measured property of those failed links.

## Options for owner and lead

1. Approve the single flag `-sGL_UNSAFE_OPTS=0` in client-config.json/link
   commands, preserving every other SDK/port/heap/stack/pack decision.
   This matches the stated safe profile and avoids implicit unsafe default.
2. Explicitly choose the default unsafe profile with revised recorded
   compatibility expectations; worker does not recommend or assume this.

## Work paused

Final link profile only. Compilation and header/assertion evidence are
unaffected. The full 61-unit rebuild still waits for Player T034 stable
source as instructed; no GL source owned by Player is edited here.
