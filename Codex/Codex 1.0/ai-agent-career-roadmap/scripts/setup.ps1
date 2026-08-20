$ErrorActionPreference = "Stop"
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python generate_files.py
Write-Host "完成。请打开 START_HERE.md"
