# Bradbury Testing Guide

Follow `STUDIO_BRADBURY_TEST_PLAN.md` for the exact Studio inputs.

## Expected Positive Flow

```text
register_policy -> policy_id 1
submit_decision -> decision_id 1
resolve_required_fields_decision(1)
get_decision(1)
is_allowed(1, 7000) -> true
```

## Expected Decision

```text
decision: 1
confidence: 9500
reason_code: required_fields_present
summary: The submission includes repository, documentation, contract address, and test evidence.
```

## Why This Test Is Stable

The first smoke test uses deterministic field detection instead of an LLM. This is deliberate. It proves the registry, storage, verifier methods, and fingerprint reuse before testing open-ended semantic decisions.
