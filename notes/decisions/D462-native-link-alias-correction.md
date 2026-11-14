# D462 — Native attempt2 failure and exact SDK linker aliases

MAIN records actual visible-native-2 terminal FAILED, exec54539 exit1, terminal chunk5a3648. Release16 objects and server linked (step066 exit0), but link-input validation refused before debug build. No server/browser run. Attempt/control/manifest/logs remain immutable. D461 verification precondition is false: do not run it.

Read-only trace/current metadata diagnosis found exactly four noncanonical external linker spellings; every resolved external input is already declared in D460 observation.inputs. Under /Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/lib, all four leaf symlinks have mode0755:
- libc++.tbd -> libc++.1.tbd
- libz.tbd -> libz.1.tbd
- libSystem.tbd -> libSystem.B.tbd
- libpthread.tbd -> libSystem.tbd -> libSystem.B.tbd (both exact edges required)
No other link alias is adopted. No SDK writes.

Amend BLACKWOOD_NATIVE_BUILD_PREPARATION to0.6 solely to accept these exact fixed SDK aliases during link closure, retaining raw link text/mode/type/ordinary ancestors and exact canonical ordinary single-link target plus declared input/system_sdk hash equality. libpthread requires both edges. Share a pure fixed stage validator if useful; builder and independent verifier must each reconstruct actual trace using it. No supplied alias map, general symlink normalization, new control selector or record schema relaxation. Existing canonical link-input records may stay canonical; original preservation already binds alias metadata. Unknown/mutated links or targets still refuse.

Release Player T273 source and one fresh targeted guarded pass11 within existing bounds, followed by stable handoff. Source-only plus fake checks; no actual native attempt/retry/verifier/tool/runtime effects. Keep original250 test cases; add at most six meaningful focused cases, selecting only relevant alias negatives, success and existing full fake build/verification. Do not expand infrastructure. MAIN reviews and separately authors candidate3 controls after acceptance. QA remains paused. Full MVP remains active/incomplete.
