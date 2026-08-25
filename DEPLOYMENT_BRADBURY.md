# Bradbury Deployment Record

## Hardened v2

| Field | Value |
|---|---|
| Network | Bradbury Phase 1 |
| Contract | `PENDING_FRESH_DEPLOYMENT` |
| Deployment transaction | `PENDING_FRESH_DEPLOYMENT` |
| Canonical source | `contracts/semantic_policy_gate.py` |
| Studio source | `studio_bradbury/semantic_policy_gate.py` |
| Source commit | `b132d803d86fd8b2b5ad1bd3ee520522ff6c505c` |
| Source SHA-256 | `d6a45c984c2f9258fedde84b08bbe046107ccf5f1c5d4761a7ce96ba05f5a724` |
| Local regressions | 19 passing |

A fresh deployment is mandatory because GenLayer contracts are immutable and the security model changed materially. The deployed Explorer source must match the canonical and Studio source byte-for-byte.

## Historical deployment

The original contract at `0xE8f0091c7b95d8D15813aAdFF593c4Df4E7c8fea` and deployment transaction `0x22ebced9109c006611152b4fbf3f944d6cf424ac921aa2409ab50d5d0e97b43f` predate the v2 hardening. They are retained only for audit history and must not be used as resubmission evidence.

## Deployment command

From the repository root, with the intended account active and unlocked:

```bash
genlayer deploy --contract contracts/semantic_policy_gate.py
```

After deployment, record the returned address and transaction above, complete every live test in `STUDIO_BRADBURY_TEST_PLAN.md`, and add the accepted transaction links to `TEST_LOG_BRADBURY.md` before resubmission.
