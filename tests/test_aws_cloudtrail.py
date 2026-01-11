import unittest

from aws_sim.cloudtrail import CloudTrailRecorder


class TestCloudTrail(unittest.TestCase):
    def test_record_event(self):
        recorder = CloudTrailRecorder()
        event = recorder.record(
            event_name="PutObject",
            user_identity="user-1",
            source_ip="1.2.3.4",
            resource="arn:aws:s3:::bucket/key",
        )
        self.assertEqual(event.event_name, "PutObject")
        self.assertEqual(len(recorder.list_events()), 1)


if __name__ == "__main__":
    unittest.main()
