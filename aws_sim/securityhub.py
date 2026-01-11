"""Security Hub aggregation simulator.

Aggregates findings from multiple sources (e.g., GuardDuty, Inspector) into a
single view and supports basic filtering.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass(frozen=True)
class SecurityHubFinding:
    finding_id: str
    source: str
    product_arn: str
    title: str
    description: str
    severity: str
    resource: Dict[str, str]
    created_at: datetime


class SecurityHub:
    """In-memory Security Hub aggregator."""

    def __init__(self, account_id: str, region: str) -> None:
        self.account_id = account_id
        self.region = region
        self._findings: Dict[str, SecurityHubFinding] = {}
        self._counter = 0

    def ingest_finding(
        self,
        source: str,
        title: str,
        description: str,
        severity: str,
        resource: Dict[str, str],
    ) -> SecurityHubFinding:
        self._counter += 1
        finding_id = f"sh-finding-{self._counter:06d}"
        finding = SecurityHubFinding(
            finding_id=finding_id,
            source=source,
            product_arn=f"arn:aws:securityhub:{self.region}:{self.account_id}:product/{source}",
            title=title,
            description=description,
            severity=severity,
            resource=resource,
            created_at=datetime.utcnow(),
        )
        self._findings[finding_id] = finding
        return finding

    def list_findings(self, severity: Optional[str] = None) -> List[SecurityHubFinding]:
        findings = list(self._findings.values())
        if severity:
            return [finding for finding in findings if finding.severity == severity]
        return findings

    def summarize_by_severity(self) -> Dict[str, int]:
        summary: Dict[str, int] = {}
        for finding in self._findings.values():
            summary[finding.severity] = summary.get(finding.severity, 0) + 1
        return summary
