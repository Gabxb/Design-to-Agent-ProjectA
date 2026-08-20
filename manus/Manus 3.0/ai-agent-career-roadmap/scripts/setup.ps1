# Initialize a local Python environment and build the tutorial book.
# Usage: powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
py -3 --version
py -3 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python generate_book.py
python scripts/check_files.py --require-pdfs
Write-Host "Setup complete. Open: output/book/ai-agent-career-roadmap.html"
