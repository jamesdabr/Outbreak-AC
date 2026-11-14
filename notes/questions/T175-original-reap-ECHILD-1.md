# T175 original reap boundary after guarded pass

Worker /root/review_native_candidate; T1751.0 / BUILDER_TERMINAL_GROUP_CLOSURE0.1/D263. Source edits/retry are prohibited after the sole pass10 invocation.

MAIN identified a possible shared T174 reap-boundary issue after T175's guarded pass had passed. Read-only inspection confirms T175 recipe.py:761 calls child.wait(timeout=...) and then marks parent_reaped=true. Installed Python3.11 subprocess.py:2008–2017 catches ChildProcessError in _try_wait and returns (self.pid,0); _wait consumes that path at2037–2040. Thus ECHILD after the fresh WNOWAIT/signal boundary can be hidden by Popen.wait, even though D263 requires lost original ownership to refuse. No such real event was observed in this task; no syscall/probe was executed.

Source pins: recipe.py fefb90727956e49a11ab6617c9657bde711f225f5e0c320ef857e1f47e7b52aa; installed stdlib subprocess.py baa9f9138d8d20df6284f67e7d2e790f847f65e2c5370de322d54cccd737f2d9. The latter was read/hashed as source only, not imported or called.

Current pass10's anchor-loss/ECHILD leaf raises from the fresh nonreaping observation before SIGKILL. It does not discriminate ECHILD masked by the underlying post-signal Popen.wait implementation. Therefore its228-group/247-leaf PASS is guarded evidence for the implemented paths, not proof of this missing boundary or full D263 correctness under ownership loss.

MAIN explicitly instructed: do not amend sources or rerun after invocation; complete/preserve the current T175 packet and disclose the same wait boundary. Following that instruction, the candidate final2/handoff will remain PENDING_MAIN_REVIEW with this limitation. No source repair, waiver, acceptance or actual effects are inferred. A subsequent explicit MAIN lease is needed for strict original-reap implementation/meaningful fake boundary coverage if MAIN confirms the disposition.
