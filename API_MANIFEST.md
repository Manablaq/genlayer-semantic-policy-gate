# API Manifest

## Contract

`SemanticPolicyGate`

## Write Methods

```python
register_policy(name: str, policy_text: str) -> u256
update_policy(policy_id: u256, name: str, policy_text: str) -> None
set_policy_active(policy_id: u256, active: bool) -> None
submit_decision(policy_id: u256, subject: str, content_uri: str, content_text: str, context: str, ttl_seconds: u256) -> u256
resolve_semantic_decision(decision_id: u256) -> None
```

`submit_decision` snapshots `policy_name`, `policy_text`, `policy_digest`, evidence inputs, and expiry. `resolve_semantic_decision` independently evaluates that immutable snapshot on every validator and accepts only strict equality of the full canonical result.

## View Methods

```python
get_policy(policy_id: u256) -> Policy
get_decision(decision_id: u256) -> Decision
get_latest_decision_by_fingerprint(...) -> u256
is_allowed(decision_id: u256, min_confidence: u32) -> bool
is_denied(decision_id: u256, min_confidence: u32) -> bool
needs_review(decision_id: u256) -> bool
is_fresh(decision_id: u256) -> bool
```

`is_allowed` and `is_denied` require a fresh `consensus_bound` decision. They cannot authorize from a schema-valid but unbound result.

## Decision Codes

```text
0 = unknown
1 = allowed
2 = denied
3 = needs_review
4 = error
```

## Storage Types

### Policy

```python
policy_id: u256
owner: Address
name: str
policy_text: str
version: u256
policy_digest: str
created_at: u256
active: bool
```

### DecisionRequest

```python
requester: Address
policy_id: u256
policy_version: u256
policy_name: str
policy_text: str
policy_digest: str
subject: str
content_uri: str
content_text: str
context: str
fingerprint: str
created_at: u256
expires_at: u256
resolved: bool
```

### Decision

```python
decision_id: u256
requester: Address
policy_id: u256
policy_version: u256
subject: str
content_uri: str
content_digest: str
context_digest: str
fingerprint: str
decision: u32
confidence: u32
reason_code: str
summary: str
evidence_digest: str
consensus_bound: bool
created_at: u256
resolved_at: u256
expires_at: u256
resolver: Address
```
