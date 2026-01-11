"""In-memory Kinesis stream simulator.

The simulator models a single stream with multiple shards. Records are stored
in order and can be iterated with shard and sequence tracking, similar to the
Kinesis APIs used by Lambda and analytics jobs.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class KinesisRecord:
    sequence_number: str
    partition_key: str
    data: bytes
    approximate_arrival_timestamp: datetime


class KinesisShard:
    """Represents a shard and its ordered records."""

    def __init__(self, shard_id: str) -> None:
        self.shard_id = shard_id
        self._records: List[KinesisRecord] = []

    def put_record(self, record: KinesisRecord) -> None:
        self._records.append(record)

    def get_records(self, start: int = 0, limit: int = 100) -> List[KinesisRecord]:
        return self._records[start : start + limit]

    def record_count(self) -> int:
        return len(self._records)


class KinesisStream:
    """Minimal Kinesis stream implementation.

    The stream distributes records to shards based on a naive hash of the
    partition key. Sequence numbers are monotonic per shard.
    """

    def __init__(self, name: str, shard_count: int = 1) -> None:
        if shard_count <= 0:
            raise ValueError("shard_count must be >= 1")
        self.name = name
        self._shards: Dict[str, KinesisShard] = {
            f"shard-{idx:04d}": KinesisShard(f"shard-{idx:04d}")
            for idx in range(shard_count)
        }
        self._sequence_counters: Dict[str, int] = {shard_id: 0 for shard_id in self._shards}

    def _select_shard(self, partition_key: str) -> KinesisShard:
        shard_ids = sorted(self._shards.keys())
        index = hash(partition_key) % len(shard_ids)
        return self._shards[shard_ids[index]]

    def put_record(self, partition_key: str, data: bytes) -> KinesisRecord:
        shard = self._select_shard(partition_key)
        sequence_number = self._next_sequence(shard.shard_id)
        record = KinesisRecord(
            sequence_number=sequence_number,
            partition_key=partition_key,
            data=data,
            approximate_arrival_timestamp=datetime.utcnow(),
        )
        shard.put_record(record)
        return record

    def put_records(self, records: Iterable[tuple[str, bytes]]) -> List[KinesisRecord]:
        return [self.put_record(partition_key, data) for partition_key, data in records]

    def get_shard_iterator(self, shard_id: str) -> int:
        if shard_id not in self._shards:
            raise KeyError(f"Unknown shard_id: {shard_id}")
        return 0

    def get_records(self, shard_id: str, iterator: int, limit: int = 100) -> tuple[List[KinesisRecord], int]:
        shard = self._shards.get(shard_id)
        if shard is None:
            raise KeyError(f"Unknown shard_id: {shard_id}")
        records = shard.get_records(start=iterator, limit=limit)
        next_iterator = iterator + len(records)
        return records, next_iterator

    def list_shards(self) -> List[str]:
        return list(self._shards.keys())

    def total_records(self) -> int:
        return sum(shard.record_count() for shard in self._shards.values())

    def _next_sequence(self, shard_id: str) -> str:
        self._sequence_counters[shard_id] += 1
        return f"{shard_id}-{self._sequence_counters[shard_id]:010d}"
