# T242 ledger fault and external descriptor boundaries

- Author: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket: T2421.0/D409 NOTES ONLY; MOTION_RECORD_FOUNDATION0.7.
- Clauses: finite reserve-before-acquire ledger; unknown bounds must refuse,not become unspecified overhead or an expected96-case refusal.
- Status: POLICY RESOLVED D414 for NOTES only; exact external descriptors/formatter/source review remain OPEN. No implementation or effect authority.

## Question

The new exact ledger specification separates all finite algorithm terms from declared external graph/source/stdlib/path inputs. Two narrow policies need explicit approval in any future source release: a budget-infrastructure fault must latch independently and abort catalog rather than count as one of the83 intended REFUSE outcomes; and physical failure formatting must not call arbitrary str(exception) before its return-size bound is established.

## Evidence and impact

Current Job.run catches BaseException and wraps errors in Refusal; run_controls catches Refusal as a case refusal. An otherwise strict budget exception can therefore mask a discriminator unless finish checks an independent failure latch before the existing expected-outcome assertion. Proposed ledger has a separate CatalogBudgetFault class PLUS sticky infrastructure_failed; a failing reserve never invokes its target primitive,does not fabricate an action/event outcome,and cannot produce matchedTrue. Intentional metadata-cap/capture-cap/driver-cap fixtures keep their existing Job counters and Refusal behavior; they do not set the infrastructure latch.

Current Job.step/Job.write/Job.run/main call str(e) or encode complete action/write/error graphs. Fixture error messages are finite closed strings from FakeBoundary/scenario names and typed status fields. Physical OSError/unknown BaseException formatting has no source-level length theorem merely because a later encoded failure file has64MiB cap. The specification bounds known fixture errors and requires predeclared physical error-return descriptors; unknown exception formatting is an unqualified acquisition,not permission to truncate or replace the original96 evidence. A future caller can retain opaque raw-return/ownership truth and stop without a failure file,as the existing optional failure protocol permits,but cannot claim formatted persistence success.

Unknown installed source/stdlib/protected graph bytes,names/link lengths,declared record counts,lease bytes and physical I/O/error-return size descriptors remain external finite DATA inputs. The specification gives exact phase inequalities over them and a normalization/scanning protocol; no collector or graph is constructed here. Four roots and every required member remain mandatory. Camera T240 is live; no whole camera graph or final hash is inferred from previous T236/T237 records.

MAIN subsequently issued D414 during this unsubmitted draft: independent sticky infrastructure failure and closed known-error formatting are adopted NOTES policy; every future catch/finish must check the latch. Unknown physical formatting retains opaque error/return/ownership truth and fails without optional failure file; no evidence truncation or altered fake cap outcomes. T240 SOURCE is now received/sealed D412,which still does not supply a whole-camera graph. External descriptor/graph sizes and exact future formatter schemas remain refusing prerequisites. Earlier live-source wording above describes the question's opening context,not current whole-root authority.

## Options for MAIN

Review and separately release the proposed sticky-latch and closed-format/known-return descriptor boundaries with the private ledger. Keep unsupported physical formatting/refusal explicit until exact semantics are specified. An infrastructure refusal must fail the whole operation,never repair a missing control result. Preserve all current11source/focus pins until MAIN's separate sequencing boundary; no silent T237 rebase.

## Work paused

Notes specification is delivered independently. Source instrumentation,installed metadata collection,caller/lease construction,all96 execution and any actual ordering change remain unreleased. This is a precise remaining source-policy question,not a request for a new experiment,probe,case,child or resource allowance.
