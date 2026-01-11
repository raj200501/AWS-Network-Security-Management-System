"""Threat intelligence lookups for local runs."""

from __future__ import annotations

from pathlib import Path

from nsms.threat_intel import ThreatIntelStore


def check_threat_intelligence(ip_address: str, intel_path: str) -> bool:
    store = ThreatIntelStore.load(Path(intel_path))
    return store.check_ip(ip_address) is not None


if __name__ == "__main__":
    from nsms.config import Config

    config = Config.load()
    store = ThreatIntelStore.load(config.threat_intel_path)
    summary = store.summary()
    print("Threat intel summary:", summary)
