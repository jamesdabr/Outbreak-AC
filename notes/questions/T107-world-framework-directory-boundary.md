# T107 nested framework directory boundary

- Author / worker: World/Match-Systems
- Ticket and revision: T1071.0 / D111
- Phase and contract revision: native0.4; GOVERNANCE/BROWSER_FOUNDATION/P0 0.5
- Exact clause affected: Inventory fixed usr/lib/**/*.tbd, followlinks=false; no framework forest scan; reject directory alias cases; do not silently omit refused entries.
- Status: OPEN (lead resolution recorded separately)

## Question

Should nested `.framework` directory entries within fixed SDK/usr/lib be explicitly excluded and recorded without descent, or should directory symlinks encountered while walking ordinary nested directories merely be recorded as refused traversal entries while continuing the .tbd leaf inventory? T107 forbids framework scans but its glob could otherwise descend into a nested framework.

## Evidence and impact

Own stdlib sorted os.walk(followlinks=False) stopped on the first directory alias at fixed SDK/usr/lib/swift/playgrounds/LiveExecutionResultsRuntime.framework/Headers. No alias was followed. No .tbd body within that framework was read; no final reports were created. The assertion was `directory alias/special refused`. SDK, source, pins and existing evidence remain unchanged. Only directory metadata enumeration within the selected root had occurred; no process/tool/project execution.

## Options for owner and lead

1. Explicitly prune all nested .framework roots without descent, recording each exclusion; retain refusal for any directory alias outside those roots. Recommended if expected513/399 pertains to nonframework stubs.
2. Record all directory aliases as nontraversed/refused entries and continue ordinary paths, clarifying whether nested framework ordinary directories are allowed. No aliases become consumed inputs.

## Work paused

Final SDK inventory and both new T107 reports await the exact traversal interpretation. Source/contract/pins remain read-only. Mandatory document/source provenance reads are complete; no further independent implementation is required.
