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

The fresh v2 deployment and its completed live security regressions are recorded below. The Explorer Code tab was also compared with `contracts/semantic_policy_gate.py` and matched byte-for-byte (35,741 characters).

| Flow | Expected result | Transaction / observation |
|---|---|---|
| Fresh deployment | accepted | [`0x2f8557…a997`](https://explorer-bradbury.genlayer.com/tx/0x2f85572738370619f06da6eeb812dd9a784cbb2d8b3fe014b039ccc440e8a997) — contract [`0xD16a…f6f0`](https://explorer-bradbury.genlayer.com/address/0xD16a0c53cE55734499554b9ef5919dc98B9Af6f0) |
| Register policy | accepted, unanimous agreement | [`0x108613…93ad`](https://explorer-bradbury.genlayer.com/tx/0x10861301b732c66bae986866b3e3fc5a816cbb95c292ed4f2fbc672ea63193ad) — policy ID `1` |
| Submit hash-pinned two-source request | accepted, unanimous agreement | [`0x3d2469…ca64`](https://explorer-bradbury.genlayer.com/tx/0x3d24696608fe64377884ecccbf0d11555e5fed88e76215b7d280ae364f6aca64) — request ID `1`, fingerprint `8d06ec8c64f995cec7b02adc66841051353d52773e73f96849547651b884f6e5` |
| Resolve request | accepted; `allowed`, integrity true, verified source count 2 | [`0xa57a71…116e`](https://explorer-bradbury.genlayer.com/tx/0xa57a714aa65af26d3c69a171a4d8dce60d3ebbaf2dbd74d8474bc4f997c6116e) |
| Exact fingerprint consumer check | `true` | `is_allowed_for(1, 8d06ec…f6e5, policy_owner, 3600)` returned `true` |
| Altered fingerprint consumer check | `false` | `is_allowed_for(1, fd06ec…f6e5, policy_owner, 3600)` returned `false` |
| Unknown decision consumer check | `false` | `is_allowed_for(999, 8d06ec…f6e5, policy_owner, 3600)` returned `false` without an exception |
| Bad registered evidence hash | resolution fails closed; integrity false; verified source count 1; no decision stored | Request [`0x612d3f…c819`](https://explorer-bradbury.genlayer.com/tx/0x612d3f411e83b282603c4546b45149c4b37b2402dbb1e581ddf231de9f7ac819), rejected resolution [`0xf094c9…246e`](https://explorer-bradbury.genlayer.com/tx/0xf094c9daadc8b433ddbfa583449ef786bd180285d464fd3207652e63ae0d246e) |
| Stale evidence submission | rejected before request storage | [`0xc681ed…6c53`](https://explorer-bradbury.genlayer.com/tx/0xc681eded6d4af2f88fe9bc212340196d7424e8f06d3255bda553ba480a586c53) — unanimous `DISAGREE`, `FINISHED_WITH_ERROR` |
| Policy deactivation/update | prior authorization returns `false` | Covered by the passing local policy-revocation regression; the live policy remains active so the accepted decision and exact-fingerprint `true` result stay reproducible for review |

The old `0xE8f0091c7b95d8D15813aAdFF593c4Df4E7c8fea` deployment is historical and is not evidence for v2.
