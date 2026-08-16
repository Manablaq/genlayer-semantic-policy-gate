# Bradbury Deployment Record

## Historical Deployment - Not Valid for Resubmission

```text
contract: 0xc088550EAE168Ccf2027d530Afc495Bb14767CC9
deployment_tx: 0x995779a73575b108ab01b4b00c9cf59b6a0bdc1b78d0fa795eadcdfd0988a800
```

This deployment predates the independent-evidence consensus redesign and must not be cited as the corrected contract.

## Corrected Deployment

The corrected, byte-identical Studio source was deployed as a new Bradbury
instance on August 16, 2026:

```text
contract: 0xE8f0091c7b95d8D15813aAdFF593c4Df4E7c8fea
deployment_tx: 0x22ebced9109c006611152b4fbf3f944d6cf424ac921aa2409ab50d5d0e97b43f
source_commit: 27911d9875debd18603952ea0b8431ee8e1629bd
source_match: contracts/semantic_policy_gate.py == studio_bradbury/semantic_policy_gate.py
```

The deployment transaction was accepted. The end-to-end Bradbury test results
are recorded in [TEST_LOG_BRADBURY.md](TEST_LOG_BRADBURY.md): an allowed result
and a denied result were independently evaluated from the same public IANA
source, each at exact confidence `9500`. `get_decision(1)` reports
`consensus_bound: true`; the consumer checks returned `is_allowed(1, 9500) =
true`, `is_denied(1, 9500) = false`, and `needs_review(1) = false`. The denied
path returned `is_denied(2, 9500) = true` and `is_allowed(2, 9500) = false`.
