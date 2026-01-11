import unittest

from aws_sim.sns import SnsTopic


class TestSns(unittest.TestCase):
    def test_publish_and_subscribe(self):
        topic = SnsTopic("arn:aws:sns:region:account:test")
        received = []

        def subscriber(message):
            received.append(message)

        topic.subscribe(subscriber)
        message = topic.publish("alert", "body")
        self.assertEqual(message.subject, "alert")
        self.assertEqual(topic.subscriber_count(), 1)
        self.assertEqual(len(received), 1)


if __name__ == "__main__":
    unittest.main()
