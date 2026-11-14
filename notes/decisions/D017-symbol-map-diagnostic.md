# D017 Symbol-map diagnosis of actual D016 trap

Approved narrow diagnostic addendum1.4 to T040 and governing browser foundation/GOVERNANCE/P0 0.5. Actual corrected D016 run progressed through real map read, then trapped memory access out of bounds before frames. Stack indices3179,3202,1694,775,2001,1064 with first offset0x1714c9 are in T030-real-D016-1.json. Font-command signature failure no longer appears, but startup recovery remains incomplete. No source cause is selected from offset proximity alone.

Engine may perform ONE diagnostic re-link of EXACT accepted D016 objects/ports/link args/shell/pack, adding ONLY --emit-symbol-map and changing output directory to web/build/generated/t040/symbol-map/index.html (same basename). Preserve web/build/out and actual QA evidence. Installed SDK tools/link.py2434-2440 and building.py1144 were inspected: retain intermediate name section, emit numeric function map, strip it from final Wasm; no code feature/behavior change is intended. No new ports, source edits or other flags.

Verify final diagnostic Wasm SHA-256 equals D016 6165af498f65cc7a51a877801679978a5672fea7c78f27c1ae143cd09c1ab229 before using the emitted map to attribute its exact function indices. If bytes differ, report mismatch and do not claim the original stack has been symbolicated; ask for separately bounded diagnostic build/run instead. Demangle mapped C++ symbols with installed SDK tooling. Read-only correlate exact mapped stack to source and provide precise likely failing memory operation. Do not implement a speculative source fix.

No browser/server launch by Engine. QA real output remains frozen. This is offline compiler/metadata inspection only under T040's existing execution/cache scope. Actual map motion/render/input/audio/network remain unverified.
