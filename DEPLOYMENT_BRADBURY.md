# Bradbury Deployment

## Network

GenLayer Bradbury Testnet

## Contract

`SemanticPolicyGate`

## Contract Address

```text
0xc088550EAE168Ccf2027d530Afc495Bb14767CC9
```

## Deploy Transaction

```text
0x995779a73575b108ab01b4b00c9cf59b6a0bdc1b78d0fa795eadcdfd0988a800
```

## Deployment Result

```text
statusName: ACCEPTED
resultName: AGREE
txExecutionResultName: FINISHED_WITH_RETURN
```

## Recorded At

```text
2026-08-07T20:16:06Z
```

## Next Test

Call `register_policy` using the first smoke-test payload in `STUDIO_BRADBURY_TEST_PLAN.md`.

## Successful Smoke Test

```text
policy_id: 1
decision_id: 1
decision: 1
confidence: 9500
reason_code: required_fields_present
is_allowed(1, 7000): true
get_latest_decision_by_fingerprint(...): 1
```
