'use strict';
// T291 local13 successor; no listener starts merely by requiring this module.
const fs = require('node:fs');
const path = require('node:path');
const {startGateway} = require('../transport/gateway.cjs');
const RUN = path.join(__dirname, 'runs/local-13');

async function main() {
  if (process.argv.length !== 2 || process.cwd() !== RUN) throw Error('fixed_launch_required');
  const file = path.join(RUN, 'gateway-config.json');
  const info = fs.lstatSync(file);
  if (!info.isFile() || info.isSymbolicLink() || info.size > 1024) throw Error('invalid_config_file');
  const config = JSON.parse(fs.readFileSync(file, 'utf8'));
  let gateway = null;
  let stopping = null;
  let timer = null;
  function stop() {
    if (stopping) return stopping;
    stopping = (async () => {
      clearTimeout(timer);
      if (!gateway) return;
      await gateway.close('owner_close');
      const state = gateway.snapshot();
      const clean = state.cleanup.state === 'closed' && state.cleanup.timers === 0 &&
        state.cleanup.tcp_handles === 0 && state.cleanup.udp_handles === 0 && !state.failure;
      const admission_reasons = {
        ordinary_http: 0, header_timeout: 0, http_parse_error: 0, wire_rate: 0,
        upgrade_limit: 0, duplicate_header: 0, admission_headers: 0, admission_route: 0,
        admission_capability: 0, active_limit: 0, capability_replay: 0,
        retirement_capacity: 0, upgrade_error: 0, other: 0,
        admission_header_method: 0, admission_header_host: 0, admission_header_origin: 0,
        admission_header_version: 0, admission_header_protocol: 0, admission_header_upgrade: 0,
        admission_header_connection: 0, admission_header_key: 0, admission_header_extensions: 0,
        admission_header_cookie: 0, admission_header_authorization: 0, admission_header_proxy_authorization: 0
      };
      // Existing diagnostics contain at most 512 rows. Emit only fixed keys/counts.
      for (const entry of state.diagnostics) {
        if (typeof entry.reason === 'string' && Object.hasOwn(admission_reasons, entry.reason)) {
          admission_reasons[entry.reason]++;
        } else {
          admission_reasons.other++;
        }
      }
      process.stdout.write(JSON.stringify({event: 'gateway_closed', clean,
        admitted: state.counters.admitted, to_udp: state.counters.to_udp_datagrams,
        to_ws: state.counters.to_ws_datagrams,
        tcp_accepted: state.counters.tcp_accepted, tcp_rejected: state.counters.tcp_rejected,
        upgrade_attempts: state.counters.upgrade_attempts, rejected: state.counters.rejected,
        send_errors: state.counters.send_errors, admission_reasons}) + '\n');
      if (!clean) process.exitCode = 1;
    })().catch(() => { process.stderr.write('gateway_cleanup_failed\n'); process.exitCode = 1; });
    return stopping;
  }
  process.on('SIGTERM', () => { void stop(); });
  process.on('SIGINT', () => { void stop(); });
  gateway = await startGateway(config); // Existing exact config/one-use policy unchanged.
  if (stopping) { await gateway.close('owner_close'); return; }
  process.stdout.write('{"event":"gateway_listening"}\n');
  timer = setTimeout(() => { void stop(); }, 1790000);
}

if (require.main === module) {
  main().catch(() => { process.stderr.write('local_gateway_failed\n'); process.exitCode = 1; });
}
