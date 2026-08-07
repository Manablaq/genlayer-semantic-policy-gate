# Semantic Policy Gate Guide

## Overview

`SemanticPolicyGate` is a reusable GenLayer Intelligent Contract for policy compliance decisions.

It answers:

```text
Does this submitted content or action comply with this registered policy?
```

The contract stores versioned policies, decision requests, structured decisions, confidence scores, expiry, and reusable fingerprints.

## Key Concepts

### Policy

A natural-language rule owned by an address.

Example:

```text
A valid GenLayer contract submission must include a repository URL, documentation URL, Bradbury contract address, and test evidence.
```

### Decision Request

A request to evaluate a subject and content against a policy.

### Decision

A stored result:

```text
allowed / denied / needs_review / error
```

### Policy Version

Every policy update increments the version. Decisions are tied to the exact version used at evaluation time.

### Fingerprint

The contract canonicalizes policy id, policy version, subject, content URI, content text, and context. Fresh duplicate requests return the existing decision id.

## Resolver Profiles

### Required Fields Resolver

`resolve_required_fields_decision` checks whether a submission includes repository, documentation, contract address, and test evidence.

It is deterministic and is the recommended first Bradbury smoke test.

### Semantic Resolver

`resolve_semantic_decision` evaluates submitted content and optional fetched content against the policy using GenLayer AI-validator consensus.

Use this for natural-language or ambiguous policy decisions.

## Integration

Downstream contracts should use:

```python
is_allowed(decision_id, min_confidence)
is_denied(decision_id, min_confidence)
needs_review(decision_id)
is_fresh(decision_id)
```

This lets applications depend on compact policy decisions instead of parsing prose.

## Example Use Cases

- DAO proposal policy gates
- grant eligibility checks
- bounty submission review
- marketplace listing compliance
- agent task acceptance
- community moderation
- escrow release conditions
- reputation credential issuance
