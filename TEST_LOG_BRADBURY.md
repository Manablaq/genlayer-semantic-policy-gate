# Test Log — Bradbury

## Local submission gate

Implementation commit: `b132d803d86fd8b2b5ad1bd3ee520522ff6c505c`

Canonical contract SHA-256: `d6a45c984c2f9258fedde84b08bbe046107ccf5f1c5d4761a7ce96ba05f5a724`

| Check | Result |
|---|---|
| Contract Python compilation | PASS |
| Studio Python compilation | PASS |
| Canonical/Studio byte parity | PASS |
| GenVM contract lint and validation | PASS |
| Behavioral security regressions | PASS — 19 tests |
| Git whitespace validation | PASS |

The 19 regressions cover canonical fingerprint binding, delimiter and suffix collision resistance, full evidence hashes, source integrity failures, two-source corroboration, policy updates/deactivation, TTL and evidence-age limits, expiry capping, safe missing-ID handling, and downstream decision-substitution resistance.

## Hardened v2 Bradbury evidence

Live evidence is intentionally pending until a fresh v2 deployment exists.

| Flow | Expected result | Transaction / observation |
|---|---|---|
| Fresh deployment | accepted | `PENDING` |
| Register policy | accepted | `PENDING` |
| Submit hash-pinned two-source request | accepted | `PENDING` |
| Resolve request | accepted with verified source count 2 | `PENDING` |
| Exact fingerprint consumer check | `true` | `PENDING` |
| Altered fingerprint consumer check | `false` | `PENDING` |
| Unknown decision consumer check | `false` | `PENDING` |
| Bad registered evidence hash | resolution fails closed | `PENDING` |
| Stale evidence submission | rejected | `PENDING` |
| Policy deactivation/update | prior authorization returns `false` | `PENDING` |

The old `0xE8f0091c7b95d8D15813aAdFF593c4Df4E7c8fea` deployment is historical and is not evidence for v2.
