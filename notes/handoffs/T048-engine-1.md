# T048 exact standalone ws source inspection

- Worker: Engine & Multiplayer
- Ticket/revision: T048 2.0 RELEASED; source-inspection submission only, not self-accepted
- Authority/context: AGENTS; D025 read-only acquisition addendum2.0 to governing browser foundation/GOVERNANCE/P0 0.5; accepted T044 static report/question
- Changed paths: NEW web/transport/ws-inspection/** metadata/archive/source-as-data/inventory/report; this NEW handoff only
- Engine/build/QA/server/assets/contracts/decisions/old notes: no writes
- Package import/execution/npm/install/lifecycle/constructor/client/server/listener/gateway: NOT RUN
- No commit/push/reset/revert, other-worker dispatch or credential/mirror/version fallback

## Results and evidence

| Acceptance area | Result | Evidence |
| --- | --- | --- |
| Exact official version metadata/archive identities and limits | PASS | Both approved registry.npmjs.org URLs returned HTTP200, verified TLS, no redirects. Name/version/tarball exactly ws/8.21.0/approved URL. Metadata2384 bytes <=256KiB; archive34987 bytes <=2MiB. Raw headers/body/transfer JSON/stderr preserved. Initial sandbox DNS failure exit6 retained; exact-URL scoped retry succeeded. |
| SHA512 SRI before safe bounded extraction | PASS | Exact metadata SHA512 matches actual compressed archive before tar processing. Gzip output bounded, all19 members prevalidated, relative contained package/ only; no links/specials/escapes/duplicates/file-parent conflicts. Actual151087 regular bytes <=16MiB, members19<=128, both registry counts match. Extracted files mode0600, none executed. |
| Source/license/manifest/modules/scripts/addons and hashes | PASS — static | acquisition-and-inventory.json pins every19 file. module-inventory.json pins all16 JS/MJS files and their require/import locations; all relative targets contained/exist. Node root closure index.js+13 lib modules. Exact exports, MIT LICENSE, three dev scripts/no install hooks, optional bufferutil/utf-8-validate peers and their import-time guards inspected. No install or module resolution executed. |
| Initialization/options/parser/backpressure/close compared with real bundle | PASS — source inspection only | REPORT.md provides exact standalone file/line anchors. bundled-comparison.json checks actual accepted bundle/sidecar hashes, 11 module-scoped implementation conditions and full MIT body. Bundler variable renaming/formatting are explicit; no whole-source equivalence or runtime purity claim. Standalone avoids the utility bundle's unrelated eager fs/global utilities. |
| Exact parser-limit caveats retained | PASS — static | maxFragments counts nonempty retained payload buffers, not all WS frames; maxBufferedChunks counts queued TCP chunks, not bytes. Payload limits are not connection memory/CPU/rate budgets. Admission/origin/protocol/version/queue/control/liveness/ENet-allocation policy remains complementary future contract work. |
| Bounded future pure-JS import/self-test proposal, honest unexecuted state | PASS — proposal only | REPORT and future-runtime-proposal.json identify existing pinned Node path/hash, direct exact entry path/hash, clean environment with both addon-disable variables, import-only<=5s/output<=64KiB, no constructor/listener/client. Separate <=10s loopback dependency test is proposed, not released/run. No gateway/interface implemented. |
| Current fingerprints / unrelated runtime preservation | PASS | Final19 member hashes rechecked; final-verification.json records no source execution and exact web/build/out preservation against runtime-freeze.json. git diff --check passes. Current T040 output remains frozen; T040 preemption still takes priority when MAIN accepts the graphics source fix. |

## Exact acquired identity

- Metadata URL: `https://registry.npmjs.org/ws/8.21.0`
- Metadata SHA-256: `93704f27b5aefb9970f720af5e59f1078d08585e1d6452b9fec3b26c6578bf17`
- Archive URL: `https://registry.npmjs.org/ws/-/ws-8.21.0.tgz`
- Archive SHA-256: `d08b726b3aae3a0fed5218a0d9a4b2ac8d75d4ad453a9271db55fe38e94eb4cf`
- Expected/verified SRI: `sha512-Vsp28b7DRcimFQvrqu2Wek3z1iYxDCWqHYB8Qsnk/S4RfaCQzPGPyBNuVjJV3cd6UiKtUtp6sNM77gWvzcCH+g==`
- 19 regular package members / 151087 uncompressed bytes / no native binary or dependency install
- Registry signature fields preserved, but independent signing-key verification NOT RUN; SRI/TLS do not establish runtime behavior

Successful curl commands used env -i PATH=/usr/bin:/bin, /usr/bin/curl -q,
HTTPS-only protocol, TLS minimum1.2 with default certificate verification,
max redirects0, timeout30s and exact size caps. Exact argv/stdout/stderr paths
are in acquisition-commands.json. Only those two successful official HTTP
requests occurred; no GitHub/readme links or alternate hosts were fetched.
Stdlib source validation/extraction inspected tar data and wrote contained
regular files; it never imported acquired JS/package code. Package scripts
were read as manifest strings, not run. No npm command was used.

## Material findings for MAIN

Standalone source provides the same relevant parser mechanisms and caveats
as T044 without Playwright's eager unrelated utility initialization. Default
CommonJS export is the WebSocket class with Server/WebSocketServer aliases;
the ESM wrapper supplies named exports. Browser.js is deliberately an error
stub; browser clients use native WebSocket. Exact module entry/hash must be
pinned rather than relying on bare package-name resolution.

Before any later import, set WS_NO_BUFFER_UTIL=1 and
WS_NO_UTF_8_VALIDATE=1 in the child environment. The validation code can use
Node's builtin buffer.isUtf8 when present. “Pure JS” here disables optional
package native addons; Node native builtins remain the selected runtime.
No optional-addon absence/side effects were measured by execution.

False handleProtocols does not reject an upgrade; WS8 and13 are accepted by
default; path comparison strips query and there is no restrictive default
Origin. Caller-owned admission and resource policies must be explicit before
any future UDP/session allocation. send does not return a drain Boolean;
buffer sharing/backpressure and caller-owned teardown remain real concerns.
Server.close does not terminate clients/close a supplied HTTP server.
No normal loopback self-test can waive the parser frame/rate/byte caveats or
ENet reassembly/allocation limits.

Future-runtime-proposal.json pins the existing Node24.19.0 executable and
entry member by SHA-256 without executing either for this task. The proposed
import-only child and later loopback self-test both need new explicit release.
The package remains inspection material; no runtime vendor/transport choice
or gateway implementation is approved by this submission.

## Reproduction / remaining work

Read REPORT.md, acquisition-and-inventory.json, module-inventory.json and
bundled-comparison.json under web/transport/ws-inspection. All19 exact file
hashes and raw official response identities are retained for independent
rechecking. No current acquisition/inspection blocker exists and no version
substitution is proposed.

Runtime import/availability, network parser enforcement, liveness/backpressure/
cleanup, browser transport, session/ENet allocation limits and multiplayer
remain NOT RUN. MAIN owns acceptance and any follow-up runtime/transport
contract. T048 remains RELEASED until MAIN updates status; ticket2.0 and D025
were reread before submission. No prior report/question/handoff was overwritten.
