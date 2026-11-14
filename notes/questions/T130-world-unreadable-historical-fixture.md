# T130 unreadable historical ordinary fixture stops full hash proof

- Author / worker: World/Match-Systems
- Ticket / revision: T1301.0 / D143; smoke0.6/D142
- Exact clause: complete fixed preservation forests; stream-hash ordinary files; any replacement/read failure stops affected proof, no repair/retry/exclusion.
- Status: OPEN (MAIN resolution recorded separately)

## Question

How should MAIN obtain the required content identity for the preserved historical mode0000 ordinary fixture below without mutating historical evidence? Current fixed-interpreter read authority cannot open it. D142 only adds seven specific FIFO metadata roles; it does not permit omitting/hash-exempting unreadable ordinary files. No policy relaxation or privileged read is inferred here.

## Concrete evidence

The ONE guarded complete-forest pass stopped after15.47881820902694seconds with PermissionError/Errno13 on:

`/Users/jd1/code/apps/outbreak/web/repro/tests/prerequisites/FIXTURE_ONLY-a6a8xiso/repo/web/build/.cache/bad-mode`

Metadata-only diagnosis (no content retry): canonical ordinary file,mode0000,nlink1,12bytes,device16777232,inode138018950,uid501/gid20. Its local ancestors are ordinary0755, fixture root0700. os.open used read-only/no-follow/nonblocking after regular lstat; permission denial occurred before body/hash. No file permission/ownership/content altered. This is historical fixture accessibility, not a browser/native build failure or special-file case.

Partial completed records:83082files/20912directories/7456opaque links/two allowed FIFO records;5548518691ordinary bytes hashed. No complete serialization/digest/complexity/headroom/full timing produced. All seven literal FIFO rows separately lstat-checked against MAIN reference and match; none opened/read/hashed.

## Options for MAIN

1. Supply a separately reviewed/read-authorized way to obtain ordinary content identities while preserving original evidence metadata/content, followed by a NEW explicitly released full pass.
2. Record a deliberate preservation-policy decision if treating inaccessible historical ordinary data differently is intended. This is outside D142's exact FIFO scope and cannot be an implicit worker exclusion or fake hash.

## Work stopped

No hash retry, escalation, chmod/chown/copy/delete, baseline/pins generation, source or special-role amendment. T130's one pass is terminal FAILED_CHARACTERIZATION_STOP_NO_RETRY; full representability/timing proof awaits MAIN resolution/new release. No claims about other unvisited unreadable files. T125/T128 evidence and human holds preserved. Details in notes/reviews/T130-world-full-forest-preflight.md.
