import unittest

from aws_sim.cloudwatch import CloudWatchMetrics, CloudWatchAlarm


class TestCloudWatch(unittest.TestCase):
    def test_alarm_evaluates_metrics(self):
        metrics = CloudWatchMetrics()
        alarm = CloudWatchAlarm(
            name="HighErrors",
            namespace="NSMS",
            metric_name="Errors",
            threshold=5,
        )
        metrics.put_metric_data("NSMS", "Errors", 10)
        state = alarm.evaluate(metrics)
        self.assertEqual(state.state, "ALARM")


if __name__ == "__main__":
    unittest.main()
