"""Smoke test for NSMS pipeline outputs."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    output_dir = Path("outputs")
    alerts_path = output_dir / "alerts.jsonl"
    incidents_path = output_dir / "incidents.jsonl"
    metrics_path = output_dir / "metrics.json"
    summary_path = output_dir / "summary.md"

    for path in (alerts_path, incidents_path, metrics_path, summary_path):
        if not path.exists():
            raise SystemExit(f"Missing expected output: {path}")

    metrics = json.loads(metrics_path.read_text())
    if metrics["total_records"] <= 0:
        raise SystemExit("Expected records to be processed")
    if metrics["threat_intel_hits"] < 1:
        raise SystemExit("Expected at least one threat intel hit")
    if metrics["anomalous_records"] < 1:
        raise SystemExit("Expected at least one anomaly")

    alert_lines = alerts_path.read_text().strip().splitlines()
    if len(alert_lines) != metrics["total_records"]:
        raise SystemExit("Alert count does not match total records")

    incident_lines = incidents_path.read_text().strip().splitlines()
    if len(incident_lines) < 1:
        raise SystemExit("Expected at least one incident")

    if "Run Summary" not in summary_path.read_text():
        raise SystemExit("Summary report missing Run Summary section")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
