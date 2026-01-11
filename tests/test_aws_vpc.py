import unittest

from aws_sim.vpc import VpcService, Subnet, SecurityGroup, SecurityGroupRule, RouteTable, Route


class TestVpc(unittest.TestCase):
    def test_create_vpc_and_subnet(self):
        service = VpcService()
        vpc = service.create_vpc("10.0.0.0/16")
        subnet = Subnet(subnet_id="subnet-1", cidr_block="10.0.1.0/24", availability_zone="us-east-1a")
        vpc.add_subnet(subnet)
        sg = SecurityGroup(group_id="sg-1", name="web", description="web")
        sg.authorize_ingress(SecurityGroupRule(protocol="tcp", port_range="80", cidr="0.0.0.0/0", description="http"))
        vpc.add_security_group(sg)
        rt = RouteTable(table_id="rt-1")
        rt.add_route(Route(destination="0.0.0.0/0", target="igw-1"))
        vpc.add_route_table(rt)
        self.assertEqual(len(vpc.subnets), 1)
        self.assertEqual(len(vpc.security_groups), 1)


if __name__ == "__main__":
    unittest.main()
