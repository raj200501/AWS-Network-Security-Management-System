import unittest

from aws_sim.sts import StsService


class TestSts(unittest.TestCase):
    def test_assume_role(self):
        sts = StsService()
        creds = sts.assume_role("arn:aws:iam::123:role/test", "session")
        self.assertTrue(creds.access_key_id.startswith("ASIA"))


if __name__ == "__main__":
    unittest.main()
