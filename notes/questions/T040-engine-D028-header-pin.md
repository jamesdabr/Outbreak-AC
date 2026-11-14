# D028 additional native-guard header requires explicit verified pin

- Author: Engine & Multiplayer
- Ticket: T040 1.3 / D028 accepted-source integration
- Clause: consume exact D028 pins; wait for fresh verification for native changes beyond published pins
- Status: OPEN (lead resolution separately recorded)

## Question

Please publish the verified non-STANDALONE boundary/hash for `source/src/serverfiles.h` before the next accepted browser build. Its current SHA-256 is `efca26aaefb9d33cc8623bc84dcf06f3a1f10d0b9d9664fff78790dab2bed75f`; D022's tracked header hash was `e9cad8bf71795e666c29896b8b6ac293b3e1705344b8e58acd6863e3c37b44fe`. The current D028 JSON pins the five expected CPP files but omits this changed header.

## Evidence / scope

The five published D028 graphics/native CPP hashes all match current source. The header diff contains guarded STANDALONE lifecycle work; visual review is not substituted for the requested fresh token/hash verification. All tracked D022 input deltas are those five CPPs plus serverfiles.h.

I made a sequencing error: after the precheck asserted on this sixth input, the same shell command continued into the build. All 61 real target units/link passed, but that attempt is explicitly UNACCEPTED pending the header decision. No browser/game/server was run. The exact output was retained in generated/t040/attempt-3/unaccepted-header-bundle; commands/results remain under attempt-3. The complete old D022 output was then restored from the immutable attempt-2/artifact snapshot, and all runtime/metadata pins reverified. No engine source or other worker output was changed.

## Work paused / options

Pause new browser build/output publication pending MAIN's explicit current-header boundary acceptance. MAIN can independently verify/pin this header, then authorize the same-scope integration with all current identities. If the header changes again, reverify it rather than reuse stale guard evidence. No new compiler flag/dependency/source fix is proposed.

Next precheck and build will be separate tool invocations so a failed precheck cannot fall through into compilation. Current root runtime is restored D022 and frozen; this note does not authorize QA against the unaccepted attempt.
