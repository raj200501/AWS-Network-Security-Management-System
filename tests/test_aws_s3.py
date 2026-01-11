import unittest

from aws_sim.s3 import S3Bucket


class TestS3Bucket(unittest.TestCase):
    def test_put_get_list(self):
        bucket = S3Bucket("logs")
        bucket.put_object("a.txt", b"data", content_type="text/plain")
        obj = bucket.get_object("a.txt")
        self.assertIsNotNone(obj)
        self.assertEqual(obj.content_type, "text/plain")
        listing = bucket.list_objects()
        self.assertEqual(len(listing), 1)


if __name__ == "__main__":
    unittest.main()
