# Generate all required PDFs from Markdown source.
# Requires Typst. Usage: powershell -ExecutionPolicy Bypass -File scripts/generate_pdfs.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python scripts/pdf_from_markdown.py --all
python scripts/check_files.py --require-pdfs
