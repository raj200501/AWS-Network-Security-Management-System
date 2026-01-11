import unittest

from aws_sim.securityhub import SecurityHub


class TestSecurityHub(unittest.TestCase):
    def test_ingest_and_summarize(self):
        hub = SecurityHub(account_id="123456789012", region="us-east-1")
        hub.ingest_finding(
            source="guardduty",
            title="Suspicious activity",
            description="Details",
            severity="HIGH",
            resource={"instance_id": "i-1"},
        )
        summary = hub.summarize_by_severity()
        self.assertEqual(summary["HIGH"], 1)


if __name__ == "__main__":
    unittest.main()
