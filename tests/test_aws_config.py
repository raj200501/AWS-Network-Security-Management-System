import unittest

from aws_sim.config_rules import ConfigRule, ConfigEvaluator


class TestConfigEvaluator(unittest.TestCase):
    def test_rule_compliance(self):
        rule = ConfigRule(
            rule_name="required-tags",
            description="Must include owner tag",
            resource_type="ec2",
            required_tags={"owner": "security"},
            allowed_regions=["us-east-1"],
        )
        evaluator = ConfigEvaluator([rule])
        evaluations = evaluator.evaluate(
            {
                "resource_id": "i-123",
                "resource_type": "ec2",
                "region": "us-east-1",
                "tags": {"owner": "security"},
            }
        )
        self.assertEqual(evaluations[0].compliance_type, "COMPLIANT")


if __name__ == "__main__":
    unittest.main()
