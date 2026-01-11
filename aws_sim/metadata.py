"""Metadata helpers for AWS-like resources."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass(frozen=True)
class ResourceTags:
    tags: Dict[str, str]

    def merged(self, extra: Dict[str, str]) -> "ResourceTags":
        combined = dict(self.tags)
        combined.update(extra)
        return ResourceTags(tags=combined)


@dataclass(frozen=True)
class ResourceMetadata:
    resource_id: str
    resource_type: str
    region: str
    created_at: datetime
    tags: ResourceTags

    def with_tags(self, tags: Dict[str, str]) -> "ResourceMetadata":
        return ResourceMetadata(
            resource_id=self.resource_id,
            resource_type=self.resource_type,
            region=self.region,
            created_at=self.created_at,
            tags=self.tags.merged(tags),
        )
