# T168 final inventory stopped before reservation

- Worker: /root/review_native_candidate.
- Ticket / revision: T1681.1 FINAL INVENTORY ONLY D241, DEFAULT_DEV_BUILD_PREPARATION0.1.
- Base/pre-existing work: preserved reviewed six-source/preparation packet; no Git command or source change.
- Changed files: only this NEW handoff. No final-1 directory or final slots were created; no prior source/evidence/authority/tool/SDK/asset edit.
- Status: finalization stopped for MAIN disposition; no final digest/freeze/acceptance claimed.

## Concrete blocker

During authorized read-only external-role identity capture, all five D044/D046 installed SDK aliases have lstat permission mode **0755 (493)**. Current reviewed `web/build/dev_regression/recipe.py:298` requires **0777 (511)** for every alias hop. Thus a future actual observation would refuse the declared installed roles before any build. The positive fixtures use0777, so their success does not prove compatibility with these actual role modes.

| Declared alias under /private/tmp/outbreak-web-sdk/ | Actual mode | Raw text |
| --- | --- | --- |
| upstream/bin/clang | 0755 | clang-24 |
| upstream/bin/clang++ | 0755 | clang |
| upstream/bin/wasm-ld | 0755 | lld |
| upstream/bin/llvm-ranlib | 0755 | llvm-ar |
| upstream/emscripten/node_modules/.bin/html-minifier-terser | 0755 | ../html-minifier-terser/cli.js |

Read-only lstat/readlink/canonical-target and streaming hash checks confirm all declared raw texts and canonical targets match. Four unique terminal hashes also match the immutable source declarations: clang-24 `9a96f4220eefe21e72a4a9a20a88f4d6c26cad1b047cb02b5b22a96bef49c423`; lld `b851d4f8a53ca2839651b62821a8981fcdb22a51c8c7fc04733ed2f6d050ad5c`; llvm-ar `ba6f5e5d5c2e8dc5b7a6fc30feae23a7681df0f9a4a86ceb196e8375670b879b`; cli.js `d8d808ad0fb98e3db9324f0256fac798d115dfefa0bf50ac00a346acaca58bf1`.

Current recipe SHA256 remains `37d9e37805f34f5dcde144a3429b68c85a96b75d0b5ed085903c610aee42de55`. Review index remains `84baffedaecbae48ba9f97f544aabae0d6e86c074c2f322efceb9ec463166da1`; prior handoff remains `632feef99b1d010a74fb4c076ee093330ced07f8832cb6d72464671a02ad8b03`. Initial read-only checks matched six sources and1,906 indexed historical preparation files plus the index. Old source/evidence/review controls have not been retargeted.

## Boundary and disposition

The first trusted metadata-authoring reader stopped while statically reading the ABI dict(...) constant; its reader was corrected without any file writes or project evaluation. The corrected capture then stopped on the actual alias-mode mismatch, still BEFORE final-1 creation/reservation. No project helper/import/entrypoint/test, tool/version probe, FFI/native call, SDK/cache copy, build/verify/runtime/network or source-manifest/Git effect occurred. Reading file identity bytes/modes is not execution or native-support proof.

MAIN was notified with the exact source line and observed modes. Minimal proposed correction is an exact0755 declared-alias role check and corresponding positive/wrong-mode fake cases, retaining all prior proof unchanged; no generic mode exemption or alias expansion. Current inventory-only lease does not authorize that source/test correction. A separate narrow MAIN source/preparation release and review are needed before a truthful final source/preparation freeze. No worker amendment, fallback, acceptance or permission was inferred.

Stopped affected final inventory work. No inventory.json/receipt.json/freeze.json was published, and final-1 remains absent. All actual build/admission/runtime/P0/QA/T149/human gates remain unchanged.
