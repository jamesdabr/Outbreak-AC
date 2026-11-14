# T032 original procedural audio prerequisite handoff

- Worker: World/Match-Systems / `01a1b92c-db5c-7a10-a0e4-46e1f5a092cf`
- Ticket/revision: T032 revision 0.7 RELEASED, submitted for MAIN review; authoritative status unchanged
- Governing subset: approved D007 addendum 0.7 to BROWSER_FOUNDATION/GOVERNANCE/P0 revision 0.5. Gameplay/product/parameters/interfaces remain draft boundaries; no gameplay balance chosen.
- Baseline: `13f0d8eea4822dee5c976661218d022be74342e3` plus D006 baseline/current work. `web/assets/audio` did not exist at start. All existing worker/source/config/build/QA files and accepted T027 pack preserved.
- Changed files: NEW `web/assets/audio/audio_pack.py`, `LICENSE.txt`, `README.md`, `tests/test_audio_pack.py`, `manifest.json`, `validation.json`, `execution.json`, and the 19 declared files in `pack-root/packages/audio/outbreak/`; this new handoff only.
- No commit/push/reset/branch/dispatch, global install, download, user-profile access or other worker contact.

## Acceptance evidence

1. **PASS** — exact nine D007 cues generated independently using integer triangle/chirp oscillators plus cue-name-seeded LCG noise. No stock/external sample transformation. All are signed little-endian PCM16 mono **22,050 Hz**, durations **0.12–0.9 seconds**, peaks **5,860–6,000** (limit 8,191), nonzero PCM, first/last samples zero, explicit **5-ms attack/25-ms release globally and on every pulse**. Pred_front has two ascending-pitch pulses (330/660 Hz), one long silent gap; pred_flank has three descending-pitch pulses (660/440/220 Hz), two long gaps. Intended temporal/pitch distinction is verified as authored structure; **listening/audible recognition is NOT RUN**.
2. **PASS** — deterministic generator and exact manifest with byte size/SHA-256/format/channels/rate/width/frames/duration/procedural recipe for every WAV. Own MIT notice is scoped to original T032 content/tools, with nine explicit per-WAV `.wav.LICENSE.txt` sidecars and one scoped staged LICENSE.txt. **19 staged files / 184,804 raw bytes**. Engine/upstream licensing untouched. Stage remains separate from T027/current build.
3. **PASS** — independent RIFF/fmt/data parser verifies header/payload lengths, PCM1/channel/rate/byte-rate/block-align/width, bounded sample count, amplitude/nonzero, endpoints, global and per-pulse envelope ceilings and silent gaps. Python standard-library wave reader cross-checks actual frames/format/payload. Hashes, notices and exact membership verified; undeclared files/symlinks/traversal rejected without deleting unexpected data. Two full generation runs produce identical file bytes and manifest. **9 targeted tests pass**, including per-pulse envelope corruption, malformed format/length/truncation, silence/excess amplitude, hash/membership/notice tampering, symlink preservation and Predator pattern checks.
4. **PASS (source-only compatibility)** — integration names and proposed future overlay documented below and in README. Inspected `source/src/openal.cpp::sbuffer::load` resolves packages/audio/name, name.wav, name.ogg, uses SDL_LoadWAV_RW for WAV and maps AUDIO_S16 mono to AL_FORMAT_MONO16. Available SDL 2.32.10 `SDL_wave.c` maps PCM16 to AUDIO_S16LSB. Wasm little-endian PCM compatibility is an inference from these sources, **not actual decode/playback evidence**. No new codec/encoder port is needed by this PCM data. No overlay, startup/source/config/build change or playback was performed.
5. **PASS** — new immutable handoff; exact Python/source/tool/output identities and commands/exit/stdout/stderr captured in `execution.json`; deterministic manifest and sample/envelope results in `validation.json`. Listening, actual SDL/OpenAL/Wasm decode, engine/browser launch, browser user-gesture activation/suspend/resume/spatial playback and audibility tests all **NOT RUN**. No invented audio success.

## Output identity and commands

Root: **`web/assets/audio/pack-root`**. Only staged subtree: **`packages/audio/outbreak/`**. Manifest: **`web/assets/audio/manifest.json`**, SHA-256 **`689941eae651adaef254cb3858f940e673661ef490c63c4821a290e9615907a3`**. Total **19 files / 184,804 raw bytes**.

