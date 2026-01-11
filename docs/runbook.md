# NSMS Operator Runbook

This runbook describes operational workflows for the local NSMS simulator.
It is intended for maintainers who need to diagnose behavior or reproduce
outputs described in the README.

## Standard Operation

1. Train the model:
   ```bash
   python -m nsms.cli train
   ```
2. Run the pipeline:
   ```bash
   python -m nsms.cli run
   ```
3. Review output artifacts in `outputs/`.

## Expected Output Artifacts

- `alerts.jsonl`
  - Contains one line per log record.
  - Includes anomaly flags, threat intel matches, and compliance violations.
- `incidents.jsonl`
  - Contains one line per incident.
  - Each incident includes severity and remediation steps.
- `metrics.json`
  - Counters for the run.
- `run_summary.json`
  - Quick summary for debugging.
- `summary.md`
  - Human-readable report for operators.

## Known Good Output Examples

Use these invariants to confirm the pipeline is operating correctly:

- `metrics.json` must include `total_records > 0`.
- `metrics.json` must include `threat_intel_hits >= 1`.
- `metrics.json` must include `anomalous_records >= 1`.
- `alerts.jsonl` line count should equal `total_records`.
- `incidents.jsonl` should contain at least one incident.

These conditions are enforced by `scripts/smoke_test.py`.

## Troubleshooting

### Problem: `FileNotFoundError` for config or data

- Ensure you are running commands from the repository root.
- Confirm `config/default_config.json` exists.
- If using custom paths, verify environment overrides are correct.

### Problem: No incidents created

- Verify that `data/sample_logs.csv` contains denied or high-volume events.
- Check `data/threat_intel.json` includes IPs present in the log data.
- Ensure the model is trained before running the pipeline.

### Problem: Validation warnings

- Validation warnings are expected if a log record contains unusual data.
- Review log data and ensure timestamps are not in the future.
- Check for empty IP addresses or invalid status codes.

### Problem: CI failure

- Run `./scripts/verify.sh` locally.
- Inspect `outputs/summary.md` for an overview of pipeline outputs.

## Operational Checks

Run the following checks during debugging:

- Verify config:
  ```bash
  python -m nsms.cli show-config
  ```

- Inspect metrics:
  ```bash
  cat outputs/metrics.json
  ```

- Inspect the first five alerts:
  ```bash
  head -n 5 outputs/alerts.jsonl
  ```

- Inspect the first five incidents:
  ```bash
  head -n 5 outputs/incidents.jsonl
  ```

## Response Playbooks

### Critical Severity Incident

1. Isolate the host or IP in question.
2. Rotate credentials.
3. Notify the security on-call engineer.
4. Open a high-priority ticket.

### High Severity Incident

1. Throttle suspicious IPs.
2. Notify the security team.
3. Capture packet traces for analysis.

### Medium Severity Incident

1. Review log context.
2. Notify the system owner.
3. Capture timeline for future audit.

### Low Severity Incident

1. Document event.
2. Reassess during the next review.

## Maintenance

### Updating Sample Data

If you update `data/sample_logs.csv`:

- Re-run `python -m nsms.cli train`.
- Re-run `python -m nsms.cli run`.
- Confirm updated metrics and outputs.

### Updating Threat Intel

If you update `data/threat_intel.json`:

- No retraining is required.
- Re-run the pipeline to refresh alerts.

### Updating Compliance Rules

If you update `data/compliance_rules.json`:

- No retraining is required.
- Re-run the pipeline to refresh compliance violations.

## Appendix: Required Files

- `config/default_config.json`
- `data/sample_logs.csv`
- `data/threat_intel.json`
- `data/compliance_rules.json`

Each file is required for the pipeline to complete successfully.

