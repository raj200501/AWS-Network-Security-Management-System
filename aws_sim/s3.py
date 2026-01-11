"""S3 bucket simulator with basic object storage semantics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass(frozen=True)
class S3Object:
    key: str
    data: bytes
    content_type: str
    updated_at: datetime


class S3Bucket:
    """In-memory S3 bucket with simple CRUD operations."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._objects: Dict[str, S3Object] = {}
        self._put_requests = 0
        self._get_requests = 0

    def put_object(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> S3Object:
        obj = S3Object(key=key, data=data, content_type=content_type, updated_at=datetime.utcnow())
        self._objects[key] = obj
        self._put_requests += 1
        return obj

    def get_object(self, key: str) -> Optional[S3Object]:
        self._get_requests += 1
        return self._objects.get(key)

    def delete_object(self, key: str) -> bool:
        if key in self._objects:
            del self._objects[key]
            return True
        return False

    def list_objects(self, prefix: str = "") -> List[S3Object]:
        return [obj for key, obj in self._objects.items() if key.startswith(prefix)]

    def metrics(self) -> Dict[str, int]:
        return {
            "put_requests": self._put_requests,
            "get_requests": self._get_requests,
            "object_count": len(self._objects),
        }
