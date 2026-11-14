# Browser service boundary decisions for follow-up implementation

- Author / worker: AI-Director
- Ticket and revision: T020 / 0.3
- Phase and contract revision: P0 prerequisite 0.3; BROWSER_FOUNDATION 0.3
- Exact clause or interface affected: T020 criteria 3, 4, 6, 7; BROWSER_FOUNDATION single-thread profile and shared service changes
- Status: OPEN (lead resolution is recorded separately)

## Question

Before a source implementation ticket, approve the offline initialization strategy, explicit runtime profile/connection-state interface, and exclusive owners of the shared service files identified in the handoff. Source alone cannot determine these intended new interfaces. No transport or authentication replacement is selected by T020.

## Evidence and impact

`server.cpp::localconnect` sends a real local handshake. `clients2c.cpp::parsemessages` answers SV_SERVINFO; `server.cpp::process` stages SV_SERVINFO_RESPONSE; `serverslice` calls `polldeferredprocessing`, which unconditionally creates a worker even in a nondedicated process. Removing that poll without replacing its required completion would stall this path. `client.cpp::multiplayer` checks only `curpeer`, `sendpackettoserv` falls back locally when it is null, and `disconnect(0,...)` calls `localconnect`. A browser transport without an ENet peer cannot preserve these assumptions by accident.

`startmap` performs player/map state setup and optional local respawn; `load_world` calls it after media work. The minimal offline proof can either retain a carefully bounded embedded local protocol/simulation or use a separately designed map-exploration initialization path. The latter's exact required state needs runtime evidence. Native no-auth local initialization is not a license to accept remote auth or gameplay messages blindly.

## Options for owner and lead

1. Recommended first experiment: explicitly labeled OFFLINE_MAP profile, retain local protocol and common data/simulation initialization, replace only local no-auth deferred completion with a bounded same-thread queue that preserves existing result checks. Keep all remote cases unavailable in this profile. Approve the exact boundary before implementation.
2. Design a map-exploration-only initializer that avoids local protocol/server state entirely. Smaller runtime service surface, but more player/map initialization changes and verification risk.

For future NETWORK_CLIENT, approve a transport-independent profile/connection state consulted by all authority/fallback checks; never derive OFFLINE_MAP from loss of a peer. Decide the experimental remote handshake/auth contract in its separately released transport ticket. Proposed file ownership is in the handoff; none is assigned by this note.

## Work paused

No T020 documentation is blocked. All service/profile adapters, auth substitutions, public-header changes and offline initialization changes remain unimplemented and require a future released allowlist and interface decision. Continue T020 source analysis and handoff independently.
