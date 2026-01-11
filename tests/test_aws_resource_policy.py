import unittest

from aws_sim.resource_policies import ResourcePolicy, ResourcePolicyStatement


class TestResourcePolicy(unittest.TestCase):
    def test_allows_principal(self):
        policy = ResourcePolicy(
            [
                ResourcePolicyStatement(
                    effect="Allow",
                    principals=["arn:aws:iam::123:role/test"],
                    actions=["s3:GetObject"],
                    resources=["arn:aws:s3:::bucket/*"],
                )
            ]
        )
        self.assertTrue(policy.allows("arn:aws:iam::123:role/test", "s3:GetObject", "arn:aws:s3:::bucket/key"))


if __name__ == "__main__":
    unittest.main()
