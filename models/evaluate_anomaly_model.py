"""Evaluate the anomaly model against the sample data."""

from nsms.config import Config
from nsms.data import load_logs
from nsms.model_io import load_model
from nsms.preprocessing import extract_features


if __name__ == "__main__":
    config = Config.load()
    model = load_model(config.model_path)
    records = load_logs(config.data_path)
    features = extract_features(records)
    predictions = model.predict(features)
    print(f"Anomalies flagged: {sum(1 for flag in predictions if flag)}")