From `/Users/jd1/code/apps/outbreak`, with Python **3.11.9** standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/audio/audio_pack.py generate
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/audio/audio_pack.py verify
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web/assets/audio/tests -v
```

Generator and verify return **0**. Final test suite returns **0**, **9 tests passed**. `verify` performs two generation runs and writes structural validation; it never plays audio. Commands, exact code/source SHA-256 values, Python identity and saved results are in execution.json. Decoder and procedural code are independently separated: structural checks do not resynthesize expected PCM to claim validity.

Inspected source identities:

- `source/src/openal.cpp`: `2a0756aeb5bfee1a13e16bd1eab95ec51aa229f4632042dbd6fc0f975b8634d4`, particularly lines 267–334 for name alternatives, SDL_LoadWAV_RW and AL_FORMAT_MONO16 mapping.
- `web/build/.cache/ports/sdl2/SDL-release-2.32.10/src/audio/SDL_wave.c`: `de4ba3818549cec5ebaff14d9ef825d40794a43c1698ee0bd3d5f34c66d076ff`, particularly PCM format handling around lines 2049–2055. Source read only; no native decoder was executed.

## Exact cue list and procedural intent

Each listed name is relative to `packages/audio`, extensionless for the native loader. Actual WAV is `<name>.wav`; its full original MIT sidecar is `<name>.wav.LICENSE.txt`. One additional `packages/audio/outbreak/LICENSE.txt` completes the exact 19-file membership. Full individual sizes/hashes/recipes are in manifest.json.

| Native loader name | Frames | Nominal ms | Peak | Intended recipe |
| --- | ---: | ---: | ---: | --- |
| outbreak/proof_tone | 6615 | 300 | 6000 | 440-Hz triangle tone |
| outbreak/pistol | 3969 | 180 | 5918 | 520→80-Hz sweep, 70% noise blend |
| outbreak/rifle | 2646 | 120 | 5968 | 740→110-Hz sweep, 85% noise blend |
| outbreak/reload | 9922 | 450 | 5902 | Three short click/sweep pulses |
| outbreak/footstep | 4410 | 200 | 5860 | 95→45-Hz thump, noise blend |
| outbreak/walker_attack | 8820 | 400 | 5931 | 170→65-Hz rough sweep |
| outbreak/predator_front | 13230 | 600 | 6000 | Two 330/660-Hz pulses; one ~100-ms gap |
| outbreak/predator_flank | 16537 | 750 | 6000 | Three 660/440/220-Hz pulses; two ~100-ms gaps |
| outbreak/extraction | 19845 | 900 | 6000 | Three ascending 262/330/524-Hz pulses |

Sample durations are quantized to whole 22,050-Hz frames: reload is about 0.449977 s and flank about 0.749977 s. No clip duration/pitch/recipe sets a gameplay cooldown, damage, range, command behavior or extraction rule.

WAV SHA-256 values:

```text
proof_tone       e37aa3c35b32a3a6b81610c08717721d22a95fb059f24894cfbaea24aa4e5f72
pistol           708999bd25f91c1a132bc04e62f487a1dea85b7e21ed851603afd31e1ec06483
rifle            1fcd2440fb09924f39b6d5260e28253636f76d2a1fa526dd2187f5eda8228693
reload           b409287328685f4648d377498eda64746a72866036f745635bd13d974324aa62
footstep         e0b2bc1d1f3a58a058692885b0a920295be6aeaa47e65be7f7df3a2f601e2400
walker_attack    17bca6cf27dd34d06a8f26528f27401cd7723c65d420448149717854e88e9c45
predator_front   1d8af04001b1fed5a3dc88cfaf4c35a416b34fba3f66a9bd72049939b146fe2d
predator_flank   51859ce446db0c50d9390110e2007f8646a471ae3ec76f959eed5b008d01bbc7
extraction       9a06d8c8d5cd3435237344611904d7bd26c8af2046c053c423f898e87e3bcf5d
```

## Implementation, omissions and future integration

Implemented original data synthesis, exact manifests/notices, independent structure/sample/envelope/membership checks and negative fixtures. No sampled audio input or external dependency. Fixtures create/delete only their owned temporary files. No host playback, engine/CubeScript execution, encoder, network, server, browser process or private profile write.

The accepted T027 manifest still hashes to **1073382bb93f689379406eb5d7556726b1dede6afa90a6d2b3796978506f5be3**, and each of its 41 files was independently checked against its accepted per-file SHA-256. Current initial browser audio=0/build/source was not altered. No mount overlay has been performed.

A later separately released ticket may overlay this stage root at `/outbreak`, adding only packages/audio/outbreak/* alongside T027. MAIN must release the real audio backend/sample registration and user-gesture hooks. Actual engine sample decode/upload, audible cue recognition, browser gesture activation, suspend/resume, and positional playback remain NOT RUN. Other sounds/models/final sound art and all full-MVP gameplay criteria remain outside this asset prerequisite. No independent T032 work is blocked; only MAIN accepts this ticket and releases integration.
