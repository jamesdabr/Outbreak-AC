# T114 browser bridge include spelling handoff

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket / revision: T1141.0 / D119
- Contracts: CANDIDATE_BUILD_FOUNDATION0.2/D091; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5.
- Base: reviewed b984954033c85161836542463e0250ca95baf713; original repository only. Shared worktree preserved; no Git command or commit.
- Changed source: source/src/client.cpp, exactly line8. Additional write: this own handoff only.

## Acceptance evidence

PASS — T112 terminal failure handoff and frozen evidence completed BEFORE original source change. notes/handoffs/T112-world-1.md SHA25630d28eb4ead81fc9b984bef7ae110e4f10348fb5e71b22b4c34b38b4a471e4aa; failure snapshot SHA2569b5d0e1678136a8366fed6f77a933c810e7b5493acdff169500137e64aa73515. No attempt retry or clean-root edit.

PASS — Pre-edit source SHA256 matched required9cad6a9d0acd65dd3c4902ebea805b1a7807bdc55dd31f2f9dcc606b13578183. Exactly one occurrence of the approved old include. Post-edit source is43531bytes, SHA256**2bbbf548e374ce4adb819400d435c4a6e5ae93bf26b4aaffcbe739028f72ec10**. Own stdlib byte comparison against unchanged D116 clean-root original proves replacing that single line reproduces the complete new file; every other byte remains identical. Static unified diff:

```diff
--- a/source/src/client.cpp
+++ b/source/src/client.cpp
@@ -5,7 +5,7 @@
 #if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
 #include "browsernet.h"
 #include "browsernet_observer.h"
-#include "../../web/transport/enet_ws_bridge.h"
+#include "enet_ws_bridge.h"
 #include <emscripten/emscripten.h>
 #endif
```

PASS — Same ordinary canonical web/transport/enet_ws_bridge.h,808bytes, SHA256**c1905aef1a57b0f599d2e176d90c1e8786fbfea5caf9ec12a8c36f3f7840b832**. Source/header ordinary ancestry checked by lstat. Existing fixed network command in web/build/profile_client.py lines351-353 adds web/transport to includes and emits `-I` plus absolute ROOT/include name. Its lines177-179 already pin this header identity. Thus approved short spelling uses the existing include root; no header/API/flag/dependency parser/alias gate change.

Read-only source references: profile_client.py SHA256a5d5e9c81676a96365d34fff5bfadcaa249d3e894251ae8e10ae338fc3048b34; candidate_recipe.py SHA25668ebfd201c2ee38afd370268a40f64b8b29ea91a7f027722091faf37b4e43dcb. These files were not edited or imported/executed.

PASS — Post-edit verification rechecked all6764 retained failed-browser inventory records plus its empty reserved publication against T112's immutable failure snapshot. All455 accepted-native frozen records and its separately pinned freeze/receipt also match. D116 clean-root original client.cpp retains the old required SHA. No old success/failure evidence or native preservation baseline rewritten.

## Implementation status

Implemented only approved browser-conditional include spelling. Static exact diff/hash checks complete; no new harness/tests/project script/compiler/Node/native/browser/server/network execution. No SDK/cache/other source/config/flags/pins/manifest/contract/ticket/decision/Git changes, status/selfacceptance/dispatch or source commit. Source correction does not accept the prior failed browser build.

## Integration and questions

No unresolved T114 question or interface change. MAIN reviews this new source identity and alone creates any successor commit/root/common manifest/pins and explicit new native/browser build releases. No actual retry is authorized or performed here. Player/QA holds remain unchanged. T1141.0/D119 re-read before submission; source/handoff now frozen for review.
