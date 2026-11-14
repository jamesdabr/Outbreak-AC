# T040 attempt 4 — D031-complete graphics integration, frozen output

- Worker: Engine & Multiplayer
- Ticket: T040 1.3 integration; D028 graphics, D030 native source/build boundary, D031 complete pins
- Status: submitted new build evidence; no self-acceptance/status edit
- Source/header/config/port/flag/media edits by Engine: NONE
- New writes: generated/t040/attempt-4 precheck/runner/link/results/artifact snapshot, current web/build/out; this handoff only
- Historical incident/attempt3/unaccepted bundle, restored D022 snapshot and prior handoffs remain immutable

## Published frozen artifact

`T040-e25210b81a0b7114d6382120514ed339ea8acf3b447ec5e755c5bcf096bab3ef`

Root `/Users/jd1/code/apps/outbreak/web/build/out`, entry `index.html`.
Current files are frozen for MAIN's actual run. Exact full copy is retained
under `web/build/generated/t040/attempt-4/artifact/`.

| File | Bytes | SHA-256 |
| --- | --- | --- |
| index.html | 1330 | `22b4e8d79b6032639783f075a2d7bed69dde780476b2889ae80cff19f34a1725` |
| index.js | 340065 | `bce8c3163cb96cbc6cf2baf9d5036cba5ba73611c205b5b60962c667420e6c89` |
| index.wasm | 1845379 | `1bce63028e054a43e70441769bf4dcbd8b3173ae792ce608de17822424b4f633` |
| index.data | 87897 | `66574ce6af122f6c10fdfa51c7030c6f25511bd0936f09d292e07f316cd30877` |
| build-metadata.json | 152812 | `0a5af803868724911dc27cfc7db76c7e026a619a063421944c59fa65d65d703c` |

## Acceptance / operation evidence

| Requirement | Result | Evidence |
| --- | --- | --- |
| Prior snapshot and complete accepted source gate | PASS | Separate awaited precheck operation checked all seven D031 CPP/header pins, every recorded shared/source/config/pack input, full current header inventory, 61 object/source hashes and Wasm magic, all six recipe/archive hashes. Restored D022 pins verified and complete before-out snapshot taken. precheck.json records PASS and D031 JSON SHA741d2d5d…; no build/link was issued before that operation succeeded. |
| Validated object reuse and actual new link | PASS | D031 expressly permits reuse of attempt3 objects after complete current identity validation. All61 actual prior compiled objects match current accepted sources, complete shared header/config identities and object hashes. No compile is falsely reported as newly executed: each record sets reused_verified_object=true and points to immutable attempt3 compile evidence. New acceptance link runs exact same command/profile/ports/pack, exit0; no --emit-symbol-map or new flag. |
| Input/output/preload/notices/native preservation | PASS | No stale inputs; D031 pin file and all accepted pins stable across link; native outputs unchanged. Existing verifier passes all current source/config/pack/output hashes, actual Wasm signature, canvas id, all41 actual data slices/87897 bytes and notices. Node --check actual index.js exits0. |
| Exact new identity, immutable attempt, truthful runtime boundary | PASS | artifact-pins.json/table above, complete current metadata, result.json/link.log and artifact snapshot. No game/browser/server executed by Engine; actual corrected GPU/pixels/input remain NOT RUN. MAIN owns actual run while QA chat holds. |
| Frozen output and unchanged integration scope | PASS for this attempt | Current files frozen after all checks. Incident and previous D022 output preserved. No other worker source, contract/decision/ticket, compiler profile or media changed. Only explicit accepted future fixes permit later T040 mutation. |

Evidence root: `web/build/generated/t040/attempt-4/`:
precheck.json; before-out/; relink_verified.py; relink.stdout.log; link.log;
result.json; verify.stdout.log; artifact-pins.json;
preload-output-verification.json; qa-launch-command.json; artifact/.

The precheck and link were **separate tool invocations**. The reviewed runner
also repeats fail-closed identity checks before any output mutation, so a
failed assertion cannot fall through into a separate shell build command.
All later checks passed; no unrelated regressions were repeated.

## Exact input decisions

D031-complete-browser-input-pins.json SHA-256
`741d2d5dd895c45f82efe22f196b7d7b3e1a28b4d817ff829f1009eb6c0c4330`
pins accepted rendergl/rendercubes plus server.cpp/serverfiles.h/log.cpp/
tools.cpp/new serverlifecycle.h. All seven current hashes match. D031 resolves
the missing-header question; no worker inference substitutes for it. The
old precheck incident remains failure/containment evidence, not retroactively
rewritten as a correctly gated build.

SDK Emscripten7.0.0/compiler777e6e5… and local Node24.19.0 unchanged. Same
D006/D009 six ports, GL_UNSAFE_OPTS=0, safe legacy emulation, initial64MiB,
stack2MiB, memory growth and exact original41-file pack mounted /outbreak.
Manifest1073382b…f5be3, all per-file bytes/notices unchanged. No symbol-map,
function-pointer emulation, undefined suppression or additional dependency.

## Reproduction / next owner

Already executed after the independent successful precheck:

```sh
python3 -B web/build/generated/t040/attempt-4/relink_verified.py
python3 -B web/build/verify_client_bundle.py --evidence-dir web/build/generated/t040/attempt-4
/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node --check web/build/out/index.js
```

All exit0. Do not rerun/mutate during MAIN's pinned runtime session. The exact
actual linker argv and environment are in result.json; it reuses only the
61 hash-valid accepted objects, not fixtures/native objects. qa-launch-command
contains candidate new-ID file pins, but MAIN owns the actual next observer
run and may choose a fresh result path. Engine executed no QA command.

No build/integrity prerequisite remains. T046 source/helper/object success
and this link do not prove correct pixels/GPU recovery. Native T045 boundary
acceptance does not prove lifecycle success. Audio/models/network/eight-player
MVP remain separate gates. Published/frozen graphics output satisfies the
priority prerequisite before Engine starts separately released T050 in its
disjoint dependency-only paths; browser files will stay untouched.
