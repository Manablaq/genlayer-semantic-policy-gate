# Semantic Policy Gate Guide

## Lifecycle

1. A policy owner registers a versioned natural-language policy.
2. A requester submits content and an optional public evidence URI.
3. The contract snapshots the exact policy text, policy digest, evidence inputs, and expiry.
4. Validators independently fetch the URI and apply that same snapshot.
5. Strict equality accepts one canonical result before it is written on-chain.
6. Consumers call `is_allowed`, `is_denied`, `needs_review`, or `is_fresh`.

## Independent Validation

The validator does not validate a leader's response shape. It repeats the consequential work: fetches the registered evidence and reapplies the registered policy. The accepted payload includes the outcome, canonical confidence, reason, summary, and evidence digest. Confidence is a function of the agreed outcome, not an untrusted model-supplied number.

## Consumer Safety

`is_allowed` and `is_denied` require both freshness and `consensus_bound = true`. A result that has not passed strict agreement cannot become an authorization signal.

## Policy Updates

Policy updates create a new version. Existing requests keep their original policy snapshot, preventing policy drift between request and resolution.
