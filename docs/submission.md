# Submission Checklist

- [x] Canonical v2 contract implemented.
- [x] Studio source is byte-identical.
- [x] Collision-resistant full fingerprints replace truncated text digests.
- [x] Evidence is HTTPS, full-hash pinned, versioned, fresh, and optionally corroborated.
- [x] Resolution fails closed on integrity or availability errors.
- [x] Consumer authorization binds expected fingerprint and policy owner.
- [x] Policy changes revoke prior authorization.
- [x] Confidence is removed from authorization.
- [x] Missing records are controlled.
- [x] Nineteen local regressions pass.
- [x] GenVM lint and validation pass.
- [x] Implementation commit and source SHA recorded.
- [x] Fresh hardened v2 contract deployed to Bradbury.
- [x] Explorer source confirmed to match the repository byte-for-byte.
- [x] Live exact-fingerprint and altered-fingerprint checks recorded.
- [x] Live bad-hash, stale-evidence, and missing-ID checks recorded.
- [x] Policy revocation covered by a passing local regression without invalidating the live review fixture.
- [x] Deployment address, transaction, and all evidence links added to the test log.

Do not resubmit the historical deployment. Use only the hardened v2 contract and evidence links recorded in `DEPLOYMENT_BRADBURY.md` and `TEST_LOG_BRADBURY.md`.
