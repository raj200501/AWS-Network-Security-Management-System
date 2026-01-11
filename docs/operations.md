# NSMS Operations Notes

This document captures operational conventions for local NSMS usage.
It is intended for release and build engineers responsible for maintaining
reproducible behavior.

## Directory Conventions

- `config/` contains configuration JSON files.
- `data/` contains sample data and feeds.
- `models/` contains generated model artifacts (ignored by git).
- `outputs/` contains run outputs (ignored by git).
- `scripts/` contains run and verification entrypoints.

## Versioning

- Source-controlled data files should remain deterministic.
- Generated artifacts (`models/anomaly_model.json`, `outputs/*`) should not be
  committed to git.
- Changes to the data schema should be reflected in `docs/data_dictionary.md`.

## Logging Behavior

- Logs are written to stdout and `outputs/nsms.log`.
- Log severity is INFO by default.
- Validation warnings are logged but do not stop the pipeline.

## Performance Expectations

- The simulator is designed for rapid execution (<1 second on modern hardware).
- The sample dataset is intentionally modest to keep CI fast.
- Execution time can be tuned by adjusting `data/sample_logs.csv` size.

## Release Checklist

1. Run `./scripts/verify.sh` locally.
2. Confirm `README.md` reflects actual behavior.
3. Ensure `docs/verification.md` reflects any changes to the pipeline.
4. Confirm `data/sample_logs.csv` is deterministic and meaningful.
5. Validate that `.github/workflows/ci.yml` is up to date.

## Known Limitations

- No external dependencies are installed by default.
- No network calls are made during runtime.
- The simulator is not meant to be production-grade.

## Extension Ideas

- Add a lightweight UI to visualize `summary.md`.
- Introduce JSON log ingestion and schema validation.
- Provide a replay mechanism for historical incidents.
- Add export of metrics in Prometheus format.

