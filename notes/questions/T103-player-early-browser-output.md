# T103 launch-time Chrome output byte bound

- Worker: Player; T1031.0 / BROWSER_CAPABILITY_PROBE0.1.
- Status: OPEN; MAIN resolves separately.
- Affected clause:8MiB all report/child output; inspected fixed Playwright launchServer policy, no private dependency mutation or automatic alternative method.

Installed coreBundle.js:8935–8941 attaches readline handlers to Chrome stdout/stderr during launch. BrowserServer.process() is available publicly only after launchServer resolves. Adding public stream listeners then cannot prove a byte bound for earlier output. RecentLogsCollector at7944 is a150-line collector, not an8MiB raw-byte limit; the public logger option is explicitly documented as incomplete in installed types.d.ts:17640. The source can bound post-handle output/report and report the earlier interval unavailable; it must not call that complete child-output proof.

Please freeze the approved launch-time output-collection/limit seam before an actual complete probe. No private Playwright process hook, installed source patch, new launcher/dependency or alternative flags are selected here. This affects actual full byte-bound acceptance, not the independent pure guard/cache/GPU/ownership fixtures. Preparation/actual report should remain explicitly partial while this and the child-pause question are unresolved. No browser/process was launched to investigate.
