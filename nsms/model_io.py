"""Persist anomaly models to disk."""

from __future__ import annotations

import json
from pathlib import Path

from nsms.model import AnomalyModel, ModelStats


def save_model(model: AnomalyModel, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "threshold": model.threshold,
        "stats": {
            "mean_bytes": model.stats.mean_bytes,
            "std_bytes": model.stats.std_bytes,
            "mean_denied": model.stats.mean_denied,
            "mean_sensitive": model.stats.mean_sensitive,
            "mean_admin": model.stats.mean_admin,
        },
    }
    path.write_text(json.dumps(payload, indent=2))


def load_model(path: Path) -> AnomalyModel:
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")
    payload = json.loads(path.read_text())
    stats = payload["stats"]
    model_stats = ModelStats(
        mean_bytes=stats["mean_bytes"],
        std_bytes=stats["std_bytes"],
        mean_denied=stats["mean_denied"],
        mean_sensitive=stats["mean_sensitive"],
        mean_admin=stats["mean_admin"],
    )
    return AnomalyModel(stats=model_stats, threshold=payload["threshold"])
