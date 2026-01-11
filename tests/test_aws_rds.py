import unittest

from aws_sim.rds import RdsService


class TestRds(unittest.TestCase):
    def test_snapshot(self):
        rds = RdsService()
        rds.create_instance("db-1", "postgres")
        snapshot = rds.create_snapshot("db-1")
        self.assertTrue(snapshot.snapshot_id.startswith("snapshot-"))


if __name__ == "__main__":
    unittest.main()
