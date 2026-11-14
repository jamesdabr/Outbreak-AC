# T069 ordinary-action observability limits for later runtime

- Author / worker: Player / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket/revision: T0694.1; read-only accepted T059/T062/T065 source
- Phase/contract: browser foundation/GOVERNANCE/P0 0.5; D055; T067 future ordinary-action-only observer
- Exact clauses affected: genuine pistol/unsupported attachment cases and explicit engine audio cleanup; no private action/state calls, no new source under T069
- Status: OPEN (MAIN resolves separately); preparation itself complete, not blocked

## Question

Should the upcoming baseline leave explicit engine-quit cleanup and unavailable weapon-selection visual subcases NOT RUN, or should MAIN separately release ordinary user-facing quit/selection controls before freezing the runtime artifact? This is a decision about later evidence coverage, not a request to change frozen code or make those changes now.

## Evidence and impact

The current network-profile config binds only WASD, SPACE, C, R and MOUSE1. The shell has no quit/weapon selector. Source has a `quit` command and SDL_QUIT path, but T067 may not invoke C++/Module/console/private state; closing the browser destroys the page and cannot demonstrate the ordinary engine cleanup path or capture its final asynchronous audio result. A platform-delivered SDL_QUIT cannot be assumed merely from browser close.

MODEL exposes only three preload booleans; no selected-weapon/animation/pixel field. AUDIO exposes observed context state or null, not a successful close acknowledgment/context count. After engine context registry removal, null does not mean actual AudioContext.close resolved. Existing entry/blur paths can test input/cue loss without proving explicit engine shutdown. Stock number/wheel selection must not be assumed when its configs were deliberately omitted. Normal existing native state may make one supported weapon visible, but that does not exercise both attachments/unsupported cases.

The checklist explicitly marks these subcases conditional/NOT RUN. It also distinguishes recoverable visible blur from backend0.2 hidden/frame-gap terminal closure; no same-page rejoin or fresh capability is introduced to work around it.

## Options for owner and lead

1. Preserve the current ordinary-input baseline; record unavailable media/cleanup subcases NOT RUN and retain later human/runtime gates.
2. Separately release narrowly scoped ordinary UI/bindings and any necessary read-only observation before final build pins. MAIN defines exact files/scope and new evidence; Player does not edit accepted source/assets or add private action APIs under this note.

No telemetry/API extension is requested automatically. Hearing/pixels still require real human observation even with ordinary controls.

## Work paused

Only the unobservable future runtime subcases lack a present proof path. No runtime work is authorized here; T069 review/handoff is complete. Frozen source, data, tooling and previous evidence are untouched. This note is not execution/release authority.
