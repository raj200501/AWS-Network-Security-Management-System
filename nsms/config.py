"""Configuration loading and validation for the local NSMS runtime."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


DEFAULT_CONFIG_PATH = Path("config/default_config.json")


@dataclass(frozen=True)
class Config:
    """Runtime configuration for the NSMS pipeline.

    This configuration is intentionally explicit to make the README instructions
    reproducible. All paths are stored as ``Path`` objects and validated when
    loading the configuration.
    """

    data_path: Path
    threat_intel_path: Path
    compliance_rules_path: Path
    model_path: Path
    output_dir: Path
    anomaly_threshold: float = 3.0
    allowed_regions: List[str] = field(default_factory=list)
    allowed_protocols: List[str] = field(default_factory=list)
    high_risk_actions: List[str] = field(default_factory=list)
    retention_days: int = 30

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "Config":
        config_path = path or DEFAULT_CONFIG_PATH
        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}. "
                "Ensure config/default_config.json exists or pass --config."
            )
        raw = json.loads(config_path.read_text())
        env_overrides = _load_env_overrides()
        merged = {**raw, **env_overrides}
        return cls.from_mapping(merged)

    @classmethod
    def from_mapping(cls, mapping: Dict[str, object]) -> "Config":
        data_path = Path(str(mapping["data_path"]))
        threat_intel_path = Path(str(mapping["threat_intel_path"]))
        compliance_rules_path = Path(str(mapping["compliance_rules_path"]))
        model_path = Path(str(mapping["model_path"]))
        output_dir = Path(str(mapping["output_dir"]))
        anomaly_threshold = float(mapping.get("anomaly_threshold", 3.0))
        allowed_regions = list(mapping.get("allowed_regions", []))
        allowed_protocols = list(mapping.get("allowed_protocols", []))
        high_risk_actions = list(mapping.get("high_risk_actions", []))
        retention_days = int(mapping.get("retention_days", 30))

        config = cls(
            data_path=data_path,
            threat_intel_path=threat_intel_path,
            compliance_rules_path=compliance_rules_path,
            model_path=model_path,
            output_dir=output_dir,
            anomaly_threshold=anomaly_threshold,
            allowed_regions=allowed_regions,
            allowed_protocols=allowed_protocols,
            high_risk_actions=high_risk_actions,
            retention_days=retention_days,
        )
        config.validate()
        return config

    def validate(self) -> None:
        _ensure_exists(self.data_path, "data_path")
        _ensure_exists(self.threat_intel_path, "threat_intel_path")
        _ensure_exists(self.compliance_rules_path, "compliance_rules_path")
        if self.anomaly_threshold <= 0:
            raise ValueError("anomaly_threshold must be greater than 0")
        if self.retention_days <= 0:
            raise ValueError("retention_days must be greater than 0")

    def ensure_output_dir(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)


def _ensure_exists(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} does not exist: {path}")


def _load_env_overrides() -> Dict[str, object]:
    """Load optional overrides from environment variables.

    This is deliberately small-scope to keep the runtime deterministic.
    """

    overrides: Dict[str, object] = {}
    env_map = {
        "NSMS_DATA_PATH": "data_path",
        "NSMS_THREAT_INTEL_PATH": "threat_intel_path",
        "NSMS_COMPLIANCE_RULES_PATH": "compliance_rules_path",
        "NSMS_MODEL_PATH": "model_path",
        "NSMS_OUTPUT_DIR": "output_dir",
        "NSMS_ANOMALY_THRESHOLD": "anomaly_threshold",
        "NSMS_RETENTION_DAYS": "retention_days",
    }
    for env_key, config_key in env_map.items():
        value = os.getenv(env_key)
        if value is None:
            continue
        overrides[config_key] = value
    return overrides
