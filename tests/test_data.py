import unittest
from pathlib import Path

from nsms.data import load_logs, summarize_protocols


class TestData(unittest.TestCase):
    def test_load_logs_returns_records(self):
        records = load_logs(Path("data/sample_logs.csv"))
        self.assertTrue(records)
        self.assertTrue(records[0].source_ip)

    def test_summarize_protocols_counts(self):
        records = load_logs(Path("data/sample_logs.csv"))
        summary = summarize_protocols(records)
        self.assertEqual(sum(summary.values()), len(records))
        self.assertIn("HTTPS", summary)


if __name__ == "__main__":
    unittest.main()
