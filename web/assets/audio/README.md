# T032 original procedural audio prerequisite

Nine independently synthesized neutral prototype cues, using Python standard-library integer triangle/chirp oscillators and a cue-name-seeded integer LCG noise source. No stock/external sample, sound configuration, download or encoder is used. This is separate staged data: the accepted T027 pack and current browser build/config remain untouched; current initial-map audio=0 is not changed.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/audio/audio_pack.py generate
PYTHONDONTWRITEBYTECODE=1 python3 web/assets/audio/audio_pack.py verify
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web/assets/audio/tests -v
```

`verify` generates twice and compares all file and manifest bytes, then independently parses RIFF/fmt/data lengths, PCM format, sample bounds and the attack/release envelope, and cross-checks Python's wave reader. Nine targeted tests cover exact names, determinism, malformed lengths/format/truncation, silence, excessive peak, endpoint/global/per-pulse envelope violations, Predator temporal distinction, hash/notice/membership tampering, traversal and symlinks/undeclared files. Rejections preserve unexpected files. No command performs playback or executes engine/source/config code.

All nine files are mono signed little-endian PCM16, **22,050 Hz**, maximum 1 second, first/last sample zero, with a **5-ms attack and 25-ms release** both per pulse and globally. Nominal durations are quantized down to whole samples. Synthesis gain is 6,000; measured peaks are 5,860–6,000, below the frozen 8,191 limit. These are sample amplitudes, not a measured browser loudness or audibility result.

Stage root: `web/assets/audio/pack-root`. All files live under `packages/audio/outbreak/`: exactly nine WAV files, nine `.wav.LICENSE.txt` sidecars and one scoped `LICENSE.txt` (**19 files / 184,804 raw bytes**). Each WAV's manifest entry records its individual notice sidecar, size/hash, format/rate/channels/width, frames/duration and procedural recipe. `manifest.json` is deterministic; Python/tool identity and structural measurements are separate in `validation.json` and `execution.json`. MIT permission applies only to these original cues/tools, not upstream engine or stock media.

| Name relative to packages/audio | Nominal ms | Intended procedural shape |
| --- | ---: | --- |
| outbreak/proof_tone | 300 | 440-Hz triangle tone |
| outbreak/pistol | 180 | 520→80-Hz sweep, noise blend |
| outbreak/rifle | 120 | 740→110-Hz sweep, higher noise blend |
| outbreak/reload | 450 | Three short click/sweep pulses |
| outbreak/footstep | 200 | 95→45-Hz thump, noise blend |
| outbreak/walker_attack | 400 | 170→65-Hz rough sweep |
| outbreak/predator_front | 600 | **Two pulses, rising 330→660 Hz**, one long gap |
| outbreak/predator_flank | 750 | **Three pulses, descending 660→440→220 Hz**, two long gaps |
| outbreak/extraction | 900 | Three ascending 262/330/524-Hz tone pulses |

The front/flank recipes intentionally differ in rhythm, pulse count and pitch contour. The validator observes one versus two long silent gaps in the actual PCM. **Listening/audible distinction is NOT RUN.** These clip recipes choose no cooldown, range, damage, spawn, command or extraction gameplay rule.

Source-only compatibility evidence: `source/src/openal.cpp::sbuffer::load` tries `packages/audio/<name>` then `.wav` then `.ogg`; non-Ogg input goes through SDL_LoadWAV_RW. AUDIO_S16 with one channel maps to AL_FORMAT_MONO16 and uses the decoded sample rate. Available SDL 2.32.10 `src/audio/SDL_wave.c` maps 16-bit PCM to AUDIO_S16LSB; the Wasm target is little-endian. This format needs no new codec/encoder port. Inspected source hashes are in execution.json. This inference is **not actual SDL/OpenAL/Wasm decoding or playback evidence**.

A future separately released integration may overlay this stage root at `/outbreak`, adding only `packages/audio/outbreak/*` to the accepted original map pack. Use extensionless names in the table (or exact `.wav` paths through the native loader). **No overlay has been performed.** Required later checks: real engine sample decode/upload, user-gesture audio activation, suspend/resume/reacquisition behavior, actual audible recognition and spatial playback as applicable. Listening, native engine/browser launch, real playback and gesture tests are all NOT RUN here. Models, other audio and final sound art remain outside this data prerequisite.
