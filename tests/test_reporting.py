import unittest
from datetime import datetime

from nsms.data import LogRecord
from nsms.metrics import Metrics
from nsms.reporting import build_report
from nsms.threat_intel import ThreatIndicator


class TestReporting(unittest.TestCase):
    def test_report_contains_summary(self):
        records = [
            LogRecord(
                timestamp=datetime.utcnow(),
                source_ip="1.2.3.4",
                destination_ip="10.0.0.1",
                protocol="HTTPS",
                bytes_transferred=100,
                action="READ",
                region="us-east-1",
                user="user1",
                resource="/app/service/1",
                status="OK",
            )
        ]
        metrics = Metrics(1, 0, 0, 0)
        report = build_report(records, metrics, [ThreatIndicator("1.2.3.4", "low", "test")], 0)
        self.assertIn("Run Summary", report)
        self.assertIn("Threat Intelligence", report)


if __name__ == "__main__":
    unittest.main()
