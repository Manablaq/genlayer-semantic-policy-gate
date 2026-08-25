# Architecture

Semantic Policy Gate separates deterministic state transitions from GenLayer's non-deterministic semantic evaluation.

## Deterministic registration

A policy owner registers a policy. The contract derives a canonical SHA-256 digest from the owner, exact name and text, version, and active state. Updates and activation changes increment the version and replace the digest.

## Immutable request snapshot

`submit_decision` snapshots the current policy and evidence specification. Its fingerprint commits to every field that can affect meaning or safe consumption, using a domain-separated canonical JSON array rather than delimiter concatenation.

## Consensus boundary

`resolve_semantic_decision` verifies request and policy freshness before entering `gl.eq_principle.strict_eq`. Inside the non-deterministic function, each source is fetched, limited to 12,000 bytes, and SHA-256 checked. Only verified evidence reaches the semantic prompt. Validators agree on strict canonical JSON with a decision, canonical reason/summary, observed hashes, verified source count, and integrity flag.

## Fail-closed commit

The deterministic commit path independently validates the consensus result. Any fetch or integrity failure raises and leaves the request unresolved. Decision expiry is capped by both the requested TTL and the remaining evidence-freshness period.

## Safe consumption

Authorization predicates bind the stored decision to an expected fingerprint and expected policy owner, then verify consensus, content integrity, current policy version/digest/active state, contract expiry, and the consumer's maximum age. The policy specification therefore remains enforceable after consensus and at every downstream use.
