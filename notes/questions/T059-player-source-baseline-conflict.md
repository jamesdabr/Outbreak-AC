# T059 dependency baseline conflict: final T052 cleanup correction

- Author / worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket and revision: T059 revision 2.9; T052 revision 2.5 acceptance D040
- Phase and contract revision: browser foundation/GOVERNANCE/P0 0.5 plus D040 prerequisite 2.9
- Exact clause or interface affected: accepted T052 source/object dependency and preservation of audio/header source
- Status: OPEN (lead resolution is recorded separately)

## Question

D040 accepts audiomanager.cpp SHA-256 d8396e5ce2c381a90e7b59cd1606f0c0c176c247a13ec7e085804ff3e4de9a45, matching notes/handoffs/T052-player-1.md. While completing final review after that handoff file was created, but before receiving MAIN's D040/T059 notification, I found and changed a cleanup ownership edge case. Thus actual source now differs from the acceptance pin. I have stopped source/test changes on seeing D040. Please review and explicitly authorize finishing the correction evidence under a T052 follow-up/release, or otherwise resolve the exact accepted dependency. No rollback is performed and this note does not authorize source changes.

## Evidence and impact

Current audiomanager.cpp SHA-256: a874699f308cefc450c5dcd8ccf535eab158af0212ab7f4505f0cbb277577c4a. main.cpp remains 52e77d11e586bbe9736455fa791ce018e54712de0b437e836f00e2a8bb7ea143 and sound.h remains 80f635fd48b40ec61524d52707ba7c6f80eb2ad2d8bead137099bdf462c11655. No T059 source has been changed.

Finding: pinned SDK libopenal.js stores buffers globally at AL.buffers with device references. alcDestroyContext only drops context/timer/device-context ref; it does not free that global buffer. The initially handed-off shutdown forced a retained failed-delete source invalid and its buffer id to zero after context teardown. On genuine deletion failure that could abandon SDK ownership. The existing sbuffer::unload also zeroes its id after deletion without returning success, so a proof helper must check deletion itself to retain failed cleanup ownership.

Current narrow correction in audiomanager.cpp:

- browserproofrelease explicitly alDeleteBuffers/checks alerr before zeroing buffer id/deleting the wrapper. On error it reports buffer deletion failure and retains its handle for cleanup retry.
- Shutdown with a retained proof source OR buffer suspends the actual context, publishes an error and returns while preserving the backend/handle for retry. It no longer discards handles after failed deletion or claims complete shutdown. Successful repeated shutdown can retry deletion then perform existing engine/backend cleanup.
- No change to normal gesture playback, main.cpp, sound.h, gameplay mappings or other source.

Evidence status is mixed and must not be represented as final acceptance of the current correction:

- Original handoff T052-player-1.md is preserved unchanged; its source/object pin is the D040-accepted version.
- A first correction (retaining failed-source ownership on shutdown) passed a rerun of all eight native/Wasm checks and extracted C++/JS helpers. That interim rerun replaced task-local result/patch/object/helper outputs, so those paths must not be assumed to still pin the original handoff.
- The additional checked-buffer-deletion correction now in actual source has NOT been compiled or run. Draft helpers.py was extended for failed-buffer deletion/repeated shutdown but NOT executed in this final form.
- final-evidence.json/evidence-manifest.json still describe the earlier accepted version; they have not been updated and are stale against current source. No current source-vs-object equivalence claim.
- No browser, audio, integrated link/build, server, SDK patch or shared out mutation ran. Original proof WAV/other sources remain untouched.

## Options for owner and lead

Authorize the narrowly described cleanup correction and final native/Wasm/helper re-verification in a precise follow-up. Alternatively direct explicit disposition of the unaccepted audio delta. T059's request-denial implementation is independently scoped to main.cpp, but its accepted dependency preservation should be pinned clearly before a combined handoff/integration.

## Work paused

All T052 correction/source/test changes are stopped because the ticket is now ACCEPTED and T059 explicitly makes audio/header files read-only. T059 implementation has not started pending dependency-baseline clarification; read-only inspection and this question note only occurred after D040 notification. Partial source and all existing notes/artifacts are preserved. No new human hold is asserted.
