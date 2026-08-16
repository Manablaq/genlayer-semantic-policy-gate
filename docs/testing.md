# Bradbury Testing Guide

Run the Studio plan in `STUDIO_BRADBURY_TEST_PLAN.md` against a fresh deployment.

Required evidence for resubmission:

1. Accepted deployment transaction for the byte-identical Studio source.
2. A request showing the captured policy snapshot and public evidence URI.
3. An accepted `resolve_semantic_decision` transaction.
4. `get_decision` showing a canonical outcome, matching canonical confidence, nonempty evidence digest, and `consensus_bound: true`.
5. The matching consumer verifier result (`is_allowed` or `is_denied`) at the canonical confidence threshold.

The regression suite `tests/test_consensus_design.py` checks that the old source-free resolver and shape-only `run_nondet_unsafe` path are absent, that Studio and primary sources match, and that consumer authorization requires the consensus binding.
