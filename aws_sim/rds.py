"""RDS simulator.

Models database instances and snapshots to allow local workflows to test
backup, restore, and tagging logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


@dataclass(frozen=True)
class DbInstance:
    db_instance_id: str
    engine: str
    status: str
    created_at: datetime


@dataclass(frozen=True)
class DbSnapshot:
    snapshot_id: str
    db_instance_id: str
    created_at: datetime


class RdsService:
    def __init__(self) -> None:
        self._instances: Dict[str, DbInstance] = {}
        self._snapshots: Dict[str, DbSnapshot] = {}
        self._counter = 0

    def create_instance(self, db_instance_id: str, engine: str) -> DbInstance:
        instance = DbInstance(
            db_instance_id=db_instance_id,
            engine=engine,
            status="available",
            created_at=datetime.utcnow(),
        )
        self._instances[db_instance_id] = instance
        return instance

    def create_snapshot(self, db_instance_id: str) -> DbSnapshot:
        if db_instance_id not in self._instances:
            raise KeyError("Instance not found")
        self._counter += 1
        snapshot = DbSnapshot(
            snapshot_id=f"snapshot-{self._counter:04d}",
            db_instance_id=db_instance_id,
            created_at=datetime.utcnow(),
        )
        self._snapshots[snapshot.snapshot_id] = snapshot
        return snapshot

    def list_instances(self) -> List[DbInstance]:
        return list(self._instances.values())

    def list_snapshots(self) -> List[DbSnapshot]:
        return list(self._snapshots.values())
