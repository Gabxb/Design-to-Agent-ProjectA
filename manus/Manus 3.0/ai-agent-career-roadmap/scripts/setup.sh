#!/usr/bin/env bash
# Initialize a local Python environment and build the tutorial book.
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
python generate_book.py
python scripts/check_files.py --require-pdfs
echo "Setup complete. Open: output/book/ai-agent-career-roadmap.html"
