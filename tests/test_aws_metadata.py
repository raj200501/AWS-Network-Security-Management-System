import unittest

from aws_sim.metadata import ResourceMetadata, ResourceTags
from datetime import datetime


class TestMetadata(unittest.TestCase):
    def test_merge_tags(self):
        tags = ResourceTags(tags={"env": "dev"})
        metadata = ResourceMetadata(
            resource_id="res-1",
            resource_type="s3",
            region="us-east-1",
            created_at=datetime.utcnow(),
            tags=tags,
        )
        updated = metadata.with_tags({"owner": "sec"})
        self.assertEqual(updated.tags.tags["owner"], "sec")


if __name__ == "__main__":
    unittest.main()
