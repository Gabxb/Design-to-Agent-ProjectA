#!/usr/bin/env bash
# Generate all required PDFs from Markdown source.
# Requires Typst. Usage: bash scripts/generate_pdfs.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 scripts/pdf_from_markdown.py --all
python3 scripts/check_files.py --require-pdfs
