"""Resource policy simulator for S3 and other services."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ResourcePolicyStatement:
    effect: str
    principals: List[str]
    actions: List[str]
    resources: List[str]


class ResourcePolicy:
    def __init__(self, statements: List[ResourcePolicyStatement]) -> None:
        self.statements = statements

    def allows(self, principal: str, action: str, resource: str) -> bool:
        explicit_deny = False
        for statement in self.statements:
            if principal not in statement.principals and "*" not in statement.principals:
                continue
            if not _match_any(statement.actions, action):
                continue
            if not _match_any(statement.resources, resource):
                continue
            if statement.effect.lower() == "deny":
                explicit_deny = True
            if statement.effect.lower() == "allow":
                if explicit_deny:
                    return False
                return True
        return False


def _match_any(patterns: List[str], value: str) -> bool:
    return any(_match(pattern, value) for pattern in patterns)


def _match(pattern: str, value: str) -> bool:
    if pattern == "*":
        return True
    if pattern.endswith("*"):
        return value.startswith(pattern[:-1])
    return pattern == value
