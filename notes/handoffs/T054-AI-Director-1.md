# T054 transport proposal handoff

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b
- Ticket/revision: T0542.5 RELEASED, proposal-only; governing browser foundation/GOVERNANCE/P0 0.5 + D033 prerequisite2.5. Re-read current ticket before submission; authoritative status untouched.
- Base: 13f0d8eea4822dee5c976661218d022be74342e3 plus shared pre-existing edits and concurrent accepted/released work. No source, dependency, build, asset, ticket, decision, runtime or other worker file changed by this assignment.
- New deliverables only: [proposal](/Users/jd1/code/apps/outbreak/notes/ticket-proposals/transport-next/T054-transport-proposal.md), [draft ticket split](/Users/jd1/code/apps/outbreak/notes/ticket-proposals/transport-next/T054-draft-tickets.md), [freeze questions](/Users/jd1/code/apps/outbreak/notes/questions/T054-AI-Director-transport-freeze.md), this handoff. No commit/dispatch.

## Acceptance evidence

**PASS proposal scope:** inspected genuine ENet Unix/platform signatures, scatter receive/send semantics, compression scratch-buffer boundary, both fragment allocation paths, packet/command/bitmap/refcount/drop/reset paths, default abort-on-OOM, packet logger retention and game gzip boundary. Source citations in proposal support concrete implementation consequences; no borrowed current-version ENet host-limit API assumption. Distinguishes ws4096 payload,16 nonempty fragments,32 TCP chunks from raw bytes/control rate/queues and native1GiB reassembly. No unsupported total memory/CPU claim.

**PASS interfaces/ownership proposal:** exact six-function private C/JS bridge and C++ lifecycle surface, complete existing platform export inventory, --js-library/normal core link strategy, single opening logical socket/host then real ENet connect after WS OPEN. Client.cpp owns JOINING; actual post-parse SERVINFO/CONTD/WELCOME/SPAWNSTATE milestones own ACTIVE. Explicit no-local-fallback/respawn/server-slice/auth-privilege boundaries and network-only timing; genuine native no-key handshake stays unchanged. Includes CONNECT's disconnect(1) teardown trap and keeping handshake/control sends enabled before ACTIVE. Ticket bodies specify exclusive files, acceptance, predecessors and future execution boundaries; no assignment implied.

**PASS updated narrow sequence:** MAIN feedback incorporated without changing contracts. Initial proof is supervisor-owned trusted normal traffic/exact original map on unchanged T051 release executable; -c2 configuration still requires a separate runtime pin/release. B core hardening and E2 native diagnostics are later branches, not handshake prerequisites. Gateway0.1/D037/T057 is now independently approved/released and takes precedence over A's retained draft. Its actual config is schema_version/run_id/capability_sha256 only. MAIN verifier/QA hold and Player T052 main/audio + Engine T056 shell ownership remain explicit; disjoint backend can precede lifecycle integration.

**PASS genuine-proof plan:** distinct actual server-assigned cn/session/ENet identities and UDP tuples, actual native-mediated A→B/B→A parsed movement, real welcome/map/spawn, disconnect/removal/reconnect and owned shutdown/ports/files. Dependency echo/component/malformed tests never substitute. Existing native binary cannot expose internal clientsequence/cache; NOT RUN for those fields, with optional later read-only derivative proposed. It cannot simultaneously be called unchanged and instrumented.

Gateway0.1 consumes only two one-use caps and has no refresh API: proposal explicitly reconnects through fresh gateway/config/run_id/two caps and fresh page/Module boots after both old native actors clear. It does not silently add cap refresh or claim continuous B during A-only rejoin; that stronger case remains NOT RUN without a new contract. This is a concrete feasibility sequence, not a request to change Engine's current release.

**PASS documentation check:** git diff --check passes. Current T054 remains2.5 RELEASED. All verification commands in proposal are labeled future, not delivered/executed. No executable fixture, import/package execution, dependency fetch, compilation, server/browser/network launch or source execution occurred in T054; read-only shell source/document inspection and writing own notes only.

**NOT RUN implementation/runtime:** gateway/backend/lifecycle/gameplay/two-browser proof not implemented or executed here. T050's original parent FAIL remains immutable alongside D033's narrow child/cleanup acceptance. T051 normal lifecycle evidence remains unchanged. No production transport, authority, P1, eight-player, P0 or MVP acceptance claimed. Untrusted ENet/map, allocator/OOM, parser synchronous work and native internal observation remain explicit risks/unknowns.

## Stable document identities

- T054-transport-proposal.md SHA256 `3b668fcb8b2da475f2b99604858fff79f0dbde5d25a78e493c4bad23cbbbf575`
- T054-draft-tickets.md SHA256 `f563f916ac239cbe6d3a312003f113e432da3302978e4a0f234609480479b5cc`
- T054-AI-Director-transport-freeze.md SHA256 `2ef4220803c81678da52872217f5774ae9282bcd5a180a3f1bd171ce0a57852d`

MAIN next review: freeze backend/header/milestones and browser timing/observation scope, reconcile source owners, then individually release remaining implementation/build/runtime tickets. No further action by this worker is inferred from the drafts.
