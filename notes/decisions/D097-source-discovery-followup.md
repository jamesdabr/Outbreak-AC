# D097 — Reconcile the concrete source audit before clean builds

MAIN reviewed T096's source-path proposal and verified two concrete browser discovery defects against source: candidate_recipe.repository_inputs recursively includes two unconsumed T063 historical .h witnesses under web/transport/results, and omits source/src/ge25519_base.data which crypto_tools.h actually includes. T096 correctly keeps the .data and excludes history. Shared source manifest must not be padded with historical witnesses to satisfy an accidental glob.

T0975.23 RELEASED Engine, priority before continuing T002 notes: narrowly fix only candidate_recipe.py repository_inputs discovery (production transport header root only; explicit ge25519_base.data). New focused tests/evidence under tests/candidate/T097. Public schemas/flags/commands/preservation/actual .d/authority/verifier behavior unchanged. Preserve original T088 source snapshot/receipts and don't rewrite its freeze. T088 accepted prep remains historical; corrected successor source needs new receipt/hash review before actual execution.

Source audit proposal is useful but not a final source/hash approval; T095 and corrected tooling path/content still need freeze. All other production sources remain unchanged. No actual compiler/build/runtime/Git mutation or source-manifest authority delegated by this follow-up.
