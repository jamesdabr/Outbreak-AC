# T232 canonical interpreter preload includes nonstdlib startup module

- Author/worker: World & Match Systems /01a1b92c-db5c-7a10-a0e4-46e1f5a092cf.
- Ticket/revision: T2321.0.
- Governing: D391 / G2_FOUNDATION1.7 / T1872.2; adopted T229 design sections1–8.
- Exact affected clauses: D391's inspected stdlib preload/closed literal input graph and narrow metadata-only allowance; T229 section3 step2 and section4 bootstrap/input scope. D391 directs posting an exact question and stopping affected work if an input/guard/ABI seam needs broader work.
- Status: OPEN. Only MAIN/owner may resolve scope; this note changes no authority or source.

## Question

How should the exact future caller qualify the canonical interpreter's already-loaded `_distutils_hack` module, given the approved inspected-stdlib-only preload and fixed Python-I-B/seven-key launch? The observed module is outside the stdlib closure, under global site-packages. I will not silently classify it as stdlib, ignore its executable input, broaden the host/profile discovery, alter installed Python, add a launch flag/environment key, or import/read an unapproved third-party startup closure as caller authority.

## Exact read-only metadata evidence

Under D391's explicit narrow stdlib metadata DATA allowance, wrote and inspected the entire own metadata-only collection source BEFORE using it:

notes/proposals/T232-stdlib-metadata-collection-1.py

SHA25663c78092e49e523d20036778a9bae637e1636d65207b0bd1bb46e1c682741caf.

The source explicitly imports only time,builtins,fractions,hashlib,io,json,math,os,pathlib,stat,struct,sys. It never imports/compiles/evaluates project source or runs a project helper/controller. It inspects loaded module file/cache metadata only under the named canonical Python stdlib prefix; site-packages or outside-prefix modules are classified unexpected before their contents are read. Ordinary accepted stdlib inputs use bounded64KiB nofollow streaming hashes/path-descriptor joins. Its only prospective NEW write is the bounded own stdlib metadata JSON, acquired exclusively only if there are no unexpected modules.

One metadata-only command (NOT the future caller/preparation) was:

```text
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -B /Users/jd1/code/apps/outbreak/notes/proposals/T232-stdlib-metadata-collection-1.py
```

Tool return chunk8a60ae, exit1, no running session. Exact emitted DATA:

```json
{"entries": [{"module": "_distutils_hack", "path": "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/_distutils_hack/__init__.py"}], "status": "UNEXPECTED_NON_STDLIB_STARTUP_METADATA"}
```

This is presence after the explicit stdlib preload in that metadata invocation. It does NOT establish which startup file imported the module, its injection origin, its contents, or exact seven-key env-i launch behavior. That command did not adopt the future fixed-seven launch profile, and no additional profile observer/launcher experiment was run to infer equivalence. No runtime UID/environment normalization or host/profile enumeration occurred.

The metadata collector returns before output acquisition on this branch. Ordinary ls confirms both notes/proposals/T232-stdlib-preload-inventory-1.json and notes/proposals/T232-R-preparation5-caller-1.py remain absent. No project import/compile/prepare/control/oracle/compiler/FFI/SDKcopy/query/target/job ran. No P5/A3/Q output root was written, no old evidence was modified, and no preparation/actual lease was consumed. The failure is in permitted construction-time metadata qualification, not a failed R preparation or a new source result.

Independent unaffected protection check completed: ordinary shasum of all13 current source roles compared with unchanged notes/proposals/T230-current13-source-pins-1.md; standard diff exit0. Production remains9915b2338fe75214292181c6daf4367ae83f18ff2f7a21be5deab618a4cd2140, Rverify456ee77124b887951a9ec5847a33bee5ab5cf0cc7296690366b0be8b8a118dba, all other source roles unchanged. This is a source pin readback, not new operation/preflight/through-interval acceptance.

## Options for MAIN/owner

1. Explicitly release a finite qualification of the exact canonical startup extension and its literal supporting startup files, then decide whether to admit a closed hashed nonstdlib bootstrap closure in the future caller. This needs exact named inputs, content/alias/metadata/effect review and a source-scope amendment; it is not authority to scan all site-packages or import third-party code deliberately now.
2. Explicitly select a different fixed launch/bootstrap profile that excludes the nonstdlib startup path, with amended flags/ENV/runtime inputs and complete separate review. No extra flag such as -S, new environment assignment, reexec or installation change will be selected by World without that release.
3. Keep the current stdlib-only/fixed launch rules and require a strict caller refusal for any such unexpected module. Then resolve whether the requested complete caller/finite inventory can be received as a fail-closed source whose installed launch qualification remains blocked; do not dispatch a known unqualified profile as successful preparation.

A recommendation is not authorization. Preferred next step is a narrowly named read-only startup-input qualification under MAIN authority so the final source can bind facts rather than omit or guess them. Existing D386 ENV selection alone does not supply a nonstdlib-code permission.

## Work paused and independent work

Pause the affected stdlib/bootstrap input roster, closure pins/reservations, preexec policy qualification and final T232 executable caller/full sealed packet. No placeholder hash or unbound project exec source is published as ready. Standard source-only review of the already named protection/clock/effect design and ordinary frozen-role hashes can continue independently; it cannot settle this executable bootstrap input gap. I have preserved the inspected collection source and its original bounded return rather than retrying, broadening discovery or silently weakening the gate.

MAIN's separate future preflight/dispatch/original external timer/capture/terminal/late-resource gates remain. This question neither reopens any previous source lease nor grants a preparation/runtime/tool probe. World stops affected construction pending the exact scope disposition.
