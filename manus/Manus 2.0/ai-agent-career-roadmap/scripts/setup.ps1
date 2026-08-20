# Initialize a local Python environment for the learning system.
# Usage: powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
py -3 --version
py -3 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python generate_files.py
python scripts/check_files.py
Write-Host "Setup complete. Start with: weeks/week-01/days/day-01.md"
