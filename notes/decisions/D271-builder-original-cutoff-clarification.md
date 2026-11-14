# D271 — Bind the existing builder cutoff exactly

Resolve immutable `notes/questions/T177-engine-original-reap-cutoff-1.md`. MAIN rechecked both actual baseline Effects.run methods: Blackwood and default-dev each set `hard=min(commandStart+120,wholeStart+3600)`, with `work=hard-5`. D269's phrase “original60s cutoff” was an incorrect description imported from the separate G1 proof. It does not impose a new60s builder cutoff or grant waitEntry+60. The exact existing hard value is passed unchanged to strict consuming reap for BOTH builders; no new clock, time allowance, grace or reset.

The independent6000-observation ceiling and <=0.01s pauses remain additional finite limits, always clipped by that original hard deadline. A helper may exhaust its observation bound sooner; it cannot extend the original command/whole budget. All pre-call checks, immediate truthful consume facts, post-call cutoff/refusal and no-expired-effects rules remain. Full guarded and separate focused jobs retain their own original300s limits, not actual builder budgets. No case/schema/API/acceptance change.

Closure0.3/T1771.1/T1781.1 reflect this routine technical clarification. T177 continues its already released correction; T178 remains READY pending explicit release. Question note remains unchanged. No other historical permission is reopened; holds unchanged.
