# T137 Engine diagnosis handoff

- Worker: Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket: T1371.0 / D158, notes-only; submitted for MAIN review, no selfacceptance.
- Changed files: own new notes/reviews/T137-engine-ack-and-receipt-diagnosis.md and this handoff only. No source, frozen evidence, pins, Git or runtime changes.
- Report SHA256: b4c17296a3fe9a424bdfc939fb15729369e937f97d992646ed5a74e9c1f9c526.

## Acceptance evidence

PASS diagnosis: frozen policy.py376 compares A initial ACK life0 with current life1; deadline itself is67.4ms, not late. Later genuine ACK life1 is236ms. B initial delay2266.5ms. Independent historical-first-active check at543 would next reject legitimate A life0 against final life1. Source explicitly records later ACTIVE milestone4 ACKs. Exact second native spawn origin remains unproved.

PASS receipt diagnosis: proof failure prevents validated captures assignment; terminal capture completeness then raises a secondary error and hides the primary error. Observer completion/two existing PNGs do not establish parent proof or acceptance. Report binds retained public file hashes and distinguishes observed from validated evidence.

PASS strict correction/regression plan documented; NOT RUN implementation/tests/replay/runtime. Only direct reads and builtin JSON/hash/metadata arithmetic occurred, with no project imports, services, processes, browser, native, admission, retry or forest audit. Existing failed evidence remains immutable and unaccepted.

## Disposition and integration

D159 confirms both lifecycle mismatches and primary-error masking. MAIN adopts only bounded sanitized primary+closure error retention for receipts. The report's broader FAIL digest-linkage/success-path proposal is explicitly NOT adopted; persisted files do not prove closure, failed null digests/empty captures remain allowed. No sealing redesign authorized.

T1381.0 separately releases new fixed-v4 guarded preparation after this handoff. No T137 result authorizes actual effects or accepts movement, visuals, P0 or gameplay. QA/T136 holds remain unchanged. MAIN controls acceptance and any future release.
