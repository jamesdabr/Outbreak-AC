# T105 actual dependency guard refuses SDK sched.h alias

- Author / worker: AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket and revision: T1051.0 / D110, one actual build invocation exhausted.
- Phase and contract: CANDIDATE_NATIVE_FOUNDATION0.3/D107; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5 actual build prerequisite only.
- Exact clause affected: native0.3 permits only the fixed compiler-header pthread.h alias; all other non-framework compiler aliases refuse. T105 requires preserving failure and stopping for MAIN with no retry/patch/workaround.
- Status: OPEN; MAIN resolution must be recorded separately.

## Question

The authorized actual builder for D110-native-1 exited1/FAILED after release log.cpp pre-discovery. The compiler command itself exited0; dependency_paths then rejected SDK/usr/include/sched.h as an undeclared alias. Should MAIN separately review this concrete alias (and any other retained raw SDK header alias evidence), revise the exact fixed recipe/contract/source as needed, and issue new source/pins/attempt authority? No correction or retry is authorized here.

## Evidence and impact

Clean root: /private/tmp/outbreak-clean-D109-1. Reviewed source31d433b993d393b1902f7f57285a1d5ea6d2042d; pins65a6d2f8f3e93d6efc5d2d6f28be2595675e2c4039043fafa03db04dd745a463; common manifestdf64341ac627b84625909beb65f293c434573453b50ecc7452fba6916c469fda. Both metadata identities still match after failure.

Actual retained file: web/server/candidate-attempts/D110-native-1/release/log.pre.d, SHA256c4fd1b45db65f65e251d9b6633a1923197787c8e98d4cb097b115cfafd5786c3. Raw dependency name:

- /Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/sched.h.
- lstat permission0755, raw target pthread/sched.h.
- Canonical target /Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/pthread/sched.h.
- Canonical target already exists in both accepted observation.inputs and system_sdk.files with SHA25607d65b8d135be978a33579b5a333bd4576a8c6b36351ef510e0cca2aa0987020. This is an alias-identity refusal, not permission to infer a new generic normalization from equal bytes.

The same .pre.d also names the approved pthread.h alias, which remains separately validated. No historical MacOSX.sdk selector appears in the failed command; current fixed canonical15.5 SDK flags were used.

Failed guard follows recorded step21, kind discover_dependencies, for release log.cpp; exact argv is in report.json. Step21 exit0, elapsed51.586ms, empty stdout/stderr, group_reaped=true, no timeout/overflow/kill fallback. Overall report error is exactly Refused: undeclared dependency alias. All22 actual child-command records exited0 and report owned groups reaped; no compiler/signing command failure is claimed.

Builder report SHA2562cbb59b820f290343ae4daa011a8b4e82de94e58c09ff1233a66188d0ba66c92; freeze SHA25626027a52829c5c8630e4c293b4bea8b3432f3da7a97fa67b67990146662340e2. Both are under the owned attempt; all153 frozen file/directory/link members were independently checked by read-only stdlib hashing/lstat after failure. No receipt exists or independent verifier ran.

Actual completed partial work: two compiler identity probes, copied nested/parent ad-hoc signing and signature/framework inspections, one genuine release crypto.cpp object and its dependency/file checks. No link, release binary or debug unit. All partial artifacts/logs/raw dependencies remain retained and unchanged.

## Options for MAIN

1. Review the exact installed sched.h identity and retained raw dependency evidence, then separately authorize a narrow successor source/contract/pins/fresh attempt. Existing failed attempt remains immutable. Additional raw dependency audit, if wanted, needs explicit scope.
2. Keep the current recipe unchanged and leave native build blocked at this guard. Do not remove/replace SDK links, relax all aliases, regenerate pins or retry the same attempt.

These options are not authority to implement either choice. No source/SDK/pins/schema/flags or old evidence changed.

## Work stopped

Actual builder allowance is exhausted. Independent verification was conditional on success and is NOT RUN. No further compile/sign/tool invocation, patch, observation regeneration, retry, native binary/server/browser/network/runtime or acceptance is authorized. Own failure handoff is the only remaining report work.
