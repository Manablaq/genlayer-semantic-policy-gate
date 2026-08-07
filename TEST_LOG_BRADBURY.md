# Bradbury Test Log

## Deployment

Contract:

```text
0xc088550EAE168Ccf2027d530Afc495Bb14767CC9
```

Deployment transaction:

```text
0x995779a73575b108ab01b4b00c9cf59b6a0bdc1b78d0fa795eadcdfd0988a800
```

Result:

```text
ACCEPTED / AGREE / FINISHED_WITH_RETURN
```

## Next Test

Register the first policy.

## Test 1: register_policy

Transaction:

```text
0xd9822384e3ad27b655138178724fea44a4f11b177a1dc0c47050806527987a95
```

Result:

```text
ACCEPTED / AGREE / FINISHED_WITH_RETURN
txSlot: 1
```

Policy:

```text
name: GenLayer Submission Completeness Policy
policy_id: 1
```

## Test 2: submit_decision

Transaction:

```text
0x6c0b9153ab6d0145bcebab0ebd2f804932c8841358ae0be455248d37301eb53e
```

Result:

```text
ACCEPTED / AGREE / FINISHED_WITH_RETURN
txSlot: 2
```

Decision request:

```text
decision_id: 1
subject: OutcomeAttestationRegistry submission
policy_id: 1
```

## Test 3: resolve_required_fields_decision

Transaction:

```text
0xc6d30e607af25c0a82664230bd0a4c6780ed4acbb27ca618c94fe282346fa4e4
```

Result:

```text
ACCEPTED / AGREE / FINISHED_WITH_RETURN
txSlot: 3
```

Resolved:

```text
decision_id: 1
resolver: resolve_required_fields_decision
```

## Test 4: get_decision

Call:

```text
get_decision(1)
```

Result:

```text
decision_id: 1
policy_id: 1
policy_version: 1
subject: OutcomeAttestationRegistry submission
decision: 1
confidence: 9500
reason_code: required_fields_present
summary: The submission includes repository, documentation, contract address, and test evidence.
```

Conclusion:

The deterministic resolver stored a structured allowed decision with high confidence.

## Test 5: Consumer Verifier API

Call:

```text
is_allowed(1, 7000)
```

Result:

```text
true
```

Conclusion:

The consumer-facing verifier API works. Downstream contracts can depend on `is_allowed` instead of parsing the full decision record.

## Test 6: Fingerprint Reuse Transaction

Transaction:

```text
0x30ac6c886363639606c9d16e4becb6ba0bf62fc804eb6016c8d37eca2d38abf6
```

Result:

```text
ACCEPTED / AGREE / FINISHED_WITH_RETURN
txSlot: 4
```

Payload:

```text
policy_id: 1
subject: OutcomeAttestationRegistry submission
content_uri: https://github.com/Manablaq/genlayer-outcome-attestation-registry
ttl_seconds: 604800
```

Expected behavior:

The exact same canonical decision request should return the existing fresh `decision_id: 1` instead of creating a duplicate.

Verification result:

```text
get_latest_decision_by_fingerprint(...): 1
```

Conclusion:

Fingerprint reuse is working. The registry maps the policy/content/context fingerprint back to the existing resolved decision.
