# Build the full offline tutorial book from Markdown sources.
# Usage: powershell -ExecutionPolicy Bypass -File scripts/build_book.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python scripts/upgrade_tutorial.py
python scripts/generate_plan_artifacts.py
python scripts/generate_mindmaps.py
python scripts/build_book.py
python scripts/build_book_pdf.py
python scripts/build_auxiliary_pdfs.py
python scripts/check_files.py --require-pdfs
python scripts/create_output_reports.py
Write-Host "Book build complete: output/book/ai-agent-career-roadmap.html"
