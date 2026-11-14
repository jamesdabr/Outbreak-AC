# T063 preflight native historical header pin versus accepted browser header

- Author: AI-Director; T063 revision3.6 / D050 prerequisite3.6; browser foundation/GOVERNANCE/P0 0.5
- Exact clause: unchanged native binary and “source-dependency pins from T045/T051” before actual launch
- Status: OPEN; MAIN resolution recorded separately

## Question

Preflight stopped before launching any native/browser/gateway process because historical native sound.h SHA0abee07769e72a97d396abc53808a9be999b50b850dc17c3a924724274d477ff differs from current80f635fd48b40ec61524d52707ba7c6f80eb2ad2d8bead137099bdf462c11655. Current value is already explicitly accepted read-only in D047/T059; its changes are browser-only __EMSCRIPTEN__ && !STANDALONE audio declarations. May the native current-source check explicitly reconcile this single accepted header pin, preserving original binary/objects and every other historical native input unchanged?

## Evidence and impact

- Preserved preflight-only FAIL: `web/transport/results/native-enet-T063/run-20261108T071124-a21e847a/result.json`; no process PID/actual launch, all fixed ports released.
- Full native dependency comparison finds **only** sound.h mismatching historical inputs. D050 binary/library/backend/gateway pins and genuine component compile/link passed.
- `git show HEAD:source/src/sound.h` exactly hashes to historical0abee..., so baseline is identified, not guessed.
- Read-only native preprocessing of historical/current files with clang -E -P -x c++ -DSTANDALONE yields identical bytes. Commands/input/output hashes: `web/transport/results/native-enet-T063/sound-pin-audit/result.json` and contained snapshots. This is evidence for MAIN, not private scope amendment.

## Options for owner and lead

Recommend a recorded single-header reconciliation to current accepted80f635... based on exact STANDALONE equivalence; unchanged native binary remains pinned49a1d... and is never rebuilt/re-signed. Alternatively retain strict historic-source matching and leave runtime NOT RUN pending a different explicit release. Do not revert Player audio/header, weaken all dependency checks or silently ignore mismatches.

## Work paused

Actual T063 baseline launch awaits this pin decision. New wrappers/compile/link/drivers are complete and independently inspected; existing source/artifacts untouched. No actual attempt consumed; preserve failed preflight and use a fresh report after any approved reconciliation. No packet/game parser/UDP/native launch follows merely from this note.
