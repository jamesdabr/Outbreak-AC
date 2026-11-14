# D466 — Fresh local2 session with loopback socket permission

D465 local1 terminated exit1 before HTTP/gateway startup: native fatal could not create server info socket. Original PID7592 reaped exit1, group_empty:true; no page delivered, no child left running. Preserve local1 logs/result. Read-only lsof of exact UDP29863/29864/28762 found no listener. Native source serverms.cpp confirms this fatal is socket create/bind failure. Network-restricted sandbox is the suspected cause; not proved by errno because legacy fatal omits it.

MAIN changes ONLY both launcher-owned fixed run literals local-1→local-2 and corresponding docs, retaining old source copies in notes/preflight/MAIN-local1-*. All native/game/browser/transport code, binary/seed identities, arguments, ports, capabilities, output/process/deadline/cleanup limits unchanged. Verified native3 build remains its prior point-in-time acceptance; no renewed source-manifest/protected-root claim. No binary rebuild is needed for a launcher output-directory literal.

Release ONE fresh exact D465 local visual invocation with execution-tool escalation to permit the already reviewed loopback sockets, under new runs/local-2 only. Automatic approval review must permit it before execution; no alternate attempt after rejection. Existing reviewed active-project game implementation scope and all D465150s/120s/8MiB/loopback/no-external/no-Git/no-database limits apply. No broader service or privilege use, no port changes, no old-output deletion/reuse. MAIN opens existing preview tab once, actual UI only; save actual screenshots. QA/T149 remain paused.

Current wrapper SHA256:
{
  "play_local.py": "7707c11bf75582efa2c03aee15eb4cb9775939f63c97932d147257f4431ee8b6",
  "gateway_local.cjs": "15d65f6bbdce65cc88c149b1ee169a858bb9040524635b7072d461a40fbad60a"
}
