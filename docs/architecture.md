# Architecture

```text
versioned policy -> immutable request snapshot -> independent validator evaluation
                                              -> strict equality of canonical result
                                              -> bound on-chain decision -> consumer verifier
```

`_evaluate_semantic_snapshot` is the sole non-deterministic boundary. It only reads the immutable snapshot, fetches the registered evidence, and derives a canonical JSON result. It performs no storage writes or transfers.

`resolve_semantic_decision` runs that evaluator under `gl.eq_principle.strict_eq`, validates the agreed result again, then writes the decision with `consensus_bound = true`. The `is_allowed` and `is_denied` views bind authorization to this flag, the exact outcome, canonical confidence, and freshness.

No source-free resolver profile exists, because all authorization-relevant outcomes must use the same independently reviewed evidence path.
