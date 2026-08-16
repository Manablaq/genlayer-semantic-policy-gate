# Bradbury Deployment Record

## Historical Deployment - Not Valid for Resubmission

```text
contract: 0xc088550EAE168Ccf2027d530Afc495Bb14767CC9
deployment_tx: 0x995779a73575b108ab01b4b00c9cf59b6a0bdc1b78d0fa795eadcdfd0988a800
```

This deployment predates the independent-evidence consensus redesign and must not be cited as the corrected contract.

## Corrected Deployment Checklist

After deploying `studio_bradbury/semantic_policy_gate.py`, record:

```text
contract: <new Bradbury address>
deployment_tx: <accepted deployment transaction>
source_commit: <commit containing this redesign>
source_match: contracts/semantic_policy_gate.py == studio_bradbury/semantic_policy_gate.py
```

The corrected deployment is ready for evidence only after its deployment transaction is accepted and the smoke test demonstrates a `consensus_bound` decision.
