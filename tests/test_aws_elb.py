import unittest

from aws_sim.elasticloadbalancing import ElbService, Target


class TestElb(unittest.TestCase):
    def test_create_load_balancer(self):
        elb = ElbService()
        lb = elb.create_load_balancer("web")
        tg = elb.create_target_group(lb.load_balancer_arn, protocol="HTTP", port=80)
        tg.register_target(Target(target_id="i-1", port=80, healthy=True))
        listener = elb.create_listener(lb.load_balancer_arn, protocol="HTTP", port=80, target_group_arn=tg.target_group_arn)
        self.assertEqual(listener.port, 80)
        self.assertEqual(len(tg.healthy_targets()), 1)


if __name__ == "__main__":
    unittest.main()
