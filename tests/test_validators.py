import unittest
from datetime import datetime, timedelta

from nsms.data import LogRecord
from nsms.validators import validate_records


class TestValidators(unittest.TestCase):
    def test_validate_records_finds_future_timestamp(self):
        record = LogRecord(
            timestamp=datetime.utcnow() + timedelta(days=1),
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
        issues = validate_records([record])
        self.assertEqual(len(issues), 1)
        self.assertIn("future", issues[0].message)


if __name__ == "__main__":
    unittest.main()
