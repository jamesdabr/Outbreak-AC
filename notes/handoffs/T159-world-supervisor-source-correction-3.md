# T1591.7 D244 supervisor source correction handoff

- Worker: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket/revision: T1591.7, RELEASED HARNESS SOURCE CORRECTION ONLY D244; D235/D238 clarifications, D233 actual barrier.
- Contracts: WORLD_QUERY_FOUNDATION0.4; unchanged adopted execution plan c7b2844ea06f00e74a0511d44b0fac69b20a142bbdf6eae244d048c77b9afb63 and publication/accepted dependency requirements. No authority/status edit.
- Base: bdaa8df7ec39d9408f97feda4560832d7ef26c3c plus preserved shared work; no Git invocation or mutation in this stage.
- Changed files: ONLY `tests/outbreak/geometry/G1/{verify.py,SCHEMA.md,README.md}`, this NEW handoff and NEW `notes/proposals/T159-G1-harness-correction-preparation-plan-3.md`.
- Commit/patch: none authorized; stable current source pins below.
- Delivery: **SOURCE CORRECTIONS FOR MAIN STATIC REVIEW. No source import, parser/py_compile, fixture, generation, tool/compiler/native/Wasm/FFI or preparation/actual execution.**

## Stable reviewed-input and new source identities

Read final review `notes/reviews/T159-harness-correction-review-2.md`, independently verified SHA25670aab4e1b45c518866877a8ee62aa6072c36604051413657c1de80b4247dacb5. MAIN's immutable five-file archive `notes/reviews/MAIN-T159-source-before-second-correction-1/manifest.json` remains7e195e90444c3adf1e64a5403971bb7a106573c9e6b3b70750a6e450a019b24b. No preliminary finding was used to edit before the D244 consolidated release.

Current prefix `tests/outbreak/geometry/G1/`:

| File | Bytes | SHA256 | D244 disposition |
| --- | ---: | --- | --- |
| verify.py | 182963 | b03bd7f896f82dab94e61bf5f3efa93d815a2915cd82c817191a0a0e6897a3fe | corrected supervisor/persistence and focused definitions |
| SCHEMA.md | 5321 | eb822bcfaf94e033280035310695021f063ece8c89bd2c15d1692ecb5db2f9b4 | private receipt/count documentation |
| README.md | 7086 | 97293e48cc47d79a9923fe46980c9a101f259d2fb84a11691ded7d9441f64b33 | source gate and corrected mechanism documentation |
| wrapper.cpp | 27636 | df4dfcc355cb5d7bcba81ff3a5e9c8377b15d3894fc7e06cba51ae3e0e2b7129 | unchanged/read-only |
| wasm_runner.mjs | 3616 | 010ac5e0e19fd5f96c808d7b3d3ac8c762a798a6bc751c6c28722a59631232cc | unchanged/read-only |

These are standard read-only `wc -c`/`shasum -a 256` observations, not execution or generated readiness evidence. Default Python script entry still refuses current source-only execution. All newly generated artifact identities are PENDING.

## R1 source disposition: anchored group cleanup before reap

Removed normal consuming wait before group cleanup. After pipe EOF, the actual supervisor now waits for a bounded nonreaping terminal observation. The fixed Darwin adapter checks original handle/PID/returncode and whole104-byte output; no-event is distinct from a terminal exit. The cleanup path independently reobserves the original waitable anchor and owned numeric group, then the backend reobserves/rechecks the anchor and fresh original deadline immediately before SIGKILL. Unknown/lost anchor or unknown group never permits mutation.

Only after the mutation/cleanup stage does eligible strict original-PID WNOHANG waitpid reap the original handle. ECHILD refuses rather than using Popen.wait's fabricated zero. No call site can reach a mutating group signal after original reaping; only nonmutating group-existence observations and truthful failure remain. Reaping and post-reap group quiescence stay separate required success facts. Normal fake completion still signals its anchored group, reaps and observes group absence; source does not blanket-refuse ordinary completed children. A late/failed operation leaves ownership/refusal facts, not a reconstructed numeric-group ownership claim.

D235 implementation is owned source, with no imported helper. Lazy loader is fixed to `/usr/lib/libSystem.B.dylib`, symbol waitid, P_PID1/originalPID/flags37. Explicit argument/result types and errno; complete zeroing before each call; declared Darwin arm64 LP64 little-endian104B/alignment8 record and field offsets12/20. Fixed ABI/source/stdlib input pins are11 ordinary files in `WAIT_INPUTS`:8 installed headers plus ctypes/__init__.py,ctypes/_endian.py and the exact _ctypes extension. The preparation/execution plan reads and protects those identities without importing them. The system dyld identifier is explicitly not an ordinary project FileRef or general alias exemption. Only a separate future actual lease may import ctypes, resolve the library/symbol or call the API.

Unknown results/record shape/PID/signo/status, ECHILD, unsupported layout and native-boundary errors refuse/loss-mark the anchor. EINTR is capped16 with original deadline checks. Exit and original-wait observations cap6000, group observations256, all within original time limits; no helper process or extra compiler/tool command. Real adapter support and system-call behavior are **NOT RUN**, not inferred from source or fake definitions.

## R2 source disposition: original cutoff through persistence and release

The exact min(original child start+60,original whole end) now travels into every stdout/stderr/raw-response/provisional-receipt durability call. Real backend setup is included in that original child time. `durable_new` preserves a supplied smaller deadline rather than substituting START+300. `durable_write` checks immediately before and after file/directory acquisitions, writes, explicit flush, fsync and eligible close. Preparation terminal persistence uses its original whole cutoff in the same methods.

