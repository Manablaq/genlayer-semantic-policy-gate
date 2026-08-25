# Studio and Bradbury Test Plan

This plan produces reviewer-reproducible evidence for the hardened v2 contract. Use the exact committed source; do not edit the Studio copy independently.

## 1. Pre-deployment verification

```bash
cmp contracts/semantic_policy_gate.py studio_bradbury/semantic_policy_gate.py
PYTHONPYCACHEPREFIX=/private/tmp/semantic-policy-gate-pycache \
  python3 -m unittest discover -s tests -p 'test_*.py'
```

## 2. Deploy

```bash
genlayer deploy --contract contracts/semantic_policy_gate.py
export C=0x_REPLACE_WITH_NEW_CONTRACT
```

Wait for acceptance/finalization as required by Bradbury before dependent writes.

## 3. Register a strict policy

```bash
genlayer write "$C" register_policy --args \
  "Reserved example-domain policy" \
  "Allow only when both registered authorities establish that example.com, example.net, and example.org are reserved for documentation and examples."
```

Use policy ID `1` in a fresh deployment.

## 4. Compute and submit an immutable evidence request

```bash
OBS=$(date +%s)

genlayer call "$C" compute_fingerprint --args \
  1 "Reserved example domains" \
  "example.com, example.net, and example.org are reserved for documentation and examples." \
  "Bradbury v2 regression" \
  "https://www.iana.org/help/example-domains" \
  "6fde51fc02d67b032e17adfe1ae5c67daf2c01bed20f533b7754ee32e14c4bc9" \
  "IANA" \
  "https://www.rfc-editor.org/rfc/rfc2606.txt" \
  "b6869c8984701701bc2e6973b6ffc750d497f845cc1a65a106e9301590a13ab0" \
  "RFC Editor / IETF" \
  "IANA help page and RFC 2606 observed for hardened v2" \
  "$OBS" 86400 2 604800

genlayer write "$C" submit_decision --args \
  1 "Reserved example domains" \
  "example.com, example.net, and example.org are reserved for documentation and examples." \
  "Bradbury v2 regression" \
  "https://www.iana.org/help/example-domains" \
  "6fde51fc02d67b032e17adfe1ae5c67daf2c01bed20f533b7754ee32e14c4bc9" \
  "IANA" \
  "https://www.rfc-editor.org/rfc/rfc2606.txt" \
  "b6869c8984701701bc2e6973b6ffc750d497f845cc1a65a106e9301590a13ab0" \
  "RFC Editor / IETF" \
  "IANA help page and RFC 2606 observed for hardened v2" \
  "$OBS" 86400 2 604800
```

Save the computed fingerprint and use decision ID `1` on a fresh deployment.

## 5. Resolve and inspect

```bash
genlayer write "$C" resolve_semantic_decision --args 1
genlayer call "$C" get_decision --args 1
```

Verify `content_verified: true`, `consensus_bound: true`, `verified_source_count: 2`, exact observed hashes, and a bounded expiry.

## 6. Consumer-binding regressions

```bash
genlayer call "$C" is_allowed_for --args \
  1 "$FINGERPRINT" 0x_REPLACE_WITH_POLICY_OWNER 3600

genlayer call "$C" is_allowed_for --args \
  1 "f${FINGERPRINT:1}" 0x_REPLACE_WITH_POLICY_OWNER 3600

genlayer call "$C" is_allowed_for --args \
  999 "$FINGERPRINT" 0x_REPLACE_WITH_POLICY_OWNER 3600
```

Expected results are `true`, `false`, and `false`.

## 7. Fail-closed and revocation regressions

- Submit a fresh request with one changed character in a registered SHA-256, then show resolution fails without creating a decision.
- Submit with an observation time older than the registered maximum age and show submission is rejected.
- Deactivate policy `1`, then repeat the previously true `is_allowed_for` call and show it returns `false`.

Record every accepted, rejected, and controlled-failure transaction in `TEST_LOG_BRADBURY.md` with direct Explorer links.
