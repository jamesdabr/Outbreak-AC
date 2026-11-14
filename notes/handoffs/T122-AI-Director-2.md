# T122 terminal supplement — known installed-role dependency edge

MAIN provisional review identified a P2 role-boundary defect after the T122
freeze. This supplement qualifies T122-AI-Director-1.md; it does not alter or
retroactively repair its frozen preparation/test results.

Confirmed by read-only source inspection: in frozen v3 admission.py:243–249,
`current_record` selects the installed-tool reader globally once that path's
native role has been armed. `native_dependencies` at lines 603–618 uses
`self.record(physical)` at line616 without an independent strict dependency-role
ordinary/single-link check. Thus an already declared multiple-link
/usr/bin/clang could be admitted as a compiler dependency/header, although D132
allows link multiplicity only for its named installed launcher role. A matching
path/input SHA is insufficient to extend that exception to dependency use.

This is a concrete static role edge, not an executed regression, actual D128
failure, observed D121 dependency, unchanged-external-digest bypass or runtime
proof. MAIN reports the frozen actual D121 dependency lists contain none of
these launcher paths. The existing29 fixture tests passed but do not cover
armed launcher role followed by dependency/header use; the previous handoff's
general strict dependency-role claim is therefore incomplete for this edge.

Per MAIN instruction, frozen v3 source/schema/tests/data/evidence and the first
handoff are preserved. Read-only rehashes still match:

- admission.py:
  `452e54274561d31b3128afe2dd659a57df909647d7ae5f5825b8fb23041c2658`.
- preparation freeze:
  `1b975108fc2d2d127ec5131e47d3b61054aa4c147d230cf5a6d962d28afef293`.
- T122-AI-Director-1.md:
  `8cc13e39536e383b04e3f1f6851ae42869f690938047925bfd945daa51e4fcb4`.

Required follow-up for MAIN's separate correction lease/new package: keep
dependency/header consumption strictly single-link even after launcher roles
are armed, with an explicit armed-role-then-dependency negative and retained
legitimate installed-role positives. No patch, new package, test rerun, actual
admission, caller/controller edit, dispatch or runtime grant was performed in
this terminal supplement. MAIN owns the correction lease and review-before-
freeze sequence; Player/QA holds and earlier immutable evidence remain.
