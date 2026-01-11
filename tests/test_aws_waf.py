import unittest
from datetime import datetime

from aws_sim.waf import WafWebAcl, WafRule, WafRequest, IpSet


class TestWaf(unittest.TestCase):
    def test_ip_block_rule(self):
        acl = WafWebAcl("test")
        rule = WafRule(name="block-ip", priority=1, action="BLOCK", ip_set=IpSet(name="bad", addresses=["1.2.3.4"]))
        acl.add_rule(rule)
        request = WafRequest(
            ip="1.2.3.4",
            uri="/login",
            method="POST",
            headers={},
            timestamp=datetime.utcnow(),
        )
        decision = acl.evaluate(request)
        self.assertEqual(decision.action, "BLOCK")


if __name__ == "__main__":
    unittest.main()
