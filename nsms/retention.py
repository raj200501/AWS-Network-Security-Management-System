"""Retention utilities for NSMS outputs."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

from nsms.logging_utils import get_logger


logger = get_logger("retention")


def enforce_retention(output_dir: Path, retention_days: int) -> int:
    """Remove files older than retention_days and return count removed."""

    cutoff = datetime.utcnow() - timedelta(days=retention_days)
    removed = 0
    for path in _iter_output_files(output_dir):
        if datetime.utcfromtimestamp(path.stat().st_mtime) < cutoff:
            path.unlink()
            removed += 1
    if removed:
        logger.info("Retention removed %s files", removed)
    return removed


def _iter_output_files(output_dir: Path) -> Iterable[Path]:
    if not output_dir.exists():
        return []
    return [path for path in output_dir.iterdir() if path.is_file()]
