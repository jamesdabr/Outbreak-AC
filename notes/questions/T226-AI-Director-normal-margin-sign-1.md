# T226 — Exact normal-margin sign/measurement bridge

- Worker: AI-Director /01a1b92c-689a-71c1-820b-f1062dd0a82b.
- Ticket: T2261.0/D379,NOTES ONLY;CAMERA_FOUNDATION1.1.
- Clause: exact normal-margin<31 versus original-boom projected>=31,
  corrected T182 blocker variant7/full certificate requirement.
- Status: OPEN for MAIN qualification/source-side disposition;
  all source read-only to AI. No source fix or past-receipt amendment.

## Exact observation

The32 fixed D379 poses have the complete paper geometry/witness/body proof
in notes/proposals/T226-camera-XY-normal-margin-proof-1.md.
Positive outward-normal setback is

    B=(N/S) dot(Camera-(Eye+D*t))=19,21,24,26.

Physical358 clearance is B+2=21,23,26,28;all are<31.
Exact original-boom projected margin is>32. No invalid seed was found.

Read-only tests/outbreak/camera/release-1/oracle.py normal_margin_certificate
instead sets u=eye-bound,v=delta,w=eye-camera and adds

    w*u/360 + v*(w+u)*t/360 + v*v*t*t/360 -31
      = (w+v*t)*(u+v*t)/360 -31
      = (N/S) dot((Eye+D*t)-Camera)-31.

For a plane it similarly adds sign*(eye-camera+delta*t).
This has the OPPOSITE sign to positive outward-normal retreat.
No evaluator/helper/oracle or calculator was executed to observe it;
this is direct source algebra.

Concrete proposed row568:
EyeX14257,bound16384,CameraX16005,Dx3534,t1/2,outwardN=-X.
u=-2127,v=3534,w=-1748;u+v*t=-360,w+v*t=19.
Raw normal product=-19,minus31 residual=-50,whereas positive setback=+19.
Other a values give raw-B=-21/-24/-26 and residual-52/-55/-57.
The raw Boolean would be true for these inputs,but it is not independently
the positive-retreat certificate. Family validity below31 under both positive
meanings does not settle this semantic/source-expression difference.

## Requested MAIN disposition and bounded options

Record the intended normal measure explicitly:
- positive expanded-contact normal setback N dot(Camera-C*)/S;
- physical358 clearance from the original obstacle (B+2 for these faces);
- or an expressly named signed quantity,without calling it positive retreat.

If the intended certificate is positive setback,review the exact source sign
and scope any correction separately under a named source lease;T226 may not
edit oracle.py,verify.py,production or existing evidence. Alternatively MAIN
may adopt this mathematical family with explicit independent positive-B checks
and separately address the raw helper's naming/meaning. These are options,
not a worker choice or waiver. Do not silently use raw-B<31 as proof B<31.

The paper proof supplies BOTH positive B and B+2,exact projection,complete
own first/priority/witness/body/rounding/full F4 geometry. No extra query,
fixture decode,root stream,search or numerical assistance is needed for it.
Other old cases/inventory source-predicate conclusions require their own
qualified review if this observation affects them;this note neither rewrites
old receipts nor changes any count or acceptance status.

## Work boundary

No source,authority,old-note,evidence or output-root edits. No parser/import/
calculator/helper/evaluator/oracle/query/search/generator/test/compiler/probe/
FFI/runtime/process/network/Git effect. Complete notes/handoff are submitted
with this explicit bridge question;thenSTOP for independent review/MAIN.
No automatic source correction or next operation follows.
