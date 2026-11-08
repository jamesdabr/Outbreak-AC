# T022 official SDK inspection and proposed setup

Scope: source acquisition and static inspection only. No acquired Python,
shell, compiler, Node binary or port recipe was executed. No installation,
activation, port download/build or game compilation occurred. T016/T017 remain
unverified for Wasm. This report proposes later actions; it does not authorize
them.

## Identities and acquired data

| Identity | Pinned value |
| --- | --- |
| Official manager commit | `1693ce7359fc9694f198694f902a2cc061239b86` |
| Manager archive SHA-256 | `fd37b19a256254cd90c1737062ee77ab4d82341c4c7bc890601b1a355034f345` |
| Approved SDK version | `7.0.0` |
| SDK release-build identity | `6afbd83493d647051772d491124187d4e9a0cda9` |
| Compiler source commit | `777e6e5db7b4990bcaeb1b9998ed642cc84e6629` |
| Compiler source archive SHA-256 | `80dc86d6a15382f234688fd491bd30692dc1c9f019c67563ae701176b9964d16` |

The manager's frozen `emscripten-releases-tags.json` maps exactly 7.0.0 to the
approved release-build identity. The [official release DEPS](https://chromium.googlesource.com/emscripten-releases/+/6afbd83493d647051772d491124187d4e9a0cda9/DEPS)
pins the compiler commit above, matching the official 7.0.0 tag. These are
three different repository identities. The release-build identity is neither
a manager commit nor an archive integrity digest.

`sources-and-artifacts.json` records all acquired URLs, byte counts and
locally measured SHA-256 values, inspected source-file hashes, future binary
artifact URLs and official recipe SHA-512 values. Local archive hashes bind
this inspection's bytes; no publisher signature or independent expected
SHA-256 for the two source archives was supplied by the inspected metadata.

Acquired source archives live only beneath
`/private/tmp/outbreak-web-sdk-inspection/`. Manager source is
`manager/emsdk-1693ce7359fc9694f198694f902a2cc061239b86/`; compiler source is
`compiler/emscripten-777e6e5db7b4990bcaeb1b9998ed642cc84e6629/`.
The own stdlib `extract_source.py` validates every member before writing,
rejects absolute/parent-escape paths, duplicate names, links and special
entries, bounds expanded size and writes files mode 0600. It never imports
the extracted code. Per-file extraction hashes are recorded in
`manager-extraction.json` and `compiler-extraction.json`.

## Inspection findings

References below are paths/line numbers in those exact source roots.

| Path | Inspected behavior and consequence |
| --- | --- |
| Manager `emsdk.py:33–44,207,475` | Download base is Google's webassembly bucket; installation root derives from manager file location, with relative `downloads/` resolved there. Moving the manager into the proposed SDK root confines normal installation paths there. |
| `emsdk_manifest.json:47–58,234–247,763–767` | macOS arm64 release uses the pinned `wasm-binaries-arm64.tar.xz`; full SDK depends on Node 24.19.0, Python 3.13.3 and release components, plus `sdk_post_install`. Proposed explicit component install avoids the extra Python and meta-package hook. Existing Python 3.11 meets the compiler's >=3.10 requirement. |
| `emsdk.py:496–509,551–595,660–742,1578–1620` | macOS invokes system `curl -f -L` then system `tar -xf ... --strip 1`; ZIP path uses zipfile and permissions. Downloads can retry the release `.tbz2` fallback. Existing install directories may be removed before extraction. No SHA-256/checksum enforcement was found in this manager's download path. Proposed execution must prevalidate archives and use a fresh SDK root, retain downloads, prohibit fallback substitution and record measured binary archive hashes before compiler execution. |
| `emsdk.py:1476–1525,2118–2218` | Full SDK meta-install can execute `npm ci --production` if packaged node_modules is missing. Git compiler installation can run bootstrap.py. Explicit Node and release component installs take archive paths with no custom installer hook and no npm invocation. If release node_modules or generated wrappers are missing, stop; do not invoke npm/bootstrap. |
| `emsdk.py:1794–1847,2660–2691` | Activation writes local `.emscripten`, moves an existing config to `.old`, and removes old local sanity marker. macOS activation does not itself source shell exports. No `--permanent`, `--system`, environment sourcing or `construct_env` execution is proposed. |
| Manager `emsdk`, `emsdk_env.sh` | Shell wrapper chooses Python then executes emsdk.py; env helper evaluates manager-generated shell text. Proposed commands bypass both using absolute existing Python and explicit child environment. No shell profile change. |
| Compiler `emcc.py:1–77`, `tools/install.py:51–120`, `bootstrap.py` | Packaged compiler is expected to have generated wrappers and node_modules prepared. The source checkout itself lacks emcc/em++ wrappers and says 7.0.0-git; it must not be substituted for the release package. Packaged version/revision and inspected source hashes must be checked after acquisition. tools/install.py's npm installation is a publisher packaging step, not an approved local action. |
| `tools/config.py:53–60,102–146,197–274` | Config is evaluated Python; explicit `EM_CONFIG` must point to the inspected generated local config. `EM_CACHE` and `EM_PORTS` override defaults; ports default to cache/ports. Missing config can otherwise cause tool auto-detection. Clean environment prevents inherited overrides. |
| `tools/shared.py:217–219,310–441,480–547` | Compiler sanity invokes Node and LLVM version/tool checks and writes sanity.txt to cache; Node compile cache defaults beneath cache. EMCC_TEMP_DIR controls scratch. Explicit Node cache and TMPDIR/EMCC_TEMP_DIR keep these local. No sanity bypass is proposed. |
| `tools/ports/__init__.py:153–170,223–285,304–449` | Recipes are imported/executed by a real compiler. macOS downloads use curl with redirects; downloaded data is checked against recipe SHA-512 before archive unpack. Source archives, extraction staging and URL markers go under PORTS. Build objects/libraries/headers go under cache; sysroot/header installation is real mutation. shutil.unpack_archive does not add this ticket's own strict source-archive member validator. |
| `tools/system_libs.py:38–44`, `tools/ports/__init__.py:260–283`, `tools/compile.py` | First use may run recursive emcc/em++, clang, llvm-ar and compiler subprocesses for sysroot/ports. Ninja is optional via EMCC_USE_NINJA; use a clean environment and no Ninja option. No CMake/make/autoconf or port repository configure script is invoked by the five selected recipes. |
| `src/settings.js:587,1510–1616`, selected port recipes | Existing probe setting names exist at this pinned revision. SDL2_IMAGE_FORMATS defaults to empty, so PNG/JPEG recipes are not selected by the current config. This is object-header feasibility, not a usable image-decoder/rendering profile. No existing flags are changed by T022. |

Selected ports and their dependencies:

| Port | Version | Fetch URL |
| --- | --- | --- |
| SDL2 | 2.32.10 | https://github.com/libsdl-org/SDL/archive/release-2.32.10.zip |
| SDL2_image | release-2.6.0 | https://github.com/libsdl-org/SDL_image/archive/refs/tags/release-2.6.0.zip |
| zlib | 1.3.2 | https://github.com/madler/zlib/archive/refs/tags/v1.3.2.tar.gz |
| Vorbis | 1.3.7 | https://github.com/xiph/vorbis/releases/download/v1.3.7/libvorbis-1.3.7.zip |
| Ogg (Vorbis dependency) | 1.3.5 | https://github.com/xiph/ogg/releases/download/v1.3.5/libogg-1.3.5.zip |

Each of these recipes supplies the exact SHA-512 in the JSON report. Those
expected hashes have been read, not verified against port downloads: no port
archive was acquired. GitHub tag archive redirects normally use
`codeload.github.com`; release assets may use
`release-assets.githubusercontent.com`. A later download must log the actual
redirect hosts and stop for unlisted hosts. Current source acquisition hosts
were `api.github.com`, `codeload.github.com`, and
`chromium.googlesource.com`. One incorrect attempted GitHub mirror URL for
DEPS returned HTTP 404, then the manager's explicit Googlesource source was
used. Initial sandbox DNS failure was retried through scoped approved curl;
no automatic approval rejection occurred.

SDK OpenAL and GL declarations are shipped in the compiler sysroot/source;
no external OpenAL port or host library link is proposed. ENet remains
repository headers only. libpng 1.6.59 and libjpeg 9f were inspected as
conditional dependencies but are outside this exact probe plan; enabling
formats would require a new scoped download/flag decision.

## Exact later setup proposal — not executed or authorized here

Repository cwd: `/Users/jd1/code/apps/outbreak`. First verify both pinned
source archives against the SHA-256 values above, ensure the proposed SDK
root is absent and nonsymlinked, and validate the release/Node archive members
as data before invoking manager extraction. Archive validation must reject
path escapes/special devices and resolve any symlink/hardlink targets within
the extracted destination after the manager's `--strip 1`. The T022 extractor
is deliberately source-only and rejects all links; do not use it as an
unreviewed binary-SDK installer. A later released ticket should own that small
validator and capture the binary archive SHA-256 plus actual redirect hosts.

Proposed binary downloads (not acquired under T022):

```sh
curl --fail --show-error --location --proto '=https' --proto-redir '=https' https://storage.googleapis.com/webassembly/emscripten-releases-builds/mac/6afbd83493d647051772d491124187d4e9a0cda9/wasm-binaries-arm64.tar.xz -o /private/tmp/outbreak-web-sdk/downloads/6afbd83493d647051772d491124187d4e9a0cda9-wasm-binaries-arm64.tar.xz
curl --fail --show-error --location --proto '=https' --proto-redir '=https' https://storage.googleapis.com/webassembly/emscripten-releases-builds/deps/node-v24.19.0-darwin-arm64.tar.gz -o /private/tmp/outbreak-web-sdk/downloads/node-v24.19.0-darwin-arm64.tar.gz
```

The inspected manager manifest supplies no expected integrity hash for these
two binary artifacts. Measure/store their SHA-256 and archive member review
before installation; do not label their build identity as integrity proof.
Only the two exact HTTPS URLs above are proposed. The manager's `.tbz2`
fallback is outside the proposal; prefetch with expected filename and
EMSDK_KEEP_DOWNLOADS=1 avoids invoking it when the validated files exist.

After a later decision authorizes the source copy and those downloads, prepare
the fresh root by copying the inspected manager as data (no source update):

```sh
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B -c 'import shutil; shutil.copytree("/private/tmp/outbreak-web-sdk-inspection/manager/emsdk-1693ce7359fc9694f198694f902a2cc061239b86", "/private/tmp/outbreak-web-sdk")'
mkdir -p /private/tmp/outbreak-web-sdk/downloads web/build/.cache/ports web/build/.cache/node_compile_cache web/build/generated/tmp web/build/generated/setup-inspection
```

Run these preparations **before** the two download commands. Then validate
archives as described above. No existing SDK root is overwritten. Next,
execute only the inspected manager component paths:

```sh
env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin EMSDK_ARCH=arm64 EMSDK_NOTTY=1 EMSDK_KEEP_DOWNLOADS=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=/Users/jd1/code/apps/outbreak/web/build/generated/tmp /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B /private/tmp/outbreak-web-sdk/emsdk.py install node-24.19.0-64bit releases-6afbd83493d647051772d491124187d4e9a0cda9-64bit
env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin EMSDK_ARCH=arm64 EMSDK_NOTTY=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=/Users/jd1/code/apps/outbreak/web/build/generated/tmp /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -B /private/tmp/outbreak-web-sdk/emsdk.py activate node-24.19.0-64bit releases-6afbd83493d647051772d491124187d4e9a0cda9-64bit
```

These use existing Python; no bundled Python component, full SDK meta-package,
postinstall npm fallback, bootstrap, update, shell sourcing or global activation.
Record stdout/stderr/exit codes in generated/setup-inspection. Before executing
the installed compiler, inspect the generated `.emscripten`, wrapper files,
`emscripten-version.txt` (must be 7.0.0), `emscripten-revision.txt` (must match
the pinned compiler commit if present), package/recipe hashes versus the
inspected source, and node_modules presence. Stop on unexpected code, path,
missing wrappers/modules or identity mismatch. The manager rewrites the
version file; that version string alone is not source authentication.

The intended config has LLVM_ROOT `/private/tmp/outbreak-web-sdk/upstream/bin`,
BINARYEN_ROOT `/private/tmp/outbreak-web-sdk/upstream`, EMSCRIPTEN_ROOT
`/private/tmp/outbreak-web-sdk/upstream/emscripten`, and NODE_JS
`/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node` (possibly expressed
using `$CFGDIR`). It must contain no external path or arbitrary extra code.

## Exact later object probes — also require a new release/authorization

The following are proposals for both clientgame.cpp and main.cpp, in release
and `_DEBUG`. They read player-owned main.cpp but do not edit it. The
T016/T017 owners/lead must pin current source hashes before executing them.
The flags match the existing config; no linking, asset packing or game launch.

```sh
env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin EMSDK=/private/tmp/outbreak-web-sdk EMSDK_PYTHON=/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 EM_CONFIG=/private/tmp/outbreak-web-sdk/.emscripten EM_CACHE=/Users/jd1/code/apps/outbreak/web/build/.cache EM_PORTS=/Users/jd1/code/apps/outbreak/web/build/.cache/ports EMCC_TEMP_DIR=/Users/jd1/code/apps/outbreak/web/build/generated/tmp TMPDIR=/Users/jd1/code/apps/outbreak/web/build/generated/tmp NODE_COMPILE_CACHE=/Users/jd1/code/apps/outbreak/web/build/.cache/node_compile_cache PYTHONDONTWRITEBYTECODE=1 /bin/sh -c '
  set -eu
  cd /Users/jd1/code/apps/outbreak
  emxx=/private/tmp/outbreak-web-sdk/upstream/emscripten/em++
  "$emxx" --version
  for unit in clientgame main; do
    "$emxx" --target=wasm32-unknown-emscripten -std=gnu++11 -fsigned-char -sUSE_SDL=2 -sUSE_SDL_IMAGE=2 -sUSE_ZLIB=1 -sUSE_VORBIS=1 -sLEGACY_GL_EMULATION=1 -O2 -Isource/src -Isource/src/bot -Isource/enet/include -c "source/src/$unit.cpp" -o "web/build/generated/setup-inspection/release-$unit.o"
    "$emxx" --target=wasm32-unknown-emscripten -std=gnu++11 -fsigned-char -sUSE_SDL=2 -sUSE_SDL_IMAGE=2 -sUSE_ZLIB=1 -sUSE_VORBIS=1 -sLEGACY_GL_EMULATION=1 -O0 -g -D_DEBUG -Isource/src -Isource/src/bot -Isource/enet/include -c "source/src/$unit.cpp" -o "web/build/generated/setup-inspection/debug-$unit.o"
  done
'
```

The loop is printed for review only and has not run. A later runner must save
each command/diagnostic/exit and object magic/hash, continue independent probes
after a source compile failure, and produce every criterion's actual result.
The existing T016 driver remains unchanged and can later reproduce its two
clientgame objects with an actual lead decision path once re-released. The
printed direct probes need no code change to that driver.

First use explicitly authorizes only the five listed ports and their recipe
SHA-512 validation, recursive target compilation/sysroot generation and normal
compiler sanity checks. Future acquisition of those third-party archives is
**not** covered by this source-inspection ticket. No host framework, binary
library, sdl2-config, PCH, game settings or native output is an input/output.
FROZEN_CACHE is not proposed for first use because missing ports/sysroot need
real preparation; later offline reruns can be separately verified.

## Scope, recovery and next authorization

Proposed writes: SDK/config/downloads only `/private/tmp/outbreak-web-sdk/**`;
ports/sysroot/Node cache only `web/build/.cache/**`; objects/logs/tmp only
`web/build/generated/**`. No shell profiles, user settings, credentials,
external repositories, database, public service or deployment. Stop rather
than widen paths/hosts, enable a missing npm hook, install more components or
change source/flags to suppress failures. Recovery is removal of newly owned
SDK/setup/cache outputs only if separately authorized; never reset/clean the
shared repository or delete a pre-existing SDK/cache.

Concrete next request: approve a new bounded setup ticket containing (1)
the pinned manager copy, two exact binary data downloads/member validation
and locally measured hashes, (2) the explicit component install/activation
commands with no postinstall hook, (3) installed-source/config comparison,
then (4) four real object probes and the five hash-pinned first-use ports,
using only the roots above. MAIN must freeze that authorization and
re-release the relevant execution tickets. T022 grants none of these later
execution actions.
