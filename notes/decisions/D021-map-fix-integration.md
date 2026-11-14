# D021 Map ownership fix accepted for integration

MAIN reviewed T042 source/helper/native/whole-Wasm-object evidence, exact guarded diff and native equivalence; independently checked current source hash and both exact target object hashes/signatures. T042 ACCEPTED in this scope. worldio.cpp stable SHA2568b6d1e7aa7197be1d5030954f48662bcaab85412b222cea027762fbdb1c488c1. Real map helper demonstrates384-byte entity capacity versus65536 base-world/87808 full-mip allocation and retained original-map decode. Optional ASan helper timed out and is NOT accepted as sanitizer evidence; runner cleaned it up. No game recovery proven yet.

D017 same-Wasm symbol mapping is independently hash-verified and accepted diagnostic evidence; original D016 stack attribution is valid. Original out and failure/diagnostic evidence remain immutable snapshots.

Existing T040 is released to consume this exact MAIN-accepted source fix, rebuild changed/stale real units and link under unchanged D006/D009 SDK/ports/profile/pack. Snapshot current D016 outputs/metadata before replacement. No added flags or other source changes. Provide new artifact identity/four runtime pins for actual QA.

T042 malformed-RLE repeat observation is separately recorded: it is not part of this valid-map ownership fix, does not permit arbitrary-map downloads and must be addressed before a future untrusted-map acceptance claim. Current proof uses only exact accepted original manifest/bytes. No native client/global decoder rewrite is authorized by D021.
