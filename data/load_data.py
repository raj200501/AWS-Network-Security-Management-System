"""Load log data for NSMS."""

from pathlib import Path

from nsms.data import load_logs


if __name__ == "__main__":
    records = load_logs(Path("data/sample_logs.csv"))
    print(f"Loaded {len(records)} records")
