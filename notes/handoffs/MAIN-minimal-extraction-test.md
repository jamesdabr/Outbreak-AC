# Minimal local extraction mock

Owner directly authorized implementation in this chat after specifying only a
third-person camera, timer, and extracted-player wins / nobody-extracted loss.
This is a new local mock on codex/extraction-test, based on origin/main c6344626.
It does not implement or amend the broader survival MVP contracts.

Implemented: shared round logic, opt-in native local adapter, existing chase
camera/body visibility enabled for the local mock, green particle extraction
ring, countdown/status/results HUD, reset/stop and map-change cancellation.
Commands: extractiontestzone, extractionteststart [1..120 seconds, default120],
extractionteststatus, extractionteststop. Network browser builds reject setup.
The mock never enables the separate offline combat/revive experiment.

Verification on Linux:
- Compiled all 61 native client/ENet source units with g++/gcc and linked an actual
  client at /tmp/outbreak-extraction-build/ac_client. Development/runtime Debian
  packages were extracted only under /tmp/outbreak-test-deps, without installing
  system packages. Build objects/logs are under /tmp/outbreak-extraction-build.
- Shared round tests passed with AddressSanitizer and UndefinedBehaviorSanitizer:
  zero/one/multiple extracted participants, exact deadline rejection, invalid/dead
  entries, duplicate extraction, restart and reset. Additional participants in
  these tests are simulated, not network connections.
- Actual SDL offscreen native engine loaded ac_desert in bot deathmatch, removed
  bots, placed a zone, started a shortened round, entered the zone, reached expiry
  and printed YOU WIN - extracted!; stop printed Extraction test inactive. The
  process exited0. See /tmp/outbreak-extraction-build/engine-final.log.
- The scripted backward console command did not move the player (movement commands
  use key-release context, not integer console arguments). The attempted second
  loss scenario therefore extracted again. The in-engine no-extraction scenario
  remains a manual check; its shared round logic test passed.
- Xvfb could not start because its hardcoded /usr/bin/xkbcomp was absent. SDL
  offscreen ran but reported a1x1 drawable: saved screenshot is NOT usable visual
  camera/HUD acceptance evidence. Camera movement/wall recovery and rendered HUD
  require an interactive display playtest. No screenshot quality claim.
- git diff --check passed. Existing format warnings in unrelated hook calls remain.

Limits: native local one-player mock only; extracted input is neutralized, not a
new authoritative removal state; local pause freezes time. No server replication,
multiplayer result acceptance, browser build/playtest, survival systems or public
release. Existing stock startup attempted its normal media-update HTTP check;
this is incidental engine behavior, not a new service integration.

Instructions and manual scenarios: docs/extraction-test.md.
