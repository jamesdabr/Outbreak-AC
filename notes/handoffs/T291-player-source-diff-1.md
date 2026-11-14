# T291 successor launcher source diff

Starting source preserved outside successor run/bundle and exact seed validation changes. No launcher/helper import or runtime execution.

## web/visible/play_local.py

Starting SHA256 b8e5ba799b388b267923f109cc7f4700fd8ff1925eebfaca8d2bf47bee7d2519; final SHA256 14b54f153add27af22a2ae1f85970f47dc00b97fbda6d9bfa4ec04902039e5d2

```diff
--- local12-source/web/visible/play_local.py
+++ T291-local13-source/web/visible/play_local.py
@@ -1,5 +1,5 @@
 #!/usr/bin/env python3
-"""T266 fixed local visual playtest. SOURCE ONLY until MAIN releases --execute."""
+"""T291 fixed Swamp local visual successor. SOURCE ONLY until MAIN releases --execute."""
 import argparse
 import hashlib
 from http.server import BaseHTTPRequestHandler, HTTPServer
@@ -9,17 +9,26 @@
 import secrets
 import selectors
 import signal
+import stat
 import sys
 import time
 
 ROOT = Path(__file__).resolve().parents[2]
 HERE = ROOT / 'web/visible'
-RUN = HERE / 'runs/local-12'
+RUN = HERE / 'runs/local-13'
+SEED = HERE / 'seeds/swamp-1'
+SEED_FILES = {
+    'packages/maps/servermaps/ac_swamp.cgz': (23987, 'acb8d878f90fb4dfa1a53aa69b4500282bace127fe426a658f348a70a4fde9aa'),
+    'config/maprot.cfg': (110, '9769eb5c2da7eb813e199ea981e7c86c46eff418c97f3abfd89775a6d7bfeb9a'),
+    'notices/swamp/PROVENANCE.json': (1486, '4652125271f098fad58c1c30c86e3b6950e28667010633582907a5696f6933bc'),
+}
+SEED_DIRS = {'packages', 'packages/maps', 'packages/maps/servermaps', 'config', 'notices', 'notices/swamp'}
+ROTATION = b'ac_swamp dm weight:100 repeat:100 time:2 mintime:2 maxtime:2 minplayers:0 maxplayers:8 maxteamsize:8 manual:0\n'
 BASE = ROOT / 'web/server/blackwood-candidate-attempts/visible-native-3'
 NATIVE = BASE / 'debug/ac_server'
 NODE = Path('/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node')
 PAGE_ROUTE = '/web/visible/play.html'
-BUNDLE_ROUTE = '/web/visible/candidates/stock-combat-1/bundle/'
+BUNDLE_ROUTE = '/web/visible/candidates/swamp-1/bundle/'
 NATIVE_ARGS = ['-i127.0.0.1', '-f29863', '-c2', '-LS5', '-LF5', '-Hlogs/',
                '-Aconfig/serverparameters.cfg', '-Uconfig/servervita', '-Wdemo/',
                '-rconfig/maprot.cfg', '-Xconfig/serverpwd.cfg', '-Bconfig/serverblacklist.cfg',
@@ -56,32 +65,35 @@
     need((BASE / 'deps-signed/SDL2.framework/Versions/A/SDL2').is_file() and
          (BASE / 'deps-signed/SDL2.framework/Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi').is_file(),
          'Native sibling deps-signed framework required; no DYLD fallback')
-    need((BASE / 'runtime-seed').is_dir() and NODE.is_file(), 'Real native seed and fixed Node required')
-    need(not os.path.lexists(RUN), 'local-12 is occupied; no overwrite, cleanup or retry')
+    need(SEED.is_dir() and all(stat.S_ISDIR(p.lstat().st_mode) for p in (SEED, *SEED.parents)) and NODE.is_file(),
+         'Ordinary fixed Swamp seed and fixed Node required')
+    need(not os.path.lexists(RUN), 'local-13 is occupied; no overwrite, cleanup or retry')
     need(not any(p.is_symlink() for p in (RUN.parent, *RUN.parents)), 'Run ancestor symlink')
     # Accepted effect-free helper definitions only; no build/verify/main entrypoint.
     sys.path.insert(0, str(ROOT / 'web/server/blackwood_candidate'))
     import build as helpers
     need(Path(helpers.__file__) == ROOT / 'web/server/blackwood_candidate/build.py', 'Fixed helper module')
     seed = {}
-    for _, name, size, digest in helpers.stage.SEED_ROWS:
-        p = BASE / 'runtime-seed' / name
-        need(p.is_file() and not any(q.is_symlink() for q in (p, *p.parents)), 'Ordinary seed file')
-        raw = p.read_bytes()
+    seed_paths = list(SEED.rglob('*'))
+    need({p.relative_to(SEED).as_posix() for p in seed_paths} == set(SEED_FILES) | SEED_DIRS,
+         'Exact three-file Swamp seed and directory membership required')
+    for p in seed_paths:
+        info = p.lstat()
+        name = p.relative_to(SEED).as_posix()
+        need((stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and stat.S_IMODE(info.st_mode) == 0o644)
+             if name in SEED_FILES else stat.S_ISDIR(info.st_mode), 'Seed symlink/special/hardlink/type refused')
+    for name, (size, digest) in SEED_FILES.items():
+        p = SEED / name
+        need(p.stat().st_size == size, 'Exact seed length required')
+        with p.open('rb') as file:
+            raw = file.read(size + 1)
         need(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, 'Actual seed bytes changed')
         seed[name] = raw
-    rotation_path = BASE / 'runtime-seed/config/maprot.cfg'
-    need(rotation_path.is_file() and not any(p.is_symlink() for p in (rotation_path, *rotation_path.parents)), 'Ordinary seed rotation')
-    rotation = rotation_path.read_bytes()
-    need(rotation == helpers.stage.ROTATION, 'Actual Blackwood seed rotation required')
-    seed['config/maprot.cfg'] = rotation
-    seed_paths = list((BASE / 'runtime-seed').rglob('*'))
-    need(not any(p.is_symlink() for p in seed_paths), 'Seed symlink refused')
-    need({p.relative_to(BASE / 'runtime-seed').as_posix() for p in seed_paths if p.is_file()} == set(seed), 'Exact inert seed membership')
+    need(seed['config/maprot.cfg'] == ROTATION, 'Exact Swamp dm rotation required')
     routes = {PAGE_ROUTE: ((HERE / 'play.html').read_bytes(), 'text/html; charset=utf-8')}
     for name, mime in [('index.html', 'text/html; charset=utf-8'), ('index.js', 'application/javascript'),
                        ('index.wasm', 'application/wasm'), ('index.data', 'application/octet-stream')]:
-        p = HERE / 'candidates/stock-combat-1/bundle' / name
+        p = HERE / 'candidates/swamp-1/bundle' / name
         need(p.is_file() and not p.is_symlink(), 'Actual immutable bundle required')
         routes[BUNDLE_ROUTE + name] = (p.read_bytes(), mime)
     need(b'<head>' in routes[PAGE_ROUTE][0], 'Inspected player page injection point')
```

## web/visible/gateway_local.cjs

Starting SHA256 987f868e4622de68c5b6556aae8603179d0b7fc8744b6f18e9be9a05936bd630; final SHA256 505f2b00911047bc424e53f495c184d33f23f2d484eec944d925b65a6a0cc072

```diff
--- local12-source/web/visible/gateway_local.cjs
+++ T291-local13-source/web/visible/gateway_local.cjs
@@ -1,9 +1,9 @@
 'use strict';
-// T266 fixed wrapper; no listener starts merely by requiring this module.
+// T291 local13 successor; no listener starts merely by requiring this module.
 const fs = require('node:fs');
 const path = require('node:path');
 const {startGateway} = require('../transport/gateway.cjs');
-const RUN = path.join(__dirname, 'runs/local-12');
+const RUN = path.join(__dirname, 'runs/local-13');
 
 async function main() {
   if (process.argv.length !== 2 || process.cwd() !== RUN) throw Error('fixed_launch_required');
```
