"""VPC and networking simulator.

Models VPCs, subnets, route tables, and security groups to allow local tests
for network security configuration without AWS access.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from ipaddress import ip_network
from typing import Dict, List


@dataclass(frozen=True)
class SecurityGroupRule:
    protocol: str
    port_range: str
    cidr: str
    description: str


@dataclass
class SecurityGroup:
    group_id: str
    name: str
    description: str
    ingress: List[SecurityGroupRule] = field(default_factory=list)
    egress: List[SecurityGroupRule] = field(default_factory=list)

    def authorize_ingress(self, rule: SecurityGroupRule) -> None:
        self.ingress.append(rule)

    def authorize_egress(self, rule: SecurityGroupRule) -> None:
        self.egress.append(rule)


@dataclass(frozen=True)
class Route:
    destination: str
    target: str


@dataclass
class RouteTable:
    table_id: str
    routes: List[Route] = field(default_factory=list)

    def add_route(self, route: Route) -> None:
        self.routes.append(route)


@dataclass(frozen=True)
class Subnet:
    subnet_id: str
    cidr_block: str
    availability_zone: str


@dataclass
class Vpc:
    vpc_id: str
    cidr_block: str
    created_at: datetime
    subnets: Dict[str, Subnet] = field(default_factory=dict)
    route_tables: Dict[str, RouteTable] = field(default_factory=dict)
    security_groups: Dict[str, SecurityGroup] = field(default_factory=dict)

    def add_subnet(self, subnet: Subnet) -> None:
        self._validate_subnet(subnet)
        self.subnets[subnet.subnet_id] = subnet

    def add_route_table(self, route_table: RouteTable) -> None:
        self.route_tables[route_table.table_id] = route_table

    def add_security_group(self, group: SecurityGroup) -> None:
        self.security_groups[group.group_id] = group

    def _validate_subnet(self, subnet: Subnet) -> None:
        vpc_net = ip_network(self.cidr_block)
        subnet_net = ip_network(subnet.cidr_block)
        if not subnet_net.subnet_of(vpc_net):
            raise ValueError("Subnet CIDR must be within VPC CIDR")


class VpcService:
    """Manager for VPC resources."""

    def __init__(self) -> None:
        self._vpcs: Dict[str, Vpc] = {}
        self._counter = 0

    def create_vpc(self, cidr_block: str) -> Vpc:
        self._counter += 1
        vpc_id = f"vpc-{self._counter:04d}"
        vpc = Vpc(vpc_id=vpc_id, cidr_block=cidr_block, created_at=datetime.utcnow())
        self._vpcs[vpc_id] = vpc
        return vpc

    def get_vpc(self, vpc_id: str) -> Vpc:
        vpc = self._vpcs.get(vpc_id)
        if vpc is None:
            raise KeyError(f"VPC not found: {vpc_id}")
        return vpc

    def list_vpcs(self) -> List[Vpc]:
        return list(self._vpcs.values())
