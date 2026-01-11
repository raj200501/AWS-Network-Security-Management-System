"""Feature extraction and preprocessing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from nsms.data import LogRecord


@dataclass(frozen=True)
class FeatureVector:
    bytes_transferred: float
    is_denied: int
    is_sensitive_resource: int
    is_admin_user: int


def extract_features(records: Iterable[LogRecord]) -> List[FeatureVector]:
    """Extract numeric feature vectors from log records."""

    features: List[FeatureVector] = []
    for record in records:
        features.append(
            FeatureVector(
                bytes_transferred=float(record.bytes_transferred),
                is_denied=1 if record.status.lower() != "ok" else 0,
                is_sensitive_resource=1 if "sensitive" in record.resource else 0,
                is_admin_user=1 if record.user.lower().startswith("admin") else 0,
            )
        )
    return features
