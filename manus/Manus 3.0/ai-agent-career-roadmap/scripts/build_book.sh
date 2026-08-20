#!/usr/bin/env bash
# Build the full offline tutorial book from Markdown sources.
# Usage: bash scripts/build_book.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 scripts/upgrade_tutorial.py
python3 scripts/generate_plan_artifacts.py
python3 scripts/generate_mindmaps.py
python3 scripts/build_book.py
python3 scripts/build_book_pdf.py
python3 scripts/build_auxiliary_pdfs.py
python3 scripts/check_files.py --require-pdfs
python3 scripts/create_output_reports.py
echo "Book build complete: output/book/ai-agent-career-roadmap.html"
