# Dynamic bootstrap dependencies and shared-build permission blockers

- Author / worker: World/Match-Systems
- Ticket and revision: T018 revision 0.3 RELEASED
- Phase and contract revision: P0 revision 0.3 prerequisites; BROWSER_FOUNDATION revision 0.3
- Exact clause or interface affected: T018 required outcome and approved manifest boundary: dynamic references must be unresolved, supplements must be manually declared, restricted/unreviewed dependencies prevent shared-build readiness
- Status: OPEN (lead resolution is recorded separately)

## Question

Which selected map and reviewed dynamic config/model/audio supplement should a later integrated browser proof use? Can the lead provide approved replacements or recorded permission evidence for the existing personal-use player model, noncommercial weapons and other unreviewed assets before any shared pack is authorized?

## Evidence and impact

`source/src/main.cpp` invokes autostart hooks, saved/default settings, native private services, audio registration, model preloads and docs. `rendermodel.cpp` tries MD2/MD3 loaders and alternate skins; `hudgun.h` derives weapon names. `worldio.cpp::load_world` chooses external versus embedded map configuration. Static font traversal does not resolve those runtime decisions. `config/mapmodelattributes.cfg` is named by startup but absent in this checkout. Its required inventory record conservatively blocks closure pending the integration profile's explicit treatment.

`packages/models/playermodels/license.txt` requires consultation for use beyond personal use. `packages/models/weapons/license.txt` specifies attribution/noncommercial/share-alike. `packages/misc/license.txt` reserves all rights in blood.png and gives attribution without a clear grant for several other files. The generated manifest preserves these permission blockers and excludes restricted/unreviewed files from its shared-build view. No private config contents were read.

## Options for owner and lead

1. Define a minimal reviewed browser profile/map, list the exact dynamic supplement and approve separately scoped service/asset substitution work.
2. Retain the current startup path and inventory its full script/model/audio closure in a later ticket, with separate asset permission decisions before distribution.

The metadata-only T018 work proceeds independently and does not require choosing a map or changing services.

## Work paused

Only resolving the dynamic/map/permission blockers and constructing or claiming a complete shared bootstrap pack is deferred. Those actions are outside this ticket's implementation authority. T018 generator, fixtures, inventory and handoff are completed independently; no source change is requested from another worker.
