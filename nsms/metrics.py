"""Metrics generation for NSMS runs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from nsms.data import LogRecord


@dataclass(frozen=True)
class Metrics:
    total_records: int
    anomalous_records: int
    threat_intel_hits: int
    compliance_violations: int

    def as_dict(self) -> Dict[str, int]:
        return {
            "total_records": self.total_records,
            "anomalous_records": self.anomalous_records,
            "threat_intel_hits": self.threat_intel_hits,
            "compliance_violations": self.compliance_violations,
        }


def compute_metrics(
    records: List[LogRecord],
    anomalies: List[bool],
    threat_hits: List[bool],
    compliance_hits: List[bool],
) -> Metrics:
    return Metrics(
        total_records=len(records),
        anomalous_records=sum(1 for flag in anomalies if flag),
        threat_intel_hits=sum(1 for flag in threat_hits if flag),
        compliance_violations=sum(1 for flag in compliance_hits if flag),
    )
