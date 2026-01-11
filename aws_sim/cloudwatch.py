"""CloudWatch metrics and alarm simulator.

Provides a minimal in-memory store for metrics and a basic alarm evaluation
engine. Designed for deterministic unit tests and local examples.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass(frozen=True)
class MetricDatum:
    namespace: str
    metric_name: str
    value: float
    unit: str
    timestamp: datetime


@dataclass(frozen=True)
class AlarmState:
    name: str
    state: str
    reason: str
    updated_at: datetime


class CloudWatchMetrics:
    def __init__(self) -> None:
        self._metrics: List[MetricDatum] = []

    def put_metric_data(self, namespace: str, metric_name: str, value: float, unit: str = "Count") -> MetricDatum:
        datum = MetricDatum(
            namespace=namespace,
            metric_name=metric_name,
            value=value,
            unit=unit,
            timestamp=datetime.utcnow(),
        )
        self._metrics.append(datum)
        return datum

    def list_metrics(self, namespace: Optional[str] = None) -> List[MetricDatum]:
        if namespace:
            return [metric for metric in self._metrics if metric.namespace == namespace]
        return list(self._metrics)

    def get_latest_metric(self, namespace: str, metric_name: str) -> Optional[MetricDatum]:
        candidates = [
            metric
            for metric in self._metrics
            if metric.namespace == namespace and metric.metric_name == metric_name
        ]
        if not candidates:
            return None
        return sorted(candidates, key=lambda m: m.timestamp)[-1]


class CloudWatchAlarm:
    """Simple alarm that checks a metric against a threshold."""

    def __init__(
        self,
        name: str,
        namespace: str,
        metric_name: str,
        threshold: float,
        comparison_operator: str = ">=",
    ) -> None:
        self.name = name
        self.namespace = namespace
        self.metric_name = metric_name
        self.threshold = threshold
        self.comparison_operator = comparison_operator
        self._state = AlarmState(name=name, state="INSUFFICIENT_DATA", reason="No data", updated_at=datetime.utcnow())

    def evaluate(self, metrics: CloudWatchMetrics) -> AlarmState:
        latest = metrics.get_latest_metric(self.namespace, self.metric_name)
        if latest is None:
            self._state = AlarmState(
                name=self.name,
                state="INSUFFICIENT_DATA",
                reason="No metric data",
                updated_at=datetime.utcnow(),
            )
            return self._state
        comparison = _compare(latest.value, self.threshold, self.comparison_operator)
        state = "ALARM" if comparison else "OK"
        reason = f"Latest value {latest.value} {self.comparison_operator} {self.threshold}"
        self._state = AlarmState(name=self.name, state=state, reason=reason, updated_at=datetime.utcnow())
        return self._state

    def state(self) -> AlarmState:
        return self._state


def _compare(value: float, threshold: float, operator: str) -> bool:
    if operator == ">=":
        return value >= threshold
    if operator == ">":
        return value > threshold
    if operator == "<=":
        return value <= threshold
    if operator == "<":
        return value < threshold
    raise ValueError(f"Unsupported comparison operator: {operator}")
