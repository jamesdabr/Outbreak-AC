# T018 metadata inventory and generator handoff

- Worker: World/Match-Systems / `01a1b92c-db5c-7a10-a0e4-46e1f5a092cf`
- Ticket / revision: T018 revision 0.3 RELEASED; submitted for lead review only, no authoritative acceptance/status change
- Phase / contract revisions: BROWSER_FOUNDATION 0.3, GOVERNANCE 0.3, P0 0.3 prerequisite subset, MVP README 0.3; product/parameters/interfaces 0.2 draft context
- Base commit and pre-existing edits: `13f0d8eea4822dee5c976661218d022be74342e3`, with exact dirty baseline in `notes/decisions/D003-source-baseline.json`. Initial status had combat changes in bot.cpp, clientgame.cpp, entities.cpp, entity.h, physics.cpp, protos.h and weapon.cpp, plus the untracked Outbreak header/contracts/notes. No `web/assets` directory existed at start. Other workers' subsequent main.cpp/platform.h/tools.h work was observed and preserved; no source/config/asset files were written by this worker.
- Changed files: `web/assets/generate_manifest.py`, `manifest.schema.json`, `bootstrap_roots.json`, `README.md`, `tests/test_manifest.py`, `tests/fixtures/config/root.cfg`, `tests/fixtures/config/nested.cfg`, `generated/bootstrap-manifest.json`, `generated/bootstrap-manifest-report.txt`, `generated/validation-report.json`; own question `notes/questions/T018-world-dynamic-bootstrap-closure.md`; this handoff.
- Commit or patch reference: none; no commit/push/branch/worktree/reset/revert operation authorized or performed.

## Acceptance evidence

1. **PASS** — `web/assets/bootstrap_roots.json` defines explicit mandatory roots, optional platform icon, excluded optional/private profile services, selected-map requirements, source references and dynamic/uninspected categories. It names each startup configuration that remains unresolved. `README.md` explains native versus browser virtual lookup assumptions. There are 12 declared roots and 22 discovered entries, never directory or checkout preloads. No CubeScript is evaluated. Root selection is the bounded inspected candidate, not a claim of complete startup assets.
2. **PASS** — two invocations of `python3 web/assets/generate_manifest.py` on unchanged inputs returned exit 1 (expected incomplete inventory), identical JSON bytes and identical text-report bytes. Manifest SHA-256: `913ef9c931cf9b65d2de9bb480feee9e85d5c7844f3bbae8af22b9f8bf8d0b77`. Text report SHA-256: `0231ac24d808bc2749ddfe713cb2190036d7a0ba0e04474f24b509833e8bd609`. Counts/hashes independently checked against each included source file. Python `3.11.9` (Clang 13.0.0), macOS 26.5.1 arm64; version/platform are recorded separately in `generated/validation-report.json`, absent from deterministic manifest/report.
3. **PASS** — actual checkout inventory includes `packages/misc/notexture.jpg`, `config/font.cfg`, nested default/monospace/serif configs, their texture dependencies and HUD atlases. Every included entry records byte length, SHA-256, classification, provenance and permission status/evidence. All entry hashes, sizes, lexical uniqueness, virtual uniqueness and aggregate sum were independently checked with Python hashlib/Path. Missing startup `config/mapmodelattributes.cfg` is explicitly reported, not treated as a successful load.
4. **PASS** — `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web/assets/tests -v`: **11 tests passed**. Covers nested references, repeats, cycles, requiredness propagation, required/optional missing input, dynamic expressions, duplicate roots and normalized virtual collisions, conflicting virtual paths, source traversal/absolute/private/hidden paths, virtual escape, outside symlinks, private aliases, identical validation for supplements, permission evidence/filtering, and actual CLI failure codes with parent/rejected-reference diagnostics. Fixtures are newly authored text; temporary symlinks/files are confined to unittest temporary directories and cleaned there.
5. **PASS** — actual permission report blocks shared readiness. There are 19 restricted/unreviewed entries; the filtered candidate view contains only 3 file-specific candidate-permitted entries. Required restricted player model/weapon config sentinels retain their personal-use/noncommercial notice pointers/reasons, and blood.png retains its all-rights-reserved blocker. Engine license is never used as asset permission. Both readiness booleans remain false while required dependency or permission blockers exist. No notice or license changed.
6. **PASS** — size/candidate/unresolved lists below and exact generated manifest/report provide review evidence. No media was repackaged, no preload pack was made, and no actual browser load was verified by this ticket.

Additional checks: JSON Schema file parses as JSON; manifest/entry required keys match schema declarations, semantic hash/count/filter/path assertions pass. A full third-party JSON Schema validator was **NOT RUN** (ticket permits standard library only; no dependency added). Real game/browser/native execution, Emscripten packaging, persistence and multiplayer are **NOT RUN**, outside T018 scope. This evidence does not satisfy T014/T015/P0 and does not claim a playable browser game.

