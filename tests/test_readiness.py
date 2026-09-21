import unittest
from src.readiness import Service, assess


def ready_service(**overrides):
    values = {"name":"research-api", "availability_slo":99.9, "availability_observed":99.95, "error_budget_remaining_pct":72, "trace_coverage_pct":98, "profiling_enabled":True, "runbook_tested":True, "incident_owner":"platform-oncall", "open_postmortem_actions":0, "rollback_tested":True, "paved_path_version":"eks-service-v3", "ai_remediation_mode":"advisory", "human_approval_required":True}
    values.update(overrides)
    return Service(**values)


class ReadinessTests(unittest.TestCase):
    def test_ready_service_is_approved(self):
        result = assess(ready_service())
        self.assertTrue(result["production_ready"])
        self.assertEqual(100, result["readiness_score"])

    def test_budget_exhaustion_blocks_rollout(self):
        result = assess(ready_service(error_budget_remaining_pct=0))
        self.assertFalse(result["production_ready"])
        self.assertIn("error-budget-exhausted", result["blockers"])

    def test_unapproved_ai_execution_is_blocked(self):
        result = assess(ready_service(ai_remediation_mode="approved-execution", human_approval_required=False))
        self.assertIn("ai-remediation-not-approved", result["blockers"])

    def test_open_postmortem_actions_are_visible(self):
        result = assess(ready_service(open_postmortem_actions=3))
        self.assertTrue(result["production_ready"])
        self.assertEqual("postmortem-actions-open", result["findings"][0]["code"])
