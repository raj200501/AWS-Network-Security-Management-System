#!/usr/bin/env bash
set -euo pipefail

python -m nsms.cli train
python -m nsms.cli run

python -m unittest discover -s tests
python scripts/smoke_test.py
