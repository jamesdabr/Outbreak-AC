# T082 revision5.5 — baseline with fixed impairment case preparation

Current extension under D077/EXPERIMENTAL_IMPAIRMENT0.1 preserves the default
baseline behavior and25 criteria. Only new run.py selects impaired40_drop50 with
strict T082 pins/profile and real-child UDP instrumentation; default baseline
never installs the shim. See web/transport/tests/impaired/T082/README.md for exact
future command/schema/receipt requirements. Current work is preparation only,
with fake-factory Node fixtures and no actual impaired run. T079 unimpeded PASS
is accepted D076, and its complete7-file driver is preserved against D074 in
source-T079-1 before these changes. All old results/receipts remain historical.

The retained T077 description below applies to timing/bounded evidence; current
source hashes/strict case tests are submitted separately under T082, not silently
substituted for the accepted T077 or T079 historical source.

Current preparation follows D070/T077 after the single failed T075 attempt.
The complete original seven-file driver is preserved byte-for-byte under
`web/transport/results/two-client-T067/source-T075-1`, with mapping/identities
matched against both D068 pins and the old preparation receipt before edits.
Original T067/T075 evidence remains historical; it is not revalidated as current
source. T075 remains FAIL, movement NOT RUN; an actual backend frame-gap violation
or long initial frame was not proven by its truncated timing trace.

T077 is PREPARATION ONLY: no actual retry, Node/JS syntax/package/compiler,
browser/native/server or network execution. Future execution additionally requires
MAIN-accepted T077 and fresh complete pins/release, never the old D068 pins.

## T077 timing, bounded failure evidence and cleanup correction

Source inspection: main.cpp1643–1660 computes first raw elapsed from initial
totalmillis; frame.frames starts0, increments before engine publication to1,
and ordinary drawing starts only after frame_count3. client.cpp204–234 publishes
the first lifecycle/WS frame advance as1. Backend JS62 deliberately has no
inter-frame-gap check before lastFrame exists. These are distinct clocks at
startup; the observer does not redefine either clock or change their limits.

A startup sample is positively identified only with timing frame_id0,
prediction0/embedded-server false; loading engine frame_count1/rendered0 on the
expected local map; one begin/one frame call/advance/WS frame, repeated-begin0,
no milestones/map-receipt/spawn-ACK/teardown; real opening or joining state and
matching timing lifecycle, prejoin own cn/life -1 and network map empty/rev0,
exact public counter set, matching initial kind0 events, no error/local attempt,
and genuine visible/frozen observations. Missing or inconsistent identity fails
as ambiguous frame0. A long positively identified initial raw interval is stored
as startup, resampled and **cannot establish readiness/ACTIVE/input success**.

For every later timing frame_id>0, published raw interval>1000ms still fails.
Real backend terminal errors/BNE15, hidden state, global errors, open/join
deadlines and all previous checks remain. The classifier checks errors before
any startup classification. Settled Python observation requires frame_id>=1,
and raw<=1000ms; no startup exception enters paired/movement evidence. No guessed
frame0 inference from BN_OPENING alone, visibility, raw duration or observation
ordinal is allowed. The JSON FIRST_FRAME_IDENTITY in JS exactly matches the
Python reference table under a SOURCE fixture; JS itself is NOT RUN here.

The observer retains at most A/B, three fixed slots each: full latest published
sample, first observed per-client ACTIVE sample, and positively identified
startup sample. Latest/first ACTIVE are retained before timing/eligibility/global
failure checks. Null explicitly means unavailable, never successful evidence.
Each full sample includes public network/main/timing/model/audio and real browser
metadata; first ACTIVE alone is not paired proof. At most512 network events and
global errors,256 remotes,3 model preload entries; total retained slots<=1MiB,
all report output still<=8MiB. Overflow fails explicitly and records a bounded
sample fault, rather than persisting an unbounded component. Cap redaction is
applied before storage/disk, leaving nonsecret raw numbers and actual errors.

