# Shared engineering interface contract

Revision: 0.2. Status: DRAFT. Interface owner: coordinating lead.

## Required shared behavior

- The browser client and authoritative dedicated server are separate runtime targets. The approved transport must work through supported browser networking APIs; native ENet/UDP compatibility cannot be assumed.
- The dedicated server owns match time, life states, damage, ammo, material awards/debits, loot availability, structures, infected decisions and extraction seats/outcomes.
- A client requests actions; it cannot grant health, report a successful authoritative hit, mint materials, spawn infected or complete a revive/extraction itself.
- World queries used by attacks, player validation, infected movement and construction share consistent map and dynamic-obstacle definitions.
- Replicated actors/objects have stable IDs, lifecycle versions and explicit removal. Join/observer synchronization includes current relevant world state and terminal player outcomes.
- Match seed, decision reason codes, server tick, interaction request IDs and acceptance/rejection outcomes are observable through diagnostics. Replayed or duplicate requests cannot award effects twice.
- Public enemy positions must not be exposed in the HUD or map. Squad identity never grants damage immunity.
- Outbreak configuration, protocol identity and connection behavior must be isolated from ordinary AssaultCube public play. No public master-server registration is required or authorized.

## Interface freeze required before dependent work

The lead must approve a technical addendum specifying concrete source modules/header ownership, public symbols/data types and any browser/native bindings, actor/object ID layout, protocol messages and validation, simulation tick/catch-up bounds, snapshot cadence, movement authority/prediction, hit timestamp policy, anchor schema, event ordering browser transport/connection setup, asset loading/configuration boundaries and test hooks. It must identify which existing source files each worker may edit.

The client foundation and transport must first be selected by the owner/lead using T014/T015 evidence. Compatibility work may be proposed for AssaultCube; workers cannot interpret browser priority as permission to change engines. Any technical spike needs its own explicitly scoped, released ticket and temporary interface boundaries.

The engine worker may submit a proposal in `notes/questions/` or `notes/handoffs/` under T002. The worker cannot edit this file or make a private proposal binding on other workers. T002 is a proposal-only ticket until the lead records the addendum. Dependent implementation stays unreleased until that approval.

Changes to a public header, wire message, cross-system event, config schema or shared asset format require an approved revision before implementation. Private helper functions inside a ticket's allowlist do not require amendment when they preserve all contracts.

The LLM tester interface is a deferred requirement, not a frozen API. The owner and lead will define its game-state observation/action contract separately before T013 is released. Workers must not add screenshot requirements or select a provider/transport on their own.

D086 adopts APPROVED P1_RULES.md0.1 for time/authority/atomicity/identity/ordering policy only. Public record definitions, wire message bodies, geometry/numeric algorithms and concrete adapters are still not fully frozen; T002 remains SUBMITTED. Existing portable numeric/envelope/map prerequisites retain their separately approved exact APIs.

D150 selects T132 remaining-tail-hold/progress direction and qualified arithmetic wording for future final P1 integration, preserving numeric rules and old frozen proposals. This does not freeze all typed interfaces or release implementation. Exact private step restoration, sticky holds, velocity/remainders/debt and required resource/runtime proofs follow D150/T132; no broader convergence claim.
