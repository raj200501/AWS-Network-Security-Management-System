"""Simplified DynamoDB table simulator.

The simulator supports put/get/update/delete operations with a single string
partition key. It includes lightweight conditional checks and metrics that help
validate workflows in unit tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class DynamoItem:
    key: str
    attributes: Dict[str, Any]
    updated_at: datetime


class DynamoTable:
    """In-memory DynamoDB table."""

    def __init__(self, name: str, partition_key: str) -> None:
        self.name = name
        self.partition_key = partition_key
        self._items: Dict[str, DynamoItem] = {}
        self._writes = 0
        self._reads = 0

    def put_item(self, item: Dict[str, Any]) -> DynamoItem:
        if self.partition_key not in item:
            raise KeyError(f"Missing partition key {self.partition_key}")
        key = str(item[self.partition_key])
        dynamo_item = DynamoItem(key=key, attributes=dict(item), updated_at=datetime.utcnow())
        self._items[key] = dynamo_item
        self._writes += 1
        return dynamo_item

    def get_item(self, key: str) -> Optional[DynamoItem]:
        self._reads += 1
        return self._items.get(key)

    def delete_item(self, key: str) -> bool:
        if key in self._items:
            del self._items[key]
            self._writes += 1
            return True
        return False

    def update_item(self, key: str, updates: Dict[str, Any]) -> DynamoItem:
        existing = self._items.get(key)
        if existing is None:
            raise KeyError(f"Item not found: {key}")
        attributes = dict(existing.attributes)
        attributes.update(updates)
        updated = DynamoItem(key=key, attributes=attributes, updated_at=datetime.utcnow())
        self._items[key] = updated
        self._writes += 1
        return updated

    def scan(self) -> List[DynamoItem]:
        self._reads += len(self._items)
        return list(self._items.values())

    def metrics(self) -> Dict[str, int]:
        return {"reads": self._reads, "writes": self._writes, "count": len(self._items)}
