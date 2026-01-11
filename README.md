# Comprehensive Network Security Management System (Local Simulator)

This repository provides a **local, fully reproducible** network security management simulator inspired by AWS security workflows. It includes:

- Real-time monitoring pipeline (local log stream simulation)
- Statistical anomaly detection
- Threat intelligence lookups
- Incident response orchestration
- Compliance evaluation
- Log aggregation and metrics

> Note: This repo is intentionally runnable without AWS access. AWS services are simulated locally with deterministic data and outputs.

---

## Features

- **Real-Time Monitoring**: Processes local CSV logs to simulate streaming security events.
- **Anomaly Detection**: Trains a statistical model to detect outliers and suspicious patterns.
- **Threat Intelligence**: Matches known bad IPs from a local JSON feed.
- **Incident Response**: Creates incidents with severity and remediation steps.
- **Compliance Management**: Validates traffic against policy rules and flags violations.
- **Logging & Metrics**: Writes alerts, incidents, and metrics to the `outputs/` directory.

---

## Getting Started

### Prerequisites

- Python 3.11+ (3.8+ works for local usage, CI uses 3.11)

### Setup

No external Python dependencies are required for the local simulator. (A `requirements.txt` file is included for clarity, but it is intentionally empty.)

### Train the anomaly model

```bash
python -m nsms.cli train
```

### Run the pipeline

```bash
python -m nsms.cli run
```

Outputs are written to `outputs/`:

- `alerts.jsonl` — every log record enriched with detections
- `incidents.jsonl` — incidents raised for anomalies/threat intel/compliance
- `metrics.json` — counters for the run
- `run_summary.json` — quick summary for the run
- `summary.md` — human-readable summary report

### Convenience script

```bash
./scripts/run.sh
```

---

## Configuration

Configuration lives in `config/default_config.json`. You can override specific fields with environment variables:

```bash
cp .env.example .env
# Edit values as needed
```

Supported overrides:

- `NSMS_DATA_PATH`
- `NSMS_THREAT_INTEL_PATH`
- `NSMS_COMPLIANCE_RULES_PATH`
- `NSMS_MODEL_PATH`
- `NSMS_OUTPUT_DIR`
- `NSMS_ANOMALY_THRESHOLD`
- `NSMS_RETENTION_DAYS`

---

## Verified Quickstart (exact commands run)

```bash
python -m nsms.cli train
python -m nsms.cli run
```

---

## Verified Verification (CI command)

```bash
./scripts/verify.sh
```

The verification script:

1. Trains the anomaly model.
2. Runs the pipeline to generate outputs.
3. Executes unit tests.
4. Executes a smoke test that validates alerts, incidents, and metrics.

---

## Troubleshooting

- **Missing outputs**: Ensure you ran `python -m nsms.cli run` or `./scripts/run.sh`.
- **Configuration errors**: Verify paths in `config/default_config.json` exist or override via `.env`.
- **No anomalies detected**: Ensure `data/sample_logs.csv` contains high-volume or denied events.

---

## Project Layout

- `nsms/` — core library and CLI
- `data/` — sample logs and JSON feeds
- `scripts/` — run and verification scripts
- `tests/` — unit/integration tests
- `outputs/` — generated artifacts (ignored by git)

---

## License

This project is licensed under the MIT License.
