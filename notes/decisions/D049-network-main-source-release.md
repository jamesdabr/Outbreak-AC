# D049 Remote-only main source wiring

MAIN releases T062 Player after accepted T059 source/D047, using accepted platform0.2 headers and approved client0.2 interfaces (T061 implementation pending). Approve EXPERIMENTAL_NETWORK_MAIN0.1, additive prerequisite3.5/browser foundation,GOVERNANCE,P0 0.5. No overlapping client edits: Player main.cpp only; Engine client/parser/world/logger and observer header. Sound/audio source frozen, World build preparation unaffected.

Required before real network app: skip local server bootstrap/slices/fallback, actual lifecycle poll despite prediction lastmillis0, unscaled50ms network-only clock, separate engine-render versus protocol-join diagnostics, safe shutdown outside parser. D048 genuine ordinary initial spawn request remains client-owned; no main fake alive. Full61-unit build/runtime after all source accepted/complete pins, not this source ticket. QA hold unchanged.
