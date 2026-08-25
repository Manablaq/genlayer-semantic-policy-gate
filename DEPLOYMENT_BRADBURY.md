# Bradbury Deployment Record

## Hardened v2

| Field | Value |
|---|---|
| Network | Bradbury Phase 1 |
| Contract | [`0xD16a0c53cE55734499554b9ef5919dc98B9Af6f0`](https://explorer-bradbury.genlayer.com/address/0xD16a0c53cE55734499554b9ef5919dc98B9Af6f0) |
| Deployment transaction | [`0x2f85572738370619f06da6eeb812dd9a784cbb2d8b3fe014b039ccc440e8a997`](https://explorer-bradbury.genlayer.com/tx/0x2f85572738370619f06da6eeb812dd9a784cbb2d8b3fe014b039ccc440e8a997) |
| Deployment result | `ACCEPTED / AGREE / FINISHED_WITH_RETURN` |
| Canonical source | `contracts/semantic_policy_gate.py` |
| Studio source | `studio_bradbury/semantic_policy_gate.py` |
| Source commit | `b132d803d86fd8b2b5ad1bd3ee520522ff6c505c` |
| Source SHA-256 | `d6a45c984c2f9258fedde84b08bbe046107ccf5f1c5d4761a7ce96ba05f5a724` |
| Local regressions | 19 passing |

The fresh deployment completed successfully. The deployment CLI submitted the canonical v2 source and returned `ACCEPTED / AGREE / FINISHED_WITH_RETURN`. Live behavioral regressions and an Explorer source-parity check remain required before resubmission.

## Historical deployment

The original contract at `0xE8f0091c7b95d8D15813aAdFF593c4Df4E7c8fea` and deployment transaction `0x22ebced9109c006611152b4fbf3f944d6cf424ac921aa2409ab50d5d0e97b43f` predate the v2 hardening. They are retained only for audit history and must not be used as resubmission evidence.

## Reproduction command

From the repository root, with the intended account active and unlocked:

```bash
genlayer deploy --contract contracts/semantic_policy_gate.py
```

Complete every live test in `STUDIO_BRADBURY_TEST_PLAN.md` and add the accepted transaction links to `TEST_LOG_BRADBURY.md` before resubmission.
