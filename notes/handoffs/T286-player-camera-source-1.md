# Ticket handoff — T286 source ready

- Worker: Player /01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket / revision: T2861.0 / D484.
- Phase / contract revisions: STOCK_FIRST_PROTOTYPE0.4; mandatory MVP/browser documents and current ticket read before implementation; current ticket/contract reread before submission. Authoritative status unchanged.
- Base/pre-existing edits: shared working sources containing accepted camera/model work and T285 submitted gun edits. No Git command/branch/reset. Starting rendergl.cpp SHA256ed39727a835a452fb0b84f4933302cc28166bdebcf3a2a3b8a7428214446b2bf; rendermodel.cpp SHA2560db111044f5f387baa647e0a9898a9e376d7e9b74c6f205dca6db963bbd7a194.
- Changed files: ONLY source/src/rendermodel.cpp and own new T286 notes. rendergl.cpp inspected, unchanged. No overlap with Engine T287 files.
- Patch reference: notes/handoffs/T286-player-source-diff-1.md. No commit.

## Acceptance evidence

Inspected actual notes/previews/T283-chrome-camera-obstruction.png and T283-chrome-after-strafe.png: first view is filled by near-camera local-body geometry; second separates the body after strafing. Existing pale overlay is a separate T287 concern, not repaired here.

Read current recomputecamera(), moveplayer()/collide(), physical entity dimensions, renderclient/renderclientp/renderclients and outbreakthirdperson() gating. Current chase path already copies the real pose into independent ENT_CAMERA, resets before setting backward motion, performs native collision microsteps and never moves player1. No justified displacement/collision-order change was found, so camera physics/order remains untouched.

PASS source readback: the browser network third-person local-body draw is now omitted while horizontal camera/player bounding radii overlap AND their vertical bounds overlap. Horizontal clearance is actual player1.radius+camera1.radius; vertical bounds use current player eyeheight/aboveeye and camera eyeheight/aboveeye, including current crouch height. No new gameplay balance distance. The decision is recomputed per draw and restores local rendering immediately after separation.

Remote-player loop and T285 renderclientp() pistol/assault mapping are unchanged. Source readback verifies that reversing only the local-body block restores the exact starting rendermodel.cpp hash; renderclientp() remains SHA256fd96ca5298e4eaed9e334a3428bcf1c92232a57c66ca1d68a672d93a9e667556. All other pre-existing code preserved. Final rendermodel.cpp SHA256 `b230acec80e7b4ad0f6ea295f3aa0852bc81476ec541ccf8c890199b8f1c86ee`.

## Implementation status

Implemented one browser-only presentation condition under the existing OUTBREAK_NETWORK_CLIENT && __EMSCRIPTEN__ && !STANDALONE guard. Only the local renderclientp(player1) call is suppressed while overlapping; native model attachments remain part of that normal draw. Remote bodies/weapons, native/offline path, death/spectator/scoping paths, geometry collision and original stock model/skin/animation/scale/weapon selection remain unchanged. The condition reads camera/player state and modifies only a local render boolean; no entity/pose/health/movement mutation, input policy, GL state, physics, wire or asset change.

SIMULATED: none. No new tests/proof framework.

NOT RUN: compiler/helpers/tests, Wasm/native build, browser/game/service/network/FFI/runtime. Existing screenshots are pre-fix evidence, not post-fix proof. Actual bounds coverage, near-wall readability, restoration after moving away, crouch/look angles, remote visibility and attached pistol/rifle appearance remain MAIN's browser checks. Source acceptance does not establish runtime or MVP acceptance.

## Integration and questions

No new interface/dependency/asset or file outside the allowed source needed. MAIN should rebuild reviewed T285/T286/T287 source and observe an ordinary Chrome near-wall movement sequence: local model omitted only at body overlap, world remains visible, model/selected attachment returns once clear, remote actors remain drawn. T285 gun code remains stable; T287 independently addresses remaining visual-state artifacts. Stop at stable source-ready handoff; no live process or further source work. Other holds/QA remain unchanged.
