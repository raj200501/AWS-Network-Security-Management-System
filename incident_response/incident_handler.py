"""Local incident handler for NSMS runs."""

from pathlib import Path

from nsms.incident import create_incident
from nsms.model_io import load_model
from nsms.preprocessing import extract_features
from nsms.data import load_logs


if __name__ == "__main__":
    model = load_model(Path("models/anomaly_model.json"))
    records = load_logs(Path("data/sample_logs.csv"))
    features = extract_features(records)
    anomalies = model.predict(features)
    for idx, is_anomaly in enumerate(anomalies):
        if is_anomaly:
            incident = create_incident(
                incident_id=f"INC-{idx:04d}",
                severity="medium",
                description="Anomalous traffic detected",
            )
            print(incident)
