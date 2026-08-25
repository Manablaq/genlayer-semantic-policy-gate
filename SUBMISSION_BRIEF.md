# Submission Brief

## Semantic Policy Gate v2

Semantic Policy Gate is a reusable GenLayer primitive for converting semantic policy evaluation into a deterministic, safely consumable on-chain decision.

The hardened v2 implementation closes the substitution and evidence-integrity risks present in the historical deployment:

- Decisions now use collision-resistant SHA-256 fingerprints over the policy owner/version/digest, exact subject, full content/context hashes, every evidence URI/hash/authority, evidence version, freshness limits, source threshold, and TTL.
- Evidence must be authoritative, HTTPS, full-content hash-pinned, explicitly versioned, and fresh. Optional two-source corroboration requires independent authorities.
- Fetch errors, oversized content, hash mismatch, stale evidence, expired requests, policy changes, and insufficient verified sources fail closed.
- Authorization no longer relies on confidence. Consumers must provide their expected fingerprint, policy owner, and maximum decision age.
- Policy updates or deactivation immediately revoke prior authorization decisions.
- Missing IDs return controlled errors or false instead of runtime attribute failures.
- The consumer example stores trusted fingerprints internally so callers cannot substitute unrelated allowed decisions.

Local validation includes GenVM lint/validation, byte-identical canonical and Studio sources, Python compilation, and 19 behavioral security regressions.

The historical Bradbury address is not the v2 submission. A fresh matching deployment and the live regressions in `STUDIO_BRADBURY_TEST_PLAN.md` are required before resubmission.
