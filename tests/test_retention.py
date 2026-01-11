import unittest
from datetime import datetime, timedelta
from pathlib import Path

from nsms.retention import enforce_retention


class TestRetention(unittest.TestCase):
    def test_enforce_retention_removes_old_files(self):
        temp_dir = Path("outputs") / "retention-test"
        temp_dir.mkdir(parents=True, exist_ok=True)
        old_file = temp_dir / "old.txt"
        old_file.write_text("old")
        old_time = datetime.utcnow() - timedelta(days=40)
        old_timestamp = old_time.timestamp()
        old_file.touch()
        old_file.chmod(0o644)
        Path(old_file).touch()
        import os
        os.utime(old_file, (old_timestamp, old_timestamp))

        removed = enforce_retention(temp_dir, retention_days=30)
        self.assertEqual(removed, 1)
        self.assertFalse(old_file.exists())


if __name__ == "__main__":
    unittest.main()
