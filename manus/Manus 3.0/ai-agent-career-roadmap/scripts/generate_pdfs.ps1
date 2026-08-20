# Generate all requested PDFs from Markdown sources.
# Usage: powershell -ExecutionPolicy Bypass -File scripts/generate_pdfs.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python scripts/pdf_from_markdown.py --all
python scripts/build_book.py
python scripts/build_book_pdf.py
python scripts/build_auxiliary_pdfs.py
python scripts/check_files.py --require-pdfs
