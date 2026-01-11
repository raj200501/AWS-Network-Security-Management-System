"""Local setup script for NSMS.

This script creates required directories and validates configuration files.
"""

from pathlib import Path

from nsms.config import Config
from nsms.threat_intel import ThreatIntelStore
from nsms.compliance import ComplianceChecker


if __name__ == "__main__":
    config = Config.load()
    config.ensure_output_dir()
    ThreatIntelStore.load(config.threat_intel_path)
    ComplianceChecker.load(config.compliance_rules_path)
    print("Local NSMS infrastructure validated")
