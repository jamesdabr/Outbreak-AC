# T060 World preparation handoff — execution NOT RUN

- Worker: World/Match-Systems, chat01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket reread: T060 revision3.1 RELEASED; browser foundation/GOVERNANCE/P0 0.5, D041 prerequisite3.0 and D044 preparation3.1. No gameplay/phase acceptance claimed.
- Base: `13f0d8eea4822dee5c976661218d022be74342e3`. Existing source/header changes, .gitignore and untracked AGENTS/MVP/tickets/notes/web were preserved. Assigned new script/config/test paths were absent. No commits or dispatch.
- Changed: NEW `web/build/build_audio_client.py`, `audio-config.json`, `verify_audio_bundle.py`, `tests/t060/test_tooling.py`, immutable evidence beneath `generated/t060/`, two own question notes and this handoff. No original driver/config/shell/pack/cache/output/source edits.

## Preparation evidence

PASS: syntax/import/helper tests after source inspection; `python3 -B -m unittest discover -s web/build/tests/t060 -p 'test_*.py' -v` gives20 passing tests. Final guarded run is `web/build/generated/t060/helper-tests-2.json`, SHA256 `4c50f3b013fb867c27472ef698c2d7aa11e958a8eee1328cb7d6b65279221888`. A subprocess mock forbade every compiler/Node invocation throughout tests and dry planning. Gate fixtures use temporary fake repository/decision roots, never real accepted pins. Negative cases cover missing/DRAFT/unreleased/hash-mismatched/escaping docs, missing/extra/changed input membership, preservation/alias identity changes and symlinked inputs. Alias tests cover exact chains, target-byte changes, changed text, escapes and unknown intermediate aliases. Synthetic preload fixtures validate all79 actual data slices and reject corrupt/duplicate/gapped slices; these are not linked engine artifacts.

PASS: `--plan-only --attempt web/build/generated/t060/attempt-plan-3` emits `NOT_EXECUTED`, `accepted_source_pins:false`, `pending_source_not_accepted:true`, `execution_ready:false`. SHA256 of its `plan.json`: `0ac6c20cc49062e6abc605806f5702f6261ba50c36da36390cfc3b7879bdc478`. It plans exactly53 genuine Makefile CPP plus8 existing ENet C units including unix.c, correct language tools and unchanged C/C++/port/link flags. Audio config differs only ticket/profile and explicit manifest/pack/output/attempt paths. It reads exact SDK7.0.0/compiler777e6e5..., Node24.19.0 regular executable hash, all six retained archives/recipes, and validates T053 through hash-checked inspected helpers. Manifest7def7d8... retains79 files/388764B,78 exact copies and sole two-line derived config, provenance/notices intact. No source acceptance is inferred from observation hashes; T059 remains pending.

PASS: final `preparation-check-3.json`, SHA256 `99ed8fad9805af2a6f7454ab351a5513f183ad211e674b650b16ae0cfa22c752`, records identical before/after6073 protected output/native/cache files plus264 pack/legacy files; subprocess calls0; `audio-out` absent. Earlier plans/checks/tests remain immutable; plan1/2 precede final driver changes and are historical preparation observations only.

OPEN: complete tool-inventory readiness. D044's four exact logical aliases are validated with exact decision SHA `7b78d4f0ce74b2e1f24459429409ba9e0350e52902b3b600f07c936b5684154f`, link-chain/text/root/final regular target hashes. Read-only follow-up inspection found unchanged O2 HTML linking calls `node_modules/.bin/html-minifier-terser`, another installed symlink not in D044. Final dry plan honestly reports this error and does not contain a complete accepted tool inventory. Strict execution refuses it. See `notes/questions/T060-world-sdk-html-minifier-alias.md` for precise SDK call sites and requested narrow MAIN decision. No implicit exception or SDK/flag rewrite was implemented. Original question is resolved only for its four D044 aliases.

## Implemented future recipe and verifier (not executed)

Future build preflight compares exact complete membership/hashes and MAIN authority/release fields before output mkdir or subprocess, rechecks after cache copying/compile/link and before publication. Inputs include all source/src and ENet C/CPP/shared headers/inc files, web/runtime headers/sources, Makefile, both drivers/verifiers/configs, shell, notices, all five original/derived pack closures/manifests/helpers, SDK inspection, compiler scripts/node modules/system headers/libraries, regular tool binaries, Node and the actual resolved Python executable. Logical SDK alias records and decision identity are separately required. VCS/bytecode metadata, unrelated uninvoked SDK bin aliases and npm .bin commands are outside regular-file tool inventory; the actually invoked HTML minifier logical path is explicitly checked and currently rejected. A missing/added/changed relevant path or unapproved symlink fails closed.

