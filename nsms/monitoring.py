"""Orchestrate the NSMS pipeline."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import List

from nsms.compliance import ComplianceChecker
from nsms.config import Config
from nsms.data import LogRecord, load_logs
from nsms.incident import create_incident
from nsms.logging_utils import get_logger
from nsms.metrics import compute_metrics
from nsms.model import AnomalyModel
from nsms.model_io import load_model, save_model
from nsms.preprocessing import extract_features
from nsms.reporting import build_report, write_report
from nsms.retention import enforce_retention
from nsms.threat_intel import ThreatIntelStore, ThreatIndicator


logger = get_logger("monitoring")


def train_model(config: Config) -> AnomalyModel:
    records = load_logs(config.data_path)
    features = extract_features(records)
    model = AnomalyModel.train(features, threshold=config.anomaly_threshold)
    save_model(model, config.model_path)
    logger.info("Saved model to %s", config.model_path)
    return model


def run_pipeline(config: Config, model: AnomalyModel | None = None) -> Path:
    """Run the full monitoring pipeline and write outputs to disk."""

    config.ensure_output_dir()
    model = model or load_model(config.model_path)
    records = load_logs(config.data_path)
    features = extract_features(records)
    anomalies = model.predict(features)

    threat_store = ThreatIntelStore.load(config.threat_intel_path)
    threat_hits: List[bool] = []
    threat_indicators: List[ThreatIndicator] = []
    compliance_checker = ComplianceChecker.load(config.compliance_rules_path)
    compliance_hits: List[bool] = []

    alerts_path = config.output_dir / "alerts.jsonl"
    incidents_path = config.output_dir / "incidents.jsonl"

    with alerts_path.open("w", encoding="utf-8") as alerts_handle, incidents_path.open(
        "w", encoding="utf-8"
    ) as incidents_handle:
        for idx, record in enumerate(records):
            indicator = threat_store.check_ip(record.source_ip)
            threat_hit = indicator is not None
            threat_hits.append(threat_hit)
            if indicator:
                threat_indicators.append(indicator)
            violations = compliance_checker.evaluate(record)
            compliance_hit = bool(violations)
            compliance_hits.append(compliance_hit)

            alert = {
                "record_index": idx,
                "timestamp": record.timestamp.isoformat(),
                "source_ip": record.source_ip,
                "destination_ip": record.destination_ip,
                "anomaly": anomalies[idx],
                "threat_intel_hit": threat_hit,
                "compliance_violations": violations,
            }
            alerts_handle.write(json.dumps(alert) + "\n")

            if anomalies[idx] or threat_hit or compliance_hit:
                severity = _severity_for_record(anomalies[idx], threat_hit, compliance_hit)
                incident = create_incident(
                    incident_id=f"INC-{idx:04d}",
                    severity=severity,
                    description=_incident_description(record, indicator, violations),
                )
                incidents_handle.write(json.dumps(_incident_payload(incident)) + "\n")

    metrics = compute_metrics(records, anomalies, threat_hits, compliance_hits)
    metrics_path = config.output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics.as_dict(), indent=2))

    summary_path = config.output_dir / "run_summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "total_records": len(records),
                "alerts": sum(1 for flag in anomalies if flag),
                "threat_intel_hits": sum(1 for flag in threat_hits if flag),
                "compliance_violations": sum(1 for flag in compliance_hits if flag),
            },
            indent=2,
        )
    )

    report = build_report(records, metrics, threat_indicators[:5], sum(1 for flag in compliance_hits if flag))
    write_report(config.output_dir / "summary.md", report)

    enforce_retention(config.output_dir, config.retention_days)

    logger.info("Pipeline complete. Outputs written to %s", config.output_dir)
    return config.output_dir


def _severity_for_record(anomaly: bool, threat_hit: bool, compliance_hit: bool) -> str:
    if threat_hit and anomaly:
        return "critical"
    if threat_hit or compliance_hit:
        return "high"
    if anomaly:
        return "medium"
    return "low"


def _incident_description(
    record: LogRecord, indicator: ThreatIndicator | None, violations: List[str]
) -> str:
    parts = [
        f"Source {record.source_ip} to {record.destination_ip}",
        f"protocol {record.protocol}",
        f"action {record.action}",
    ]
    if indicator is not None:
        parts.append("matched threat intelligence")
    if violations:
        parts.append(f"violated compliance rules {', '.join(violations)}")
    return "; ".join(parts)


def _incident_payload(incident: object) -> dict:
    payload = asdict(incident)
    payload["created_at"] = payload["created_at"].isoformat()
    return payload
