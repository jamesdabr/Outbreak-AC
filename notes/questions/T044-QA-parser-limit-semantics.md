# T044 parser count limits differ from proposed wire-frame/byte bounds

- Worker: QA/Performance / `01a1b92d-28be-7110-9ac6-7ae01476c117`
- Ticket: T044 1.6 RELEASED, static dependency inspection
- Clause affected: T044 acceptance 2, T035 proposed parser/session bounds
- Status: OPEN (lead resolution separately recorded)

## Question

Before freezing future gateway limits, adopt the inspected parser semantics and
a separately reviewed complementary policy, or select another inspected library.
The installed ws 8.21.0 supports maxFragments:16, but it counts nonempty retained
payload buffers, not all WS frames. Empty continuation/control frames do not
increase that count. maxBufferedChunks:32 counts queued TCP chunks, not bytes.
Neither provides a total wire-frame/control-rate/queued-byte cap by itself.

## Evidence and impact

Pinned utilsBundle source references and hashes are in
`web/transport/dependency-inspection/REPORT.md` and `SHA256SUMS.txt`. Receiver
checks are near 11305 and 11645/11686. maxPayload:4096 is cumulative message
payload, not whole-connection memory/CPU/rate. Whole-bundle import also eagerly
patches shared fs.close/closeSync and attempts optional addons; the report bounds
these findings and proposes a future isolated import-only scope.

## Options / work paused

MAIN can freeze the actual option semantics plus complementary reviewed resource
policy, or request a different dependency inspection. No new adapter, parser,
package, import or network test is implemented/authorized by this question. T044
report/hash work is complete independently; only future reuse/strict-bound
claims need resolution. T030 actual-game priority remains unaffected.
