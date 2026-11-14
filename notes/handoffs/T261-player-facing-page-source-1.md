# T261 — Player-facing page source ready

- World & Match Systems; T2611.0/D438, VISIBLE_SLICE0.2. Source stable; writes CLOSED; stop for MAIN.
- Changes: NEW web/visible/play.html; concise usage section appended to web/visible/README.md; this NEW handoff only. Candidate,engine,assets,SDK and runtime files unchanged.
- Page uses actual first-playable-1 index.js,canvas960×540 and Module.locateFile for its index.wasm/index.data. Responsive dark canvas layout,real loading/error/exit hooks,collapsible actual client messages and packaged WASD/Space/C/R/primary-mouse controls. Canvas pointerdown only focuses; existing engine handles real capture/audio.
- MAIN's requested copy applied: “Engine loaded · Waiting for a game connection” and “A private game session is required.” No gameplay-ready/join/spawn success claim,fake HUD,join button,synthetic input,dependencies or boot-token creation.
- Source inspection: generated Module/canvas/locateFile/status/abort/initialized hooks,packaged browser.cfg controls and engine canvas gesture inspected; HTML/JS structure and relative bundle routing reviewed as text. No script/syntax checker execution,browser/server/native/runtime/build/network/Git or new proof framework. Actual render/input/audio/join behavior remains unrun by World.
- Route: /web/visible/play.html through the authorized runtime. Existing supervisor must supply OUTBREAK_NETWORK_BOOT before client startup; technical details remain in README/comment. Player/T167/QA holds unchanged. No rebuild needed; no runtime started.
- SHA256 play.html:22f0b51782268e951e97400fc5904bd9cc3b0c1bd6aea764cd2665a295f4e44e; README.md:9c09b39a5ed0ef7486aa82e6265fbef78bcf9660bc695b8a3437fd6f2f52af30.
