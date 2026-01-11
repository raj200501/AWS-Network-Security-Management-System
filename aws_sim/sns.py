"""SNS topic and subscription simulator."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Dict, List


Subscriber = Callable[["SnsMessage"], None]


@dataclass(frozen=True)
class SnsMessage:
    message_id: str
    topic_arn: str
    subject: str
    body: str
    published_at: datetime


class SnsTopic:
    """In-memory SNS topic."""

    def __init__(self, arn: str) -> None:
        self.arn = arn
        self._subscribers: List[Subscriber] = []
        self._messages: List[SnsMessage] = []
        self._counter = 0

    def subscribe(self, handler: Subscriber) -> None:
        self._subscribers.append(handler)

    def publish(self, subject: str, body: str) -> SnsMessage:
        self._counter += 1
        message = SnsMessage(
            message_id=f"msg-{self._counter:06d}",
            topic_arn=self.arn,
            subject=subject,
            body=body,
            published_at=datetime.utcnow(),
        )
        self._messages.append(message)
        for subscriber in self._subscribers:
            subscriber(message)
        return message

    def list_messages(self) -> List[SnsMessage]:
        return list(self._messages)

    def subscriber_count(self) -> int:
        return len(self._subscribers)
