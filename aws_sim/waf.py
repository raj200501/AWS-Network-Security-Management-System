"""AWS WAF rule simulator.

Provides a rule engine that can evaluate web requests against IP sets,
rate-based rules, and string match conditions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass(frozen=True)
class IpSet:
    name: str
    addresses: List[str]


@dataclass(frozen=True)
class StringMatchStatement:
    field: str
    pattern: str


@dataclass(frozen=True)
class RateBasedStatement:
    limit: int
    window_seconds: int


@dataclass
class WafRule:
    name: str
    priority: int
    action: str
    ip_set: IpSet | None = None
    string_match: StringMatchStatement | None = None
    rate_based: RateBasedStatement | None = None


@dataclass(frozen=True)
class WafRequest:
    ip: str
    uri: str
    method: str
    headers: Dict[str, str]
    timestamp: datetime


@dataclass(frozen=True)
class WafDecision:
    rule_name: str
    action: str
    reason: str


class WafWebAcl:
    """In-memory WAF Web ACL with ordered rules."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._rules: List[WafRule] = []
        self._request_log: List[WafRequest] = []

    def add_rule(self, rule: WafRule) -> None:
        self._rules.append(rule)
        self._rules.sort(key=lambda r: r.priority)

    def evaluate(self, request: WafRequest) -> WafDecision:
        self._request_log.append(request)
        for rule in self._rules:
            if self._matches_rule(rule, request):
                return WafDecision(rule_name=rule.name, action=rule.action, reason="Matched rule")
        return WafDecision(rule_name="default", action="ALLOW", reason="No rule matched")

    def _matches_rule(self, rule: WafRule, request: WafRequest) -> bool:
        if rule.ip_set and request.ip in rule.ip_set.addresses:
            return True
        if rule.string_match:
            field_value = _extract_field(request, rule.string_match.field)
            if rule.string_match.pattern in field_value:
                return True
        if rule.rate_based:
            return _rate_exceeded(self._request_log, request, rule.rate_based)
        return False


def _extract_field(request: WafRequest, field: str) -> str:
    if field == "uri":
        return request.uri
    if field == "method":
        return request.method
    if field.startswith("header:"):
        header = field.split(":", 1)[1]
        return request.headers.get(header, "")
    return ""


def _rate_exceeded(
    requests: List[WafRequest],
    current: WafRequest,
    rate_statement: RateBasedStatement,
) -> bool:
    window_start = current.timestamp.timestamp() - rate_statement.window_seconds
    recent = [
        req
        for req in requests
        if req.ip == current.ip and req.timestamp.timestamp() >= window_start
    ]
    return len(recent) > rate_statement.limit
