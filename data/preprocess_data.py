"""Preprocess log data for NSMS."""

from pathlib import Path

from nsms.data import load_logs
from nsms.preprocessing import extract_features


if __name__ == "__main__":
    records = load_logs(Path("data/sample_logs.csv"))
    features = extract_features(records)
    print(f"Extracted {len(features)} feature vectors")