Parent cleanup merges valid UDP tuples from BOTH final/retired gateway sessions
and any earlier baseline gateway receipt, even if the observer exits failure
before paired validation. It validates the fixed loopback gateway identity,
bounded session IDs/facts, exact UDP tuple address/port/IPv4 shape (UDP comes from
the accepted udp_tuple schema), integer1..65535 port, then merges uniquely into
existing lsof/bind checks. Missing/invalid final or connected tuple facts keep
ports_released false and fail cleanup; valid other tuples are still checked.
No unrelated owner is killed or inferred closed. All other supervisor behavior
is unchanged. Guarded tests include actual historical T075 final snapshot as
read-only DATA and confirm both61734/62986 are collected; no sockets are opened.

The suite now has25 tests: the previous17 criteria plus eight T077 methods with
multiple negative cases. Only stdlib reference/helper/source/data checks run;
all process/socket effects are forbidden. New test output/current hashes will
be frozen in a separate `preparation-T077-*` receipt. Current source is submitted
for MAIN review, not self-accepted or authorized for runtime.

The following retained recipe description continues to apply subject to this
T077 correction and additional dependency. Its original preparation-only
statements describe that component, not a denial of the historical T075 failure.

PREPARATION ONLY. The Python checks below are labeled FIXTURE_ONLY and read-only
pack verification. No Node, compiler, version command, package import, browser,
server, native game or network has been executed for this ticket. JavaScript
syntax and every actual runtime criterion remain NOT RUN. MAIN reviews this
candidate; this document does not accept dependencies or release execution.

## Files and reproduction now

`policy.py` contains pure authorization, routing and published evidence checks.
`ownership.py` contains pure process-table selection and injected signaling.
`supervise.py` contains the guarded future parent and pure preparation plan.
`observe.cjs` contains the unexecuted static/gateway/Playwright observer source.
`diagnostic-schema.json` is the D055/T061 exact schema, also checked against the
future pins. `test_preparation.py` forbids subprocess.Popen/run, os.system,
os.posix_spawn and socket.socket during all tests. It uses fake file identities,
fake effects and temporary fixture authority files, never actual MAIN pins.

From `/Users/jd1/code/apps/outbreak`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/transport/tests/two-client/T067/test_preparation.py
PYTHONDONTWRITEBYTECODE=1 python3 web/transport/tests/two-client/T067/supervise.py --prepare-plan
```

The second command is pure JSON output; it stages nothing. Do not run Node syntax
checks at this stage. Tests cover complete fixture acceptance, missing/wrong
authority/release/dependencies (including T070/T072), source/file digest,
membership and symlink changes, bundle roles/root/metadata, pack revision,
native capacity, tools/output paths, canonical routes, exact favicon exception,
genuine auto-spawn with zero requests, incorrect/fabricated observations,
missing ACK/map/milestones, alive state, stage-lag settling, passive focus,
frozen frames/duplicate identity/own-only or stale remote receipts, movement
deadline, cleanup missing facts, partial-start/Node-failure owned cleanup,
reparenting and PID reuse, and capability redaction. Only the accepted79-file
pack test hashes actual data; the pin filesystem is explicitly a test double.

## Future command — NOT AUTHORIZED / NOT RUN

After a separate execution release expands the runtime output allowlist and
binds D064's accepted T070 artifact plus T072 verifier/receipt, MAIN supplies
an immutable pin JSON directly in `notes/decisions` and its SHA through a separate
trusted instruction. No accepted pin JSON is supplied or generated here.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/transport/tests/two-client/T067/supervise.py \
  --execute --pins /Users/jd1/code/apps/outbreak/notes/decisions/MAIN-SUPPLIED.json \
  --pins-sha MAIN-SUPPLIED-64-LOWERCASE-HEX --attempt MAIN-SUPPLIED-UNIQUE-ID
```

Those placeholders deliberately cannot authorize execution. A missing or wrong
pin refuses before any child, listener or runtime-directory creation. Refusal
does not select a fallback bundle. Each real attempt must be new. The driver
does not retry automatically; native crash, nonzero shutdown, fallback kill or
cleanup/evidence fault records `reruns_frozen` and needs a question/MAIN decision
before any later actual attempt. Published output is always read-only.

## Pin schema1 (future MAIN owned)

The exact top-level fields are enforced by `validate_pins`; unknown fields fail.
Values below describe a schema, not an accepted execution manifest.

