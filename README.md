# Semantic Policy Gate

`SemanticPolicyGate` is a reusable GenLayer **Intelligent Contract** primitive for registering natural-language policies and resolving whether submitted actions, content, agent outputs, or project submissions comply with those policies.

It is designed as infrastructure for builders who need a shared on-chain decision about policy compliance.

```text
policy + subject + content + context -> allowed / denied / needs_review
```

## Why This Exists

Many GenLayer applications need policy decisions:

- Does a bounty submission satisfy the requirements?
- Does a DAO proposal follow governance rules?
- Does an agent output meet task acceptance criteria?
- Does a marketplace listing comply with listing policy?
- Does a grant application include enough required evidence?

Without a reusable primitive, every app must rebuild policy registration, request tracking, semantic evaluation, result storage, expiry, caching, and verifier methods.

## Core Contract

```text
contracts/semantic_policy_gate.py
```

Active Bradbury deployment:

```text
0xc088550EAE168Ccf2027d530Afc495Bb14767CC9
```

Studio paste-ready copy:

```text
studio_bradbury/semantic_policy_gate.py
```

## Public API

```python
register_policy(name, policy_text) -> u256
update_policy(policy_id, name, policy_text) -> None
set_policy_active(policy_id, active) -> None
submit_decision(policy_id, subject, content_uri, content_text, context, ttl_seconds) -> u256
resolve_required_fields_decision(decision_id) -> None
resolve_semantic_decision(decision_id) -> None
get_policy(policy_id) -> Policy
get_decision(decision_id) -> Decision
get_latest_decision_by_fingerprint(...) -> u256
is_allowed(decision_id, min_confidence) -> bool
is_denied(decision_id, min_confidence) -> bool
needs_review(decision_id) -> bool
is_fresh(decision_id) -> bool
```

## Decision Codes

```text
0 = unknown
1 = allowed
2 = denied
3 = needs_review
4 = error
```

## Resolver Profiles

### Required Fields Resolver

```python
resolve_required_fields_decision(decision_id)
```

Deterministic resolver profile for Bradbury smoke tests and structured submission checks. It verifies that a submission includes:

- repository evidence
- documentation evidence
- contract address
- test evidence

### Semantic Resolver

```python
resolve_semantic_decision(decision_id)
```

Generic policy resolver for natural-language decisions. It evaluates submitted text and optional fetched content against the registered policy using GenLayer's AI-validator consensus model.

## Bradbury Smoke Test Target

Positive test policy:

```text
A valid GenLayer contract submission must include a repository URL, documentation URL, Bradbury contract address, and test evidence.
```

Positive submission:

```text
Repository: https://github.com/Manablaq/genlayer-outcome-attestation-registry
Documentation: https://manablaq.github.io/genlayer-outcome-attestation-registry/
Contract: 0xd660ef089b4798e9c47B94CDDDE0EcEe5Fd29F63
Test Evidence: https://github.com/Manablaq/genlayer-outcome-attestation-registry/blob/main/TEST_LOG_BRADBURY.md
```

Expected:

```text
decision: 1
confidence: 9500
reason_code: required_fields_present
is_allowed(decision_id, 7000): true
```

## Repository Layout

```text
contracts/
  semantic_policy_gate.py

studio_bradbury/
  semantic_policy_gate.py

examples/
  consumer_contract.py
  genlayer-js-usage.ts

docs/
  guide.md
  architecture.md
  testing.md
  submission.md

API_MANIFEST.md
DEPLOYMENT_BRADBURY.md
STUDIO_BRADBURY_TEST_PLAN.md
SUBMISSION_BRIEF.md
TEST_LOG_BRADBURY.md
```

## Submission Positioning

This is not a one-off policy checker. It is a reusable policy-decision layer for GenLayer applications that need trustless adjudication over natural-language rules and submitted evidence.
