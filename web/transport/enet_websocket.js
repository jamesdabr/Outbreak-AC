// Emscripten JS-library platform component. No game parser or asynchronous C calls.
addToLibrary({
  $OutbreakWS: {
    consumed: false, generation: 0, session: null, lastOpenError: 9,
    staleCallbacks: 0,
    now: function() { return performance.now(); },
    valid: function(s, ws, generation) {
      if (this.session === s && s.live && s.ws === ws && s.generation === generation) return true;
      this.staleCallbacks++; return false;
    },
    bucket: function() { return { count: 64, bytes: 131072, at: this.now() }; },
    refill: function(b) {
      var now = this.now(), elapsed = Math.max(0, now - b.at) / 1000;
      b.count = Math.min(64, b.count + elapsed * 256);
      b.bytes = Math.min(131072, b.bytes + elapsed * 524288); b.at = now;
    },
    admit: function(b, n) {
      this.refill(b);
      if (b.count < 1 || b.bytes < n) return false;
      b.count--; b.bytes -= n; return true;
    },
    finishClose: function(s) {
      if (s.closeTimer !== null) clearTimeout(s.closeTimer);
      s.closeTimer = null;
      if (s.ws && s.closeHandler) s.ws.removeEventListener('close', s.closeHandler);
      s.closeHandler = null;
      s.closeObserved = s.closeObserved || (!!s.ws && s.ws.readyState === 3);
      if (s.closeObserved) s.ws = null;
    },
    stop: function(s, reason) {
      if (!s || !s.live) return;
      if (!s.error) s.error = reason > 0 && reason <= 15 ? reason : 3;
      s.live = false; ++this.generation; // invalidate before closing/racing callbacks
      s.queue.length = 0; s.queuedBytes = 0;
      if (s.timer !== null) clearInterval(s.timer);
      s.timer = null;
      document.removeEventListener('visibilitychange', s.visibility);
      if (s.ws) {
        s.ws.removeEventListener('open', s.openHandler);
        s.ws.removeEventListener('message', s.messageHandler);
        s.ws.removeEventListener('error', s.errorHandler);
        if (s.ws.readyState === 3) this.finishClose(s);
        else {
          var self = this;
          s.closeTimer = setTimeout(function() {
            // Browser has no terminate API: deadline releases owned listeners,
            // but does not pretend a noncooperative peer reached CLOSED.
            s.closeTimer = null;
            s.closeDeadlineMissed = s.ws.readyState !== 3;
            if (!s.closeDeadlineMissed) self.finishClose(s);
            // Otherwise retain this single passive observer until actual close
            // or owned page destruction (platform0.2); never forward data.
          }, 2000);
          try { s.ws.close(1000, 'backend closed'); } catch (_) { /* deadline still observed */ }
        }
      }
    },
    check: function(s) {
      if (!s || !s.live) return;
      var now = this.now();
      if (document.visibilityState === 'hidden') return this.stop(s, 15);
      if (s.lastFrame !== null && now - s.lastFrame > 1000) return this.stop(s, 15);
      if (!s.opened && now - s.started >= 2000) return this.stop(s, 2);
      if (now - s.started >= 1800000) return this.stop(s, 7);
      if (s.queue.length && now - s.queue[0].at > 500) return this.stop(s, 7);
      if (s.ws && s.ws.bufferedAmount > 0) {
        if (s.backlogAt === null) s.backlogAt = now;
        if (now - s.backlogAt > 500) return this.stop(s, 7);
      } else s.backlogAt = null;
    },
    get: function(handle) {
      var s = this.session;
      return s && handle === s.handle ? s : null;
    },
    status: function(handle) {
      if (handle === 0) return -this.lastOpenError;
      var s = this.get(handle);
      if (!s) return -9;
      this.check(s);
      if (s.error) return -s.error;
      if (s.ws.readyState >= 2) { this.stop(s, 3); return -s.error; }
      return s.opened && s.ws.readyState === 1 ? 1 : 0;
    },
    open: function() {
      if (this.consumed) { this.lastOpenError = 13; return -1; }
      this.consumed = true;
      var boot, values = {}, keys = ['schema_version', 'runId', 'endpoint', 'capability'];
      try {
        var root = Object.getOwnPropertyDescriptor(window, 'OUTBREAK_NETWORK_BOOT');
        if (!root || !Object.prototype.hasOwnProperty.call(root, 'value')) throw 0;
        boot = root.value;
        if (!boot || typeof boot !== 'object' || (Object.getPrototypeOf(boot) !== Object.prototype && Object.getPrototypeOf(boot) !== null)) throw 0;
        var names = Reflect.ownKeys(boot);
        if (names.length !== 4 || names.some(function(k) { return keys.indexOf(k) < 0; })) throw 0;
        keys.forEach(function(k) {
          var d = Object.getOwnPropertyDescriptor(boot, k);
          if (!d || !Object.prototype.hasOwnProperty.call(d, 'value')) throw 0;
          values[k] = d.value;
        });
        if (values.schema_version !== 1 || typeof values.runId !== 'string' || !/^[0-9a-f]{32}$/.test(values.runId) ||
            values.endpoint !== 'ws://outbreak.localhost:29865/enet' || typeof values.capability !== 'string' ||
            !/^[A-Za-z0-9_-]{21}[AQgw]$/.test(values.capability) || window.location.origin !== 'http://outbreak.localhost:29866') throw 0;
      } catch (_) { this.lastOpenError = 1; return -1; }
      var generation = ++this.generation;
      var s = this.session = {
        handle: generation, generation: generation, live: true, error: 0,
        ws: null, opened: false, started: this.now(), lastFrame: null, frameId: null,
        leftCount: 0, leftBytes: 0, queue: [], queuedBytes: 0, backlogAt: null,
        inbound: this.bucket(), outbound: this.bucket(), timer: null, closeTimer: null,
        closeObserved: false, closeDeadlineMissed: false, sent: 0, received: 0
      };
      var self = this, ws;
      try {
        ws = new WebSocket(values.endpoint + '?cap=' + values.capability, 'outbreak-enet-dgram.v1');
        s.ws = ws; ws.binaryType = 'arraybuffer';
      } catch (_) { this.lastOpenError = 2; this.stop(s, 2); return -1; }
      s.openHandler = function() {
        if (!self.valid(s, ws, generation)) return;
        self.check(s);
        if (!s.live) return;
        if (ws.protocol !== 'outbreak-enet-dgram.v1') return self.stop(s, 8);
        s.opened = true;
      };
      s.messageHandler = function(event) {
        if (!self.valid(s, ws, generation)) return;
        self.check(s); if (!s.live) return;
        if (!(event.data instanceof ArrayBuffer)) return self.stop(s, 4);
        var n = event.data.byteLength;
        if (n < 2 || n > 4096) return self.stop(s, 5);
        if (!self.admit(s.inbound, n) || s.queue.length >= 64 || s.queuedBytes + n > 131072) return self.stop(s, 6);
        // Independent ownership; async path never touches Wasm memory or parser.
        s.queue.push({ bytes: new Uint8Array(event.data).slice(), at: self.now() });
        s.queuedBytes += n; ++s.received;
      };
      s.errorHandler = function() { if (self.valid(s, ws, generation)) self.stop(s, 3); };
      s.closeHandler = function() {
        if (s.live && self.valid(s, ws, generation)) self.stop(s, 3);
        self.finishClose(s);
      };
      s.visibility = function() { if (document.visibilityState === 'hidden') self.stop(s, 15); };
      ws.addEventListener('open', s.openHandler);
      ws.addEventListener('message', s.messageHandler);
      ws.addEventListener('error', s.errorHandler);
      ws.addEventListener('close', s.closeHandler);
      document.addEventListener('visibilitychange', s.visibility);
      s.timer = setInterval(function() { self.check(s); }, 25);
      self.check(s);
      return s.handle;
    },
    send: function(handle, ptr, n) {
      var s = this.get(handle);
      if (!s) return -1;
      if (this.status(handle) !== 1) { this.stop(s, s.error || 2); return -1; }
      ptr = ptr >>> 0;
      if (n < 2 || n > 4096 || !ptr || ptr > HEAPU8.length || n > HEAPU8.length - ptr) { this.stop(s, 5); return -1; }
      if (s.ws.bufferedAmount + n > 131072 || !this.admit(s.outbound, n)) { this.stop(s, 6); return -1; }
      var bytes = HEAPU8.slice(ptr, ptr + n);
      try { s.ws.send(bytes); } catch (_) { this.stop(s, 3); return -1; }
      ++s.sent; this.check(s); return n;
    },
    recv: function(handle, ptr, capacity) {
      var s = this.get(handle);
      if (!s || this.status(handle) < 0) return -1;
      if (!s.queue.length || s.leftCount <= 0) return 0;
      var n = s.queue[0].bytes.length;
      if (s.leftBytes < n) return 0;
      ptr = ptr >>> 0;
      if (capacity < n || !ptr || ptr > HEAPU8.length || n > HEAPU8.length - ptr) { this.stop(s, 5); return -1; }
      var item = s.queue.shift(); s.queuedBytes -= n;
      HEAPU8.set(item.bytes, ptr); --s.leftCount; s.leftBytes -= n; return n;
    },
    frame: function(id) {
      var s = this.session; if (!s || !s.live) return;
      this.check(s); if (!s.live) return;
      id = id >>> 0;
      if (s.frameId !== null && (((id - s.frameId) >>> 0) === 0 || ((id - s.frameId) >>> 0) >= 0x80000000)) return;
      s.frameId = id; s.lastFrame = this.now(); s.leftCount = 32; s.leftBytes = 65536;
    },
    readiness: function(handle, conditions) {
      var s = this.get(handle);
      if (!s) return -9;
      if (conditions & ~3) { this.stop(s, 14); return -(s.error || 14); }
      var status = this.status(handle); if (status < 0) return status;
      var ready = 0;
      if (status === 1) {
        if (s.ws.bufferedAmount < 131072) ready |= 1;
        if (s.queue.length && s.leftCount > 0 && s.leftBytes >= s.queue[0].bytes.length) ready |= 2;
      }
      return ready & conditions;
    }
  },
  ob_ws_open__deps: ['$OutbreakWS'],
  ob_ws_open: function() { return OutbreakWS.open(); },
  ob_ws_status__deps: ['$OutbreakWS'],
  ob_ws_status: function(h) { return OutbreakWS.status(h); },
  ob_ws_send__deps: ['$OutbreakWS'],
  ob_ws_send: function(h, p, n) { return OutbreakWS.send(h, p, n); },
  ob_ws_recv__deps: ['$OutbreakWS'],
  ob_ws_recv: function(h, p, n) { return OutbreakWS.recv(h, p, n); },
  ob_ws_frame__deps: ['$OutbreakWS'],
  ob_ws_frame: function(id) { OutbreakWS.frame(id); },
  ob_ws_close__deps: ['$OutbreakWS'],
  ob_ws_close: function(h, reason) { var s = OutbreakWS.get(h); if (s) OutbreakWS.stop(s, reason); },
  ob_ws_readiness__deps: ['$OutbreakWS'],
  ob_ws_readiness: function(h, conditions) { return OutbreakWS.readiness(h, conditions); }
});
