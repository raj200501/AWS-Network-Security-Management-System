"""Threat intelligence store and lookup."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from nsms.logging_utils import get_logger


logger = get_logger("threat_intel")


@dataclass(frozen=True)
class ThreatIndicator:
    ip_address: str
    severity: str
    description: str


class ThreatIntelStore:
    """Simple JSON-backed threat intelligence store."""

    def __init__(self, indicators: List[ThreatIndicator]) -> None:
        self._indicators = indicators
        self._by_ip = {indicator.ip_address: indicator for indicator in indicators}

    @classmethod
    def load(cls, path: Path) -> "ThreatIntelStore":
        if not path.exists():
            raise FileNotFoundError(f"Threat intel file not found: {path}")
        payload = json.loads(path.read_text())
        indicators = [
            ThreatIndicator(
                ip_address=item["ip_address"],
                severity=item["severity"],
                description=item["description"],
            )
            for item in payload["indicators"]
        ]
        logger.info("Loaded %s threat indicators", len(indicators))
        return cls(indicators)

    def check_ip(self, ip_address: str) -> ThreatIndicator | None:
        return self._by_ip.get(ip_address)

    def summary(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for indicator in self._indicators:
            counts[indicator.severity] = counts.get(indicator.severity, 0) + 1
        return counts
