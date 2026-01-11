"""Generate human-readable reports for NSMS runs."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from nsms.data import LogRecord
from nsms.metrics import Metrics
from nsms.threat_intel import ThreatIndicator


@dataclass(frozen=True)
class ReportSection:
    title: str
    lines: List[str]

    def render(self) -> str:
        underline = "-" * len(self.title)
        return "\n".join([self.title, underline, *self.lines, ""])


def build_report(
    records: Iterable[LogRecord],
    metrics: Metrics,
    top_threats: Iterable[ThreatIndicator],
    compliance_violations: int,
) -> str:
    sections = [
        _summary_section(metrics),
        _threats_section(list(top_threats)),
        _compliance_section(compliance_violations),
        _records_section(list(records)),
    ]
    return "\n".join(section.render() for section in sections).strip() + "\n"


def write_report(path: Path, report: str) -> None:
    path.write_text(report, encoding="utf-8")


def _summary_section(metrics: Metrics) -> ReportSection:
    return ReportSection(
        title="Run Summary",
        lines=[
            f"Total records processed: {metrics.total_records}",
            f"Anomalies detected: {metrics.anomalous_records}",
            f"Threat intel matches: {metrics.threat_intel_hits}",
            f"Compliance violations: {metrics.compliance_violations}",
        ],
    )


def _threats_section(threats: List[ThreatIndicator]) -> ReportSection:
    if not threats:
        lines = ["No threat intelligence matches detected."]
    else:
        lines = [
            f"{indicator.ip_address} ({indicator.severity}) - {indicator.description}"
            for indicator in threats
        ]
    return ReportSection(title="Threat Intelligence", lines=lines)


def _compliance_section(violations: int) -> ReportSection:
    lines = [
        f"Total compliance violations: {violations}",
        "Review incidents.jsonl for per-record details.",
    ]
    return ReportSection(title="Compliance", lines=lines)


def _records_section(records: List[LogRecord]) -> ReportSection:
    sample = records[:5]
    lines = [
        json.dumps(
            {
                "timestamp": record.timestamp.isoformat(),
                "source_ip": record.source_ip,
                "destination_ip": record.destination_ip,
                "protocol": record.protocol,
                "bytes": record.bytes_transferred,
                "action": record.action,
                "status": record.status,
            },
            indent=2,
        )
        for record in sample
    ]
    lines.append("...")
    return ReportSection(title="Sample Records", lines=lines)
