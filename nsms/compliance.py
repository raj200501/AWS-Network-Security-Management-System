"""Compliance checking logic."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from nsms.data import LogRecord
from nsms.logging_utils import get_logger


logger = get_logger("compliance")


@dataclass(frozen=True)
class ComplianceRule:
    rule_id: str
    description: str
    allowed_regions: List[str]
    allowed_protocols: List[str]
    high_risk_actions: List[str]

    @classmethod
    def from_mapping(cls, mapping: Dict[str, object]) -> "ComplianceRule":
        return cls(
            rule_id=mapping["rule_id"],
            description=mapping["description"],
            allowed_regions=list(mapping["allowed_regions"]),
            allowed_protocols=list(mapping["allowed_protocols"]),
            high_risk_actions=list(mapping["high_risk_actions"]),
        )


class ComplianceChecker:
    def __init__(self, rules: List[ComplianceRule]):
        self.rules = rules

    @classmethod
    def load(cls, path: Path) -> "ComplianceChecker":
        if not path.exists():
            raise FileNotFoundError(f"Compliance rules file not found: {path}")
        payload = json.loads(path.read_text())
        rules = [ComplianceRule.from_mapping(item) for item in payload["rules"]]
        logger.info("Loaded %s compliance rules", len(rules))
        return cls(rules)

    def evaluate(self, record: LogRecord) -> List[str]:
        """Return a list of violated rule IDs."""

        violations: List[str] = []
        for rule in self.rules:
            if record.region not in rule.allowed_regions:
                violations.append(rule.rule_id)
                continue
            if record.protocol not in rule.allowed_protocols:
                violations.append(rule.rule_id)
                continue
            if record.action in rule.high_risk_actions:
                violations.append(rule.rule_id)
        return violations
