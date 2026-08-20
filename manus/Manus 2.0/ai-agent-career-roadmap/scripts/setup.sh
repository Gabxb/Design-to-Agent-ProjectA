#!/usr/bin/env bash
# Initialize a local Python environment for the learning system.
# Usage: bash scripts/setup.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 --version
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python generate_files.py
python scripts/check_files.py
echo "Setup complete. Start with: weeks/week-01/days/day-01.md"
