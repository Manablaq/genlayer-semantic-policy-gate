# Submission Brief

## Semantic Policy Gate

A reusable GenLayer Intelligent Contract primitive that turns an immutable natural-language policy and public evidence into a consensus-bound authorization decision.

## What Makes It Safe to Compose

For every resolution, validators independently fetch the registered evidence and reapply the policy snapshot captured with the request. `strict_eq` binds the complete canonical result: decision, derived confidence, reason code, summary, and evidence digest. Storage is updated only after that agreement. Consumer methods `is_allowed` and `is_denied` require a fresh, consensus-bound decision, so a schema-valid but contradictory model response cannot authorize an action.

## Reuse

Builders can use it for bounty acceptance, DAO proposal gates, marketplace rules, grant review, agent output checks, moderation, and escrow conditions. Policies are versioned; requests preserve the exact policy text and digest used for evaluation; fingerprints reuse fresh equivalent work.

## Deployment Evidence

Corrected contract: `0xE8f0091c7b95d8D15813aAdFF593c4Df4E7c8fea`.

Accepted deployment transaction:
`0x22ebced9109c006611152b4fbf3f944d6cf424ac921aa2409ab50d5d0e97b43f`.

The deployed source is commit `27911d9875debd18603952ea0b8431ee8e1629bd` and
matches `studio_bradbury/semantic_policy_gate.py`. The prior deployment is
historical only.

The corrected deployment has both Bradbury consensus paths documented in
`TEST_LOG_BRADBURY.md`:

- allowed: `decision_id 1`, exact confidence `9500`, `consensus_bound: true`,
  `is_allowed(1, 9500) = true`, and `is_denied(1, 9500) = false`;
- denied: `decision_id 2`, exact confidence `9500`,
  `is_denied(2, 9500) = true`, and `is_allowed(2, 9500) = false`.

The two resolutions independently fetched the IANA Example Domains page and
reapplied the policy snapshot, proving that contradictory outcomes cannot pass
the same downstream authorization check.
