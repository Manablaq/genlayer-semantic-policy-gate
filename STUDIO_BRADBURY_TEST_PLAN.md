# Studio Bradbury Test Plan

## Pre-deploy Integrity Check

1. In GenLayer Studio create `semantic_policy_gate.py`.
2. Paste `studio_bradbury/semantic_policy_gate.py` exactly.
3. Confirm it matches `contracts/semantic_policy_gate.py` byte-for-byte in the repository.
4. Deploy a new instance; do not upgrade or reuse the historical rejected deployment.
5. Save the address and accepted deployment transaction in `DEPLOYMENT_BRADBURY.md`.

## Smoke Test 1: Register a Policy

Call `register_policy`:

```text
name: Documentation claim policy
policy_text: Allow only when the registered evidence explicitly states that the submitted claim is true. Deny only when it explicitly states the opposite. Use needs_review when the evidence is absent, ambiguous, or does not address the claim.
```

## Smoke Test 2: Submit a Decision

Call `submit_decision` using a stable public HTTPS page as `content_uri`, a matching claim as `subject`, concise supporting `content_text`, and a nonzero TTL.

The request captures the exact policy text and digest. Changing the policy later cannot alter this request's evaluation rule.

## Smoke Test 3: Resolve With Independent Consensus

Call:

```text
resolve_semantic_decision(decision_id)
```

Expected behavior:

- Each validator independently fetches the registered URI and reapplies the stored policy.
- `strict_eq` accepts only an identical canonical decision, confidence, reason code, summary, and evidence digest.
- The resulting record has `consensus_bound: true`.

## Smoke Test 4: Verify Consumer Binding

Call `get_decision(decision_id)`, then call one of:

```text
is_allowed(decision_id, 9500)
is_denied(decision_id, 9500)
needs_review(decision_id)
```

Only the method matching the stored canonical decision can return `true`; `is_allowed` and `is_denied` also require `consensus_bound: true` and freshness.

## Regression Check

Do not look for or call `resolve_required_fields_decision`: it was removed because it could create authorization-relevant decisions without independent evidence review.
