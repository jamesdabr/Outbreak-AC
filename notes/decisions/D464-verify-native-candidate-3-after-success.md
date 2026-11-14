# D464 — Conditional native3 independent verification

Only if D463's original actual native3 build command exits0 and reports BLACKWOOD_NATIVE_LINKED_NOT_RUN without a failure marker, MAIN may run ONE independent invocation from repository root with the same actual pins/digest:

/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -E -S -B web/server/blackwood_candidate/verify.py --candidate-id visible-native-3 --pins /Users/jd1/code/apps/outbreak/notes/decisions/D463-visible-native-pins.json --pins-sha256 <actual computed control digest> --receipt /Users/jd1/code/apps/outbreak/web/server/blackwood-candidate-attempts/visible-native-3/verification/receipt.json

This authorizes existing fixed20 read-only file/otool/codesign inspections and exact owned receipt, all current source/alias/SDK/framework/hash/protection checks and existing bounded original-child supervision. No compiler/signing/build replay/game execution/server/browser/network. On build failure this release is inapplicable; preserve all artifacts. Keep other source writers idle until verification terminal. Success proves a build only. QA remains paused.
