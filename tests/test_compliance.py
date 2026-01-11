import unittest
from pathlib import Path

from nsms.compliance import ComplianceChecker
from nsms.data import load_logs


class TestCompliance(unittest.TestCase):
    def test_compliance_flags_violation(self):
        checker = ComplianceChecker.load(Path("data/compliance_rules.json"))
        records = load_logs(Path("data/sample_logs.csv"))
        violations = [checker.evaluate(record) for record in records]
        self.assertTrue(any(violations))


if __name__ == "__main__":
    unittest.main()
