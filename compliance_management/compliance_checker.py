"""Run compliance checks on the dataset."""

from pathlib import Path

from nsms.compliance import ComplianceChecker
from nsms.data import load_logs


if __name__ == "__main__":
    checker = ComplianceChecker.load(Path("data/compliance_rules.json"))
    records = load_logs(Path("data/sample_logs.csv"))
    violations = sum(1 for record in records if checker.evaluate(record))
    print(f"Compliance violations: {violations}")