## Implementation status

Implemented: read-only partial config traversal with explicit unresolved records; normalized confined source/virtual paths and collision checks; private-path rejection before reads; SHA-256 and byte counts; deterministic provenance and reports; manual supplement validation without implicit dynamic resolution; conservative file-specific permission evidence and filtered shared-build metadata; failure exit codes; authored fixture tests. No simulation of engine execution is used. Text atlas fixtures are test doubles only.

Incomplete by design and explicitly blocked: full startup configuration closure, autostart/aliases, selected-map content/embedded config, model geometry/skins, registered sounds, docs/loading/igraph assets and distribution permission for every required file. Static analysis is not runtime closure proof. Unsupported model commands remain unresolved instead of guessing MD2/MD3/skin alternatives. Supplement entries cannot silently clear unresolved expressions. The generator is intended for ordinary local repository files; it does not search native home profiles, archives or package overlays.

Raw-size summary: **22 entries / 513,359 raw bytes**; **21 required entries / 512,043 bytes** and **1 optional icon / 1,316 bytes**. Candidate-permitted filtered metadata covers **293,065 bytes** (`chars_monospace.png`, `chars_serif.png`, `explosion.png`), not a functional or cleared pack. No compressed-transfer, browser heap or startup-time claim is made.

Smallest justified explicit candidate for the inspected calls (not a complete game):

- `config/font.cfg`, `config/font_default.cfg`, `config/font_monospace.cfg`, `config/font_serif.cfg`.
- `packages/misc/notexture.jpg`, `chars_default.png`, `chars_monospace.png`, `chars_serif.png`, `huddigits.png`, `serverquality.png`, `bargraphs.png`, `radaricons.png`.
- Particle textures under `packages/misc/`: `base.png`, `smoke.png`, `explosion.png`, `bullethole.png` (decal modifier is metadata, not part of path), `blood.png`, `scorch.png`, `muzzleflash.jpg`.
- `packages/misc/icon.png` optional pending browser platform guard selection.
- `packages/models/playermodels/md2.cfg` and `packages/models/weapons/knife/md3.cfg` are restricted model dependency/permission sentinels, not a substitute for the model files themselves.

Explicit unresolved list: **27 records** in `generated/bootstrap-manifest.json` and the human report:

- Dynamic autostart scripts/hooks/aliases from startup.
- Runtime model names/geometry/skins and audio, with restricted notices.
- Selected map, default/per-map/embedded config; no map chosen.
- Auxiliary loading/igraph/docs/resdata dependencies.
- `config/scontext.cfg`, `keymap.cfg`, `mapmodelattributes.cfg` (missing), `menus.cfg`, `scripts.cfg`, `prefabs.cfg`, `sounds.cfg`, `securemaps.cfg`, `admin.cfg`, `defaults.cfg`, `docs.cfg` (all under config; uninspected closure except the missing file).
- Built-in `registerdefaultsounds` sound paths and decoder/backend requirements.
- Five unsupported commands with exact parent line numbers in playermodel `md2.cfg` and six in knife `md3.cfg` (including `md3load tris_high.md3` and the weapon/hands skin declarations). Exact expressions are retained in the manifest/report.

## Integration and questions

Canonical output: `web/assets/generated/bootstrap-manifest.json`. Human-readable provenance/dependency report: `web/assets/generated/bootstrap-manifest-report.txt`. Execution evidence: `web/assets/generated/validation-report.json` contains exact generator/test commands, both return codes/stdout/stderr, independent-validation results, environment and hashes.

Reproduce from `/Users/jd1/code/apps/outbreak`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s web/assets/tests -v
python3 web/assets/generate_manifest.py
shasum -a 256 web/assets/generated/bootstrap-manifest.json web/assets/generated/bootstrap-manifest-report.txt
python3 web/assets/generate_manifest.py
shasum -a 256 web/assets/generated/bootstrap-manifest.json web/assets/generated/bootstrap-manifest-report.txt
```

Generator exit 1 is the expected blocked inventory outcome; tests exit 0. No public server or package installer is needed. Use `--supplement PATH` only for a reviewed explicit JSON roots list; it passes the same validation and adds evidence without clearing dynamic blockers.

No shared source interface changed; schema v1 stays within T018's approved metadata boundary. No new dependency or media asset was added. Lead must review candidate permission reasoning, choose the map/browser service profile, resolve the question in `notes/questions/T018-world-dynamic-bootstrap-closure.md`, and separately authorize integration/asset replacement or packaging. Do not consume the filtered 3-entry candidate view as a game pack. Ticket and pinned governing revisions were re-read before handoff and remain 0.3.
