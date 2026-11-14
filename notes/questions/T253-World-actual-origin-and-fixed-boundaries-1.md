# T253 — Actual origin, preparation sequencing and fixed backend boundaries

- Author / worker: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket and revision: T2531.0/D429 NOTES ONLY.
- Phase and contract revision: G2_FOUNDATION1.8/T239 source receipt D408; T2321.3 is submitted SOURCE under review, no accepted/generated P5.
- Exact clause or interface affected: D429 requires early original300 with unchanged26+2 plan/nonreaping ownership and accepted P5/current source identity. Current R actual() resets START after source clearance; plan contains four original version commands and backend uses fixed waitid FFI.
- Status: OPEN (lead resolution is recorded separately).

## Question

Before any future actual-caller/source construction, please resolve the source-origin seam and its ordering relative to P5, and make the existing fixed command/backend boundaries explicit. This does not block completing the T253 notes design; no implementation or operation is released by the question.

## Evidence and impact

Exact current tests/outbreak/geometry/G2/regression-G1/verify.py SHA d65480cf24da406c180a15ade56a81df8e75dbb01ecbb03bfd3834f5bda48ed7:

1. actual(clearance),lines3313–3321, calls require_source_clearance() BEFORE assigning START=time.monotonic(); METADATA_BYTES=0; deadline=START+300. It has no operation_start parameter,finite-origin validation or no-reentry refusal. Thus source/control reads can consume time before the source deadline begins, and a future early caller origin is not propagated unchanged. prepare(),lines1479–1496, already has the exact D387-style required origin/no-reset boundary. An external original300 clock remains independently necessary, but it does not make the current actual START identical to the earlier caller origin.
2. validate_preparation_identity(),lines3263–3274, compares prepared manifest source/dependency/full file records to LIVE files. Source-clearance separately binds13+18. Any future actual-only edit of R verify.py changes a file in accepted P5's source map; T232caller1 also embeds its exact current R bytes. A changed source cannot silently consume an old P5 or an unchanged sealed T232 caller. P5 currently remains pending, so ordering can be settled before consuming it. No new preparation slot/name,source lease,caller successor or digest is invented here.
3. execution_plan(),lines1087–1124, has20 compilation commands+2links+FOUR existing --version commands (nativeclang,wasmclang,wasm-ld,Node),then2targets=28. Accepted P4 plan453f13...6096fb and failed A2 process argv confirm this. D429 also says no version/help/preprocessor/probe/extra child. I preserve the exact26+2 design and interpret the prohibition as NO ADDITIONAL probes; deleting those four would violate the required original order/count/flags. MAIN should confirm this precise boundary rather than leaving an apparent wording conflict in a future executable lease.
4. RealProcessBackend.__init__(),lines1673–1682, lazily imports subprocess/selectors/signal and constructs DarwinWaitid(); load_darwin_waitid(),lines1617–1640, imports ctypes and binds fixed waitid from the literal DYLD system identifier /usr/lib/libSystem.B.dylib, with original104-byte Darwin arm64 layout/flags37/idtype1. This is the existing nonreaping control boundary,not a geometry library or extra child. D429 prohibits native-library/FFI effects while requiring original nonreaping ownership. No FFI/library/probe is called in this notes task. Future authority must explicitly distinguish retaining this ORIGINAL fixed waitid boundary from any extra native-library/query/FFI experiment. The11 ABI input files as DATA and a PENDING library identifier are not an observed installed callable capability.

No parser/import/helper/calculator/analyzer/preparation/control/corpus/compiler/tool/FFI/runtime was used to establish these facts: fixed source/retained plan/receipt/review text only. Current source/old evidence remain read-only.

## Options for owner and lead

For the origin seam, the smallest direct future correction is R actual's private entry: required operation_start,exact finite float/current interval check,no-reset/reentry guard and START assignment BEFORE source clearance; same unchanged START drives all downstream ticks,durable writes,child min(start+60,whole),terminal and eligible failure retention. No cap/fallback or algorithm change. R README/SCHEMA would need matching narrowly released private-entry wording. This is a PROPOSAL ONLY,not authority to write those files.

Resolve sequencing explicitly: preferably dispose source review/correction and receive new current13 pins BEFORE any P5 operation,then separately construct/review a NEW correctly pinned preparation caller. Preserve T232caller1/current packet unchanged. If P5 is already consumed before correction, preserve its artifacts and require MAIN to name a new preparation/source/caller path and authority; do not rewrite P5's source map,update a digest in place or assume another operation is available. An alternative that keeps source unchanged must demonstrate every required original deadline/no-reset obligation through an explicitly reviewed boundary; merely claiming external supervision fixes START is insufficient.

For command/backend wording, explicitly retain the four ORIGINAL version commands as entries22–25 and original fixed waitid ABI as a narrowly scoped control effect in a future actual authority, with no additional version/help/preprocessor/probe/child/native query/library/FFI scope. If MAIN intends to exclude either original boundary, it must separately dispose the conflict with the SAME26+2/nonreaping requirement; the worker will not substitute tools or drop commands.

## Work paused

Future actual source/caller/preload/lease/manifest/preflight/dispatch construction and any execution remain unreleased regardless of this question. T253's complete notes/handoff can finish now with these gates pending. No source file,T232 packet,P5/output root,authority,status or old evidence is changed. No experiment is needed to discover the cited source facts.
