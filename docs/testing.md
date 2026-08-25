# Testing

## Local gate

```bash
PYTHONPYCACHEPREFIX=/private/tmp/semantic-policy-gate-pycache \
  python3 -m py_compile contracts/semantic_policy_gate.py \
  studio_bradbury/semantic_policy_gate.py examples/consumer_contract.py

PYTHONPYCACHEPREFIX=/private/tmp/semantic-policy-gate-pycache \
  python3 -m unittest discover -s tests -p 'test_*.py'

cmp contracts/semantic_policy_gate.py studio_bradbury/semantic_policy_gate.py
git diff --check
```

Run the configured GenVM linter/validator against `contracts/semantic_policy_gate.py` before every deployment.

## Regression coverage

The behavioral suite verifies:

- complete non-deterministic consensus containment;
- source parity;
- strict consensus and integrity validation;
- policy owner/text/version/active binding;
- delimiter and suffix collision resistance;
- fingerprint sensitivity for every security field;
- full-content hashing;
- fail-closed fetch and hash mismatch behavior;
- explicit two-source corroboration;
- policy revocation and update behavior;
- TTL, evidence-age, request, and consumer freshness bounds;
- controlled missing-ID behavior;
- removal of unsafe confidence and truncated-digest APIs.

## Live tests

Local tests cannot prove deployed source parity or live consensus behavior. Complete `STUDIO_BRADBURY_TEST_PLAN.md` on the fresh Bradbury deployment and record direct Explorer links in `TEST_LOG_BRADBURY.md`.
