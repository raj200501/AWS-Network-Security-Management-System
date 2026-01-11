# Verification Guide

This guide documents how verification is performed and how it maps back to the
README contract. It is intended to make CI behavior transparent and reproducible.

## Canonical Verification Command

```bash
./scripts/verify.sh
```

The verification script must be used by CI and local development. It ensures
that core functionality executes correctly without network access.

## Verification Steps

1. **Train the anomaly model**
   - Executes `python -m nsms.cli train`.
   - Persists the model to `models/anomaly_model.json`.

2. **Run the monitoring pipeline**
   - Executes `python -m nsms.cli run`.
   - Produces `alerts.jsonl`, `incidents.jsonl`, `metrics.json`, `run_summary.json`, and `summary.md`.

3. **Unit tests**
   - Executes `python -m unittest discover -s tests`.
   - Covers configuration, model training, threat intel lookup, compliance rules,
     pipeline outputs, reporting, retention, and validation.

4. **Smoke test**
   - Executes `python scripts/smoke_test.py`.
   - Verifies that the output artifacts exist and contain expected values.

## Mapping to README Contract

| README Claim | Verification Coverage |
| --- | --- |
| Pipeline runs locally | `python -m nsms.cli run` in verify script |
| Anomaly detection works | Unit tests for `AnomalyModel` and smoke test metrics |
| Threat intel works | Unit tests for `ThreatIntelStore` and smoke test metrics |
| Incident response works | Pipeline generates `incidents.jsonl` |
| Compliance checks work | Unit tests and smoke test metrics |
| Outputs are generated | Smoke test checks presence and content |

## Determinism Guarantees

- No network calls are made during verification.
- All data sources are local files committed to the repo.
- Outputs are overwritten on each run for repeatability.

## Troubleshooting Failed Verification

- **Model file missing**: ensure `python -m nsms.cli train` succeeds.
- **Output files missing**: ensure `python -m nsms.cli run` succeeded.
- **Smoke test failure**: inspect `outputs/metrics.json` and `outputs/summary.md`.
- **Unit test failure**: run `python -m unittest discover -s tests -v` for details.

