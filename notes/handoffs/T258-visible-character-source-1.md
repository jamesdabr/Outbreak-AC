# T258 — Living browser character source

- Worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket/contract: T2581.0, VISIBLE_SLICE0.1, D435; source only.
- Changed: `source/src/clientgame.cpp`, `source/src/rendergl.cpp`, `source/src/rendermodel.cpp`, and this new handoff. No Git operations; existing prototype, browser/network/model code preserved outside the patch below. No other worker's files changed.

## Concrete change summary

1. `outbreakthirdperson()` now has a browser-network-only presentation branch for the actual living `ENT_PLAYER`, with normal spectator mode, outside demo/edit/scope. `outbreakactive()` still returns false for this build; combat/revive prototype activation is unchanged. Other builds retain the original predicate.
2. `recomputecamera()` now handles that branch with a separate `physent` chase camera. Each frame it copies actual pose/yaw/pitch, clears copied motion/input, uses a small camera collision volume, seeds backward/upward velocity from view direction, and applies ten existing collision-aware `moveplayer` steps. Only camera position moves. It returns before legacy camera handling; leaving the predicate uses the existing death/spectator/reset paths. New camera code is guarded to the network browser build.
3. `renderclients()` ORs the new living-local condition into the existing dead/reflection condition before one `renderclientp(player1)` call. Existing survivor/pistol/rifle selection is reused. Remote iteration and dead/reflection eligibility are preserved. The chase camera's `ENT_CAMERA` type suppresses the existing first-person HUD-gun path, whose gate requires `ENT_PLAYER`.

## Verification and remaining work

Source inspection: checked predicate exits, independent camera object/reset, existing collision path, existing mouse yaw/pitch copy-back to player, HUD-gun type gate, and single local draw call. `getclient()` resolves the local client to `player1`; normal remote storage remains separate. Intermission's `ENT_CAMERA` player is excluded. No public headers, dependencies, assets, protocol, spawn, combat/revive, authoritative transforms or p1 components changed.

**NOT RUN:** compiler/build, helpers/tests, native/server, browser/runtime, screenshots, input or clipping playtest. No simulated gameplay result. This implements presentation source, not a demonstrated playable build or final camera/multiplayer acceptance. The chase uses existing physics with prototype presentation offsets; near-wall/ceiling, pitch extremes, crouch, movement, scope, death and spectator transitions still require actual visual checks after MAIN's separate build/runtime release. Human Player/native/QA holds remain.

MAIN can review the three localized hunks and use T259's isolated build preparation next. Stopping without additional source or proof expansion.
