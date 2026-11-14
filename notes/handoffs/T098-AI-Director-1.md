# T098 targeted native preparation correction

- Worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket / revision: T0985.24 RELEASED assignment; correction submitted for MAIN review. No authoritative status changed or self-acceptance.
- Phase / contracts: CANDIDATE_NATIVE_FOUNDATION0.2 / D091 / D098; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5 preparation only. Re-read current ticket/native contract/governance before submission.
- Base: 13f0d8eea4822dee5c976661218d022be74342e3 plus preserved existing overlay. No production source/header, SDK/library, historical native/browser helper/artifact, contract, ticket, decision, branch or commit changed.
- Changed files: only the five targeted web/server/candidate/{stage.py,build.py,verify.py,test_preparation.py,README.md}; NEW preparation-T098-20261108-1/** and this own handoff.
- Commit/patch: no commit authorized or created; targeted-source.diff contains the exact five-file original→corrected diff.

## Acceptance evidence

| Ticket requirement | Result | Evidence |
| --- | --- | --- |
| Archive all five exact pre-correction T092 source/docs first | PASS | preparation-T098-20261108-1/T092-source/ and T092-source-archive.json. All five hashes match original T092 freeze. Mapping retained in new freeze. Original T092 receipts/freeze/evidence unchanged, not rewritten. |
| Read actual retained T051 FAT2 output; robust same-file thin/FAT section parser | PASS in pure fixtures | retained-otool.json copies exact two framework libraries/stdout fields from web/server/T051-20261108T060101-484f0948-release.json, with report path/SHA provenance. SDL2 has42 total dependency rows; hidapi8. Current producer and independent verifier consume validated same-inspected-file thin or x86_64/arm64 headers; no arbitrary lines discarded. |
| Reject malformed/foreign/duplicate/empty/unknown/mixed headers and dependency sections; retain diagnostics and dylib scope | PASS in fixtures | New parser negatives plus foreign dylib in FAT section rejected by producer and independently by live inspection double. Raw retained-format stdout is asserted exact in the simulated build log. Existing dylib scope checks and all commands/flags remain unchanged. |
| Reject new owned links except exact approved staged-framework links/chains before reads/seal | PASS in fixtures | Shared pure owned-path/inventory helpers validate every entry kind before hashing/resolving, constrain framework links by exact path/text/mode/resolution and require canonical ordinary record/log/dep/object/binary paths plus ancestors. Producer refuses invalid tree seal; verifier applies independent gates before owned record/log reads and against resealed inventories. |
| Resealed tmp/log/ancestor/extra-framework aliases, records/deps/objects/binaries/receipt links | PASS in fixtures | Escaping tmp, same-content log, log-directory ancestor, report/freeze/receipt/object/.d/.pre.d/binary, extra inside-framework alias and changed existing framework link regressions. Log spy asserts no read through the rejected same-content log link. Ordinary outputs/approved staged Headers→Versions/Current→A chains still pass. |
| Protected historical malformed/dangling links remain opaque | PASS | Original opaque-history tests unchanged and pass; no existing preservation helper definition changed. No global link ban. |
| Original25 guarded cases plus new cases | PASS | Archived exact T092 suite:25 tests/exit0/5.518s, original-25.log. Corrected suite:38 tests/exit0/19.094s, corrected-2.log. All25 original test bodies AST-identical. All original stage.py definitions AST-identical; new shared pure helpers only. static-review.json records these checks. |
| Freeze corrected source/schema/test/receipts and preserve failures | PASS | New freeze covers18 files including five corrected source/docs, five archived source/docs, original/current logs, retained-format provenance, mappings, static review, diff and result. corrected-1.log retained (37/38 passed; fixture miscount43→42 corrected without parser change). |
| Actual compiler/signing/probe/native/browser/network or accepted manifests | NOT RUN / not authorized | No actual attempt container created, compiler/tool invocation, signing, SDK install/download, service, game or browser launch. No source/execution/accepted-native manifests authored. Test fake objects/signatures remain FIXTURE_ONLY and temporary. |

Reproducible commands already run from repository root, all Python standard-library guarded preparation only:

```text
python3 -B web/server/candidate/preparation-T098-20261108-1/T092-source/test_preparation.py > web/server/candidate/preparation-T098-20261108-1/original-25.log 2>&1
python3 -B web/server/candidate/test_preparation.py > web/server/candidate/preparation-T098-20261108-1/corrected-1.log 2>&1
python3 -B web/server/candidate/test_preparation.py > web/server/candidate/preparation-T098-20261108-1/corrected-2.log 2>&1
```

Do not overwrite frozen receipts on rerun. Tests forbid real subprocess/socket/compiler/signing effects. Existing bounded capture control is exercised only with fake child/fd/selector/read/signal/clock effects. Host is the existing macOS arm64 workspace with Python3.11.9; no native toolchain execution or performance claim.

## Implementation status

Implemented only D098 corrections: pure validated otool dependency-section parser shared by producer/independent verifier; strict owned path/ancestor/link inventory gates and per-use checks; corresponding fixture regressions and private-schema documentation. No target, compiler/link/otool flags, SDK/library choice, public schema fields, fixed recipe, capture limits or historical preservation behavior changed. Full raw diagnostics remain bounded logs.

Producer now rejects invalid owned paths before sealing. If report.json and ancestors remain safe, it retains a FAILED report and the invalid tree, without a freeze. If the report path itself is unsafe, it refuses that write too. No offending path is followed, removed or replaced to create apparently valid evidence. Existing ordinary failed-command/timeout/overflow attempts still retain their failure report/freeze as before. Verifier never trusts a resealed inventory to authorize opaque new links.

Simulated only: every build command result, object, signature, linked executable, and live inspector response in tests. The retained T051 stdout is actual historical read-only output used for format regression; it is not a current probe or new signature/build proof. The successful temporary simulated NATIVE_LINKED_NOT_RUN / VERIFIED_BUILD_ONLY_NOT_RUN statuses do not accept a real artifact.

## Frozen identities

- preparation-T098-20261108-1/preparation-result.json SHA256: `3be9f1a2b8b00195af62b3c57ab00668d06678e79dd1c3dcd133993466bc7711`.
- preparation-T098-20261108-1/freeze.json SHA256: `9fca5730ec1136a0c014247d61af7ef14eaea878b152185bf9a0f1071185119e`.
- Original T092 freeze remains `1e47a7cbc5edd604277dda42c7f40b88790eedbfca51a27f5fb791cdb2b6e321`. Its five former live source names map to the exact archived bytes; all other old frozen members remain at their original paths/hashes. It is not misrepresented as a freeze of corrected live code.

The new freeze excludes only itself and this separate handoff. Verify its exact18-member file set against the five live source/docs plus preparation-T098-20261108-1/** excluding freeze.json; check mode/size/SHA and the explicit T092 archive mapping. Static review already rechecked all original T092 frozen evidence through that mapping.

## Integration and questions

No new dependency, asset, service or gameplay interface. No unresolved question for this narrow correction. MAIN must review corrected source/private schema/evidence before accepting T092/T098 or releasing any real build. Common MAIN source manifest/reviewed revision, execution pins/digest and separate signing/build release remain future prerequisites. No further mutation of frozen correction or historical evidence is authorized by this handoff.
