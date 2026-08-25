"""Behavioral and structural regressions for SemanticPolicyGate v2."""

import ast
import hashlib
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "contracts" / "semantic_policy_gate.py").read_text()
STUDIO_SOURCE = (ROOT / "studio_bradbury" / "semantic_policy_gate.py").read_text()


def _load_contract_helpers():
    selected = {
        "_canonical",
        "_sha256_hex",
        "_normalize_sha256",
        "_is_sha256_hex",
        "_canonical_json_sha256",
        "_policy_digest",
        "_decision_fingerprint",
        "_fresh_at",
        "_coerce_json_object",
        "_canonical_reason_code",
        "_canonical_summary",
        "_normalize_semantic_decision",
        "_is_valid_semantic_decision",
    }
    tree = ast.parse(SOURCE)
    functions = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name in selected
    ]
    namespace = {"hashlib": hashlib, "json": json, "re": re}
    exec(
        compile(ast.Module(body=functions, type_ignores=[]), "helpers", "exec"),
        namespace,
    )
    return namespace


HELPERS = _load_contract_helpers()


def _fingerprint_spec(**overrides):
    values = {
        "policy_id": 7,
        "policy_owner": "0x1111111111111111111111111111111111111111",
        "policy_version": 3,
        "policy_digest": "a" * 64,
        "subject": "Verify the registered action",
        "submitted_content_sha256": "b" * 64,
        "context_sha256": "c" * 64,
        "primary_evidence_uri": "https://authority.example/policy/v3.json",
        "primary_evidence_sha256": "d" * 64,
        "primary_authority": "Official Authority",
        "corroborating_evidence_uri": "",
        "corroborating_evidence_sha256": "",
        "corroborating_authority": "",
        "evidence_version": "release-v3",
        "evidence_observed_at": 1_700_000_000,
        "max_evidence_age_seconds": 86_400,
        "minimum_sources": 1,
        "ttl_seconds": 3_600,
    }
    values.update(overrides)
    return values


def _snapshot(**overrides):
    values = {
        "primary_evidence_uri": "https://authority.example/policy/v3.json",
        "primary_evidence_sha256": "d" * 64,
        "corroborating_evidence_uri": "",
        "corroborating_evidence_sha256": "",
        "minimum_sources": 1,
    }
    values.update(overrides)
    return values


