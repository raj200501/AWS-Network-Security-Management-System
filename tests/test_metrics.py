import unittest
from datetime import datetime

from nsms.metrics import compute_metrics
from nsms.data import LogRecord


class TestMetrics(unittest.TestCase):
    def _record(self):
        return LogRecord(
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

    def test_compute_metrics_counts(self):
        records = [self._record(), self._record()]
        metrics = compute_metrics(records, [True, False], [False, True], [False, False])
        self.assertEqual(metrics.total_records, 2)
        self.assertEqual(metrics.anomalous_records, 1)
        self.assertEqual(metrics.threat_intel_hits, 1)


if __name__ == "__main__":
    unittest.main()
