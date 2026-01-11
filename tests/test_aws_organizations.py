import unittest

from aws_sim.organizations import OrganizationsService


class TestOrganizations(unittest.TestCase):
    def test_create_account_and_ou(self):
        org = OrganizationsService()
        account = org.create_account("sec", "sec@example.com")
        ou = org.create_organizational_unit("Security")
        org.move_account(account.account_id, ou.ou_id)
        self.assertEqual(len(org.list_accounts()), 1)
        self.assertEqual(len(org.list_organizational_units()), 1)


if __name__ == "__main__":
    unittest.main()
