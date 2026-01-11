"""Local anomaly detection helpers."""

from __future__ import annotations

from pathlib import Path

from nsms.model_io import load_model
from nsms.preprocessing import extract_features
from nsms.data import load_logs


def detect_anomalies(log_path: str, model_path: str) -> list[bool]:
    """Load logs and detect anomalies using the saved model."""

    model = load_model(Path(model_path))
    records = load_logs(Path(log_path))
    features = extract_features(records)
    return model.predict(features)


if __name__ == "__main__":
    from nsms.config import Config

    config = Config.load()
    model = load_model(config.model_path)
    records = load_logs(config.data_path)
    features = extract_features(records)
    results = model.predict(features)
    print(f"Detected {sum(1 for flag in results if flag)} anomalies")
