"""STS session token simulator.

Provides a minimal API to assume roles and issue session credentials. Tokens
are deterministic for testing and include expiration timestamps.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class SessionCredentials:
    access_key_id: str
    secret_access_key: str
    session_token: str
    expiration: datetime


class StsService:
    def __init__(self) -> None:
        self._counter = 0

    def assume_role(self, role_arn: str, session_name: str, duration_seconds: int = 3600) -> SessionCredentials:
        self._counter += 1
        expiration = datetime.utcnow() + timedelta(seconds=duration_seconds)
        return SessionCredentials(
            access_key_id=f"ASIA{self._counter:08d}",
            secret_access_key=f"secret-{self._counter:08d}",
            session_token=f"token-{session_name}-{self._counter:08d}",
            expiration=expiration,
        )
