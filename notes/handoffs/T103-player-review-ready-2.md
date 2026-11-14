# T103 — REVIEW-READY2 before freeze

- Worker: Player / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e.
- Ticket / revision: T1031.2/D151 same unfrozen four-file lease; review checkpoint, no authoritative status change.
- Phase / contract revisions: GOVERNANCE/BROWSER_FOUNDATION/P0 0.5 prerequisite only, BROWSER_CAPABILITY_PROBE0.2, D108/D148/D151. No policy/scope amendment.
- Base commit and pre-existing edits: continuation of REVIEW-READY1 existing partial four files; its observed HEAD was bdaa8df7ec39d9408f97feda4560832d7ef26c3c. No Git changes/commits performed by this worker. Original preparation-1/handoff/questions retained; other project/source/tools/evidence read-only.
- Changed files: exactly probe.cjs/test.cjs/SCHEMA.md/README.md, NEW preparation-2 and preparation-3 evidence, preparation-node-cache-2/3 and empty preparation-temp-2/3, this own new handoff. No old evidence overwrite.
- Commit or patch reference: none authorized/created.

## Acceptance evidence

PASS (FIXTURE_ONLY): inspected pure builtin/VM fixtures using exact installed Node24.19.0 SHA27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1. Preparation-3 exit0,113 named PASS cases, stderr empty, VM host effects/import attempts0. Original79 case names/order remain identical;34 focused regressions added. Exact invocation/environment/stdout in preparation-3/invocation.json. macOS arm64 preparation only; no hardware/performance acceptance.

PASS (preservation): all25 referenced identities agree before/after and were rechecked before this handoff. Graph binds D151/findings, prior handoff and original preparation-1 receipt/reference/invocation, preparation-2 before-reference/failure files, own four files and installed reference source/tools. Original preparation-1 receipt remains SHA6fdb48a89d6d6b1113210f0d055c607ebe0c520c6390b64bec7c79ccb4f3affc. Prior source hashes remain in historical records; no historical handoff/receipt rewritten.

FAILED INTERMEDIATE (preserved): preparation-2 exit1, assertion expected stopped acquisition refusal at entry but observed acquisition cutoff in the deferred factory. No resource started; source needed an explicit acquisition-entry stop gate. Added that gate, retained preparation-2/references-before.json and failure.txt, then used NEW preparation-3. No preparation-2 receipt fabricated and no failed outcome relabeled PASS.

| Returned finding | Implemented correction / regression evidence |
| --- | --- |
| CDP detach after cold page.close | Actual private releasePage detaches its owned session while page lives, then closes page. sessionOwnership observes public close events and explicit detach completion, handles prior automatic disposal without a second detach, preserves unrelated detach errors. Fixtures model real page-close automatic session disposal, successful explicit detach with queued close event and transport failure. All session cleanup precedes page/context teardown. |
| Eager raced resource promises / deadline grace | operationScope receives deferred factories; checks work/total cutoff before invocation, with no1ms grace. acquire registers BrowserServer/connection/context/page/CDP promises, retains handles before returning and continues observing timeout results; late handles are retained/disposed within the original cutoff. Stopping forbids new acquisition, drain is bounded to10s and total120s; unresolved/rejected/failed disposal facts prevent clean closure. Eight actual acquisition kinds have delayed-result regression cases; separate tests cover cutoff before invocation, per-operation cutoff, failed disposal, unresolved drain and post-total-cutoff refusal. Helpers are private and receive fake clock/timer/effects in tests. |
| Retained root birth overwritten on PID reuse | selectOwned bootstraps only an empty retained set; existing PID rows must match original birth/command. retainOwned keeps original identities and freezes new copies; merges cannot replace retained root/descendant identities. Fixtures exercise reused root with identical command/profile, reused descendant and immutable merge/refresh; signalPlan excludes changed births. |
| First scan failure loses public root recovery | Public BrowserServer handle immediately retains process/provisional PID,parent PID,executable,profile,spawn command before first ps. observeOwned/refreshOwned recover only that still-live public root with matching exact current parent/PID/command/executable/profile and any previously retained birth, then descendants. Failed recovery cannot fall through to bootstrap. Fixture's actual observeOwned sees a first scan exception, fake normal close fails through actual operation helper, second scan recovers only owned root/child. Dead/signalled/wrongPID/parent/command/profile/birth negatives adopt/signal no unrelated row. |

## Exact review identities

| File under web/qa/capabilities/T103 | Bytes | SHA256 |
| --- | ---: | --- |
| `probe.cjs` | 43568 | `506f4d1dd4105cc1d68733e79edf012080646d7e796ce684e770880848909a4e` |
| `test.cjs` | 32019 | `29af0a40f779d053e9bade349d3c3e95bfeddaac1c3ad5f1d8c0b742fa57ef1d` |
| `SCHEMA.md` | 14543 | `fa6b24717a093e1c896248c0416befc56622558febe0d67530ab8105290be292` |
| `README.md` | 3738 | `eb45ed7bd9d2410ff24d08cdf109cb68149f69b61b44502b8b3ff919949aa624` |
| `preparation-3/receipt.json` | 25823 | `76696ec641794af7b4ba686dd27dee01382cf4cc9f64ea82d5c2ca6162b476ee` |
| `preparation-3/references-before.json` | 4899 | `0ddcfe5209123c96e13b374d04ee37022d1cf47951c22556976704a60927c279` |
| `preparation-3/references-after.json` | 4899 | `0ddcfe5209123c96e13b374d04ee37022d1cf47951c22556976704a60927c279` |
| `preparation-3/invocation.json` | 845 | `4a12f134a853daa48d65eee6fd28eba815dad9ffcaa890c74f84ce60a6302413` |
| `preparation-2/failure.txt` | 393 | `8874d8c1f34d2cdab5f0fa206a6416a9cb07e44e5405b90bd76ac9e0c86ed7f9` |

## Implementation status

Implemented source remains UNRUN against host APIs. Existing fixed topology, one same-origin guarded iframe, exact flags/guard/cache/GPU/120s/evidence limits remain unchanged. New private helpers are tested through VM-only exposure and are not public exports. Private schema documents acquisition/session/provisional ownership fields.

Simulated: all113 current cases are FIXTURE_ONLY/actual_browser:false. Fake Page/CDP/server/process/clock/promise facts exercise actual internal helpers; no Playwright/http/net/child_process import, actual process/browser/listener/socket/service or real runFixedProbe call. Test driver uses only Node fs/vm/assert/crypto/path plus source reads and owned preparation writes. Installed Playwright session/source was inspected read-only, not executed.

NOT RUN / incomplete: installed Chrome enforcement, actual late-resource/session/process lifecycle/closure, cache/HTTP/WS/GPU/iframe capability, game/P0/performance/RSS gates. The full effectful future runner is not proven by helper fixtures. Unresolved acquisition/disposal is explicit failed cleanup, never clean-closure proof. D108 early raw browser output remains NOT_OBSERVED/PUBLIC_HANDLE_NOT_AVAILABLE_EARLY/complete_byte_bound_proven:false and overall scope PARTIAL.

## Integration and questions

No shared/public API, dependencies/assets, browser flags, private Playwright API, network target, existing controller or policy change. D108 questions remain resolved and originals unchanged. No new question required for these exact D151 corrections.

Exact inspected invocation is recorded in preparation-3/invocation.json and README. Preparation attempts1/2/3 are once-only; preserve them. This submits REVIEW-READY2 before freeze and waits for MAIN clearance. Actual run-1 and every preparation freeze remain absent. No actual probe or QA resumption is authorized/requested by this handoff; no self-acceptance.
