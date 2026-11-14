# T058 browser close deadline versus native WebSocket API

- Author: AI-Director; T058 revision2.8; platform contract0.1 / D039 prerequisite2.8
- Exact clause: “close clears queued bytes/timers/listeners, invalidates generation before callback races, closes real WS<=2s”
- Status: OPEN; MAIN resolution recorded separately

## Question

Browser-native WebSocket exposes close(), not terminate(). Calling close does not guarantee readyState CLOSED within2s if the peer never completes its close handshake. Unlike Node ws, this platform cannot kill a browser socket independently. Does <=2s mean deadline for backend-owned admission/queues/listeners/timers cleanup and close request, with failure reported if CLOSED is not observed, while actual socket closure remains browser-managed? Or must a separately owned page/context termination enforce actual closure on timeout?

## Evidence and impact

The approved bridge has no browser/context supervisor function or Node ws object in production. A fabricated CLOSED state or forgotten socket would not prove actual network release. Normal cooperative component server closure can be measured; it does not establish a hard guarantee for an unresponsive peer. No new close semantics/public API or page termination is implemented from this question alone.

## Options for owner and lead

Recommend explicit owner cleanup/close-request deadline, retain/report actual CLOSED observation separately, and have the component/runtime supervisor close its owned context on deadline. Alternatively approve a stricter session-owner destruction contract, which belongs to future lifecycle/supervisor scope, not the seven-function backend alone.

## Work paused

Only the unconditional unresponsive-peer actual-CLOSED<=2s claim awaits clarification. Continue new platform/header implementation, compiler checks, simulated ownership/bounds tests and cooperative real-wrapper component evidence. No gateway/native/game/ENet parser execution.
