# Bradbury Test Log

## Historical Result

The deployment at `0xc088550EAE168Ccf2027d530Afc495Bb14767CC9` and its original smoke tests are retained only as historical context. They used a source-free required-fields resolver and do not demonstrate the corrected security model.

## Corrected Test Requirements

The replacement deployment must record:

```text
accepted deployment transaction
new contract address
resolve_semantic_decision transaction
get_decision output with consensus_bound: true
consumer verifier output at the canonical confidence threshold
```

The corrected resolver requires all validators to independently fetch evidence and reapply the stored policy before strict equality commits the result.
