# Submission Brief

## Semantic Policy Gate

A reusable GenLayer Intelligent Contract primitive that turns an immutable natural-language policy and public evidence into a consensus-bound authorization decision.

## What Makes It Safe to Compose

For every resolution, validators independently fetch the registered evidence and reapply the policy snapshot captured with the request. `strict_eq` binds the complete canonical result: decision, derived confidence, reason code, summary, and evidence digest. Storage is updated only after that agreement. Consumer methods `is_allowed` and `is_denied` require a fresh, consensus-bound decision, so a schema-valid but contradictory model response cannot authorize an action.

## Reuse

Builders can use it for bounty acceptance, DAO proposal gates, marketplace rules, grant review, agent output checks, moderation, and escrow conditions. Policies are versioned; requests preserve the exact policy text and digest used for evaluation; fingerprints reuse fresh equivalent work.

## Deployment Evidence

Use the new Bradbury address and accepted deployment transaction recorded after deploying the corrected matching Studio source. The prior deployment is historical only.
