#!/usr/bin/env bash
# Generate all requested PDFs from Markdown sources.
# Usage: bash scripts/generate_pdfs.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 scripts/pdf_from_markdown.py --all
python3 scripts/build_book.py
python3 scripts/build_book_pdf.py
python3 scripts/build_auxiliary_pdfs.py
python3 scripts/check_files.py --require-pdfs
