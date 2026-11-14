# D446 — Preserve seven deliberately unreadable historical fixture files

T264's one observation ended BLOCKED_INPUT_READINESS on a pre-existing mode0000 twelve-byte bad-mode fixture. No native build ran or original changed. MAIN's read-only lstat/access scan found exactly seven such ordinary files, all historical non-consumed prerequisite fixtures, with no traversal errors. Changing their permissions/content is unnecessary and would disturb retained tests.

Approve BLACKWOOD_NATIVE_BUILD_PREPARATION0.2's narrow engineering amendment: the exact seven fixture paths below are retained by strict lstat identity, size, mode, owner, links, mtime and ctime rather than opening them for a content hash. All readable original files retain byte-hash preservation. Unknown unreadable paths still refuse. These seven may never be source-manifest/declared consumed inputs, framework/SDK/tool/dependency roles or alias targets. No generic permission-error fallback, prefix exemption, omitted old subtree or chmod is allowed. Before/after metadata equality remains required; content verification is explicitly unavailable for these seven test artifacts. No product scope, gameplay validation, budget, process ownership or final acceptance threshold changes.

Paths relative to repository, all bytes12/mode0000/nlink1/uid501/gid20/device16777232:

| Path | inode | mtime_ns | ctime_ns |
| --- | ---: | ---: | ---: |
| web/repro/tests/prerequisites/FIXTURE_ONLY-a6a8xiso/repo/web/build/.cache/bad-mode | 138018950 | 1794133833737008579 | 1794133833737028537 |
| web/repro/tests/prerequisites/T101/FIXTURE_ONLY-_ul9woy_/repo/web/build/.cache/bad-mode | 138138188 | 1794136186239760878 | 1794136186239782419 |
| web/repro/tests/prerequisites/FIXTURE_ONLY-am2d_ogp/repo/web/build/.cache/bad-mode | 138048696 | 1794134709255204182 | 1794134709255226848 |
| web/repro/tests/prerequisites/FIXTURE_ONLY-wxoxh5ho/repo/web/build/.cache/bad-mode | 138002194 | 1794133651660215054 | 1794133651660235304 |
| web/repro/tests/prerequisites/FIXTURE_ONLY-gx0ewpha/repo/web/build/.cache/bad-mode | 138037844 | 1794134245530215563 | 1794134245530245646 |
| web/repro/tests/prerequisites/FIXTURE_ONLY-hghnb9_0/repo/web/build/.cache/bad-mode | 138028804 | 1794134032415877479 | 1794134032415897853 |
| web/repro/tests/prerequisites/FIXTURE_ONLY-ktpjacgc/repo/web/build/.cache/bad-mode | 138010533 | 1794133723100585246 | 1794133723100612621 |

Release Player T265 for the minimal existing preservation-schema/helper correction and targeted guarded regression checks. All unrelated source behavior and historical evidence stay fixed. No native/tool/FFI/real build/runtime effect or repeat T264 observation is released here. After review, the current-input observation can be performed in a fresh output; actual build remains next. This resolves a specific obsolete test-history coupling, not a new audit framework.
