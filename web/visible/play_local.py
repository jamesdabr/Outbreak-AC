#!/usr/bin/env python3
"""T266 fixed local visual playtest. SOURCE ONLY until MAIN releases --execute."""
import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import secrets
import selectors
import signal
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / 'web/visible'
RUN = HERE / 'runs/local-14'
BASE = ROOT / 'web/server/blackwood-candidate-attempts/visible-native-3'
NATIVE = BASE / 'debug/ac_server'
NODE = Path('/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node')
PAGE_ROUTE = '/web/visible/play.html'
BUNDLE_ROUTE = '/web/visible/candidates/stock-combat-1/bundle/'
NATIVE_ARGS = ['-i127.0.0.1', '-f29863', '-c2', '-LS5', '-LF5', '-Hlogs/',
               '-Aconfig/serverparameters.cfg', '-Uconfig/servervita', '-Wdemo/',
               '-rconfig/maprot.cfg', '-Xconfig/serverpwd.cfg', '-Bconfig/serverblacklist.cfg',
               '-Gconfig/geoip.cfg', '-Kconfig/nicknameblacklist.cfg', '-Iconfig/serverinfo',
               '-Oconfig/motd', '-gconfig/forbidden.cfg', '-Z0']
# Native also inherits loopback information UDP sockets 29864 and 28762.
OWNERS = []  # Retain original handles, including any unresolved cleanup.


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


