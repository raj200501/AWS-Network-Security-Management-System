"""AWS Config rule evaluator simulator.

The evaluator checks resource configurations against rule definitions. Each rule
returns COMPLIANT or NON_COMPLIANT along with optional annotations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class ConfigRule:
    rule_name: str
    description: str
    resource_type: str
    required_tags: Dict[str, str]
    allowed_regions: List[str]


@dataclass(frozen=True)
class ConfigEvaluation:
    rule_name: str
    resource_id: str
    compliance_type: str
    annotation: str


class ConfigEvaluator:
    """Evaluate resources against config rules."""

    def __init__(self, rules: List[ConfigRule]) -> None:
        self.rules = rules

    def evaluate(self, resource: Dict[str, object]) -> List[ConfigEvaluation]:
        evaluations: List[ConfigEvaluation] = []
        for rule in self.rules:
            if resource.get("resource_type") != rule.resource_type:
                continue
            evaluation = self._evaluate_rule(rule, resource)
            evaluations.append(evaluation)
        return evaluations

    def _evaluate_rule(self, rule: ConfigRule, resource: Dict[str, object]) -> ConfigEvaluation:
        resource_id = str(resource.get("resource_id"))
        tags = resource.get("tags", {})
        region = resource.get("region", "unknown")

        missing_tags = [
            key for key, value in rule.required_tags.items() if tags.get(key) != value
        ]
        if missing_tags:
            return ConfigEvaluation(
                rule_name=rule.rule_name,
                resource_id=resource_id,
                compliance_type="NON_COMPLIANT",
                annotation=f"Missing required tags: {', '.join(missing_tags)}",
            )
        if region not in rule.allowed_regions:
            return ConfigEvaluation(
                rule_name=rule.rule_name,
                resource_id=resource_id,
                compliance_type="NON_COMPLIANT",
                annotation=f"Region {region} is not allowed",
            )
        return ConfigEvaluation(
            rule_name=rule.rule_name,
            resource_id=resource_id,
            compliance_type="COMPLIANT",
            annotation="Resource is compliant",
        )