| Field | Required meaning |
| --- | --- |
| schema_version/ticket/status |1 / T067 / RELEASED |
| authority | owner MAIN, recorded D-number, pinned decision Markdown path |
| execution_release | EXPLICIT_TWO_CLIENT_NATIVE_GAME_EXECUTION |
| attempt | exact CLI unique ID,1–48 alphanumeric/underscore/hyphen |
| scope | profile network-client; role full-cpp-two-browser-native-game; clients2; capacity2; map_revision2; trusted_only/baseline_only true |
| accepted_dependencies | exact T061,T065,T066,T070,T072,T077,T058,T057,T064,T062 set, each ACCEPTED **by MAIN**, not fixture status or tooling alone |
| files | canonical path → {sha256,role}; all inputs hashed, no escaping/unrecorded symlink path; roles source/driver/sdk/node/tool/vendor/gateway/native/library/pack/bundle/metadata/notice/authority/schema all required |
| trees | exact root+complete regular-file member inventory for source/src, source/enet, this driver, /private/tmp/outbreak-web-sdk, vendor/ws-8.21.0, network-out, network pack-root, Chrome.app, installed playwright and playwright-core |
| aliases | every SDK/browser/Playwright symlink: path, literal target, resolved path, sha256 of file target; null sha only for a directory target within a completely inventoried tree |
| bundle | network-out root; exactly four distinct shell/js/wasm/data relative names; explicit notice list; metadata name and exact profile/status/bundle_id assertions |
| pack | accepted network manifest SHA c9ecfa62…359d7,79 files388791 bytes, map2; every manifest entry rehashed/size checked |
| native | unchanged49a1… binary; pinned historical dependency ledger and exact D052 manifest; exact c2 argv, parameters and rotation; no other source mismatch exception |
| diagnostic_contract | exact diagnostic-schema.json content and pinned accepted T061 handoff |
| tools | exact accepted Node binary path/SHA, Chrome executable, Playwright index; additionally pin unifdef/codesign/lsof/ps and all transitive package/tool tree bytes |
| outputs | result web/transport/results/two-client-T067/runtime-ID; native web/server/run/T067-ID; both nonexistent before execution |

Metadata meanings come from the actual T066 recipe, not invented public fields:
profile=`NETWORK_CLIENT original-network-media`, status=`LINKED_NOT_BROWSER_VERIFIED`,
artifact ID=`bundle_id`. Full-game role also requires actual61 units/compiles,
T066 revision4.0, object_reuse false, stable_inventory true and no claimed runtime
acceptance. Future MAIN must bind T070/T072 acceptance to those exact current
bytes. D064 now accepts that BUILD component; the observer requires its exact
acceptance JSON hash, every published member/hash, separate build pins, additive
verifier and immutable receipt in future runtime pins. It does not import/run
that verifier or replace the retained historical verifier failure. Metadata's
status is build evidence, never game PASS. All53 real C++ units,
seven core C units and the eighth backend C source are mandatory, with JS bridge,
observer/header/gateway files; partial ENet peers cannot substitute.

Absolute paths are restricted to the approved SDK/CLT, browser and installed
Playwright/core roots plus the four named OS tools. The native historical compile
ledger's exact current dependencies are also required in `files`; normalize
project-absolute ledger names to repository-relative keys. D052 alone permits
the exact preserved/current sound.h transition and checks the pinned unifdef's
410-token native view. Both copied signed library binaries must have their
accepted exact hashes. Codesign and token tools run only **after** full pins.

## Future topology and evidence

Unchanged native c2 binds UDP127.0.0.1:29863 with D010 isolated argv/config,
accepted map2 CGZ/cfg/license in **packages/maps/servermaps**, not its parent.
Official/incoming remain empty; no accounts/master/syslog/private config serving.
Gateway29865 receives two fresh one-use capabilities held only in memory.
Static29866 serves exact pinned runtime/notices, exactly GET /favicon.ico204/empty,
and rejects other unknown methods/routes. A response CSP and browser request
allowlist confine loading to the fixed origin/gateway. No repo/metadata/SDK route.

Two separate Chrome processes/contexts/profiles load immutable approved boot
configuration before the full game. Default unsafe/throttling overrides are
removed, no fake focus/visibility. The observer reads only published network,
main/timing/model/audio snapshots and canvas/browser metadata. Input uses ordinary
canvas click, W250ms/key-up and Escape. No C/private ENet/Module exports, packet
injection, state setters, teleport, ghost actors or alternate movement retry.

