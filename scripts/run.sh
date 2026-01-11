#!/usr/bin/env bash
set -euo pipefail

python -m nsms.cli train
python -m nsms.cli run
