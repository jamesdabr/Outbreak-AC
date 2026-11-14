# D008 stable assertion header accepted

MAIN reviewed the exact tools.h architecture guard and T031-engine-assert-1 handoff/regression evidence. The only new behavior selects the genuine builtin trap on native arm64; x86 and release paths remain unchanged. Stable source/src/tools.h SHA-256 e53d32d55e5b81ac5e5be3e8a2411a8363dae858631f06cfd3ed11b16eef6fcf.

T033 source-read-only worker is released to rebuild all native release/debug objects consuming this header and produce final real executables. T031 must conservatively rebuild its header consumers too. This accepts the narrow header fix only, not either full build or server/browser runtime. Engine owns any further header edits; no additional changes are authorized without a lead decision.
