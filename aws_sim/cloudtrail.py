"""CloudTrail event recorder simulator.

Records events emitted by the simulated services. Each event captures metadata
that mirrors CloudTrail's shape, enabling deterministic auditing in tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


@dataclass(frozen=True)
class CloudTrailEvent:
    event_id: str
    event_name: str
    event_time: datetime
    user_identity: str
    source_ip: str
    resource: str
    request_parameters: Dict[str, str]
    response_elements: Dict[str, str]


class CloudTrailRecorder:
    """In-memory recorder for CloudTrail-like events."""

    def __init__(self) -> None:
        self._events: List[CloudTrailEvent] = []
        self._counter = 0

    def record(
        self,
        event_name: str,
        user_identity: str,
        source_ip: str,
        resource: str,
        request_parameters: Dict[str, str] | None = None,
        response_elements: Dict[str, str] | None = None,
    ) -> CloudTrailEvent:
        self._counter += 1
        event = CloudTrailEvent(
            event_id=f"evt-{self._counter:06d}",
            event_name=event_name,
            event_time=datetime.utcnow(),
            user_identity=user_identity,
            source_ip=source_ip,
            resource=resource,
            request_parameters=request_parameters or {},
            response_elements=response_elements or {},
        )
        self._events.append(event)
        return event

    def list_events(self) -> List[CloudTrailEvent]:
        return list(self._events)

    def filter_by_event_name(self, event_name: str) -> List[CloudTrailEvent]:
        return [event for event in self._events if event.event_name == event_name]
