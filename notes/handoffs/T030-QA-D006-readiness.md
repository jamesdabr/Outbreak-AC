# T030 D006 route inspection and remaining runtime integration

- Worker: QA/Performance / `01a1b92d-28be-7110-9ac6-7ae01476c117`
- Assignment: inspect D006 resolution and observer readiness; T030 revision 0.5 SUBMITTED, pending actual-run identity
- Scope of this follow-up: read-only inspection and this new note only
- Runtime status: NOT RUN; no server/browser/game launched, no negative suite repeated

## Resolved geometry

D006 resolves the geometry portion of the earlier T030 question. Checked against
T027 `generate_pack.py`, original `validation.json`, map/config documentation and
the current native movement formulas:

- World 64×64; courtyard x/y `[8,56)`.
- Structure x `[26,38)`, y `[24,40)`; western solid wall x `[26,28)`, y `[24,30)`.
- Both western/eastern doors are open at y `[30,34)`; through route is
  `(16,32) → (48,32)` across x `[26,28)` and `[36,38)`.
- Radius 1.1: wall approach `(22,25)` toward +X should stop near center x ≤ 24.9.
  The y=32 through-door route has 0.9 units of lateral center margin per side
  after accounting for radius, based on the declared geometry.
- FFA starts are `(16,32,5)` yaw 90° and `(48,32,5)` yaw 270°. Team starts are
  `(16,16,5)` yaw 90° and `(48,48,5)` yaw 270°; do not assume which is selected.
- `physics.cpp` computes forward x/y from yaw−90°, so yaw 90° gives +X and
  yaw 270° gives −X. Original `browser.cfg` binds W/S/A/D to forward/back/left/right.

These are inspected geometry/source expectations, not observed collision results.
No pack generator, validator, CubeScript or native/engine binary was executed.
The previous question/handoff files were not edited.

## Prepared actual-route procedure

After MAIN supplies and authorizes the concrete accepted artifact:

1. Observe actual running phase/map/counters and starting position. Use only
   normal canvas gesture, fresh keys and mouse input. Establish the forward and
   strafe directions from source-backed spawn heading plus measured horizontal
   displacement; the frozen diagnostics do not expose yaw directly. Do not read
   private engine internals, teleport or add an observation/action API.
2. Confirm the clear y=32 approach and actual travel through both doorways. A
   player starting on the opposite side uses the mirrored approach; do not assume
   a particular random spawn or infer passage from a single coordinate sample.
3. Reach the declared clear point `(22,25)` through ordinary input, verify the
   approach position and movement direction, and observe +X motion toward the
   wall while both frame counters continue advancing. Check the D006 x ≤ 24.9
   bound while the approach remains in the solid wall segment.
4. Require the positive through-door travel evidence alongside the wall-bound
   observation. A plateau alone could be lack of input or another failure. If
   position/heading/route cannot be controlled reproducibly with normal input,
   retain collision NOT RUN and continue independent frame/lifecycle observations.

No new numerical gameplay tolerances or timing/performance thresholds are chosen
here. Actual motion/settling, heading control and browser pointer behavior remain
runtime observations.

## Concrete remaining integration needs

1. **T031 actual bundle and lead pins:** `web/build/out` is still absent at this
   inspection. Need MAIN's exact accepted build ID and SHA-256 per runtime file,
   including entry HTML/JS/Wasm/data and any other requested resource. T031's
   `index.html`/canvas `canvas` convention matches the observer's entry/canvas
   expectations. QA will not serve that root before MAIN supplies those pins.
2. **Actual runtime observations:** real bundle delivery, WebGL/asset decode,
   D005 phase/map/frame/render/position/lock trajectory, fresh-input motion and
   normal Escape/blur/resume have not been exercised by QA. Source instrumentation
   currently exposes the frozen D005 fields; no yaw/collision API is assumed.
3. **Route-specific observer integration:** the submitted observer implements
   generic movement/lifecycle observations and currently always leaves collision
   NOT RUN. It does not yet navigate the D006 route or compare its wall bound.
   Its historical message about pending collision expectations should now be read
   as pending route execution/verification, not an unresolved geometry choice.
   Route-specific code/actual measurement must be covered by MAIN's next concrete
   implementation/run direction; this inspection does not alter submitted code.

Current `game_probe.mjs` SHA-256 remains
`ef0c755c37b1293e493e1f653b411215d19d5407065a7e92249977cd7641f459`, matching the
last executed `T030-fixture-negative-2.json` source identity. No code changed, so
no negative-suite rerun was warranted. No game/render/input/collision or multiplayer
gate changes status in this follow-up. All actual-game checks remain NOT RUN.
