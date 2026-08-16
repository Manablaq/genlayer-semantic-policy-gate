# Bradbury Test Log

## Historical Result

The deployment at `0xc088550EAE168Ccf2027d530Afc495Bb14767CC9` and its original smoke tests are retained only as historical context. They used a source-free required-fields resolver and do not demonstrate the corrected security model.

## Corrected Deployment

```text
contract: 0xE8f0091c7b95d8D15813aAdFF593c4Df4E7c8fea
deployment_tx: 0x22ebced9109c006611152b4fbf3f944d6cf424ac921aa2409ab50d5d0e97b43f
source_commit: 27911d9875debd18603952ea0b8431ee8e1629bd
deployment_status: accepted
```

## End-to-End Consensus Tests

Both paths used policy `2`, the duplicate registration retained after an accidental
second `register_policy` call. The duplicate has the same immutable policy text;
all subsequent requests explicitly reference policy `2`.

### Allowed Path

```text
submit transaction:  0xf1bbbef7b7ce56fd0a9fe0b3eb901d1b410bc58748020e1c98b348d1f4e920b8
resolve transaction: 0x24a33155dee8c30613f33432ccabf7bc50ace0d7b8339b2b0557179e9429b055
decision id:         1
source:              https://www.iana.org/help/example-domains
decision:            allowed
confidence:          9500
consensus_bound:     true
is_allowed(1, 9500): true
is_denied(1, 9500):  false
needs_review(1):     false
```

`get_decision(1)` reports a policy snapshot (`policy_id: 2`,
`policy_version: 1`), an evidence digest derived from the independently fetched
IANA page, and `reason_code: policy_satisfied`.

### Denied Path

```text
submit transaction:  0xb037c88c47179d280242fcde286903651332508abdc7e21757b55a11e8fd88e0
resolve transaction: 0xf56647a485cc34c2fb79388751653715de272ed5a77daf9b6287e50f604c1a85
decision id:         2
source:              https://www.iana.org/help/example-domains
decision:            denied
confidence:          9500
is_denied(2, 9500):  true
is_allowed(2, 9500): false
```

The denied request asserted the opposite of the IANA page: that `example.com`
and `example.org` are available for registration or transfer. The independently
reviewed source contradicts that assertion, and the contract returned the
canonical `denied` outcome with `reason_code: policy_violated`.

## Conclusion

The corrected resolver requires every validator to independently fetch the
registered evidence and reapply the immutable policy snapshot. `strict_eq`
binds the full canonical result before storage is written. The two Bradbury
tests show that downstream consumers can only authorize the exact consensus-bound
allowed result and can only deny the exact consensus-bound denied result.
