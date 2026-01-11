"""Aggregate logs for NSMS."""

from pathlib import Path

from nsms.data import load_logs, summarize_protocols


if __name__ == "__main__":
    records = load_logs(Path("data/sample_logs.csv"))
    summary = summarize_protocols(records)
    print("Protocol summary:", summary)
