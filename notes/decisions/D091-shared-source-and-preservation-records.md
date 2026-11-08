# D091 — Shared source package and opaque historical links

MAIN technical amendment to candidate browser/native PREPARATION contracts0.1→0.2 and released tickets T0885.11→5.18/T0925.15→5.19. File ownership, fixed recipes/commands/flags/output roots, source manifest field schema, ordinary source/tool/actual-dependency/authority gates unchanged. No actual build/runtime or new dependency.

## One reviewed source manifest for both targets

web/repro/source-manifest.json represents ONE MAIN-reviewed source package for browser+native tooling and the portable game sources, rather than a different exact per-recipe list at the same path. Every listed ordinary file must match its exact hash/size/mode, sorted unique canonical names; every current recipe's required production/helper/decision source must be included. A recipe must reject missing consumed members. Additional explicitly MAIN-listed ordinary source/doc/fixture members for the other target are valid package members, never executable selectors or implicit dependency permissions. Add all listed entries to the stable source input inventory so changes during build/verification fail. Unknown/unlisted files actually consumed by compiler remain rejected. A new manifest/member change still needs new MAIN expected digest and execution pins.

Do not enforce equality with only one recipe's closure or an arbitrary maximum of one .md decision. Both builders consume and validate the same source_manifest SHA and reviewed source revision. Authorization decision is explicitly included/hashed; interpreter and required imported stdlib identities are recorded separately as authoring-tool inputs. Existing Python3.11.9 at /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 and its actually imported stdlib/extension files are allowed authoring inputs, not an arbitrary program hook. Compiler/signing roles remain the fixed installed tool list.

The manifest excludes itself. Source code commit is created first; its manifest is generated afterwards against that exact revision as release/build metadata, so there is no self-referential Git commit hash. That generated manifest and future MAIN execution pins may be provided as documented build prerequisites in an otherwise clean checkout; they must not be misrepresented as a pre-existing dirty source overlay.

## Exact preservation record, common to both targets

observation.preservation is now exactly {files,directories,links,absent_roots}:
- files: map canonical absolute ordinary file→SHA256 (never a symlink-followed file);
- directories: sorted unique canonical absolute ordinary directory paths;
- links: map canonical absolute link location→{target:exact raw link text,mode:integer lstat permission mode};
- absent_roots: sorted unique canonical absolute explicitly protected roots absent at baseline.

Walk protected historical trees with followlinks=false. Preserve existing directory/file/link membership and ordinary bytes/modes as required by their role. Historical link records are opaque provenance, never followed or approved as a compiler input, source manifest entry, output alias or path escape. This includes genuine old deps-signed framework links and intentionally malformed retained test-fixture links; do not reject or dereference the latter merely to preserve them. Link ancestors in consumed source/tool/output paths remain forbidden except separately declared approved SDK/framework chains. New owned outputs remain ordinary confined paths, with only separately allowed native staged-framework links. Every originally recorded link must retain exact location/text/mode, unexpected additions/removals fail. Do not exempt entire history/output roots.

Existing protections were private historical map shapes. Updating them before any actual successor execution is necessary to avoid rejecting unchanged valid historical framework links or forcing clean builds to carry old test caches. This is not a raw-hash waiver or permission to change old artifacts. Tests must distinguish opaque protected link preservation from forbidden link traversal in actual inputs/outputs, and shared declared source-package members from undeclared consumed headers. Retain intermediate failed fixture receipts; final prep re-reviews amended contracts and private schema.