Preservation inventory includes exact current `web/build/out`, `web/server/out`, native source-tree object/library/executable products and original complete cache. A new direct `attempt-*` only is permitted; existing attempts and audio-out are refused. No object reuse: all61 objects are freshly compiled with actual commands/status/signatures/hashes, checked before link, and verified afterward. Original cache is copied to the new attempt; `EM_FROZEN_CACHE=1`, attempt-local temp/node/cache paths and clean exact environment are recorded. No acquisition fallback.

Future post-link validation checks successful exact link/Node `--check`/Node `WebAssembly.validate` commands (no game instantiation), actual HTML canvas/script, exact79 JS preload records/nonoverlapping contiguous data slices and their pinned hashes, Wasm signature, exact notices, all object/log/output hashes, metadata/result consistency and deterministic bundle identity. Matching read-only verifier takes explicit root/attempt/pins/SHA, rechecks current source/tool/preservation membership and outputs. Only a complete validated bundle is copied and renamed to absent `audio-out`. Historical attempt bundle/result remains. Runtime/audio audibility/model rendering/multiplayer stay explicitly unverified; embedded offline simulation and no gameplay sound mapping are stated truthfully.

## Future MAIN pins schema / command

No accepted pins document was created. Only MAIN after source acceptance, tooling review and separate execution release may supply an absolute `notes/decisions/*.json` path and its independently expected SHA256. Exact top-level keys, no extras:

- `schema`:1; `authority`:"MAIN"; `status`:"ACCEPTED"; `ticket`:"T060 revision 3.1"; `execution_release`:"EXPLICIT_AUDIO_BUILD_EXECUTION".
- `attempt`: the exact new repo-relative `web/build/generated/t060/attempt-NAME`.
- `inputs`: complete absolute regular input path->SHA256 mapping from a then-current successful strict `observe()`; exact equality required (not a subset).
- `preservation`: complete exact absolute preservation path->SHA256 mapping.
- `units`: ordered genuine61-source inventory; `ports`: exact six records with archive path/SHA256/SHA512 and installed recipe path/SHA256.
- `aliases`: exact D044 approved logical records; `alias_decision_sha256`: exact decision digest. A later minifier resolution will require a reviewed schema/recipe revision before execution.

The document's ownership/acceptance is an operator/MAIN responsibility; self-declared JSON fields or an observation plan do not grant project authority. Given an independently reviewed document and explicit later release, the intended command is:

```sh
python3 -B web/build/build_audio_client.py --execute --attempt web/build/generated/t060/attempt-MAIN-NAME --pins /Users/jd1/code/apps/outbreak/notes/decisions/MAIN-FUTURE-PINS.json --pins-sha256 MAIN_EXPECTED_64_HEX_DIGEST
```

Then read-only verification:

```sh
python3 -B web/build/verify_audio_bundle.py --audio-root /Users/jd1/code/apps/outbreak/web/build/audio-out --attempt /Users/jd1/code/apps/outbreak/web/build/generated/t060/attempt-MAIN-NAME --pins /Users/jd1/code/apps/outbreak/notes/decisions/MAIN-FUTURE-PINS.json --pins-sha256 MAIN_EXPECTED_64_HEX_DIGEST
```

These are future commands with placeholders, NOT executed. Current CLI fails closed on the unapproved minifier alias and absent future authority. No compiler/version/link/cache write/download/browser/game/server/package/network command ran. Actual execution path and end-to-end verifier on a real linked audio bundle remain NOT RUN; preparation/helper results cannot establish them.

## Exact new code identities

| File | SHA256 |
| --- | --- |
| web/build/build_audio_client.py | 0974999788af03da4ea01cd43014502e86e3867e79773f99246b8df0b4f1cf23 |
| web/build/audio-config.json | 9d68bdcc157da2f2ca615efd48f1fe2a00dd381b8d87e70da11dc0266741c437 |
| web/build/verify_audio_bundle.py | 8afe337ac0327066d87c7567ef0e94c5c1dd76c505f00f0de2282b4d9a55b240 |
| web/build/tests/t060/test_tooling.py | 956b43ce68957b8c95c7250f5abe39d4e12f146bb5728cbc5980ba2d9d344606 |
