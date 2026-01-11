# NSMS Architecture Overview

This document explains the internal architecture of the local NSMS simulator.
It is designed to be explicit so that new maintainers can follow the flow of
log ingestion, detection, incident creation, and reporting without relying on
external services.

## High-Level Flow

1. **Ingest**: CSV log events are loaded from `data/sample_logs.csv`.
2. **Validate**: Records are validated for schema and timestamp sanity.
3. **Feature Extraction**: Numeric features are derived from each record.
4. **Anomaly Detection**: A statistical model flags anomalous patterns.
5. **Threat Intelligence**: Source IPs are matched against the local feed.
6. **Compliance**: Policy rules are applied to each record.
7. **Incident Response**: Incidents are generated for flagged records.
8. **Reporting**: Metrics and summary reports are written to `outputs/`.

## Component Responsibilities

### Config

- Loads JSON config from `config/default_config.json`.
- Applies environment overrides from `.env` or shell variables.
- Validates critical paths so runtime errors fail fast.

### Data Loader

- Reads CSV logs with strict header expectations.
- Converts timestamps to `datetime` objects.
- Normalizes fields into the `LogRecord` dataclass.

### Validation

Validation focuses on deterministic, local checks:

- Future timestamps are flagged.
- Missing IPs or invalid statuses are flagged.
- Negative byte counts are rejected.

Validation warnings are logged but do not halt execution. This mirrors how a
real-world pipeline would proceed while still surfacing data quality issues.

### Feature Extraction

The simulator does not rely on external ML libraries. Features are intentionally
simple:

- Bytes transferred (float)
- Whether the record is denied
- Whether the resource contains a sensitive keyword
- Whether the user is an admin

### Anomaly Model

The statistical model calculates a mean and standard deviation for bytes
transferred, then applies heuristic penalties for denied requests, sensitive
resources, and admin users. This provides a reproducible and explainable signal
without external dependencies.

### Threat Intel

Threat intelligence is backed by a JSON file (`data/threat_intel.json`).
Indicators are keyed by IP address and include severity and descriptions.
The store provides:

- Lookup by IP address
- Severity distribution summary

### Compliance

Compliance rules are loaded from `data/compliance_rules.json`.
Each rule defines:

- Allowed regions
- Allowed protocols
- High-risk actions

A record violates a rule if it falls outside allowed values or triggers a
high-risk action.

### Incident Response

Incidents are created whenever a record is anomalous, a threat intel hit, or a
compliance violation. Severity mapping:

- **Critical**: anomaly + threat intel hit
- **High**: threat intel hit or compliance violation
- **Medium**: anomaly only
- **Low**: none (not persisted)

Remediation steps are predefined based on severity to keep the simulator
consistent and deterministic.

### Reporting

The pipeline generates:

- `alerts.jsonl` — every record and its detection outcomes
- `incidents.jsonl` — incidents with timestamps and remediation steps
- `metrics.json` — high-level counters
- `run_summary.json` — summary used for debugging and CI
- `summary.md` — human-readable summary for operators

### Retention

Retention is enforced on files in `outputs/` based on `retention_days`. This
simulates cleanup policies used in production systems.

## Extensibility Notes

The simulator is intentionally modular:

- Replace `AnomalyModel` with a real ML model if desired.
- Swap the log source to a streaming API (Kinesis, Kafka) if integrating with
  real infrastructure.
- Replace JSON threat intel with a live feed or DynamoDB-backed store.

## Operational Notes

- All operations are deterministic; there are no network calls.
- The pipeline is designed to run in CI using `scripts/verify.sh`.
- Outputs are overwritten on each run to keep behavior repeatable.

## Failure Modes and Mitigations

- **Missing config files**: The CLI fails fast with explicit error messages.
- **Bad log data**: Validation warnings are logged, but processing continues.
- **Missing model**: Use `python -m nsms.cli train` to create one.
- **No incidents**: Ensure sample data contains anomalies and threat intel hits.

## Future Enhancements

Potential extensions that maintain determinism:

- Add pluggable alert routing (email, Slack, local webhook).
- Support JSON log format in addition to CSV.
- Include additional metrics (latency percentiles, per-user rates).
- Add a small web UI to visualize `summary.md` and metrics.

