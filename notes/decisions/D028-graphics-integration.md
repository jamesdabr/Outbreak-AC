# D028 Graphics compatibility accepted for real integration

MAIN reviewed exact T046 rendergl/rendercubes diff, source-native preservation, real geometry/array helper evidence and actual native/Wasm whole-TU checks; independently checked current source fingerprints and four Wasm signatures. T046 ACCEPTED source/object scope. No actual GPU recovery or correct pixels is proved. Stable graphics hashes in D028-graphics-build-inputs.json.

Concurrent T045 native lifecycle work currently has PASS guard-verification: every browser/native-client preprocessed token comparison matches its pre-change baseline, six actual target objects compile and their source/object hashes match current bytes. MAIN independently checked these exact hashes. This accepts only the non-STANDALONE boundary for the current browser rebuild, not native lifecycle correctness/whole T045. Do not consume any later unverified source change. Native worker's full review/handoff/runtime remain pending.

Existing T040 now consumes these exact accepted graphics/unchanged-browser guarded inputs, snapshots D022 and rebuilds all stale/header consumers then links SAME SDK/ports/safeGL/heap/stack/original41-file pack. No symbol-map flag in acceptance output, new compiler/dependency or media overlay. Detect concurrent changes and rerun stale units; if native sources differ from D028 guard pins, wait for fresh guard verification/lead acceptance.

MAIN owns next actual run under D027 while QA chat holds. Freeze output after publishing pins; all historical failures/metadata remain immutable. No T014/P0/MVP acceptance from this source/build decision.
