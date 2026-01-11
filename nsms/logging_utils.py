"""Logging utilities for NSMS."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional


DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def setup_logging(log_dir: Optional[Path] = None, level: int = logging.INFO) -> None:
    """Configure root logging with optional file output."""

    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "nsms.log")
        handlers.append(file_handler)

    logging.basicConfig(level=level, format=DEFAULT_LOG_FORMAT, handlers=handlers)


def get_logger(name: str) -> logging.Logger:
    """Return a logger with a consistent namespace."""

    return logging.getLogger(f"nsms.{name}")
