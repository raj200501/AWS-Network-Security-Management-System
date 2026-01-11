"""Anomaly detection model implementation."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Iterable, List

from nsms.preprocessing import FeatureVector


@dataclass(frozen=True)
class ModelStats:
    mean_bytes: float
    std_bytes: float
    mean_denied: float
    mean_sensitive: float
    mean_admin: float


class AnomalyModel:
    """Simple statistical anomaly detector.

    The model flags a record as anomalous if the bytes transferred exceed
    ``mean + threshold * std`` or if the record is a denied request to a
    sensitive resource performed by an admin.
    """

    def __init__(self, stats: ModelStats, threshold: float = 3.0) -> None:
        self.stats = stats
        self.threshold = threshold

    @classmethod
    def train(cls, features: Iterable[FeatureVector], threshold: float = 3.0) -> "AnomalyModel":
        feature_list = list(features)
        if not feature_list:
            raise ValueError("Cannot train anomaly model with empty dataset")
        bytes_values = [feature.bytes_transferred for feature in feature_list]
        denied_values = [feature.is_denied for feature in feature_list]
        sensitive_values = [feature.is_sensitive_resource for feature in feature_list]
        admin_values = [feature.is_admin_user for feature in feature_list]
        stats = ModelStats(
            mean_bytes=mean(bytes_values),
            std_bytes=pstdev(bytes_values) or 1.0,
            mean_denied=mean(denied_values),
            mean_sensitive=mean(sensitive_values),
            mean_admin=mean(admin_values),
        )
        return cls(stats=stats, threshold=threshold)

    def score(self, feature: FeatureVector) -> float:
        deviation = (feature.bytes_transferred - self.stats.mean_bytes) / self.stats.std_bytes
        penalty = 0.0
        if feature.is_denied:
            penalty += 0.5
        if feature.is_sensitive_resource:
            penalty += 0.75
        if feature.is_admin_user:
            penalty += 0.5
        return deviation + penalty

    def is_anomalous(self, feature: FeatureVector) -> bool:
        if (
            feature.is_denied
            and feature.is_sensitive_resource
            and feature.is_admin_user
        ):
            return True
        return self.score(feature) >= self.threshold

    def predict(self, features: Iterable[FeatureVector]) -> List[bool]:
        return [self.is_anomalous(feature) for feature in features]
