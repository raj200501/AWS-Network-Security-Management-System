import unittest

from aws_sim.iam import IamPolicy, IamRole, PolicyStatement


class TestIam(unittest.TestCase):
    def test_policy_allows_action(self):
        policy = IamPolicy([
            PolicyStatement(effect="Allow", actions=["s3:GetObject"], resources=["arn:aws:s3:::bucket/*"])
        ])
        role = IamRole(name="reader", policies=[policy])
        decision = role.authorize("s3:GetObject", "arn:aws:s3:::bucket/key")
        self.assertTrue(decision.allowed)


if __name__ == "__main__":
    unittest.main()
