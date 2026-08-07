# Submission Brief

## Contract

`SemanticPolicyGate`

## Category

Reusable GenLayer Intelligent Contract primitive.

## Summary

`SemanticPolicyGate` lets builders register natural-language policies and resolve whether submitted content, actions, agent outputs, or project submissions comply with those policies.

## Problem

Many GenLayer applications need a shared decision about policy compliance. Traditional contracts cannot interpret natural-language policies or messy evidence, and centralized moderation or review services become trusted intermediaries.

## Primitive Provided

The contract standardizes:

```text
policy + subject + content + context -> allowed / denied / needs_review
```

It stores versioned policies, decision requests, structured decision results, confidence, reason codes, summaries, expiry, and canonical fingerprints.

## Reusable Integrations

This primitive can be used by:

- bounty platforms
- DAO proposal gates
- agent marketplaces
- content moderation systems
- grant review processes
- reputation registries
- marketplace listing reviews
- escrow release conditions

## Key Design Choices

- Versioned policies for auditability.
- Decision fingerprints for reuse and caching.
- Deterministic resolver profile for Bradbury smoke tests.
- Generic semantic resolver for natural-language policy decisions.
- Small verifier methods for downstream integrations.

## Why It Fits GenLayer

Policy compliance often depends on language, evidence, ambiguity, and judgment. GenLayer makes that adjudication on-chain and consensus-backed instead of outsourcing it to an operator.

## Bradbury Smoke Test

The deterministic required-fields resolver passed on GenLayer Bradbury Testnet:

```text
contract: 0xc088550EAE168Ccf2027d530Afc495Bb14767CC9
policy_id: 1
decision_id: 1
decision: allowed
confidence: 9500
reason_code: required_fields_present
is_allowed(1, 7000): true
get_latest_decision_by_fingerprint(...): 1
```
