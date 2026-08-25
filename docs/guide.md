# Integration Guide

## Policy publishers

Register precise policy text, retain the returned policy ID, and publish the owner address and policy digest that consumers should trust. Any update creates a new version and invalidates earlier decisions for authorization.

## Decision requesters

Choose authoritative HTTPS sources whose complete response bodies can be stably SHA-256 pinned. Record a clear evidence version and observation timestamp. Use two independently named authorities where the decision warrants corroboration. Compute the expected fingerprint before submission and retain it alongside the business action.

## Resolvers

Resolve within 24 hours while the evidence remains fresh and the policy snapshot is current. A failed resolution does not create a decision; correct the evidence record and submit a new request rather than weakening integrity rules.

## Consumers

Never accept a decision ID alone. Store the expected fingerprint and expected policy owner in trusted application or contract state, choose a consumer-specific maximum age, and call `is_allowed_for`, `is_denied_for`, or `needs_review_for`. See `examples/consumer_contract.py`.

## Operational guidance

- Prefer immutable documents or explicit document versions.
- Hash the exact bytes returned by the registered URI.
- Avoid mutable landing pages when a versioned record is available.
- Treat `needs_review` and `error` as non-authorization outcomes.
- Recompute and compare fingerprints before submitting transactions.
- Monitor policy version and active status before presenting decisions to users.
