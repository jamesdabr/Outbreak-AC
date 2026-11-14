# T016 pinned SDK and first-use port setup missing

- Author / worker: Engine & Multiplayer
- Ticket and revision: T016 revision 0.3 RELEASED
- Phase and contract revision: P0 prerequisite subset 0.3; BROWSER_FOUNDATION 0.3; GOVERNANCE 0.3
- Exact clause or interface affected: T016 SDK/dependency authorization; implementation boundaries 5–6; acceptance criteria 2–3
- Status: OPEN (lead resolution is recorded separately)

## Question

Please provide the approved Emscripten 7.0.0 SDK plus prepared target ports,
or record a separately scoped acquisition/setup authorization after the exact
official installer and first-use port code have been inspected. D003 approves
the experimental SDK identity, but T016 explicitly reserves acquisition and
first-use downloads for a further recorded authorization. No such decision or
preinstalled SDK was available at inspection.

## Evidence and impact

`command -v emcc em++ emar emranlib emcmake emmake` found no tools.
`/private/tmp/outbreak-web-sdk` did not exist. The authored preflight/probe
report missing prerequisites and do not invoke an installer or compiler.
The selected pin is 7.0.0 / release metadata identity
`6afbd83493d647051772d491124187d4e9a0cda9` from D003. Compiler/port behavior
cannot yet be inspected locally. Attempts to read version-tagged official
compiler source via the web reader returned cache misses; no code was acquired
or executed from those requests.

## Options for owner and lead

1. Provide an already inspected SDK under `/private/tmp/outbreak-web-sdk`,
   configured there, with a recorded exact port/cache preparation procedure.
2. Authorize a separate inspect-first official emsdk acquisition/setup step,
   pinning installer revision, archive hashes and port sources before any
   installer execution. Expected scope: SDK writes only beneath
   `/private/tmp/outbreak-web-sdk`; target/cache writes only beneath
   `web/build/.cache`; temporary files beneath `web/build/generated/tmp`.
   No global activation/profile changes. Cleanup, if later authorized, is
   limited to these task-owned paths. Exact installer execution commands are
   intentionally not proposed as inspected: no installer has been read yet.

After provision/inspection and a concrete lead authorization, the local probe
entry point is `python3 web/build/compile_probe.py --sdk-root
/private/tmp/outbreak-web-sdk --dependency-authorization
notes/decisions/<actual-lead-authorization>.md`, from this repository root.
It invokes the pinned `em++ --version` and release/debug `em++ -c` commands
recorded in `web/build/generated/result.json`. First-use port acquisition is
the only anticipated external dependency action and requires exact approval.

## Work paused

The applied [confirm-cross-system-execution skill](/Users/jd1/.codex/skills/confirm-cross-system-execution/SKILL.md)
says: “Inspect first, explain the boundary crossing, and wait for explicit
approval before running the proposed command.” This applies to unfamiliar SDK
installer execution and first-use dependency acquisition; T016 separately
requires recorded authorization for those actions. No approval review rejection
occurred, and no installer was executed.

SDK/port acquisition and actual Wasm compiler execution only. Independent
tooling, missing-SDK validation, narrow guarded headers and native syntax
checks continue. Neither Wasm compilation nor playable browser game acceptance
is claimed.