class EndInteraction(BaseException):
    pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    if not args.execute:
        print('No effects. MAIN must release the fixed local visual playtest before --execute.')
        return 0

    started = time.monotonic()
    work_end, hard_end = started + 1800, started + 1830
    def check(end=hard_end):
        need(time.monotonic() < end, 'Original local playtest deadline')
    # Require the real current native build/seed BEFORE reservation or processes.
    need(NATIVE.is_file() and not NATIVE.is_symlink() and os.access(NATIVE, os.X_OK),
         'Real visible-native-3 debug binary required')
    need((BASE / 'deps-signed/SDL2.framework/Versions/A/SDL2').is_file() and
         (BASE / 'deps-signed/SDL2.framework/Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi').is_file(),
         'Native sibling deps-signed framework required; no DYLD fallback')
    need((BASE / 'runtime-seed').is_dir() and NODE.is_file(), 'Real native seed and fixed Node required')
    need(not os.path.lexists(RUN), 'local-14 is occupied; no overwrite, cleanup or retry')
    need(not any(p.is_symlink() for p in (RUN.parent, *RUN.parents)), 'Run ancestor symlink')
    # Accepted effect-free helper definitions only; no build/verify/main entrypoint.
    sys.path.insert(0, str(ROOT / 'web/server/blackwood_candidate'))
    import build as helpers
    need(Path(helpers.__file__) == ROOT / 'web/server/blackwood_candidate/build.py', 'Fixed helper module')
    seed = {}
    for _, name, size, digest in helpers.stage.SEED_ROWS:
        p = BASE / 'runtime-seed' / name
        need(p.is_file() and not any(q.is_symlink() for q in (p, *p.parents)), 'Ordinary seed file')
        raw = p.read_bytes()
        need(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, 'Actual seed bytes changed')
        seed[name] = raw
    rotation_path = BASE / 'runtime-seed/config/maprot.cfg'
    need(rotation_path.is_file() and not any(p.is_symlink() for p in (rotation_path, *rotation_path.parents)), 'Ordinary seed rotation')
    rotation = rotation_path.read_bytes()
    need(rotation == helpers.stage.ROTATION, 'Actual Blackwood seed rotation required')
    seed['config/maprot.cfg'] = rotation
    seed_paths = list((BASE / 'runtime-seed').rglob('*'))
    need(not any(p.is_symlink() for p in seed_paths), 'Seed symlink refused')
    need({p.relative_to(BASE / 'runtime-seed').as_posix() for p in seed_paths if p.is_file()} == set(seed), 'Exact inert seed membership')
    routes = {PAGE_ROUTE: ((HERE / 'play.html').read_bytes(), 'text/html; charset=utf-8')}
    for name, mime in [('index.html', 'text/html; charset=utf-8'), ('index.js', 'application/javascript'),
                       ('index.wasm', 'application/wasm'), ('index.data', 'application/octet-stream')]:
        p = HERE / 'candidates/stock-combat-1/bundle' / name
        need(p.is_file() and not p.is_symlink(), 'Actual immutable bundle required')
        routes[BUNDLE_ROUTE + name] = (p.read_bytes(), mime)
    need(b'<head>' in routes[PAGE_ROUTE][0], 'Inspected player page injection point')
    need(b'candidates/stock-combat-1/bundle/' in routes[PAGE_ROUTE][0], 'Stock-combat player page required')
    check()
    native_ops, gateway_ops = helpers.RealOps(), helpers.RealOps()
    native_ops.process_support(); gateway_ops.process_support()  # Original DarwinWaitid loader.
    acquiring = False
    def alarm():
        if not acquiring:
            raise EndInteraction()
    guard = {}
    server = None
    selector = None
    run_created = False
    total_log = 0
    pages_delivered = 0
    gateway_ready = gateway_clean = False
    errors = []
    records = []

    def drain(timeout=0):
        nonlocal total_log, gateway_ready, gateway_clean
        if selector is None: return
        for key, _ in selector.select(timeout):
            owner, stream, log = key.data
            try:
                data = os.read(stream.fileno(), 16384)
            except BlockingIOError:
                continue
            if not data:
                owner['eof'].add(stream)
                selector.unregister(stream)
                continue
            total_log += len(data)
            need(total_log <= 8 * 1024 * 1024, 'Combined child log bound')
            log.write(data); log.flush()
            owner['recent'] = (owner['recent'] + data)[-65536:]
            if owner['name'] == 'gateway' and stream is owner['child'].stdout:
                owner['lines'] += data
                while b'\n' in owner['lines']:
                    line, owner['lines'] = owner['lines'].split(b'\n', 1)
                    message = json.loads(line)
                    if message.get('event') == 'gateway_listening': gateway_ready = True
                    if message.get('event') == 'gateway_closed': gateway_clean = message.get('clean') is True

    def spawn(name, ops, argv, cwd):
        nonlocal acquiring
        owner = dict(name=name, ops=ops, child=None, recent=b'', lines=b'', logs=[], pipes=[], eof=set(), reaped=False)
        OWNERS.append(owner)
        env = dict(PATH='/usr/bin:/bin:/usr/sbin:/sbin', LANG='C', LC_ALL='C', TMPDIR=str(RUN / 'tmp'))
        check(work_end); acquiring = True
        try:
            owner['child'] = ops.spawn(argv, cwd, env)
            owner['pipes'] = [owner['child'].stdout, owner['child'].stderr]
        finally:
            acquiring = False
        child = owner['child']
        ops.retain(child)
        check(work_end)
        for label, stream in [('stdout', child.stdout), ('stderr', child.stderr)]:
            log = (RUN / 'logs' / (name + '.' + label)).open('xb')
            owner['logs'].append(log)
            ops.nonblock(stream); selector.register(stream, selectors.EVENT_READ, (owner, stream, log))
        return owner

    def observed(owner):
        return owner['ops'].observe_exit(owner['child'], check)

    def send_term(owner):
        ops, child = owner['ops'], owner['child']
        if observed(owner) is None:
            ops.wait_adapter.require_anchor(child); check()
            shutdown_signal = signal.SIGINT if owner['name'] == 'native' else signal.SIGTERM
            os.kill(child.pid, shutdown_signal)  # Exact original unreaped owned PID.

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup(); self.connection.settimeout(.5)
        def log_message(self, *_): pass  # No URLs, headers, boot data or capabilities in logs.
        def send_error(self, code, message=None, explain=None):
            self.send_response(code); self.send_header('Content-Length', '0')
            self.send_header('Connection', 'close'); self.end_headers(); self.close_connection = True
        def do_GET(self):
            nonlocal pages_delivered
            check(work_end)
            if self.headers.get('Host') != 'outbreak.localhost:29866' or self.headers.get('Transfer-Encoding') or self.headers.get('Content-Length', '0') != '0':
                self.send_error(400); return
            if self.path not in routes:
                self.send_error(404); return
            raw, mime = routes[self.path]
            if self.path == PAGE_ROUTE:
                if pages_delivered >= len(injections):
                    self.send_error(410); return
                injection = injections[pages_delivered]
                pages_delivered += 1  # Each of the two existing capabilities is delivered once.
                raw = raw.replace(b'<head>', b'<head>' + injection, 1)
            self.send_response(200); self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(raw))); self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff'); self.send_header('Connection', 'close')
            self.end_headers(); self.close_connection = True
            for offset in range(0, len(raw), 65536):
                check(work_end); self.wfile.write(raw[offset:offset + 65536])
        def do_HEAD(self): self.send_error(405)
        do_POST = do_PUT = do_DELETE = do_OPTIONS = do_PATCH = do_HEAD

    class LocalHTTP(HTTPServer):
        allow_reuse_address = False
        def handle_error(self, request, client_address):
            errors.append('http_request_failed')  # No raw request/credential traceback.

    try:
        native_ops.arm(guard, alarm, max(.001, work_end - time.monotonic()))
        RUN.parent.mkdir(parents=True, exist_ok=True); RUN.mkdir(mode=0o700)
        run_created = True
        acquiring = True
        try:
            selector = selectors.DefaultSelector()
        finally:
            acquiring = False
        check(work_end)
        for directory in ('native', 'tmp', 'logs', 'native/config/serverinfo', 'native/config/motd',
                          'native/logs/misc', 'native/logs/docs', 'native/demo', 'native/private',
                          'native/packages/maps/official', 'native/packages/maps/servermaps/incoming'):
            check(work_end); (RUN / directory).mkdir(parents=True, exist_ok=True)
        for name, raw in seed.items():
            p = RUN / 'native' / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(raw)
        (RUN / 'native/config/serverparameters.cfg').write_text('demo_save:0\nmandatory_auth:0\nlogthreshold_syslog:5\nlogthreshold_file:5\n')
        for name in ('serverpwd.cfg', 'serverblacklist.cfg', 'geoip.cfg', 'nicknameblacklist.cfg', 'forbidden.cfg'):
            (RUN / 'native/config' / name).write_bytes(b'')
        caps = [secrets.token_urlsafe(16), secrets.token_urlsafe(16)]
        need(caps[0] != caps[1], 'Distinct fresh capabilities')
        run_id = secrets.token_hex(16)
        config = dict(schema_version=1, run_id=run_id,
                      capability_sha256=[hashlib.sha256(c.encode('ascii')).hexdigest() for c in caps])
        with (RUN / 'gateway-config.json').open('x') as file:
            json.dump(config, file)
        os.chmod(RUN / 'gateway-config.json', 0o600)
        injections = []
        for capability in caps:
            boot = dict(schema_version=1, runId=run_id, endpoint='ws://outbreak.localhost:29865/enet', capability=capability)
            injections.append(('<script>Object.defineProperty(window,"OUTBREAK_NETWORK_BOOT",{value:Object.freeze(' +
                               json.dumps(boot, separators=(',', ':')) + '),writable:false,configurable:false});</script>').encode('ascii'))
        native = spawn('native', native_ops, [str(NATIVE), *NATIVE_ARGS], RUN / 'native')
        startup_end = min(work_end, time.monotonic() + 20)
        while b'dedicated server started' not in native['recent'] or b'added 1 servermaps' not in native['recent']:
            check(startup_end); need(observed(native) is None, 'Native exited during startup'); drain(.05)
        gateway = spawn('gateway', gateway_ops, [str(NODE), str(HERE / 'gateway_local.cjs')], RUN)
        ready_end = min(work_end, time.monotonic() + 5)
        while not gateway_ready:
            check(ready_end); need(observed(gateway) is None, 'Gateway exited during startup'); drain(.05)
        acquiring = True
        try:
            server = LocalHTTP(('127.0.0.1', 29866), Handler)
        finally:
            acquiring = False
        server.timeout = .05
        check(work_end)
        print('Local playtest: http://outbreak.localhost:29866/web/visible/play.html', flush=True)
        print('30-minute local session; two one-use player pages. Real server join/spawn required.', flush=True)
        while time.monotonic() < work_end:
            server.handle_request(); drain(0)
            need(observed(native) is None, 'Native exited during interaction')
            if observed(gateway) is not None:
                need(gateway_clean, 'Gateway ended without confirmed cleanup'); break
    except (EndInteraction, KeyboardInterrupt):
        pass
    except BaseException as error:
        errors.append(type(error).__name__)  # Never reflect credentials/config/URLs.
    finally:
        # Restore the one owned alarm first, then close only owned resources.
        native_ops.restore(guard, lambda action, error: errors.append(action), check)
        if server is not None:
            try: check(); server.server_close(); check()
            except BaseException: errors.append('http_close_unknown')
        for owner in reversed(OWNERS):
            if owner['child'] is None: continue
            row = dict(name=owner['name'], pid=owner['child'].pid, reaped=False, group_empty=False)
            records.append(row)
            try:
                check()
                try: send_term(owner)
                except BaseException: errors.append(owner['name'] + '_shutdown_signal_unknown')
                until = min(hard_end - 4, time.monotonic() + 4)
                while observed(owner) is None and time.monotonic() < until:
                    drain(.05)
                if observed(owner) is None:
                    owner['ops'].wait_adapter.require_anchor(owner['child']); check()
                    os.kill(owner['child'].pid, signal.SIGKILL); row['forced_kill'] = True
                check(); code = owner['ops'].wait(owner['child'], min(2, hard_end - time.monotonic()))
                owner['reaped'] = row['reaped'] = True; row['exit'] = code
                check(); row['group_empty'] = owner['ops'].group_empty(owner['child']); check()
                if not row['group_empty'] or code != 0: errors.append(owner['name'] + '_cleanup_failed')
            except BaseException:
                errors.append(owner['name'] + '_ownership_or_cleanup_unknown')
            # Drain the actual final pipe bytes/EOF before closing their logs.
            try:
                until = min(hard_end, time.monotonic() + .5)
                while len(owner['eof']) < len(owner['pipes']) and time.monotonic() < until:
                    check(); drain(.01)
                if len(owner['eof']) != len(owner['pipes']): errors.append(owner['name'] + '_capture_incomplete')
            except BaseException: errors.append(owner['name'] + '_capture_unknown')
            for value in owner['pipes'] + owner['logs']:
                try:
                    if value in owner['pipes']:
                        try: selector.unregister(value)
                        except KeyError: pass
                    check(); value.close(); check()
                except BaseException: errors.append(owner['name'] + '_close_unknown')
        try:
            if selector is not None: check(); selector.close(); check()
        except BaseException: errors.append('selector_or_log_drain_unknown')
        if not gateway_clean: errors.append('gateway_socket_cleanup_unconfirmed')
        result = dict(status='CLOSED_VISUAL_SESSION' if not errors else 'FAILED_OR_UNRESOLVED',
                      elapsed_seconds=time.monotonic() - started, children=records,
                      logs_bytes=total_log, page_delivered=pages_delivered > 0,
                      pages_delivered=pages_delivered, errors=errors,
                      rendering_and_input='REQUIRES_ACTUAL_OBSERVATION_NOT_INFERRED')
        try:
            check()
            if run_created:
                with (RUN / 'result.json').open('x') as file: json.dump(result, file, indent=2)
            check()
        except BaseException:
            errors.append('result_publication_or_deadline_unknown')
        result['status'] = 'CLOSED_VISUAL_SESSION' if not errors else 'FAILED_OR_UNRESOLVED'
        print(json.dumps(dict(status=result['status'], errors=errors)), flush=True)
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
