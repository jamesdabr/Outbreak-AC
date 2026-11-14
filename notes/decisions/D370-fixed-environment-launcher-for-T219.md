# D370 — Bind the fixed clean-environment launcher for T219

MAIN resolves T219's source-construction dispatch seam. This does NOT execute the caller/job or grant an actual lease. Existing T219 source-only construction continues under D368; no project source edits or output/scaffold writes.

Select /usr/bin/env -i followed ONLY by fixed ENV assignments,canonical Python3.11.9 -I -B and the literal T219 caller path. This known system utility replaces its process image with Python; it does not add a project subprocess or probe. The exec tool's ordinary shell/PTY wrapper is part of the observed original command; don't claim that zero pre-Python executable images existed. No self-reexec,shell sanitizer,dynamic command,version/help probe or fallback.

Exact proposed command:

/usr/bin/env -i PATH=/usr/bin:/bin LANG=C LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -B /Users/jd1/code/apps/outbreak/notes/proposals/T219-blackwood-deadline-caller-1.py

Tool options repo cwd,login=false,tty=true,yield1000,max_output_tokens8192; ONE future original command/session,original caller300s whole. Original hard interval also requires external tool observation; no timer reset from env/bootstrapping/inner source. Poll same livehandle<=30s after future explicit dispatch,never restart from observationtimeout. Actual scope/caller/effect review and literal MAIN dispatch remain separately required. All source16/fixedfinite inputs/histories/pre-post-through protection/denial/evidence/retention/capture/case/cleanup/terminal limits remain.

Read-only MAIN launcher descriptor/hash snapshot:

```json
{
  "bytes": 102368,
  "ctime_ns": 1779353822000000000,
  "device": 16777232,
  "inode": 1152921500312571973,
  "mode": "100755",
  "mtime_ns": 1779353822000000000,
  "nlink": 1,
  "path": "/usr/bin/env",
  "sha256": "6e506aec3c0cff703ac1e66cedc6f1945354ad41339a38db4425c7c88227128f"
}
```

This is an explicitly selected system executable launcher role,not ordinary consumed game/test DATA. Preserve its actual nlink/type/mode/identity; no broad single-link data exemption follows. Canonical Python remains separately pinned. T219 author may update its still-unsubmitted own caller/input/protection/effect inventories to bind this decision and exact launcher role,with fresh stable selfconsistent pins/counts. Do not execute the utility/caller now. Independent reviewer must check exact launch/scope/observed-original semantics before any actual release. No held/user-profile/network/game effect is authorized.
