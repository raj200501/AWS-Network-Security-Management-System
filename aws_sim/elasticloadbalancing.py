"""Elastic Load Balancing simulator.

Models application load balancers with listeners and target groups.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass(frozen=True)
class Target:
    target_id: str
    port: int
    healthy: bool


@dataclass
class TargetGroup:
    target_group_arn: str
    protocol: str
    port: int
    targets: List[Target] = field(default_factory=list)

    def register_target(self, target: Target) -> None:
        self.targets.append(target)

    def healthy_targets(self) -> List[Target]:
        return [target for target in self.targets if target.healthy]


@dataclass
class Listener:
    listener_arn: str
    protocol: str
    port: int
    default_target_group_arn: str


@dataclass
class LoadBalancer:
    load_balancer_arn: str
    name: str
    scheme: str
    created_at: datetime
    listeners: Dict[str, Listener] = field(default_factory=dict)
    target_groups: Dict[str, TargetGroup] = field(default_factory=dict)


class ElbService:
    def __init__(self) -> None:
        self._load_balancers: Dict[str, LoadBalancer] = {}
        self._counter = 0

    def create_load_balancer(self, name: str, scheme: str = "internet-facing") -> LoadBalancer:
        self._counter += 1
        lb = LoadBalancer(
            load_balancer_arn=f"arn:aws:elbv2::loadbalancer/{self._counter:04d}",
            name=name,
            scheme=scheme,
            created_at=datetime.utcnow(),
        )
        self._load_balancers[lb.load_balancer_arn] = lb
        return lb

    def create_target_group(self, load_balancer_arn: str, protocol: str, port: int) -> TargetGroup:
        lb = self._load_balancers.get(load_balancer_arn)
        if lb is None:
            raise KeyError("Load balancer not found")
        self._counter += 1
        tg = TargetGroup(target_group_arn=f"arn:aws:elbv2::targetgroup/{self._counter:04d}", protocol=protocol, port=port)
        lb.target_groups[tg.target_group_arn] = tg
        return tg

    def create_listener(self, load_balancer_arn: str, protocol: str, port: int, target_group_arn: str) -> Listener:
        lb = self._load_balancers.get(load_balancer_arn)
        if lb is None:
            raise KeyError("Load balancer not found")
        self._counter += 1
        listener = Listener(
            listener_arn=f"arn:aws:elbv2::listener/{self._counter:04d}",
            protocol=protocol,
            port=port,
            default_target_group_arn=target_group_arn,
        )
        lb.listeners[listener.listener_arn] = listener
        return listener

    def list_load_balancers(self) -> List[LoadBalancer]:
        return list(self._load_balancers.values())
