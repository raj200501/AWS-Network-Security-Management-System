import unittest

from aws_sim.dynamodb import DynamoTable


class TestDynamoTable(unittest.TestCase):
    def test_put_get_update_delete(self):
        table = DynamoTable("ThreatIntel", partition_key="id")
        table.put_item({"id": "ip-1", "ip": "1.2.3.4"})
        item = table.get_item("ip-1")
        self.assertIsNotNone(item)
        updated = table.update_item("ip-1", {"severity": "high"})
        self.assertEqual(updated.attributes["severity"], "high")
        removed = table.delete_item("ip-1")
        self.assertTrue(removed)


if __name__ == "__main__":
    unittest.main()
