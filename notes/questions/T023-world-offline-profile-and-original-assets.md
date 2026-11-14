# Remaining offline profile and original-asset decisions

- Author / worker: World/Match-Systems
- Ticket and revision: T023 revision 0.4 RELEASED
- Phase and contract revision: P0 prerequisites 0.4; BROWSER_FOUNDATION/GOVERNANCE 0.4
- Exact clause or interface affected: T023 criteria 2 and 6: exact dynamic references and prioritized distributable replacement inventory; no script execution or replacement implementation
- Status: OPEN (lead resolution is recorded separately)

## Question

For a later integrated proof, should MAIN retain the common native menu/docs/script configuration or release a minimal original offline startup profile? Which of the exact paths in `web/assets/generated/ac-complex-manifest-replacements.json` should receive permission review versus newly authored/generated original replacements?

## Evidence and impact

The selected version-10 ac_complex map has embedded HX_CONFIG and the HX_MAPINFO license marker `ac-default` with an author/copyright comment. That marker has not been treated as permission clearance. Declared map references resolve to 45 textures, 6 sky faces, 14 map-model names and 7 ambience files, with model fallback/mesh/load success unresolved. Common startup configs and nested literal includes are now inventoried as data. Script blocks/lists, unsupported commands and exact built-in source expressions remain in `ac-complex-manifest.json`; no CubeScript has been evaluated to collapse them.

The inventory has 159 entries and 156 restricted/unreviewed paths requiring review or original replacement before a distributable proof. The generated priority list names every original path, SHA-256, target virtual path and source notice pointer. It includes mode-dependent HUD and model fallback alternatives, so it is not a minimal runtime pack. Known native runtime calls still derive further model/audio/igraph names; exact expressions are retained instead of guessing filenames.

The missing mapmodelattributes.cfg is recorded as an optional generated cache based on ignored startup execfile failure, setmodelattributes populating model registry data, and writemapmodelattributes writing it on quit. No fake cache is created; the older T018 missing-required record remains historical and unchanged.

## Options for owner and lead

1. Freeze a minimal original offline startup/config/media profile in a new ticket. Preserve required fallback/font/sky/map/model semantics while separately authorizing any native-service/menu removal or original asset generation.
2. Retain current startup and review every exact script/model/audio requirement and permission before packing anything.

Either choice requires new release authority for source/config changes or asset creation; this question note grants none.

## Work paused

No independent T023 metadata work is waiting. Actual script evaluation, asset replacement, permission clearance, packaging and renderer/browser integration remain outside this ticket and unperformed. Readiness stays false pending those decisions and evidence.