Local files and Popen pipes are unbuffered. Each close is marked attempted before invocation and is never retried after error/late ambiguity. An expired release is skipped and reported; the acquired handle stays strongly retained. Independent still-eligible releases continue to preserve primary/secondary facts. Late writes/fsyncs/closes cannot trigger a new flush/fsync/open/close. Child stream release follows the same rule, including fresh checks after pipe write or before EOF unregister/release. No syscall in progress is claimed interruptible and no cleanup grace is introduced.

Failure raw prefixes remain strongly retained in memory with receipt facts under the shared output cap. The outer failure.json path is explicitly FAIL-only, using remaining original whole time. It cannot resume expired child descriptors/logs/receipt persistence or report child success. Child elapsed time is measured after cleanup/retention, with late completion refused; no pre-retention timing is presented as complete elapsed success. Marker/candidate/late-unlink rules remain unchanged and now use corrected unbuffered storage ownership. A late unlink requires unresolved/nonzero outer outcome, never atomic publication or consumption from file presence alone.

## Focused fake definitions and unchanged obligations

Exactly24 new focused definitions in `focused_regressions`, plus prior76, total100. All **NOT RUN**:

| Category | Count | Source-defined checks |
| --- | ---: | --- |
| Original anchor/group supervisor | 4 | Post-reap remaining/unknown groups never signal; lost/unknown original anchors never signal; ordinary group mutation precedes original reap |
| Adapter/binder/call | 12 | Fixed no-event/call ABI/zeroing/errno, exit, killed, dumped, EINTR recovery/cap, ECHILD, wrong PID, unsupported layout, late native return, unknown result, invalid status |
| Actual supervisor and storage with shared fake clock | 8 | Write/flush/fsync/file close/directory acquisition/sync/close/provisional receipt crosses60 to61 below300; no subsequent child effect starts; no ambiguous close retry; distinct outer FAIL ledger remains separate |

Adapter fakes inject the library/native boundary before construction; fixed binder/call fakes use only bytes/local Python objects. No ctypes/subprocess/native import/library/API/VM/sleep/wait/signal occurs. Existing76 are preserved as40 supervisor/16 terminal/6 guard/14 analyzer cases; old supervisor assertions now demand each eligible or explicitly skipped release, rather than require an expired close or a renewed consuming wait. These cases are not target rows, OS cleanup proof or actual ABI evidence.

No geometry oracle, semantic case allocation, transform parent, setup/corpus schema, guard wrapper/runner, production math/API/domain, compiler flags/28-child command recipes or stack/output cap was changed. Review-2's other source dispositions remain review findings, not new generated or actual pass claims. Primary rows16384; families3072/3072/4096/3072/1536/1536; body sum15360. Proposed invocation retains300 seconds,8MiB input/fixture and64MiB retained evidence envelopes. Source assertions, including the100-count/artifact-cap checks, remain unexecuted.

## Exact next proposal and gates

NEW `notes/proposals/T159-G1-harness-correction-preparation-plan-3.md` is a standalone source-bound proposal: exact isolated Python argv/cwd, proposed fresh preparation-2 only, explicit before/after input/SDK/header/tool/D235/historical graph identities, original deadline/effect denial, exact100-fake plan and unchanged per-artifact caps. Both preparation-2 and attempt-1 remain absent. No source import, fixture or directory creation was performed to obtain these notes/pins.

D233 remains before actual attempt-1: live p1_rules.cpp913ce462a5c3896d766adc66751f278d188462ee6b3b97973269d976b3cf00b2 has the known normal initializer memcpy frame gap. No T166 candidate is imported/installed/linked. MAIN must resolve proof/acceptance/separate installation with protected intervals closed, explicitly refresh source/dependency/preparation pins, and later release actual execution. Unknown normal helpers never receive zero-frame treatment.

## Acceptance evidence and preserved files

| Requirement | Status / evidence |
| --- | --- |
| R1/R2 source mechanism and focused definitions | IMPLEMENTED FOR STATIC REVIEW; NOT RUN |
| Source identities and immutable file pins | Read-only wc/shasum, tables above and below |
| Python syntax/import/fixtures/generation | NOT RUN; no py_compile/parser invocation |
| Native/Wasm/compiler/FFI/SDK copy | NOT RUN |
| Full protected graph verifier / actual frame proof | NOT RUN; proposed future checks only |
| preparation-2 / attempt-1 | ABSENT by read-only shell tests |
| Production source | read-only hashes unchanged |
| Old notes/preparation/archive | unchanged observed hashes; no writes |

Production hashes: geometry.h8bfa5558899bcbaa172ce8a4ab38df3f48cae8468e9b43c976ad0e047e096a90; geometry.cppbf30f77b8c9e7d51a641c27597484cec58c005569178551dd8e744d3e4fbf385; store.h7a7b185ddba685cfdf313398c24558e54abb1ca674d2e305793e27420d4c0bc3. preparation-1 manifestf7173ba02e86ab086c625401bc71b539e5d50c8ba7cda4a55050e876b8f518d8 and first MAIN archive manifest4de1e5d0b147a05fe212a7d0171f54494540d284a1dc0ad06993802651a63be5 remain unchanged. Prior handoff2aac9980afb050a7fb521bbe20f237831bb9357c19f14c44b8ef7abda79627616 and proposal293a694702597a762871428ecd251a351a978e3d74f9fe17a841a148d1c58dbb6 remain unchanged.

Current stage used allowed source/note patches and standard read-only cat/sed/rg/wc/shasum/absence inspection only. No project code, preparation, fixture, generator, tool probe/compiler/Node/native/Wasm/FFI, SDK copy, network, Git, dependency/source installation, authoritative status or dispatch. Re-read ticket1.7/contract0.4 before submission. Work stops for MAIN review; no G2/caller/gameplay/runtime/P0/performance/RSS/human or QA/T149 gate changed.
