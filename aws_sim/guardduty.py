"""GuardDuty finding simulator.

Provides a minimal set of operations to create and query findings. It is meant
for deterministic unit testing and local demos of AWS-like threat detection.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass(frozen=True)
class GuardDutyFinding:
    finding_id: str
    detector_id: str
    finding_type: str
    severity: float
    description: str
    resource: Dict[str, str]
    created_at: datetime
    updated_at: datetime


class GuardDutyDetector:
    """In-memory GuardDuty detector with findings and filters."""

    def __init__(self, detector_id: str) -> None:
        self.detector_id = detector_id
        self._findings: Dict[str, GuardDutyFinding] = {}
        self._counter = 0
        self._filters: Dict[str, Dict[str, str]] = {}

    def create_finding(
        self,
        finding_type: str,
        severity: float,
        description: str,
        resource: Dict[str, str],
    ) -> GuardDutyFinding:
        self._counter += 1
        finding_id = f"finding-{self._counter:06d}"
        now = datetime.utcnow()
        finding = GuardDutyFinding(
            finding_id=finding_id,
            detector_id=self.detector_id,
            finding_type=finding_type,
            severity=severity,
            description=description,
            resource=resource,
            created_at=now,
            updated_at=now,
        )
        self._findings[finding_id] = finding
        return finding

    def update_finding(self, finding_id: str, severity: Optional[float] = None) -> GuardDutyFinding:
        finding = self._findings.get(finding_id)
        if finding is None:
            raise KeyError(f"Finding not found: {finding_id}")
        new_severity = severity if severity is not None else finding.severity
        updated = GuardDutyFinding(
            finding_id=finding.finding_id,
            detector_id=finding.detector_id,
            finding_type=finding.finding_type,
            severity=new_severity,
            description=finding.description,
            resource=finding.resource,
            created_at=finding.created_at,
            updated_at=datetime.utcnow(),
        )
        self._findings[finding_id] = updated
        return updated

    def list_findings(self) -> List[GuardDutyFinding]:
        return list(self._findings.values())

    def get_finding(self, finding_id: str) -> Optional[GuardDutyFinding]:
        return self._findings.get(finding_id)

    def create_filter(self, name: str, criteria: Dict[str, str]) -> None:
        self._filters[name] = dict(criteria)

    def match_filter(self, name: str) -> List[GuardDutyFinding]:
        criteria = self._filters.get(name)
        if criteria is None:
            raise KeyError(f"Filter not found: {name}")
        results = []
        for finding in self._findings.values():
            if _matches_criteria(finding, criteria):
                results.append(finding)
        return results


def _matches_criteria(finding: GuardDutyFinding, criteria: Dict[str, str]) -> bool:
    for key, value in criteria.items():
        if key == "finding_type" and finding.finding_type != value:
            return False
        if key == "severity" and str(finding.severity) != value:
            return False
        if key.startswith("resource."):
            resource_key = key.split("resource.", 1)[1]
            if finding.resource.get(resource_key) != value:
                return False
    return True