Initial1/2/3 milestones and map/cn precede any joining click. Wait>=2s after
parsed SERVINFO; retry ordinary still-JOINING click/release no faster than1100ms.
Already ACTIVE gets no artificial request. Zero spawn_requests can be genuine
native spawn without a published request; the internal branch remains unobserved.
Both clients still need genuine parsed SPAWNSTATE/ACK, initial ordered milestones,
distinct assigned cn and current nonnegative life/alive0. The spawn event must be
strictly within15s of real OPEN (second kind0 event), regardless of getter lag.
Transition sampling has a bounded2s publication-settle allowance only for an
already timely event; runtime errors or late genuine joins never get forgiven.
Settled samples require consistent state/timing; frame IDs need not equal.

Active paired snapshots and both movement directions are retained. Moving client
needs actual focus/capture; passive peer needs genuine visible/advancing frames.
Each W250ms release/settle must move own x/y>=2; other client must receive a newer
matching-cn/life parsed receipt within2s, x/y error<=1, counters and receiver-local
timestamp advance, and yielding rendered/frame progress on both pages. Distinct
gateway UDP tuples supplement this proof. Sequential admission associates page
phase with a gateway session; no independent cn-to-tuple binding/internal native
cache/clientsequence/server authority is claimed.

## Failure, bounds and owned cleanup

Every component collection is bounded512 or fails, child output8MiB, raw frame
gap<=1000ms, prediction0..50ms. The observer uses monotonic clocks. Parent starts
shutdown by160s to reserve cleanup within the overall180s deadline; hard watchdog
kills only its Node/native groups. Only T047's two exact compatibility strings
are classified once per page; other console warnings/errors, page/rejection,
network/runtime/GPU failures remain failures. Cap/token text is redacted before
persistence, preserving the error class. No raw packet payload/private key stored.

Node writes a bounded atomic capability-free early browser ownership receipt
immediately after each launchServer returns. Before launch, each profile is
created by inspected Playwright mkdtemp under the attempt's browser-temp-A/B
TMPDIR. Parent independently scans ps during startup and after Node death, selects
only exact Chrome executable+owned unique profile prefix and proved descendants,
and records pid/ppid/pgid plus birth identity in memory. Final receipts are not
needed to discover a surviving Chrome from partial startup. Signals are limited
to still-matching pid/birth/command; reparenting is allowed, PID reuse skipped.
Unrelated process-table rows are discarded. Missing receipts never prove cleanup.

Finally release held W/buttons/Escape; close owned contexts/browsers/profiles;
gateway close<=2s and measured zero active/retired/pending TCP/UDP handles/timers;
static close; native SIGINT<=3s with exit0. Browser destruction means abrupt peer
loss. Parent bounds fallback TERM/KILL to independently proven owned Chrome
identities, removes only its isolated profile roots, and records fallback as
FAIL/frozen reruns. Verify owned groups/PIDs gone, exact component handle facts,
profile removal, all fixed and recorded gateway-UDP/Chrome-control ports using
lsof ownership/no TCP LISTEN plus TCP SO_REUSEADDR bind/UDP bind and errno.
Unrelated occupied owners are reported, never killed. Stage and evidence files
remain immutable attempt history; temporary profiles are removed.

Cleanup missing any fact cannot PASS. Exceptions and partial startup remain
failures, with runtime_started accurately distinguished from preflight refusal.
The parent rehashes pinned inputs after cleanup; child OBSERVATIONS_COMPLETE is
not PASS until Python validates both directional proofs and all cleanup facts.

## Separate gates — NOT RUN / unobserved

Actual full-game join/spawn/movement, actual browser scheduling/CSP/package/JS
syntax, runtime cleanup, viewport/model pixels/animations/attachments, physical
audio, held-fire/jump release, ordinary weapon selection/engine quit/internal
AudioContext-close ACK (D060/T069), native internal cache/clientsequence,
authority, reconnect/impairment, performance, human playtest and P0/P1/MVP
acceptance remain separate. Preload outcomes and audio counters are observations,
not human hearing or correct pixels. No same-page rejoin or fresh-gateway shortcut
is included. No source/assets/bundle fixes are allowed during future baseline.
