"""Regression checks for the reviewer-required consensus boundary."""

import ast
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "contracts" / "semantic_policy_gate.py").read_text()
STUDIO_SOURCE = (ROOT / "studio_bradbury" / "semantic_policy_gate.py").read_text()


class SemanticPolicyGateConsensusTests(unittest.TestCase):
    def test_nondeterminism_is_not_in_contract_write_methods(self):
        tree = ast.parse(SOURCE)
        contract = next(
            node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "SemanticPolicyGate"
        )
        for method in contract.body:
            if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                implementation = ast.get_source_segment(SOURCE, method) or ""
                self.assertNotIn("gl.nondet", implementation, method.name)

    def test_studio_source_matches_deployable_source(self):
        self.assertEqual(SOURCE, STUDIO_SOURCE)

    def test_semantic_review_uses_strict_independent_consensus(self):
        self.assertIn("def _evaluate_semantic_snapshot(snapshot)", SOURCE)
        self.assertIn("gl.nondet.web.get", SOURCE)
        self.assertIn("gl.nondet.exec_prompt", SOURCE)
        self.assertIn("gl.eq_principle.strict_eq(evaluate_semantic_decision)", SOURCE)
        self.assertNotIn("gl.vm.run_nondet_unsafe", SOURCE)

    def test_authorization_requires_a_bound_consensus_record(self):
        self.assertIn("consensus_bound: bool", SOURCE)
        self.assertIn("and decision.consensus_bound", SOURCE)
        self.assertIn("\"policy_text\": req.policy_text", SOURCE)
        self.assertIn("\"policy_digest\": req.policy_digest", SOURCE)
        self.assertIn("evidence_digest=evidence_digest[:512]", SOURCE)

    def test_no_deterministic_authorization_bypass_remains(self):
        self.assertNotIn("resolve_required_fields_decision", SOURCE)


if __name__ == "__main__":
    unittest.main()
