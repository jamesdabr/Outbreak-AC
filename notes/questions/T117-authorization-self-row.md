# Runtime authorization self-row in the original-UNION ledger

- Author / worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90
- Ticket / revision: T1171.1, preparation only
- Contract: CANDIDATE_PAIR_SMOKE0.2, runtime authorization/preservation section
- Exact interface: preservation.files inside digest-bound runtime pins versus complete controller-root preservation
- Status: OPEN (MAIN resolution separately)

## Question and evidence

Runtime pins are themselves a new ordinary notes/decisions JSON inside the
controller forest. Requiring that same document's preservation.files row to
contain the final hash of the whole pins document is self-referential. The fixed
four preservation fields have no separately supplied baseline reference.

Propose one deterministic derived authorization row: the declared preservation
map covers all other original members; after checking the supplied pins path and
EXTERNAL expected SHA before parse, the read-only gate derives this file's actual
bytes/hash/mode/nlink and unions that exact row into the immutable runtime
original baseline. It is never omitted from before/after preservation, never
has an unchecked/null hash and cannot be a worker-selected historical exception.
The private validated plan names this one derived row, without modifying pins.

## Options and impact

1. Approve this exact self-row interpretation as a private schema completion
   before real pins. No new runtime-pins top-level selector or historical-path
   exclusion; fixture coverage checks source/auth changes before/after.
2. Supply a separately digest-bound original baseline record/explicit slot via a
   MAIN contract revision, before controller acceptance/real pins.

Independent fixtures and future effectful-source preparation continue; no real
authority/pins/runtime is produced or invoked here. This note is not an adopted
exception. Terminal ledger/receipt hashes likewise use finite explicitly named
acyclic self slots plus final independently returned hashes, not a blanket
generated-history exemption; exact private schema is submitted for MAIN review.
