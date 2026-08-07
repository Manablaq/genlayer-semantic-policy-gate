# Architecture

## Flow

```text
Policy owner
  |
  | register_policy
  v
Versioned policy stored
  |
  | submit_decision
  v
Decision request stored
  |
  | resolver profile
  v
GenLayer consensus and deterministic storage
  |
  | verifier methods
  v
Consumer contract or frontend
```

## Storage

The contract stores three primary records:

- `Policy`
- `DecisionRequest`
- `Decision`

Policies are versioned. Decision requests preserve the policy version used at submission time. Decisions store compact, integration-ready outputs.

## Resolver Strategy

The contract supports multiple resolver profiles:

- deterministic resolver for structured evidence completeness
- semantic resolver for language-heavy policy decisions

This keeps the registry reusable while allowing domain-specific logic to be added over time.

## Consumer Surface

The most important integration methods are:

```python
is_allowed(decision_id, min_confidence)
is_denied(decision_id, min_confidence)
needs_review(decision_id)
is_fresh(decision_id)
```

These methods turn policy compliance into a clean on-chain primitive.
