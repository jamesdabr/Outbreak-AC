# T177 strict reap original cutoff binding

- Author / worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket and revision: T1771.0/D269.
- Phase and contract revision: BLACKWOOD_BUILD_PREPARATION0.2; BUILDER_TERMINAL_GROUP_CLOSURE0.2.
- Exact clause affected: D269's “WNOHANG at most6000 observations, pauses <=0.01s inside original60s cutoff” and “no fresh wait budget,” versus the unchanged Blackwood Effects.run original command120s/cleanup-inclusive hard cutoff.
- Status: OPEN (MAIN resolution recorded separately).

## Question

Please bind the exact deadline argument for Blackwood's strict consuming helper. Current source sets hard=min(commandStart+120,wholeStart+3600), work=hard-5. T177 requires preserving those caps, while D269 names an original60s cutoff. Making reap use commandStart+60 would reject otherwise timely commands that finish after60s; granting waitEntry+60 would create a fresh budget the decision forbids.

## Evidence and impact

Current recipe source is the preserved T177 baseline aae1f95b4e2de3ae6a32a395d72257f221ff53a98afc499b4d56ab8dd1d0333d. All source/history is still unchanged in this task; no test has run. Read-only baseline/review/fake-boundary inspection can continue independently. Only the helper's exact clock binding and its expected cutoff cases need this clarification before source freeze/invocation.

## Options for owner and lead

Recommended: Blackwood strict wait receives the existing original hard=min(commandStart+120,wholeStart+3600) directly, never resets it, and additionally has the fixed6000 observation/0.01s pause ceilings. Default-dev receives its existing original cutoff. Treat “60s” as describing that other builder's existing bound, rather than a new Blackwood command cutoff. All sleeps/checks/publication remain within the passed original cutoff. No new time allowance, protocol or API field is proposed.

Alternatively MAIN may explicitly require a separately specified tighter Blackwood reap deadline and state its reference point/precedence without silently changing the preserved command120s contract. This note adopts neither alternative.

## Work paused

Affected helper deadline binding/source freeze and both jobs await this narrow recorded resolution. No retry, test, source implementation or actual effect follows from this question. Other read-only preparation continues; no worker negotiation or authority amendment.
