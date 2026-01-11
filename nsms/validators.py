"""Validation helpers for NSMS inputs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List, TYPE_CHECKING

from nsms.logging_utils import get_logger

if TYPE_CHECKING:
    from nsms.data import LogRecord


logger = get_logger("validators")


@dataclass(frozen=True)
class ValidationIssue:
    record_index: int
    message: str


def validate_records(records: Iterable["LogRecord"]) -> List[ValidationIssue]:
    """Validate log records and return a list of issues."""

    issues: List[ValidationIssue] = []
    for idx, record in enumerate(records):
        if record.bytes_transferred < 0:
            issues.append(ValidationIssue(idx, "Bytes transferred cannot be negative"))
        if not record.source_ip:
            issues.append(ValidationIssue(idx, "Missing source IP"))
        if not record.destination_ip:
            issues.append(ValidationIssue(idx, "Missing destination IP"))
        if record.timestamp > datetime.utcnow():
            issues.append(ValidationIssue(idx, "Timestamp is in the future"))
        if record.status.upper() not in {"OK", "DENIED", "ERROR"}:
            issues.append(ValidationIssue(idx, "Unknown status"))
    if issues:
        logger.warning("Validation found %s issues", len(issues))
    return issues
