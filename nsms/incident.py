"""Incident response orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

from nsms.logging_utils import get_logger


logger = get_logger("incident")


@dataclass(frozen=True)
class Incident:
    incident_id: str
    severity: str
    description: str
    created_at: datetime
    remediation_steps: List[str]


def create_incident(incident_id: str, severity: str, description: str) -> Incident:
    steps = _remediation_steps_for_severity(severity)
    incident = Incident(
        incident_id=incident_id,
        severity=severity,
        description=description,
        created_at=datetime.utcnow(),
        remediation_steps=steps,
    )
    logger.warning("Created incident %s with severity %s", incident_id, severity)
    return incident


def _remediation_steps_for_severity(severity: str) -> List[str]:
    if severity == "critical":
        return [
            "Isolate affected host",
            "Rotate credentials",
            "Notify on-call security engineer",
            "Open ticket with high priority",
        ]
    if severity == "high":
        return [
            "Throttle suspicious IP",
            "Notify security team",
            "Capture packet trace",
        ]
    if severity == "medium":
        return [
            "Review logs",
            "Notify system owner",
        ]
    return ["Document event", "Review during next audit"]
