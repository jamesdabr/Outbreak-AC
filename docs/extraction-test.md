# Minimal extraction test

This is an opt-in **native, local, one-player engine mock**. It uses the actual
player, map collision, third-person camera, particles and HUD. It does not use
the offline Outbreak combat/revive experiment. Network/browser play is rejected;
there is no claim of synchronized multiplayer extraction.

## Playtest

Build the native client using the normal `source/src/Makefile` and its SDL2,
SDL2_image, OpenGL, OpenAL, Vorbis, zlib and ENet dependencies. Launch the client
from the repository root so it can find the bundled maps and models.

1. Open a local bot deathmatch map (for example `/mode 8`, then `/map ac_desert`).
   Remove bots with `/kickallbots` for an unobstructed camera/timer test.
2. Stand where extraction should be, leave edit mode, and enter
   `/extractiontestzone`. A green particle ring marks the zone. This also enables
   the collision-aware third-person view.
3. Walk away from the ring and enter `/extractionteststart 120`.
   The countdown appears at the top of the HUD. Omit the number for 120 seconds;
   use `10` for a quick test. Allowed duration: 1–120 seconds.
4. Enter the ring before expiry. Entry requires a living player, within four
   horizontal engine units and two vertical units of the marked foot position.
   Extraction is immediate and permanent for that round; movement/fire are
   neutralized while waiting for the countdown to finish.
5. At zero, the HUD displays `YOU WIN - extracted!` or
   `EVERYONE LOST - nobody extracted.` Results remain visible. `/extractionteststatus` returns the same status text for console checks.
6. Restart with `/extractionteststart 120`. To reposition/respawn first, use
   `/extractionteststop`, then place a new zone. Changing maps clears the test.

An unextracted death cannot respawn during the round. Local pause freezes the
countdown. Entering edit mode cancels the test. Extraction at/after expiry is
rejected. This is a local mock: extracted actors are input-neutralized rather
than removed through a new authoritative lifecycle.

## Manual checks

- Walk, turn, jump and crouch; check the character is visible in third person.
- Back into a wall and turn near a corner: camera retracts, avoids viewing
  through geometry, and recovers; the local body hides when overlapping it.
- Stay outside for the entire round: everyone loses.
- Enter before expiry: extracted status appears, then a win at zero.
- Restart: countdown and extraction reset; old wins do not carry over.
- Stop/change map: the custom HUD/zone disappear and normal camera returns.

## Automated logic check

From the repository root:

```sh
g++ -std=c++11 -Wall -Wextra -pedantic source/tests/extractiontest.cpp -o /tmp/outbreak-extraction-test
/tmp/outbreak-extraction-test
```

This checks the same round rules used by the engine, including simulated
zero/one/multiple-winner cases. Simulated participants are not connected clients.
Actual two-client extraction needs server-owned zone/time/state and replicated
results; that is outside this initial local mock.
