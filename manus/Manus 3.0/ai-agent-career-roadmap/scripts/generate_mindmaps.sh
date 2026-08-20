#!/usr/bin/env bash
# Render Mermaid tutorial sources to PNG and SVG wrappers.
# Usage: bash scripts/generate_mindmaps.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 scripts/generate_mindmaps.py
