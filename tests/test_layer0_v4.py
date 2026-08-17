import unittest

from layer0_functional_conformance_v4 import (
    REQUIRED_RESPONSIBILITIES,
    evaluate_candidate,
    reference_candidate,
)


class Layer0V4Tests(unittest.TestCase):
    def test_symbolic_candidate_passes(self):
        self.assertEqual(evaluate_candidate(reference_candidate())["status"], "PASS")

    def test_neural_construction_is_not_required(self):
        c = reference_candidate()
        c["construction_profile"] = ["authored", "compiled"]
        self.assertEqual(evaluate_candidate(c)["status"], "PASS")

    def test_merged_roles_are_allowed(self):
        c = reference_candidate()
        c["mechanisms"] = [{"mechanism_id": "one", "responsibilities": list(REQUIRED_RESPONSIBILITIES)}]
        self.assertEqual(evaluate_candidate(c)["status"], "PASS")

    def test_required_responsibility_failure_is_fail(self):
        c = reference_candidate()
        c["functional_evidence"]["RESULT_SURFACE"]["status"] = "FAIL"
        self.assertEqual(evaluate_candidate(c)["status"], "FAIL")

    def test_unknown_is_suspend(self):
        c = reference_candidate()
        c["functional_evidence"]["CONTEXT_BOUND_STATE"]["status"] = "UNKNOWN"
        self.assertEqual(evaluate_candidate(c)["status"], "SUSPEND")

    def test_empty_trace_is_suspend(self):
        c = reference_candidate()
        c["execution_trace"] = []
        self.assertEqual(evaluate_candidate(c)["status"], "SUSPEND")

    def test_negative_control_failure_is_fail(self):
        c = reference_candidate()
        c["negative_controls"]["context_removed_or_fixed"] = "FAIL"
        self.assertEqual(evaluate_candidate(c)["status"], "FAIL")

    def test_bad_digest_is_suspend(self):
        c = reference_candidate()
        c["source_material_digest"] = "abc"
        self.assertEqual(evaluate_candidate(c)["status"], "SUSPEND")

    def test_not_applicable(self):
        c = reference_candidate()
        c["scope"] = "NOT_APPLICABLE"
        self.assertEqual(evaluate_candidate(c)["status"], "NOT_APPLICABLE")


if __name__ == "__main__":
    unittest.main()
