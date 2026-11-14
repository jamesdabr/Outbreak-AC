# T084 D080 continuation handoff — required sanitizer still blocked

- Worker: World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf
- Ticket: T0845.7; contracts PORTABLE_FORMAT_FOUNDATION0.1 / D079, continuation D080. No status/self acceptance/phase changes.
- Base/pre-existing edits: same shared dirty tree as T084-world-1; no commits/reset/revert/source integration.
- Additive changed files: new retry_sanitizer.py, sanitizer-D080-1/**, terminal-freeze-2.json, own question T084-world-sanitizer-after-D080.md and this handoff. All242 previous frozen records unchanged; production/header/validator/corpus/native/Wasm artifacts unchanged.

## Acceptance evidence

PASS — Unchanged actual shared B decoder source and native/Wasm oracle evidence
from [first handoff](T084-world-1.md):9639cases/76batches,1376positive/8263negative,
every positive cell/metadata field equal, every negative destination/control/
canary byte untouched, all15failure categories, owned T064/T080 independent source
geometry plus synthetic6/7/8 maps and deterministic malformed/mutation corpus.
Native/Wasm full output SHA2567580f9b1ed9565f8a9145cf1062a04fc148e01f4b044fc8c2eecf89c45787062.

PASS — D080's ONE identical startup retry executed through platform scoped
require_escalated mechanism. Inspected new retry helper/pre-invocation plan
verified the exact original attempt1 executable, empty stdin, cwd, environment
and flags. No recompile/substitute/acquisition/suppression. No network/services.
The helper writes only new task-owned output; original task TMP/cache locations
remain as recorded. Existing timeout10s control preserved for empty-input retry.

FAIL / BLOCKED — Startup timed out again after10seconds, empty stdout/stderr.
Child killed/reaped; startup_pass=false, sanitizer cases=0/batches=0. Required
actual ASan/UBSan coverage remains NOT RUN, never promoted from compilation or
native/Wasm success. Stopped affected execution immediately as D080 requires;
no repeated retry or new runtime/flag experiment. All prior60s/10s timeouts kept.

PASS —38251 protected files unchanged before/after escalated retry; source and
frozen corpus inputs unchanged. Prior242-record terminal freeze independently
reverified. No current source/src/enet/assets/build/SDK/numeric or old evidence
mutation, commit, dispatch or integration.

NOT RUN — Native engine importer/render, shared capsule/navigation, gameplay,
balance, human/eight-player and fullP0/P1/MVP gates. Exact implemented source is
unused already-decompressed dry-flat subset, not general map support or actors.

## Reproduction/evidence

Do NOT rerun the one-shot retry. Its STARTED marker prohibits another invocation.
Inspect tests/outbreak/map-import/T084/retry_sanitizer.py and
sanitizer-D080-1/plan.json for exact command/environment/input hashes and flags.
startup.json records timeout/kill/reap; startup.stdout/.stderr preserve raw empty
outputs; result.json records failure and unchanged inputs. The final result is
still incomplete, with no sanitizer/full-ticket acceptance claim.

Original executable SHA256:
5c2d900240142f83a8adf212d9affc68873ad93b58805a1d06adedf48c376f8c.
Retry result SHA256:
7089a5d116284a26fccee07af6588797a84add795d7ec499a2a7ad81cd2d2a02.
Additive terminal-freeze-2.json (11new records; pins prior freeze and first
handoff; excludes itself/this handoff) SHA256:
b7c1d6a5be2f734664ae21d8f90a4012ae1432dd27bbee435ce47a49ec79770e.
Previous freeze SHA256 remains
b13b7fbdcbc86a37bc2ad917536f1f453536e473a5c007a8eee8cd61f3f08398.

## Integration and questions

Actual production decoder/native/Wasm test work is ready for review. Full-ticket
completion is blocked on required actual sanitizer coverage. New
[question](../questions/T084-world-sanitizer-after-D080.md) requests an explicitly
approved installed-runtime diagnostic or approved alternate local sanitizer
environment; startup failure cause is unknown. Existing source/corpus can be
reused under that release, with fresh additive evidence. No further execution or
changes inferred from this handoff. MAIN decides acceptance/release; no gate waived.
