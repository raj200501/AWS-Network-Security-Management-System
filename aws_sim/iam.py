"""IAM policy simulator.

Supports basic allow/deny evaluation for actions and resources. This is not a
full IAM engine but provides enough behavior for local testing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PolicyStatement:
    effect: str
    actions: List[str]
    resources: List[str]


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str


class IamPolicy:
    def __init__(self, statements: List[PolicyStatement]) -> None:
        self.statements = statements

    def evaluate(self, action: str, resource: str) -> PolicyDecision:
        explicit_deny = False
        for statement in self.statements:
            if not _matches(statement.actions, action):
                continue
            if not _matches(statement.resources, resource):
                continue
            if statement.effect.lower() == "deny":
                explicit_deny = True
            if statement.effect.lower() == "allow":
                if explicit_deny:
                    return PolicyDecision(False, "Explicit deny overrides allow")
                return PolicyDecision(True, "Allowed by matching statement")
        if explicit_deny:
            return PolicyDecision(False, "Explicit deny")
        return PolicyDecision(False, "No matching allow")


@dataclass
class IamRole:
    name: str
    policies: List[IamPolicy]

    def authorize(self, action: str, resource: str) -> PolicyDecision:
        decisions = [policy.evaluate(action, resource) for policy in self.policies]
        if any(decision.allowed for decision in decisions):
            return PolicyDecision(True, "Allowed by role policy")
        return PolicyDecision(False, "No policy allowed the action")


def _matches(patterns: List[str], value: str) -> bool:
    return any(_match(pattern, value) for pattern in patterns)


def _match(pattern: str, value: str) -> bool:
    if pattern == "*":
        return True
    if pattern.endswith("*"):
        return value.startswith(pattern[:-1])
    return pattern == value
