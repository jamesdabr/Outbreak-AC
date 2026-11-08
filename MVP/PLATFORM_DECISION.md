# Browser MVP platform and measurement baseline

Revision:0.1. Status: APPROVED by MAIN under D084 for the existing browser-first eight-player MVP. This selects the foundation and freezes initial measurement targets; it does not accept P0 or release gameplay.

## Foundation

Retain the AssaultCube-derived C++ renderer/client platform compiled to WebAssembly with Emscripten, browser SDL/WebGL compatibility and browser gesture audio. Retain native dedicated-server process/ENet and binary WebSocket-to-UDP gateway as transport adapters. The new Outbreak simulation must be server-authoritative and use a distinct application protocol; legacy client-position/hit forwarding is only prerequisite evidence. No engine migration, streamed-video substitute, native client installation, public master registration or accounts are required.

Basis: actual render/navigation receipts D032/D034; full61-unit build D064; real two-full-browser native joins/spawn/parsed movement D076; actual fixed-datagram impairment T086 reviewed under D084. These justify the foundation choice with known compatibility and TCP head-of-line limitations; they do not prove remaining rendering/input/audio/performance/clean-build or gameplay gates.

## Initial supported target and reference

Desktop keyboard/mouse, macOS26.5.1 arm64, Google Chrome156.0.8078.80 is the measured development target. Candidate acceptance must record its exact installed browser build and rerun on a changed browser; a historical version claim is not future compatibility proof. Other browser/OS/mobile combinations are unverified and must be listed honestly; broader support is not inferred. Browser URL delivery stays mandatory.

Reference hardware: Mac15,10 / Apple M3 Max /96GiB RAM, read using sysctl hw.model/hw.memsize/machdep.cpu.brand_string; OS build25F80. No serial/device identifier recorded. Native development target same macOS arm64; remote hosting platform remains a later deployment decision, not an implementation blocker.

Measurement viewport1280x720 CSS pixels, DPR1, ordinary desktop perspective. Responsive canvas must preserve its aspect ratio with no stretched projection or clipped controls; smaller/aspect<1 viewports may letterbox a16:9 active viewport. Record actual CSS/intrinsic viewport and WebGL renderer identity. Do not claim hardware GPU performance from software rendering. No throttle/visibility/pointer/audio/security-disabling browser flags in acceptance.

## Initial frozen acceptance targets

These are new initial targets, set before new acceptance measurement, not retroactive passes from old evidence. Any later change requires an owner/lead amendment; workers cannot tune them.

- Initial requested client runtime/assets/notices<=16MiB total transferred, with raw and transferred byte totals separately recorded. Ready/control-capable within15s from URL navigation on the local reference service; also record cold-cache and warm-cache separately. Internet startup is unmeasured until a separately approved network-load profile is exercised.
- Browser steady-play60s sample: average>=55 rendered frames/s and p95 frame interval<=33.4ms at reference viewport, excluding separately reported startup only. Record interval counts, elapsed time, long frames and actual rendered-counter progress; no single instantaneous FPS value. No lifecycle/page/network/WebGL errors or unreported dropped samples. Later eight-player/12-walker/1-Predator scene must pass the same profile over an actual normal900s round.
- Per-client Wasm committed memory<=512MiB and owned Chrome process-tree peak resident memory<=2GiB; report JS heap separately when exposed. Native server peak resident memory<=512MiB. Unsupported measurement APIs require another real installed measurement path or a question, never a fabricated zero/pass. Original64MiB initial Wasm/2MiB stack build flags remain unchanged until a separate build amendment.
- Future authoritative simulation50Hz/exact20ms, <=4 catch-up ticks/turn, debt>200ms faults the measured match; tick-cost p95<=10ms/p99<=20ms under full MVP population. These targets do not implement its scheduler. Full shared-state/API freeze remains required.
- Existing transport proof gates retain genuine join<15s and bidirectional normal W250ms movement>=2units with a newer matching parsed remote receipt within1unit/2s. Fixed impairment is40ms each direction/every50th raw datagram lost, with actual effect/accounting required. Added nominal80ms is not measured Internet RTT. Later authoritative/input/performance profiles must add their own preapproved metrics and cannot substitute this relay proof.
- Browser gesture establishes actual pointer capture and audio-context/backend state; key and relative-mouse input must affect the real scene. Escape/blur/lock loss must release held input, and resume requires an ordinary gesture. Record normal browser denial/error behavior. Physical audibility, visual comfort/animation/alignment and the final human playtest remain human evidence requirements; API state alone is insufficient.

## Remaining P0 and release boundary

Integrated T014/T015/T001/T002/T003, clean checkout/browser+native builds, source ownership, approved shared record/wire/body interfaces, all P0/P1 numeric rules and actual approved smoke/measurements still need completion. No P1/P2 implementation follows solely from this decision. Existing frozen legacy recipes/artifacts/limits remain unchanged; any successor build/backend/profile gets a new exact contract and ticket. QA's human hold remains in effect; another named worker may prepare/execute explicitly released local evidence without dispatching that QA chat.