class SemanticPolicyGateV2Tests(unittest.TestCase):
    def test_nondeterminism_is_not_in_contract_methods(self):
        tree = ast.parse(SOURCE)
        contract = next(
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "SemanticPolicyGate"
        )
        for method in contract.body:
            if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                implementation = ast.get_source_segment(SOURCE, method) or ""
                self.assertNotIn("gl.nondet", implementation, method.name)

    def test_studio_source_matches_primary_source(self):
        self.assertEqual(SOURCE, STUDIO_SOURCE)

    def test_full_content_hashes_are_inside_strict_consensus(self):
        self.assertIn("gl.nondet.web.get", SOURCE)
        self.assertIn("_sha256_hex(body)", SOURCE)
        self.assertIn(
            "gl.eq_principle.strict_eq(evaluate_semantic_decision)",
            SOURCE,
        )
        self.assertIn('if not agreed["integrity_ok"]', SOURCE)
        self.assertNotIn("gl.vm.run_nondet_unsafe", SOURCE)

    def test_policy_digest_is_cryptographic_and_versioned(self):
        digest = HELPERS["_policy_digest"]
        base = digest("0xabc", "Policy", "Require A", 1, True)
        self.assertRegex(base, r"^[0-9a-f]{64}$")
        self.assertNotEqual(base, digest("0xdef", "Policy", "Require A", 1, True))
        self.assertNotEqual(base, digest("0xabc", "Policy", "Require B", 1, True))
        self.assertNotEqual(base, digest("0xabc", "Policy", "Require A", 2, True))
        self.assertNotEqual(base, digest("0xabc", "Policy", "Require A", 1, False))

    def test_separator_injection_cannot_collide(self):
        fingerprint = HELPERS["_decision_fingerprint"]
        first = _fingerprint_spec(subject="alpha|beta", primary_evidence_uri="gamma")
        second = _fingerprint_spec(subject="alpha", primary_evidence_uri="beta|gamma")
        self.assertNotEqual(fingerprint(**first), fingerprint(**second))

    def test_suffix_mutation_changes_content_and_fingerprint(self):
        sha256_hex = HELPERS["_sha256_hex"]
        prefix = b"x" * 512
        first_hash = sha256_hex(prefix + b"allowed suffix")
        second_hash = sha256_hex(prefix + b"denied suffix")
        self.assertNotEqual(first_hash, second_hash)
        fingerprint = HELPERS["_decision_fingerprint"]
        self.assertNotEqual(
            fingerprint(**_fingerprint_spec(submitted_content_sha256=first_hash)),
            fingerprint(**_fingerprint_spec(submitted_content_sha256=second_hash)),
        )

    def test_every_security_field_changes_the_fingerprint(self):
        fingerprint = HELPERS["_decision_fingerprint"]
        base_spec = _fingerprint_spec()
        base = fingerprint(**base_spec)
        changes = {
            "policy_id": 8,
            "policy_owner": "0x2222222222222222222222222222222222222222",
            "policy_version": 4,
            "policy_digest": "f" * 64,
            "subject": "Different subject",
            "submitted_content_sha256": "1" * 64,
            "context_sha256": "2" * 64,
            "primary_evidence_uri": "https://different.example/v3.json",
            "primary_evidence_sha256": "3" * 64,
            "primary_authority": "Different Authority",
            "corroborating_evidence_uri": "https://second.example/v3.json",
            "corroborating_evidence_sha256": "4" * 64,
            "corroborating_authority": "Second Authority",
            "evidence_version": "release-v4",
            "evidence_observed_at": 1_700_000_001,
            "max_evidence_age_seconds": 86_401,
            "minimum_sources": 2,
            "ttl_seconds": 3_601,
        }
        for field, value in changes.items():
            with self.subTest(field=field):
                changed = dict(base_spec)
                changed[field] = value
                self.assertNotEqual(base, fingerprint(**changed))

    def test_hash_case_is_normalized_but_policy_case_is_not(self):
        fingerprint = HELPERS["_decision_fingerprint"]
        lower = _fingerprint_spec(policy_digest="a" * 64)
        upper = _fingerprint_spec(policy_digest="A" * 64)
        self.assertEqual(fingerprint(**lower), fingerprint(**upper))
        self.assertNotEqual(
            fingerprint(**_fingerprint_spec(subject="Policy ID A")),
            fingerprint(**_fingerprint_spec(subject="Policy ID a")),
        )

    def test_primary_hash_mismatch_fails_closed(self):
        normalize = HELPERS["_normalize_semantic_decision"]
        primary = {"ok": True, "body": b"changed", "sha256": "e" * 64}
        empty = {"ok": True, "body": b"", "sha256": ""}
        result = normalize(
            {"decision": "allowed"},
            _snapshot(),
            primary,
            empty,
        )
        self.assertFalse(result["integrity_ok"])
        self.assertEqual(result["decision"], "error")

    def test_fetch_failure_cannot_store_allowed(self):
        normalize = HELPERS["_normalize_semantic_decision"]
        failed = {"ok": False, "body": b"", "sha256": ""}
        empty = {"ok": True, "body": b"", "sha256": ""}
        result = normalize(
            {"decision": "allowed"},
            _snapshot(),
            failed,
            empty,
        )
        self.assertFalse(result["integrity_ok"])
        self.assertEqual(result["decision"], "error")

    def test_two_source_policy_requires_both_hashes(self):
        normalize = HELPERS["_normalize_semantic_decision"]
        snapshot = _snapshot(
            corroborating_evidence_uri="https://second.example/v3.json",
            corroborating_evidence_sha256="e" * 64,
            minimum_sources=2,
        )
        primary = {"ok": True, "body": b"", "sha256": "d" * 64}
        bad_secondary = {"ok": True, "body": b"", "sha256": "f" * 64}
        result = normalize(
            {"decision": "allowed"}, snapshot, primary, bad_secondary
        )
        self.assertFalse(result["integrity_ok"])
        self.assertEqual(result["verified_source_count"], 1)
        self.assertEqual(result["decision"], "error")

    def test_consumer_freshness_is_measured_from_resolution(self):
        fresh_at = HELPERS["_fresh_at"]
        self.assertTrue(fresh_at(1_000, 2_000, 1_300, 300))
        self.assertFalse(fresh_at(1_000, 2_000, 1_301, 300))
        self.assertFalse(fresh_at(1_000, 1_300, 1_300, 300))
        self.assertFalse(fresh_at(1_000, 2_000, 999, 300))

    def test_consumers_bind_fingerprint_owner_and_age(self):
        self.assertIn("def is_allowed_for(", SOURCE)
        self.assertIn("def is_denied_for(", SOURCE)
        self.assertIn("expected_fingerprint: str", SOURCE)
        self.assertIn("expected_policy_owner: Address", SOURCE)
        self.assertIn("consumer_max_age_seconds: u256", SOURCE)
        self.assertIn("decision.fingerprint ==", SOURCE)
        self.assertIn("decision.policy_owner == expected_policy_owner", SOURCE)
        self.assertNotIn("def is_allowed(", SOURCE)
        self.assertNotIn("def is_denied(", SOURCE)

    def test_policy_change_and_deactivation_revoke_old_decisions(self):
        self.assertIn("policy.version = policy.version + u256(1)", SOURCE)
        self.assertIn("and policy.version == decision.policy_version", SOURCE)
        self.assertIn("and policy.policy_digest == decision.policy_digest", SOURCE)
        self.assertIn("policy.active", SOURCE)

    def test_decision_expiry_is_capped_by_evidence_freshness(self):
        self.assertIn("ttl_expiry = resolved_at + req.decision_ttl_seconds", SOURCE)
        self.assertIn(
            "evidence_expiry = req.evidence_observed_at + req.max_evidence_age_seconds",
            SOURCE,
        )
        self.assertIn("if evidence_expiry < expires_at:", SOURCE)

    def test_request_and_evidence_lifetimes_are_bounded(self):
        self.assertIn("MIN_TTL_SECONDS", SOURCE)
        self.assertIn("MAX_TTL_SECONDS", SOURCE)
        self.assertIn("REQUEST_RESOLUTION_WINDOW_SECONDS", SOURCE)
        self.assertIn("MAX_EVIDENCE_AGE_SECONDS", SOURCE)
        self.assertIn("MAX_EVIDENCE_BYTES", SOURCE)
        self.assertIn('raise gl.vm.UserError("evidence is already stale")', SOURCE)
        self.assertIn(
            'raise gl.vm.UserError("evidence became stale before resolution")',
            SOURCE,
        )

    def test_source_free_and_non_https_requests_are_rejected(self):
        self.assertIn(
            'self._require_https_uri(primary_evidence_uri, "primary evidence URI")',
            SOURCE,
        )
        self.assertIn('field + " must use HTTPS"', SOURCE)
        self.assertNotIn('if uri == "":\n        return ""', SOURCE)

    def test_unknown_records_are_checked_before_attribute_access(self):
        self.assertIn("if policy_id not in self.policies:", SOURCE)
        self.assertIn("if decision_id not in self.requests:", SOURCE)
        self.assertIn("if decision_id not in self.decisions:", SOURCE)
        self.assertNotIn("if decision.created_at == u256(0):", SOURCE)
        self.assertNotIn("if policy.created_at == u256(0):", SOURCE)

    def test_plaintext_truncation_digests_are_removed(self):
        self.assertNotIn("def _text_digest", SOURCE)
        self.assertNotIn("def _semantic_evidence_digest", SOURCE)
        self.assertNotIn("material[:512]", SOURCE)
        self.assertIn("submitted_content_sha256", SOURCE)
        self.assertIn("primary_content_sha256", SOURCE)


if __name__ == "__main__":
    unittest.main()
