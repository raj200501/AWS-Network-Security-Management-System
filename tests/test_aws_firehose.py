import unittest

from aws_sim.firehose import FirehoseDeliveryStream
from aws_sim.s3 import S3Bucket


class TestFirehose(unittest.TestCase):
    def test_flush_writes_to_s3(self):
        bucket = S3Bucket("logs")
        stream = FirehoseDeliveryStream("delivery", bucket, prefix="test/")
        stream.put_record(b"line1")
        keys = stream.flush()
        self.assertEqual(len(keys), 1)
        obj = bucket.get_object(keys[0])
        self.assertIsNotNone(obj)


if __name__ == "__main__":
    unittest.main()
