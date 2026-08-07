# Studio Bradbury Test Plan

Use this plan to deploy and test `SemanticPolicyGate` in GenLayer Studio on Bradbury Testnet.

## Deploy

1. Open GenLayer Studio.
2. Confirm the selected network is `Genlayer Bradbury Testnet`.
3. Create a new contract file named `semantic_policy_gate.py`.
4. Paste the code from `studio_bradbury/semantic_policy_gate.py`.
5. Deploy a new instance.

The contract constructor takes no arguments.

## Smoke Test 1: Register Policy

Call:

```text
register_policy
```

Inputs:

```text
name:
GenLayer Submission Completeness Policy
```

```text
policy_text:
A valid GenLayer contract submission must include a repository URL, documentation URL, Bradbury contract address, and test evidence. Allow submissions that clearly include all four. Deny submissions that include none. Mark incomplete or ambiguous submissions as needs_review.
```

Expected:

```text
ACCEPTED / AGREE / FINISHED_WITH_RETURN
policy_id: 1
```

## Smoke Test 2: Submit Decision

Call:

```text
submit_decision
```

Inputs:

```text
policy_id:
1
```

```text
subject:
OutcomeAttestationRegistry submission
```

```text
content_uri:
https://github.com/Manablaq/genlayer-outcome-attestation-registry
```

```text
content_text:
Repository: https://github.com/Manablaq/genlayer-outcome-attestation-registry
Documentation: https://manablaq.github.io/genlayer-outcome-attestation-registry/
Contract: 0xd660ef089b4798e9c47B94CDDDE0EcEe5Fd29F63
Test Evidence: https://github.com/Manablaq/genlayer-outcome-attestation-registry/blob/main/TEST_LOG_BRADBURY.md
```

```text
context:
Submission package for a reusable GenLayer Intelligent Contract primitive.
```

```text
ttl_seconds:
604800
```

Expected:

```text
decision_id: 1
```

## Smoke Test 3: Resolve Deterministically

Call:

```text
resolve_required_fields_decision
```

Input:

```text
decision_id:
1
```

Expected:

```text
ACCEPTED / AGREE / FINISHED_WITH_RETURN
```

## Smoke Test 4: Read Decision

Call:

```text
get_decision
```

Input:

```text
decision_id:
1
```

Expected:

```text
decision: 1
confidence: 9500
reason_code: required_fields_present
summary: The submission includes repository, documentation, contract address, and test evidence.
```

## Smoke Test 5: Consumer API

Call:

```text
is_allowed
```

Inputs:

```text
decision_id:
1
min_confidence:
7000
```

Expected:

```text
true
```

## Smoke Test 6: Fingerprint Reuse

Call `submit_decision` again with the exact same inputs from Smoke Test 2.

Expected:

```text
1
```
