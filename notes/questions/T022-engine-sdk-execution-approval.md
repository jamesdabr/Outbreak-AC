# T022 inspected SDK setup proposal for lead authorization

- Author / worker: Engine & Multiplayer
- Ticket and revision: T022 revision 0.4 RELEASED
- Phase and contract revision: P0 prerequisite subset 0.4; BROWSER_FOUNDATION 0.4; GOVERNANCE 0.4
- Exact clause or interface affected: T022 criteria 3–5 and exclusion of installer/compiler/port execution; T016/T017 missing Wasm prerequisites
- Status: OPEN (lead resolution is recorded separately)

## Question

Will MAIN record and release the bounded setup/verification operation in
`web/build/sdk-inspection/REPORT.md` after reviewing its exact commands and
source evidence? This is the concrete next authorization request, not a
request to expand T022 or silently resume blocked T016.

## Evidence and impact

Official manager commit `1693ce7359fc9694f198694f902a2cc061239b86` and
compiler source commit `777e6e5db7b4990bcaeb1b9998ed642cc84e6629` were acquired
as data and inspected. Official frozen manager metadata maps 7.0.0 to release
build `6afbd83493d647051772d491124187d4e9a0cda9`; that build's official
Googlesource DEPS confirms the inspected compiler commit. Archive and
individual file SHA-256 values, exact proposed URLs and official port
SHA-512 expectations are in `sources-and-artifacts.json`.

Full SDK meta-install can fall back to npm ci. The proposed explicit
Node 24.19.0 and pinned release component install bypasses that meta-hook
and reuses existing Python 3.11. It stops if packaged wrappers/node_modules
are missing. No npm, bootstrap, global install or shell sourcing is proposed.
The manager's archive download path lacks independent checksum enforcement;
binary archives have not been acquired and no publisher integrity hash was
supplied by the inspected manifest. The proposed next ticket must validate
member paths/links and record measured archive hashes before execution.

## Options for owner and lead

1. Release a setup ticket approving the exact two Google bucket binary
   downloads, fresh pinned manager copy, member/hash validation, explicit
   component install/activation, installed source/config comparison, then
   four real release/debug clientgame.cpp/main.cpp object probes with the
   five listed SHA-512-pinned ports. Exact commands/environment are in REPORT.
   SDK/config/download writes: `/private/tmp/outbreak-web-sdk/**` only.
   Port/sysroot/Node cache: `web/build/.cache/**` only. Object/log/tmp:
   `web/build/generated/**` only. No user/profile/global setting writes,
   external repository execution, databases, servers or publication.
2. Supply an already prepared and inspected SDK/ports with exact identities
   under those roots, then authorize the local compiler probes only.

Recovery, if later needed and separately authorized, is limited to newly
task-owned SDK/cache/probe files. No shared-tree reset/clean and no deletion
of a pre-existing root/cache. Stop on any unlisted host/path, archive escape,
identity mismatch or unexpected installer hook.

## Work paused

T022 source inspection is complete. SDK binary acquisition, installer
execution, activation, ports and compiler probes remain outside T022 and
unexecuted. T016/T017 Wasm acceptance remains outstanding.

The applied [confirm-cross-system-execution skill](/Users/jd1/.codex/skills/confirm-cross-system-execution/SKILL.md)
instructs: “Inspect first, explain the boundary crossing, and wait for explicit
approval before running the proposed command.” The report makes that later
operation concrete; T022 itself also explicitly prohibits it. No automatic
approval review rejection occurred.
