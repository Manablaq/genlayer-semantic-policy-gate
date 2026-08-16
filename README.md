# Semantic Policy Gate

`SemanticPolicyGate` is a reusable GenLayer Intelligent Contract primitive for registering natural-language policies and producing consensus-bound `allowed`, `denied`, or `needs_review` decisions.

```text
policy snapshot + submitted evidence -> independently reviewed consensus decision
```

## Security Model

The consequential result is not accepted merely because it has the right JSON shape. When `resolve_semantic_decision` runs, every validator independently fetches the request's registered evidence, reapplies the immutable policy snapshot captured at submission, and independently derives a canonical result. `strict_eq` requires those full canonical results to match before storage changes.

The contract stores the exact resulting decision, canonical confidence, reason code, summary, and evidence digest with `consensus_bound = true`. `is_allowed` and `is_denied` return `true` only for a fresh, consensus-bound result with the requested canonical outcome and confidence threshold.

## Core API

```python
register_policy(name, policy_text) -> u256
update_policy(policy_id, name, policy_text) -> None
set_policy_active(policy_id, active) -> None
submit_decision(policy_id, subject, content_uri, content_text, context, ttl_seconds) -> u256
resolve_semantic_decision(decision_id) -> None
get_policy(policy_id) -> Policy
get_decision(decision_id) -> Decision
get_latest_decision_by_fingerprint(...) -> u256
is_allowed(decision_id, min_confidence) -> bool
is_denied(decision_id, min_confidence) -> bool
needs_review(decision_id) -> bool
is_fresh(decision_id) -> bool
```

There is deliberately no source-free required-fields resolver. Every authorization-relevant decision follows the same independently reviewed evidence path.

## Canonical Decisions

```text
allowed       confidence 9500
denied        confidence 9500
needs_review  confidence 6000
error         confidence 0
```

Confidence is derived from the agreed decision, rather than trusted from the model response. This prevents a validator-compatible response from changing downstream authorization by varying decision metadata.

## Deployment Status

The prior Bradbury deployment at `0xc088550EAE168Ccf2027d530Afc495Bb14767CC9` is historical and must not be used for this corrected version. Deploy a fresh instance from the byte-identical source in `studio_bradbury/semantic_policy_gate.py`, record its accepted transaction, and update the deployment log before resubmission.

## Repository Layout

```text
contracts/semantic_policy_gate.py        Primary source
studio_bradbury/semantic_policy_gate.py  Paste-ready, byte-identical Studio source
tests/test_consensus_design.py            Static regression checks for the consensus boundary
docs/                                    Guide, architecture, testing, and submission material
```

## Reuse

The verifier surface lets bounty platforms, DAOs, agent workflows, listing systems, grants, and escrow contracts consume a compact, auditable policy decision without parsing prose or trusting an off-chain reviewer.
