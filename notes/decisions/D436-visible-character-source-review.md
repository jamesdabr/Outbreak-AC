# D436 — Receive visible-character source

MAIN inspected T258 handoff and the three actual source diffs, plus physent reset, moveplayer collision/velocity behavior, existing spectator camera and local-body rendering. Receive T258 as SOURCE ONLY and close its three-file write lease. The presentation predicate leaves outbreakactive false in network builds; the separate ENT_CAMERA starts from player pose and cannot move player1; local rendering uses one call with existing survivor/weapon assets. Death/spectator/scope/edit exits retain existing camera paths. No protocol or combat change.

This is not runtime acceptance. Actual compile, camera distance/pitch/near-wall behavior, model animation/attachments, input and aim alignment still need observation. T259 is the current client-build preparation dependency. Broad proof work stays held under D434; no native/Player/QA hold is released.
