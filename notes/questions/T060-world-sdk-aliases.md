# T060 installed SDK aliases versus strict symlink gate

- Ticket: T060 revision 3.0, D041 preparation only.
- Clause: reject escaping/symlinked tool inputs before compiler/artifact mutations; retain exact installed SDK.
- Observation (read only): approved SDK `/private/tmp/outbreak-web-sdk/upstream/bin/clang -> clang-24`, `clang++ -> clang`, `wasm-ld -> lld`, `llvm-ranlib -> llvm-ar`. Emscripten invokes these aliases. No tool executed.
- Impact: the prepared strict execution preflight rejects these installed aliases. Dry planning, pack validation and negative tests can proceed. Actual execution already requires a separate future release/pins document and is additionally blocked on this conflict.
- Proposed resolution: MAIN explicitly authorize only the installed SDK's internal, confined aliases, with exact alias membership/link text and resolved target SHA256 in the future pins schema, or specify an inspected equivalent tool layout without symlinks. Worker has not implemented an exception, rewritten SDK config or altered tools.
- Requested decision: define the narrow approved alias policy before actual build execution. The current preparation does not manufacture that approval.
