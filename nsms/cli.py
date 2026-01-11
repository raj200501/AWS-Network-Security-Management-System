"""Command line interface for the NSMS pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from nsms.config import Config
from nsms.logging_utils import setup_logging
from nsms.monitoring import run_pipeline, train_model


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local NSMS pipeline")
    parser.add_argument("--config", type=Path, help="Path to config JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("train", help="Train the anomaly model")
    subparsers.add_parser("run", help="Run the monitoring pipeline")
    subparsers.add_parser("show-config", help="Print the effective configuration")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    config = Config.load(args.config)
    setup_logging(config.output_dir)

    if args.command == "train":
        train_model(config)
        return 0
    if args.command == "run":
        run_pipeline(config)
        return 0
    if args.command == "show-config":
        print(json.dumps(config.__dict__, default=str, indent=2))
        return 0
    parser.error("Unknown command")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
