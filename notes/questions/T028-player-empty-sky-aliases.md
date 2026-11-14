# T028 retained map loader requires six original empty-sky aliases

- Author / worker: player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e
- Ticket and revision: T028 0.5 RELEASED
- Phase and contract revision: BROWSER_FOUNDATION / GOVERNANCE 0.5; D005
- Exact clause or interface affected: T028 criteria 1/2/6 (real map load, required generated paths, visible failure); D005/T027 permits additional original aliases for proved literal bootstrap dependencies.
- Status: OPEN (lead resolution is recorded separately)

## Question

Please route the retained loader's six empty-sky paths into the original pack/integration closure. Main.cpp cannot supply media or change texture.cpp. Source implementation, native/Wasm object compilation and isolated helpers continue; actual map runtime remains blocked pending full linkage/pack closure.

## Evidence and impact

`source/src/texture.cpp::loadskymap` defaults `loadsky` to the empty string but does not skip loading when empty. Its loop unconditionally resolves `packages/%s%s_%s.jpg` with `legacyprefix="textures/skymaps/"` and six sides. `source/src/worldio.cpp::load_world` calls `loadskymap(true)` and records a missing-media warning when any face equals notexture. T028 startup rejects nonzero map-load warnings visibly instead of treating missing bootstrap media as a real-game pass.

At inspection the generated original browser/map configs do not set loadsky, and the pack has no paths for these six faces:

- `packages/textures/skymaps/_lf.jpg`
- `packages/textures/skymaps/_rt.jpg`
- `packages/textures/skymaps/_ft.jpg`
- `packages/textures/skymaps/_bk.jpg`
- `packages/textures/skymaps/_dn.jpg`
- `packages/textures/skymaps/_up.jpg`

This is a source-derived predicted runtime blocker, not a real-game failure observation. main.cpp's required-file list now names these proven literal dependencies so missing files fail early with the exact path. No stock sky media was copied and no World-owned file was edited.

## Options for owner and lead

Supply six original procedural aliases via T027's already-approved literal-dependency allowance, documenting their real encoded format and provenance; or separately authorize a renderer/config change with exact file ownership. The original-alias route preserves the retained renderer and main.cpp-only scope.

## Work paused

Actual integrated map validation awaits asset closure and a lead-provided linked artifact; source/compile/helper work is not paused. This note does not authorize another worker or change any ticket/contract.
