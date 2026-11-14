# MAIN — Actual stock-first runtime progress

Owner direction: player → guns → existing large map; owner selected Swamp after44-map inventory. This record separates source acceptance and actual behavior.

Implemented/source/data accepted: original player and default PNG skins; original pistol/assault world MD2 assets and notices; native attachment from real selection; real load checks;97-file pack; browser indexed-model triangle compatibility repair; glyph current-color batch repair; local-body omission only when camera overlaps actual bounds. Native/offline/wire/gameplay preserved. No simulated actors/weapon/ammo grants.

Actual build: stock-player-2 exec20897 exit0; stock-combat-1 exec27820 exit0; linked JS395511/24c842 exit0. Local9/local10 originals89107/94257 Ctrl-C returned CLOSED_VISUAL_SESSION errors[]. Local11 originalTTY66555 started successfully,30min bounded runtime, both page capabilities consumed in Chrome then IAB.

Actual observations: recognizable original player and attached stock assault weapon; genuine Chrome mouse lock and S/A movement in local10; repaired HUD/text and original pale overlay absent at idle in local11. Native AssaultCube assault magsize20 (source/src/server.h); real mouse fire20→17, Rreload20 with reserve40→37. MAIN initially inferred pistol visually, corrected D488. Pistol selection not observed, not a proved rifle-selection bug. Chrome game tab subsequently closed/other surface active, further testing stopped. IAB cannot capture mouse (WrongDocumentError), so is visual evidence only. Own public-model diagnostic read in IAB returned undefined in the read-only evaluation scope; not used as a load acceptance claim. Required model/skin failure checks did not abort and actual world/body render.

Evidence: notes/previews/T283-stock-player-runtime.jpg; T283-chrome-stock-player.png; T283-chrome-camera-obstruction.png; T283-chrome-after-strafe.png; T285-stock-combat-start.png; T285-stock-pistol-fired.png and T285-stock-pistol-reload.png (historical filenames mislabel rifle, preserved unchanged); T285-stock-combat-runtime.jpg. Native Chrome screenshots include browser context; IAB image is a clean actual game view, not a mockup.

Incomplete: polished lighting/framing, full near-wall/crouch/aim/animation checks, pistol switching, gun audio, transient firing-particle correctness, stock Swamp integration/expansion, enemies/survival/extraction, final eight-player authority/performance/QA/MVP. T288 inventory in progress; no speculative map or public publication. Other leases idle, broad goal/QA remains paused.
