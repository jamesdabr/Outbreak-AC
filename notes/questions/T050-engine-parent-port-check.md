# T050 parent plain-rebind failure and complementary cleanup evidence

- Worker: Engine & Multiplayer
- Ticket: T050 2.3 / D029 bounded dependency-only runtime
- Affected criterion: owned HTTP listener/port cleanup evidence
- Status: OPEN for MAIN evidence disposition; no request to rerun package code

## Observation

The single authorized WS loopback child passed all eight delivery/rejection/
close cases, closed its owned HTTP/WS listener, reported zero client/peer/
network handles and exited0 naturally. Parent elapsed0.086s; no timeout or
kill fallback. The original parent report nevertheless records FAIL because
an immediate plain TCP bind to the owned port returned unavailable.

The plain bind omitted SO_REUSEADDR; that result alone does not distinguish
a listener leak from TCP socket-reuse/TIME_WAIT behavior. Exact original errno/
TCP state was not recorded, so no definite TIME_WAIT diagnosis is asserted.
The original report and executed driver remain unchanged.

## Independent owned-port verification

Without rerunning package code or opening a listener/connection, checked
recorded owned port127.0.0.1:51793 using lsof's LISTEN filter: exit1, empty
stdout/stderr. One separate TCP socket with SO_REUSEADDR successfully bound
the same exact address/port and closed. Evidence is
web/transport/results/T050-port-cleanup.json. This verifies release separately
from the original overly restrictive plain-bind measurement.

## Disposition requested

Review the child/source/cleanup evidence together and accept or return the
criterion. No original FAIL was overwritten or silently promoted. No second
loopback package child, dependency/driver retry or source patch occurred.
Future cleanup probes should record exact errno and use a deliberate
listener/rebind interpretation rather than conflating all bind errors with
active listeners. Any further runtime needs a separate explicit release.

Browser graphics output remains frozen and byte-identical. No gateway, UDP,
ENet, browser/native server or game code was run by T050.
