# API Manifest

All IDs are `u256`, timestamps are Unix seconds, hashes are lowercase 64-character SHA-256 hex strings, and addresses are GenLayer `Address` values.

## Write methods

### `register_policy(name, policy_text) -> policy_id`

Creates an active, owner-controlled policy at version 1 and stores its canonical digest.

### `update_policy(policy_id, name, policy_text)`

Policy-owner only. Replaces the specification, increments the version, reactivates the policy, and creates a new digest. Older decisions immediately fail consumer authorization.

### `set_policy_active(policy_id, active)`

Policy-owner only. Any activation change increments the version and digest. Deactivation revokes consumption of prior decisions.

### `submit_decision(...) -> decision_id`

Parameters, in order:

```text
policy_id
subject
content_text
context
primary_evidence_uri
primary_evidence_sha256
primary_authority
corroborating_evidence_uri
corroborating_evidence_sha256
corroborating_authority
evidence_version
evidence_observed_at
max_evidence_age_seconds
minimum_sources
ttl_seconds
```

The request stores a snapshot of the current policy and a canonical fingerprint. `minimum_sources` must be 1 or 2. Corroborating fields may be empty only when one source is sufficient. A zero TTL selects the seven-day default; allowed TTLs are five minutes through 30 days. Evidence age must be 60 seconds through 30 days, and evidence must still be fresh when submitted.

### `resolve_semantic_decision(decision_id)`

Fetches and hashes the registered evidence inside the non-deterministic execution boundary, evaluates the policy, and commits a strict consensus result. The request must resolve within 24 hours, the policy snapshot must still match the active policy, and every required source must match its registered hash. The resulting expiry is capped by both decision TTL and evidence freshness.

## View methods

### `compute_fingerprint(...) -> str`

Uses the same arguments as `submit_decision` and returns the canonical expected fingerprint without changing state. A zero TTL is normalized to the default.

### `get_policy(policy_id) -> object`

Returns policy owner, name, text, version, digest, timestamps, and active state. Unknown IDs raise `unknown policy`.

### `get_request(decision_id) -> object`

Returns the immutable request snapshot and evidence rules. Unknown IDs raise `unknown request`.

### `get_decision(decision_id) -> object`

Returns the resolved decision, verified hashes, source count, fingerprint, consensus flag, and expiry. Unknown IDs raise `unknown decision`.

### `get_latest_decision_by_fingerprint(fingerprint) -> decision_id`

Returns the latest currently usable decision ID for an exact fingerprint, or `0` when none is available.

### `is_allowed_for(decision_id, expected_fingerprint, expected_policy_owner, consumer_max_age_seconds) -> bool`

Returns true only for a current, active-policy, consensus-bound, content-verified allowed decision matching every consumer expectation.

### `is_denied_for(decision_id, expected_fingerprint, expected_policy_owner, consumer_max_age_seconds) -> bool`

Applies the same binding and freshness checks for a denied decision.

### `needs_review_for(decision_id, expected_fingerprint, expected_policy_owner, consumer_max_age_seconds) -> bool`

Applies the same binding and freshness checks for a needs-review decision.

### `is_fresh_for(decision_id, expected_fingerprint, expected_policy_owner, consumer_max_age_seconds) -> bool`

Checks decision existence, fingerprint, policy owner, current policy state, contract expiry, resolution timestamp, and the consumer's stricter maximum age. It does not authorize an outcome by itself.

## Limits

Fetched evidence is capped at 12,000 bytes per source. Text, URI, authority, and version fields have explicit on-chain length limits. Source fetch errors, oversized bodies, hash mismatches, stale evidence, expired requests, policy changes, and insufficient verified sources fail closed.
