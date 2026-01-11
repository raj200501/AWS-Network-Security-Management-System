"""KMS key simulator.

This simulator supports envelope encryption with a trivial XOR cipher to keep
behavior deterministic without external dependencies. It tracks key usage and
rotation metadata.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass(frozen=True)
class KeyMetadata:
    key_id: str
    alias: str
    created_at: datetime
    enabled: bool
    rotation_enabled: bool


class KmsKey:
    """Represents a simplified KMS key."""

    def __init__(self, key_id: str, alias: str) -> None:
        self.metadata = KeyMetadata(
            key_id=key_id,
            alias=alias,
            created_at=datetime.utcnow(),
            enabled=True,
            rotation_enabled=False,
        )
        self._usage_count = 0

    def enable(self) -> None:
        self.metadata = KeyMetadata(
            key_id=self.metadata.key_id,
            alias=self.metadata.alias,
            created_at=self.metadata.created_at,
            enabled=True,
            rotation_enabled=self.metadata.rotation_enabled,
        )

    def disable(self) -> None:
        self.metadata = KeyMetadata(
            key_id=self.metadata.key_id,
            alias=self.metadata.alias,
            created_at=self.metadata.created_at,
            enabled=False,
            rotation_enabled=self.metadata.rotation_enabled,
        )

    def enable_rotation(self) -> None:
        self.metadata = KeyMetadata(
            key_id=self.metadata.key_id,
            alias=self.metadata.alias,
            created_at=self.metadata.created_at,
            enabled=self.metadata.enabled,
            rotation_enabled=True,
        )

    def encrypt(self, plaintext: bytes, encryption_context: Dict[str, str]) -> bytes:
        self._ensure_enabled()
        self._usage_count += 1
        key = _context_key(encryption_context)
        return _xor(plaintext, key)

    def decrypt(self, ciphertext: bytes, encryption_context: Dict[str, str]) -> bytes:
        self._ensure_enabled()
        self._usage_count += 1
        key = _context_key(encryption_context)
        return _xor(ciphertext, key)

    def usage_count(self) -> int:
        return self._usage_count

    def _ensure_enabled(self) -> None:
        if not self.metadata.enabled:
            raise PermissionError("KMS key is disabled")


def _context_key(context: Dict[str, str]) -> bytes:
    joined = "|".join(f"{key}={value}" for key, value in sorted(context.items()))
    return joined.encode("utf-8") or b"default"


def _xor(data: bytes, key: bytes) -> bytes:
    return bytes(byte ^ key[idx % len(key)] for idx, byte in enumerate(data))
