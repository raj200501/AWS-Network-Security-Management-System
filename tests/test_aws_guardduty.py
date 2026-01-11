import unittest

from aws_sim.guardduty import GuardDutyDetector


class TestGuardDuty(unittest.TestCase):
    def test_create_and_filter_findings(self):
        detector = GuardDutyDetector("det-1")
        detector.create_finding(
            finding_type="Recon:EC2/PortProbe",
            severity=5.0,
            description="Port probe detected",
            resource={"instance_id": "i-123"},
        )
        detector.create_filter("port-probe", {"finding_type": "Recon:EC2/PortProbe"})
        findings = detector.match_filter("port-probe")
        self.assertEqual(len(findings), 1)


if __name__ == "__main__":
    unittest.main()
