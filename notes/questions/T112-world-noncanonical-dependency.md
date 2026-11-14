# T112 browser dependency parser refusal

- Author / worker: World/Match-Systems
- Ticket and revision: T1121.0 / D116/D117
- Contracts: CANDIDATE_BUILD_FOUNDATION0.2/D091; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5; PLATFORM_DECISION0.1
- Exact clause: ONE fixed attempt; any guard failure preserves/stops without retry/patch; actual compiler dependency membership guard.
- Status: OPEN (MAIN resolution recorded separately)

## Question

The authorized actual browser attempt stopped on the exact raw dependency token `/private/tmp/outbreak-clean-D115-1/source/src/../../web/transport/enet_ws_bridge.h`. Which separately reviewed preparation correction should MAIN release before a NEW attempt? No correction or retry is authorized by this note.

## Evidence and impact

`source/src/client.cpp:8` contains `#include "../../web/transport/enet_ws_bridge.h"`. Actual `deps/03.pre.d` retains this spelling. `candidate_recipe.py` parse_dependencies rejects any token whose Path.parts contains `..` with `noncanonical compiler dependency`, before the later alias/current-byte/declared-input checks. The client compilation itself never ran. This is an observed parser gate refusal, not a compiler/link failure or a missing-input conclusion.

Exact builder ran ONCE in /private/tmp/outbreak-clean-D115-1 as T112 requires, terminal session89195 exit2. Retained failure.json SHA256cb91ecdce4f37ee0d0bf42392938526be0742dc6f9e054a08f3df807b100fbf7. Three fresh objects completed; fourth pre-scan succeeded then parsing refused. Seven recorded children exit0/reaped/bounded. No link, JS/Wasm validation, success verifier or runtime.

Post-failure inputs/source/pins/common manifest/original cache and all455 native frozen records plus native freeze/receipt unchanged. Own failure evidence snapshot: notes/handoffs/T112-world-failure-freeze.json, SHA2569b5d0e1678136a8366fed6f77a933c810e7b5493acdff169500137e64aa73515. Failed attempt and empty reserved publication preserved; no result/success freeze fabricated.

## Options for MAIN

1. Release a narrowly tested dependency spelling correction that preserves selected-root/ordinary-ancestor/link/current-byte/declaration checks before admitting any normalized token. A generic unchecked resolve/normalization would weaken the current gate.
2. Review a source include-path correction and new common source/pins instead. It likewise requires an explicit successor source and fresh candidate release.

## Work stopped

No retry, patch, source/config/flags/SDK/cache/pins/manifest/native baseline change or success-only verifier. MAIN reviews immutable failure evidence and selects any successor work. Player/QA holds remain unchanged.
