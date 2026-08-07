# API Manifest

## Contract

`SemanticPolicyGate`

## Constructor

```python
__init__()
```

No arguments.

## Write Methods

### register_policy

```python
register_policy(name: str, policy_text: str) -> u256
```

Creates a versioned policy.

### update_policy

```python
update_policy(policy_id: u256, name: str, policy_text: str) -> None
```

Updates a policy and increments its version. Only the policy owner can update.

### set_policy_active

```python
set_policy_active(policy_id: u256, active: bool) -> None
```

Activates or deactivates a policy. Only the policy owner can update.

### submit_decision

```python
submit_decision(
    policy_id: u256,
    subject: str,
    content_uri: str,
    content_text: str,
    context: str,
    ttl_seconds: u256,
) -> u256
```

Creates a decision request or returns an existing fresh request/decision for the same policy version and canonical content fingerprint.

### resolve_required_fields_decision

```python
resolve_required_fields_decision(decision_id: u256) -> None
```

Deterministic resolver profile for evidence-completeness checks.

### resolve_semantic_decision

```python
resolve_semantic_decision(decision_id: u256) -> None
```

Generic semantic resolver for policy compliance decisions.

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
created_at: u256
resolved_at: u256
expires_at: u256
resolver: Address
```
