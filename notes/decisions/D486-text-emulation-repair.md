# D486 — Resolve T287 rendertext allowance

MAIN reviewed Engine question T287-rendertext-color-layout-1.md, actual draw_text initial glBegin/glColor order and inline TEXTCOLOR macro, and cached libglemu color-record writes. Permit exact recommended browser-network-only correction: initial current color before begin; inline color transition ends complete glyph batch, updates actual existing text_color outside begin and resumes quads. Preserve all glyph layout/UV/color/alpha/pulse and native/offline behavior. This avoids a demonstrated incompatible immediate record layout; actual overlay resolution remains runtime-unproved. Do not alter model brightness without separate evidence.

T2871.1 replaces previous implementation allowlist with ONLY source/src/rendertext.cpp plus own new notes. Other sources read-only. Contract STOCK_FIRST_PROTOTYPE0.4/D484 plus this decision. No runtime or new framework release. Re-read revised ticket before edits/submission.
