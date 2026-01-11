"""Kinesis Data Firehose simulator.

Consumes records and delivers them to an S3 bucket in batches. It is used to
model log delivery pipelines without external dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

from aws_sim.s3 import S3Bucket


@dataclass(frozen=True)
class FirehoseRecord:
    record_id: str
    data: bytes
    received_at: datetime


class FirehoseDeliveryStream:
    def __init__(self, name: str, bucket: S3Bucket, prefix: str = "") -> None:
        self.name = name
        self.bucket = bucket
        self.prefix = prefix
        self._buffer: List[FirehoseRecord] = []
        self._counter = 0

    def put_record(self, data: bytes) -> FirehoseRecord:
        self._counter += 1
        record = FirehoseRecord(
            record_id=f"fh-{self._counter:06d}",
            data=data,
            received_at=datetime.utcnow(),
        )
        self._buffer.append(record)
        return record

    def flush(self) -> List[str]:
        """Flush buffered records to S3 and return object keys."""

        if not self._buffer:
            return []
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        key = f"{self.prefix}firehose-{timestamp}.log"
        payload = b"\n".join(record.data for record in self._buffer)
        self.bucket.put_object(key, payload, content_type="text/plain")
        self._buffer.clear()
        return [key]
