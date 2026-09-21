import unittest
from src.readiness import Service,assess
class T(unittest.TestCase):
 def test_ready(self):self.assertTrue(assess(Service(*([True]*10)))["production_ready"])
 def test_unsafe_aiops_is_blocked(self):self.assertIn("ai-remediation-not-approved",assess(Service(*([False]*10)))["findings"])
