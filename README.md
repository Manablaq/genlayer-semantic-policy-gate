# Semantic Policy Gate

Semantic Policy Gate is a reusable GenLayer intelligent-contract primitive for resolving policy decisions against authoritative, hash-pinned evidence. The hardened v2 contract binds every decision to the exact policy version, policy owner, subject, submitted content, context, evidence records, freshness rules, corroboration requirement, and decision lifetime.

## Security model

- **Specification-bound decisions:** a canonical SHA-256 fingerprint commits to every security-relevant input.
- **Immutable evidence records:** each source is registered with an HTTPS URI, named authority, full-content SHA-256, version label, observation time, and maximum evidence age.
- **Explicit corroboration:** callers choose one or two sources; two-source requests require distinct URIs and independently named authorities.
- **Fail-closed integrity:** fetch failures, oversized responses, hash mismatches, insufficient verified sources, expired requests, and stale evidence cannot create a decision.
- **Revocation-aware consumption:** policy updates and activation changes increment the policy version and invalidate previously issued authorization decisions.
- **Consumer-bound authorization:** consumers must supply the expected fingerprint, expected policy owner, and their own maximum decision age. A caller cannot substitute an unrelated permissive decision.
- **Exact consensus output:** validators agree on a strict canonical result containing only the decision and integrity metadata. Confidence scores are deliberately excluded from authorization.

## Decision lifecycle

1. Register a policy.
2. Compute the expected fingerprint from the exact policy and evidence specification.
3. Submit a decision request with one or two hash-pinned authoritative sources.
4. Resolve through GenLayer equivalence consensus.
5. Consume with `is_allowed_for`, `is_denied_for`, or `needs_review_for` using the expected fingerprint and policy owner.

Decision codes are `0 unknown`, `1 allowed`, `2 denied`, `3 needs_review`, and `4 error`.

## Repository layout

- `contracts/semantic_policy_gate.py` — canonical contract source.
- `studio_bradbury/semantic_policy_gate.py` — byte-identical Studio source.
- `examples/consumer_contract.py` — safe downstream consumer pattern.
- `examples/genlayer-js-usage.ts` — request and verification example.
- `tests/test_consensus_design.py` — behavioral security regressions.
- `API_MANIFEST.md` — complete public API.
- `STUDIO_BRADBURY_TEST_PLAN.md` — reproducible live test procedure.

## Verification

```bash
PYTHONPYCACHEPREFIX=/private/tmp/semantic-policy-gate-pycache \
  python3 -m py_compile contracts/semantic_policy_gate.py \
  studio_bradbury/semantic_policy_gate.py examples/consumer_contract.py

PYTHONPYCACHEPREFIX=/private/tmp/semantic-policy-gate-pycache \
  python3 -m unittest discover -s tests -p 'test_*.py'

cmp contracts/semantic_policy_gate.py studio_bradbury/semantic_policy_gate.py
git diff --check
```

The suite currently contains 19 regressions covering fingerprint collisions, suffix mutations, policy revocation, evidence integrity, corroboration, expiry, missing IDs, and consumer substitution.

## Deployment status

Hardened v2 is deployed on Bradbury at [`0xD16a0c53cE55734499554b9ef5919dc98B9Af6f0`](https://explorer-bradbury.genlayer.com/address/0xD16a0c53cE55734499554b9ef5919dc98B9Af6f0). The Explorer source matches the canonical repository contract byte-for-byte, and live positive and fail-closed security regressions are recorded in `TEST_LOG_BRADBURY.md`. The original deployment remains historical and must not be submitted as v2 evidence.

## License

MIT
