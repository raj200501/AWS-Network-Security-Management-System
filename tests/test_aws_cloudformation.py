import unittest

from aws_sim.cloudformation import CloudFormationService, StackTemplate


class TestCloudFormation(unittest.TestCase):
    def test_create_stack(self):
        template = StackTemplate(description="test")
        template.add_resource("Bucket", "AWS::S3::Bucket", {"BucketName": "test"})
        template.add_output("BucketName", "test", "Bucket name")
        service = CloudFormationService()
        stack = service.create_stack("stack", template)
        self.assertEqual(len(stack.list_resources()), 1)
        self.assertEqual(len(stack.list_outputs()), 1)


if __name__ == "__main__":
    unittest.main()
