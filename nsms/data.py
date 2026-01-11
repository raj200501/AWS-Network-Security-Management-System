"""Data loading and validation utilities."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Sequence

from nsms.logging_utils import get_logger
from nsms.validators import validate_records


logger = get_logger("data")


@dataclass(frozen=True)
class LogRecord:
    timestamp: datetime
    source_ip: str
    destination_ip: str
    protocol: str
    bytes_transferred: int
    action: str
    region: str
    user: str
    resource: str
    status: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "LogRecord":
        try:
            timestamp = datetime.fromisoformat(row["timestamp"])
        except ValueError as exc:
            raise ValueError(f"Invalid timestamp: {row.get('timestamp')}") from exc
        return cls(
            timestamp=timestamp,
            source_ip=row["source_ip"],
            destination_ip=row["destination_ip"],
            protocol=row["protocol"],
            bytes_transferred=int(row["bytes"]),
            action=row["action"],
            region=row["region"],
            user=row["user"],
            resource=row["resource"],
            status=row["status"],
        )


def load_logs(path: Path) -> List[LogRecord]:
    """Load logs from a CSV file."""

    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        records = [LogRecord.from_row(row) for row in reader]

    issues = validate_records(records)
    if issues:
        logger.warning("%s validation issues detected", len(issues))

    logger.info("Loaded %s log records", len(records))
    return records


def write_logs(path: Path, records: Sequence[LogRecord]) -> None:
    """Write logs back to CSV for reproducibility."""

    fieldnames = [
        "timestamp",
        "source_ip",
        "destination_ip",
        "protocol",
        "bytes",
        "action",
        "region",
        "user",
        "resource",
        "status",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "timestamp": record.timestamp.isoformat(),
                    "source_ip": record.source_ip,
                    "destination_ip": record.destination_ip,
                    "protocol": record.protocol,
                    "bytes": record.bytes_transferred,
                    "action": record.action,
                    "region": record.region,
                    "user": record.user,
                    "resource": record.resource,
                    "status": record.status,
                }
            )


def summarize_protocols(records: Iterable[LogRecord]) -> dict[str, int]:
    """Count logs by protocol."""

    counts: dict[str, int] = {}
    for record in records:
        counts[record.protocol] = counts.get(record.protocol, 0) + 1
    return counts
