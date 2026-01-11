import unittest

from aws_sim.kinesis import KinesisStream


class TestKinesis(unittest.TestCase):
    def test_put_and_get_records(self):
        stream = KinesisStream("test-stream", shard_count=2)
        stream.put_record("key1", b"payload1")
        stream.put_record("key2", b"payload2")
        shard_id = stream.list_shards()[0]
        iterator = stream.get_shard_iterator(shard_id)
        records, next_iter = stream.get_records(shard_id, iterator, limit=10)
        self.assertGreaterEqual(len(records), 1)
        self.assertGreaterEqual(next_iter, len(records))
        self.assertEqual(stream.total_records(), 2)


if __name__ == "__main__":
    unittest.main()
